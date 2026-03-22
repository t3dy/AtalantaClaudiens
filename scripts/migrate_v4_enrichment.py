"""Stage 1: Add enrichment columns missing from DB but documented in ONTOLOGY.md.

Adds to `emblems`: visual_elements, fugue_mode, fugue_interval, epigram_german
Adds to `dictionary_terms`: registers

Updates schema_version to v5.
"""
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'atalanta.db')

EMBLEM_COLUMNS = [
    ('visual_elements', 'TEXT'),
    ('fugue_mode', 'TEXT'),
    ('fugue_interval', 'TEXT'),
    ('epigram_german', 'TEXT'),
]

DICT_COLUMNS = [
    ('registers', 'TEXT'),
]


def column_exists(cursor, table, column):
    cols = [r[1] for r in cursor.execute(f'PRAGMA table_info({table})').fetchall()]
    return column in cols


def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    added = []

    for col, typ in EMBLEM_COLUMNS:
        if not column_exists(c, 'emblems', col):
            c.execute(f'ALTER TABLE emblems ADD COLUMN {col} {typ}')
            added.append(f'emblems.{col}')
            print(f'  Added emblems.{col} ({typ})')
        else:
            print(f'  Skipped emblems.{col} (already exists)')

    for col, typ in DICT_COLUMNS:
        if not column_exists(c, 'dictionary_terms', col):
            c.execute(f'ALTER TABLE dictionary_terms ADD COLUMN {col} {typ}')
            added.append(f'dictionary_terms.{col}')
            print(f'  Added dictionary_terms.{col} ({typ})')
        else:
            print(f'  Skipped dictionary_terms.{col} (already exists)')

    # Update schema version
    existing = c.execute('SELECT version FROM schema_version WHERE version = 5').fetchone()
    if not existing:
        c.execute(
            'INSERT INTO schema_version (version, applied_at, description) VALUES (?, ?, ?)',
            (5, datetime.now().isoformat(), 'Enrichment columns: visual_elements, fugue_mode, fugue_interval, epigram_german, registers')
        )
        print('  Schema version -> 5')

    conn.commit()
    conn.close()
    print(f'\nMigration complete. Added {len(added)} columns: {", ".join(added) if added else "none (all existed)"}')


if __name__ == '__main__':
    main()
