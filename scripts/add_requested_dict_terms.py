"""Add 8 dictionary terms requested by user: Quadrivium, Prisca Sapientia,
Steganography, Aurum Potabile, Medea, Geryon, Naaman, Apocalyptic Woman."""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'atalanta.db')

TERMS = [
    {
        "slug": "quadrivium",
        "label": "Quadrivium",
        "category": "CONCEPT",
        "label_latin": "Quadrivium",
        "definition_short": "The four mathematical disciplines of medieval university education: arithmetic, music, geometry, and astronomy.",
        "definition_long": (
            "The quadrivium comprises the four mathematical sciences of the medieval university curriculum: arithmetic, "
            "music, geometry, and astronomy. Together with the trivium (grammar, logic, rhetoric), they formed the "
            "seven liberal arts that constituted the foundation of educated discourse. Peter Forshaw demonstrates that "
            "Maier systematically structures each Atalanta Fugiens discourse around all four quadrivium disciplines, "
            "mapping every alchemical concept arithmetically (as the root of the cube), musically (as the disdiapason "
            "or double octave), geometrically (as a generative point on a flowing line), and astronomically (as the "
            "center of Saturn, Jupiter, and Mars). This quadrivium structure reveals Maier's ambition to present "
            "alchemy as a comprehensive mathematical-philosophical science, not merely a laboratory craft."
        ),
        "significance_to_af": (
            "Forshaw identifies the quadrivium as the organizing framework for each AF discourse. Maier's subtitle "
            "promises content for 'the eyes and intellect' and 'for the ears and for the soul's recreation,' mapping "
            "directly onto the quadrivium's four domains. The fifty fugues represent the musica branch; the geometric "
            "formula of Emblem XXI represents the geometry branch; and the astronomical references throughout map the "
            "alchemical work onto celestial correspondences."
        ),
        "emblem_links": [1, 21, 39],
    },
    {
        "slug": "prisca-sapientia",
        "label": "Prisca Sapientia",
        "category": "CONCEPT",
        "label_latin": "Prisca Sapientia",
        "definition_short": "The 'ancient wisdom' or perennial philosophy transmitted from Hermes Trismegistus through successive mystery schools to the modern age.",
        "definition_long": (
            "Prisca sapientia ('ancient wisdom') or philosophia perennis ('perennial philosophy') is the Renaissance "
            "belief that a single, coherent body of divine knowledge was transmitted from the earliest sages — "
            "particularly Hermes Trismegistus in Egypt — through successive civilizations and mystery schools to the "
            "present day. Tilton identifies this doctrine as the foundational framework of Maier's alchemical "
            "philosophy: Maier conceived of twelve mystery schools appearing chronologically in twelve nations, from "
            "Hermes through the Hebrews, Greeks, Romans, and Arabs to the Rosicrucian Brotherhood in modern Germany. "
            "The Symbola Aureae Mensae is organized around this scheme, and the Atalanta Fugiens draws on the same "
            "tradition by weaving Egyptian (Hermes, Osiris), Greek (Atalanta, Oedipus), and Arabic (Rhazes, Avicenna) "
            "sources into a single alchemical curriculum."
        ),
        "significance_to_af": (
            "Tilton argues that Maier's alchemy is not Paracelsian Tria Prima but prisca sapientia — a perennial "
            "wisdom transmitted through ancient source texts. The AF's systematic citation of authorities from "
            "the Turba Philosophorum through the Rosarium to Basil Valentine enacts this genealogy of wisdom. "
            "Godwin notes that Maier never uses the term philosophia perennis but 'obviously conceived of a "
            "perennial philosophy, a traditional wisdom handed down from the ancient days.'"
        ),
        "emblem_links": [0, 42],
    },
    {
        "slug": "steganography",
        "label": "Steganography",
        "category": "CONCEPT",
        "label_latin": "Steganographia",
        "definition_short": "The art of concealing messages within an apparently innocent cover text or image; Bilak argues AF contains a hidden magic square.",
        "definition_long": (
            "Steganography (from Greek steganos, 'covered,' and graphein, 'to write') is the practice of hiding "
            "messages within an innocuous carrier — a text, image, or composition that appears to communicate one "
            "thing while secretly encoding another. The tradition was codified by Trithemius in his Steganographia "
            "(c. 1499) and by Giambattista della Porta in De Furtivis Literarum Notis (1563). Donna Bilak's central "
            "thesis about the Atalanta Fugiens is that Maier engineered it as a steganographic work: the fifty "
            "sequential emblems can be reshuffled according to a mathematical magic square, revealing a hidden "
            "structure of binary pairs ('doublings') that encodes a second reading of the entire work. Bilak argues "
            "that Maier exploits the emblem form's inherent duality — the allegorical art of simultaneously "
            "concealing and revealing information — to create 'two books in one.'"
        ),
        "significance_to_af": (
            "Bilak's steganographic reading of AF won the 2022 Rosenzweig Prize (via Furnace and Fugue). She "
            "demonstrates patterns of 'doubling' in Emblems 1, 2, 26, and 50 that suggest intentional structural "
            "encoding. The magic square thesis proposes that the emblems' apparently sequential order conceals a "
            "second, non-linear reading accessible only to initiates who know the mathematical key."
        ),
        "emblem_links": [1, 2, 26, 50],
    },
    {
        "slug": "aurum-potabile",
        "label": "Aurum Potabile",
        "category": "SUBSTANCE",
        "label_latin": "Aurum Potabile",
        "definition_short": "Drinkable gold — the supreme alchemical medicine; Maier devoted his De Circulo Physico Quadrato (1616) to this concept.",
        "definition_long": (
            "Aurum potabile ('drinkable gold' or 'potable gold') is the alchemical preparation of gold in a form "
            "that can be ingested as a universal medicine. The concept rests on the Hermetic correspondence between "
            "the sun and gold: if gold is the material expression of solar virtue, then consuming gold should confer "
            "solar vitality on the human body. Maier dedicated his De Circulo Physico Quadrato (1616) to this "
            "doctrine, arguing that gold was 'the sun in the material sphere, just as the sun was the divine "
            "principle in the heavens.' Szulakowska notes that both Maier and Ficino discussed potable gold as a "
            "cure for melancholy and disease, connecting it to the broader Paracelsian project of iatrochemistry — "
            "the use of chemical preparations as medicines."
        ),
        "significance_to_af": (
            "Aurum potabile represents the practical medical goal underlying Maier's alchemical project. Godwin "
            "reveals that Maier claimed to have produced the Universal Medicine during his Kiel laboratory period "
            "(1602-1608), describing it as 'of a bright lemon color.' The AF's emphasis on the philosopher's stone "
            "as both a transmuting agent and a healing elixir reflects this dual aspiration — material "
            "transformation and medical cure as aspects of the same alchemical operation."
        ),
        "emblem_links": [9, 48],
    },
    {
        "slug": "medea",
        "label": "Medea",
        "category": "FIGURE",
        "label_latin": "Medea",
        "definition_short": "Sorceress of Greek mythology who rejuvenates old Aeson by boiling him in a cauldron; model for alchemical rejuvenation in Emblem IX.",
        "definition_long": (
            "Medea is the sorceress-princess of Colchis in Greek mythology, famous for helping Jason obtain the "
            "Golden Fleece and for her mastery of pharmaceutical magic. Among her most celebrated acts was the "
            "rejuvenation of Jason's elderly father Aeson, whom she restored to youth by draining his blood and "
            "replacing it with a potion of herbs and minerals boiled in a cauldron. In alchemical mytho-alchemy, "
            "Medea represents the active feminine principle (philosophical mercury) whose transformative power can "
            "dissolve and reconstitute the aged, impure body (the philosophical gold in its debased state). Her "
            "cauldron is the alchemical vessel, her potion the menstruum or solvent, and Aeson's rejuvenation "
            "the successful completion of the opus."
        ),
        "significance_to_af": (
            "Maier draws on the Medea/Aeson rejuvenation myth in Emblem IX, where the old man fixed to the tree "
            "in celestial dew is restored to youth. De Jong identifies the parallel between Medea's cauldron "
            "magic and the alchemical process of dissolution and reconstitution that the emblem depicts. Forshaw "
            "connects the rejuvenation motif to Ficino's De Vita Libri Tres on curing melancholy through "
            "astral-magical means."
        ),
        "emblem_links": [9],
    },
    {
        "slug": "geryon",
        "label": "Geryon",
        "category": "FIGURE",
        "label_latin": "Geryon",
        "definition_short": "Three-bodied king of Spain whose cattle Hercules stole as his tenth labor; in AF, a figure for the composite nature of the prima materia.",
        "definition_long": (
            "Geryon is a figure from Greek mythology described as a three-bodied (or three-headed) giant king "
            "who ruled the island of Erytheia in the far west. His prized cattle were guarded by the herdsman "
            "Eurytion and the two-headed dog Orthrus. Hercules killed Geryon as his tenth labor to steal the "
            "cattle. In Maier's mytho-alchemical reading, Geryon's three bodies represent the composite nature "
            "of the prima materia — a single substance that manifests as three interrelated principles so "
            "intimately connected that destroying one annihilates all. The myth warns the alchemist against "
            "violent separation: the four elements must be gently distinguished, not forcibly torn apart."
        ),
        "significance_to_af": (
            "Maier invokes Geryon in Emblem XIX ('If you kill one of the four, everybody will be dead immediately'), "
            "using the three-bodied king as an allegory for the inseparability of the philosophical substance's "
            "components. De Jong traces this to the Turba Philosophorum's teaching that the Stone's elements "
            "cannot be isolated without destroying the work. Szulakowska reads the four-warriors motif as a "
            "disguised Christological resurrection allegory."
        ),
        "emblem_links": [19],
    },
    {
        "slug": "naaman",
        "label": "Naaman",
        "category": "FIGURE",
        "label_latin": "Naaman Syrus",
        "definition_short": "The Syrian military commander healed of leprosy by washing seven times in the Jordan River; alchemical figure for purification through repeated washing.",
        "definition_long": (
            "Naaman is the Syrian army commander whose story appears in 2 Kings 5: afflicted with leprosy, he "
            "is told by the prophet Elisha to wash seven times in the Jordan River, after which his flesh is "
            "restored 'like the flesh of a young boy.' In alchemical exegesis, Naaman's leprosy represents "
            "the impurity of the philosophical ore (the 'dropsical' condition of the unrefined prima materia), "
            "and his sevenfold washing represents the repeated cycles of dissolution and purification required "
            "to produce the white stone. De Jong traces this allegory to the Clangor Buccinae, where the dropsical "
            "ore 'wants to be washed seven times in the river.' The sacramental overtone is deliberate: Naaman's "
            "cure prefigures Christian baptism, and Maier exploits this to connect alchemical purification with "
            "spiritual cleansing."
        ),
        "significance_to_af": (
            "Naaman is the central figure of Emblem XIII ('The ore of the philosophers is dropsical and wants to "
            "be washed seven times in the river, just as Naaman the leper washed in the Jordan'). De Jong "
            "identifies this as part of the albedo washing sequence running through Emblems XI-XIII. Szulakowska "
            "reads the baptismal overtone as evidence of Maier's concealed Eucharistic theology."
        ),
        "emblem_links": [13, 43],
    },
    {
        "slug": "apocalyptic-woman",
        "label": "Apocalyptic Woman / Turkish Madonna",
        "category": "FIGURE",
        "label_latin": "Mulier Apocalyptica",
        "definition_short": "The Woman of Revelation 12 — identified by Szulakowska as the Virgin Mary in Maier's alchemical Eucharist, connected to Ottoman war imagery.",
        "definition_long": (
            "The Apocalyptic Woman appears in Revelation 12:1 as 'a woman clothed with the sun, with the moon "
            "under her feet, and on her head a crown of twelve stars.' In Maier's illustration for the Symbola "
            "Aureae Mensae (1617), this figure appears in an alchemical mass scene engraved by Matthaeus Merian. "
            "Szulakowska identifies this image as an early example of the 'Turkish Madonna' — Marian imagery "
            "connected to the Ottoman wars and the defense of Christendom. She argues that Maier's illustration "
            "identifies Christ with the philosopher's stone and the Communion with alchemical transmutation, "
            "constituting 'a far more radical disquisition on the alchemical mass' than the fifteenth-century "
            "text of Nicolaus Melchior Cibinensis that it accompanies. The Woman's role as lac virginis (virgin's "
            "milk) producer connects to the alchemical tradition of the volatile spirit as feminine nourishment."
        ),
        "significance_to_af": (
            "While the Apocalyptic Woman appears in the Symbola Aureae Mensae rather than directly in the Atalanta "
            "Fugiens, Szulakowska argues that the same sacramental theology underlies both works. AF Emblem XL's "
            "two fountains are identified as Maier's most overt reference to the alchemical Eucharist — the elixir "
            "of life described as analogous to 'the water of life of Christ, meaning both Baptism and the Eucharist.' "
            "The nursing motif in AF Emblem V connects to the lac virginis tradition."
        ),
        "emblem_links": [5, 40],
    },
]


def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    added = 0

    for term in TERMS:
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
            for emblem_num in term.get('emblem_links', []):
                emblem_id = c.execute('SELECT id FROM emblems WHERE number = ?', (emblem_num,)).fetchone()
                if emblem_id:
                    c.execute('INSERT OR IGNORE INTO term_emblem_refs (term_id, emblem_id) VALUES (?, ?)',
                              (term_id, emblem_id[0]))
            added += 1
            print(f'  Added: {term["label"]} ({term["category"]})')
        else:
            print(f'  Exists: {term["label"]}')

    conn.commit()
    total = c.execute('SELECT count(*) FROM dictionary_terms').fetchone()[0]
    conn.close()
    print(f'\nDictionary terms: {total} (+{added} new)')


if __name__ == '__main__':
    main()
