#!/usr/bin/env python3
"""
fill_missing_discourses.py — Fill 3 remaining NULL discourse_summary values.

Emblems XI, XXXVIII, and XLVIII were missed by regex extraction due to
severe OCR garbling in their section headers. This script inserts
manually extracted summaries from the De Jong markdown.

Usage:
    python scripts/fill_missing_discourses.py
"""

import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "atalanta.db"

# Import clean_text from the OCR cleanup module
sys.path.insert(0, str(Path(__file__).parent))
from clean_ocr_text import clean_text

# ─── Discourse summaries extracted from De Jong markdown ───
# Source: Helena Maria Elisabeth Jong Michael Maier s Atalanta fugiens...384.md

DISCOURSE_SUMMARIES = {
    11: (
        "The variety of writings of the authors is so great that searchers after truth "
        "would despair of reaching the ultimate aim of the art, as the allegorical stories "
        "are already difficult to understand and are the cause of many errors, still the "
        "more so when the same expressions are used for different things, and different "
        "expressions for the same things. The philosophers say that a clear intellect is "
        "not sufficient without manual labour, nor manual labour without a clear mind; "
        "theory is not sufficient without practice and vice versa. So as not to exhaust "
        "anybody too much by this study, the philosophers have used this emblematic "
        "pronouncement that Latona must be made white and that the books should be torn up. "
        "Latona is an imperfect body composed of Sol and Luna; she is dark with black stains "
        "on the face, which can only be washed away by making Latona white. The philosophers "
        "want to make the face of Latona thoroughly white and to change the skin; she should "
        "first be sought for and recognized, and if brought from a humble place, immersed in "
        "dung, for there she becomes really white and turns into white lead, and from this "
        "white lead originates red lead, and that is the beginning and end of the opus."
    ),
    38: (
        "When Socrates was asked whether he was a citizen of the town or of the world, he "
        "answered that though he was born in Athens as far as his body was concerned, he "
        "wandered all over the world with his spirit. In the same way, the Hermaphrodite is "
        "considered to be the inhabitant of two mountains, namely the mountains of Mercury "
        "and Venus, from where he also takes his name after his parents Hermes and Aphrodite. "
        "The mountains were unknown but became known all over the world through the fame of "
        "the Hermaphrodite. Morienus has to be considered all the more blessed by God because "
        "he came to know the birth-place of the Rebis from the mouth of living masters "
        "instead of from the books. The Philosophers' books may be considered as an immense "
        "ocean; the mountain of the Philosophical Mercury is the two-topped Parnassus, on "
        "the one top of which Hermes stays and on the other top Venus, and there Apollo and "
        "the Muses are to be found. It is no wonder that only one in thousands completes "
        "these labours of Hercules to set foot on top of the mountain and to be crowned "
        "with the laurel-wreath of immortality."
    ),
    48: (
        "Xerxes, the most powerful king of the Persians, liked to drink the muddy water a "
        "soldier brought him when he passed through dry desert regions with his army. In the "
        "same way the king about whom the Philosophers state that he was thirsty had fresh "
        "water brought to him, of which he drank till he was saturated, as is known from the "
        "Merlini-allegory. The recovery of the sick king was taken in hand by several "
        "physicians: first came the Egyptian physicians who expelled the coarse liquids, "
        "whereupon the king became unconscious, but then the Alexandrian physicians came and "
        "made the king healthy again. Curing the king about whom the Philosophers speak is "
        "rewarded still more amply than any worldly physician's fee. Bernard of Treves "
        "relates that the king gives to six of his courtiers as much power as he has himself, "
        "if they only wait till he himself has regained his youth in the bath and will be "
        "dressed with several clothes: a black cuirass, a white upper tunic and a "
        "purple-red cloak. Then he will give them of his blood and let them share his wealth."
    ),
}


def main():
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    for emblem_num, raw_summary in DISCOURSE_SUMMARIES.items():
        # Check current value
        row = cursor.execute(
            "SELECT discourse_summary FROM emblems WHERE number = ?",
            (emblem_num,)
        ).fetchone()

        if row is None:
            print(f"  [SKIP] Emblem {emblem_num}: not found in DB")
            continue

        if row[0] is not None:
            print(f"  [SKIP] Emblem {emblem_num}: already has discourse_summary")
            continue

        # Clean OCR artifacts
        cleaned = clean_text(raw_summary)

        cursor.execute(
            """UPDATE emblems
               SET discourse_summary = ?,
                   source_method = 'LLM_ASSISTED',
                   confidence = 'MEDIUM'
               WHERE number = ? AND discourse_summary IS NULL""",
            (cleaned, emblem_num)
        )
        print(f"  [OK] Emblem {emblem_num}: discourse_summary set ({len(cleaned)} chars)")

    conn.commit()

    # Verify
    print("\nVerification:")
    for num in sorted(DISCOURSE_SUMMARIES.keys()):
        row = cursor.execute(
            "SELECT number, source_method, confidence, LENGTH(discourse_summary) "
            "FROM emblems WHERE number = ?",
            (num,)
        ).fetchone()
        if row:
            print(f"  Emblem {row[0]}: source_method={row[1]}, confidence={row[2]}, length={row[3]}")

    # Check total coverage
    total = cursor.execute("SELECT COUNT(*) FROM emblems WHERE discourse_summary IS NOT NULL").fetchone()[0]
    total_all = cursor.execute("SELECT COUNT(*) FROM emblems").fetchone()[0]
    print(f"\nTotal discourse summaries: {total}/{total_all}")

    conn.close()
    print("Done.")


if __name__ == "__main__":
    main()
