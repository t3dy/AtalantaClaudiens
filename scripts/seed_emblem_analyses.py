"""
seed_emblem_analyses.py — Assemble structured analysis HTML for each emblem
from existing database content (motto, discourse, scholarly refs, sources, terms).

Deterministic: no LLM calls. Assembles template from DB fields.
Idempotent: overwrites analysis_html on each run.
"""

import sqlite3
import html
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "atalanta.db"

AI_BANNER = (
    '<div class="ai-banner">Assembled from De Jong (1969) corpus extraction. '
    'Not reviewed by a human scholar. Citations should be verified against original sources.</div>'
)


def esc(text):
    """HTML-escape text, return empty string for None."""
    if not text:
        return ''
    return html.escape(str(text))


def build_analysis(conn, emblem_id, num, roman, motto, discourse):
    """Build analysis HTML for one emblem."""
    sections = []

    # --- Overview ---
    if motto:
        overview = f'<p>Emblem {roman or "F"} bears the motto: <em>"{esc(motto[:300])}"</em></p>'
    else:
        overview = f'<p>Emblem {roman or "F"}.</p>'
    sections.append(f'<h3>Overview</h3>\n{overview}')

    # --- Source Texts ---
    sources = conn.execute("""
        SELECT sa.name, sa.authority_id, sa.type, es.relationship_type
        FROM emblem_sources es
        JOIN source_authorities sa ON es.authority_id = sa.id
        WHERE es.emblem_id = ?
        ORDER BY es.relationship_type, sa.name
    """, (emblem_id,)).fetchall()

    if sources:
        motto_sources = [s for s in sources if s[3] == 'MOTTO_SOURCE']
        disc_sources = [s for s in sources if s[3] != 'MOTTO_SOURCE']

        parts = []
        if motto_sources:
            names = ', '.join(
                f'<a href="../sources.html#{s[1]}" class="cross-link">{esc(s[0])}</a>'
                for s in motto_sources
            )
            parts.append(f'De Jong identifies the motto source as {names}.')
        if disc_sources:
            names = ', '.join(
                f'<a href="../sources.html#{s[1]}" class="cross-link">{esc(s[0])}</a>'
                for s in disc_sources
            )
            parts.append(f'The discourse draws on {names}.')

        sections.append(f'<h3>Maier\'s Source Texts</h3>\n<p>{" ".join(parts)}</p>')

    # --- Scholarly Commentary Summary ---
    refs = conn.execute("""
        SELECT sr.summary, b.author, sr.confidence
        FROM scholarly_refs sr
        JOIN bibliography b ON sr.bib_id = b.id
        WHERE sr.emblem_id = ?
        ORDER BY b.af_relevance, sr.confidence
        LIMIT 3
    """, (emblem_id,)).fetchall()

    if refs:
        ref_parts = []
        for summary, author, conf in refs:
            if summary:
                # Take first 200 chars of summary
                short = summary[:200] + ('...' if len(summary) > 200 else '')
                ref_parts.append(f'{esc(author)} notes: {esc(short)}')
        if ref_parts:
            sections.append(
                '<h3>Alchemical Significance</h3>\n<p>' +
                '</p>\n<p>'.join(ref_parts) + '</p>'
            )

    # --- Related Dictionary Terms ---
    terms = conn.execute("""
        SELECT dt.slug, dt.label, dt.label_latin
        FROM term_emblem_refs ter
        JOIN dictionary_terms dt ON ter.term_id = dt.id
        WHERE ter.emblem_id = ?
        ORDER BY dt.label
    """, (emblem_id,)).fetchall()

    if terms:
        term_links = ', '.join(
            f'<a href="../dictionary/{t[0]}.html" class="cross-link">{esc(t[1])}'
            f'{" (" + esc(t[2]) + ")" if t[2] and t[2] != t[1] else ""}</a>'
            for t in terms
        )
        sections.append(f'<h3>Related Terms</h3>\n<p>{term_links}</p>')

    if not sections:
        return None

    return (
        '<div class="emblem-analysis">\n'
        f'{AI_BANNER}\n'
        + '\n'.join(f'<section>\n{s}\n</section>' for s in sections)
        + '\n</div>'
    )


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    emblems = conn.execute("""
        SELECT id, number, roman_numeral, motto_english, discourse_summary
        FROM emblems WHERE number > 0
        ORDER BY number
    """).fetchall()

    updated = 0
    for eid, num, roman, motto, discourse in emblems:
        analysis = build_analysis(conn, eid, num, roman, motto, discourse)
        if analysis:
            conn.execute(
                "UPDATE emblems SET analysis_html = ? WHERE id = ?",
                (analysis, eid)
            )
            updated += 1

    conn.commit()

    # Report
    with_analysis = conn.execute(
        "SELECT COUNT(*) FROM emblems WHERE analysis_html IS NOT NULL"
    ).fetchone()[0]
    conn.close()

    print(f"  Emblem analyses: {with_analysis}/50 generated ({updated} updated)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
