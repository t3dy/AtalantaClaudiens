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
    ('Essays', 'essays/index.html'),
    ('Bibliography', 'bibliography.html'),
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


def confidence_badge(level):
    if not level: return ''
    cls = f'confidence-{level.lower()}'
    return f'<span class="badge {cls}">{level}</span>'


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
    body = f"""
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
        body = f"""
    <div class="emblem-detail">
        <div class="emblem-nav">
            <span>{prev_link}</span>
            <a href="../">Gallery</a>
            <span>{next_link}</span>
        </div>

        <h1 style="font-size:1.8rem;margin-bottom:1.5rem">{title} — {label}</h1>

        <div class="comparative-view">
            <div class="source-panel">
                <h2>Original Source</h2>
                {(lambda p, e: f'<img src="../{p}" alt="Emblem {display_num}" class="emblem-plate">' if e else f'<div class="placeholder-img">{display_num}</div>')(*resolve_image(identity_map, num))}
                {f'<div class="motto-block">{motto_en}</div>' if motto_en else '<p style="color:var(--text-muted)"><em>Motto not yet extracted</em></p>'}
                {f'<details style="margin-bottom:1.5rem"><summary style="cursor:pointer;color:var(--accent);font-family:var(--font-sans)">Epigram</summary><div class="epigram-block">{epigram}</div></details>' if epigram else ''}
                {f'<div class="discourse-block"><h3 style="font-size:1rem;color:var(--accent);margin-bottom:0.5rem">Discourse Summary</h3><p style="font-size:0.92rem">{discourse[:1500]}{"..." if discourse and len(discourse) > 1500 else ""}</p></div>' if discourse else ''}
                {analysis_html if analysis_html else ''}
                {f'<p><span class="badge badge-stage">{stage}</span></p>' if stage else ''}
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
    grid_html = ''
    for e in emblems:
        num, roman, label = e[1], e[2], e[3]
        motto = e[5] or ''
        fname = 'frontispiece.html' if num == 0 else f'emblem-{num:02d}.html'
        display = roman or 'F'
        has_data = '&#10003;' if e[5] else '&middot;'
        img_path, img_exists = resolve_image(identity_map, num)
        if img_exists:
            img_tag = f'<img src="../{img_path}" alt="Emblem {display}" style="width:100%;aspect-ratio:auto;display:block">'
        else:
            img_tag = f'<div class="card-placeholder" style="aspect-ratio:1;font-size:2rem">{display}</div>'
        grid_html += f"""
        <a href="{fname}" class="card" style="text-decoration:none;color:inherit">
            {img_tag}
            <div class="card-body">
                <div class="card-sig">{display}. {label}</div>
                <div class="card-desc">{motto[:80]}{'...' if len(motto) > 80 else ''}</div>
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
        <table style="width:100%;border-collapse:collapse;margin:1rem 0">
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
        </table>

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
        <div class="card" onclick="location.href='scholar/{slug}.html'" style="cursor:pointer">
            <div class="card-body">
                <div class="card-sig">{name}</div>
                <div class="card-label">{spec or ''}</div>
                <div class="card-desc">{focus or ''}</div>
                <div style="margin-top:0.5rem;font-size:0.8rem;color:var(--text-muted);font-family:var(--font-sans)">
                    {work_count} work{'s' if work_count != 1 else ''} &middot; {ref_count} emblem{'s' if ref_count != 1 else ''} covered
                </div>
            </div>
        </div>"""

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
            {f'<p style="margin-bottom:1.5rem">{focus}</p>' if focus else ''}
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
        SELECT source_id, author, title, year, journal, publisher, pub_type, af_relevance, in_collection
        FROM bibliography ORDER BY year
    """).fetchall()

    rows_html = ''
    for e in entries:
        src_id, author, title, year, journal, pub, ptype, rel, incoll = e
        rel_badge = f'<span class="badge badge-{"primary" if rel == "PRIMARY" else "direct" if rel == "DIRECT" else "contextual"}">{rel}</span>'
        venue = journal or pub or ''
        rows_html += f"""
        <div class="ref-card">
            <h4>{author} ({year or '?'}) {rel_badge}</h4>
            <p><em>{title}</em></p>
            <p style="font-size:0.8rem;color:var(--text-muted)">{venue} &middot; {ptype or ''}</p>
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
               significance_to_af, source_basis, review_status, label_latin
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
    html = page_shell('Dictionary', body, active_nav='Dictionary')
    (dict_dir / 'index.html').write_text(html, encoding='utf-8')

    # Individual term pages
    for t in terms:
        tid, slug, label, cat, def_short, def_long, sig, basis, status, label_latin = t

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
            {f'<div style="margin-bottom:1.5rem"><p style="font-size:0.95rem;line-height:1.7">{def_long}</p></div>' if def_long else ''}
            {f'<h2>In <em>Atalanta Fugiens</em></h2><p style="font-size:0.95rem;line-height:1.7">{sig}</p>' if sig else ''}
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
    build_about(conn)
    conn.close()
    print("Site build complete.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
