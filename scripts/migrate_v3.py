"""
migrate_v3.py — Add content enrichment columns for emblem analysis,
dictionary Latin terms, source descriptions, and timeline descriptions.

Idempotent: safe to re-run (checks column existence before ALTER).
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "atalanta.db"


def add_column_if_missing(conn, table, column, col_type="TEXT"):
    cols = [row[1] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()]
    if column not in cols:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}")
        return True
    return False


def main():
    conn = sqlite3.connect(DB_PATH)

    added = []
    if add_column_if_missing(conn, "emblems", "analysis_html"):
        added.append("emblems.analysis_html")
    if add_column_if_missing(conn, "dictionary_terms", "label_latin"):
        added.append("dictionary_terms.label_latin")
    if add_column_if_missing(conn, "source_authorities", "description_long"):
        added.append("source_authorities.description_long")
    if add_column_if_missing(conn, "timeline_events", "description_long"):
        added.append("timeline_events.description_long")
    if add_column_if_missing(conn, "bibliography", "annotation"):
        added.append("bibliography.annotation")

    conn.execute("""
        INSERT OR IGNORE INTO schema_version (version, description)
        VALUES (3, 'Content enrichment: emblems.analysis_html, dictionary_terms.label_latin, source_authorities.description_long, timeline_events.description_long')
    """)
    conn.commit()
    conn.close()

    if added:
        print(f"  v3: Added columns: {', '.join(added)}")
    else:
        print("  v3: All columns already exist")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
