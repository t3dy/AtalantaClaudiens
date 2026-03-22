"""Add Peter Forshaw as a scholar + add missing mythological figures to dictionary.

From FORSHAWREPORT.md analysis of Forshaw's lecture on AF.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'atalanta.db')


FORSHAW_PROFILE = (
    "Peter J. Forshaw is a historian of Western esotericism at the Center for the History of Hermetic "
    "Philosophy and Related Currents (GHF), University of Amsterdam. His research focuses on the intersection "
    "of alchemy, Kabbalah, and natural philosophy in the early modern period, with particular expertise in "
    "Heinrich Khunrath, Michael Maier, and John Dee.\n\n"

    "Forshaw approaches Maier through the lens of what he terms 'mytho-alchemy' — the systematic practice of "
    "reading classical mythology as encoded alchemical teaching. He identifies Maier as 'the main figurehead' "
    "for this tradition, distinguishing it from gold-making alchemy, chemical medicine, and Khunrath's "
    "theo-alchemy. Forshaw argues that Maier's Arcana Arcanissima (1614) is the foundational text of "
    "mytho-alchemy, with the Atalanta Fugiens as its visual culmination.\n\n"

    "Forshaw's detailed analysis of the AF emblems reveals structural features overlooked by other scholars. "
    "He demonstrates that Maier organizes each emblem's discourse around the four disciplines of the medieval "
    "quadrivium — arithmetic, music, geometry, and astronomy — systematically mapping each alchemical concept "
    "across all four mathematical sciences. He also identifies sources not noted by De Jong, including "
    "Horapollo's Hieroglyphica as a model for Emblem XXVII's impossibility motif, Ficino's De Vita Libri Tres "
    "as a source for Emblem IX's rejuvenation imagery, and Khalid ibn Yazid's Kitab al-Thalath Kalimat for "
    "the gestation metaphor in Emblem I.\n\n"

    "Forshaw is emphatic that Maier is 'not Paracelsian' — the AF works exclusively with the Mercury-Sulphur "
    "dyad without Paracelsus's third principle (Salt). He also insists that Maier preferred the term 'chemical' "
    "over 'alchemical' and explicitly described his work as natural rather than supernatural, even as later "
    "interpreters have read spiritual dimensions into it. Forshaw acknowledges 'parallel processing' in Maier's "
    "work — a mirroring between alchemical transformation and personal spiritual development — but maintains "
    "that the primary register is laboratory chemistry.\n\n"

    "His published article 'Laboratorium, Auditorium, Oratorium' examines alchemical music including Maier's "
    "fugues, and his webinar lectures for the Ritman Library's Infinite Fire series have introduced Maier's "
    "work to a broad digital audience. For this site, Forshaw's mytho-alchemical framework and his quadrivium "
    "analysis provide essential context for understanding how Maier structured each emblem as a multi-dimensional "
    "intellectual exercise."
)

# Missing mythological figures that appear in AF (from Forshaw's lecture)
NEW_DICT_TERMS = [
    {
        "slug": "hercules",
        "label": "Hercules",
        "category": "FIGURE",
        "label_latin": "Hercules",
        "definition_short": "Greek hero whose twelve labors include stealing the golden apples of the Hesperides; archetype of the alchemist in Maier's mytho-alchemy.",
        "definition_long": (
            "Hercules (Greek Heracles) is the divine hero of Greek mythology whose twelve labors represent the "
            "supreme tests of human strength and ingenuity. In the alchemical tradition developed by Maier, Hercules "
            "serves as one of the primary archetypes of the alchemist — alongside Ulysses and Jason — figures who "
            "undertake impossible quests and succeed through a combination of physical endurance, divine aid, and "
            "cunning. His eleventh labor, stealing the golden apples from the Garden of the Hesperides, appears "
            "prominently on the frontispiece of the Atalanta Fugiens, where Hercules in his lion-skin reaches for "
            "the fruit of immortality guarded by the dragon Ladon and the three Hesperides."
        ),
        "significance_to_af": "Hercules appears on the AF frontispiece reaching for the golden apples of the Hesperides. Forshaw identifies him as Maier's archetype of the alchemist — the hero who uses both strength and cunning to obtain the fruit of immortality (the philosopher's stone). His lion-skin connects him to the alchemical lion symbolism that recurs throughout the fifty emblems.",
        "emblem_links": [0],
    },
    {
        "slug": "cybele",
        "label": "Cybele",
        "category": "FIGURE",
        "label_latin": "Cybele",
        "definition_short": "Phrygian mother goddess who transforms Atalanta and Hippomenes into lions as punishment for profaning her temple.",
        "definition_long": (
            "Cybele (also Kybele) is the Phrygian mother goddess adopted into Greek and Roman religion as Magna Mater, "
            "the Great Mother. In the myth of Atalanta and Hippomenes retold by Ovid and adopted by Maier, the young "
            "couple consummate their love in Cybele's temple, provoking the goddess to transform them into the lions "
            "that pull her chariot. In Maier's alchemical reading, this transformation represents the fixation of "
            "the volatile (Atalanta/Mercury) and the fixed (Hippomenes/Sulphur) into a stable, powerful form — the "
            "lions being traditional alchemical symbols for mature, activated substances."
        ),
        "significance_to_af": "Cybele appears on the AF frontispiece where the transformation of Atalanta and Hippomenes into lions is depicted. The couple embraces in her temple entrance before emerging behind it as lion and lioness. Forshaw notes that Cybele's chariot is traditionally pulled by lions, connecting the mythological punishment to the alchemical symbolism of the winged and wingless lions that recur throughout the emblem series.",
        "emblem_links": [0],
    },
    {
        "slug": "boreas",
        "label": "Boreas",
        "category": "FIGURE",
        "label_latin": "Boreas",
        "definition_short": "Greek god of the North Wind who carries the philosophical embryo in his belly; central figure of Emblem I.",
        "definition_long": (
            "Boreas is the Greek personification of the North Wind, one of the four Anemoi (wind gods). In Maier's "
            "Atalanta Fugiens, Boreas appears in Emblem I as a dramatic male figure with streaming hair, carrying "
            "an embryo in his belly — a visual literalization of the Emerald Tablet's declaration that 'the wind "
            "carried it in its belly.' Forshaw notes that Boreas is unusual as a male representation of Mercury "
            "(quicksilver), since Mercury is more typically female in alchemical allegory. Maier draws on the "
            "Pseudo-Lullian tradition where argent vive (quicksilver) is the prima materia from which God creates "
            "everything — Boreas carrying the sulfurous seed represents the volatile substance bearing the "
            "generative principle within itself."
        ),
        "significance_to_af": "Boreas is the central figure of Emblem I, visualizing the Emerald Tablet's teaching. Forshaw identifies him as Mercury/quicksilver in the Pseudo-Lullian tradition of argent vive. His two sons (red-haired and white-haired) represent Sulphur and Quicksilver. The Ritman Library's 17th-century painting pairs this first emblem with the last (Emblem L), suggesting the work's circular structure.",
        "emblem_links": [1],
    },
    {
        "slug": "jason",
        "label": "Jason",
        "category": "FIGURE",
        "label_latin": "Iason",
        "definition_short": "Greek hero who quests for the Golden Fleece, slaying the dragon that guards it; alchemical archetype of the seeker.",
        "definition_long": (
            "Jason is the leader of the Argonauts in Greek mythology, famous for his quest to obtain the Golden "
            "Fleece from Colchis. The fleece, guarded by a sleepless dragon, can only be obtained through a "
            "combination of divine aid (Medea's magic), heroic courage, and the slaying of the guardian. In the "
            "alchemical tradition that Maier draws upon, the Golden Fleece represents the philosopher's stone or "
            "the perfected tincture, and the quest narrative maps onto the stages of the alchemical work. The "
            "dragon that must be slain corresponds to the prima materia that must be dissolved before the 'golden' "
            "product can be extracted."
        ),
        "significance_to_af": "Jason appears as one of Maier's three archetypes of the alchemist (alongside Hercules and Ulysses). The Golden Fleece quest is explicitly referenced in Emblem XXV, where the dragon must be killed by Sol and Luna before the treasure can be obtained. Forshaw notes that dragons guarding gold is a persistent motif connecting the Hesperides, the Golden Fleece, and alchemical imagery.",
        "emblem_links": [25],
    },
    {
        "slug": "kronos-saturn",
        "label": "Kronos / Saturn",
        "category": "FIGURE",
        "label_latin": "Saturnus",
        "definition_short": "Titan who devours his children and vomits the stone; alchemical figure for dissolution, nigredo, and the prima materia.",
        "definition_long": (
            "Kronos (Roman Saturn) is the Titan who devoured his own children to prevent the prophecy of his "
            "overthrow, only to be tricked by Zeus into vomiting them up along with the stone that had been "
            "substituted for the infant god. In alchemical mytho-alchemy as practiced by Maier, Saturn represents "
            "the principle of dissolution and putrefaction — the nigredo stage where existing forms are broken down "
            "into prima materia. Saturn's devouring represents the universal solvent consuming all metals; his "
            "vomiting of the stone represents the emergence of the philosopher's stone from the dissolved mass. "
            "The planet Saturn governs lead, melancholy, and the leaden darkness that must be overcome in the "
            "first stage of the work."
        ),
        "significance_to_af": "Saturn governs the nigredo emblems throughout AF. Forshaw notes that Maier discusses Saturn vomiting up the stone as an alchemical myth. The allegory of Saturn in Emblem X is interpreted as the dissolution of metals back into mercurial prima materia. Saturn's planetary influence (coldness, blackness, melancholy) maps onto the first stage of every alchemical operation depicted in the series.",
        "emblem_links": [10, 22, 24],
    },
    {
        "slug": "ulysses-odysseus",
        "label": "Ulysses / Odysseus",
        "category": "FIGURE",
        "label_latin": "Ulysses",
        "definition_short": "Greek hero of endurance and wisdom; Maier's self-identification in his final work, representing the alchemist who perseveres through shipwreck.",
        "definition_long": (
            "Ulysses (Greek Odysseus) is the hero of Homer's Odyssey, celebrated for his cunning intelligence "
            "(metis), endurance through trials, and ultimate homecoming after twenty years of wandering. Maier "
            "adopted Ulysses as a personal emblem in his final published work, Ulysses (1624, posthumous), where "
            "the hero's journey becomes an allegory for Maier's own life — a physician-alchemist who traveled from "
            "Kiel to Padua, Prague, London, Frankfurt, and Magdeburg before dying far from home. Forshaw identifies "
            "Ulysses alongside Hercules and Jason as one of Maier's three archetypes of the alchemist: heroes who "
            "combine wisdom, practical skill, and divine favor to complete impossible tasks."
        ),
        "significance_to_af": "Though Ulysses does not appear directly in the AF emblems, he represents Maier's self-understanding as an alchemist-wanderer. The AF's emphasis on the alchemist following nature's footsteps (Emblem XLII) and the need for both experience and reason echoes Odyssean themes of learning through suffering and observation. Maier's last book, Ulysses, explicitly frames the alchemical quest as an Odyssean homecoming.",
        "emblem_links": [42],
    },
    {
        "slug": "mytho-alchemy",
        "label": "Mytho-Alchemy",
        "category": "CONCEPT",
        "label_latin": "Mytho-Alchemia",
        "definition_short": "The practice of reading classical mythology as encoded alchemical teaching; Maier is identified by Forshaw as its 'main figurehead.'",
        "definition_long": (
            "Mytho-alchemy is a term used by Peter Forshaw to describe the systematic interpretation of Greek, "
            "Egyptian, and Roman mythology as concealed alchemical doctrine. The practice rests on the Hermetic "
            "assumption that ancient myths were not naive fictions but deliberate encodings of natural philosophical "
            "secrets, composed by sages who wished to transmit dangerous knowledge only to qualified readers. "
            "Maier's Arcana Arcanissima (1614) is the foundational text of mytho-alchemy, offering alchemical "
            "readings of the myths of Osiris, Atalanta, Hercules, Jason, and others. The Atalanta Fugiens "
            "represents the visual culmination of this method, transforming fifty mythological and allegorical "
            "scenes into an integrated alchemical curriculum."
        ),
        "significance_to_af": "The entire AF is an exercise in mytho-alchemy. Every emblem takes a mythological, biblical, or allegorical scene and reveals its alchemical content — the race of Atalanta, the labors of Hercules, the killing of Osiris, the riddle of the Sphinx. Forshaw's term captures what De Jong's source-critical method demonstrates empirically: Maier systematically reads myth as chemistry.",
        "emblem_links": [0, 4, 25, 39, 44],
    },
]


def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Add Forshaw as scholar
    existing = c.execute('SELECT id FROM scholars WHERE name = ?', ('Peter J. Forshaw',)).fetchone()
    if not existing:
        c.execute('''INSERT INTO scholars (name, specialization, af_focus, overview, review_status)
                     VALUES (?, ?, ?, ?, ?)''',
                  ('Peter J. Forshaw',
                   'Western esotericism, alchemy, Kabbalah',
                   'Mytho-alchemy, quadrivium structure, alchemical music',
                   FORSHAW_PROFILE,
                   'DRAFT'))
        print('Added scholar: Peter J. Forshaw')
    else:
        c.execute('UPDATE scholars SET overview = ? WHERE name = ?', (FORSHAW_PROFILE, 'Peter J. Forshaw'))
        print('Updated scholar: Peter J. Forshaw')

    # Add dictionary terms
    added = 0
    for term in NEW_DICT_TERMS:
        existing = c.execute('SELECT id FROM dictionary_terms WHERE slug = ?', (term['slug'],)).fetchone()
        if not existing:
            c.execute('''INSERT INTO dictionary_terms
                         (slug, label, category, label_latin, definition_short, definition_long,
                          significance_to_af, review_status)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                      (term['slug'], term['label'], term['category'], term['label_latin'],
                       term['definition_short'], term['definition_long'],
                       term['significance_to_af'], 'DRAFT'))
            term_id = c.lastrowid
            # Add emblem links
            for emblem_num in term.get('emblem_links', []):
                emblem_id = c.execute('SELECT id FROM emblems WHERE number = ?', (emblem_num,)).fetchone()
                if emblem_id:
                    c.execute('INSERT OR IGNORE INTO term_emblem_refs (term_id, emblem_id) VALUES (?, ?)',
                              (term_id, emblem_id[0]))
            added += 1
            print(f'  Added term: {term["label"]} ({term["category"]})')
        else:
            print(f'  Skipped (exists): {term["label"]}')

    conn.commit()

    # Final counts
    scholars = c.execute('SELECT count(*) FROM scholars').fetchone()[0]
    terms = c.execute('SELECT count(*) FROM dictionary_terms').fetchone()[0]
    conn.close()
    print(f'\nScholars: {scholars}, Dictionary terms: {terms} (+{added} new)')


if __name__ == '__main__':
    main()
