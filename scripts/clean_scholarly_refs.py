"""Replace garbled OCR scholarly_refs with clean academic summaries.

These refs were extracted raw from De Jong's OCR'd text and contain
unreadable Latin/Greek OCR artifacts, run-together words, and citation soup.
Replace with clean 2-3 sentence scholarly summaries.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'atalanta.db')

# Map ref_id -> clean summary
CLEAN_SUMMARIES = {
    33: "De Jong traces the motto to the pronouncement of Balgus in the Turba Philosophorum, where the old man must be fixed to the tree in celestial dew to be rejuvenated. She identifies this as an allegory for the volatile spirit descending upon and renewing the fixed philosophical body, drawing on the Pseudo-Lullian tradition of argent vive as prima materia.",

    34: "De Jong identifies the motto source in the Aurora Consurgens and connects Maier's image of Christ drawing all men to himself through death and resurrection to the alchemical process of dissolution and reconstitution. She demonstrates that Maier weaves Christian sacrificial imagery into the same allegorical framework as the classical myths.",

    36: "De Jong traces the sources for this emblem to Hesiod's Theogony and to the Turba Philosophorum, identifying the underlying chemistry as the addition of fire to fire and mercury to mercury — the principle of philosophical homogeneity. She connects the allegory of Saturn devouring his children to the dissolution of metals back into their mercurial prima materia.",

    32: "De Jong identifies the motto source in the Clangor Buccinae and traces the Latona allegory to the metallurgical process of whitening a dark alloy. She demonstrates that 'Latona' derives from 'laton' (electrum or yellow silver), connecting the mythological goddess to the albedo stage of transmutation from black lead through transitional stages to white silver and ultimately red gold.",

    35: "De Jong traces the source of the dropsical ore metaphor to the Clangor Buccinae and identifies the underlying process as the repeated washing and purification of impure philosophical mercury. She connects the Naaman baptism story to the albedo purification sequence running through Emblems XI-XIII.",

    39: "De Jong identifies the motto source in the Clangor Buccinae and traces the discourse's discussion of Mercury's distillation processes to the same text. She demonstrates how Maier connects the potter's craft of working with wet and dry materials to the alchemical manipulation of mercurial and sulphurous components through successive stages.",

    62: "De Jong traces this emblem's sources to the Opus Mulierum and the Pseudo-Lullian Codicillus, identifying the 'woman's work' of cooking as an allegory for the sustained, gentle heating required after the albedo stage to mature the white substance toward the rubedo.",

    40: "De Jong traces the source imagery to Senior's Tabula Chimica and Lambsprinck's De Lapide Philosophico, identifying the two lions as complementary representations of the volatile and fixed principles. She demonstrates how Maier draws on medieval and Renaissance alchemical bestiary traditions to develop the lion as a solar symbol of the citrinitas stage.",

    41: "De Jong identifies the source in George Ripley's Liber Duodecim Portarum and demonstrates how Maier connects the killing of one of four interconnected elements to the Hermetic principle that the Stone's components are inseparable. She traces the Geryon myth to Maier's argument that violent separation destroys the work.",

    43: "De Jong traces the motto source to the Opus Mulierum et Ludus Puerorum and identifies additional sources in Arnold of Villanova and the Turba Philosophorum. She demonstrates how Maier assembles multiple alchemical authorities to construct his threefold maxim that Nature teaches, conquers, and rules Nature.",

    31: "De Jong identifies the motto source in the Tabula Smaragdina and traces how Maier develops the nursing metaphor across Emblems I-II, connecting the wind (volatile mercury) as father to the earth (fixed body) as nurse. She demonstrates the systematic use of the Emerald Tablet as a structural template for the opening emblem sequence.",

    44: "De Jong traces the golden rain motif to the Turba Philosophorum and identifies Socrates as the speaker in the source text. She demonstrates how Maier connects the alchemical production of white lead to the Hermetic tradition of herms as guideposts, and how the command to 'do woman's work' (cooking) signals the transition from albedo to the sustained heating of the citrinitas.",

    45: "De Jong identifies the wolf-king allegory's source in Strabo and in Basil Valentine's Twelve Keys, demonstrating that the wolf represents antimony used to purify gold from base alloys. She traces the metallurgical process of antimony refining behind Maier's mythological narrative of royal death and resurrection.",

    46: "De Jong traces the dragon imagery to Basil Valentine's Practica cum Duodecim Clavibus and identifies the underlying chemistry as the dissolution of mercury by its own 'brother and sister' (Sol and Luna, gold and silver). She connects this to the Golden Fleece myth where the guardian dragon must be slain before the treasure is obtained.",

    48: "De Jong identifies the steam bath allegory's source in the Processus Chemici and the Allegoria Merlini, tracing King Duenech's purification through therapeutic bathing to the medical tradition of humoral purgation. She connects the black bile (aqua foetida) to the nigredo impurity that must be expelled through gentle, sustained moist heat.",

    49: "De Jong traces the salamander-in-fire motif to Avicenna's Tractatulus de Alchimia, identifying the philosophical stone's fire-resistance as the key test of successful fixation. She connects the coral analogy (growing soft underwater, hardening in air) to the same principle of state-change from fluid process to solid product.",

    56: "De Jong identifies the source in the Rosarium Philosophorum's account of the Rebis, connecting the Hermaphrodite born of two mountains (Mercury and Venus) to Morienus's teaching that the substance must be found through living masters rather than books. She traces the two-topped Parnassus allegory to the philosophical Mercury's dual nature.",

    50: "De Jong traces the king-in-the-sea allegory to the Rosarium Philosophorum and identifies the 'vegetable stone' that grows and multiplies as the product of successful fixation. She connects the king's promise of reward to the alchemical doctrine of multiplication — whoever rescues the dissolved gold will receive manifold return.",

    51: "De Jong identifies the source in the Allegoriae super Turbam and traces the coral growth analogy to the alchemical principle of fixation. She demonstrates how the underwater-to-air transition mirrors the philosophical substance's change from volatile fluid to fixed solid during the rubedo completion.",

    52: "De Jong traces the source to Senior's Tabula Chimica and the Scala Philosophorum, connecting the digestion-and-fire imagery to Ceres tempering Triptolemus and Thetis dipping Achilles. She identifies the underlying principle as graduated calcination — the slow, repeated application of heat to fix and harden the volatile components.",

    54: "De Jong identifies the source in the Rosarium Philosophorum's teaching that the Stone has been cast down onto the earth yet exalted on the mountains. She connects this to the broader tradition that the prima materia is found everywhere yet recognized by none, and identifies a nationalistic element in Maier's earth-as-mother imagery.",

    55: "De Jong traces the Hermaphrodite's standing posture to Morienus's De Transmutatione Metallorum, identifying this as the completed union of Mercury and Venus. She demonstrates how Maier uses the Socratic cosmopolitanism allegory to argue that the perfected substance inhabits multiple domains simultaneously.",

    64: "De Jong identifies the standing Hermaphrodite as the completed product of the conjunction, drawing on the Rosarium Philosophorum's account of the Rebis as the final stage of the rubedo where masculine and feminine principles achieve permanent, autonomous stability.",

    57: "De Jong traces the Oedipus-Sphinx allegory to Maier's distinctive alchemical reinterpretation of the riddle: the four legs represent the four elements, the two legs the half-moon of the immature white stone, and the three legs the triangle of body, spirit, and soul. She cites Rhazes as authority for the 'triangle in essence, quadrangle in quality' formula.",

    42: "De Jong identifies the source in the Opus Mulierum and traces Maier's alchemical reading of the two waters (volatile ascending and fixed descending) to the Hermetic tradition of the caduceus. She connects the 'water of holiness' to both baptismal and Lullian elixir symbolism.",

    30: "De Jong traces the four guides (Nature, Reason, Experience, Reading) to the Tabula Smaragdina tradition, identifying them as Maier's systematic summation of the alchemical method. She demonstrates how Maier maps these four onto fire, vessel, water, and earth — the essential components of the practical work.",

    59: "De Jong identifies the two eagles from East and West in the Consilium Conjugii and traces the philosophical conjunction of Sulphur (Eastern, solar) and Mercury (Western, lunar) through the Aristotelian tradition transmitted via Petrus Bonus's Margarita Pretiosa.",

    60: "De Jong traces the wolf-and-dog allegory to Rhazes's Epistola as cited in Petrus Bonus, identifying the terrestrial counterpart to the aerial eagle-conjunction of the preceding emblem. She demonstrates how the mutual biting represents reciprocal dissolution at the material register.",

    61: "De Jong identifies the sick king allegory in the Merlini tradition and traces the physician's cure through the sequence of Egyptian and Alexandrian doctors to the progressive refinement of alchemical technique. She connects Bernard of Treves's account of the king dressed in black cuirass, white tunic, and purple-red cloak to the three colors of the opus (nigredo, albedo, rubedo).",
}


def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    updated = 0

    for ref_id, summary in CLEAN_SUMMARIES.items():
        result = c.execute('UPDATE scholarly_refs SET summary = ? WHERE id = ?', (summary, ref_id))
        if result.rowcount > 0:
            updated += 1

    conn.commit()
    conn.close()
    print(f'Cleaned {updated}/{len(CLEAN_SUMMARIES)} scholarly ref summaries.')


if __name__ == '__main__':
    main()
