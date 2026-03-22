#!/usr/bin/env python3
"""
fix_term_links.py — Add emblem links for 11 dictionary terms that have zero connections.

Each mapping is based on:
- The term's significance_to_af text (which mentions specific emblems)
- Grep results from the De Jong / Tilton / Craven corpus
- Alchemical domain knowledge of Atalanta Fugiens

Uses INSERT OR IGNORE since PK is (term_id, emblem_id).
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'atalanta.db')


def get_emblem_id(cursor, emblem_number):
    """Look up emblem id by emblem number."""
    cursor.execute("SELECT id FROM emblems WHERE number = ?", (emblem_number,))
    row = cursor.fetchone()
    if row:
        return row[0]
    raise ValueError(f"No emblem with number {emblem_number}")


# Mappings: term_id -> [(emblem_number, context), ...]
# Rationale documented per term.
TERM_LINKS = {
    # Citrinitas (id=4, PROCESS) — yellowing phase between albedo and rubedo.
    # significance_to_af: Tilton reads yellowing into Emblem XXI (geometric progression).
    # Tilton also places it in color sequence (black-white-yellow-red) spanning late emblems.
    # Emblem 42 (XLIII) references color transformations; Emblem 36 references the Stone in air/rivers.
    4: [
        (21, "Tilton reads the yellowing into Emblem XXI geometric progression"),
        (36, "Stone living in air/rivers — intermediate vivification stage"),
        (42, "Color transformation sequence in the opus"),
    ],

    # Fugue (id=20, MUSICAL) — the three-voice musical form structuring all 50 emblems.
    # Every emblem has a fugue, but the frontispiece (0) introduces the conceit,
    # and Wescott's analysis focuses on Emblems XXIV and XLIV for musical structure.
    20: [
        (0, "Frontispiece introduces the three-voice fugue conceit"),
        (1, "First emblem fugue — Atalanta, Hippomenes, Apple voices"),
        (24, "Wescott analyzes musical dissonance in Emblem XXIV"),
        (44, "Wescott analyzes triple-time musical structure in Emblem XLIV"),
    ],

    # Atalanta (id=34, FIGURE) — the titular figure, volatile mercurial principle.
    # She appears in the frontispiece and structures all 50 emblems per De Jong.
    # Emblem 44 (Typhon/Osiris) and 50 (dragon/woman) dramatize volatile-fixed dynamics.
    34: [
        (0, "Frontispiece depicts the Atalanta-Hippomenes race"),
        (1, "First emblem — Earth as nurse, volatile principle introduced"),
        (44, "Typhon kills Osiris — volatile-fixed dynamic"),
        (50, "Dragon and woman — final volatile-fixed resolution"),
    ],

    # Hippomenes (id=35, FIGURE) — the alchemical adept, fixed principle.
    # Paired with Atalanta in the frontispiece and the pursuit allegory.
    35: [
        (0, "Frontispiece depicts Hippomenes pursuing Atalanta"),
        (1, "First emblem — fixed principle begins pursuit"),
        (21, "Circle from man and woman — coniunctio of pursuer and pursued"),
        (50, "Final emblem — culmination of the pursuit"),
    ],

    # Metamorphoses (id=43, SOURCE_TEXT) — Ovid's Metamorphoses X.560-704.
    # Source of the Atalanta-Hippomenes myth framing the entire work.
    # Frontispiece commentary draws directly on Ovid.
    43: [
        (0, "Frontispiece commentary draws on Metamorphoses X"),
        (44, "Typhon/Osiris — Ovidian mythological parallel"),
        (45, "Two eagles from East and West — mythological geography"),
    ],

    # De Veritate Artis Chemicae (id=47, SOURCE_TEXT) — Robertus Vallensis.
    # De Jong identifies it as source for frontispiece commentary.
    47: [
        (0, "Direct source for frontispiece commentary per De Jong"),
    ],

    # Secretum Nobilissimorum (id=48, SOURCE_TEXT) — Greverus.
    # De Jong identifies alongside Vallensis as frontispiece commentary source.
    48: [
        (0, "Source for frontispiece commentary alongside Vallensis"),
    ],

    # Fama Fraternitatis (id=50, SOURCE_TEXT) — Rosicrucian manifesto.
    # Tilton: provides ideological framework, no direct motto derivation.
    # Most relevant to late emblems where philosophical-spiritual register intensifies.
    50: [
        (0, "Rosicrucian ideological framework for the entire work"),
        (49, "Philosophical Child and triple fathers — Rosicrucian spiritual register"),
        (50, "Final emblem — culmination of spiritual-alchemical synthesis"),
    ],

    # Aqua Regia (id=66, SUBSTANCE) — universal solvent dissolving gold.
    # Related to dissolution imagery. Emblem 12: washing Latona white (purification).
    # Emblem 28: king bathed, freed from black bile. Emblem 6: dissolution/coagulation.
    66: [
        (6, "Dissolution and coagulation of metals"),
        (12, "Make Latona white — purification through powerful solvent"),
        (28, "King bathed and freed from black bile — dissolution imagery"),
    ],

    # Cauda Pavonis (id=72, CONCEPT) — peacock's tail, intermediate color spectrum.
    # Tilton: between nigredo and albedo, the multi-colored peacock phase.
    # Craven: peacock refers to dragon's tail and changing colors.
    # Color transformation emblems in the middle sequence.
    72: [
        (21, "Geometric progression — intermediate color phase"),
        (34, "Born in bath, becomes red — color transformation"),
        (42, "Color transformation in the opus sequence"),
    ],

    # Pelicanus (id=73, CONCEPT) — pelican vessel and Christological self-sacrifice.
    # Tilton: pelican represents the red phase (rubedo).
    # Circulatio theme — the Work feeds upon itself.
    # Emblem 50: dragon and woman bathing in blood — self-sacrifice motif.
    73: [
        (34, "Strides over waters having become red — rubedo phase"),
        (44, "Osiris scattered and reassembled — self-sacrifice and renewal"),
        (50, "Dragon and woman bathe in blood — circulatio and self-sacrifice"),
    ],
}


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    total_inserted = 0
    for term_id, links in TERM_LINKS.items():
        # Verify term exists
        cur.execute("SELECT slug FROM dictionary_terms WHERE id = ?", (term_id,))
        term_row = cur.fetchone()
        if not term_row:
            print(f"  WARNING: term_id {term_id} not found, skipping")
            continue

        term_slug = term_row[0]
        for emblem_number, context in links:
            emblem_id = get_emblem_id(cur, emblem_number)
            cur.execute(
                "INSERT OR IGNORE INTO term_emblem_refs (term_id, emblem_id, context) VALUES (?, ?, ?)",
                (term_id, emblem_id, context)
            )
            if cur.rowcount > 0:
                total_inserted += 1
                print(f"  {term_slug} -> Emblem {emblem_number}: {context}")
            else:
                print(f"  {term_slug} -> Emblem {emblem_number}: (already exists)")

    conn.commit()
    conn.close()

    print(f"\nInserted {total_inserted} new term-emblem links.")

    # Verify: count terms still with zero links
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM dictionary_terms dt
        LEFT JOIN term_emblem_refs ter ON dt.id = ter.term_id
        WHERE ter.term_id IS NULL
    """)
    remaining = cur.fetchone()[0]
    conn.close()
    print(f"Terms with zero emblem links remaining: {remaining}")


if __name__ == '__main__':
    main()
