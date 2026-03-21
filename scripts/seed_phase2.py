"""
seed_phase2.py — Populate scholars, dictionary, timeline from seed JSON.

Requires migrate_v2.py to have run first.
Idempotent: uses INSERT OR IGNORE.
"""

import json
import re
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "atalanta.db"
SEED_PATH = BASE_DIR / "atalanta_fugiens_seed.json"

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

def slugify(text):
    s = text.lower().strip()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')


def seed_scholars(conn, seed):
    for s in seed.get("scholars", []):
        conn.execute("""
            INSERT OR IGNORE INTO scholars (name, specialization, af_focus)
            VALUES (?, ?, ?)
        """, (s["name"], s.get("specialization"), s.get("af_focus")))

        # Update overview if provided
        overview = s.get("overview")
        if overview:
            conn.execute(
                "UPDATE scholars SET overview = ? WHERE name = ? AND (overview IS NULL OR overview = '')",
                (overview, s["name"])
            )

        # Link to bibliography
        scholar_row = conn.execute("SELECT id FROM scholars WHERE name = ?", (s["name"],)).fetchone()
        if scholar_row:
            for work_id in s.get("key_works", []):
                bib_row = conn.execute("SELECT id FROM bibliography WHERE source_id = ?", (work_id,)).fetchone()
                if bib_row:
                    conn.execute("INSERT OR IGNORE INTO scholar_works (scholar_id, bib_id) VALUES (?, ?)",
                                 (scholar_row[0], bib_row[0]))

    count = conn.execute("SELECT COUNT(*) FROM scholars").fetchone()[0]
    links = conn.execute("SELECT COUNT(*) FROM scholar_works").fetchone()[0]
    print(f"  scholars: {count} rows, {links} work links")


def seed_dictionary(conn, seed):
    for entry in seed.get("dictionary_entries", []):
        slug = slugify(entry["term"])
        conn.execute("""
            INSERT OR IGNORE INTO dictionary_terms
                (slug, label, category, definition_short, source_basis)
            VALUES (?, ?, ?, ?, ?)
        """, (
            slug,
            entry["term"],
            entry.get("category"),
            entry.get("definition"),
            ', '.join(entry.get("sources", [])),
        ))

        # Update optional enrichment fields (latin, significance)
        latin = entry.get("latin")
        sig = entry.get("significance_to_af")
        if latin or sig:
            updates = []
            values = []
            if latin:
                updates.append("label_latin = ?")
                values.append(latin)
            if sig:
                updates.append("significance_to_af = ?")
                values.append(sig)
            values.append(slug)
            conn.execute(
                f"UPDATE dictionary_terms SET {', '.join(updates)} WHERE slug = ?",
                values
            )

        # Link to emblems
        term_row = conn.execute("SELECT id FROM dictionary_terms WHERE slug = ?", (slug,)).fetchone()
        if term_row:
            for emblem_ref in entry.get("related_emblems", []):
                if emblem_ref == "ALL":
                    continue
                num = roman_to_int(emblem_ref)
                if num > 0:
                    emblem_row = conn.execute("SELECT id FROM emblems WHERE number = ?", (num,)).fetchone()
                    if emblem_row:
                        conn.execute("INSERT OR IGNORE INTO term_emblem_refs (term_id, emblem_id) VALUES (?, ?)",
                                     (term_row[0], emblem_row[0]))

    terms = conn.execute("SELECT COUNT(*) FROM dictionary_terms").fetchone()[0]
    refs = conn.execute("SELECT COUNT(*) FROM term_emblem_refs").fetchone()[0]
    print(f"  dictionary_terms: {terms} rows, {refs} emblem refs")


def seed_timeline(conn, seed):
    for event in seed.get("timeline_events", []):
        # Try to find scholar_id
        scholar_id = None
        bib_id = None

        conn.execute("""
            INSERT OR IGNORE INTO timeline_events
                (year, event_type, title, description, scholar_id, bib_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            event["year"],
            event.get("event_type"),
            event["title"],
            event.get("description"),
            scholar_id,
            bib_id,
        ))

        # Update description_long if provided
        desc_long = event.get("description_long")
        if desc_long:
            conn.execute(
                "UPDATE timeline_events SET description_long = ? WHERE year = ? AND title = ?",
                (desc_long, event["year"], event["title"])
            )

    count = conn.execute("SELECT COUNT(*) FROM timeline_events").fetchone()[0]
    print(f"  timeline_events: {count} rows")


def main():
    seed = json.loads(SEED_PATH.read_text(encoding="utf-8"))
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    print("Seeding Phase 2-3 data...")
    seed_scholars(conn, seed)
    seed_dictionary(conn, seed)
    seed_timeline(conn, seed)

    conn.commit()
    conn.close()
    print("Seed complete.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
