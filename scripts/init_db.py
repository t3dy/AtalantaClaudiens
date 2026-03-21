"""
init_db.py — Create the minimal schema for the De Jong extraction loop.

Stage 1A: 5 tables only. Additional tables added by future migration scripts
when their phases begin (see docs/ROADMAP.md "Deferred Schema").

Idempotent: safe to re-run.
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "db"
DB_PATH = DB_DIR / "atalanta.db"

SCHEMA = """
-- ============================================================
-- PHASE 1 MINIMAL SCHEMA — De Jong Extraction Loop
-- 5 tables: emblems, bibliography, source_authorities,
--           scholarly_refs, emblem_sources
-- ============================================================

-- The primary organizing unit. 51 rows: frontispiece (0) + emblems I-L (1-50).
CREATE TABLE IF NOT EXISTS emblems (
    id              INTEGER PRIMARY KEY,
    number          INTEGER UNIQUE NOT NULL,
    roman_numeral   TEXT,
    canonical_label TEXT NOT NULL,
    motto_latin     TEXT,
    motto_english   TEXT,
    motto_german    TEXT,
    epigram_latin   TEXT,
    epigram_english TEXT,
    discourse_summary TEXT,
    image_description TEXT,
    image_path      TEXT,
    alchemical_stage TEXT CHECK(alchemical_stage IN ('NIGREDO','ALBEDO','CITRINITAS','RUBEDO') OR alchemical_stage IS NULL),
    source_method   TEXT DEFAULT 'SEED_DATA',
    review_status   TEXT DEFAULT 'DRAFT' CHECK(review_status IN ('DRAFT','REVIEWED','VERIFIED')),
    confidence      TEXT DEFAULT 'MEDIUM' CHECK(confidence IN ('HIGH','MEDIUM','LOW'))
);

-- Source works in our corpus. FK target for scholarly_refs.
CREATE TABLE IF NOT EXISTS bibliography (
    id              INTEGER PRIMARY KEY,
    source_id       TEXT UNIQUE,
    author          TEXT NOT NULL,
    title           TEXT NOT NULL,
    year            INTEGER,
    journal         TEXT,
    publisher       TEXT,
    pub_type        TEXT,
    af_relevance    TEXT CHECK(af_relevance IN ('PRIMARY','DIRECT','CONTEXTUAL')),
    in_collection   INTEGER DEFAULT 1
);

-- Maier's textual sources as identified by De Jong.
-- First-class entities, not just citation strings.
CREATE TABLE IF NOT EXISTS source_authorities (
    id                  INTEGER PRIMARY KEY,
    authority_id        TEXT UNIQUE NOT NULL,
    name                TEXT NOT NULL,
    type                TEXT CHECK(type IN ('CLASSICAL','ALCHEMICAL','BIBLICAL','MEDICAL','PATRISTIC','HERMETIC','MOVEMENT')),
    author              TEXT,
    era                 TEXT,
    relationship_to_maier TEXT
);

-- The core concordance table: links a scholar's interpretation to a specific emblem.
CREATE TABLE IF NOT EXISTS scholarly_refs (
    id                      INTEGER PRIMARY KEY,
    emblem_id               INTEGER REFERENCES emblems(id),
    bib_id                  INTEGER NOT NULL REFERENCES bibliography(id),
    interpretation_type     TEXT CHECK(interpretation_type IN ('ICONOGRAPHIC','ALCHEMICAL','MYTHOLOGICAL','HISTORICAL','MUSICAL')),
    summary                 TEXT NOT NULL,
    source_texts_referenced TEXT,
    section_page            TEXT,
    confidence              TEXT DEFAULT 'HIGH' CHECK(confidence IN ('HIGH','MEDIUM','LOW'))
);

-- Links emblems to their textual sources (De Jong's source identifications).
CREATE TABLE IF NOT EXISTS emblem_sources (
    id                  INTEGER PRIMARY KEY,
    emblem_id           INTEGER NOT NULL REFERENCES emblems(id),
    authority_id        INTEGER NOT NULL REFERENCES source_authorities(id),
    relationship_type   TEXT CHECK(relationship_type IN ('MOTTO_SOURCE','DISCOURSE_CITATION','THEMATIC_PARALLEL','NARRATIVE_SOURCE')),
    de_jong_page        TEXT,
    notes               TEXT,
    confidence          TEXT DEFAULT 'HIGH' CHECK(confidence IN ('HIGH','MEDIUM','LOW'))
);

-- Schema version tracking
CREATE TABLE IF NOT EXISTS schema_version (
    version     INTEGER PRIMARY KEY,
    applied_at  TEXT DEFAULT (datetime('now')),
    description TEXT
);

INSERT OR IGNORE INTO schema_version (version, description)
VALUES (1, 'Phase 1 minimal schema: emblems, bibliography, source_authorities, scholarly_refs, emblem_sources');
"""


def main():
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    conn.close()

    # Verify
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()

    print(f"Database: {DB_PATH}")
    print(f"Tables ({len(tables)}): {', '.join(tables)}")

    expected = {'bibliography', 'emblem_sources', 'emblems', 'scholarly_refs', 'schema_version', 'source_authorities'}
    missing = expected - set(tables)
    if missing:
        print(f"ERROR: Missing tables: {missing}")
        return 1

    print("Schema v1 ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
