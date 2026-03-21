"""
extract_dejong_pass2.py — Second pass extraction for emblems missed by regex.

For the 13 emblems where OCR garbled the EMBLEM+MOTTO pattern beyond
recognition, this script uses De Jong's known page order to find
emblem sections by page range.

De Jong's book analyzes emblems in order, roughly pages 50-330.
Each emblem gets ~4-8 pages. We can locate missing sections by
finding them between known sections.

Idempotent: updates only NULL fields.
"""

import re
import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "atalanta.db"
SOURCE_DIR = BASE_DIR / "atalanta fugiens"

DJ_FILE = None
for f in SOURCE_DIR.glob("Helena Maria*Jong*.md"):
    DJ_FILE = f
    break

ROMAN_VALS = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}

def roman_to_int(s):
    if not s: return 0
    s = s.strip().upper()
    total = 0
    for i, c in enumerate(s):
        v = ROMAN_VALS.get(c, 0)
        if i + 1 < len(s) and v < ROMAN_VALS.get(s[i + 1], 0):
            total -= v
        else:
            total += v
    return total

def clean_ocr(text):
    """OCR cleanup."""
    text = re.sub(r'## Page \d+', '', text)
    text = re.sub(r'\d+\s*EMBLEM\s*[IVXLCDM]+', '', text)
    text = re.sub(r'EMBLEM\s*[IVXLCDM]+\s*\d+', '', text)
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    text = re.sub(r'\.([A-Z])', r'. \1', text)
    text = re.sub(r',([A-Za-z])', r', \1', text)
    text = re.sub(r';([A-Za-z])', r'; \1', text)
    text = re.sub(r'\)([A-Za-z])', r') \1', text)
    text = re.sub(r'(\w)- (\w)', r'\1\2', text)
    text = re.sub(r'  +', ' ', text)
    return text.strip()


def find_page_positions(text):
    """Map page numbers to character positions."""
    pages = {}
    for m in re.finditer(r'## Page (\d+)', text):
        pages[int(m.group(1))] = m.start()
    return pages


def extract_motto_from_chunk(chunk):
    """Try to find a MOTTO in a text chunk, even with OCR noise."""
    # Look for MOTTO or MO TTO or M OTTO patterns
    m = re.search(r'M\s*O\s*T\s*T\s*O\s*(.*?)(?:E\s*P\s*I\s*G\s*R\s*A\s*M|SUMMARY|$)',
                  chunk, re.DOTALL | re.IGNORECASE)
    if m:
        motto = m.group(1).strip()
        # Take first sentence/line
        motto = re.split(r'\n', motto)[0].strip()
        if len(motto) > 10:
            return clean_ocr(motto)
    return None


def extract_epigram_from_chunk(chunk):
    """Try to find EPIGRAM content."""
    m = re.search(r'E\s*P\s*I\s*G\s*R\s*A\s*M\s*(.*?)(?:SUMMARY|SOURCE|$)',
                  chunk, re.DOTALL | re.IGNORECASE)
    if m:
        text = m.group(1).strip()
        if len(text) > 10:
            return clean_ocr(text[:1000])
    return None


def extract_summary_from_chunk(chunk):
    """Try to find SUMMARY OF THE DISCOURSE content."""
    # OCR-tolerant: handle garbled SUMMARY (e.g., "SUl\'IMA.RYOF")
    m = re.search(r'(?:SUMMARY|SU.{0,6}ARY)\s*(?:OF)?\s*THE\s*DIS\s*COURSE\s*(.*?)(?:SOURCE\s+OF|COM\s*M?\s*ENTARY|$)',
                  chunk, re.DOTALL | re.IGNORECASE)
    if m:
        text = m.group(1).strip()
        if len(text) > 20:
            return clean_ocr(text[:3000])
    return None


def extract_source_from_chunk(chunk):
    """Try to find SOURCE OF THE MOTTO content."""
    m = re.search(r'SOURCE\s+OF\s+THE\s*M\s*O\s*T\s*T\s*O\s*(.*?)(?:COMMENTARY|$)',
                  chunk, re.DOTALL | re.IGNORECASE)
    if m:
        text = m.group(1).strip()
        if len(text) > 10:
            return clean_ocr(text[:1000])
    return None


def find_authorities_in_chunk(chunk):
    """Identify source authorities mentioned."""
    lc = chunk.lower()
    authorities = []
    patterns = [
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
    ]
    for auth_id, pattern in patterns:
        if re.search(pattern, lc):
            authorities.append(auth_id)
    return authorities


def derive_page_ranges(text, pages):
    """
    Derive emblem page ranges from actual EMBLEM+MOTTO positions in the text,
    rather than hardcoding. Falls back to interpolation for missing emblems.
    """
    import re

    # Find all emblem sections (same logic as extract_dejong.py pass 1)
    emblem_pattern = re.compile(r'EMBLEM\s*([IVXLCDM]+)(?=[^IVXLCDM]|$)', re.IGNORECASE)
    # Also find (fig/fie N) MOTTO patterns for garbled headers
    fig_pattern = re.compile(r'\(fi[eg]\s*(\d+)\)\s*M\s*O\s*T\s*T\s*O', re.IGNORECASE)

    # Map emblem number -> text position of its section
    emblem_positions = {}

    for m in emblem_pattern.finditer(text):
        roman = m.group(1).upper()
        num = roman_to_int(roman)
        if not (1 <= num <= 50):
            continue
        lookahead = text[m.end():m.end() + 800]
        motto = re.search(r'M\s*O\s*T\s*T\s*O', lookahead, re.IGNORECASE)
        if motto and m.start() > 20000:
            if num not in emblem_positions or m.start() > emblem_positions[num]:
                # Prefer later match (in the analysis section) for emblems in 30+ range
                # but use earliest analysis-section match for early emblems
                if num not in emblem_positions:
                    emblem_positions[num] = m.start()

    for m in fig_pattern.finditer(text):
        fig_num = int(m.group(1))
        if 1 <= fig_num <= 50 and fig_num not in emblem_positions and m.start() > 20000:
            emblem_positions[fig_num] = m.start()

    # Convert positions to page numbers
    sorted_pages = sorted(pages.items())  # (page_num, char_pos) sorted by page_num
    def pos_to_page(pos):
        """Find which page a character position falls on."""
        best_page = sorted_pages[0][0]
        for pnum, ppos in sorted_pages:
            if ppos <= pos:
                best_page = pnum
            else:
                break
        return best_page

    # Build page ranges: each emblem runs from its start page to just before the next emblem
    emblem_page_starts = {}
    for num, pos in sorted(emblem_positions.items()):
        emblem_page_starts[num] = pos_to_page(pos)

    # For emblems we found, derive ranges from consecutive starts
    all_nums = sorted(emblem_page_starts.keys())
    max_page = max(pages.keys()) if pages else 318

    result = {}
    for i, num in enumerate(all_nums):
        start_page = emblem_page_starts[num]
        if i + 1 < len(all_nums):
            end_page = emblem_page_starts[all_nums[i + 1]] - 1
        else:
            end_page = min(start_page + 10, max_page)
        result[num] = (start_page, end_page)

    # For missing emblems, interpolate between neighbors
    for num in range(1, 51):
        if num not in result:
            # Find nearest known neighbors
            prev_end = 50
            next_start = max_page
            for n in sorted(result.keys()):
                if n < num:
                    prev_end = result[n][1]
                elif n > num:
                    next_start = result[n][0]
                    break
            # Interpolate
            mid = (prev_end + next_start) // 2
            result[num] = (max(prev_end - 1, 51), min(mid + 3, max_page))

    # Add frontispiece
    result[0] = (43, 50)
    return result


def main():
    if not DJ_FILE:
        print("ERROR: De Jong file not found")
        return 1

    text = DJ_FILE.read_text(encoding='utf-8', errors='replace')
    pages = find_page_positions(text)

    # Derive page ranges dynamically from actual emblem positions
    EMBLEM_PAGES = derive_page_ranges(text, pages)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    # Find missing emblems
    missing = conn.execute(
        "SELECT number, roman_numeral FROM emblems WHERE number > 0 AND motto_english IS NULL ORDER BY number"
    ).fetchall()

    print(f"Pass 2: {len(missing)} emblems missing mottos")

    dj_bib = conn.execute("SELECT id FROM bibliography WHERE source_id = 'de_jong_1969'").fetchone()
    dj_bib_id = dj_bib[0] if dj_bib else None

    updated = 0
    refs_added = 0
    sources_added = 0

    for num, roman in missing:
        page_range = EMBLEM_PAGES.get(num)
        if not page_range:
            print(f"  Emblem {roman}: no page range defined, skipping")
            continue

        start_page, end_page = page_range
        # Find text between these pages
        start_pos = pages.get(start_page)
        end_pos = pages.get(end_page + 1, pages.get(end_page, len(text)))

        if not start_pos:
            # Try nearby pages
            for p in range(start_page - 2, start_page + 3):
                if p in pages:
                    start_pos = pages[p]
                    break

        if not start_pos:
            print(f"  Emblem {roman}: page {start_page} not found, skipping")
            continue

        chunk = text[start_pos:end_pos]

        motto = extract_motto_from_chunk(chunk)
        epigram = extract_epigram_from_chunk(chunk)
        summary = extract_summary_from_chunk(chunk)
        source = extract_source_from_chunk(chunk)
        authorities = find_authorities_in_chunk(chunk)

        fields = sum(1 for x in [motto, epigram, summary, source] if x)
        print(f"  Emblem {roman:>5}: {fields}/4 fields, {len(authorities)} authorities (pages {start_page}-{end_page})")

        if motto or summary:
            # Update emblem
            updates = {}
            if motto:
                updates['motto_english'] = motto[:500]
            if epigram:
                updates['epigram_english'] = epigram[:2000]
            if summary:
                updates['discourse_summary'] = summary[:3000]

            if updates:
                set_clause = ', '.join(f"{k} = ?" for k in updates)
                values = list(updates.values()) + [num]
                conn.execute(
                    f"UPDATE emblems SET {set_clause}, source_method = 'CORPUS_EXTRACTION', "
                    f"confidence = 'MEDIUM' WHERE number = ? AND motto_english IS NULL",
                    values
                )
                updated += 1

            # Add scholarly ref
            if dj_bib_id and (source or summary):
                emblem_id = conn.execute("SELECT id FROM emblems WHERE number = ?", (num,)).fetchone()[0]
                ref_text = f"Source: {source[:500]}" if source else summary[:500]
                auth_json = json.dumps(authorities)
                existing = conn.execute(
                    "SELECT id FROM scholarly_refs WHERE emblem_id = ? AND bib_id = ?",
                    (emblem_id, dj_bib_id)
                ).fetchone()
                if not existing:
                    conn.execute("""
                        INSERT INTO scholarly_refs (emblem_id, bib_id, interpretation_type,
                            summary, source_texts_referenced, confidence)
                        VALUES (?, ?, 'ALCHEMICAL', ?, ?, 'MEDIUM')
                    """, (emblem_id, dj_bib_id, ref_text, auth_json))
                    refs_added += 1

                # Add source links
                for auth_id in authorities:
                    auth_row = conn.execute(
                        "SELECT id FROM source_authorities WHERE authority_id = ?", (auth_id,)
                    ).fetchone()
                    if auth_row:
                        existing = conn.execute(
                            "SELECT id FROM emblem_sources WHERE emblem_id = ? AND authority_id = ?",
                            (emblem_id, auth_row[0])
                        ).fetchone()
                        if not existing:
                            conn.execute("""
                                INSERT INTO emblem_sources (emblem_id, authority_id,
                                    relationship_type, confidence)
                                VALUES (?, ?, 'DISCOURSE_CITATION', 'MEDIUM')
                            """, (emblem_id, auth_row[0]))
                            sources_added += 1

    conn.commit()

    # Report
    total_mottos = conn.execute("SELECT COUNT(*) FROM emblems WHERE motto_english IS NOT NULL").fetchone()[0]
    total_disc = conn.execute("SELECT COUNT(*) FROM emblems WHERE discourse_summary IS NOT NULL").fetchone()[0]
    total_refs = conn.execute("SELECT COUNT(*) FROM scholarly_refs").fetchone()[0]
    total_sources = conn.execute("SELECT COUNT(*) FROM emblem_sources").fetchone()[0]
    conn.close()

    print(f"\nPass 2 results:")
    print(f"  Updated: {updated}")
    print(f"  Refs added: {refs_added}")
    print(f"  Source links added: {sources_added}")
    print(f"\nDatabase totals:")
    print(f"  Mottos: {total_mottos}/50")
    print(f"  Discourses: {total_disc}/50")
    print(f"  Scholarly refs: {total_refs}")
    print(f"  Source links: {total_sources}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
