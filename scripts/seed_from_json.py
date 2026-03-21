"""
seed_from_json.py — Ingest atalanta_fugiens_seed.json into the Phase 1 schema.

Populates:
  - emblems (51 rows: frontispiece + I-L)
  - bibliography (10 rows)
  - source_authorities (15 rows)
  - scholarly_refs (from seed emblem data)
  - emblem_sources (from seed source_map)

Idempotent: uses INSERT OR IGNORE throughout.
"""

import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "atalanta.db"
SEED_PATH = BASE_DIR / "atalanta_fugiens_seed.json"

# Roman numeral conversion
ROMAN_MAP = [
    (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
    (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
    (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
]

def int_to_roman(n):
    if n <= 0:
        return None
    result = []
    for value, numeral in ROMAN_MAP:
        while n >= value:
            result.append(numeral)
            n -= value
    return ''.join(result)

def roman_to_int(s):
    if not s:
        return 0
    vals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    for i, c in enumerate(s):
        v = vals.get(c, 0)
        if i + 1 < len(s) and v < vals.get(s[i + 1], 0):
            total -= v
        else:
            total += v
    return total


def seed_emblems(conn, seed):
    """Insert 51 emblem rows: frontispiece (0) + emblems 1-50."""
    # Build lookup from seed data
    seed_emblems = {}
    for e in seed.get("emblems", []):
        num = e["emblem_number"]
        if num == "Frontispiece":
            seed_emblems[0] = e
        else:
            seed_emblems[roman_to_int(num)] = e

    for n in range(0, 51):
        roman = int_to_roman(n) if n > 0 else None
        se = seed_emblems.get(n, {})
        label = se.get("canonical_label", f"Emblem {roman or 'Frontispiece'}")

        conn.execute("""
            INSERT OR IGNORE INTO emblems
                (number, roman_numeral, canonical_label, motto_latin, motto_english,
                 image_description, source_method, confidence)
            VALUES (?, ?, ?, ?, ?, ?, 'SEED_DATA', ?)
        """, (
            n, roman, label,
            se.get("motto_latin"),
            se.get("motto_english"),
            se.get("image_description"),
            'MEDIUM' if se else 'LOW'
        ))

    count = conn.execute("SELECT COUNT(*) FROM emblems").fetchone()[0]
    print(f"  emblems: {count} rows")


def seed_bibliography(conn, seed):
    """Insert bibliography entries from corpus array."""
    for src in seed.get("corpus", []):
        conn.execute("""
            INSERT OR IGNORE INTO bibliography
                (source_id, author, title, year, journal, publisher, pub_type, af_relevance, in_collection)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            src.get("source_id"),
            src["author"],
            src["title"],
            src.get("year"),
            src.get("journal"),
            src.get("publisher"),
            src.get("type"),
            src.get("af_relevance", "CONTEXTUAL"),
        ))

        # Update annotation if provided
        annotation = src.get("annotation")
        if annotation:
            conn.execute(
                "UPDATE bibliography SET annotation = ? WHERE source_id = ?",
                (annotation, src.get("source_id"))
            )

    count = conn.execute("SELECT COUNT(*) FROM bibliography").fetchone()[0]
    print(f"  bibliography: {count} rows")


def seed_authorities(conn, seed):
    """Insert source authority entries."""
    for auth in seed.get("source_authorities", []):
        conn.execute("""
            INSERT OR IGNORE INTO source_authorities
                (authority_id, name, type, author, relationship_to_maier)
            VALUES (?, ?, ?, ?, ?)
        """, (
            auth["authority_id"],
            auth["name"],
            auth.get("type"),
            auth.get("author"),
            auth.get("relationship"),
        ))

        # Update description_long if provided
        desc_long = auth.get("description_long")
        if desc_long:
            conn.execute(
                "UPDATE source_authorities SET description_long = ? WHERE authority_id = ?",
                (desc_long, auth["authority_id"])
            )

    count = conn.execute("SELECT COUNT(*) FROM source_authorities").fetchone()[0]
    print(f"  source_authorities: {count} rows")


def seed_scholarly_refs(conn, seed):
    """Insert scholarly references from seed emblem data."""
    inserted = 0
    for e in seed.get("emblems", []):
        num = e["emblem_number"]
        if num == "Frontispiece":
            emblem_num = 0
        else:
            emblem_num = roman_to_int(num)

        emblem_row = conn.execute(
            "SELECT id FROM emblems WHERE number = ?", (emblem_num,)
        ).fetchone()
        if not emblem_row:
            continue
        emblem_id = emblem_row[0]

        for ref in e.get("scholarly_refs", []):
            # Resolve bib_id from scholar name
            scholar = ref.get("scholar", "")
            bib_row = conn.execute(
                "SELECT id FROM bibliography WHERE source_id = ?", (scholar,)
            ).fetchone()
            if not bib_row:
                # Try partial match
                bib_row = conn.execute(
                    "SELECT id FROM bibliography WHERE source_id LIKE ?",
                    (f"%{scholar.split('_')[0]}%",)
                ).fetchone()
            if not bib_row:
                continue
            bib_id = bib_row[0]

            source_texts = json.dumps(ref.get("source_texts", []))
            conn.execute("""
                INSERT OR IGNORE INTO scholarly_refs
                    (emblem_id, bib_id, summary, source_texts_referenced,
                     section_page, confidence)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                emblem_id, bib_id,
                ref["summary"],
                source_texts,
                ref.get("citation"),
                ref.get("confidence", "HIGH"),
            ))
            inserted += 1

    count = conn.execute("SELECT COUNT(*) FROM scholarly_refs").fetchone()[0]
    print(f"  scholarly_refs: {count} rows ({inserted} attempted)")


def seed_source_map(conn, seed):
    """Insert emblem-source links from source_map array."""
    inserted = 0
    for mapping in seed.get("source_map", []):
        emblem_label = mapping["emblem"]
        if emblem_label == "Frontispiece":
            emblem_num = 0
        else:
            emblem_num = roman_to_int(emblem_label)

        emblem_row = conn.execute(
            "SELECT id FROM emblems WHERE number = ?", (emblem_num,)
        ).fetchone()
        if not emblem_row:
            continue

        # Find authority by name match
        auth_row = conn.execute(
            "SELECT id FROM source_authorities WHERE name LIKE ?",
            (f"%{mapping['source_text'].split(',')[0][:30]}%",)
        ).fetchone()
        if not auth_row:
            # Try authority_id pattern
            auth_row = conn.execute(
                "SELECT id FROM source_authorities WHERE authority_id LIKE ?",
                (f"%{mapping.get('author', '').split()[0].upper()[:6]}%",)
            ).fetchone()
        if not auth_row:
            continue

        rel_type_map = {
            "MOTTO_SOURCE": "MOTTO_SOURCE",
            "NARRATIVE_SOURCE": "NARRATIVE_SOURCE",
            "CITATION": "DISCOURSE_CITATION",
            "THEMATIC_PARALLEL": "THEMATIC_PARALLEL",
            "influence": "THEMATIC_PARALLEL",
        }
        rel_type = rel_type_map.get(mapping.get("relationship"), "DISCOURSE_CITATION")

        conn.execute("""
            INSERT OR IGNORE INTO emblem_sources
                (emblem_id, authority_id, relationship_type, confidence)
            VALUES (?, ?, ?, 'HIGH')
        """, (emblem_row[0], auth_row[0], rel_type))
        inserted += 1

    count = conn.execute("SELECT COUNT(*) FROM emblem_sources").fetchone()[0]
    print(f"  emblem_sources: {count} rows ({inserted} attempted)")


def main():
    if not SEED_PATH.exists():
        print(f"ERROR: Seed file not found: {SEED_PATH}")
        return 1

    seed = json.loads(SEED_PATH.read_text(encoding="utf-8"))
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    print("Seeding from atalanta_fugiens_seed.json...")
    seed_emblems(conn, seed)
    seed_bibliography(conn, seed)
    seed_authorities(conn, seed)
    seed_scholarly_refs(conn, seed)
    seed_source_map(conn, seed)

    conn.commit()
    conn.close()
    print("Seed complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
