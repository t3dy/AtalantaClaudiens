#!/usr/bin/env python3
"""
extract_tilton.py — Extract scholarly references from Tilton's
'The Quest for the Phoenix' (2003) into scholarly_refs and emblem_sources.

Tilton discusses Atalanta Fugiens emblems throughout his study of Maier's
alchemical and Rosicrucian work. This script adds emblem-specific
interpretations identified by LLM-assisted reading of the full text.

All data: confidence='MEDIUM' (LLM-assisted extraction from Tilton).
Uses INSERT OR IGNORE to avoid duplicates.
"""

import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'atalanta.db')


def get_emblem_id(cursor, emblem_number):
    """Look up emblem id by emblem number."""
    cursor.execute("SELECT id FROM emblems WHERE number = ?", (emblem_number,))
    row = cursor.fetchone()
    return row[0] if row else None


def get_bib_id(cursor, source_id):
    """Look up bibliography id by source_id."""
    cursor.execute("SELECT id FROM bibliography WHERE source_id = ?", (source_id,))
    row = cursor.fetchone()
    return row[0] if row else None


def get_authority_id(cursor, name_fragment):
    """Look up source authority id by partial name match."""
    cursor.execute(
        "SELECT id FROM source_authorities WHERE name LIKE ?",
        (f'%{name_fragment}%',)
    )
    row = cursor.fetchone()
    return row[0] if row else None


def insert_scholarly_refs(cursor, bib_id):
    """Insert Tilton's emblem-specific scholarly interpretations."""

    refs = [
        # (emblem_number, interpretation_type, summary, source_texts_referenced, section_page)
        (1, 'ALCHEMICAL',
         "Tilton connects discourse 1 to Maier's critique of Agrippa's claims about extracting spirit from gold. Maier argues Agrippa was impoverished despite his claims, illustrating the futility of charlatanism versus true chemia.",
         json.dumps(["Agrippa, De Occulta Philosophia"]),
         "Ch. IV, p. 123 (cf. Examen Fucorum)"),

        (4, 'ALCHEMICAL',
         "Tilton identifies the 'philothesia' in epigram 4 as a love potion offered at the Saturnalia. The brother-sister conjunction and nectar cup connect to Maier's Rosicrucian enigmas in Symbola Aureae Mensae, linking alchemical marriage to the fraternity's invitation.",
         json.dumps(["Symbola Aureae Mensae"]),
         "Ch. IV, pp. 143-144"),

        (6, 'HISTORICAL',
         "Tilton notes that discourse 6 references Ficino's De Vita Libri Tres (1489), raising the possibility that Maier was directly influenced by Ficino's Neoplatonic musical philosophy. This connects AF's fugal structure to Renaissance Hermetic musical cosmology.",
         json.dumps(["Ficino, De Vita Libri Tres"]),
         "Ch. V, pp. 183-184"),

        (9, 'ALCHEMICAL',
         "Tilton reads discourse 9 as Maier's statement that death is the only path to rejuvenation: 'there is nothing that can restore youth to man but death itself.' This encapsulates the paradoxical circular nature of Maier's spiritual alchemy, mirroring the ouroboros.",
         json.dumps([]),
         "Ch. V, p. 215"),

        (10, 'ALCHEMICAL',
         "Tilton discusses discourse 10's reference to the aqua foetida — the powerful spirit with the smell of sulphur and the grave — identified as the quintessence from Parnassus's fountain struck by Pegasus. This connects to Maier's Rosicrucian allegorical reading of the Fama Fraternitatis.",
         json.dumps([]),
         "Ch. IV, pp. 170-171"),

        (12, 'MYTHOLOGICAL',
         "Tilton connects discourse 12's retelling of the Chronos/Saturn myth (devouring children, tricked by a stone) to the broader Saturnian framework of Maier's alchemy. The difficult ascent of Helicon to see the stone parallels the alchemical ladder of the Scala Arcis Philosophicae.",
         json.dumps(["Macrobius, Saturnalia"]),
         "Ch. III, p. 96 (cf. Examen Fucorum)"),

        (18, 'ALCHEMICAL',
         "Tilton reads discourse 18 as Maier's refutation of instant transmutation ('projection') — those who claim to convert metals in the time it takes to eat an egg. Maier rejects antimony-based projection as charlatanism, insisting on slow fermentation mimicking natural processes.",
         json.dumps(["Ruland, Lexicon Alchemiae"]),
         "Ch. III, pp. 96-98"),

        (21, 'ALCHEMICAL',
         "Tilton interprets the squaring of the circle through Aristotelian elemental transmutation rather than the Paracelsian tria prima. The circle-square-triangle-circle sequence represents the cosmic work from monad through elements to perfected unity, the return to the Monad.",
         json.dumps(["AUTH_ROSARIUM"]),
         "Ch. V, pp. 186-188"),

        (22, 'ALCHEMICAL',
         "Tilton discusses discourse 22's quotation of Rhazes: Saturn opens the gates of knowledge and lead is the father of all metals. Saturn/lead as the materia artis is the indispensable first step on Maier's alchemical ladder, connecting to Saturnus Sterculius — the god of manure, the thing of little value trampled in the dungheap.",
         json.dumps(["Rhazes (al-Razi)"]),
         "Ch. II, pp. 41-42"),

        (28, 'ALCHEMICAL',
         "Tilton reads discourse 28's Duenech allegory as purification through sweating: the melancholic king enters the bath to expel impurities. Maier explains this as purification of both human and metallic bodies. The allegory connects to the Merlini tradition and Maier's own illness while writing Symbola Aureae Mensae.",
         json.dumps(["Duenech Allegory", "Allegory of Merlin"]),
         "Ch. IV, pp. 142-143"),

        (36, 'HISTORICAL',
         "Tilton contextualizes discourse 36 within Maier's German nationalism. Following Tacitus, Maier boasts of the Cimbri who defeated Roman legions. The alchemical truth conveyed is that earth, though the last repository of putrefied things, is also most precious as the mother of all things — and German earth most of all.",
         json.dumps(["Tacitus, Germania"]),
         "Ch. V, pp. 199-200"),

        (37, 'ALCHEMICAL',
         "Tilton pairs discourse 37 with discourse 10 as references to the aqua foetida — the sulphurous, grave-smelling spirit used in alchemical solution. This is the 'perpetual spring' or quintessence that Pegasus struck from Parnassus, central to Maier's Rosicrucian allegory.",
         json.dumps([]),
         "Ch. IV, p. 171"),

        (39, 'ALCHEMICAL',
         "Tilton gives extensive treatment to discourse 39 as Maier's most personal statement on the alchemical quest. Quoting Baqsam from the Turba Philosophorum, Maier warns that truth comes only through error and grief. The Sphinx riddle allegory means those who fail to solve nature's enigmas are destroyed by grief in the Art.",
         json.dumps(["AUTH_TURBA"]),
         "Ch. V, pp. 214-215"),

        (42, 'ALCHEMICAL',
         "Tilton connects emblem 42 to Daniel Stoltzius's reception of Maier. Nature, reason, experience and reading are the guide, staff, spectacles and lamp of the alchemist. Maier insists the first intention must be to discover through intimate contemplation how Nature proceeds — a staple of medieval alchemical literature reinforced by Paracelsian empiricism.",
         json.dumps([]),
         "Ch. VI, pp. 238-239"),

        (46, 'ALCHEMICAL',
         "Tilton reads emblem 46 in the context of the Allegoria Bella: two eagles circumnavigating the globe from east and west signify masculine Sulphur and feminine Mercury. The eagle restores itself to youth by plunging three times into a fountain, linking to the cyclical processes in the vessel and Maier's own circumnavigation-pilgrimage.",
         json.dumps(["Symbola Aureae Mensae, Allegoria Bella"]),
         "Ch. V, pp. 221-222"),
    ]

    count = 0
    for emblem_num, interp_type, summary, sources, page in refs:
        emblem_id = get_emblem_id(cursor, emblem_num)
        if emblem_id is None:
            print(f"  WARNING: Emblem {emblem_num} not found in DB, skipping")
            continue

        # Check for existing duplicate (same emblem + bib + similar summary start)
        cursor.execute(
            """SELECT id FROM scholarly_refs
               WHERE emblem_id = ? AND bib_id = ? AND section_page = ?""",
            (emblem_id, bib_id, page)
        )
        if cursor.fetchone():
            print(f"  Emblem {emblem_num}: already exists for section {page}, skipping")
            continue

        cursor.execute(
            """INSERT INTO scholarly_refs
               (emblem_id, bib_id, interpretation_type, summary,
                source_texts_referenced, section_page, confidence)
               VALUES (?, ?, ?, ?, ?, ?, 'MEDIUM')""",
            (emblem_id, bib_id, interp_type, summary, sources, page)
        )
        count += 1
        print(f"  Emblem {emblem_num}: added {interp_type} ref")

    return count


def insert_emblem_sources(cursor):
    """Insert source authority connections identified by Tilton."""

    # Source connections Tilton explicitly makes for AF emblems
    # (emblem_number, authority_name_fragment, relationship_type, notes)
    sources = [
        # Emblem 22: Rhazes quoted on Saturn/lead
        (22, 'Turba', 'DISCOURSE_CITATION',
         'Tilton notes Maier quotes Rhazes on Saturn as gate of knowledge (Ch. II, p. 42)'),

        # Emblem 28: Duenech allegory and Merlini
        (28, 'Merlini', 'THEMATIC_PARALLEL',
         'Tilton connects discourse 28 to the Allegory of Merlin tradition (Ch. IV, p. 142)'),

        # Emblem 39: Turba Philosophorum (Baqsam)
        # Already likely exists, but INSERT OR IGNORE handles it
        (39, 'Turba', 'DISCOURSE_CITATION',
         'Tilton: Baqsam from Turba quoted on patience and error in the Art (Ch. V, p. 214)'),

        # Emblem 21: Rosarium Philosophorum
        # Already likely exists
        (21, 'Rosarium', 'DISCOURSE_CITATION',
         'Tilton: Rosarium is source for squaring the circle dictum (Ch. V, p. 186)'),

        # Emblem 6: Ficino (not a source authority yet — skip, no matching authority)

        # Emblem 46: No specific classical source authority — Tilton links to Allegoria Bella

        # Emblem 12: Lactantius tradition (phoenix) — check if relevant
        (12, 'Ovid', 'THEMATIC_PARALLEL',
         'Tilton: Saturn/Chronos myth from classical tradition retold in discourse 12 (Ch. III, p. 96)'),
    ]

    count = 0
    for emblem_num, auth_fragment, rel_type, notes in sources:
        emblem_id = get_emblem_id(cursor, emblem_num)
        authority_id = get_authority_id(cursor, auth_fragment)

        if emblem_id is None:
            print(f"  WARNING: Emblem {emblem_num} not found, skipping source link")
            continue
        if authority_id is None:
            print(f"  WARNING: Authority matching '{auth_fragment}' not found, skipping")
            continue

        # Check for existing link
        cursor.execute(
            """SELECT id FROM emblem_sources
               WHERE emblem_id = ? AND authority_id = ? AND relationship_type = ?""",
            (emblem_id, authority_id, rel_type)
        )
        if cursor.fetchone():
            print(f"  Emblem {emblem_num} <-> {auth_fragment}: already linked, skipping")
            continue

        cursor.execute(
            """INSERT INTO emblem_sources
               (emblem_id, authority_id, relationship_type, notes, confidence)
               VALUES (?, ?, ?, ?, 'MEDIUM')""",
            (emblem_id, authority_id, rel_type, notes)
        )
        count += 1
        print(f"  Emblem {emblem_num} <-> {auth_fragment}: added {rel_type}")

    return count


def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Verify Tilton exists in bibliography
    bib_id = get_bib_id(cursor, 'tilton_2003')
    if bib_id is None:
        print("ERROR: tilton_2003 not found in bibliography table")
        return

    print(f"Tilton bibliography entry: id={bib_id}")
    print()

    # Count before
    cursor.execute("SELECT COUNT(*) FROM scholarly_refs")
    refs_before = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM emblem_sources")
    sources_before = cursor.fetchone()[0]

    print(f"Before: {refs_before} scholarly_refs, {sources_before} emblem_sources")
    print()

    # Insert scholarly refs
    print("=== Inserting Tilton scholarly_refs ===")
    refs_added = insert_scholarly_refs(cursor, bib_id)
    print()

    # Insert emblem source links
    print("=== Inserting Tilton emblem_sources ===")
    sources_added = insert_emblem_sources(cursor)
    print()

    conn.commit()

    # Count after
    cursor.execute("SELECT COUNT(*) FROM scholarly_refs")
    refs_after = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM emblem_sources")
    sources_after = cursor.fetchone()[0]

    print(f"After: {refs_after} scholarly_refs, {sources_after} emblem_sources")
    print(f"Added: {refs_added} scholarly_refs, {sources_added} emblem_sources")

    # Summary of Tilton refs
    cursor.execute(
        """SELECT e.number, sr.interpretation_type, sr.section_page
           FROM scholarly_refs sr
           JOIN emblems e ON e.id = sr.emblem_id
           WHERE sr.bib_id = ?
           ORDER BY e.number""",
        (bib_id,)
    )
    print()
    print("=== All Tilton refs in DB ===")
    for row in cursor.fetchall():
        itype = row[1] or 'N/A'
        print(f"  Emblem {row[0]:2d}: {itype:<14s} | {row[2]}")

    conn.close()


if __name__ == '__main__':
    main()
