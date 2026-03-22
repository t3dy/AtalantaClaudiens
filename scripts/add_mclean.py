"""Add Adam McLean as scholar + timeline events for his AF contributions."""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'atalanta.db')

MCLEAN_PROFILE = (
    "Adam McLean (born 7 March 1948, Glasgow) is a Scottish writer, editor, and publisher who has done more "
    "than any other individual to make alchemical texts and imagery accessible to a modern English-speaking "
    "audience. John Granger named him as one of the three figureheads of modern alchemical influence alongside "
    "Carl Jung and Titus Burckhardt. McLean accessed the wealth of alchemical manuscripts in the Ferguson "
    "Collection at Glasgow University Library, the Young Collection, and the John Read Collection at the "
    "University of St Andrews, building from these resources a publishing and editorial project that has "
    "shaped the field for over four decades.\n\n"

    "McLean's editorial career began in 1978 with the founding of the Hermetic Journal, which he published "
    "until 1992, and the Magnum Opus Hermetic Sourceworks series, which has produced 55 editions of key "
    "source texts of the Hermetic tradition through 2018. The series includes landmark editions of the "
    "Rosary of the Philosophers, the Splendor Solis, the Mutus Liber, and — most significant for Atalanta "
    "Fugiens scholarship — Joscelyn Godwin's 1987 edition of the Atalanta Fugiens with the first complete "
    "recording of the fifty fugues. McLean's role as publisher of Godwin's edition made him instrumental in "
    "bringing Maier's work to a new generation of readers and performers.\n\n"

    "In 1995 McLean founded The Alchemy Website (originally at levity.com/alchemy, now alchemywebsite.com), "
    "which became the most comprehensive online resource for alchemical texts, images, and encyclopedic "
    "information. The site's Atalanta Fugiens section hosts the English translation from British Library "
    "MS Sloane 3645, transcribed collaboratively by Clay Holden (emblems 1-10), Hereward Tilton (11-34), "
    "and Peter Branwin (35-50). In 1999, McLean hand-coloured all fifty emblem plates, creating a vivid "
    "chromatic interpretation that highlights allegorical details invisible in the monochrome originals — "
    "the alchemical colors of nigredo (black), albedo (white), citrinitas (yellow), and rubedo (red) become "
    "literally visible in his painted versions.\n\n"

    "McLean's approach to alchemy is distinctive in combining scholarly editing with artistic practice. He "
    "treats alchemical images not merely as illustrations of textual ideas but as autonomous symbolic "
    "compositions that reward visual meditation — an approach that aligns with Maier's own multi-sensory "
    "pedagogy. His colouring of the AF plates is itself a form of interpretive scholarship, requiring "
    "decisions about which elements should be red (sulphurous), which white (mercurial), and which gold "
    "(perfected) — decisions grounded in alchemical theory.\n\n"

    "For this site, McLean's contributions are threefold. His Magnum Opus series published the Godwin "
    "edition that remains the standard English-language reference. His Alchemy Website made the AF texts "
    "freely available online for the first time, democratizing access to a work previously confined to "
    "rare book rooms. And his hand-coloured plates offer a visual interpretation that complements the "
    "black-and-white scholarship of De Jong and Tilton with chromatic insight into the alchemical "
    "color symbolism encoded in Merian's engravings."
)

TIMELINE_EVENTS = [
    {
        "year": 1987,
        "event_type": "PUBLICATION",
        "title": "Godwin edition of Atalanta Fugiens (Magnum Opus)",
        "description": "First modern scholarly edition with musical transcriptions",
        "description_long": (
            "Joscelyn Godwin's edition of the Atalanta Fugiens, published by Adam McLean's Magnum Opus "
            "Hermetic Sourceworks, included the first complete recording of the fifty three-voice fugues "
            "performed by Rachel Platt, Emily Van Evera, Rufus Muller, and Richard Wistreich. The edition "
            "with its introductory essay by Hildemarie Streich made the musical dimension of the work "
            "accessible for the first time, transforming scholarly understanding of Maier's multi-sensory project."
        ),
    },
    {
        "year": 1995,
        "event_type": "DIGITAL",
        "title": "Adam McLean founds The Alchemy Website",
        "description": "First major online resource for alchemical texts and imagery",
        "description_long": (
            "Adam McLean launched The Alchemy Website (originally levity.com/alchemy, now alchemywebsite.com), "
            "which became the most comprehensive online repository of alchemical texts, images, and encyclopedic "
            "information. The site hosted the Atalanta Fugiens English translation from British Library MS Sloane "
            "3645, transcribed collaboratively by Clay Holden, Hereward Tilton, and Peter Branwin, making the "
            "work freely accessible to a global audience for the first time."
        ),
    },
    {
        "year": 1999,
        "event_type": "SCHOLARSHIP",
        "title": "McLean hand-colours all 50 Atalanta Fugiens emblems",
        "description": "Chromatic interpretation reveals alchemical color symbolism",
        "description_long": (
            "Adam McLean produced hand-coloured versions of all fifty Atalanta Fugiens emblem plates, "
            "applying pigments based on alchemical color theory to Merian's monochrome engravings. The "
            "colouring makes visible the nigredo (black), albedo (white), citrinitas (yellow), and rubedo "
            "(red) stages encoded in the compositions, offering a form of visual-interpretive scholarship "
            "that complements textual analysis."
        ),
    },
    {
        "year": 2020,
        "event_type": "DIGITAL",
        "title": "Furnace and Fugue digital edition (UVA Press)",
        "description": "Born-digital scholarly edition by Bilak and Nummedal",
        "description_long": (
            "Donna Bilak and Tara Nummedal published Furnace and Fugue: A Digital Edition of Michael Maier's "
            "Atalanta fugiens with Scholarly Commentary through the University of Virginia Press and Brown "
            "University's Digital Publications Initiative. The interactive edition features fully searchable text "
            "in Latin, German, and English, high-resolution zoomable images, newly commissioned vocal recordings, "
            "and essays by Forshaw, Bilak, and other scholars. It won the 2022 Roy Rosenzweig Prize for "
            "Creativity in Digital History from the American Historical Association."
        ),
    },
]


def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Add McLean as scholar
    existing = c.execute('SELECT id FROM scholars WHERE name = ?', ('Adam McLean',)).fetchone()
    if not existing:
        c.execute('''INSERT INTO scholars (name, birth_year, specialization, af_focus, overview, review_status)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  ('Adam McLean', 1948,
                   'Alchemical texts and symbolism, editing, publishing',
                   'Published Godwin AF edition; Alchemy Website with AF texts and hand-coloured plates',
                   MCLEAN_PROFILE, 'DRAFT'))
        print('Added scholar: Adam McLean')
    else:
        c.execute('UPDATE scholars SET overview = ? WHERE name = ?', (MCLEAN_PROFILE, 'Adam McLean'))
        print('Updated scholar: Adam McLean')

    # Add timeline events (check for duplicates by year + title)
    added = 0
    for event in TIMELINE_EVENTS:
        existing = c.execute('SELECT id FROM timeline_events WHERE year = ? AND title = ?',
                             (event['year'], event['title'])).fetchone()
        if not existing:
            c.execute('''INSERT INTO timeline_events (year, event_type, title, description, description_long, confidence)
                         VALUES (?, ?, ?, ?, ?, ?)''',
                      (event['year'], event['event_type'], event['title'],
                       event['description'], event['description_long'], 'HIGH'))
            added += 1
            print(f'  Added timeline: {event["year"]} — {event["title"]}')
        else:
            print(f'  Skipped (exists): {event["year"]} — {event["title"]}')

    conn.commit()
    scholars = c.execute('SELECT count(*) FROM scholars').fetchone()[0]
    events = c.execute('SELECT count(*) FROM timeline_events').fetchone()[0]
    conn.close()
    print(f'\nScholars: {scholars}, Timeline events: {events} (+{added} new)')


if __name__ == '__main__':
    main()
