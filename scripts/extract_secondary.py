"""
extract_secondary.py — Extract scholarly references from 4 secondary scholars.

Sources:
  1. Pagel (1973) — Book review of De Jong, Medical History
  2. Miner (2012) — Blake and Atalanta Fugiens, Notes and Queries
  3. Wescott (n.d.) — Alchemical King in Transformation, AthanorX
  4. Craven (1910) — Count Michael Maier biography, W. Peace & Sons

Populates:
  - bibliography (4 new entries)
  - scholars (4 new entries)
  - scholar_works (4 links)
  - scholarly_refs (emblem-specific interpretations)

Idempotent: uses INSERT OR IGNORE throughout.
All new data: source_method='LLM_ASSISTED', confidence='MEDIUM', review_status='DRAFT'
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "atalanta.db"


# ── Bibliography entries ──────────────────────────────────────────────

BIBLIOGRAPHY = [
    {
        "source_id": "pagel_1973",
        "author": "Walter Pagel",
        "title": "Review of Michael Maier's Atalanta Fugiens: Sources of an Alchemical Book of Emblems by H.M.E. De Jong",
        "year": 1973,
        "journal": "Medical History",
        "publisher": None,
        "pub_type": "review",
        "af_relevance": "DIRECT",
    },
    {
        "source_id": "miner_2012",
        "author": "Paul Miner",
        "title": "Blake and Atalanta Fugiens: Two Plates, Three Conjectures",
        "year": 2012,
        "journal": "Notes and Queries",
        "publisher": None,
        "pub_type": "article",
        "af_relevance": "DIRECT",
    },
    {
        "source_id": "wescott_nd",
        "author": "Catherine Morris Wescott",
        "title": "Atalanta Fugiens: The Alchemical King in Transformation",
        "year": None,
        "journal": "AthanorX",
        "publisher": None,
        "pub_type": "article",
        "af_relevance": "PRIMARY",
    },
    {
        "source_id": "craven_1910",
        "author": "J.B. Craven",
        "title": "Count Michael Maier: Doctor of Philosophy and of Medicine, Alchemist, Rosicrucian, Mystic, 1568-1622",
        "year": 1910,
        "journal": None,
        "publisher": "W. Peace & Sons",
        "pub_type": "monograph",
        "af_relevance": "CONTEXTUAL",
    },
]


# ── Scholar entries ───────────────────────────────────────────────────

SCHOLARS = [
    {
        "name": "Walter Pagel",
        "specialization": "History of Medicine",
        "af_focus": "Medical analogies in alchemical symbolism; Maier's relationship to Paracelsus and humoralism",
        "overview": "Medical historian who reviewed De Jong's 1969 edition of Atalanta Fugiens, highlighting Maier's use of medical analogies (dropsy, humoral cures) in alchemical emblems and his complex relationship to Paracelsus.",
        "key_works": ["pagel_1973"],
    },
    {
        "name": "Paul Miner",
        "specialization": "Blake Studies",
        "af_focus": "William Blake's borrowings from Atalanta Fugiens emblem imagery",
        "overview": "Blake scholar who identified specific visual borrowings from Maier's Atalanta Fugiens in Blake's Marriage of Heaven and Hell, Jerusalem, and Gates of Paradise, focusing on Emblems XXXIII and XXXIV.",
        "key_works": ["miner_2012"],
    },
    {
        "name": "Catherine Morris Wescott",
        "specialization": "Music and Alchemy",
        "af_focus": "Modal analysis of Maier's fugues as text-painting for alchemical Putrefaction and Albification",
        "overview": "Musicologist who analyzed four 'Alchemical King' emblems (XXIV, XXVIII, XXXI, XLIV) in Atalanta Fugiens, demonstrating how Maier used modal shifts and chromaticism in the fugues to parallel the King's transformation through Putrefaction and Albification.",
        "key_works": ["wescott_nd"],
    },
    {
        "name": "J.B. Craven",
        "specialization": "Biography, Rosicrucianism",
        "af_focus": "Biographical context for Maier's alchemical emblem work; survey of AF's contents and editions",
        "overview": "Early biographer of Michael Maier who provided the first English-language survey of Atalanta Fugiens, summarizing select emblems and cataloguing the 1617, 1618, 1687, and 1708 editions.",
        "key_works": ["craven_1910"],
    },
]


# ── Scholarly References ──────────────────────────────────────────────
# Each entry: (emblem_number, bib_source_id, interpretation_type, summary, source_texts_referenced, section_page)

SCHOLARLY_REFS = [
    # ── Pagel (1973) ──────────────────────────────────────────────────
    (16, "pagel_1973", "ALCHEMICAL",
     "Pagel identifies the winged lion in Emblem XVI as volatile Mercury (primeval water, moon) to be united with the wingless lion (Sulphur, sun), demonstrating Maier's systematic use of alchemical opposition symbolism.",
     '["AUTH_TURBA"]', "p. 101"),

    (28, "pagel_1973", "ALCHEMICAL",
     "Pagel discusses King Duenech as dropsical and discoloured, presented in a Turkish bath undergoing purgation of black bile until red colour returns, representing the alchemical work's characteristic colour changes from black to red.",
     None, "p. 101"),

    (48, "pagel_1973", "ALCHEMICAL",
     "Pagel notes Emblem XLVIII shows the King in his canopied bed accepting a potion, another representation of the alchemical colour-change process from black to red alongside Emblem XXVIII.",
     None, "p. 101"),

    (13, "pagel_1973", "ALCHEMICAL",
     "Pagel explains the 'dropsy of the ore' cured by purifying water comparable to the waters of Jordan which cured Naaman's leprosy, a comparison Maier took from medieval alchemical sources (Clangor buccinae and Aurora consurgens).",
     '["AUTH_AURORA_CONSURGENS"]', "p. 101"),

    (10, "pagel_1973", "ALCHEMICAL",
     "Pagel discusses Maier's Empedoclean cosmology in the discourse to Emblem X: air and earth as secondary elements arising from the conjunction of primary elements water (mercury) and fire (sulphur), the union of opposites.",
     None, "p. 102"),

    (2, "pagel_1973", "ICONOGRAPHIC",
     "Pagel identifies Emblem II's pregnant female figure with the terrestrial globe as symbolizing the earth as 'nurse of the tender child of the Philosophers', tracing its iconographic tradition to Albertus Magnus' Philosophia pauperum (1493) and Mylius' Philosophia reformata (1622).",
     '["AUTH_EMERALD_TABLE"]', "p. 102"),

    (0, "pagel_1973", "ALCHEMICAL",
     "Pagel connects the frontispiece imagery to the keynote myth of Atalanta dropping golden apples, the conjunction of Atalanta and Hippomenes, and their metamorphosis into lion and lioness, recognizing the alchemical principles of union of opposites (Sulphur and Mercury).",
     None, "p. 100"),

    # ── Miner (2012) ──────────────────────────────────────────────────
    (34, "miner_2012", "ICONOGRAPHIC",
     "Miner identifies Emblem XXXIV's imagery of a foetus emerging head-first from a supine nude female among clouds as a source for Blake's Marriage of Heaven and Hell plate 3, where a similar birth scene appears. The motto addresses 'conception' of a male 'born in the sky' relating to transmutation of metals.",
     None, "pp. 366-367"),

    (34, "miner_2012", "ICONOGRAPHIC",
     "Miner argues the lower portion of Emblem XXXIV, showing a nude masculine sun (with huge halo-like flames) and nude feminine moon kissing and sexually embracing, influenced Blake's hierogamos scene in Jerusalem 99.",
     None, "p. 367"),

    (33, "miner_2012", "ICONOGRAPHIC",
     "Miner connects Emblem XXXIII's blackened Hermaphrodite engulfed in flames beneath a waxing moon to Blake's revisions of the 'Fire' plate in For the Sexes: The Gates of Paradise, where Blake darkened Satan's body and added hermaphroditic features.",
     None, "p. 367"),

    (38, "miner_2012", "ICONOGRAPHIC",
     "Miner references Emblem XXXVIII's nude standing Hermaphrodite as a further instance of Maier's hermaphroditic imagery that may have influenced Blake's visual vocabulary.",
     None, "p. 367 n.8"),

    # ── Wescott (n.d.) ────────────────────────────────────────────────
    (24, "wescott_nd", "MUSICAL",
     "Wescott provides detailed modal analysis of Emblem XXIV's fuga: the Dorian mode (representing the King/Sun) undergoes musical alteration through chromatic shifts to resolve in the Venusian Hypolydian centered on C, paralleling the King's transformation from Putrefaction to Albification.",
     None, "pp. 3-4"),

    (24, "wescott_nd", "ICONOGRAPHIC",
     "Wescott reads Emblem XXIV's landscape as showing the King's simultaneous death (devoured by wolf/Saturn in foreground) and resurrection (walking toward river/water of Albification in background), with the circular building resembling an alchemical furnace.",
     None, "p. 3"),

    (28, "wescott_nd", "MUSICAL",
     "Wescott analyzes Emblem XXVIII's fuga: Atalanta enters at G and Hippomenes imitates at A. The E-flat/E-natural dissonance (minor second) represents the King Duenech's sufferings during his cure from Saturnian melancholy in the steam-bath.",
     None, "pp. 3-4"),

    (28, "wescott_nd", "ALCHEMICAL",
     "Wescott identifies King Duenech in Emblem XXVIII as being cured of Saturnian melancholy in the steam-bath, connecting the medical tradition of music curing Saturnian melancholy to the double cleansing function in alchemical operations.",
     None, "p. 2"),

    (31, "wescott_nd", "MUSICAL",
     "Wescott analyzes Emblem XXXI's fuga: the consistent E-flat and B-flat centered on D indicate the Phrygian mode (violence), while stately half-notes shifting to rapid quarter notes musically depict the King's cry for help as he drowns. All three voices are treble, denying stability.",
     None, "p. 4"),

    (31, "wescott_nd", "ICONOGRAPHIC",
     "Wescott notes Emblem XXXI's King wears a unique crown studded with gems and topped by five tri-lobes, distinct from all other King images in AF, serving as identification for the wise rescuer.",
     None, "p. 3"),

    (44, "wescott_nd", "MUSICAL",
     "Wescott analyzes Emblem XLIV's fuga: three voices enter simultaneously (unique in AF), the comes voice in triple-time parallels Osiris' dismemberment, and the piece resolves unexpectedly in Mixolydian Saturn rather than the expected C triad, reinforcing the cyclical nature of the alchemical process.",
     None, "pp. 4-5"),

    (44, "wescott_nd", "ICONOGRAPHIC",
     "Wescott reads Emblem XLIV's tripartite image: Isis over dismembered Osiris (left background), turbaned man at table with chalice, rebec, and beaker (right background), and the King found intact in a box (foreground), with the table objects symbolizing faith, music, and alchemy.",
     None, "pp. 4-5"),

    (44, "wescott_nd", "MYTHOLOGICAL",
     "Wescott identifies the Osiris-Typhon-Isis narrative in Emblem XLIV as symbolizing the Alchemical King's distribution throughout prima materia (dismemberment) and subsequent reunification, with the magus witnessing the complete alchemical process.",
     None, "p. 4"),

    # General Wescott refs (no specific emblem — about AF's musical structure)
    (None, "wescott_nd", "MUSICAL",
     "Wescott identifies the cantus firmus in all 50 fugues as 'Christe eleison' from Gregorian Mass IV (Cunctipotens genitor), following Helen Joy Sleeper's 1938 identification, noting the tripartite sung structure mirrors the three repetitions in the Mass.",
     None, "p. 2"),

    (None, "wescott_nd", "MUSICAL",
     "Wescott interprets the cantus firmus beginning on D (Sun/Dorian) and ending on G (Saturn/Mixolydian) as symbolizing the alchemical journey from the spiritual realm to the earthly sphere, following Streich's analysis of planetary-modal correspondences.",
     None, "p. 3"),

    # ── Craven (1910) ─────────────────────────────────────────────────
    (0, "craven_1910", "ICONOGRAPHIC",
     "Craven describes the frontispiece title-page: Venus handing golden apples to Hippomenes, Atalanta picking up one apple, the temple where the lovers embrace and emerge as lion and lioness, and Hercules reaching for the apples of the Hesperides above.",
     None, "pp. 87-88"),

    (34, "craven_1910", "ICONOGRAPHIC",
     "Craven calls Emblem 34 'probably the most curious picture' in AF, showing the Sun and Moon in human form in the act of coition standing in a pool of water.",
     None, "p. 89"),

    (1, "craven_1910", "ALCHEMICAL",
     "Craven summarizes Emblem 1: 'The wind has taken him in the belly' — the fruit concealed in the wind must come living to earth in right measure. The nurse thereof is the earth.",
     '["AUTH_EMERALD_TABLE"]', "p. 89"),

    (7, "craven_1910", "ALCHEMICAL",
     "Craven summarizes Emblem 7: the eagle in a hollow rock nourishes its young; one feathered easily rises while the featherless falls back, illustrating 'It ascends from earth to heaven, and again descends to earth.'",
     '["AUTH_EMERALD_TABLE"]', "p. 89"),

    (8, "craven_1910", "ALCHEMICAL",
     "Craven summarizes Emblem 8: 'Take the Egg and strike it with a glowing sword' — seek help from Mars the fire god, illustrating the strength of superiors and inferiors.",
     None, "p. 89"),

    (11, "craven_1910", "ALCHEMICAL",
     "Craven summarizes Emblem 11: 'Make Latona white and tear up the books' — the twin race born of Jove (Sun and Moon), with instruction to make Latona white in the face and tear up the books.",
     None, "p. 90"),

    (13, "craven_1910", "ALCHEMICAL",
     "Craven summarizes Emblem 13: the brass of the wise desires to be bathed seven times in the river, like leprous Naaman in Jordan.",
     None, "p. 90"),

    (14, "craven_1910", "ALCHEMICAL",
     "Craven summarizes Emblem 14: the dragon eating its own tail — hunger compels self-consumption and recreation, illustrating 'the strongest of all fortitudes.'",
     None, "p. 90"),

    (21, "craven_1910", "ALCHEMICAL",
     "Craven summarizes Emblem 21: squaring the circle — make of man and woman a circle, then quadrangle, then triangle, then circle again to obtain the Stone of the Wise.",
     None, "p. 90"),

    (23, "craven_1910", "MYTHOLOGICAL",
     "Craven summarizes Emblem 23: gold rains while Pallas is born at Rhodes and the sun lies by Venus, connecting the birth of Athena to the alchemical rain of gold in the vessel.",
     None, "p. 90"),

    (25, "craven_1910", "ALCHEMICAL",
     "Craven summarizes Emblem 25: the dragon that does not die unless killed by his brother (Apollo/Sun) and sister (Diana/Moon), the only means of its destruction.",
     None, "p. 90-91"),

    (29, "craven_1910", "ALCHEMICAL",
     "Craven summarizes Emblem 29: as the Salamander lives in fire, so does the Stone — the Philosopher's Stone is born in perpetual fire and stands in equal heat with the Salamander.",
     None, "p. 91"),

    (35, "craven_1910", "ALCHEMICAL",
     "Craven summarizes Emblem 35: as Ceres, Triptolemus, and Thetis Achilles lingered under fire, so will the maker of the Stone — fire as the milk from the mother's breast nourishing the medicine of the wise.",
     None, "p. 91"),

    (41, "craven_1910", "MYTHOLOGICAL",
     "Craven summarizes Emblem 41: Adonis killed by wild boar, Venus colours roses with his blood — the white rose becomes red through Venus' blood, and Adonis is laid to rest under soft lettuce.",
     None, "p. 91"),

    (43, "craven_1910", "ALCHEMICAL",
     "Craven summarizes Emblem 43: Atalanta listens to the Vulture declaring 'I alone am the white and black, the lemon yellow and the red' — the four colours of the alchemical work, from which the whole art proceeds.",
     None, "p. 91"),

    (39, "craven_1910", "ALCHEMICAL",
     "Craven notes Emblem 39 refers to Coral: a man fishing out a branch from water, the epigram explaining that Coral grows under water and becomes hard in air, 'sic lapis.'",
     None, "p. 92"),

    (45, "craven_1910", "ALCHEMICAL",
     "Craven summarizes Emblem 45: the earth in space with motto 'Sol et ejus umbra perficiunt opus' — silver as the shadow of gold, the Dragon must become as the Salamander in fire.",
     None, "p. 92"),
]


def main():
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")

    # ── 1. Bibliography ───────────────────────────────────────────────
    bib_added = 0
    for b in BIBLIOGRAPHY:
        cur = conn.execute("""
            INSERT OR IGNORE INTO bibliography
                (source_id, author, title, year, journal, publisher, pub_type, af_relevance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (b["source_id"], b["author"], b["title"], b["year"],
              b["journal"], b["publisher"], b["pub_type"], b["af_relevance"]))
        bib_added += cur.rowcount
    conn.commit()
    print(f"  bibliography: {bib_added} new entries added")

    # ── 2. Scholars ───────────────────────────────────────────────────
    sch_added = 0
    links_added = 0
    for s in SCHOLARS:
        cur = conn.execute("""
            INSERT OR IGNORE INTO scholars
                (name, specialization, af_focus, overview, review_status)
            VALUES (?, ?, ?, ?, 'DRAFT')
        """, (s["name"], s["specialization"], s["af_focus"], s["overview"]))
        sch_added += cur.rowcount

        # Link to bibliography
        scholar_row = conn.execute(
            "SELECT id FROM scholars WHERE name = ?", (s["name"],)
        ).fetchone()
        if scholar_row:
            for work_id in s.get("key_works", []):
                bib_row = conn.execute(
                    "SELECT id FROM bibliography WHERE source_id = ?", (work_id,)
                ).fetchone()
                if bib_row:
                    cur2 = conn.execute(
                        "INSERT OR IGNORE INTO scholar_works (scholar_id, bib_id) VALUES (?, ?)",
                        (scholar_row[0], bib_row[0])
                    )
                    links_added += cur2.rowcount

    conn.commit()
    print(f"  scholars: {sch_added} new entries, {links_added} work links added")

    # ── 3. Scholarly References ───────────────────────────────────────
    refs_added = 0
    for emblem_num, bib_source_id, interp_type, summary, source_texts, section_page in SCHOLARLY_REFS:
        # Look up emblem_id from emblem number
        emblem_id = None
        if emblem_num is not None:
            row = conn.execute(
                "SELECT id FROM emblems WHERE number = ?", (emblem_num,)
            ).fetchone()
            if row:
                emblem_id = row[0]

        # Look up bib_id
        bib_row = conn.execute(
            "SELECT id FROM bibliography WHERE source_id = ?", (bib_source_id,)
        ).fetchone()
        if not bib_row:
            print(f"  WARNING: bibliography '{bib_source_id}' not found, skipping ref")
            continue
        bib_id = bib_row[0]

        cur = conn.execute("""
            INSERT OR IGNORE INTO scholarly_refs
                (emblem_id, bib_id, interpretation_type, summary,
                 source_texts_referenced, section_page, confidence)
            VALUES (?, ?, ?, ?, ?, ?, 'MEDIUM')
        """, (emblem_id, bib_id, interp_type, summary, source_texts, section_page))
        refs_added += cur.rowcount

    conn.commit()
    print(f"  scholarly_refs: {refs_added} new references added")

    # ── 4. Summary by scholar ─────────────────────────────────────────
    print("\n  Per-scholar breakdown:")
    for b in BIBLIOGRAPHY:
        bib_row = conn.execute(
            "SELECT id FROM bibliography WHERE source_id = ?", (b["source_id"],)
        ).fetchone()
        if bib_row:
            count = conn.execute(
                "SELECT COUNT(*) FROM scholarly_refs WHERE bib_id = ?", (bib_row[0],)
            ).fetchone()[0]
            print(f"    {b['source_id']}: {count} refs")

    # Total counts
    total_refs = conn.execute("SELECT COUNT(*) FROM scholarly_refs").fetchone()[0]
    total_bib = conn.execute("SELECT COUNT(*) FROM bibliography").fetchone()[0]
    total_sch = conn.execute("SELECT COUNT(*) FROM scholars").fetchone()[0]
    print(f"\n  Totals: {total_bib} bibliography, {total_sch} scholars, {total_refs} scholarly_refs")

    conn.close()
    print("\nDone.")


if __name__ == "__main__":
    main()
