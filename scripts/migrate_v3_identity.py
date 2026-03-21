"""
migrate_v3_identity.py — Create emblem_identity table for deterministic
image mapping and emblem identity grounding.

Each emblem gets an explicit identity record with labeled image source,
filename, and alignment confidence. All image rendering flows through
this table — no hardcoded number-to-filename assumptions.

Idempotent: safe to re-run.
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "atalanta.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS emblem_identity (
    id                      INTEGER PRIMARY KEY,
    emblem_number            INTEGER NOT NULL UNIQUE CHECK(emblem_number >= 0 AND emblem_number <= 50),
    roman_label              TEXT NOT NULL,
    canonical_order          INTEGER NOT NULL,
    image_filename           TEXT,
    image_source             TEXT,
    image_url                TEXT,
    alignment_confidence     TEXT CHECK(alignment_confidence IN ('HIGH','MEDIUM','LOW')),
    source_method            TEXT DEFAULT 'MANUAL',
    notes                    TEXT
);

INSERT OR IGNORE INTO schema_version (version, description)
VALUES (4, 'Emblem identity layer: emblem_identity table for deterministic image grounding');
"""


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    conn.close()

    conn = sqlite3.connect(DB_PATH)
    tables = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()]
    has_identity = 'emblem_identity' in tables
    row_count = conn.execute("SELECT COUNT(*) FROM emblem_identity").fetchone()[0] if has_identity else 0
    conn.close()

    print(f"  v4: emblem_identity table {'exists' if has_identity else 'CREATED'} ({row_count} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
