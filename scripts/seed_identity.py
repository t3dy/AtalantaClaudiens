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
SEED_FILE = BASE_DIR / "data" / "emblem_manifest.json"  # Canonical source of truth


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
        # Handle both manifest format (number/roman/image_file) and legacy (emblem_number/roman_label/image_filename)
        num = entry.get("number", entry.get("emblem_number"))
        roman = entry.get("roman", entry.get("roman_label", ""))
        img_file = entry.get("image_file", entry.get("image_filename"))
        img_src = entry.get("image_source")
        img_url = entry.get("image_url")
        confirmed = entry.get("image_confirmed", False)
        conf = 'HIGH' if confirmed else entry.get("alignment_confidence")
        notes = entry.get("notes")

        result = conn.execute("""
            INSERT OR IGNORE INTO emblem_identity
                (emblem_number, roman_label, canonical_order,
                 image_filename, image_source, image_url,
                 alignment_confidence, source_method, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'MANUAL', ?)
        """, (num, roman, num, img_file, img_src, img_url, conf, notes))

        if result.rowcount > 0:
            inserted += 1
        else:
            conn.execute("""
                UPDATE emblem_identity
                SET image_filename = ?, image_source = ?,
                    image_url = ?, alignment_confidence = ?
                WHERE emblem_number = ?
            """, (img_file, img_src, img_url, conf, num))
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
