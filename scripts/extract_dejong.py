"""
extract_dejong.py — Parse De Jong's emblem-by-emblem analysis from the markdown file.

Strategy:
  1. Read the full file and split by page markers (## Page N)
  2. Identify emblem section starts by finding EMBLEM headers followed by MOTTO
  3. Extract motto, epigram, discourse summary, source of motto, commentary
  4. Store in emblems (updates), scholarly_refs, emblem_sources

Source method: CORPUS_EXTRACTION
Confidence: HIGH for mottos/sources, MEDIUM for summaries
"""

import re
import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "atalanta.db"

# Find the De Jong markdown
SOURCE_DIR = BASE_DIR / "atalanta fugiens"
DJ_FILE = None
for f in SOURCE_DIR.glob("Helena Maria*Jong*.md"):
    DJ_FILE = f
    break

# Roman numeral helpers
ROMAN_VALS = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}

def roman_to_int(s):
    s = s.strip().upper()
    total = 0
    for i, c in enumerate(s):
        v = ROMAN_VALS.get(c, 0)
        if i + 1 < len(s) and v < ROMAN_VALS.get(s[i + 1], 0):
            total -= v
        else:
            total += v
    return total


def int_to_roman(num):
    """Convert integer to Roman numeral."""
    vals = [(50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
    result = ''
    for v, s in vals:
        while num >= v:
            result += s
            num -= v
    return result


def clean_ocr(text):
    """OCR cleanup: fix run-together words and common artifacts."""
    # Remove page markers
    text = re.sub(r'## Page \d+', '', text)
    # Remove running headers (e.g., "64 EMBLEMII", "EMBLEMIII 69")
    text = re.sub(r'\d+\s*EMBLEM\s*[IVXLCDM]+', '', text)
    text = re.sub(r'EMBLEM\s*[IVXLCDM]+\s*\d+', '', text)

    # Fix common run-togethers at word boundaries (lowercase-uppercase)
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    # Fix missing spaces after periods
    text = re.sub(r'\.([A-Z])', r'. \1', text)
    # Fix missing spaces after commas
    text = re.sub(r',([A-Za-z])', r', \1', text)
    # Fix missing spaces after semicolons
    text = re.sub(r';([A-Za-z])', r'; \1', text)
    # Fix missing spaces after closing parens
    text = re.sub(r'\)([A-Za-z])', r') \1', text)

    # Common OCR-specific fixes for run-together lowercase words
    # Pattern: lowercase letter immediately followed by common word starts
    common_words = (
        'the|that|this|and|but|for|not|with|from|into|also|which|have|has|'
        'was|were|are|his|her|its|who|how|one|all|can|may|must|will|'
        'it|is|in|of|to|as|at|by|on|or|be|so|if|he|an|up|do|no'
    )
    text = re.sub(
        rf'([a-z])({common_words})(?=[^a-z]|$)',
        lambda m: m.group(1) + ' ' + m.group(2) if len(m.group(1) + m.group(2)) > 3 else m.group(0),
        text
    )

    # Fix hyphenated line breaks: "some- thing" -> "something"
    text = re.sub(r'(\w)- (\w)', r'\1\2', text)

    # Collapse multiple spaces and clean
    text = re.sub(r'  +', ' ', text)
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    return text.strip()


def extract_between(text, start_pattern, end_patterns):
    """Extract text between a start marker and the first matching end marker."""
    start_match = re.search(start_pattern, text, re.IGNORECASE)
    if not start_match:
        return None, text

    rest = text[start_match.end():]

    # Find earliest end marker
    earliest_pos = len(rest)
    for pat in end_patterns:
        m = re.search(pat, rest, re.IGNORECASE)
        if m and m.start() < earliest_pos:
            earliest_pos = m.start()

    extracted = rest[:earliest_pos].strip()
    return clean_ocr(extracted), rest[earliest_pos:]


def find_emblem_sections(text):
    """
    Find emblem section starts. A real section start has EMBLEM + numeral
    followed by MOTTO within ~300 chars (may be on a different line).
    Running page headers don't have MOTTO nearby.
    """
    sections = []

    # Find all EMBLEM + roman numeral occurrences
    # Handle OCR noise: digits, tildes, periods mixed in before/after
    # Match EMBLEM + roman numeral, with word boundary after numeral
    # to avoid EMBLEMXVI matching as XV + trailing I
    emblem_pattern = re.compile(r'EMBLEM\s*([IVXLCDM]+)(?=[^IVXLCDM]|$)', re.IGNORECASE)

    for m in emblem_pattern.finditer(text):
        roman = m.group(1).upper()
        num = roman_to_int(roman)
        if not (1 <= num <= 50):
            continue

        # Check if MOTTO appears within 500 chars after this match
        # Allow OCR variants: "MOTTO", "MO TTO", "M OTTO", "MOTTOIf", "wean MOTTO"
        lookahead = text[m.end():m.end() + 500]
        motto_match = re.search(r'M\s*O\s*T\s*T\s*O', lookahead, re.IGNORECASE)
        if not motto_match:
            # Also check next few lines for MOTTO on a separate line
            # (handles cases like EMBLEM\n(fig N) MOTTO)
            lookahead_extended = text[m.end():m.end() + 800]
            motto_match = re.search(r'M\s*O\s*T\s*T\s*O', lookahead_extended, re.IGNORECASE)
        if motto_match:
            motto_pos = m.end() + motto_match.end()
            sections.append({
                'number': num,
                'roman': roman,
                'start': m.start(),
                'motto_start': motto_pos,
            })

    # Recovery pass: find garbled EMBLEM headers that the main regex misses.
    # These have OCR damage to the word EMBLEM itself but valid (fig N) MOTTO nearby.
    # Pattern: "(fig/fie NN) MOTTO" or "(fig NN) M OTTO" preceded by garbled text
    fig_motto_pattern = re.compile(
        r'\(fi[eg]\s*(\d+)\)\s*M\s*O\s*T\s*T\s*O', re.IGNORECASE
    )
    found_numbers = {s['number'] for s in sections}
    for m in fig_motto_pattern.finditer(text):
        fig_num = int(m.group(1))
        if fig_num < 1 or fig_num > 50:
            continue
        if fig_num in found_numbers:
            continue
        # Only accept if in the analysis section
        if m.start() < 20000:
            continue
        motto_pos = m.end()
        # Use fig_num position as section start (approximate)
        # Look back up to 200 chars to find start of line
        line_start = text.rfind('\n', max(0, m.start() - 200), m.start())
        if line_start == -1:
            line_start = m.start() - 100
        sections.append({
            'number': fig_num,
            'roman': int_to_roman(fig_num),
            'start': line_start,
            'motto_start': motto_pos,
        })
        found_numbers.add(fig_num)

    # Deduplicate — for each emblem number, collect all candidates
    # then pick the best one based on position ordering
    from collections import defaultdict
    candidates = defaultdict(list)
    for s in sections:
        candidates[s['number']].append(s)

    # The emblem analysis in De Jong runs pages 51-310, roughly positions
    # 25000-700000+. Emblems appear in order. For each emblem number,
    # prefer the candidate in the emblem-analysis section (text position > 20000)
    # and with MOTTO closest to the EMBLEM header.
    seen = {}
    for n in sorted(candidates.keys()):
        cands = candidates[n]
        # Filter to candidates likely in the analysis section (not intro references)
        analysis_cands = [c for c in cands if c['start'] > 20000]
        if not analysis_cands:
            analysis_cands = cands

        # Among analysis candidates, pick the one with MOTTO closest to header
        best = min(analysis_cands, key=lambda c: c['motto_start'] - c['start'])
        seen[n] = best

    # Sort by text position (file order) to ensure section boundaries are correct
    return sorted(seen.values(), key=lambda x: x['start'])


def find_frontispiece(text):
    """Find the frontispiece analysis section."""
    # Look for "FRONTISPIECE" or the Atalanta narrative section
    m = re.search(r'(?:THE\s+)?FRONTISPIECE', text, re.IGNORECASE)
    if m:
        return m.start()
    return None


def parse_emblem_section(text, section, next_start=None):
    """Extract structured data from one emblem section."""
    # Use a generous window for extraction. De Jong's analysis per emblem
    # can span 4-10 pages (~3000-8000 chars). The next_start boundary
    # from section-finding may be too tight (e.g., a running header for the
    # NEXT emblem may appear before the current emblem's SUMMARY section).
    # Use max(next_start + 2000, motto_start + 8000) to catch overflow.
    end = section['motto_start'] + 8000
    if next_start and next_start > section['motto_start']:
        # Extend 2000 chars past the next section start to catch
        # SUMMARY/SOURCE/COMMENTARY that bleeds past the boundary
        end = max(next_start + 2000, end)
    section_text = text[section['motto_start']:end]

    result = {
        'number': section['number'],
        'roman': section['roman'],
        'motto': None,
        'epigram': None,
        'discourse_summary': None,
        'source_of_motto': None,
        'commentary': None,
        'source_authorities': [],
    }

    # OCR-tolerant section header patterns
    # XXXIX has "SUl\'IMA.RYOF" for SUMMARY, XLI has "THEDISCOURSE" (no space)
    PAT_EPIGRAM = r'E\s*P\s*I\s*G\s*R\s*A\s*M'
    PAT_SUMMARY = r'(?:SUMMARY|SU.{0,6}ARY)\s*(?:OF)?\s*THE\s*DIS\s*COURSE'
    PAT_SOURCE = r'SOURCE\s+OF\s+THE\s*M\s*O\s*T\s*T\s*O'
    PAT_COMMENTARY = r'COM\s*M?\s*ENTARY'

    # Extract MOTTO (text before EPIGRAM)
    motto_text, remaining = extract_between(
        section_text,
        r'^',  # start of section_text (after MOTTO marker)
        [PAT_EPIGRAM, PAT_SUMMARY, r'SOURCE\s+OF']
    )
    if motto_text:
        # Clean up page numbers and running headers
        motto_text = re.sub(r'\d+\s*EMBLEM\s*[IVXLCDM]+', '', motto_text)
        motto_text = re.sub(r'## Page \d+', '', motto_text)
        result['motto'] = clean_ocr(motto_text).strip()

    # Extract EPIGRAM
    epigram, _ = extract_between(
        section_text,
        PAT_EPIGRAM,
        [PAT_SUMMARY, PAT_SOURCE, PAT_COMMENTARY]
    )
    if epigram:
        epigram = re.sub(r'\d+\s*EMBLEM\s*[IVXLCDM]+', '', epigram)
        epigram = re.sub(r'## Page \d+', '', epigram)
        result['epigram'] = clean_ocr(epigram).strip()

    # Extract SUMMARY OF THE DISCOURSE
    discourse, _ = extract_between(
        section_text,
        PAT_SUMMARY,
        [PAT_SOURCE, PAT_COMMENTARY]
    )
    if discourse:
        discourse = re.sub(r'\d+\s*EMBLEM\s*[IVXLCDM]+', '', discourse)
        discourse = re.sub(r'## Page \d+', '', discourse)
        result['discourse_summary'] = clean_ocr(discourse).strip()

    # Extract SOURCE OF THE MOTTO
    source, _ = extract_between(
        section_text,
        PAT_SOURCE,
        [PAT_COMMENTARY, r'EMBLEM\s*[IVXLCDM]+\s*(?:\(fig)?']
    )
    if source:
        source = re.sub(r'\d+\s*EMBLEM\s*[IVXLCDM]+', '', source)
        source = re.sub(r'## Page \d+', '', source)
        result['source_of_motto'] = clean_ocr(source).strip()

    # Extract COMMENTARY
    commentary, _ = extract_between(
        section_text,
        PAT_COMMENTARY,
        [r'EMBLEM\s*[IVXLCDM]+\s*\(fig']
    )
    if commentary:
        commentary = re.sub(r'\d+\s*EMBLEM\s*[IVXLCDM]+', '', commentary)
        commentary = re.sub(r'## Page \d+', '', commentary)
        result['commentary'] = clean_ocr(commentary).strip()

    # Identify source authorities mentioned
    full_text = section_text.lower()
    authority_patterns = [
        ('AUTH_TABULA_SMARAGDINA', r'tabula?\s*s(?:ma|rnara)'),
        ('AUTH_TURBA', r'turb[ao]\s*(?:phil|p/z)'),
        ('AUTH_ROSARIUM', r'rosar(?:ium|imn)\s*(?:phil|p/z)'),
        ('AUTH_PSEUDO_ARISTOTLE', r'(?:pseudo.?)?aristotle|tractatulus'),
        ('AUTH_SENIOR', r'senior(?:\s+zadith)?|tabula\s*chimica'),
        ('AUTH_OVID', r'ovid|metamorphos'),
        ('AUTH_AURORA', r'aurora\s*consurgens'),
        ('AUTH_SOLOMONIC', r'proverbs|solomon|sapienti'),
        ('AUTH_LAMBSPRINCK', r'lambsprinck|lambspring'),
        ('AUTH_MERLINI', r'merlini'),
        ('AUTH_LULLIUS', r'lull(?:ius|y)|r\.?\s*lull'),
        ('AUTH_LACTANTIUS', r'lactantius'),
        ('AUTH_ROBERTUS_VALLENSIS', r'robertus\s*vallensis|veritate.*antiquitate'),
        ('AUTH_JODOCUS_GREVERUS', r'jodocus\s*greverus|secretum\s*nobiliss'),
    ]

    for auth_id, pattern in authority_patterns:
        if re.search(pattern, full_text):
            result['source_authorities'].append(auth_id)

    return result


def update_database(conn, results):
    """Write extraction results to the database."""
    # Get De Jong bibliography ID
    dj_row = conn.execute(
        "SELECT id FROM bibliography WHERE source_id = 'de_jong_1969'"
    ).fetchone()
    if not dj_row:
        print("ERROR: de_jong_1969 not found in bibliography. Run seed_from_json.py first.")
        return 0, 0

    dj_bib_id = dj_row[0]

    refs_inserted = 0
    sources_inserted = 0
    emblems_updated = 0

    for r in results:
        # Get emblem row
        emblem_row = conn.execute(
            "SELECT id FROM emblems WHERE number = ?", (r['number'],)
        ).fetchone()
        if not emblem_row:
            continue
        emblem_id = emblem_row[0]

        # Update emblem with extracted data
        updates = {}
        if r['motto']:
            updates['motto_english'] = r['motto'][:500]
        if r['epigram']:
            updates['epigram_english'] = r['epigram'][:2000]
        if r['discourse_summary']:
            updates['discourse_summary'] = r['discourse_summary'][:3000]

        if updates:
            set_clause = ', '.join(f"{k} = ?" for k in updates)
            values = list(updates.values()) + [emblem_id]
            conn.execute(
                f"UPDATE emblems SET {set_clause}, source_method = 'CORPUS_EXTRACTION', "
                f"confidence = 'HIGH' WHERE id = ?",
                values
            )
            emblems_updated += 1

        # Insert scholarly ref (De Jong's analysis)
        summary_parts = []
        if r['source_of_motto']:
            summary_parts.append(f"Source: {r['source_of_motto'][:500]}")
        if r['commentary']:
            summary_parts.append(r['commentary'][:1500])
        elif r['discourse_summary']:
            summary_parts.append(r['discourse_summary'][:1000])

        if summary_parts:
            summary = ' | '.join(summary_parts)
            auth_json = json.dumps(r['source_authorities'])

            existing = conn.execute(
                "SELECT id FROM scholarly_refs WHERE emblem_id = ? AND bib_id = ? AND confidence = 'HIGH'",
                (emblem_id, dj_bib_id)
            ).fetchone()

            if not existing:
                conn.execute("""
                    INSERT INTO scholarly_refs
                        (emblem_id, bib_id, interpretation_type, summary,
                         source_texts_referenced, confidence)
                    VALUES (?, ?, 'ALCHEMICAL', ?, ?, 'HIGH')
                """, (emblem_id, dj_bib_id, summary, auth_json))
                refs_inserted += 1

        # Insert emblem_sources for identified authorities
        for auth_id in r['source_authorities']:
            auth_row = conn.execute(
                "SELECT id FROM source_authorities WHERE authority_id = ?",
                (auth_id,)
            ).fetchone()
            if not auth_row:
                continue

            existing = conn.execute(
                "SELECT id FROM emblem_sources WHERE emblem_id = ? AND authority_id = ?",
                (emblem_id, auth_row[0])
            ).fetchone()
            if not existing:
                # Determine relationship type
                rel_type = 'DISCOURSE_CITATION'
                if r['source_of_motto'] and auth_id.lower() in (r.get('source_of_motto', '') or '').lower():
                    rel_type = 'MOTTO_SOURCE'

                conn.execute("""
                    INSERT INTO emblem_sources
                        (emblem_id, authority_id, relationship_type, confidence)
                    VALUES (?, ?, ?, 'HIGH')
                """, (emblem_id, auth_row[0], rel_type))
                sources_inserted += 1

    return emblems_updated, refs_inserted, sources_inserted


def main():
    if not DJ_FILE or not DJ_FILE.exists():
        print(f"ERROR: De Jong markdown not found in {SOURCE_DIR}")
        return 1

    print(f"Reading: {DJ_FILE.name}")
    text = DJ_FILE.read_text(encoding="utf-8", errors="replace")
    print(f"  {len(text)} chars, {text.count(chr(10))} lines")

    # Find emblem sections
    sections = find_emblem_sections(text)
    print(f"  Found {len(sections)} emblem section starts")

    if not sections:
        print("ERROR: No emblem sections found. Check regex patterns.")
        return 1

    # Parse each section
    results = []
    for i, section in enumerate(sections):
        next_start = sections[i + 1]['start'] if i + 1 < len(sections) else None
        result = parse_emblem_section(text, section, next_start)
        results.append(result)

        has_fields = sum(1 for k in ['motto', 'epigram', 'discourse_summary', 'source_of_motto', 'commentary']
                        if result.get(k))
        authorities = len(result['source_authorities'])
        print(f"  Emblem {result['roman']:>5}: {has_fields}/5 fields, {authorities} authorities")

    # Update database
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    emblems_updated, refs_inserted, sources_inserted = update_database(conn, results)

    conn.commit()

    # Report
    total_emblems = conn.execute("SELECT COUNT(*) FROM emblems").fetchone()[0]
    with_motto = conn.execute(
        "SELECT COUNT(*) FROM emblems WHERE motto_english IS NOT NULL"
    ).fetchone()[0]
    with_discourse = conn.execute(
        "SELECT COUNT(*) FROM emblems WHERE discourse_summary IS NOT NULL"
    ).fetchone()[0]
    total_refs = conn.execute("SELECT COUNT(*) FROM scholarly_refs").fetchone()[0]
    total_sources = conn.execute("SELECT COUNT(*) FROM emblem_sources").fetchone()[0]

    conn.close()

    print(f"\nResults:")
    print(f"  Emblem sections parsed: {len(results)}")
    print(f"  Emblems updated: {emblems_updated}")
    print(f"  Scholarly refs inserted: {refs_inserted}")
    print(f"  Emblem-source links inserted: {sources_inserted}")
    print(f"\nDatabase totals:")
    print(f"  Emblems: {total_emblems} ({with_motto} with motto, {with_discourse} with discourse)")
    print(f"  Scholarly refs: {total_refs}")
    print(f"  Emblem-source links: {total_sources}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
