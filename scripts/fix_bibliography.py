"""Fix bibliography: add missing entries, fix academic formatting."""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'atalanta.db')

# Missing entries to add
NEW_ENTRIES = [
    # Hofmeier edition that Smith reviewed
    ("hofmeier_2008", "Thomas Hofmeier (ed.)", "Michael Maiers Chymisches Cabinet: Atalanta fugiens deutsch, nach der Ausgabe von 1708", 2008,
     "Berlin and Basel: Thurn", "edition", "DIRECT",
     "German edition based on the 1708 translation, with extensive indices. Reviewed by Smith (2009)."),

    # De Jong's Netherlands Yearbook article
    ("de_jong_1965", "H.M.E. de Jong", "Michael Maier's Atalanta Fugiens", 1965,
     "Nederlands Kunsthistorisch Jaarboek 15", "article", "PRIMARY",
     "Early article version of De Jong's source-critical analysis, preceding the 1969 monograph."),

    # Streich's introductory essay in Godwin edition
    ("streich_1987", "Hildemarie Streich", "Introductory Essay on the Music of Atalanta Fugiens", 1987,
     "In Godwin (ed.), Atalanta Fugiens (Magnum Opus)", "chapter", "DIRECT",
     "First detailed analysis of the fugues' musical structure. Identifies three-voice parts as Atalanta, Hippomenes, and the golden apple."),

    # Ludwig's Farmer discovery (in Furnace and Fugue)
    ("ludwig_2020", "Maximilian Ludwig", "John Farmer and the Canons of Atalanta fugiens", 2020,
     "In Bilak and Nummedal (eds.), Furnace and Fugue (UVA Press)", "chapter", "DIRECT",
     "Discovery that 40 of the 50 fugues derive from compositions by John Farmer published in Divers and Sundry Waies (1591)."),

    # Nummedal's monograph (context for her AF work)
    ("nummedal_2007", "Tara Nummedal", "Alchemy and Authority in the Holy Roman Empire", 2007,
     "Chicago: University of Chicago Press", "monograph", "CONTEXTUAL",
     "Legal and economic history of alchemical practice in the same patronage networks Maier navigated."),

    # Abraham's dictionary
    ("abraham_1998", "Lyndy Abraham", "A Dictionary of Alchemical Imagery", 1998,
     "Cambridge: Cambridge University Press", "monograph", "CONTEXTUAL",
     "Comprehensive dictionary of alchemical symbols and imagery, citing AF emblems extensively (47 Maier-relevant pages)."),

    # Godwin's Hermetic Journal articles
    ("godwin_1985a", "Joscelyn Godwin", "A Background for Michael Maier's Atalanta Fugiens (1617)", 1985,
     "Hermetic Journal 29: 5-10", "article", "DIRECT",
     "Intellectual context for the musical emblem book, preceding the 1987 edition."),

    ("godwin_1985b", "Joscelyn Godwin", "Musical Alchemy: The Work of Composer and Listener", 1985,
     "Temenos 6: 57-75", "article", "DIRECT",
     "Theoretical foundations of Maier's musical-alchemical synthesis."),

    # Forshaw's published article on alchemical music
    ("forshaw_nd", "Peter J. Forshaw", "Laboratorium, Auditorium, Oratorium", None,
     None, "article", "DIRECT",
     "Discusses alchemical music including Maier's fugues and Khunrath's songs."),

    # Figala and Neumann's bio-bibliographical discoveries
    ("figala_neumann_1990", "Karin Figala and Ulrich Neumann", "Michael Maier (1569-1622): New Bio-Bibliographical Material", 1990,
     "In von Martels (ed.), Alchemy Revisited (Leiden: Brill), pp. 34-50", "chapter", "DIRECT",
     "Archival discoveries establishing Maier's birth in Kiel (1569), father's profession, and biographical chronology."),

    # Smith's Body of the Artisan
    ("smith_2004", "Pamela H. Smith", "The Body of the Artisan: Art and Experience in the Scientific Revolution", 2004,
     "Chicago: University of Chicago Press", "monograph", "CONTEXTUAL",
     "Framework of artisanal knowledge applied to understanding alchemical emblem books as craft practice."),

    # Principe's Secrets of Alchemy
    ("principe_2013", "Lawrence M. Principe", "The Secrets of Alchemy", 2013,
     "Chicago: University of Chicago Press", "monograph", "CONTEXTUAL",
     "Chemical interpretation of alchemical allegories. Identifies antimony as the wolf in Basil Valentine/AF Emblem XXIV."),

    # Jung
    ("jung_1944", "C.G. Jung", "Psychology and Alchemy (Collected Works, vol. 12)", 1944,
     "Princeton: Princeton University Press", "monograph", "CONTEXTUAL",
     "Psychological interpretation of AF plates as expressions of the individuation process. 44 Maier-relevant pages."),

    # Yates
    ("yates_1972", "Frances A. Yates", "The Rosicrucian Enlightenment", 1972,
     "London: Routledge and Kegan Paul", "monograph", "CONTEXTUAL",
     "Foundational study placing Maier within the Rosicrucian movement. Called Maier 'the deepest of the Rosicrucians.'"),

    # Maier's other key works referenced throughout
    ("maier_1614", "Michael Maier", "Arcana Arcanissima", 1614,
     "London [?]", "primary_source", "DIRECT",
     "Mytho-alchemical interpretation of Egyptian and Greek mythology. Forshaw identifies this as the foundational text of mytho-alchemy."),

    ("maier_1616", "Michael Maier", "De Circulo Physico, Quadrato", 1616,
     "Oppenheim: Lucas Jennis", "primary_source", "DIRECT",
     "Treatise on the role of the sun in making potable gold. Squaring the circle as alchemical geometry."),

    ("maier_1617b", "Michael Maier", "Symbola Aureae Mensae Duodecim Nationum", 1617,
     "Frankfurt: Lucas Jennis", "primary_source", "DIRECT",
     "Compendium of twelve alchemical traditions. Contains the alchemical mass illustration analyzed by Szulakowska."),

    ("maier_1618", "Michael Maier", "Themis Aurea: The Laws of the Fraternity of the Rosie Cross", 1618,
     "Frankfurt: Lucas Jennis", "primary_source", "CONTEXTUAL",
     "Defense of the Rosicrucian Brotherhood. Translated into English in 1656."),
]

# Academic formatting fixes for existing entries
FORMAT_FIXES = {
    "craven_1910": ("J.B. Craven", "Count Michael Maier: Doctor of Philosophy and of Medicine, Alchemist, Rosicrucian, Mystic, 1568-1622", "Kirkwall: William Peace and Son. Facsimile ed., London: Dawson's of Pall Mall, 1968"),
    "de_jong_1969": ("H.M.E. de Jong", "Michael Maier's Atalanta Fugiens: Sources of an Alchemical Book of Emblems", "Leiden: E.J. Brill"),
    "tilton_2003": ("Hereward Tilton", "The Quest for the Phoenix: Spiritual Alchemy and Rosicrucianism in the Work of Count Michael Maier (1569-1622)", "Berlin: Walter de Gruyter (Arbeiten zur Kirchengeschichte, 88)"),
    "pagel_1973": ("Walter Pagel", "Review of H.M.E. de Jong, Michael Maier's Atalanta Fugiens", "Medical History 17(1): 101-102"),
    "leedy_1991": ("Douglas Leedy", "Review of Joscelyn Godwin (ed.), Atalanta Fugiens: An Edition of the Fugues, Emblems, and Epigrams", "Notes: Quarterly Journal of the Music Library Association 47(3): 941-943"),
    "smith_2009": ("Pamela H. Smith", "Review of Thomas Hofmeier (ed.), Michael Maiers Chymisches Cabinet", "Medical History 53(1): 141-142"),
    "miner_2012": ("Paul Miner", "Blake and Atalanta Fugiens: Two Plates, Three Conjectures", "Notes and Queries 59(3): 358-362"),
    "maier_1617": ("Michael Maier", "Atalanta Fugiens, hoc est Emblemata Nova de Secretis Naturae Chymica", "Oppenheim: Johann Theodor de Bry"),
    "de_jong_1964": ("H.M.E. de Jong", "Michael Maier's Atalanta Fugiens", "Netherlands Yearbook for History of Art 15: 1-15"),
    "hasler_2011": ("Johann F.W. Hasler", "Performative and Multimedia Aspects of Late-Renaissance Meditative Alchemy: The Case of Michael Maier's Atalanta Fugiens (1617)", "Universitas Humanistica 72: 135-145"),
    "long_2012": ("Kathleen Perry Long", "Music and Meditative Practices in Early Modern Alchemy: The Example of the Atalanta fugiens", "Lo Sguardo 10(3): 125-135"),
}


def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Add new entries
    added = 0
    for entry in NEW_ENTRIES:
        sid = entry[0]
        existing = c.execute('SELECT source_id FROM bibliography WHERE source_id = ?', (sid,)).fetchone()
        if not existing:
            c.execute('''INSERT INTO bibliography (source_id, author, title, year, publisher, pub_type, af_relevance, annotation)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', entry)
            added += 1
            print(f'  Added: {sid}')

    # Fix formatting on existing entries
    fixed = 0
    for sid, (author, title, publisher) in FORMAT_FIXES.items():
        c.execute('UPDATE bibliography SET author = ?, title = ?, publisher = ? WHERE source_id = ?',
                  (author, title, publisher, sid))
        fixed += 1

    conn.commit()
    total = c.execute('SELECT count(*) FROM bibliography').fetchone()[0]
    conn.close()
    print(f'\nBibliography: {total} entries (+{added} new, {fixed} formatted)')


if __name__ == '__main__':
    main()
