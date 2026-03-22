"""Add Playful Reading essay + de Rola bibliography entry."""
import json
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'atalanta.db')
STAGING = os.path.join(os.path.dirname(__file__), '..', 'staging')

ESSAY_BODY = (
    '<p>Michael Maier\'s subtitle for the <em>Atalanta Fugiens</em> promises content "adapted partly '
    'for the eyes and intellect, in figures engraved on copper with mottos, epigrams, and notes '
    'attached, partly for the ears and for the soul\'s recreation, with some 50 musical fugues in '
    'three voices... to be looked at, read, meditated on, understood, weighed, sung and listened to, '
    'not without a certain pleasure." This extraordinary sentence establishes the work as something '
    'more than either a book to be read or music to be heard. It is, in Peter Forshaw\'s phrase, a '
    '<em>lusus serius</em>: a serious game.</p>'

    '<h3>The Lusus Serius Tradition</h3>'
    '<p>The concept of the "serious game" was not Maier\'s invention. He borrowed the phrase for the '
    'title of one of his 1616 publications, <em>Lusus Serius</em>, dedicated to the English alchemist '
    'Francis Anthony. The tradition of encoding serious philosophical content in playful, riddling, or '
    'game-like forms has deep roots in the emblem tradition inaugurated by Andrea Alciato (1531) and '
    'in the broader Renaissance culture of <em>imprese</em>, devices, and hieroglyphic puzzles. But '
    'Maier took the concept further than any predecessor by integrating three sensory modalities &mdash; '
    'sight (the engraved plates), hearing (the three-voice fugues), and intellect (the Latin discourses '
    'and epigrams) &mdash; into a single unified game. The reader is not merely reading but playing: '
    'chasing meaning through the golden apples of image, verse, and music, just as Hippomenes chases '
    'Atalanta.</p>'

    '<h3>The Frontispiece as Instruction Manual</h3>'
    '<p>De Jong identified the frontispiece as the interpretive key to the entire work. The myth of '
    'Atalanta and Hippomenes &mdash; the swift huntress who can only be caught when distracted by golden '
    'apples thrown by her suitor &mdash; functions as Maier\'s pedagogical program. The reader is '
    'Hippomenes, pursuing the fugitive wisdom (Atalanta/Mercury); the fifty emblems are the golden '
    'apples, each one a sensory enticement designed to slow the reader\'s intellectual sprint and '
    'redirect attention toward a deeper meditation. The "certain pleasure" promised in the subtitle is '
    'not incidental entertainment but the mechanism of learning itself: play is the method by which '
    'alchemical secrets are absorbed.</p>'

    '<h3>Bilak: Playful Humanism and Steganography</h3>'
    '<p>Donna Bilak\'s work-in-progress paper "Playful Humanism in Atalanta fugiens" (Columbia Italian '
    'Academy, 2017) develops the most sustained argument for reading the AF as an exercise in ludic '
    'epistemology. Bilak argues that Maier\'s combination of motto, plate, epigram, fugue, and discourse '
    'creates a work that can be read sequentially or reshuffled according to a hidden mathematical '
    'structure &mdash; a magic square that conceals a second reading order within the apparent sequence. '
    'Her steganographic thesis proposes that the AF is literally a game with rules: the reader who '
    'discovers the mathematical key unlocks a level of meaning invisible to the sequential reader. This '
    'is play in the Renaissance sense &mdash; not frivolous diversion but the highest form of '
    'intellectual engagement, comparable to the <em>Gesprachspiele</em> (conversation games) that '
    'Hasler connects to the AF\'s performance context.</p>'

    '<h3>Hasler: Performance as Meditation</h3>'
    '<p>Johann F.W. Hasler argues that the AF "requires a performative attitude and activity (in the '
    'form of singing) and not merely to be read, for its original purpose to be fully accomplished." '
    'The act of singing the three-voice fugues while contemplating the emblem plate and meditating on '
    'the discourse transforms the reader from a passive recipient into an active participant &mdash; a '
    'player in Maier\'s alchemical game. Hasler connects this to the tradition of meditative emblem '
    'books influenced by Ignatian spiritual exercises, where visualization, intellectual reflection, '
    'and affective response are systematically combined. The AF\'s multi-sensory design is not '
    'decorative but functional: it engages the whole person &mdash; body (singing), eyes (looking), '
    'and mind (reading) &mdash; in simultaneous action.</p>'

    '<h3>The Rosicrucian Ludibrium</h3>'
    '<p>The Rosicrucian context adds another dimension to the AF\'s playfulness. The Rosicrucian '
    'manifestos &mdash; the <em>Fama Fraternitatis</em> (1614), the <em>Confessio</em> (1615), and '
    'Johann Valentin Andreae\'s <em>Chemical Wedding of Christian Rosenkreutz</em> (1616) &mdash; were '
    'later described by Andreae himself as a <em>ludibrium</em>: a prank, a jest, a playful fiction '
    'designed to provoke thought rather than convey literal truth. Yet Maier took this "prank" with '
    'deadly seriousness, devoting two books (<em>Silentium post Clamores</em> and <em>Themis Aurea</em>) '
    'to defending the Brotherhood\'s principles. As Godwin observes, if Maier knew the manifestos were '
    'a ludibrium, then his lifelong defense of Rosicrucianism must have been undertaken to "turn the '
    'prank to deadly earnest, because he so passionately agreed with the sentiments expressed therein." '
    'The AF participates in this ludibrium tradition: it is simultaneously a jest (a footrace over '
    'golden apples) and the most serious work of chemical philosophy Maier produced. Tobias Churton\'s '
    '<em>The Golden Builders</em> explores this Rosicrucian humor as a mystical teaching tool &mdash; '
    'the jest that conceals the deepest wisdom.</p>'

    '<h3>The Golden Game</h3>'
    '<p>Stanislas Klossowski de Rola\'s <em>The Golden Game: Alchemical Engravings of the Seventeenth '
    'Century</em> (Thames and Hudson, 1988) reproduces the AF emblems alongside other alchemical '
    'engravings of the period, and its title explicitly invokes the ludic tradition that runs through '
    'alchemical culture. The "golden game" (<em>ludus aureus</em>) is an old alchemical conceit: the '
    'pursuit of gold is itself a game, governed by rules that the adept must discover through study, '
    'practice, and &mdash; crucially &mdash; play. The term connects to the broader Renaissance culture '
    'of <em>ludi</em> (games, spectacles, performances) and to the specific tradition of alchemical '
    'riddle-texts where the reader must solve puzzles to advance. For de Rola, the entire corpus of '
    'alchemical illustration constitutes a golden game &mdash; a visual puzzle tradition in which every '
    'image simultaneously reveals and conceals, educates and entertains. The AF is the masterpiece of '
    'this tradition: fifty puzzles, each with its own musical accompaniment, each inviting the viewer '
    'to play the game of interpretation.</p>'

    '<h3>Tilton and Szulakowska: Spiritual Dimensions of Play</h3>'
    '<p>The playful dimension of the AF has spiritual implications that scholars read differently. '
    'Hereward Tilton argues that Maier perceived his own alchemical quest as mirroring the Great Work '
    '&mdash; not as Jungian projection but as a conscious understanding that material transformation '
    'and spiritual development are structurally identical. In this reading, the AF\'s ludic pedagogy is '
    'a form of spiritual exercise: by playing the game of the emblems, the reader undergoes a '
    'transformation parallel to the chemical process depicted. Szulakowska proposes that the Pythagorean '
    'musical ratios encoded in the fugues were intended to create correspondences with celestial forces. '
    'While this interpretation goes beyond what most scholars in the new historiography would endorse, '
    'it raises a genuine question about what Maier thought was happening when someone sang, looked, and '
    'meditated simultaneously. Was it merely learning? Or was the multi-sensory engagement itself a '
    'transformative operation &mdash; a kind of alchemical work performed on the reader rather than '
    'on matter in a flask?</p>'

    '<h3>Long: Music as Therapy</h3>'
    '<p>Kathleen Perry Long\'s neuroscientific framing offers a more grounded way to understand the '
    'AF\'s therapeutic ambitions. Drawing on Ficino\'s theory of music as a vehicle for healing '
    'melancholy and on contemporary research into music\'s effects on brain function, Long proposes '
    'that Maier may have intended the AF as a genuine therapeutic intervention &mdash; a work designed '
    'to address the melancholy and political despair of early seventeenth-century Europe through the '
    'combined action of visual meditation, musical engagement, and intellectual exercise. This is play '
    'as medicine: the "certain pleasure" of the subtitle is not merely aesthetic but therapeutic.</p>'

    '<h3>The Reader as Alchemist</h3>'
    '<p>Ultimately, what makes the AF\'s playfulness distinctive is that it collapses the distinction '
    'between reading about alchemy and doing alchemy. The reader who sings the fugue, contemplates the '
    'plate, puzzles over the motto, reads the discourse, and connects the emblem to its sources in the '
    'Turba and the Rosarium is not merely studying a chemical process &mdash; she is performing a '
    'version of it. The multi-sensory engagement that Maier prescribes ("to be looked at, read, '
    'meditated on, understood, weighed, sung and listened to") is itself an operation on the reader\'s '
    'understanding, transforming base ignorance into philosophical gold. The game is the work. The play '
    'is the opus. And the golden apples that Hippomenes throws &mdash; the fifty emblems &mdash; are '
    'both the distraction and the prize.</p>'
)


def main():
    # Add de Rola to bibliography
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    existing = c.execute('SELECT source_id FROM bibliography WHERE source_id = ?', ('de_rola_1988',)).fetchone()
    if not existing:
        c.execute('''INSERT INTO bibliography (source_id, author, title, year, publisher, pub_type, af_relevance, annotation)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                  ('de_rola_1988', 'Stanislas Klossowski de Rola',
                   'The Golden Game: Alchemical Engravings of the Seventeenth Century',
                   1988, 'London: Thames and Hudson', 'monograph', 'CONTEXTUAL',
                   'Lavishly illustrated survey reproducing AF emblems and other Maier works. '
                   'The title invokes the lusus serius tradition of alchemical play.'))
        print('Added de Rola to bibliography')

    # Also add Churton
    existing = c.execute('SELECT source_id FROM bibliography WHERE source_id = ?', ('churton_2005',)).fetchone()
    if not existing:
        c.execute('''INSERT INTO bibliography (source_id, author, title, year, publisher, pub_type, af_relevance, annotation)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                  ('churton_2005', 'Tobias Churton',
                   'The Golden Builders: Alchemists, Rosicrucians, and the First Freemasons',
                   2005, 'New York: Red Wheel/Weiser', 'monograph', 'CONTEXTUAL',
                   'Explores Rosicrucian humor as a mystical teaching tool and the ludibrium tradition.'))
        print('Added Churton to bibliography')

    conn.commit()
    total = c.execute('SELECT count(*) FROM bibliography').fetchone()[0]
    conn.close()
    print(f'Bibliography: {total} entries')

    # Add essay to enriched collection
    enriched_path = os.path.join(STAGING, 'enriched_essays.json')
    with open(enriched_path, encoding='utf-8') as f:
        enriched = json.load(f)

    enriched['playful-reading'] = ESSAY_BODY
    with open(enriched_path, 'w', encoding='utf-8') as f:
        json.dump(enriched, f, ensure_ascii=False)
    print(f'Enriched essays: {len(enriched)} (added playful-reading)')


if __name__ == '__main__':
    main()
