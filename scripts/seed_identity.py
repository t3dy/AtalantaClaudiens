"""
seed_identity.py — Populate emblem_identity table from seed JSON.

Loads data/emblem_identity_seed.json and inserts into emblem_identity.
Uses INSERT OR IGNORE — does not overwrite existing rows.

Idempotent: safe to re-run.
"""

import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "atalanta.db"
SEED_FILE = BASE_DIR / "data" / "emblem_identity_seed.json"


def main():
    if not SEED_FILE.exists():
        print(f"ERROR: {SEED_FILE} not found")
        return 1

    seed = json.loads(SEED_FILE.read_text(encoding="utf-8"))

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    inserted = 0
    updated = 0
    for entry in seed:
        result = conn.execute("""
            INSERT OR IGNORE INTO emblem_identity
                (emblem_number, roman_label, canonical_order,
                 image_filename, image_source, image_url,
                 alignment_confidence, source_method, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'MANUAL', ?)
        """, (
            entry["emblem_number"],
            entry["roman_label"],
            entry["canonical_order"],
            entry.get("image_filename"),
            entry.get("image_source"),
            entry.get("image_url"),
            entry.get("alignment_confidence"),
            entry.get("notes"),
        ))
        if result.rowcount > 0:
            inserted += 1
        else:
            # Row exists — sync image fields from manifest
            conn.execute("""
                UPDATE emblem_identity
                SET image_filename = ?, image_source = ?,
                    image_url = ?, alignment_confidence = ?
                WHERE emblem_number = ?
            """, (
                entry.get("image_filename"),
                entry.get("image_source"),
                entry.get("image_url"),
                'HIGH' if entry.get("image_confirmed") else entry.get("alignment_confidence"),
                entry["emblem_number"],
            ))
            updated += 1

    conn.commit()

    total = conn.execute("SELECT COUNT(*) FROM emblem_identity").fetchone()[0]
    with_image = conn.execute(
        "SELECT COUNT(*) FROM emblem_identity WHERE image_filename IS NOT NULL"
    ).fetchone()[0]
    high = conn.execute(
        "SELECT COUNT(*) FROM emblem_identity WHERE alignment_confidence = 'HIGH'"
    ).fetchone()[0]
    conn.close()

    print(f"  emblem_identity: {total} rows ({inserted} inserted, {updated} synced), "
          f"{with_image} with images, {high} HIGH confidence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
