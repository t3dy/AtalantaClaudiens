"""
migrate_v5_arguments.py — Add scholarly_arguments table for book-level
scholarly theses that span multiple emblems.

scholarly_refs stores per-emblem commentary.
scholarly_arguments stores overarching theses (e.g., "Tilton argues AF
should not be read through a Paracelsian Tria Prima framework").

Idempotent: safe to re-run.
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "atalanta.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS scholarly_arguments (
    id              INTEGER PRIMARY KEY,
    bib_id          INTEGER REFERENCES bibliography(id),
    argument_type   TEXT CHECK(argument_type IN (
        'THESIS', 'COUNTER_ARGUMENT', 'METHODOLOGY', 'HISTORICAL_CLAIM',
        'BIOGRAPHICAL', 'ATTRIBUTION', 'INTERPRETATION'
    )),
    claim           TEXT NOT NULL,
    evidence        TEXT,
    chapter_section TEXT,
    page_range      TEXT,
    responds_to_id  INTEGER REFERENCES scholarly_arguments(id),
    emblem_range    TEXT,
    confidence      TEXT DEFAULT 'MEDIUM' CHECK(confidence IN ('HIGH','MEDIUM','LOW')),
    source_method   TEXT DEFAULT 'LLM_ASSISTED',
    review_status   TEXT DEFAULT 'DRAFT' CHECK(review_status IN ('DRAFT','REVIEWED','VERIFIED'))
);

INSERT OR IGNORE INTO schema_version (version, description)
VALUES (5, 'scholarly_arguments table for book-level theses spanning multiple emblems');
"""


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    count = conn.execute("SELECT COUNT(*) FROM scholarly_arguments").fetchone()[0]
    conn.close()
    print(f"  v5: scholarly_arguments table ({count} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
