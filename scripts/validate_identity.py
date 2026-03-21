"""
validate_identity.py — Validate emblem_identity table integrity and image grounding.

Checks:
1. 51 rows exist (0-50)
2. No duplicate emblem_number
3. All roman_label values valid
4. All HIGH confidence entries have corresponding image files
5. Summary report

Idempotent: read-only, no mutations.
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "atalanta.db"
IMAGES_DIR = BASE_DIR / "site" / "images" / "emblems"

VALID_ROMAN = {
    'F', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X',
    'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX',
    'XXI', 'XXII', 'XXIII', 'XXIV', 'XXV', 'XXVI', 'XXVII', 'XXVIII', 'XXIX', 'XXX',
    'XXXI', 'XXXII', 'XXXIII', 'XXXIV', 'XXXV', 'XXXVI', 'XXXVII', 'XXXVIII', 'XXXIX', 'XL',
    'XLI', 'XLII', 'XLIII', 'XLIV', 'XLV', 'XLVI', 'XLVII', 'XLVIII', 'XLIX', 'L',
}


def main():
    conn = sqlite3.connect(DB_PATH)
    errors = 0

    # Check 1: Row count
    total = conn.execute("SELECT COUNT(*) FROM emblem_identity").fetchone()[0]
    if total != 51:
        print(f"  FAIL: Expected 51 rows, got {total}")
        errors += 1
    else:
        print(f"  OK: 51 rows present")

    # Check 2: No duplicate emblem_number
    dupes = conn.execute("""
        SELECT emblem_number, COUNT(*) as cnt
        FROM emblem_identity GROUP BY emblem_number HAVING cnt > 1
    """).fetchall()
    if dupes:
        print(f"  FAIL: Duplicate emblem_numbers: {dupes}")
        errors += 1
    else:
        print(f"  OK: No duplicate emblem_numbers")

    # Check 3: All roman_label values valid
    labels = conn.execute("SELECT emblem_number, roman_label FROM emblem_identity").fetchall()
    invalid = [(n, r) for n, r in labels if r not in VALID_ROMAN]
    if invalid:
        print(f"  FAIL: Invalid roman_labels: {invalid}")
        errors += 1
    else:
        print(f"  OK: All roman_labels valid")

    # Check 4: HIGH confidence entries have image files
    high_entries = conn.execute("""
        SELECT emblem_number, roman_label, image_filename
        FROM emblem_identity WHERE alignment_confidence = 'HIGH'
    """).fetchall()
    missing_images = []
    for num, roman, fname in high_entries:
        if not fname:
            missing_images.append((num, roman, "no filename"))
        elif not (IMAGES_DIR / fname).exists():
            missing_images.append((num, roman, f"{fname} not found"))
    if missing_images:
        print(f"  FAIL: HIGH confidence entries missing images:")
        for num, roman, reason in missing_images:
            print(f"    Emblem {roman}: {reason}")
        errors += 1
    else:
        print(f"  OK: All {len(high_entries)} HIGH confidence entries have image files")

    # Check 5: Consistency with emblems table
    emblem_nums = set(r[0] for r in conn.execute("SELECT number FROM emblems").fetchall())
    identity_nums = set(r[0] for r in conn.execute("SELECT emblem_number FROM emblem_identity").fetchall())
    if emblem_nums != identity_nums:
        only_emblems = emblem_nums - identity_nums
        only_identity = identity_nums - emblem_nums
        if only_emblems:
            print(f"  FAIL: In emblems but not identity: {sorted(only_emblems)}")
        if only_identity:
            print(f"  FAIL: In identity but not emblems: {sorted(only_identity)}")
        errors += 1
    else:
        print(f"  OK: emblem_identity matches emblems table (51 entries)")

    # Summary report
    with_image = conn.execute(
        "SELECT COUNT(*) FROM emblem_identity WHERE image_filename IS NOT NULL"
    ).fetchone()[0]
    without_image = total - with_image
    high = conn.execute(
        "SELECT COUNT(*) FROM emblem_identity WHERE alignment_confidence = 'HIGH'"
    ).fetchone()[0]
    medium = conn.execute(
        "SELECT COUNT(*) FROM emblem_identity WHERE alignment_confidence = 'MEDIUM'"
    ).fetchone()[0]
    low = conn.execute(
        "SELECT COUNT(*) FROM emblem_identity WHERE alignment_confidence = 'LOW'"
    ).fetchone()[0]
    null_conf = conn.execute(
        "SELECT COUNT(*) FROM emblem_identity WHERE alignment_confidence IS NULL"
    ).fetchone()[0]

    conn.close()

    print(f"\n=== EMBLEM IDENTITY REPORT ===")
    print(f"  Total emblems:      {total}")
    print(f"  Images present:     {with_image}")
    print(f"  Missing images:     {without_image}")
    print(f"  Confidence: HIGH={high}, MEDIUM={medium}, LOW={low}, NULL={null_conf}")
    print(f"  Errors:             {errors}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
