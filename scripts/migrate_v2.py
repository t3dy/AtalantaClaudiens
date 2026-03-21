"""
migrate_v2.py — Add Phase 2-3 tables: scholars, dictionary, timeline, editions.

Idempotent: safe to re-run.
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "atalanta.db"

SCHEMA_V2 = """
CREATE TABLE IF NOT EXISTS scholars (
    id              INTEGER PRIMARY KEY,
    name            TEXT UNIQUE NOT NULL,
    birth_year      INTEGER,
    death_year      INTEGER,
    specialization  TEXT,
    af_focus        TEXT,
    overview        TEXT,
    review_status   TEXT DEFAULT 'DRAFT' CHECK(review_status IN ('DRAFT','REVIEWED','VERIFIED'))
);

CREATE TABLE IF NOT EXISTS scholar_works (
    scholar_id  INTEGER REFERENCES scholars(id),
    bib_id      INTEGER REFERENCES bibliography(id),
    PRIMARY KEY (scholar_id, bib_id)
);

CREATE TABLE IF NOT EXISTS dictionary_terms (
    id                  INTEGER PRIMARY KEY,
    slug                TEXT UNIQUE NOT NULL,
    label               TEXT NOT NULL,
    category            TEXT CHECK(category IN ('PROCESS','SUBSTANCE','FIGURE','CONCEPT','MUSICAL','SOURCE_TEXT')),
    definition_short    TEXT,
    definition_long     TEXT,
    significance_to_af  TEXT,
    source_basis        TEXT,
    review_status       TEXT DEFAULT 'DRAFT' CHECK(review_status IN ('DRAFT','REVIEWED','VERIFIED'))
);

CREATE TABLE IF NOT EXISTS dictionary_term_links (
    term_id         INTEGER REFERENCES dictionary_terms(id),
    linked_term_id  INTEGER REFERENCES dictionary_terms(id),
    link_type       TEXT CHECK(link_type IN ('RELATED','SEE_ALSO','OPPOSITE','PARENT','CHILD')),
    PRIMARY KEY (term_id, linked_term_id)
);

CREATE TABLE IF NOT EXISTS term_emblem_refs (
    term_id     INTEGER REFERENCES dictionary_terms(id),
    emblem_id   INTEGER REFERENCES emblems(id),
    context     TEXT,
    PRIMARY KEY (term_id, emblem_id)
);

CREATE TABLE IF NOT EXISTS timeline_events (
    id          INTEGER PRIMARY KEY,
    year        INTEGER NOT NULL,
    year_end    INTEGER,
    event_type  TEXT CHECK(event_type IN ('PUBLICATION','EDITION','SCHOLARSHIP','BIOGRAPHY','DIGITAL','FACSIMILE')),
    title       TEXT NOT NULL,
    description TEXT,
    scholar_id  INTEGER REFERENCES scholars(id),
    bib_id      INTEGER REFERENCES bibliography(id),
    confidence  TEXT DEFAULT 'HIGH' CHECK(confidence IN ('HIGH','MEDIUM','LOW'))
);

INSERT OR IGNORE INTO schema_version (version, description)
VALUES (2, 'Phase 2-3 tables: scholars, scholar_works, dictionary_terms, dictionary_term_links, term_emblem_refs, timeline_events');
"""

def main():
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA_V2)
    conn.close()

    conn = sqlite3.connect(DB_PATH)
    tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()]
    versions = conn.execute("SELECT version, description FROM schema_version ORDER BY version").fetchall()
    conn.close()

    print(f"Tables ({len(tables)}): {', '.join(tables)}")
    for v, d in versions:
        print(f"  v{v}: {d}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
