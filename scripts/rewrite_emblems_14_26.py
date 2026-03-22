"""
Rewrite image_description and discourse_summary for Emblems 14-26
to museum-level curation quality, following WRITING_TEMPLATES.md.

Section 1 (The Plate): Visual description, present tense, no interpretation.
Section 2 (Maier's Discourse): Academic summary of Maier's argument.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'atalanta.db')

UPDATES = {
    14: {
        "image_description": (
            "A large winged dragon coils in the foreground of a ruined landscape, "
            "its jaws clamped firmly around its own tail to form a continuous loop. "
            "The creature's scaled body, rendered in fine crosshatching, curves in a "
            "tight circle against bare earth. Behind the ouroboros, crumbling stone "
            "walls and the remnants of classical architecture rise against an open sky, "
            "suggesting an ancient, abandoned setting."
        ),
        "discourse_summary": (
            "Maier argues that the dragon devouring its own tail represents the "
            "circular course of the alchemical process, in which matter is repeatedly "
            "dissolved, evaporated, and redistilled until its volatile, poisonous "
            "components are digested and stabilized. He draws on Lullius's Codicillus "
            "to identify the dragon with sulphur and cites the Rosarium Philosophorum's "
            "dictum that the dragon cannot die unless killed by its brother and sister "
            "(Sol and Luna, the subject of Emblem XXV). The discourse connects the "
            "ouroboros to both the annual solar cycle and the gnostic dragon of outer "
            "darkness from the Pistis Sophia, framing the image as a symbol of "
            "alchemical unity in which destruction and regeneration are inseparable."
        ),
    },
    15: {
        "image_description": (
            "A potter sits at his wheel inside a workshop, shaping a vessel with both "
            "hands as the wheel turns beneath him. He wears a broad-brimmed hat and "
            "a working apron, his posture bent in concentration over the wet clay. "
            "Around him on shelves and on the floor stand finished vessels of various "
            "sizes -- pitchers, bowls, and wide-mouthed jars. A basin of water sits "
            "in the left foreground, and through a latticed window on the right, "
            "daylight enters the enclosed workshop."
        ),
        "discourse_summary": (
            "Maier develops an extended analogy between the potter's craft and the "
            "alchemical opus, arguing that both depend on achieving a proper ratio "
            "of dry and moist elements. He cites the Scala Philosophorum to establish "
            "that dissolving and coagulating are the twin foundations of the art, "
            "just as the potter tempers earth with water to produce a kneadable mass "
            "that is then hardened by fire into stone. The discourse warns against "
            "diabolical conjurations and impossible experiments, alluding to the folly "
            "of Julius Sperber, and concludes by invoking the sulphur-mercury theory "
            "of Jabir ibn Hayyan: gold ripens naturally in the earth from sulphur and "
            "mercury over millennia, and the alchemist must replicate this natural "
            "process rather than circumvent it."
        ),
    },
    16: {
        "image_description": (
            "Two lions grapple in fierce combat at the center of a wooded landscape. "
            "The lion on the right, wingless and standing firmly on the ground, seizes "
            "the winged lioness on the left, who rears up with feathered wings spread "
            "wide as if attempting to take flight. The wingless lion grips the lioness "
            "with its foreclaws, holding her down by sheer weight. In the background, "
            "a stone tower stands at the left edge, and dense foliage frames the "
            "struggle on both sides."
        ),
        "discourse_summary": (
            "Maier constructs an elaborate allegory of the mercury-sulphur union through "
            "the figure of the lion, arguing that the wingless lion represents fixed, "
            "combustible sulphur while the winged lioness embodies volatile, liquid "
            "mercury. He draws on Senior's Tabula Chimica, where the wingless male "
            "restrains the winged female, and on Lambsprinck's emblem of two lions in "
            "a dark valley, to argue that spirit and soul must be reunited with their "
            "body. The discourse describes how the red lion must be captured from the "
            "mountaintop and led into the valley to mate with the winged lioness, after "
            "which the pair must be raised together to the summit in an indissoluble "
            "union -- a process analogous to the conjunction of superiora and inferiora "
            "from the Tabula Smaragdina."
        ),
    },
    17: {
        "image_description": (
            "Four large fireballs, blazing with curling flames, are stacked vertically "
            "in a column that rises from the ground into the sky. Each sphere is "
            "rendered with dense, swirling lines suggesting intense radiant heat. "
            "The column of fire stands beside a river or canal in a flat landscape; "
            "a small house and a tree appear at the left, and a boat with figures "
            "floats on the water at the right. Clouds gather in the upper portion "
            "of the sky behind the topmost fireball."
        ),
        "discourse_summary": (
            "Maier identifies four grades of fire essential to the alchemical opus, "
            "drawing on Riplaeus's Liber Duodecim Portarum and the Scala Philosophorum. "
            "He assigns each fireball a planetary correspondence: Vulcan for the common "
            "elementary fire, Mercury for the corrosive fire contrary to nature (the "
            "fiery dragon that dissolves matter), Luna for the gentle warmth of ashes "
            "or baths, and Apollo for the natural fire inherent in all things. The "
            "discourse argues that these fires form a chain-like sequence of active "
            "and passive principles, each dependent on the others, and compares their "
            "mutual action to a magnet communicating its power through a series of "
            "iron rings. Maier further cites Lullius's Testamentum to connect the "
            "four fires to the cosmic transmutation of elements from earth through "
            "water and air to fire, a graduated ascent toward the divine."
        ),
    },
    18: {
        "image_description": (
            "A man in Renaissance attire and a plumed hat stands at a workbench, "
            "tending a vessel set over an open fire. He holds a long-handled tool "
            "in his right hand, stirring or adjusting the contents of the heated "
            "container, which sits on a low stump or furnace with flames leaping "
            "around it. In the right foreground, a small monkey or ape crouches on "
            "the floor. Through an archway in the background, a second scene is "
            "visible: figures walking near a church or large building in a pastoral "
            "landscape."
        ),
        "discourse_summary": (
            "Maier argues that fire assimilates everything it touches to its own "
            "nature, but gold cannot be made simply by applying fire -- one must "
            "seek the Tinctura from which gold originates. He cites Avicenna's "
            "Liber de Congelatione Lapidum on the principle that every natural "
            "substance strives to impose its own form on what is added to it, and "
            "draws an analogy to the concentrating power of a burning-glass that "
            "focuses diffused sunbeams into a destructive point. The discourse "
            "warns alchemists against attempting transmutation with materials foreign "
            "to gold's nature, invoking Riplaeus's dictum that gold is the true "
            "foundation for making gold, just as fire is the foundation for making "
            "things fiery. Maier expresses notable skepticism about the possibility "
            "of genuine species-transmutation by human art, citing Avicenna's denial "
            "that the essential differences between metals can be removed artificially."
        ),
    },
    19: {
        "image_description": (
            "Four muscular men stand in a tight group, arranged in a row across the "
            "foreground of a mountainous landscape. Each holds a different object "
            "representing one of the four elements: one grasps a lump of earth, "
            "another carries a vessel of water, a third holds a billowing cloth or "
            "sack of air, and the fourth brandishes a flaming torch. The figure at "
            "the far right raises a heavy club overhead, poised to strike one of his "
            "brothers. A walled city with towers rises in the distant background."
        ),
        "discourse_summary": (
            "Maier argues that the four elements are so intimately bound that killing "
            "any one of them triggers the destruction of the remaining three, like "
            "conjoined twins who cannot survive one another's death. He frames the "
            "allegory through the myth of Geryon's three bodies and the warriors sprung "
            "from dragon's teeth sown by Jason and Cadmus, who slaughtered one another "
            "on the battlefield. The discourse counsels that the alchemist must kill "
            "the elements in such a way that they can be revived, citing Hermes on "
            "the dragon fleeing from sunbeams and the Belinus-metaphor from the "
            "Rosarium Philosophorum, in which death and resurrection extend from the "
            "chemical domain to the purification of the human soul."
        ),
    },
    20: {
        "image_description": (
            "An armored knight advances from the right, his shield raised and his "
            "sword drawn, positioning himself between a nude young woman and a "
            "raging fire that threatens to engulf her from the left. The woman "
            "stands with arms partly raised in a gesture of distress, her body "
            "turned toward the knight as flames curl aggressively around the "
            "scene. The knight wears a plumed helmet and full plate armor. In the "
            "background, a hilly landscape stretches beneath a clouded sky, with "
            "the fire's glow illuminating the foreground."
        ),
        "discourse_summary": (
            "Maier develops the maxim from Pseudo-Democritus and the Turba "
            "Philosophorum -- that nature teaches, conquers, and rules nature -- "
            "into an argument about protective instruction within the alchemical "
            "process. He compares the way adult birds teach fledglings to fly "
            "with the way one chemical substance shields another from the "
            "destructive violence of fire, citing the example of iron protecting "
            "gold and silver from arsenic and antimony during smelting. The "
            "discourse identifies the protective agent as eudica (glass gall), "
            "drawn from Morienus's De Transmutatione Metallorum, and equates the "
            "armed knight of the emblem with the red sulphur that guards the "
            "volatile mercury (the virgin, also called Beya or Blanca from the "
            "Visio Arislei) against the scorching fire."
        ),
    },
    21: {
        "image_description": (
            "A robed geometrician stands at the left, holding a large pair of "
            "compasses with which he inscribes or measures a set of nested "
            "geometric figures on a vertical surface or wall. The diagram consists "
            "of a circle enclosing a square, which in turn contains a triangle, "
            "and within the triangle a smaller circle encloses two standing human "
            "figures -- a nude man and a nude woman. The geometrician wears a long "
            "gown and cap, and the background shows a brick or stone wall extending "
            "to the right."
        ),
        "discourse_summary": (
            "Maier presents the entire alchemical process as a geometric "
            "progression: from the circle of primary matter (man and woman as "
            "sulphur and mercury), through the square of the four elements "
            "separated by their colors, to the triangle of body, spirit, and soul "
            "(the tria prima), and finally back to the circle of the perfected "
            "Philosophers' Stone. He grounds this schema in the Rosarium "
            "Philosophorum and the commentary on Hermes Trismegistus's Tractatus "
            "Vere Aureus, arguing that the quadrature of the circle -- sought "
            "in vain by mathematicians -- was already known to the natural "
            "philosophers. The discourse concludes that the final stage returns "
            "the multiplicity of elements to the monad, invoking John Dee's "
            "Monas Hieroglyphica and the Hermetic Poimander to frame the "
            "alchemical opus as a return to divine unity in which rest and "
            "eternal peace are achieved."
        ),
    },
    22: {
        "image_description": (
            "A woman stands in a domestic kitchen, attending to a large pot "
            "suspended over an open hearth fire by a chain from above. Dense "
            "steam rises from the vessel into the chimney. She wears a long dress "
            "and head covering, and holds a paddle or ladle in one hand. Around "
            "her on the kitchen bench and floor are smaller vessels, a basin "
            "containing what appear to be fish, and various cooking implements. "
            "Through a window on the right wall, a landscape with trees is "
            "faintly visible."
        ),
        "discourse_summary": (
            "Maier argues that once the black lead of Saturn has been whitened "
            "into the philosophical Jupiter (tin), the remaining work is merely "
            "women's work -- that is, patient cooking. He cites the Turba "
            "Philosophorum's Socrates, who declared that after obtaining white "
            "lead nothing remains but the opus mulierum. The discourse develops "
            "an analogy between a woman cooking fish in a sealed double vessel "
            "and the alchemist's procedure of dissolving the subject in its own "
            "caustic water, then coagulating and hardening it in the sealed vas "
            "hermeticum. Maier identifies the pregnant woman in the emblem's "
            "plate as the personification of the albedo, the white stage from "
            "which the rubedo and the Philosophers' Stone will be born."
        ),
    },
    23: {
        "image_description": (
            "The plate is divided into two scenes. In the foreground, Vulcan "
            "stands with his back to a blazing forge fire, an axe raised in his "
            "hands, having just split open the head of a reclining Jupiter from "
            "which the fully formed figure of Athena (Pallas) emerges in armor "
            "with a radiant nimbus. In the background, a separate scene shows Sol "
            "and Venus reclining together beneath a canopy or bower while a shower "
            "of gold coins descends from the sky around them. Birds fly overhead "
            "in the middle distance."
        ),
        "discourse_summary": (
            "Maier interprets the golden rain that fell on Rhodes at Athena's "
            "birth as an allegory for the vivifying power of Sol united with "
            "Venus -- a variant of the coniunctio motif that recurs throughout "
            "the Atalanta Fugiens. He traces the Isle of Rhodes through three "
            "names (Ophiusa for its serpents, Rhodes for its roses, Colossicola "
            "for its sun-statue) and maps each onto stages of the alchemical "
            "process: raw mercury as serpent, the prepared matter as the purple "
            "rose, and the perfected gold as the radiant sun. The discourse "
            "identifies Athena-Sapientia as wisdom born when power and love unite, "
            "connecting this emblem to Emblem VIII (the egg pierced by Vulcan's "
            "fiery sword) and to Emblem XXVI (the fruit of wisdom as the Tree "
            "of Life)."
        ),
    },
    24: {
        "image_description": (
            "In the foreground, a large grey wolf crouches over the prostrate body "
            "of a crowned king, its jaws clamped on the king's torso as it devours "
            "him. The king lies supine on bare ground, his crown still visible, his "
            "arms slack. Behind them, in the middle distance, a figure tends a "
            "large bonfire in which a second wolf -- or the same wolf at a later "
            "stage -- burns amid leaping flames. A walled city with towers and "
            "spires stretches across the horizon beneath a darkening sky."
        ),
        "discourse_summary": (
            "Maier draws on the first of Basil Valentine's Twelve Keys to argue "
            "that the king (gold, or the Philosophers' Stone in its impure state) "
            "must be devoured by the voracious grey wolf (antimony) and then "
            "purified by fire, after which the king rises immortal and invincible "
            "with the heart of a lion. He describes the wolf as a son of Saturn "
            "and subject to bellicose Mars, roaming mountains and valleys consumed "
            "by insatiable hunger. The discourse develops the royal allegory further: "
            "the king, youngest and humblest of his six planetary brothers, travels "
            "from the East, is captured and imprisoned in successive sublimations, "
            "and must endure misery before attaining his throne -- a narrative "
            "pattern Maier connects to the death-and-resurrection motifs of "
            "Emblems XIX, XXV, XXVIII, and XXXI."
        ),
    },
    25: {
        "image_description": (
            "In the foreground, Sol and Luna -- depicted as a male and female "
            "figure -- attack a large winged dragon with a heavy club, smashing "
            "its rearing head. The dragon's wings spread wide and its serpentine "
            "tail coils behind it. In the middle ground, the same pair appears "
            "again, now armed with bows and arrows, shooting at the dragon from "
            "a distance. Behind them, a seascape stretches to the horizon, where "
            "a small figure swims with arms outstretched, calling for rescue. "
            "The header identifies the discourse as XXV."
        ),
        "discourse_summary": (
            "Maier argues that the philosophical dragon -- volatile Mercury "
            "separated from the bodies -- cannot be killed except by the joint "
            "action of its brother Sol and its sister Luna, citing the Rosarium "
            "Philosophorum and the precedent of Jason, who conquered the Golden "
            "Fleece dragon using images of the Sun and Moon given to him by Medea. "
            "The discourse identifies the dragon as the aqua permanens, the "
            "eternal philosophical water that arises after putrefaction and the "
            "separation of the elements, and emphasizes that Mercury must be "
            "coagulated with both Sol and Luna together -- not by one alone. "
            "Maier connects this emblem to the ouroboros of Emblem XIV and to "
            "the swimming king of Emblem XXXI, extending the allegory from "
            "chemical transformation to the endangered human soul submerged in "
            "the waters of destruction."
        ),
    },
    26: {
        "image_description": (
            "A crowned female figure, Lady Sapientia (Wisdom), stands at the "
            "center of an open landscape, richly dressed in flowing robes. She "
            "extends both arms outward, each hand holding a banderole inscribed "
            "with Latin text: the right reads 'longitudo dierum et sanitas' "
            "(length of days and health) and the left reads 'gloria ac divitiae "
            "infinitae' (honor and infinite riches). Beside her on the right "
            "stands a fruit-bearing tree -- the Tree of Life -- its branches "
            "spreading above her. In the far background at the left, rays of "
            "light break through clouds over a distant mountain."
        ),
        "discourse_summary": (
            "Maier argues that true human wisdom consists not in rhetorical "
            "sophistication or grammatical subtlety but in the knowledge and "
            "application of True Chemistry, which he elevates above all the "
            "liberal arts of the trivium. He draws extensively on the Old "
            "Testament -- Proverbs III on the Tree of Life, the Book of Wisdom "
            "on Sapientia's friendship, and Baruch on the distribution of "
            "length of days and peace -- alongside Morienus's declaration that "
            "alchemical knowledge is a divine gift entrusted only to God's "
            "faithful servants. The discourse frames the Philosophers' Stone as "
            "the fruit of this wisdom-tree: not eternal salvation itself, but "
            "the path to health, wealth, and inner peace that distinguishes the "
            "wise from those who remain, as Maier puts it, dead while still alive."
        ),
    },
}


def main():
    db_path = os.path.normpath(DB_PATH)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    for emblem_num, fields in UPDATES.items():
        cur.execute(
            """UPDATE emblems
               SET image_description = ?,
                   discourse_summary = ?,
                   source_method = 'LLM_ASSISTED',
                   review_status = 'DRAFT',
                   confidence = 'MEDIUM'
               WHERE number = ?""",
            (fields["image_description"], fields["discourse_summary"], emblem_num)
        )
        if cur.rowcount == 1:
            print(f"  [OK] Emblem {emblem_num} updated")
        else:
            print(f"  [WARN] Emblem {emblem_num}: {cur.rowcount} rows affected")

    conn.commit()
    conn.close()
    print(f"\nDone. Updated {len(UPDATES)} emblems (14-26).")


if __name__ == "__main__":
    main()
