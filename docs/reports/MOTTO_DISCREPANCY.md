# Motto Numbering Discrepancy — Investigation

## Finding
Emblem I and II both have the motto "His nurse is the earth" in the database.
F&F confirms:
- Emblem I = "Portavit eum ventus in ventre suo" (The wind carried him in his belly)
- Emblem II = "Nutrix ejus terra est" (His nurse is the earth)

## Root Cause
The seed JSON pre-assigned "His nurse is the Earth" as Emblem I's label. The extraction then found EMBLEM I in De Jong's text and extracted a motto — but the regex may have matched the wrong section, or the section boundary overlapped with Emblem II's content.

Both Emblem 1 and Emblem 2 in the DB have identical mottos, confirming a duplication.

## Impact
- Emblem I's motto is wrong (should be about wind, not nursing)
- Emblem II's motto is correct but duplicated from I
- The canonical_label for Emblem I is wrong ("His nurse is the Earth" → should be something like "The wind carried him")
- All 48 other emblems appear unaffected

## Fix Required
1. Correct seed JSON: Emblem I label → "The wind carried him in his belly"
2. Re-extract or manually set Emblem I motto_english → "The wind carried him in his belly"
3. Verify Emblem II motto is independently extracted (not copied from I)
4. Update manifest with correct Latin mottos

## Status
Documented. Fix deferred to next content session.
