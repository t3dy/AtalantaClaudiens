"""Add bibliography entries and scholar_works links for all unlinked scholars."""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'atalanta.db')

# New bibliography entries to add
NEW_BIBS = [
    {
        "source_id": "godwin_1987",
        "author": "Joscelyn Godwin",
        "title": "Atalanta Fugiens: An Edition of the Fugues, Emblems, and Epigrams",
        "year": 1987,
        "publisher": "Magnum Opus Hermetic Sourceworks / Phanes Press",
        "pub_type": "edition",
        "af_relevance": "PRIMARY",
        "annotation": "First modern musical edition with complete transcription of all 50 fugues and first recording. Introductory essay by Hildemarie Streich. Standard English-language reference for the musical dimension.",
    },
    {
        "source_id": "godwin_1999",
        "author": "Joscelyn Godwin",
        "title": "The Deepest of the Rosicrucians: Michael Maier",
        "year": 1999,
        "publisher": "Lindisfarne Press",
        "pub_type": "chapter",
        "af_relevance": "DIRECT",
        "annotation": "Most detailed English-language biographical essay on Maier, drawing on Figala-Neumann archival discoveries. In The Rosicrucian Enlightenment Revisited.",
    },
    {
        "source_id": "bilak_nummedal_2020",
        "author": "Donna Bilak and Tara Nummedal (eds.)",
        "title": "Furnace and Fugue: A Digital Edition of Michael Maier's Atalanta fugiens with Scholarly Commentary",
        "year": 2020,
        "publisher": "University of Virginia Press / Brown University",
        "pub_type": "edition",
        "af_relevance": "PRIMARY",
        "annotation": "Born-digital scholarly edition with interactive text, image, music. Winner of 2022 Rosenzweig Prize. Includes essays by Forshaw, Bilak, Nummedal, Gaudio, Oosterhoff, Ludwig.",
    },
    {
        "source_id": "forshaw_2020",
        "author": "Peter J. Forshaw",
        "title": "Michael Maier and Mythoalchemy",
        "year": 2020,
        "publisher": "In Furnace and Fugue (UVA Press)",
        "pub_type": "chapter",
        "af_relevance": "DIRECT",
        "annotation": "Defines mytho-alchemy as a genre; argues Arcana Arcanissima is the foundational text; identifies quadrivium structure in AF discourses.",
    },
    {
        "source_id": "forshaw_2012",
        "author": "Peter J. Forshaw",
        "title": "The Emblemata of the Atalanta Fugiens (Infinite Fire Webinar)",
        "year": 2012,
        "publisher": "Ritman Library / University of Amsterdam",
        "pub_type": "lecture",
        "af_relevance": "DIRECT",
        "annotation": "Detailed lecture walking through individual emblems, discussing mytho-alchemy, quadrivium structure, and emblem tradition context.",
    },
    {
        "source_id": "hasler_2011",
        "author": "Johann F.W. Hasler",
        "title": "Performative and Multimedia Aspects of Late-Renaissance Meditative Alchemy: The Case of Michael Maier's Atalanta Fugiens (1617)",
        "year": 2011,
        "publisher": "Universitas Humanistica",
        "pub_type": "article",
        "af_relevance": "DIRECT",
        "annotation": "Argues AF is an early form of multimedia requiring performative engagement (singing) for its purpose to be accomplished.",
    },
    {
        "source_id": "long_2012",
        "author": "Kathleen Perry Long",
        "title": "Music and Meditative Practices in Early Modern Alchemy: The Example of the Atalanta fugiens",
        "year": 2012,
        "publisher": "Lo Sguardo",
        "pub_type": "article",
        "af_relevance": "DIRECT",
        "annotation": "Connects AF's musical program to neuroscience, Ficinian music therapy, and Ignatian meditative practice.",
    },
    {
        "source_id": "bilak_2017",
        "author": "Donna Bilak",
        "title": "Playful Humanism in Atalanta fugiens (1618)",
        "year": 2017,
        "publisher": "Italian Academy, Columbia University (work-in-progress)",
        "pub_type": "chapter",
        "af_relevance": "DIRECT",
        "annotation": "Develops steganography/magic square thesis. Explores AF as a work of playful humanism combining epistemology of play with alchemical concealment.",
    },
    {
        "source_id": "rozenrichter_2024",
        "author": "Amber Rozenrichter",
        "title": "The Fruit that Blossoms from the Daughter: The Hidden Dryads in Michael Maier's Atalanta Fugiens",
        "year": 2024,
        "publisher": "SHAC Annual Autumn Meeting, University of Amsterdam",
        "pub_type": "conference",
        "af_relevance": "DIRECT",
        "annotation": "Identifies hidden dryads (tree-nymphs) in AF emblems as concealed feminine guiding forces. Addresses gendered violence in mytho-alchemical allegory.",
    },
    {
        "source_id": "szulakowska_sacrificial",
        "author": "Urszula Szulakowska",
        "title": "The Sacrificial Body and the Day of Doom: Alchemy and Apocalyptic Discourse in the Protestant Reformation",
        "year": 2006,
        "publisher": "Brill",
        "pub_type": "monograph",
        "af_relevance": "CONTEXTUAL",
        "annotation": "Reads AF emblems XIX, XXIV, XXVIII, XXXV, XL, XLIV through lens of Eucharistic theology and Reformation bodily politics. Argues Khunrath-Maier-Fludd triad performed alchemical mass.",
    },
    {
        "source_id": "szulakowska_light",
        "author": "Urszula Szulakowska",
        "title": "The Alchemy of Light: Geometry and Optics in Late Renaissance Alchemical Illustration",
        "year": 2000,
        "publisher": "Brill",
        "pub_type": "monograph",
        "af_relevance": "CONTEXTUAL",
        "annotation": "Chapter 11 on Maier's alchemical geometry of the sun. Analyzes De Circulo Physico Quadrato, Emblem XXI geometric formula, Emblem VIII optical structure, and Pythagorean musical ratios.",
    },
    {
        "source_id": "szulakowska_virgin",
        "author": "Urszula Szulakowska",
        "title": "The Alchemical Virgin Mary in the Religious and Political Context of the Renaissance",
        "year": 2011,
        "publisher": "Cambridge Scholars Publishing",
        "pub_type": "monograph",
        "af_relevance": "CONTEXTUAL",
        "annotation": "Connects Maier's Apocalyptic Woman illustration to Turkish Madonna tradition. Traces AF sources to Rosarium Philosophorum and Marian theology.",
    },
    {
        "source_id": "mclean_website",
        "author": "Adam McLean",
        "title": "The Alchemy Website: Atalanta Fugiens Section",
        "year": 1995,
        "publisher": "alchemywebsite.com",
        "pub_type": "digital",
        "af_relevance": "DIRECT",
        "annotation": "First online resource for AF texts. Hosts English translation from MS Sloane 3645, MIDI files of fugues, and hand-coloured emblem plates (1999).",
    },
    {
        "source_id": "lang_2022",
        "author": "Sarah Lang",
        "title": "Review of Furnace and Fugue (RIDE)",
        "year": 2022,
        "publisher": "RIDE: A Review Journal for Digital Editions and Resources",
        "pub_type": "review",
        "af_relevance": "CONTEXTUAL",
        "annotation": "Most detailed scholarly assessment of the Furnace and Fugue digital edition's methodology, technical infrastructure, and editorial standards.",
    },
]

# Scholar -> works mappings (scholar name -> list of source_ids)
SCHOLAR_WORKS = {
    "Joscelyn Godwin": ["godwin_1987", "godwin_1999"],
    "Donna Bilak": ["bilak_2017", "bilak_nummedal_2020"],
    "Tara Nummedal": ["bilak_nummedal_2020"],
    "Peter J. Forshaw": ["forshaw_2020", "forshaw_2012"],
    "Johann F.W. Hasler": ["hasler_2011"],
    "Kathleen Perry Long": ["long_2012"],
    "Amber Rozenrichter": ["rozenrichter_2024"],
    "Urszula Szulakowska": ["szulakowska_sacrificial", "szulakowska_light", "szulakowska_virgin"],
    "Adam McLean": ["mclean_website"],
    "Sarah Lang": ["lang_2022"],
}


def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Add bibliography entries
    bib_added = 0
    for bib in NEW_BIBS:
        existing = c.execute('SELECT id FROM bibliography WHERE source_id = ?', (bib['source_id'],)).fetchone()
        if not existing:
            c.execute('''INSERT INTO bibliography (source_id, author, title, year, publisher, pub_type, af_relevance, annotation)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                      (bib['source_id'], bib['author'], bib['title'], bib['year'],
                       bib['publisher'], bib['pub_type'], bib['af_relevance'], bib.get('annotation')))
            bib_added += 1
            print(f'  Bib added: {bib["source_id"]}')
        else:
            # Update annotation if missing
            c.execute('UPDATE bibliography SET annotation = ? WHERE source_id = ? AND (annotation IS NULL OR annotation = "")',
                      (bib.get('annotation'), bib['source_id']))

    # Link scholars to works
    links_added = 0
    for scholar_name, source_ids in SCHOLAR_WORKS.items():
        scholar = c.execute('SELECT id FROM scholars WHERE name = ?', (scholar_name,)).fetchone()
        if not scholar:
            print(f'  ** Scholar not found: {scholar_name}')
            continue
        for sid in source_ids:
            bib = c.execute('SELECT id FROM bibliography WHERE source_id = ?', (sid,)).fetchone()
            if not bib:
                print(f'  ** Bib not found: {sid}')
                continue
            existing = c.execute('SELECT scholar_id FROM scholar_works WHERE scholar_id = ? AND bib_id = ?',
                                 (scholar[0], bib[0])).fetchone()
            if not existing:
                c.execute('INSERT INTO scholar_works (scholar_id, bib_id) VALUES (?, ?)',
                          (scholar[0], bib[0]))
                links_added += 1

    conn.commit()
    total_bib = c.execute('SELECT count(*) FROM bibliography').fetchone()[0]
    total_links = c.execute('SELECT count(*) FROM scholar_works').fetchone()[0]
    conn.close()

    print(f'\nBibliography: {total_bib} (+{bib_added})')
    print(f'Scholar-work links: {total_links} (+{links_added})')


if __name__ == '__main__':
    main()
