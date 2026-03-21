"""
link_dictionary.py — Create cross-references between related dictionary terms.

Links terms that share emblems or belong to related semantic groups.
Idempotent: uses INSERT OR IGNORE.
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "atalanta.db"

# Manual semantic groupings for cross-linking
RELATED_GROUPS = [
    # Stages of the Great Work
    ['nigredo', 'albedo', 'citrinitas', 'rubedo'],
    # Core substances
    ['mercurius', 'sulphur', 'philosopher-s-stone', 'philosophical-egg', 'white-lead'],
    # Processes
    ['coniunctio', 'putrefaction', 'calcination', 'coagulation', 'dissolution'],
    # Figures
    ['hermaphrodite', 'king-duenech', 'ouroboros'],
    # Source texts
    ['tabula-smaragdina', 'turba-philosophorum', 'rosarium-philosophorum'],
    # Concepts
    ['sapientia', 'catena-aurea', 'tria-prima'],
]


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    # Get all term slugs -> ids
    terms = {}
    for row in conn.execute("SELECT id, slug FROM dictionary_terms"):
        terms[row[1]] = row[0]

    linked = 0
    for group in RELATED_GROUPS:
        # Get IDs for terms in this group that exist
        group_ids = [(slug, terms[slug]) for slug in group if slug in terms]
        # Cross-link all pairs
        for i, (slug_a, id_a) in enumerate(group_ids):
            for slug_b, id_b in group_ids[i+1:]:
                conn.execute(
                    "INSERT OR IGNORE INTO dictionary_term_links (term_id, linked_term_id, link_type) VALUES (?, ?, 'RELATED')",
                    (id_a, id_b)
                )
                conn.execute(
                    "INSERT OR IGNORE INTO dictionary_term_links (term_id, linked_term_id, link_type) VALUES (?, ?, 'RELATED')",
                    (id_b, id_a)
                )
                linked += 1

    conn.commit()
    total = conn.execute("SELECT COUNT(*) FROM dictionary_term_links").fetchone()[0]
    conn.close()
    print(f"  dictionary_term_links: {total} total ({linked} pairs added)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
