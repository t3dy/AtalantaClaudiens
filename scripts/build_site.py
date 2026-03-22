"""
build_site.py — Generate static HTML site from SQLite database.

Stage 4: Reads db/atalanta.db, generates:
  - site/index.html (gallery home)
  - site/data.json (gallery data for JS)
  - site/emblems/emblem-NN.html (51 emblem detail pages)
  - site/about.html
"""

import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "atalanta.db"
SITE_DIR = BASE_DIR / "site"


def load_identity_map(conn):
    """Load emblem_identity table into a dict keyed by emblem_number.

    Returns {emblem_number: {'image_filename': str|None, 'alignment_confidence': str|None, ...}}
    All image rendering must flow through this map — no hardcoded filename assumptions.
    """
    rows = conn.execute("""
        SELECT emblem_number, roman_label, image_filename,
               image_source, alignment_confidence
        FROM emblem_identity
        ORDER BY emblem_number
    """).fetchall()
    identity = {}
    for r in rows:
        identity[r[0]] = {
            'image_filename': r[2],
            'image_source': r[3],
            'alignment_confidence': r[4],
        }
    return identity


def resolve_image(identity_map, emblem_number):
    """Resolve image path for an emblem via the identity layer.

    Returns (relative_path, exists) tuple. Returns (None, False) if no image mapped.
    """
    entry = identity_map.get(emblem_number)
    if not entry or not entry['image_filename']:
        return None, False
    rel_path = f"images/emblems/{entry['image_filename']}"
    exists = (SITE_DIR / rel_path).exists()
    return rel_path, exists

ROMAN_MAP = [
    (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
    (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
    (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
]

def int_to_roman(n):
    if n <= 0: return None
    result = []
    for value, numeral in ROMAN_MAP:
        while n >= value:
            result.append(numeral)
            n -= value
    return ''.join(result)

def slugify(text):
    return text.lower().replace(' ', '-').replace('/', '-')


# ============================================================
# Page Shell
# ============================================================

NAV_ITEMS = [
    ('Home', 'index.html'),
    ('Emblems', 'emblems/index.html'),
    ('Scholars', 'scholars.html'),
    ('Dictionary', 'dictionary/index.html'),
    ('Timeline', 'timeline.html'),
    ('Sources', 'sources.html'),
    ('Maier', 'maier.html'),
    ('Music', 'music.html'),
    ('Works', 'works.html'),
    ('Szulakowska', 'szulakowska.html'),
    ('Essays', 'essays/index.html'),
    ('Bibliography', 'bibliography.html'),
    ('Biography', 'biography.html'),
    ('About', 'about.html'),
]

def nav_html(active='', prefix=''):
    links = []
    for label, href in NAV_ITEMS:
        cls = ' class="active"' if label == active else ''
        links.append(f'<a href="{prefix}{href}"{cls}>{label}</a>')
    return '\n            '.join(links)

def page_shell(title, body, active_nav='', depth=0):
    prefix = '../' * depth
    css_path = f'{prefix}style.css'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — Atalanta Fugiens</title>
    <link rel="stylesheet" href="{css_path}">
</head>
<body>
    <header>
        <div class="header-content">
            <h1><em>Atalanta Fugiens</em></h1>
            <div class="subtitle">The Scholarship of H.M.E. De Jong on Michael Maier's Alchemical Emblems</div>
            <nav class="site-nav">
                {nav_html(active_nav, prefix)}
            </nav>
        </div>
    </header>
    {body}
    <footer>
        <p>AtalantaClaudiens &middot; A digital humanities project &middot;
        <a href="https://github.com/t3dy/AtalantaClaudiens">GitHub</a></p>
    </footer>
</body>
</html>"""


def autolink_emblems(text):
    """Convert 'Emblem XXIV', 'Emblem 24', 'Emblems XXIV and XXV' references into clickable links."""
    if not text:
        return text
    import re
    roman_map = {'I':1,'II':2,'III':3,'IV':4,'V':5,'VI':6,'VII':7,'VIII':8,'IX':9,'X':10,
                 'XI':11,'XII':12,'XIII':13,'XIV':14,'XV':15,'XVI':16,'XVII':17,'XVIII':18,
                 'XIX':19,'XX':20,'XXI':21,'XXII':22,'XXIII':23,'XXIV':24,'XXV':25,'XXVI':26,
                 'XXVII':27,'XXVIII':28,'XXIX':29,'XXX':30,'XXXI':31,'XXXII':32,'XXXIII':33,
                 'XXXIV':34,'XXXV':35,'XXXVI':36,'XXXVII':37,'XXXVIII':38,'XXXIX':39,'XL':40,
                 'XLI':41,'XLII':42,'XLIII':43,'XLIV':44,'XLV':45,'XLVI':46,'XLVII':47,
                 'XLVIII':48,'XLIX':49,'L':50}
    def replace_roman(m):
        roman = m.group(1)
        num = roman_map.get(roman)
        if num is not None:
            return f'<a href="../emblems/emblem-{num:02d}.html" class="cross-link">Emblem {roman}</a>'
        return m.group(0)
    def replace_arabic(m):
        num = int(m.group(1))
        if 0 <= num <= 50:
            href = f'emblem-{num:02d}.html' if num > 0 else 'frontispiece.html'
            return f'<a href="../emblems/{href}" class="cross-link">Emblem {num}</a>'
        return m.group(0)
    # Match "Emblem XXIV" (roman), longest match first
    text = re.sub(r'Emblem\s+(XLVIII|XXXVIII|XXXIII|XXVIII|XXIII|XVIII|XLVII|XXXVII|XXXIV|XXXII|XXVII|XXXIX|XXXVI|XXXV|XXVI|XXIV|XXII|XVII|XLVI|XLIV|XLIII|XLII|XIII|XXXI|XXIX|XVI|XLV|XLI|XII|XXX|XIV|XXV|XIX|XV|XXI|XX|XI|IX|XL|IV|VI|II|VIII|VII|III|XLIX|I|V|X|L)',
                  replace_roman, text)
    # Match "Emblem 24" (arabic)
    text = re.sub(r'Emblem\s+(\d{1,2})(?=[^0-9]|$)', replace_arabic, text)
    return text


def format_paragraphs(text):
    """Convert \\n\\n-separated text into HTML paragraphs."""
    if not text:
        return ''
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    html = ''.join(f'<p style="font-size:0.95rem;line-height:1.7;margin-bottom:1rem">{p}</p>' for p in paragraphs)
    return f'<div style="margin-bottom:1.5rem">{html}</div>'


def confidence_badge(level):
    if not level: return ''
    cls = f'confidence-{level.lower()}'
    return f'<span class="badge {cls}">{level}</span>'


def build_registers_html(registers_json):
    """Build HTML for multi-register definitions (alchemical, medical, spiritual, cosmological)."""
    if not registers_json:
        return ''
    import json
    try:
        regs = json.loads(registers_json)
    except (json.JSONDecodeError, TypeError):
        return ''
    if not any(regs.get(k) for k in ('alchemical', 'medical', 'spiritual', 'cosmological')):
        return ''

    reg_labels = {
        'alchemical': ('Alchemical', '#8b4513'),
        'medical': ('Medical', '#2980b9'),
        'spiritual': ('Spiritual', '#6c3483'),
        'cosmological': ('Cosmological', '#1a5276'),
    }
    items = ''
    for key, (display, color) in reg_labels.items():
        val = regs.get(key)
        if val:
            items += f'''
                <div style="margin-bottom:0.8rem;padding-left:1rem;border-left:3px solid {color}">
                    <dt style="font-weight:600;font-size:0.85rem;color:{color};font-family:var(--font-sans);margin-bottom:0.2rem">{display}</dt>
                    <dd style="margin:0;font-size:0.92rem;line-height:1.6">{val}</dd>
                </div>'''
    return f'''
            <div style="margin-bottom:1.5rem">
                <h2>Meanings Across Registers</h2>
                <p style="font-size:0.85rem;color:var(--text-muted);margin-bottom:1rem">
                    De Jong shows that alchemical terms operate simultaneously across material, medical, spiritual, and cosmological dimensions.
                </p>
                <dl style="margin:0">{items}</dl>
            </div>'''


# ============================================================
# Data Export
# ============================================================

def export_data_json(conn, identity_map):
    rows = conn.execute("""
        SELECT e.number, e.roman_numeral, e.canonical_label,
               e.motto_english, e.discourse_summary, e.confidence
        FROM emblems e ORDER BY e.number
    """).fetchall()

    entries = []
    for r in rows:
        num = r[0]
        page = 'frontispiece.html' if num == 0 else f'emblem-{num:02d}.html'
        img_path, img_exists = resolve_image(identity_map, num)
        entries.append({
            'number': num,
            'roman': r[1],
            'label': r[2],
            'motto': r[3],
            'discourse': r[4],
            'confidence': r[5],
            'page': page,
            'image': img_path if img_exists else None,
        })

    stats = {
        'total_emblems': len([e for e in entries if e['number'] > 0]),
        'with_motto': len([e for e in entries if e['motto']]),
        'scholarly_refs': conn.execute("SELECT COUNT(*) FROM scholarly_refs").fetchone()[0],
        'source_links': conn.execute("SELECT COUNT(*) FROM emblem_sources").fetchone()[0],
    }

    data = {'entries': entries, 'stats': stats}
    out = SITE_DIR / 'data.json'
    out.write_text(json.dumps(data, indent=2), encoding='utf-8')
    print(f"  data.json: {len(entries)} entries")


# ============================================================
# Gallery Home
# ============================================================

def build_gallery(conn):
    stats = conn.execute("SELECT COUNT(*) FROM emblems WHERE number > 0").fetchone()[0]
    terms = conn.execute("SELECT COUNT(*) FROM dictionary_terms").fetchone()[0]
    sources = conn.execute("SELECT COUNT(*) FROM source_authorities").fetchone()[0]
    body = f"""
    <div style="max-width:700px;margin:2rem auto;padding:0 2rem;text-align:center">
        <p style="font-size:1.05rem;line-height:1.8;color:var(--text)">In 1617, the physician and alchemist Michael Maier published fifty emblems combining engraved plates, Latin mottos, poetic epigrams, philosophical discourses, and three-voice musical fugues &mdash; a work without parallel in the history of the emblem book. In 1969, the Dutch art historian H.M.E. De Jong unlocked these emblems by tracing each one to its ancient and medieval sources. This site presents her findings.</p>
        <div style="margin-top:1.5rem">
            <a href="emblems/frontispiece.html" style="display:inline-block;padding:0.6rem 1.5rem;background:var(--accent);color:white;text-decoration:none;border-radius:4px;font-family:var(--font-sans);font-size:0.9rem">Start with the Frontispiece &rarr;</a>
        </div>
    </div>
    <div class="stats" id="stats"></div>
    <div class="gallery" id="gallery"></div>
    <div class="lightbox" id="lightbox">
        <button class="lightbox-close" onclick="closeLightbox()">&times;</button>
        <button class="lightbox-nav lightbox-prev" onclick="navigateLightbox(-1)">&lsaquo;</button>
        <button class="lightbox-nav lightbox-next" onclick="navigateLightbox(1)">&rsaquo;</button>
        <div class="lightbox-content">
            <div class="lightbox-details"></div>
        </div>
    </div>
    <script src="script.js"></script>"""

    html = page_shell("Emblem Gallery", body, active_nav='Home')
    (SITE_DIR / 'index.html').write_text(html, encoding='utf-8')
    print(f"  index.html")


# ============================================================
# Emblem Detail Pages
# ============================================================

def build_emblem_pages(conn, identity_map):
    emblems_dir = SITE_DIR / 'emblems'
    emblems_dir.mkdir(exist_ok=True)

    emblems = conn.execute("""
        SELECT id, number, roman_numeral, canonical_label,
               motto_latin, motto_english, epigram_english,
               discourse_summary, image_description,
               alchemical_stage, confidence, analysis_html
        FROM emblems ORDER BY number
    """).fetchall()

    for i, e in enumerate(emblems):
        eid, num, roman, label = e[0], e[1], e[2], e[3]
        motto_lat, motto_en, epigram = e[4], e[5], e[6]
        discourse, img_desc, stage, conf = e[7], e[8], e[9], e[10]
        analysis_html = e[11]

        # Navigation
        prev_link = ''
        next_link = ''
        if i > 0:
            prev_num = emblems[i-1][1]
            prev_file = 'frontispiece.html' if prev_num == 0 else f'emblem-{prev_num:02d}.html'
            prev_link = f'<a href="{prev_file}">&larr; Previous</a>'
        if i < len(emblems) - 1:
            next_num = emblems[i+1][1]
            next_file = 'frontispiece.html' if next_num == 0 else f'emblem-{next_num:02d}.html'
            next_link = f'<a href="{next_file}">Next &rarr;</a>'

        title = f'Emblem {roman}' if roman else 'Frontispiece'
        display_num = roman or 'F'

        # Scholarly refs
        refs = conn.execute("""
            SELECT sr.summary, sr.confidence, sr.interpretation_type,
                   sr.source_texts_referenced, sr.section_page,
                   b.author, b.title, b.source_id
            FROM scholarly_refs sr
            JOIN bibliography b ON sr.bib_id = b.id
            WHERE sr.emblem_id = ?
            ORDER BY b.af_relevance, sr.confidence
        """, (eid,)).fetchall()

        refs_html = ''
        for ref in refs:
            summary, rconf, interp_type = ref[0], ref[1], ref[2]
            auth_json, page, author, btitle, src_id = ref[3], ref[4], ref[5], ref[6], ref[7]
            type_badge = f'<span class="badge badge-stage">{interp_type}</span>' if interp_type else ''
            conf_badge = confidence_badge(rconf)
            # Truncate long summaries
            if summary and len(summary) > 800:
                summary = summary[:800] + '...'
            refs_html += f"""
            <div class="ref-card">
                <h4>{author} {type_badge} {conf_badge}</h4>
                <p>{summary or 'No summary available.'}</p>
                {f'<p style="font-size:0.8rem;color:var(--text-muted);margin-top:0.5rem">Citation: {page}</p>' if page else ''}
            </div>"""

        # Source authorities
        sources = conn.execute("""
            SELECT sa.name, sa.type, es.relationship_type, es.confidence
            FROM emblem_sources es
            JOIN source_authorities sa ON es.authority_id = sa.id
            WHERE es.emblem_id = ?
            ORDER BY es.relationship_type
        """, (eid,)).fetchall()

        sources_html = ''
        for s in sources:
            sname, stype, rel, sconf = s
            sources_html += f'<span class="source-link">{sname} ({rel})</span>\n'

        # Build page
        # Stage badge styling
        stage_colors = {'NIGREDO': '#2c2418', 'ALBEDO': '#a89880', 'CITRINITAS': '#b8860b', 'RUBEDO': '#c0392b'}
        stage_text = {'NIGREDO': '#f5f0e8', 'ALBEDO': '#2c2418', 'CITRINITAS': '#2c2418', 'RUBEDO': '#f5f0e8'}
        stage_badge_html = ''
        if stage:
            bg = stage_colors.get(stage, '#7f8c8d')
            fg = stage_text.get(stage, '#fff')
            stage_badge_html = f'<span class="badge" style="background:{bg};color:{fg};font-size:0.85rem;padding:0.3rem 0.8rem;border-radius:3px">{stage}</span>'

        # Bilingual motto block
        motto_html = ''
        if motto_lat or motto_en:
            motto_html = '<div class="motto-block">'
            if motto_lat:
                motto_html += f'<p style="font-style:italic;color:var(--accent);margin-bottom:0.3rem;font-size:1.05rem">{motto_lat}</p>'
            if motto_en:
                motto_html += f'<p style="margin-top:0">{motto_en}</p>'
            motto_html += '</div>'
        else:
            motto_html = '<p style="color:var(--text-muted)"><em>Motto not yet extracted</em></p>'

        # Epigram (shown by default, not collapsed)
        epigram_html = ''
        if epigram:
            epigram_html = f'<div class="epigram-block" style="margin-bottom:1.5rem;padding:0.8rem 1rem;background:var(--bg);border-left:3px solid var(--accent-light);font-size:0.92rem"><h3 style="font-size:0.9rem;color:var(--accent);margin-bottom:0.4rem;font-family:var(--font-sans)">Epigram</h3>{epigram}</div>'

        # "What You See" visual description
        visual_html = ''
        if img_desc:
            visual_html = f'<div class="visual-description" style="margin-bottom:1.5rem;padding:0.8rem 1rem;background:#faf8f4;border-radius:4px"><h3 style="font-size:0.9rem;color:var(--accent);margin-bottom:0.4rem;font-family:var(--font-sans)">What You See</h3><p style="font-size:0.92rem;margin:0">{img_desc}</p></div>'

        body = f"""
    <div class="emblem-detail">
        <div class="emblem-nav">
            <span>{prev_link}</span>
            <a href="../">Gallery</a>
            <span>{next_link}</span>
        </div>

        <h1 style="font-size:1.8rem;margin-bottom:0.5rem">{title} — {label} {stage_badge_html}</h1>

        <div class="comparative-view">
            <div class="source-panel">
                <h2>Original Source</h2>
                {(lambda p, e: f'<img src="../{p}" alt="Emblem {display_num}" class="emblem-plate">' if e else f'<div class="placeholder-img">{display_num}</div>')(*resolve_image(identity_map, num))}
                {visual_html}
                {motto_html}
                {epigram_html}
                {f'<div class="discourse-block"><h3 style="font-size:1rem;color:var(--accent);margin-bottom:0.5rem">Discourse Summary</h3><p style="font-size:0.92rem">{discourse[:1500]}{"..." if discourse and len(discourse) > 1500 else ""}</p></div>' if discourse else ''}
                {autolink_emblems(analysis_html) if analysis_html else ''}
            </div>

            <div class="scholarship-panel">
                <h2>Scholarly Commentary</h2>
                {refs_html if refs_html else '<p style="color:var(--text-muted)"><em>No scholarly references extracted yet.</em></p>'}

                {f'<h3 style="font-size:1rem;color:var(--accent);margin-top:1.5rem;margin-bottom:0.5rem">Maier\'s Sources</h3>{sources_html}' if sources_html else ''}
            </div>
        </div>
    </div>"""

        filename = 'frontispiece.html' if num == 0 else f'emblem-{num:02d}.html'
        html = page_shell(f'{title} — {label}', body, active_nav='Emblems', depth=1)
        (emblems_dir / filename).write_text(html, encoding='utf-8')

    # Emblem index page
    stage_colors = {'NIGREDO': '#2c2418', 'ALBEDO': '#a89880', 'CITRINITAS': '#b8860b', 'RUBEDO': '#c0392b'}
    stage_fg = {'NIGREDO': '#f5f0e8', 'ALBEDO': '#2c2418', 'CITRINITAS': '#2c2418', 'RUBEDO': '#f5f0e8'}

    grid_html = ''
    for e in emblems:
        num, roman, label = e[1], e[2], e[3]
        motto = e[5] or ''
        e_stage = e[9]
        fname = 'frontispiece.html' if num == 0 else f'emblem-{num:02d}.html'
        display = roman or 'F'
        img_path, img_exists = resolve_image(identity_map, num)
        if img_exists:
            img_tag = f'<img src="../{img_path}" alt="Emblem {display}" style="width:100%;aspect-ratio:auto;display:block">'
        else:
            img_tag = f'<div class="card-placeholder" style="aspect-ratio:1;font-size:2rem">{display}</div>'
        sbadge = ''
        if e_stage:
            sbg = stage_colors.get(e_stage, '#7f8c8d')
            sfg = stage_fg.get(e_stage, '#fff')
            sbadge = f'<span style="display:inline-block;background:{sbg};color:{sfg};font-size:0.65rem;padding:0.15rem 0.4rem;border-radius:2px;font-family:var(--font-sans)">{e_stage}</span>'
        grid_html += f"""
        <a href="{fname}" class="card" style="text-decoration:none;color:inherit">
            {img_tag}
            <div class="card-body">
                <div class="card-sig">{display}. {label} {sbadge}</div>
                <div class="card-desc">{motto[:80]}{'...' if len(motto) > 80 else ''}</div>
                <div style="margin-top:0.5rem"><span style="font-size:0.8rem;color:var(--accent);font-family:var(--font-sans)">View details &rarr;</span></div>
            </div>
        </a>"""

    idx_body = f"""
    <div class="page-content" style="max-width:1400px">
        <h2>All 50 Emblems + Frontispiece</h2>
        <p>Click any emblem for the comparative view with scholarly commentary.</p>
        <div class="gallery" style="grid-template-columns:repeat(auto-fill, minmax(200px, 1fr));padding:1rem 0">{grid_html}</div>
    </div>"""
    html = page_shell('All Emblems', idx_body, active_nav='Emblems', depth=1)
    (emblems_dir / 'index.html').write_text(html, encoding='utf-8')

    print(f"  emblems/: {len(emblems)} detail pages + index")


# ============================================================
# About Page
# ============================================================

def build_about(conn):
    total = conn.execute("SELECT COUNT(*) FROM emblems WHERE number > 0").fetchone()[0]
    with_motto = conn.execute("SELECT COUNT(*) FROM emblems WHERE motto_english IS NOT NULL").fetchone()[0]
    with_disc = conn.execute("SELECT COUNT(*) FROM emblems WHERE discourse_summary IS NOT NULL").fetchone()[0]
    refs = conn.execute("SELECT COUNT(*) FROM scholarly_refs").fetchone()[0]
    sources = conn.execute("SELECT COUNT(*) FROM emblem_sources").fetchone()[0]
    bib = conn.execute("SELECT COUNT(*) FROM bibliography").fetchone()[0]
    auths = conn.execute("SELECT COUNT(*) FROM source_authorities").fetchone()[0]

    body = f"""
    <div class="page-content">
        <h2>About This Project</h2>
        <p>AtalantaClaudiens is a digital humanities project showcasing H.M.E. De Jong's scholarship
        on Michael Maier's <em>Atalanta Fugiens</em> (1618), an alchemical emblem book combining
        50 engraved plates, Latin mottos, epigrams, prose discourses, and three-voice musical fugues.</p>

        <h2>Project Statistics</h2>
        <div class="stats" style="max-width:100%">
            <div class="stat-card"><span class="stat-number">{total}</span><span class="stat-label">Emblems</span></div>
            <div class="stat-card"><span class="stat-number">{with_motto}</span><span class="stat-label">Mottos Extracted</span></div>
            <div class="stat-card"><span class="stat-number">{refs}</span><span class="stat-label">Scholarly References</span></div>
            <div class="stat-card"><span class="stat-number">{sources}</span><span class="stat-label">Source Links</span></div>
        </div>
        <div class="stats" style="max-width:100%">
            <div class="stat-card"><span class="stat-number">{bib}</span><span class="stat-label">Bibliography Entries</span></div>
            <div class="stat-card"><span class="stat-number">{auths}</span><span class="stat-label">Source Authorities</span></div>
            <div class="stat-card"><span class="stat-number">{with_disc}</span><span class="stat-label">Discourse Summaries</span></div>
        </div>

        <h2>Data Provenance</h2>
        <p>Data is extracted from scholarly sources using deterministic regex parsing.
        All content is tracked by source method and confidence level.
        AI-assisted content is explicitly marked.</p>
        <div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;margin:1rem 0">
            <tr style="border-bottom:1px solid var(--border)">
                <td style="padding:0.5rem"><strong>SEED_DATA</strong></td>
                <td style="padding:0.5rem">Loaded from structured JSON seed file</td>
            </tr>
            <tr style="border-bottom:1px solid var(--border)">
                <td style="padding:0.5rem"><strong>CORPUS_EXTRACTION</strong></td>
                <td style="padding:0.5rem">Parsed from source text by Python scripts</td>
            </tr>
            <tr>
                <td style="padding:0.5rem"><strong>LLM_ASSISTED</strong></td>
                <td style="padding:0.5rem">Generated by language model (marked with review badges)</td>
            </tr>
        </table></div>

        <h2>Architecture</h2>
        <p>SQLite database &rarr; Python scripts &rarr; Static HTML/CSS/JS &rarr; GitHub Pages.
        No frameworks, no build tools, no runtime dependencies.</p>
        <p><a href="https://github.com/t3dy/AtalantaClaudiens" style="color:var(--accent)">View on GitHub &rarr;</a></p>
    </div>"""

    html = page_shell('About', body, active_nav='About')
    (SITE_DIR / 'about.html').write_text(html, encoding='utf-8')
    print(f"  about.html")


# ============================================================
# Scholars Pages
# ============================================================

def build_scholars_pages(conn):
    scholars_dir = SITE_DIR / 'scholar'
    scholars_dir.mkdir(exist_ok=True)

    scholars = conn.execute("""
        SELECT id, name, specialization, af_focus, overview, review_status
        FROM scholars ORDER BY name
    """).fetchall()

    # Index page
    cards_html = ''
    for s in scholars:
        sid, name, spec, focus, overview, status = s
        work_count = conn.execute(
            "SELECT COUNT(*) FROM scholar_works WHERE scholar_id = ?", (sid,)
        ).fetchone()[0]
        ref_count = conn.execute("""
            SELECT COUNT(DISTINCT sr.emblem_id) FROM scholarly_refs sr
            JOIN bibliography b ON sr.bib_id = b.id
            JOIN scholar_works sw ON sw.bib_id = b.id
            WHERE sw.scholar_id = ?
        """, (sid,)).fetchone()[0]
        slug = slugify(name)
        cards_html += f"""
        <a href="scholar/{slug}.html" class="card" style="text-decoration:none;color:inherit">
            <div class="card-body">
                <div class="card-sig">{name}</div>
                <div class="card-label">{spec or ''}</div>
                <div class="card-desc">{focus or ''}</div>
                <div style="margin-top:0.5rem;font-size:0.8rem;color:var(--text-muted);font-family:var(--font-sans)">
                    {work_count} work{'s' if work_count != 1 else ''} &middot; {ref_count} emblem{'s' if ref_count != 1 else ''} covered
                </div>
                <div style="margin-top:0.4rem"><span style="font-size:0.8rem;color:var(--accent);font-family:var(--font-sans)">View profile &rarr;</span></div>
            </div>
        </a>"""

    body = f"""
    <div class="page-content" style="max-width:1200px">
        <h2>Scholars</h2>
        <p>{len(scholars)} scholars who have published on <em>Atalanta Fugiens</em>.</p>
        <div class="gallery" style="padding:1rem 0">{cards_html}</div>
    </div>"""
    html = page_shell('Scholars', body, active_nav='Scholars')
    (SITE_DIR / 'scholars.html').write_text(html, encoding='utf-8')

    # Individual pages
    for s in scholars:
        sid, name, spec, focus, overview, status = s
        slug = slugify(name)

        works = conn.execute("""
            SELECT b.author, b.title, b.year, b.journal, b.publisher, b.af_relevance, b.pub_type
            FROM bibliography b
            JOIN scholar_works sw ON sw.bib_id = b.id
            WHERE sw.scholar_id = ?
            ORDER BY b.year
        """, (sid,)).fetchall()

        works_html = ''
        for w in works:
            rel_badge = f'<span class="badge badge-{"primary" if w[5] == "PRIMARY" else "direct" if w[5] == "DIRECT" else "contextual"}">{w[5]}</span>'
            works_html += f"""
            <div class="ref-card">
                <h4>{w[0]} ({w[2] or '?'}) {rel_badge}</h4>
                <p><em>{w[1]}</em></p>
                <p style="font-size:0.8rem;color:var(--text-muted)">{w[3] or w[4] or ''} &middot; {w[6] or ''}</p>
            </div>"""

        body = f"""
        <div class="page-content">
            <a href="../scholars.html" class="back-link">&larr; All Scholars</a>
            <h1 style="font-size:1.8rem;margin-bottom:0.5rem">{name}</h1>
            <p style="color:var(--text-muted);font-family:var(--font-sans);margin-bottom:1.5rem">{spec or ''}</p>
            {f'<p style="margin-bottom:1rem">{focus}</p>' if focus else ''}
            {format_paragraphs(overview) if overview else ''}
            {f'<h2>Works in Archive</h2>{works_html}' if works_html else '<p style="color:var(--text-muted)"><em>No works linked yet.</em></p>'}
        </div>"""
        html = page_shell(name, body, active_nav='Scholars', depth=1)
        (scholars_dir / f'{slug}.html').write_text(html, encoding='utf-8')

    print(f"  scholars.html + {len(scholars)} scholar pages")


# ============================================================
# Bibliography Page
# ============================================================

def build_bibliography(conn):
    entries = conn.execute("""
        SELECT source_id, author, title, year, journal, publisher, pub_type, af_relevance, in_collection, annotation
        FROM bibliography ORDER BY year
    """).fetchall()

    rows_html = ''
    for e in entries:
        src_id, author, title, year, journal, pub, ptype, rel, incoll, annotation = e
        rel_badge = f'<span class="badge badge-{"primary" if rel == "PRIMARY" else "direct" if rel == "DIRECT" else "contextual"}">{rel}</span>'
        venue = journal or pub or ''
        rows_html += f"""
        <div class="ref-card">
            <h4>{author} ({year or '?'}) {rel_badge}</h4>
            <p><em>{title}</em></p>
            <p style="font-size:0.8rem;color:var(--text-muted)">{venue} &middot; {ptype or ''}</p>
            {f'<p style="font-size:0.88rem;line-height:1.6;margin-top:0.5rem">{annotation}</p>' if annotation else ''}
        </div>"""

    primary = len([e for e in entries if e[7] == 'PRIMARY'])
    direct = len([e for e in entries if e[7] == 'DIRECT'])
    body = f"""
    <div class="page-content">
        <h2>Bibliography</h2>
        <div class="stats" style="max-width:100%">
            <div class="stat-card"><span class="stat-number">{len(entries)}</span><span class="stat-label">Total Works</span></div>
            <div class="stat-card"><span class="stat-number">{primary}</span><span class="stat-label">Primary</span></div>
            <div class="stat-card"><span class="stat-number">{direct}</span><span class="stat-label">Direct</span></div>
        </div>
        {rows_html}
    </div>"""
    html = page_shell('Bibliography', body, active_nav='Bibliography')
    (SITE_DIR / 'bibliography.html').write_text(html, encoding='utf-8')
    print(f"  bibliography.html: {len(entries)} entries")


# ============================================================
# Dictionary Pages
# ============================================================

def build_dictionary_pages(conn):
    dict_dir = SITE_DIR / 'dictionary'
    dict_dir.mkdir(exist_ok=True)

    terms = conn.execute("""
        SELECT id, slug, label, category, definition_short, definition_long,
               significance_to_af, source_basis, review_status, label_latin, registers
        FROM dictionary_terms ORDER BY label
    """).fetchall()

    # Count emblem refs per term
    emblem_counts = {}
    for t in terms:
        cnt = conn.execute(
            "SELECT COUNT(*) FROM term_emblem_refs WHERE term_id = ?", (t[0],)
        ).fetchone()[0]
        emblem_counts[t[0]] = cnt

    # Group by category
    categories = {}
    for t in terms:
        cat = t[3] or 'UNCATEGORIZED'
        categories.setdefault(cat, []).append(t)

    # Index page with rich cards
    cat_html = ''
    for cat in sorted(categories.keys()):
        cat_terms = categories[cat]
        cards = ''
        for t in cat_terms:
            tid, slug, label, tcat, def_short = t[0], t[1], t[2], t[3], t[4]
            label_latin = t[9]
            ecnt = emblem_counts.get(tid, 0)
            latin_line = f'<div class="dict-latin">{label_latin}</div>' if label_latin and label_latin != label else ''
            cards += f"""
            <a href="{slug}.html" class="dict-card">
                <div class="dict-label">{label}
                    <span class="badge badge-stage">{tcat}</span>
                    {f'<span class="badge badge-contextual">{ecnt} emblems</span>' if ecnt else ''}
                </div>
                {latin_line}
                <div class="dict-def">{def_short or ""}</div>
                <div style="margin-top:0.3rem"><span style="font-size:0.75rem;color:var(--accent);font-family:var(--font-sans)">View definition &rarr;</span></div>
            </a>"""
        cat_html += f"""
        <div style="margin-bottom:2rem">
            <h3 style="font-size:1.1rem;color:var(--accent);margin-bottom:0.75rem">{cat} <span class="badge badge-contextual">{len(cat_terms)}</span></h3>
            {cards}
        </div>"""

    body = f"""
    <div class="page-content">
        <h2>Dictionary of <em>Atalanta Fugiens</em></h2>
        <p>Key alchemical terms as they appear in Maier's text, with Latin originals. {len(terms)} terms across {len(categories)} categories.</p>
        {cat_html}
    </div>"""
    html = page_shell('Dictionary', body, active_nav='Dictionary', depth=1)
    (dict_dir / 'index.html').write_text(html, encoding='utf-8')

    # Individual term pages
    for t in terms:
        tid, slug, label, cat, def_short, def_long, sig, basis, status, label_latin = t[:10]
        registers_json = t[10] if len(t) > 10 else None

        # Find linked emblems
        emblem_refs = conn.execute("""
            SELECT e.number, e.roman_numeral, e.canonical_label
            FROM term_emblem_refs ter
            JOIN emblems e ON ter.emblem_id = e.id
            WHERE ter.term_id = ?
            ORDER BY e.number
        """, (tid,)).fetchall()

        emblem_links = ' '.join(
            f'<a href="../emblems/emblem-{er[0]:02d}.html" class="source-link">Emblem {er[1]}: {er[2]}</a>'
            for er in emblem_refs if er[0] > 0
        )

        # Related terms
        related = conn.execute("""
            SELECT dt.slug, dt.label, dtl.link_type
            FROM dictionary_term_links dtl
            JOIN dictionary_terms dt ON dtl.linked_term_id = dt.id
            WHERE dtl.term_id = ?
        """, (tid,)).fetchall()
        related_html = ' '.join(
            f'<a href="{r[0]}.html" class="source-link">{r[1]}</a>'
            for r in related
        )

        latin_display = f'<div class="term-latin">{label_latin}</div>' if label_latin and label_latin != label else ''

        body = f"""
        <div class="page-content">
            <a href="index.html" class="back-link">&larr; Dictionary of <em>Atalanta Fugiens</em></a>
            <h1 style="font-size:1.8rem;margin-bottom:0.3rem">{label}
                <span class="badge badge-stage">{cat}</span>
            </h1>
            {latin_display}
            {f'<div class="motto-block">{def_short}</div>' if def_short else ''}
            {format_paragraphs(autolink_emblems(def_long)) if def_long else ''}
            {build_registers_html(registers_json)}
            {f'<h2>In <em>Atalanta Fugiens</em></h2><p style="font-size:0.95rem;line-height:1.7">{autolink_emblems(sig)}</p>' if sig else ''}
            {f'<h2>Appears in Emblems</h2><div>{emblem_links}</div>' if emblem_links else ''}
            {f'<h2>Related Terms</h2><div>{related_html}</div>' if related_html else ''}
            {f'<p style="margin-top:1.5rem;font-size:0.8rem;color:var(--text-muted)">Source: {basis}</p>' if basis else ''}
        </div>"""
        html = page_shell(label, body, active_nav='Dictionary', depth=1)
        (dict_dir / f'{slug}.html').write_text(html, encoding='utf-8')

    print(f"  dictionary/: {len(terms)} term pages + index")


# ============================================================
# Timeline Page
# ============================================================

def build_timeline(conn):
    events = conn.execute("""
        SELECT year, year_end, event_type, title, description, confidence,
               description_long
        FROM timeline_events ORDER BY year
    """).fetchall()

    TYPE_COLORS = {
        'PUBLICATION': '#27ae60', 'EDITION': '#2980b9', 'SCHOLARSHIP': '#8e44ad',
        'BIOGRAPHY': '#e67e22', 'DIGITAL': '#16a085', 'FACSIMILE': '#795548',
    }

    events_html = ''
    prev_year = None
    for e in events:
        year, year_end, etype, title, desc, conf, desc_long = e
        color = TYPE_COLORS.get(etype, '#7f8c8d')
        year_header = f'<div class="timeline-year">{year}</div>' if year != prev_year else ''
        display_desc = desc_long or desc or ''
        events_html += f"""{year_header}
        <div class="timeline-card" style="border-left:4px solid {color}">
            <h4><span class="badge" style="background:{color};color:white">{etype}</span> {title}</h4>
            <div class="event-desc">{display_desc}</div>
        </div>"""
        prev_year = year

    body = f"""
    <div class="page-content">
        <h2>Timeline of Atalanta Fugiens</h2>
        <p>Reception and scholarship from 1568 to the present. {len(events)} events.</p>
        {events_html}
    </div>"""
    html = page_shell('Timeline', body, active_nav='Timeline')
    (SITE_DIR / 'timeline.html').write_text(html, encoding='utf-8')
    print(f"  timeline.html: {len(events)} events")


# ============================================================
# Sources Page
# ============================================================

def build_sources(conn):
    authorities = conn.execute("""
        SELECT sa.id, sa.authority_id, sa.name, sa.type, sa.author,
               sa.relationship_to_maier, sa.description_long,
               COUNT(es.id) as emblem_count
        FROM source_authorities sa
        LEFT JOIN emblem_sources es ON es.authority_id = sa.id
        GROUP BY sa.id
        ORDER BY sa.type, emblem_count DESC
    """).fetchall()

    TYPE_COLORS = {
        'CLASSICAL': '#8e44ad', 'ALCHEMICAL': '#c0392b', 'BIBLICAL': '#2980b9',
        'MEDICAL': '#27ae60', 'PATRISTIC': '#e67e22', 'HERMETIC': '#16a085',
        'MOVEMENT': '#795548',
    }

    # Group by type
    by_type = {}
    for a in authorities:
        t = a[3] or 'OTHER'
        by_type.setdefault(t, []).append(a)

    sections_html = ''
    for stype in ['HERMETIC', 'ALCHEMICAL', 'CLASSICAL', 'BIBLICAL', 'MEDICAL', 'PATRISTIC', 'MOVEMENT']:
        if stype not in by_type:
            continue
        color = TYPE_COLORS.get(stype, '#7f8c8d')
        auths = by_type[stype]
        cards = ''
        for a in auths:
            aid, auth_id, name, atype, author, rel, desc_long, count = a
            # Find which emblems use this authority with numbers for links
            emblem_data = conn.execute("""
                SELECT e.number, e.roman_numeral FROM emblem_sources es
                JOIN emblems e ON es.emblem_id = e.id
                WHERE es.authority_id = ? AND e.number > 0
                ORDER BY e.number
            """, (aid,)).fetchall()
            emblem_badges = ' '.join(
                f'<a href="emblems/emblem-{ed[0]:02d}.html" class="emblem-link-badge">{ed[1]}</a>'
                for ed in emblem_data if ed[1]
            )
            cards += f"""
            <div class="source-card" id="{auth_id}" style="border-left:4px solid {color}">
                <h4>{name} <span class="badge" style="background:{color};color:white">{count} emblems</span></h4>
                {f'<div class="source-desc">{desc_long}</div>' if desc_long else (f'<p style="font-size:0.9rem">{rel}</p>' if rel else '')}
                {f'<div class="emblem-links" style="margin-top:0.5rem">{emblem_badges}</div>' if emblem_badges else ''}
            </div>"""
        sections_html += f"""
        <h2 style="margin-top:2rem"><span class="badge" style="background:{color};color:white;font-size:0.8rem">{stype}</span> {stype.title()} Sources</h2>
        {cards}"""

    body = f"""
    <div class="page-content">
        <h2>Maier's Sources &amp; Influences</h2>
        <p>{len(authorities)} source traditions identified by De Jong and other scholars, linked to {conn.execute("SELECT COUNT(*) FROM emblem_sources").fetchone()[0]} emblem references.</p>
        {sections_html}
    </div>"""
    html = page_shell('Sources & Influences', body, active_nav='Sources')
    (SITE_DIR / 'sources.html').write_text(html, encoding='utf-8')
    print(f"  sources.html: {len(authorities)} authorities")


# ============================================================
# Essays (placeholder index)
# ============================================================

def build_essays(conn):
    essays_dir = SITE_DIR / 'essays'
    essays_dir.mkdir(exist_ok=True)

    planned = [
        ("playful-reading", "Playful Reading in Atalanta Fugiens",
         "How Maier's emblem book invites ludic engagement through its combination of image, text, and music."),
        ("alchemical-symbolism", "Alchemical Symbolism and the Emblem Tradition",
         "The visual language of the 50 emblems and their roots in the European emblem book tradition."),
        ("musical-fugues", "Maier's Musical Fugues",
         "The role of the 50 three-voice canons and their structural relationship to alchemical process."),
        ("rosicrucian-context", "The Rosicrucian Context",
         "Maier's engagement with the Rosicrucian movement and its expression in Atalanta Fugiens."),
        ("reception-history", "Reception History: From 1618 to Digital Humanities",
         "Four centuries of scholarship on Atalanta Fugiens, from Craven to Furnace and Fugue."),
    ]

    cards_html = ''
    for slug, title, desc in planned:
        cards_html += f"""
        <div class="card" style="cursor:default">
            <div class="card-body">
                <div class="card-sig">{title}</div>
                <div class="card-desc">{desc}</div>
                <div style="margin-top:0.5rem"><span class="review-badge">COMING SOON</span></div>
            </div>
        </div>"""

    body = f"""
    <div class="page-content" style="max-width:1200px">
        <h2>Essays</h2>
        <p>Planned essays synthesized from the scholarly corpus. These will be AI-drafted and clearly marked.</p>
        <div class="gallery" style="padding:1rem 0">{cards_html}</div>
    </div>"""
    html = page_shell('Essays', body, active_nav='Essays', depth=1)
    (essays_dir / 'index.html').write_text(html, encoding='utf-8')
    print(f"  essays/: index (5 planned)")


# ============================================================
# Biography Page
# ============================================================

def build_szulakowska_page():
    """Build the Szulakowska feature page — in-depth treatment of Maier in her three monographs."""

    def emblem_img(num, caption=''):
        fname = f'emblem-{num:02d}.jpg' if num > 0 else 'emblem-00.jpg'
        cap = f'<figcaption style="font-size:0.8rem;color:var(--text-muted);margin-top:0.3rem;text-align:center">{caption}</figcaption>' if caption else ''
        return f'<figure style="margin:1rem auto;max-width:400px"><img src="images/emblems/{fname}" alt="Emblem {num}" style="width:100%;border-radius:4px;box-shadow:0 2px 8px rgba(0,0,0,0.15)">{cap}</figure>'

    body = f"""
    <div class="page-content">
        <h1 style="font-size:1.8rem;margin-bottom:0.3rem">Szulakowska on Maier</h1>
        <p style="font-size:1.1rem;color:var(--text-muted);margin-bottom:1rem;font-style:italic">
            The Religious Politics of Alchemical Illustration
        </p>
        <p style="font-size:0.95rem;line-height:1.7;margin-bottom:1.5rem">
            Urszula Szulakowska's three monographs — <em>The Sacrificial Body and the Day of Doom</em> (Brill),
            <em>The Alchemy of Light</em> (Brill), and <em>The Alchemical Virgin Mary</em> (Cambridge Scholars) —
            offer a dimension of Maier scholarship found nowhere else: the religious and political context of
            alchemical illustration. Where De Jong traces each emblem to its textual sources and Tilton
            situates Maier within Rosicrucianism, Szulakowska reveals the Reformation theology, Eucharistic
            controversy, and Habsburg court politics encoded in the same images.
        </p>
        <div class="ai-banner">This page synthesizes material from three Szulakowska monographs in our corpus. Not reviewed by a human scholar.</div>

        <h2>I. The Khunrath-Maier-Fludd Triad</h2>
        {format_paragraphs(
            "Szulakowska positions Maier within a triad of late-Renaissance Paracelsian alchemists — Heinrich "
            "Khunrath (1560-1605), Michael Maier (1568-1622), and Robert Fludd (1574-1637) — who collectively "
            "transformed alchemical illustration from medieval Christological imagery into a new classicizing "
            "visual language. She argues that Maier's emblems in the Atalanta Fugiens 'set the style for "
            "alchemical illustration for the next three centuries, replacing the earlier Christological motifs.' "
            "Fludd and Johann Daniel Mylius subsequently copied and adapted Maier's visual innovations, with "
            "Mylius reproducing AF emblems in detail in his Philosophia Reformata (1622)."
            "\\n\\n"
            "What distinguishes the triad is not merely their artistry but their theological ambition. "
            "Szulakowska argues that all three regarded their chemical procedures 'as being essentially the same "
            "rite as the mass' — a 'symbolic usurpation of the highest spiritual and political authority since "
            "the right to offer Communion was jealously guarded.' The alchemical laboratory becomes, in this "
            "reading, an alternative altar where the transmutation of matter re-enacts the Eucharistic "
            "transformation of bread and wine into the body and blood of Christ."
            "\\n\\n"
            "Yet Maier is the most reticent of the three. Where Khunrath openly identified Christ with the "
            "philosopher's stone, and Fludd developed elaborate cosmological diagrams, Maier 'disguised his "
            "religious references in barely decipherable signifiers.' His classical mythological surface — "
            "Atalanta, Hippomenes, Osiris, Oedipus — conceals what Szulakowska identifies as a fundamentally "
            "Eucharistic understanding of alchemical transformation. The reader who sees only pagan myth misses "
            "the sacramental structure beneath."
        )}

        <h2>II. The Alchemical Mass</h2>
        {format_paragraphs(
            "Szulakowska's most sustained analysis of Maier concerns the alchemical mass illustration from "
            "the Symbola Aureae Mensae Duodecim Nationum (1617). Maier reprinted a fifteenth-century treatise "
            "by Nicolaus Melchior Cibinensis (Processus sub forma missae) and commissioned Matthaeus Merian to "
            "engrave an accompanying illustration of the Virgin Mary as the Apocalyptic Woman from Revelation "
            "12:1 — 'a woman clothed with the sun, with the moon under her feet, and on her head a crown of "
            "twelve stars.'"
            "\\n\\n"
            "Szulakowska argues that Maier's illustration is 'a far more radical disquisition on the alchemical "
            "mass than Cibinensis' discrete original text.' Where the fifteenth-century author had cautiously "
            "discontinued his account before the consecration of bread and wine, Maier's engraving 'clearly "
            "identifies Christ with the lapis philosophorum and the elixir of life.' The chasuble of the "
            "officiating priest, the gestures of consecration, the presence of the Apocalyptic Woman — all "
            "constitute a bold exposition of the alchemical process as a re-enactment, not merely a "
            "symbolization, of the Catholic Communion."
            "\\n\\n"
            "In The Alchemical Virgin Mary, Szulakowska connects this image to the 'Turkish Madonna' "
            "tradition — Marian imagery linked to the Ottoman wars and the defense of Christendom. Emperor "
            "Rudolf II, Maier's patron, had been heavily involved in military campaigns against the Turks. "
            "The Apocalyptic Woman in Maier's illustration may thus function simultaneously as the Virgin Mary, "
            "as the alchemical lac virginis (virgin's milk), and as a political emblem of Christian resistance "
            "to Ottoman expansion — a triple register that exemplifies the density of meaning Szulakowska "
            "finds in Maier's visual program."
        )}

        <h2>III. Atalanta Fugiens: The Sacrificial Body</h2>
        <p style="font-size:0.95rem;line-height:1.7;margin-bottom:1rem">
            In <em>The Sacrificial Body</em>, Szulakowska reads six AF emblems through the lens of
            bodily transformation, Eucharistic symbolism, and Reformation theology. Her central argument
            is that the theme of dismemberment and resurrection — pervasive in the AF — encodes a
            specifically Christian soteriology beneath its classical surface.
        </p>

        <h3>Emblem XIX — The Four Warriors</h3>
        {emblem_img(19, 'Emblem XIX: If you kill one of the four, everybody will be dead immediately')}
        {format_paragraphs(
            "Szulakowska reads the four interconnected warriors (representing the four elements whose death "
            "is mutual) as a Christological allegory. She identifies Maier's reference to Hermes testifying "
            "that 'our Son shall live and the dead King shall come out of the fire' as a disguised reference "
            "to Christ's resurrection. When 'this dead one arises, then death, darkness and the waters of "
            "the abyss shall flee from him.' The dragon that guards the abyss flees from the sun-beams — "
            "'our Son' — in language that maps precisely onto Christian eschatology."
            "\\n\\n"
            "Where De Jong identifies the source as the myth of Geryon and the Turba Philosophorum's teaching "
            "about elemental inseparability, Szulakowska adds the Christological layer: the four warriors are "
            "not merely four elements but four aspects of the sacrificial body that must die together before "
            "resurrection is possible. Maier 'mitigates the degree of physical violence exhibited in his visual "
            "symbols' compared to earlier alchemical imagery, but retains their salvific meaning."
        )}

        <h3>Emblem XXIV — The Wolf Devouring the King</h3>
        {emblem_img(24, 'Emblem XXIV: The wolf devoured the king')}
        {format_paragraphs(
            "The wolf (antimony) devours the crowned king (Saturn/prime matter), then the wolf is consumed "
            "by fire, and the king returns to life 'in a young and vigorous form as the tincture that cures "
            "every disease.' Szulakowska traces this allegory to Basil Valentine's Twelve Keys, where the wolf "
            "symbolizes the mineral antimony used to separate gold from its matrix."
            "\\n\\n"
            "Lawrence Principe has identified the metallurgical reality behind this imagery: antimony sulphide "
            "was used in assaying to extract gold from base alloys. Szulakowska reads beyond the chemistry to "
            "identify the sacrificial-body theology: the king's dismemberment and reconstitution mirrors the "
            "Eucharistic sacrifice where the body of Christ is broken and distributed before being mystically "
            "reunited in the Resurrection."
        )}

        <h3>Emblem XXVIII — King Duenech in the Steam Bath</h3>
        {emblem_img(28, 'Emblem XXVIII: The king is bathed, sitting in a steam-bath')}
        {format_paragraphs(
            "King Duenech sits immersed in a steaming bath while black bile (aqua foetida) drains from his "
            "body, attended by physicians who regulate the temperature. Szulakowska connects this emblem to "
            "the alchemical understanding of bodily purification through the humoral system: 'alchemists used "
            "baths in order to improve the proportions of the humours in their chemicals, to produce healthy "
            "blood in the body and to convert cold and moist materials into warm and dry ones.'"
            "\\n\\n"
            "She notes that Maier 'refers to himself as a cook at the golden table' — a reference to the "
            "Symbola Aureae Mensae — connecting the domestic imagery of cooking and bathing to the Rosicrucian "
            "fraternity described as being 'seated at a golden table.' The purification is simultaneously "
            "medical (humoral rebalancing), chemical (distillation), and sacramental (baptismal cleansing)."
        )}

        <h3>Emblem XXXV — Digestion and Feeding</h3>
        {emblem_img(35, 'Emblem XXXV: As Ceres accustomed Triptolemus to endure fire')}
        {format_paragraphs(
            "Szulakowska discusses Maier's treatment of digestion as 'an indispensable stage in alchemical "
            "practice, comparable to the feeding of a young child and to agricultural processes.' Where "
            "wider Reformation culture treated bodily functions as taboo, the alchemists continued to regard "
            "digestion as a positive process, 'due to the very nature of their chemical process whose essential "
            "function was to change substance.'"
            "\\n\\n"
            "This rehabilitation of the body is, for Szulakowska, a specifically alchemical contribution to "
            "Reformation culture — a refusal to accept the Protestant separation of spirit and matter that "
            "was reshaping European attitudes toward the physical body."
        )}

        <h3>Emblem XL — The Two Fountains</h3>
        {emblem_img(40, 'Emblem XL: Make one water out of two waters')}
        {format_paragraphs(
            "Two streams merge into a single pool — the 'water of holiness.' Szulakowska identifies this as "
            "one of the 'slightly more overt references to the alchemical sacrament' in AF. Maier states "
            "that the elixir's meaning is 'analogous to the water of life of Christ, meaning by this both "
            "the sacrament of Baptism and also that of the Eucharist.'"
            "\\n\\n"
            "De Jong traced the source to the Lullian elixir tradition. Szulakowska adds the sacramental "
            "dimension: the two waters represent the two sacraments (Baptism and Eucharist) unified in the "
            "alchemical operation. This is as close as Maier comes to explicitly naming the Christian "
            "sacramental meaning that Szulakowska argues pervades the entire series."
        )}

        <h3>Emblem XLIV — Osiris Dismembered and Reassembled</h3>
        {emblem_img(44, 'Emblem XLIV: Typhon kills Osiris by a ruse')}
        {format_paragraphs(
            "Typhon murders Osiris and scatters his limbs; Isis gathers them. Szulakowska identifies the "
            "figure of Belinus — a late Hellenistic version of Osiris drawn from the Rosarium Philosophorum — "
            "as a Christ-figure. She quotes the text: 'when you have taken me partly out of my nature, and "
            "my wife out of hers and after you have killed these natures and we are raised by a new and "
            "incorporeal resurrection, so that after that we cannot die any more.'"
            "\\n\\n"
            "The language of 'incorporeal resurrection' maps directly onto Christian eschatology. Szulakowska "
            "argues that this is the most explicit Christological moment in the AF — the Egyptian myth of "
            "Osiris serving as a classical-mythological vehicle for what is essentially the death, "
            "dismemberment, and bodily resurrection of Christ."
        )}

        <h2>IV. The Alchemy of Light: Maier's Solar Geometry</h2>
        {format_paragraphs(
            "In her most technically detailed analysis of Maier, Szulakowska devotes Chapter 11 of The Alchemy "
            "of Light to 'Michael Maier's Alchemical Geometry of the Sun.' She begins by distinguishing "
            "Maier's courtly, classicizing style from Khunrath's pietistic intensity and Fludd's cosmological "
            "ambition. Maier's work 'emerges from the context of courtly humanism, rather than out of the "
            "academic discourses of the Protestant universities.' The Atalanta Fugiens, she argues, 'takes the "
            "form of a masque, with stage sets displaying scenes from classical mythology, accompanied by a "
            "musical score' — entertainment designed to instruct."
            "\\n\\n"
            "Szulakowska traces Maier's theoretical program to his treatise De Circulo Physico, Quadrato "
            "(1616), which she identifies as 'an account of the role of the sun in the making of potable "
            "gold.' Maier argued that gold's essential form is the circle — the Platonic form of eternal "
            "Being — and that the incorrupt nature of gold proves the circle 'is not an abstract mathematical "
            "concept, but a physical reality.' The static circle is nature perfected, manifesting as red, "
            "coagulated sulphur — that is, gold."
        )}

        <h3>Emblem XXI — The Geometric Formula</h3>
        {emblem_img(21, 'Emblem XXI: Make a circle out of a man and a woman')}
        {format_paragraphs(
            "Szulakowska connects the famous geometric diagram of Emblem XXI — circle, square, triangle, "
            "circle — to Maier's treatise on squaring the circle and to the Rosarium Philosophorum. The circle "
            "represents the primal matter (Chaos) and the perfected stone; the square symbolizes the four "
            "elements and the four seasons; the triangle represents the Paracelsian body, spirit, and soul "
            "(though Maier himself is not Paracelsian in method). The same geometric sequence appears in the "
            "seventh key of Basil Valentine's De Lapide Sapientum, which Maier published in his Tripus Aureus "
            "(1618)."
        )}

        <h3>Emblem VIII — The Theurgical Egg</h3>
        {emblem_img(8, 'Emblem VIII: Take the egg and pierce it with a fiery sword')}
        {format_paragraphs(
            "Szulakowska's most original reading concerns Emblem VIII, which she interprets through the lens "
            "of optical alchemy. The illustration shows an armed warrior (Mars) shattering the alchemical egg "
            "with a sword before a roaring fire. Behind him, a battlemented wall is pierced by 'a curious "
            "tunnel drawn in a diagrammatic form according to the rules of single-point perspective.' The "
            "tunnel's 'excessive depth does not correspond with the actual thickness of the wall' — it is "
            "not realistic architecture but, Szulakowska argues, a catoptrical diagram representing the "
            "concentration of solar rays."
            "\\n\\n"
            "Szulakowska connects this perspectival structure to the use of catoptrical mirrors (burning "
            "glasses) described by John Dee in the Propaedeumata Aphoristica and to Khunrath's optical "
            "imagery in the Amphitheatrum. She reads the tunnel as representing solar force being focused "
            "onto the alchemical egg — analogous to a burning glass concentrating sunlight. De Jong had "
            "compared the egg to Dee's macro-microcosmic egg in the Monas Hieroglyphica; Szulakowska extends "
            "this comparison to argue that the composition encodes an optical-alchemical program. This is "
            "a provocative reading that goes beyond what the image alone can confirm, but it usefully draws "
            "attention to the geometric and optical sophistication of Merian's engravings."
        )}

        <h3>The Fugues as Theurgical Talismans</h3>
        {format_paragraphs(
            "Szulakowska's most provocative argument concerns the fugues themselves. She proposes that "
            "Maier's Pythagorean musical score was intended to operate on the same astral-magical principles "
            "as Dee's and Khunrath's geometric sigils — that the musical ratios encoded correspondences with "
            "celestial forces. She argues that the fifth interval (diapente), whose ratio of 3:2 Ficino "
            "had identified with the proportional distance from earth to the sun, served as a musical "
            "signifier of solar virtue."
            "\\n\\n"
            "This interpretation — that the fugues function as something like astral-magical instruments — "
            "is characteristic of Szulakowska's willingness to push interpretive boundaries. It should be "
            "noted that Forshaw and other scholars in the new historiography of alchemy prefer to read AF "
            "as a work of alchemical synthesis rather than active theurgy, and Maier himself describes "
            "his emblems as 'chemical' rather than magical. Pamela H. Smith's framework of artisanal "
            "knowledge — where alchemy is understood as a sophisticated craft practice rather than either "
            "mysticism or modern chemistry — offers a more grounded interpretive model. Nonetheless, "
            "Szulakowska usefully draws attention to the Pythagorean mathematical structure of the fugues, "
            "which has not been adequately explored by other scholars, and to the broader context of "
            "Ficinian music theory within which Maier's compositions operated."
        )}

        <h2>V. Maier and the Rosarium Tradition</h2>
        {format_paragraphs(
            "In The Alchemical Virgin Mary, Szulakowska draws on De Jong's research to situate Maier's AF "
            "within the tradition of the Rosarium Philosophorum (Basel, 1550). She writes that De Jong 'has "
            "revealed' that Maier 'was basing himself substantially on the Rosarium (as well as on the Aurora "
            "Consurgens and the much older Turba Philosophorum)' — the same sources that contained Marian and "
            "Christological imagery that Maier transformed into his classicizing emblems."
            "\\n\\n"
            "The alchemical marriage in the Rosarium tradition involved an incestuous coupling of brother and "
            "sister (Sol and Luna), who then 'died' and putrefied — the same sequence Maier develops across "
            "multiple AF emblems (IV, XXX, XXXIII, XXXVIII). Szulakowska notes that this alchemical coniunctio "
            "drew on Marian theology through the Rosarium's mediation: the Virgin Mary as the vessel of "
            "transformation, the lac virginis as the volatile spirit that nourishes the philosophical embryo."
            "\\n\\n"
            "Szulakowska also identifies Adam McLean's observation that the Splendor Solis of Salomon Trismosin "
            "(1598) 'acts as a bridge between the Rosarium and the Rosicrucian period' — and argues that "
            "Maier's AF occupies the Rosicrucian end of this bridge, transforming the Rosarium's medieval "
            "Christian imagery into a classicized, humanist visual language while preserving its sacramental "
            "core."
        )}

        <h2>VI. Why Szulakowska Matters</h2>
        {format_paragraphs(
            "Szulakowska's contribution is unique because she reads the same images that De Jong analyzes "
            "source-critically and that Forshaw reads mytho-alchemically through a third lens: the religious "
            "politics of the Reformation. Her argument that Maier, Khunrath, and Fludd constituted an "
            "alchemical counter-church — performing a chemical Eucharist that usurped the Catholic sacramental "
            "monopoly — adds a political dimension that purely textual or symbolic readings miss."
            "\\n\\n"
            "Her most original contribution, from The Alchemy of Light, is her attention to the Pythagorean "
            "mathematical structure of both the geometric diagrams and the fugues. While her interpretation "
            "of these as astral-magical instruments goes further than most scholars in the field would "
            "endorse, she rightly identifies an underexplored dimension of the AF: the relationship between "
            "its mathematical structures (geometric, musical, arithmetical) and the alchemical content they "
            "accompany. This is territory that Forshaw's quadrivium analysis also addresses, from a more "
            "measured perspective."
            "\\n\\n"
            "Taken together, Szulakowska's three books reveal a Maier who is more politically and "
            "theologically engaged than either De Jong's source-critical method or Tilton's Rosicrucian "
            "framing alone suggest. Read alongside Smith's artisanal-knowledge framework and Forshaw's "
            "mytho-alchemical analysis, Szulakowska's religious-political lens adds a dimension that enriches "
            "without displacing these other approaches. The classical surface of the Atalanta Fugiens, in her "
            "reading, conceals not merely chemical knowledge in allegorical form but a sacramental theology "
            "and a political program — registers that become visible only when the images are read against "
            "the full backdrop of Reformation religious controversy."
        )}
    </div>"""

    html = page_shell('Szulakowska on Maier', body, active_nav='Szulakowska')
    (SITE_DIR / 'szulakowska.html').write_text(html, encoding='utf-8')
    print("  szulakowska.html")


def build_maier_page(conn):
    """Build 'Emblems According to Maier' — each emblem with large image, epigram summary, and discourse summary."""

    emblems = conn.execute("""
        SELECT number, roman_numeral, canonical_label,
               motto_latin, motto_english, epigram_english,
               discourse_summary, alchemical_stage, image_description
        FROM emblems ORDER BY number
    """).fetchall()

    cards_html = ''
    for e in emblems:
        num, roman, label = e[0], e[1], e[2]
        motto_lat, motto_en, epigram = e[3], e[4], e[5]
        discourse, stage, img_desc = e[6], e[7], e[8]

        display = roman or 'Frontispiece'
        title = f'Emblem {display}' if roman else 'Frontispiece'
        fname = f'emblem-{num:02d}.jpg' if num >= 0 else 'emblem-00.jpg'
        link = f'emblems/emblem-{num:02d}.html' if num > 0 else 'emblems/frontispiece.html'

        # Stage badge
        stage_colors = {'NIGREDO': '#2c2418', 'ALBEDO': '#a89880', 'CITRINITAS': '#b8860b', 'RUBEDO': '#c0392b'}
        stage_fg = {'NIGREDO': '#f5f0e8', 'ALBEDO': '#2c2418', 'CITRINITAS': '#2c2418', 'RUBEDO': '#f5f0e8'}
        sbadge = ''
        if stage:
            bg = stage_colors.get(stage, '#7f8c8d')
            fg = stage_fg.get(stage, '#fff')
            sbadge = f'<span class="badge" style="background:{bg};color:{fg};font-size:0.8rem;padding:0.25rem 0.6rem;border-radius:3px;margin-left:0.5rem">{stage}</span>'

        # Epigram section
        epigram_html = ''
        if epigram and epigram.strip():
            epigram_html = f"""
                <div style="margin-bottom:1rem">
                    <h4 style="font-size:0.9rem;color:var(--accent);margin-bottom:0.4rem;font-family:var(--font-sans)">Epigram</h4>
                    <div style="font-style:italic;font-size:0.92rem;line-height:1.6;padding:0.6rem 1rem;background:var(--bg);border-left:3px solid var(--accent-light)">{epigram}</div>
                </div>"""

        # Discourse section
        discourse_html = ''
        if discourse and discourse.strip():
            discourse_html = f"""
                <div>
                    <h4 style="font-size:0.9rem;color:var(--accent);margin-bottom:0.4rem;font-family:var(--font-sans)">Maier's Discourse</h4>
                    <div style="font-size:0.92rem;line-height:1.7">{autolink_emblems(discourse)}</div>
                </div>"""

        # Motto block
        motto_html = ''
        if motto_lat:
            motto_html += f'<p style="font-style:italic;color:var(--accent);margin-bottom:0.2rem;font-size:0.95rem">{motto_lat}</p>'
        if motto_en:
            motto_html += f'<p style="margin-top:0;margin-bottom:1rem;font-size:0.95rem">{motto_en}</p>'

        cards_html += f"""
        <div class="ref-card" style="margin-bottom:2.5rem;padding:0;overflow:hidden" id="emblem-{num}">
            <div style="display:grid;grid-template-columns:minmax(250px, 1fr) 2fr;gap:0">
                <div style="padding:1rem;background:#faf8f4;display:flex;flex-direction:column;align-items:center;justify-content:flex-start">
                    <a href="{link}">
                        <img src="images/emblems/{fname}" alt="{title}" style="width:100%;max-width:350px;border-radius:4px;box-shadow:0 2px 8px rgba(0,0,0,0.12)">
                    </a>
                    <div style="margin-top:0.8rem;text-align:center">
                        <a href="{link}" style="font-size:0.85rem;color:var(--accent);font-family:var(--font-sans)">View full analysis &rarr;</a>
                    </div>
                </div>
                <div style="padding:1.5rem">
                    <h3 style="font-size:1.15rem;margin-bottom:0.3rem">{title} — {label}{sbadge}</h3>
                    {motto_html}
                    {epigram_html}
                    {discourse_html}
                </div>
            </div>
        </div>"""

    body = f"""
    <div class="page-content" style="max-width:1200px">
        <h1 style="font-size:1.8rem;margin-bottom:0.5rem">The Emblems According to Maier</h1>
        <p style="font-size:1.05rem;color:var(--text-muted);margin-bottom:0.5rem;line-height:1.6">
            Each of the fifty emblems of <em>Atalanta Fugiens</em> is accompanied by a Latin epigram
            and a two-page prose discourse in which Maier develops the alchemical meaning of the emblem's
            visual allegory. Here we present each emblem with its verse and a scholarly summary of the
            discourse argument, as Maier intended them to be encountered: image and text together,
            inviting the reader to meditate on the secrets of Nature.
        </p>
        <p style="font-size:0.85rem;color:var(--text-muted);margin-bottom:2rem;font-family:var(--font-sans)">
            51 emblems &middot; Click any image for the full scholarly analysis
        </p>
        <style>
            @media (max-width: 768px) {{
                .ref-card > div {{
                    grid-template-columns: 1fr !important;
                }}
            }}
        </style>
        {cards_html}
    </div>"""

    html = page_shell('The Emblems According to Maier', body, active_nav='Maier')
    (SITE_DIR / 'maier.html').write_text(html, encoding='utf-8')
    print(f"  maier.html: {len(emblems)} emblems")


def build_works_page():
    """Build the Scholarly Works page from merged staging JSON."""
    merged_path = BASE_DIR / 'staging' / 'works_merged.json'
    if not merged_path.exists():
        print("  works.html: skipped (no staging/works_merged.json)")
        return

    works_data = json.loads(merged_path.read_text(encoding='utf-8'))
    works = works_data.get('works', [])

    sections_html = ''
    for w in works:
        source_id = w.get('source_id', '')
        author = w.get('author', '')
        title = w.get('title', '')
        year = w.get('year', '')
        summary_html = w.get('summary_html', '')
        emblems = w.get('emblems_discussed', [])
        findings = w.get('key_findings', [])

        year_display = str(year) if year else 'n.d.'
        emblem_badges = ''
        if emblems:
            emblem_badges = '<div style="margin-top:0.5rem">' + ' '.join(
                f'<a href="emblems/emblem-{n:02d}.html" class="source-link" style="font-size:0.75rem">Emblem {n}</a>'
                if n > 0 else '<a href="emblems/frontispiece.html" class="source-link" style="font-size:0.75rem">Frontispiece</a>'
                for n in emblems
            ) + '</div>'

        findings_html = ''
        if findings:
            items = ''.join(f'<li style="font-size:0.85rem;margin-bottom:0.3rem">{f}</li>' for f in findings)
            findings_html = f'<div style="background:#faf8f4;padding:0.8rem 1rem;border-radius:4px;margin-top:1rem"><strong style="font-size:0.85rem;font-family:var(--font-sans)">Key Findings</strong><ul style="margin:0.5rem 0 0 1rem;padding:0">{items}</ul></div>'

        sections_html += f"""
        <div class="ref-card" style="margin-bottom:2rem;padding:1.5rem" id="{source_id}">
            <h3 style="font-size:1.1rem;margin-bottom:0.3rem;color:var(--accent)">{author} ({year_display})</h3>
            <p style="font-size:1rem;font-style:italic;margin-bottom:1rem">{title}</p>
            <div style="font-size:0.95rem;line-height:1.7">{summary_html}</div>
            {emblem_badges}
            {findings_html}
        </div>"""

    body = f"""
    <div class="page-content">
        <h1 style="font-size:1.8rem;margin-bottom:0.5rem">Scholarly Works on <em>Atalanta Fugiens</em></h1>
        <p style="font-size:1.05rem;color:var(--text-muted);margin-bottom:1.5rem;line-height:1.6">
            A curated library of secondary scholarship on Michael Maier's <em>Atalanta Fugiens</em>,
            from J.B. Craven's pioneering 1910 biography through the 2020 <em>Furnace and Fugue</em>
            digital edition. Each entry summarizes the work's arguments, methods, and specific
            contributions to understanding Maier's alchemical emblems.
        </p>
        <div class="ai-banner">Summaries assembled from corpus analysis and scholarly sources. Not reviewed by a human scholar.</div>
        <p style="font-size:0.9rem;color:var(--text-muted);margin-bottom:2rem">{len(works)} works surveyed, ordered chronologically.</p>
        {sections_html}
    </div>"""

    html = page_shell('Works', body, active_nav='Works')
    (SITE_DIR / 'works.html').write_text(html, encoding='utf-8')
    print(f"  works.html: {len(works)} scholarly works")


def build_music_page():
    """Build the Music page: recordings, performances, MIDI, and web resources."""

    body = """
    <div class="page-content">
        <h1 style="font-size:1.8rem;margin-bottom:0.3rem">Musical Recordings &amp; Performances</h1>
        <p style="font-size:1.1rem;color:var(--text-muted);margin-bottom:2rem;font-style:italic">
            The fifty three-voice fugues of <em>Atalanta Fugiens</em> &mdash; composed for Atalanta (soprano),
            Hippomenes (tenor), and the Golden Apple (cantus firmus) &mdash; represent the earliest known
            attempt to integrate musical composition into an alchemical emblem book.
        </p>
        <div class="ai-banner">This page assembles information from published sources, web resources, and scholarly references. Links were verified as of March 2026.</div>

        <h2>Recordings</h2>

        <div class="ref-card" style="margin-bottom:1rem">
            <h4>Ensemble Plus Ultra, dir. Michael Noone</h4>
            <p><strong>&ldquo;Maier: Atalanta Fugiens&rdquo;</strong> &mdash; Complete cycle of all 50 fugues (~71 minutes).
            Claudio Records CR5468, issued 2011. Booklet notes by Joscelyn Godwin. Available on
            Apple Music, Spotify, and other streaming platforms. This is the standard modern recording and the
            most widely cited commercial release.</p>
        </div>

        <div class="ref-card" style="margin-bottom:1rem">
            <h4>Joscelyn Godwin Edition Recording (1987)</h4>
            <p>The first complete recording of the fifty fugues, produced for Godwin's Magnum Opus Hermetic
            Sourceworks edition. Performed by <strong>Rachel Platt, Emily Van Evera, Rufus Muller, and Richard
            Wistreich</strong>. Originally issued on cassette tape; later remastered and released on CD by
            Claudio Records. The Godwin edition (Phanes Press, 1989) includes modern notation that has been
            the basis for most subsequent performances and digital realizations.</p>
        </div>

        <div class="ref-card" style="margin-bottom:1rem">
            <h4>Furnace and Fugue Vocal Recordings (2020)</h4>
            <p>Newly commissioned vocal recordings of all fifty fugues, produced for the
            <a href="https://furnaceandfugue.org" target="_blank" rel="noopener">Furnace and Fugue</a>
            digital edition (Brown University / University of Virginia Press, 2020). Streamable emblem-by-emblem
            within the interactive edition. These recordings are integrated with high-resolution images and
            searchable text, allowing synchronized experience of Maier's multi-sensory program.</p>
        </div>

        <div class="ref-card" style="margin-bottom:1rem">
            <h4>RIM c-Orchestra / David Kanaga (2021)</h4>
            <p><strong>&ldquo;Atalanta Fugiens 1&ndash;18&rdquo;</strong> &mdash; Electronic and experimental
            re-imagining of fugues 1 through 18. Released via Bandcamp. A creative interpretation rather than
            a historically informed performance.</p>
        </div>

        <div class="ref-card" style="margin-bottom:1rem">
            <h4>Camerata Mediolanense</h4>
            <p>Albums titled <em>Atalanta Fugiens</em> and <em>Atalanta Fugiens (Deluxe Edition)</em> &mdash;
            a free creative work inspired by Maier's themes rather than a direct realization of the 50 canons.
            Neo-medieval / dark ambient aesthetic.</p>
        </div>

        <h2>Known Performances</h2>

        <div class="ref-card" style="margin-bottom:1rem">
            <h4>International Conference on the History of Alchemy and Chymistry, Philadelphia (2006)</h4>
            <p>The conference &ldquo;commenced with a performance of the early music ensemble <strong>Arcanum</strong>,&rdquo;
            including three canons from Atalanta Fugiens, sung in Latin. Noted by Joscelyn Godwin as evidence
            that the work &ldquo;is an obligatory inclusion at any alchemical musical recital.&rdquo;</p>
        </div>

        <div class="ref-card" style="margin-bottom:1rem">
            <h4>Les Canards Chantants (2014&ndash;present)</h4>
            <p>This vocal ensemble has performed and workshopped Atalanta Fugiens regularly since 2014, in
            collaboration with historians Donna Bilak and Tara Nummedal. Their lecture-performances include
            events at the Bard Graduate Center with performance demonstrations exploring the relationship
            between singing, seeing, and alchemical meditation.</p>
        </div>

        <div class="ref-card" style="margin-bottom:1rem">
            <h4>MITO Festival (2020)</h4>
            <p>A performance project for the MITO SettembreMusica Festival, directed by <strong>Vanni Moretto</strong>.
            Documented in a four-video YouTube playlist titled &ldquo;Atalanta Fugiens a MITO 2020.&rdquo;</p>
        </div>

        <h2>MIDI Files &amp; Digital Realizations</h2>

        <div class="ref-card" style="margin-bottom:1rem">
            <h4>Adam McLean&rsquo;s Alchemy Website</h4>
            <p>The most comprehensive free source of MIDI files for Maier's fugues. The
            <a href="https://www.alchemywebsite.com/atalanta.html" target="_blank" rel="noopener">Atalanta Fugiens section</a>
            includes downloadable MIDI realizations for a substantial subset of the 50 fugues, each with a
            &ldquo;Save the MIDI file to your computer&rdquo; link. McLean also hosts the
            <a href="https://alchemywebsite.com/atalanta_thumbnails.html" target="_blank" rel="noopener">hand-coloured emblem plates</a>
            (1999) and the English translation from British Library MS Sloane 3645.</p>
        </div>

        <div class="ref-card" style="margin-bottom:1rem">
            <h4>BitMidi / MidiCities</h4>
            <p>Individual fugue MIDI downloads available for selected fugues, including No. 22 and No. 33.
            Searchable by title on BitMidi.com and MidiCities.com.</p>
        </div>

        <div class="ref-card" style="margin-bottom:1rem">
            <h4>Amaranth Publishing</h4>
            <p>Sells a notation and arrangement package of the Atalanta Fugiens with transcriptions.
            Useful as a source for creating custom MIDI realizations, though the files themselves are not free.</p>
        </div>

        <h2>Video &amp; Web Resources</h2>

        <div class="ref-card" style="margin-bottom:1rem">
            <h4>Furnace and Fugue Digital Edition</h4>
            <p><a href="https://furnaceandfugue.org" target="_blank" rel="noopener">furnaceandfugue.org</a> &mdash;
            The born-digital scholarly edition by Donna Bilak and Tara Nummedal (University of Virginia Press, 2020).
            Features interactive synchronized text, image, and music for all 50 emblems. Winner of the 2022
            Roy Rosenzweig Prize for Creativity in Digital History. Includes essays by Peter Forshaw on mytho-alchemy
            and Donna Bilak on steganography.</p>
        </div>

        <div class="ref-card" style="margin-bottom:1rem">
            <h4>Peter Forshaw: &ldquo;The Emblemata of the Atalanta Fugiens&rdquo;</h4>
            <p>Infinite Fire Webinar II, Ritman Library / University of Amsterdam (November 2012).
            A detailed scholarly lecture walking through individual emblems, discussing mytho-alchemy,
            the quadrivium structure of each discourse, and Maier's relationship to the emblem tradition.
            Available on YouTube via the Embassy of the Free Mind channel.</p>
        </div>

        <div class="ref-card" style="margin-bottom:1rem">
            <h4>&ldquo;Singing Nature&rsquo;s Secrets&rdquo; Lecture</h4>
            <p>Public lecture with live performances exploring Michael Maier's Atalanta Fugiens (1618)
            and the Furnace and Fugue digital edition (2020). Available on the Furnace and Fugue YouTube channel.</p>
        </div>

        <div class="ref-card" style="margin-bottom:1rem">
            <h4>MITO 2020 YouTube Playlist</h4>
            <p>&ldquo;Atalanta Fugiens a MITO 2020&rdquo; &mdash; Four-video playlist documenting Vanni Moretto's
            performance project for the MITO SettembreMusica Festival. Searchable on YouTube.</p>
        </div>

        <div class="ref-card" style="margin-bottom:1rem">
            <h4>YouTube Coloured Prints with Instrumental Music</h4>
            <p>A full set of 50 emblems with accompanying instrumental versions of the music has been uploaded
            to YouTube. Individual emblem videos pair Adam McLean's coloured prints with instrumental realizations
            of the corresponding fugues.</p>
        </div>

        <div class="ref-card" style="margin-bottom:1rem">
            <h4>Adam McLean's Alchemy Website</h4>
            <p><a href="https://www.alchemywebsite.com/atalanta.html" target="_blank" rel="noopener">alchemywebsite.com/atalanta.html</a> &mdash;
            The most comprehensive single web resource for <em>Atalanta Fugiens</em> outside of Furnace and Fugue.
            Hosts the English translation (from MS Sloane 3645, transcribed by Clay Holden, Hereward Tilton,
            and Peter Branwin), MIDI files, and hand-coloured plates.</p>
        </div>

        <h2>Scholarly Writing on the Music</h2>

        <div style="margin-bottom:1.5rem">
            <table style="width:100%;border-collapse:collapse;margin:1rem 0">
                <tr style="border-bottom:2px solid var(--border);font-family:var(--font-sans);font-size:0.85rem">
                    <th style="padding:0.5rem;text-align:left">Author</th>
                    <th style="padding:0.5rem;text-align:left">Work</th>
                    <th style="padding:0.5rem;text-align:left">Year</th>
                    <th style="padding:0.5rem;text-align:left">Focus</th>
                </tr>
                <tr style="border-bottom:1px solid var(--border)">
                    <td style="padding:0.5rem">Joscelyn Godwin</td>
                    <td style="padding:0.5rem"><em>Atalanta Fugiens: An Edition of the Fugues, Emblems, and Epigrams</em></td>
                    <td style="padding:0.5rem">1987</td>
                    <td style="padding:0.5rem">First modern musical edition with complete transcriptions and recording</td>
                </tr>
                <tr style="border-bottom:1px solid var(--border)">
                    <td style="padding:0.5rem">Joscelyn Godwin</td>
                    <td style="padding:0.5rem">&ldquo;Musical Alchemy: the Work of Composer and Listener&rdquo; (<em>Temenos</em>)</td>
                    <td style="padding:0.5rem">1985</td>
                    <td style="padding:0.5rem">Theoretical foundations of Maier's musical-alchemical synthesis</td>
                </tr>
                <tr style="border-bottom:1px solid var(--border)">
                    <td style="padding:0.5rem">Joscelyn Godwin</td>
                    <td style="padding:0.5rem">&ldquo;A Background for Michael Maier's Atalanta Fugiens&rdquo; (<em>Hermetic Journal</em>)</td>
                    <td style="padding:0.5rem">1985</td>
                    <td style="padding:0.5rem">Intellectual context for the musical emblem book</td>
                </tr>
                <tr style="border-bottom:1px solid var(--border)">
                    <td style="padding:0.5rem">Douglas Leedy</td>
                    <td style="padding:0.5rem">Review of Godwin edition (<em>Notes</em>)</td>
                    <td style="padding:0.5rem">1991</td>
                    <td style="padding:0.5rem">Technical musicological assessment of the fugues' sophistication</td>
                </tr>
                <tr style="border-bottom:1px solid var(--border)">
                    <td style="padding:0.5rem">C. Morris Wescott</td>
                    <td style="padding:0.5rem">&ldquo;Atalanta Fugiens&rdquo; (<em>AthanorX</em>)</td>
                    <td style="padding:0.5rem">n.d.</td>
                    <td style="padding:0.5rem">Modal-planetary correspondences; cantus firmus as structural anchor</td>
                </tr>
                <tr style="border-bottom:1px solid var(--border)">
                    <td style="padding:0.5rem">Peter Forshaw</td>
                    <td style="padding:0.5rem">&ldquo;Laboratorium, Auditorium, Oratorium&rdquo;</td>
                    <td style="padding:0.5rem">n.d.</td>
                    <td style="padding:0.5rem">Alchemical music including Maier's fugues and Khunrath's songs</td>
                </tr>
                <tr style="border-bottom:1px solid var(--border)">
                    <td style="padding:0.5rem">Johann F.W. Hasler</td>
                    <td style="padding:0.5rem">&ldquo;Performative and Multimedia Aspects of Late-Renaissance Meditative Alchemy&rdquo;</td>
                    <td style="padding:0.5rem">2011</td>
                    <td style="padding:0.5rem">AF as meditative practice; performance dimensions</td>
                </tr>
                <tr style="border-bottom:1px solid var(--border)">
                    <td style="padding:0.5rem">Bilak &amp; Nummedal (eds.)</td>
                    <td style="padding:0.5rem"><em>Furnace and Fugue</em></td>
                    <td style="padding:0.5rem">2020</td>
                    <td style="padding:0.5rem">Digital edition with newly commissioned vocal recordings of all 50 fugues</td>
                </tr>
            </table>
        </div>

        <h2>About the Fugues</h2>
        <p style="font-size:0.95rem;line-height:1.7">
            Each of the fifty emblems includes a three-voice fugue (more precisely, a canon) composed for
            three vocal parts. The three voices represent the dramatis personae of the overarching
            Atalanta myth: <strong>Atalanta</strong> (the fleeing volatile principle, typically the soprano),
            <strong>Hippomenes</strong> (the pursuing fixed principle, typically the tenor), and
            <strong>the Golden Apple</strong> (the catalytic agent, as the cantus firmus or bass).
            C. Morris Wescott has demonstrated that Maier's modal choices &mdash; Dorian, Phrygian,
            Mixolydian &mdash; correspond to planetary associations that relate to the alchemical stages
            depicted in each emblem's plate. The cantus firmus derives from the liturgical chant tradition,
            and the canons employ archaic compositional techniques including retrograde motion and mensural
            manipulation. Forty of the fifty fugues have been identified as based on compositions by
            the Elizabethan composer John Farmer.
        </p>
        <p style="font-size:0.95rem;line-height:1.7">
            Nothing is known about Maier's ideas on how the fugues were to be performed in practice,
            though some scholars believe they served as auditory support during corresponding alchemical
            work in the laboratory. Since Maier served as counsellor to Rudolf II, it is possible
            that the music was performed at the imperial court. The subtitle of the work promises
            compositions &ldquo;suitable for singing in couplets, to be looked at, read, meditated on,
            understood, weighed, sung, and listened to, not without a certain pleasure.&rdquo;
        </p>
    </div>"""

    html = page_shell('Music', body, active_nav='Music')
    (SITE_DIR / 'music.html').write_text(html, encoding='utf-8')
    print("  music.html")


# ============================================================
# Biography
# ============================================================

def build_biography():
    """Build Maier biography page from seed JSON."""
    seed_path = BASE_DIR / 'atalanta_fugiens_seed.json'
    if not seed_path.exists():
        print("  biography: skipped (no seed JSON)")
        return

    seed = json.loads(seed_path.read_text(encoding='utf-8'))
    bio = seed.get('biography')
    if not bio:
        print("  biography: skipped (no biography data)")
        return

    sections_html = ''
    for section in bio.get('sections', []):
        heading = section.get('heading', '')
        content = section.get('content', '')
        # Convert newlines to paragraphs
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        para_html = ''.join(f'<p style="font-size:0.95rem;line-height:1.7;margin-bottom:1rem">{p}</p>' for p in paragraphs)
        sections_html += f"""
        <h2>{heading}</h2>
        {para_html}"""

    body = f"""
    <div class="page-content">
        <h1 style="font-size:1.8rem;margin-bottom:0.3rem">{bio.get('title', 'Michael Maier')}</h1>
        <p style="font-size:1.1rem;color:var(--text-muted);margin-bottom:2rem;font-style:italic">{bio.get('subtitle', '')}</p>
        <div class="ai-banner">Biography assembled from Craven (1910), Tilton (2003), and De Jong (1969). Not reviewed by a human scholar.</div>
        {sections_html}
    </div>"""
    html = page_shell('Biography', body, active_nav='Biography')
    (SITE_DIR / 'biography.html').write_text(html, encoding='utf-8')
    print(f"  biography.html: {len(bio.get('sections', []))} sections")


# ============================================================
# Main
# ============================================================

def main():
    conn = sqlite3.connect(DB_PATH)
    print("Building site...")
    identity_map = load_identity_map(conn)
    export_data_json(conn, identity_map)
    build_gallery(conn)
    build_emblem_pages(conn, identity_map)
    build_scholars_pages(conn)
    build_bibliography(conn)
    build_dictionary_pages(conn)
    build_timeline(conn)
    build_sources(conn)
    build_essays(conn)
    build_maier_page(conn)
    build_works_page()
    build_szulakowska_page()
    build_music_page()
    build_biography()
    build_about(conn)
    conn.close()
    print("Site build complete.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
