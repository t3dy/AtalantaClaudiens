"""Add new scholars from pdftoaddaf corpus + dictionary terms from Szulakowska and new sources."""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'atalanta.db')

NEW_SCHOLARS = [
    {
        "name": "Sarah Lang",
        "specialization": "Digital humanities, history of alchemy",
        "af_focus": "RIDE review of Furnace and Fugue; computational approaches to AF",
        "overview": (
            "Sarah Lang is a digital humanities scholar at the University of Graz whose work bridges computational "
            "methods and the history of alchemy. Her RIDE review of the Furnace and Fugue digital edition (2022) "
            "provides the most detailed scholarly assessment of the project's editorial methodology, technical "
            "infrastructure, and contribution to digital publishing standards.\n\n"

            "Lang's review evaluates Furnace and Fugue against established criteria for digital scholarly editions, "
            "praising its innovative MEI music player with piano-roll visualization that allows users without musical "
            "training to experience the fugues' contrapuntal structure. She notes that De Jong's 1969 study 'remains "
            "the only substantive scholarly examination of Maier's text,' positioning the digital edition as a "
            "complement to rather than replacement for source-critical scholarship.\n\n"

            "Lang also delivered a guest lecture introducing alchemy and the Atalanta Fugiens at the University of "
            "Graz (2020), connecting the work to the alchemical traditions preserved at Schloss Eggenberg. Her "
            "computational approach to alchemical texts represents an emerging methodological frontier that may "
            "yield new insights into the structural patterns of Maier's emblem sequences.\n\n"

            "For this site, Lang's RIDE review provides the most authoritative external assessment of how the "
            "Atalanta Fugiens has been translated into digital form, and her criteria for evaluating digital "
            "editions inform the standards this project aspires to."
        ),
    },
    {
        "name": "Kathleen Perry Long",
        "specialization": "Early modern literature, music and medicine",
        "af_focus": "Music as meditative and therapeutic practice in AF",
        "overview": (
            "Kathleen Perry Long is a scholar of early modern literature and intellectual history whose article "
            "'Music and Meditative Practices in Early Modern Alchemy: The Example of the Atalanta fugiens' "
            "(Lo Sguardo, 2012) brings neuroscientific perspectives on music therapy into dialogue with Maier's "
            "multi-sensory alchemical program.\n\n"

            "Long's central argument is that Maier's integration of music into the emblem book was not merely "
            "decorative but therapeutically intentional, drawing on Marsilio Ficino's theory of music as a "
            "vehicle for healing melancholy and related disorders. She connects the AF's meditative program — "
            "'to be looked at, read, meditated, understood, weighed, sung and listened to' — to the systematized "
            "prayer and visualization practices developed by Ignatius of Loyola and other Counter-Reformation "
            "spiritual directors, arguing that alchemical emblem books participate in this broader culture of "
            "disciplined contemplation.\n\n"

            "Long poses the provocative question of whether Maier hoped to solve social and political ills "
            "through musical-meditative practices — a question that situates the AF within the context of the "
            "political upheaval and widespread war of the early seventeenth century. Her neuroscientific framing "
            "suggests that modern research into music's effects on brain function may vindicate early modern "
            "intuitions about music's transformative power.\n\n"

            "For this site, Long's work enriches the discussion of Maier's pedagogical method, connecting the "
            "frontispiece's ludic pedagogy to broader traditions of meditative practice and therapeutic music."
        ),
    },
    {
        "name": "Johann F.W. Hasler",
        "specialization": "Musicology, performance studies",
        "af_focus": "AF as early multimedia and performative work",
        "overview": (
            "Johann F.W. Hasler is a musicologist whose article 'Performative and Multimedia Aspects of "
            "Late-Renaissance Meditative Alchemy: The Case of Michael Maier's Atalanta Fugiens (1617)' "
            "(Universitas Humanistica, 2011) provides the most sustained argument for understanding the AF "
            "as an early form of multimedia requiring performative engagement rather than passive reading.\n\n"

            "Hasler argues that the AF 'requires a performative attitude and activity (in the form of singing) "
            "and not merely to be read, for its original purpose to be fully accomplished.' He demonstrates "
            "that the three-voice canons are not supplementary illustrations but integral components of a "
            "unified meditative exercise combining sight (engravings), intellect (discourses and epigrams), "
            "and embodied practice (singing). This makes the AF, in Hasler's analysis, a genuine precursor "
            "to modern multimedia — a work designed for simultaneous multi-sensory engagement.\n\n"

            "Hasler also describes Godwin as 'without any doubt the leading authority on the historical study "
            "of speculative music,' and his article provides valuable context for understanding the AF's place "
            "within the broader tradition of musica speculativa — the philosophical contemplation of musical "
            "harmony as a mirror of cosmic order.\n\n"

            "For this site, Hasler's performative analysis supports the treatment of the fugues as essential "
            "rather than decorative elements, and his multimedia framing informs the site's own attempt to "
            "present text, image, and musical information together."
        ),
    },
    {
        "name": "Amber Rozenrichter",
        "specialization": "Classical mythology, alchemical iconography",
        "af_focus": "Hidden dryads and gendered violence in AF mythological allegories",
        "overview": (
            "Amber Rozenrichter is a scholar of classical mythology and alchemical iconography whose conference "
            "paper 'The Fruit that Blossoms from the Daughter: The Hidden Dryads in Michael Maier's Atalanta "
            "Fugiens' was presented at the SHAC Annual Autumn Meeting on 'Alchemy, Freemasonry, Hermeticism "
            "and Rosicrucianism' at the Allard Pierson / University of Amsterdam in October 2024.\n\n"

            "Rozenrichter's paper focuses on overlooked aspects of Maier's mythological allegories, particularly "
            "the concealed presence of women who have been transformed into trees — dryads — within the emblem "
            "compositions. She argues that these hidden dryads serve as 'guiding forces for the alchemist,' "
            "representing a feminine dimension of the alchemical work that has been obscured by the predominantly "
            "masculine narrative of pursuit and conquest.\n\n"

            "Rozenrichter also addresses Maier's utilization of classical myths involving rape and incest — "
            "stories that, as Forshaw noted, would be 'absolutely appalling' if read literally. She examines "
            "how Maier transforms these 'distressing occurrences' into alchemical allegories, using the "
            "mythological language of violation and transformation to encode chemical processes of dissolution, "
            "conjunction, and regeneration.\n\n"

            "For this site, Rozenrichter's work opens a dimension of AF scholarship focused on gender, "
            "hidden iconographic elements, and the ethical complexities of mytho-alchemical allegory."
        ),
    },
    {
        "name": "Urszula Szulakowska",
        "specialization": "Art history, alchemical illustration, religious politics",
        "af_focus": "Religious-political context of AF; Eucharistic symbolism; Turkish Madonna",
        "overview": (
            "Urszula Szulakowska is an art historian whose three monographs — The Sacrificial Body and the Day "
            "of Doom (Brill), The Alchemy of Light (Brill), and The Alchemical Virgin Mary (Cambridge Scholars) — "
            "place Maier within the broader context of Protestant Reformation theology, Eucharistic controversy, "
            "and the political dynamics of early modern Central Europe.\n\n"

            "Szulakowska's most distinctive contribution is her argument that Paracelsian alchemists — "
            "specifically Khunrath, Maier, and Fludd — regarded their chemical procedures 'as being essentially "
            "the same rite as the mass,' constituting a 'symbolic usurpation of the highest spiritual and "
            "political authority.' She reads Maier's Atalanta Fugiens within this framework, identifying the "
            "classical mythological surface (Atalanta, Osiris, Oedipus) as concealing a fundamentally Eucharistic "
            "understanding of alchemical transformation.\n\n"

            "Szulakowska discusses six AF emblems in detail: XIX (four warriors as Christological resurrection), "
            "XXIV (wolf/king as sacrificial body theology), XXVIII (steam bath as Eucharistic cleansing), XXXV "
            "(digestion as rehabilitated bodily function), XL (two fountains as Baptism/Eucharist), and XLIV "
            "(Osiris as Christ-figure with incorporeal resurrection). She argues that Maier's emblem plates "
            "'set the style for alchemical illustration for the next three centuries, replacing the earlier "
            "Christological motifs.'\n\n"

            "In The Alchemical Virgin Mary, Szulakowska connects Maier's apocalyptic Woman illustration in the "
            "Symbola Aureae Mensae to the 'Turkish Madonna' tradition and Emperor Rudolf II's Ottoman campaigns. "
            "She demonstrates that Maier's imagery operated simultaneously in religious, political, and "
            "alchemical registers — a finding that extends De Jong's multi-register model into the domains of "
            "theology and geopolitics.\n\n"

            "For this site, Szulakowska provides the religious-political dimension absent from De Jong's "
            "source-critical approach, enriching the scholarly commentary on six specific emblems with readings "
            "that connect laboratory alchemy to Reformation sacramental theology."
        ),
    },
]

# New dictionary terms from Szulakowska, Forshaw, Rozenrichter, and Long
NEW_TERMS = [
    {
        "slug": "lusus-serius",
        "label": "Lusus Serius",
        "category": "CONCEPT",
        "label_latin": "Lusus Serius",
        "definition_short": "The 'serious game' — Maier's term for the playful-yet-profound engagement with alchemical wisdom through emblems, music, and riddles.",
        "definition_long": (
            "Lusus serius ('serious game' or 'serious play') is the phrase Maier used as the title of one of his "
            "1616 publications and as a description of his overall approach to alchemical communication. The concept "
            "reflects a Renaissance pedagogical tradition in which play, riddle-solving, and multi-sensory engagement "
            "are understood not as frivolous diversions but as the most effective means of apprehending complex truths. "
            "De Jong identified the lusus serius as the governing principle of the Atalanta Fugiens, where the reader "
            "must chase meaning through images, verses, discourses, and music simultaneously — just as Hippomenes "
            "must chase Atalanta through the distraction of golden apples. Forshaw and Bilak have both emphasized "
            "that this playful structure is deliberate and sophisticated, not a sign of intellectual confusion."
        ),
        "significance_to_af": "The entire AF is structured as a lusus serius. Maier's subtitle promises content 'to be looked at, read, meditated, understood, weighed, sung, and listened to, not without a certain pleasure.' The frontispiece race of Atalanta and Hippomenes is itself a figure for this serious play — the reader pursues wisdom through the enticements of sensory pleasure.",
        "emblem_links": [0],
    },
    {
        "slug": "dryad",
        "label": "Dryad",
        "category": "FIGURE",
        "label_latin": "Dryas",
        "definition_short": "Tree-nymph of Greek mythology; Rozenrichter identifies hidden dryads in AF emblems as feminine guiding forces for the alchemist.",
        "definition_long": (
            "Dryads are tree-nymphs in Greek mythology — female spirits inhabiting and protecting trees, particularly "
            "oaks. In the Ovidian metamorphosis tradition that Maier draws upon extensively, dryads represent women "
            "transformed into trees, preserving their consciousness within a new botanical form. Amber Rozenrichter's "
            "2024 SHAC conference paper identifies concealed dryads within several Atalanta Fugiens emblem compositions, "
            "arguing that these hidden feminine presences serve as guiding forces for the alchemist — a dimension of "
            "the iconographic program that has been overlooked by scholarship focused on the dominant male narrative "
            "of pursuit and conquest."
        ),
        "significance_to_af": "Rozenrichter argues that hidden dryads in AF emblems represent a feminine dimension of the alchemical work concealed within the compositions. The Tree of Life in Emblem XXVI and the tree motifs in several other emblems may contain these transformed women, connecting Maier's mytho-alchemy to the Ovidian tradition of metamorphosis as a form of preservation.",
        "emblem_links": [26, 35],
    },
    {
        "slug": "lac-virginis",
        "label": "Lac Virginis",
        "category": "SUBSTANCE",
        "label_latin": "Lac Virginis",
        "definition_short": "Virgin's milk — a volatile alchemical spirit considered a form of the quintessence, used in the first stage of creating the philosopher's stone.",
        "definition_long": (
            "Lac virginis ('virgin's milk') is an alchemical term for a volatile spirit or distillate considered to be "
            "a purified form of the quintessence — the fifth element beyond earth, air, fire, and water. In Szulakowska's "
            "analysis, lac virginis connects to the Marian theology underlying much alchemical imagery: the Virgin Mary's "
            "milk, which nourished the Christ-child, becomes an allegory for the purified mercurial fluid that nourishes "
            "the philosophical embryo. The production of this fluid was considered the first stage in creating the stone "
            "or elixir capable of transmuting base metals into silver."
        ),
        "significance_to_af": "Szulakowska identifies lac virginis as the alchemical concept underlying Maier's Apocalyptic Woman illustration in the Symbola Aureae Mensae, where the Virgin's life-giving fluid has transformatory qualities analogous to the Communion wine. The nursing motif in AF Emblem V (woman suckling the toad) may also connect to this tradition of sacred feminine nourishment.",
        "emblem_links": [5],
    },
    {
        "slug": "musica-speculativa",
        "label": "Musica Speculativa",
        "category": "CONCEPT",
        "label_latin": "Musica Speculativa",
        "definition_short": "The philosophical contemplation of musical harmony as a mirror of cosmic order; the tradition within which Maier's fugues operate.",
        "definition_long": (
            "Musica speculativa ('speculative music') is the medieval and Renaissance tradition of understanding music "
            "not primarily as entertainment or aesthetic experience but as a mathematical-philosophical discipline "
            "revealing the harmonic structure of the cosmos. Rooted in Pythagorean and Boethian theory, musica speculativa "
            "distinguishes between musica mundana (the harmony of the spheres), musica humana (the harmony of body and "
            "soul), and musica instrumentalis (audible, performed music). Maier's integration of three-voice fugues into "
            "an alchemical emblem book is an exercise in musica speculativa — the audible canons are designed to attune "
            "the listener's soul to the same cosmic harmonies that govern the alchemical transformation of matter."
        ),
        "significance_to_af": "The AF's fifty fugues operate within the musica speculativa tradition. Hasler argues that the work requires performative engagement (singing) for its original purpose to be accomplished. Wescott's modal analysis demonstrates that the musical structures encode planetary and alchemical correspondences. The subtitle's promise of content 'to be sung and listened to' places the fugues within this contemplative musical tradition.",
        "emblem_links": [0, 1],
    },
    {
        "slug": "emblem-book",
        "label": "Emblem Book",
        "category": "CONCEPT",
        "label_latin": "Liber Emblematum",
        "definition_short": "A genre of illustrated books combining motto, image, and epigram in a tripartite structure; AF is the most complex example with added music.",
        "definition_long": (
            "The emblem book is a literary and artistic genre that emerged in the sixteenth century, initiated by Andrea "
            "Alciato's Emblematum liber (1531). Each emblem combines three elements: an inscriptio (motto or title), a "
            "pictura (image), and a subscriptio (explanatory verse or epigram). The reader is expected to meditate on "
            "the relationship between these elements, which may complement, tension, or complicate each other. Maier's "
            "Atalanta Fugiens extends the standard tripartite structure by adding a fourth element — the three-voice "
            "fugue — and a fifth — the two-page Latin discourse. Forshaw identifies the Rosarium Philosophorum (1550) "
            "as the most likely structural model for AF's combination of motto, image, and text."
        ),
        "significance_to_af": "AF is described by scholars as the most complex emblem book ever produced. Its five-part structure (motto, plate, epigram, fugue, discourse) exceeds the standard tripartite form. Hasler identifies it as an early form of multimedia. Bilak reads it as a work of steganography. The emblem book genre provides the framework within which Maier's innovations must be understood.",
        "emblem_links": [0],
    },
    {
        "slug": "eucharist-alchemical",
        "label": "Alchemical Eucharist",
        "category": "CONCEPT",
        "label_latin": "Eucharistia Alchemica",
        "definition_short": "The identification of alchemical transmutation with the Catholic Communion rite; Szulakowska's key argument about Maier's religious dimension.",
        "definition_long": (
            "The alchemical Eucharist is Szulakowska's term for the identification, by Paracelsian alchemists "
            "including Khunrath, Maier, and Fludd, of their chemical procedures with the Catholic rite of Communion. "
            "This was, in Szulakowska's analysis, 'a symbolic usurpation of the highest spiritual and political "
            "authority since the right to offer Communion was jealously guarded.' The alchemical process of "
            "transmutation — dissolving, purifying, and reconstituting matter — was understood not merely as "
            "analogous to but essentially identical with the Eucharistic transformation of bread and wine into "
            "the body and blood of Christ. The philosopher's stone, in this reading, is the alchemical equivalent "
            "of the consecrated Host."
        ),
        "significance_to_af": "Szulakowska identifies AF Emblem XL (two fountains/elixir of life) as containing one of the 'slightly more overt references to the alchemical sacrament,' where Maier states the elixir's meaning is analogous to 'the water of life of Christ, meaning by this both the sacrament of Baptism and also that of the Eucharist.' The entire AF, in her reading, conceals Eucharistic theology beneath its classical mythological surface.",
        "emblem_links": [40],
    },
]


def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Add scholars
    for scholar in NEW_SCHOLARS:
        existing = c.execute('SELECT id FROM scholars WHERE name = ?', (scholar['name'],)).fetchone()
        if not existing:
            c.execute('''INSERT INTO scholars (name, specialization, af_focus, overview, review_status)
                         VALUES (?, ?, ?, ?, ?)''',
                      (scholar['name'], scholar['specialization'], scholar['af_focus'],
                       scholar['overview'], 'DRAFT'))
            print(f'  Added scholar: {scholar["name"]}')
        else:
            c.execute('UPDATE scholars SET overview = ?, specialization = ?, af_focus = ? WHERE name = ?',
                      (scholar['overview'], scholar['specialization'], scholar['af_focus'], scholar['name']))
            print(f'  Updated scholar: {scholar["name"]}')

    # Add dictionary terms
    added_terms = 0
    for term in NEW_TERMS:
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
            added_terms += 1
            print(f'  Added term: {term["label"]} ({term["category"]})')
        else:
            print(f'  Exists: {term["label"]}')

    conn.commit()
    scholars = c.execute('SELECT count(*) FROM scholars').fetchone()[0]
    terms = c.execute('SELECT count(*) FROM dictionary_terms').fetchone()[0]
    conn.close()
    print(f'\nScholars: {scholars}, Dictionary terms: {terms} (+{added_terms} new)')
    print('\nSuggested additional dictionary topics for future sessions:')
    print('  - Quadrivium (arithmetic, music, geometry, astronomy — Forshaw)')
    print('  - Prisca Sapientia / Perennial Philosophy (Tilton)')
    print('  - Steganography / Magic Square (Bilak)')
    print('  - Potable Gold / Aurum Potabile (Maier, Ficino)')
    print('  - Rosarium Philosophorum as source text (already exists)')
    print('  - Medea (rejuvenation myth, Emblem IX)')
    print('  - Geryon (three-bodied king, Emblem XIX)')
    print('  - Naaman (biblical washing, Emblem XIII)')
    print('  - Golden Fleece (Jason quest, already linked)')
    print('  - Apocalyptic Woman / Turkish Madonna (Szulakowska)')


if __name__ == '__main__':
    main()
