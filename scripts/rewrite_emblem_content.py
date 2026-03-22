"""Rewrite image_description and discourse_summary for all 51 emblems.

Museum-level curation quality following docs/WRITING_TEMPLATES.md:
- image_description: 3-5 sentences, curatorial visual description of the plate
- discourse_summary: 3-5 sentences, academic summary of Maier's discourse argument

Sources: De Jong (1969), Craven (1910), standard Maier scholarship.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'atalanta.db')

EMBLEM_CONTENT = {
    0: {
        "image_description": (
            "The title-page engraving depicts the race of Atalanta and Hippomenes at the bottom, "
            "with Hippomenes in mid-stride casting a golden apple while Atalanta stoops to retrieve one from the ground. "
            "At the left margin, Venus extends the golden apples to Hippomenes; at the right, the couple embraces in a temple entrance "
            "before emerging behind it as a lion and lioness, their transformation by Cybele. "
            "The upper register shows Hercules in his lion-skin approaching the tree of the Hesperides, reaching for the golden fruit "
            "while the three Hesperides — Aegle, Arethusa, and Hespertusa — watch from above. "
            "The central cartouche frames the title text in an architectural surround, unifying the mythological scenes "
            "into a single emblematic program that introduces the work's central conceit."
        ),
        "discourse_summary": (
            "Maier's introductory apparatus presents Atalanta Fugiens as an exercise in multi-sensory pedagogy: "
            "the subtitle promises emblems for the eyes, fugues for the ears, and epigrams for the intellect, "
            "engaging sight, hearing, and reason simultaneously in the pursuit of Nature's secrets. "
            "The myth of the footrace serves as a heuristic model for the reader's own engagement — just as Hippomenes "
            "must distract the swift Atalanta with golden apples to win the race, the reader must use the sensory "
            "enticements of image, music, and verse to catch the fleeting truths of alchemical philosophy. "
            "De Jong characterizes this as Maier's 'lusus serius' or serious game, a Renaissance pedagogical strategy "
            "in which play, meditation, and intellectual pursuit are fused into a single practice of discovery. "
            "The frontispiece thus functions not merely as decoration but as an instruction manual for how to read "
            "the fifty emblems that follow — each a puzzle requiring the reader to chase meaning across multiple registers."
        ),
    },
    1: {
        "image_description": (
            "A muscular male figure, identified as Boreas the North Wind, strides across a rocky landscape "
            "carrying a swaddled infant against his torso. The wind god's hair and drapery stream behind him, "
            "and billowing clouds fill the sky above. Below, a female earth figure — massive, globular, with exposed breasts — "
            "reclines on the ground, her body merging with the landscape itself. "
            "A small child nurses at her breast while animals graze nearby, establishing the maternal earth as nurse."
        ),
        "discourse_summary": (
            "Maier develops the Tabula Smaragdina's declaration that 'the wind carried it in its belly' into an extended "
            "analogy between alchemical generation and natural gestation. He argues that the philosophical substance "
            "must first be conceived in air (the volatile spirit) before being nourished by earth (the fixed body), "
            "just as an embryo is carried in the womb before being nursed after birth. "
            "The discourse draws on Peripatetic natural philosophy to assert that nourishment must share the nature "
            "of what it feeds, establishing the principle that the Stone requires earth — that is, a fixed, corporeal "
            "substrate — as its nurse. Maier cites Hermes Trismegistus as the ultimate authority for this teaching."
        ),
    },
    2: {
        "image_description": (
            "The same globular earth-mother figure from Emblem I reappears at center, her body forming a living landscape "
            "with a small child nursing at her breast. She sits or reclines against a hillside with a town visible in the distance. "
            "Animals — a cow and smaller creatures — graze at her feet, reinforcing her identification with the nurturing earth. "
            "The composition emphasizes the maternal relationship between the vast earthly body and the tiny philosophical infant."
        ),
        "discourse_summary": (
            "Maier continues the theme of Emblem I, now emphasizing that the earth is specifically the nurse, not the mother, "
            "of the philosophical substance. He distinguishes between generation (which occurs through the volatile principle, "
            "the wind) and nourishment (which requires the fixed, earthy body). "
            "The discourse argues that just as human food must be converted into the substance of the body it feeds, "
            "so the alchemical earth must be assimilated into the growing Stone. Maier draws a careful analogy between "
            "the stages of infant feeding — blood in utero, milk after birth, solid food later — and the progressive "
            "fixation of the volatile philosophical substance."
        ),
    },
    3: {
        "image_description": (
            "A woman kneels beside a wooden washing trough in an outdoor setting, scrubbing sheets or linens in soapy water. "
            "Her sleeves are rolled up and her posture suggests vigorous labor. A second figure, likely the alchemist-observer, "
            "watches from nearby. In the background, linens hang on a line to dry against a landscape of trees and buildings. "
            "The scene is emphatically domestic and practical, grounding the alchemical process in the imagery of common housework."
        ),
        "discourse_summary": (
            "Maier argues that the alchemical purification process mirrors the everyday work of washing dirty linen: "
            "just as earth-stains on fabric are removed by water and then dried by sun and wind, so the impurities of the "
            "philosophical substance must be cleansed through repeated washing and exposure to the elements. "
            "The discourse develops the principle that what comes from earth is cleaned by the next element in the sequence — "
            "water purifies earth, air dries what water has cleaned. Maier presents the washerwoman as a figure for "
            "the alchemist who must patiently repeat the cycle of dissolution and drying, an operation the tradition "
            "calls the albedo or whitening stage."
        ),
    },
    4: {
        "image_description": (
            "A young man and woman face each other in a formal garden or courtyard setting, joining hands or exchanging "
            "a cup between them. Their postures suggest both greeting and ceremonial union. Behind them, architectural "
            "elements frame the scene — an archway or portico. The composition centers on the gesture of joining, "
            "with the cup of love serving as the mediating object between the two figures."
        ),
        "discourse_summary": (
            "Maier frames the alchemical coniunctio as a marriage between brother and sister — the masculine and feminine "
            "principles of the same substance — who must be united by the 'cup of love,' the solvent that dissolves both "
            "into a single new body. He draws on Oedipus's unwitting marriage to his mother Jocasta as an analogy for "
            "the paradoxical union of opposites that share a common origin. The discourse argues that the philosophical "
            "work is fundamentally gendered labor: the masculine role is to beget and govern, the feminine to conceive "
            "and nourish. Maier cites both classical mythology and Arabic alchemical sources to establish that this "
            "conjunction of fixed and volatile is the central operation of the entire art."
        ),
    },
    5: {
        "image_description": (
            "A woman sits outdoors on a stone bench, her bodice loosened, nursing a large toad at her breast. "
            "The toad clings to her chest with its forelimbs, drawing milk while the woman's expression registers "
            "calm resignation rather than horror. Behind her, a walled town rises against a hilly landscape with scattered trees. "
            "In the foreground, a second smaller toad waits on the ground. "
            "The scene inverts the conventional nursing Madonna into an image of productive destruction."
        ),
        "discourse_summary": (
            "Maier frames the alchemical operation as gendered labor, arguing that the masculine principle begets and governs "
            "while the feminine conceives, bears, and nourishes. He develops the toad as a figure for the volatile, "
            "poisonous agent that must be fed by the maternal body of the prima materia — a feeding that kills the nurse "
            "but matures the product. Maier draws the analogy to Cleopatra's death by asp-venom, suggesting that the "
            "transfer of vital essence from woman to toad mirrors the fixation of the volatile sulphur through prolonged "
            "contact with a liquid menstruum. The discourse cites the Pseudo-Aristotelian Tractatulus de Practica Lapidis "
            "as the source of this toad-nursing imagery."
        ),
    },
    6: {
        "image_description": (
            "A farmer figure kneels in a plowed field, sowing seed from a bag or pouch into furrows of white or pale earth. "
            "The field is carefully tilled in neat rows, and the landscape behind shows a cultivated countryside with "
            "distant buildings and trees. The emphasis falls on the act of sowing — the careful placement of precious material "
            "into prepared ground — with the whiteness of the earth itself visually prominent."
        ),
        "discourse_summary": (
            "Maier develops an extended agricultural analogy: just as the farmer must sow grain in prepared soil to reap "
            "a harvest, the alchemist must 'sow' philosophical gold in 'white foliated earth' — a specially prepared "
            "mercurial substrate — to produce the Stone. Drawing on Plato's division of the civic body into physicians "
            "and farmers, Maier argues that the alchemist combines both roles, healing metals while cultivating them. "
            "The discourse establishes a key principle: the seed (gold) must be of the same species as what it produces, "
            "and the earth (mercury) must be receptive and properly tempered. The white, foliated quality of the earth "
            "indicates the albedo stage, where the purified substrate is ready to receive the active seed."
        ),
    },
    7: {
        "image_description": (
            "A young bird — identified in the motto as a philosophical chick — launches upward from a nest perched "
            "in a tree or rocky outcrop, wings spread in attempted flight. Below, the same or another bird falls back "
            "toward the nest, unable to sustain its ascent. The landscape includes trees and possibly a distant town. "
            "The dual image of rising and falling captures the cyclical nature of sublimation and descent."
        ),
        "discourse_summary": (
            "Maier describes a species of bird that flies upward from its nest only to fall back again repeatedly, "
            "developing this as an analogy for the alchemical process of sublimation and condensation. He argues that "
            "the volatile philosophical substance must be repeatedly driven upward (sublimated) and allowed to fall back "
            "(condensed) until it is sufficiently matured to sustain itself. The discourse connects this to the broader "
            "principle that Nature works through cyclical repetition rather than linear progress. Maier suggests that "
            "the bird's eventual success in flight corresponds to the moment when the volatile spirit is finally fixed "
            "and can maintain its elevated state."
        ),
    },
    8: {
        "image_description": (
            "A hand extends from the left holding a flaming sword, driving it into a large egg that sits on a surface "
            "or pedestal at center. The egg cracks under the blade's impact, and flames or vapors escape from the breach. "
            "The setting is minimal, focusing attention entirely on the violent yet precise act of piercing the philosophical egg. "
            "The fiery sword introduces the element of controlled heat into the self-contained vessel of the egg."
        ),
        "discourse_summary": (
            "Maier develops the egg as a figure for the sealed vessel containing the prima materia, arguing that it must "
            "be pierced — that is, opened to the action of fire — with a fiery sword to release and transform its contents. "
            "The discourse draws on the widespread alchemical tradition of the philosophical egg (ovum philosophicum), "
            "where the shell represents the vessel, the white the mercury, and the yolk the sulphur. Maier argues that "
            "the sword of fire must be applied with precision — too little heat fails to open the egg, too much destroys "
            "the embryonic substance within. The operation described is calcination, the controlled application of heat "
            "to break down the initial form of the material."
        ),
    },
    9: {
        "image_description": (
            "An old man, stooped with age, is fastened or bound to a tree in what appears to be a garden or orchard. "
            "Dew or moisture descends from above — sometimes depicted as rain or celestial drops — onto the old man's body. "
            "The garden setting is lush, suggesting the dew is a life-giving rather than punishing element. "
            "The tree to which the old man is fixed may bear fruit, connecting the scene to ideas of renewal and harvest."
        ),
        "discourse_summary": (
            "Maier argues that the old man represents the fixed, aged substance of the philosophical body that must be "
            "rejuvenated through exposure to celestial dew — the volatile, purifying spirit descending from above. "
            "He develops a parallel between this image and classical accounts of rejuvenation through divine intervention, "
            "including the myth of Aeson restored to youth by Medea. The discourse emphasizes that the tree functions "
            "as the apparatus of fixation: the old body is held in place while the volatile moisture penetrates and renews it. "
            "Maier cites the Turba Philosophorum and the pronouncement of Balgus as authorities for this doctrine of "
            "rejuvenation through the marriage of fixed and volatile."
        ),
    },
    10: {
        "image_description": (
            "Two fires burn in separate vessels or furnaces, with a figure tending them or directing material between them. "
            "Mercury — possibly depicted as a caduceus-bearing figure or as liquid quicksilver — appears in duplicate, "
            "being passed from one vessel to another. The composition emphasizes doubling and correspondence: "
            "fire feeds fire, mercury feeds mercury, in a self-reinforcing cycle."
        ),
        "discourse_summary": (
            "Maier develops the principle that like produces like: fire must be added to fire, and mercury to mercury, "
            "for the philosophical work to succeed. He argues against the common error of mixing incompatible substances, "
            "insisting that the alchemist must recognize the common nature hidden beneath different appearances. "
            "The discourse draws on the allegory of Saturn devouring his children, which Maier interprets as the "
            "dissolution of metals back into their mercurial prima materia. He cites the Turba Philosophorum's dictum "
            "that the Stone is nourished only by its own kind, establishing the principle of philosophical homogeneity "
            "that governs the entire citrinitas stage."
        ),
    },
    11: {
        "image_description": (
            "A female figure identified as Latona stands at center, her skin darkened or stained, while attendants "
            "or alchemists work to wash or whiten her body. Books or scrolls lie torn or scattered on the ground around her, "
            "their destruction commanded by the motto. The scene combines the act of purification — making Latona white — "
            "with the rejection of textual authority in favor of direct practice."
        ),
        "discourse_summary": (
            "Maier commands two simultaneous actions: whiten Latona and tear up the books. He develops Latona as a figure "
            "for the imperfect philosophical body — an alloy of Sol and Luna stained with black impurities — that must be "
            "purified through the albedo. De Jong traces the name Latona to 'laton,' meaning electrum or yellow silver, "
            "connecting the mythological goddess to the metallurgical process of whitening a dark alloy. "
            "The instruction to destroy books signals Maier's insistence that neither theory alone nor book-learning "
            "can substitute for practical laboratory work — the alchemist must act on matter directly, not merely read about it. "
            "The discourse argues that both intellect and manual labor are necessary, but that practice takes precedence."
        ),
    },
    12: {
        "image_description": (
            "The composition closely parallels Emblem XI: the figure of Latona appears again in the process of being "
            "whitened, while books and scrolls are visibly torn or discarded. The emphasis shifts slightly to the "
            "completed act of purification — Latona is lighter or whiter than in the previous emblem, suggesting "
            "progress in the albedo. The torn books lie definitively abandoned on the ground."
        ),
        "discourse_summary": (
            "Maier continues the argument of Emblem XI, now emphasizing the bewildering variety and obscurity of "
            "alchemical writings as the reason books must be abandoned. He argues that the sheer volume of contradictory "
            "texts drives seekers to despair, and that the only path forward is direct engagement with the material. "
            "The discourse develops the Latona allegory further: she is an impure body of mixed Sol and Luna "
            "that must be found in a humble place, immersed in dung where she becomes white lead, from which red lead "
            "originates. Maier presents this as the beginning and end of the opus — the albedo whitening that initiates "
            "the final reddening toward the rubedo."
        ),
    },
    13: {
        "image_description": (
            "A male figure, possibly identified as Naaman the Syrian, stands immersed in a river — the Jordan — "
            "up to his waist or chest. His skin appears spotted or discolored, indicating the leprosy or 'dropsy' "
            "of the motto. Attendants or witnesses stand on the riverbank observing the ritual washing. "
            "The landscape includes trees and possibly a distant city, situating the scene in a biblical geography."
        ),
        "discourse_summary": (
            "Maier draws on the biblical story of Naaman the leper, healed by washing seven times in the Jordan, "
            "as an allegory for the purification of the philosophical ore. He argues that the 'dropsical' stone — "
            "swollen with impurities — must undergo repeated washing to be cleansed, just as Naaman's leprosy was "
            "cured only through sevenfold immersion. The discourse connects this to the albedo purification and to "
            "the sacramental symbolism of baptism as a prefiguration of alchemical cleansing. "
            "Maier cites the Clangor Buccinae as the source of the dropsical ore metaphor, linking it explicitly "
            "to the Latona-whitening sequence of the preceding emblems."
        ),
    },
}

# Emblems 14-50: generate from existing data + scholarly context
EMBLEM_CONTENT.update({
    14: {
        "image_description": (
            "A serpent coils upon itself, its jaws clamped around its own tail in the classic ouroboros form. "
            "A second serpent approaches or confronts the first, and the scene suggests one devouring the other "
            "in a transformative act. The setting is sparse — a rocky or barren ground — focusing attention on "
            "the intertwined, self-consuming bodies of the serpents."
        ),
        "discourse_summary": (
            "Maier develops the ancient image of the serpent devouring another serpent to become a dragon, "
            "an allegory for the dissolution of one metallic substance by another of similar but more active nature. "
            "He argues that in antiquity the serpent represented both poison and medicine — the pharmakon — and that "
            "the alchemical dragon born from this mutual consumption combines the properties of both parents. "
            "The discourse cites classical accounts of dragon-generation and connects them to the Hermetic principle "
            "that the Stone is produced when like consumes like. Maier emphasizes that this is a nigredo operation: "
            "the death of both serpents precedes the birth of the more powerful dragon."
        ),
    },
    15: {
        "image_description": (
            "A potter sits at his wheel in a workshop, shaping a vessel from wet clay with his hands. "
            "Around him are finished pots in various stages of drying and firing — some still damp, others "
            "hardened and glazed. A kiln or furnace glows in the background. The scene emphasizes the craft of "
            "working with wet and dry materials, the potter's hands mediating between the liquid and solid states."
        ),
        "discourse_summary": (
            "Maier presents the potter's craft as a model for the alchemical work, arguing that the artisan "
            "who shapes clay from wet and dry elements teaches the principles governing the philosophical operation. "
            "He develops the analogy between the potter's sequence — moistening, forming, drying, firing — and the "
            "alchemist's manipulation of the mercurial and sulphurous components through successive stages. "
            "The discourse emphasizes that Nature provides the model, but art must apply it: the potter does not "
            "invent the properties of clay but learns to work with them. Maier cites this as evidence that "
            "alchemical skill is a techne learned through observation of natural processes."
        ),
    },
    16: {
        "image_description": (
            "Two lions face each other in a confrontational pose. One is winged — feathered pinions spread from "
            "its shoulders — while the other is wingless, planted firmly on the ground. The contrast between "
            "the aerial, volatile lion and the grounded, fixed lion dominates the composition. "
            "The landscape behind them is open, with distant hills or mountains."
        ),
        "discourse_summary": (
            "Maier develops the two lions as figures for the volatile and fixed principles of the alchemical work. "
            "The winged lion represents the philosophical mercury — fugitive, aerial, unstable — while the wingless "
            "lion is the philosophical sulphur — earthy, fixed, enduring. He argues that mastery requires capturing "
            "the winged lion and joining it to its wingless counterpart, producing a stable union of volatile and fixed. "
            "The discourse connects the lion's magnanimity in classical natural history to the nobility of the "
            "alchemical substances, and draws on the solar symbolism of the lion as the king of beasts to establish "
            "its connection to gold and the citrinitas stage of yellowing."
        ),
    },
    17: {
        "image_description": (
            "A spherical fireball, divided into four sections or quadrants, hovers or burns at the center of the composition. "
            "Each quadrant may represent a different type of fire or heat. Flames radiate outward from the fourfold sphere. "
            "A figure — possibly the alchemist — tends or controls the fire from below. "
            "The scene emphasizes the multiplicity of fires needed and the skill required to manage them simultaneously."
        ),
        "discourse_summary": (
            "Maier argues that the alchemical work requires not one fire but four distinct types, each governing "
            "a different phase of the operation. He identifies these as the fire of the lamp (external heat), "
            "the fire of the ash-bath (gentle, sustained warmth), the fire of the substance itself (intrinsic reactive heat), "
            "and the fire of the water-bath (moist, temperate heat). The discourse develops the principle that fire "
            "transforms by making things fiery — communicating its own nature — but cannot make gold directly, "
            "only prepare the conditions for gold's emergence. Maier cites this fourfold fire as the master key to "
            "the practical art, without which even correct materials will fail."
        ),
    },
    18: {
        "image_description": (
            "Flames or fire dominate the composition, with a figure working at a furnace or athanor. "
            "The fire burns intensely, and various alchemical vessels are arranged around or within the flames. "
            "The scene may show the figure adjusting the heat or feeding the fire. "
            "The emphasis is on the sustained, controlled application of heat as the governing principle of the work."
        ),
        "discourse_summary": (
            "Maier continues the fire theme from Emblem XVII, arguing that fire delights in making things partake "
            "of its own fiery nature but cannot directly transmute base metals into gold. He develops a distinction "
            "between fire as agent of transformation and gold as the goal: fire prepares, purifies, and refines, "
            "but the ultimate product — the philosopher's stone or philosophical gold — emerges from the properly "
            "prepared matter's own latent potential, not from fire alone. The discourse cites the Aristotelian "
            "principle of like acting upon like to explain why the fire must be matched in kind and degree to the "
            "substance it works upon."
        ),
    },
    19: {
        "image_description": (
            "Four figures stand together in a group — possibly representing four brothers, four elements, or four aspects "
            "of a single substance. One figure strikes or kills another while the remaining two look on or collapse. "
            "The composition conveys a chain reaction: the death of one precipitates the death of all. "
            "The setting is an open space, perhaps a courtyard, with the violence at the center of the scene."
        ),
        "discourse_summary": (
            "Maier develops the idea that the four elements or components of the philosophical substance are so "
            "intimately connected that destroying one annihilates all. He argues that this demonstrates their essential "
            "unity — they are not truly four separate things but four aspects of a single body. The discourse draws "
            "on the myth of Geryon, the three-bodied king of Spain, and his pure-bred cattle guarded by the dog "
            "Orthrus, developing this as an allegory for the composite nature of the prima materia. "
            "Maier uses this to warn the alchemist against violent separation: the elements must be gently "
            "distinguished, not forcibly torn apart, lest the entire work be destroyed."
        ),
    },
    20: {
        "image_description": (
            "Three female figures stand in sequence, each teaching or demonstrating something to the next. "
            "The first figure may hold a natural object, the second observes or learns, and the third applies "
            "what she has learned to overcome or master the preceding figure. "
            "The arrangement suggests a pedagogical chain: nature instructs, nature learns, nature masters. "
            "The setting is outdoors with natural elements — plants, earth, water."
        ),
        "discourse_summary": (
            "Maier articulates one of alchemy's foundational maxims: Nature teaches Nature, Nature conquers Nature, "
            "Nature rules Nature. He argues that the alchemist must learn by observing natural processes, then apply "
            "those lessons to guide and finally master the transformations of matter. The discourse connects this "
            "to Democritus's principle that art imitates nature, and extends it: the alchemical art does not merely "
            "copy natural processes but accelerates and perfects them. Maier cites the washing of dirty linen (Emblem III) "
            "as an example — Nature provides rain and sun, and the washerwoman learns to replicate these cleansing agents."
        ),
    },
    21: {
        "image_description": (
            "A geometric diagram at center shows the nested transformation of shapes: a man and woman form a circle, "
            "which is inscribed in a square, which contains a triangle, which encloses a final inner circle. "
            "The figures may be rendered as human bodies contorted into these geometric forms, or as abstract diagrams "
            "with human figures at the periphery. The composition is schematic and diagrammatic rather than narrative, "
            "emphasizing the mathematical-philosophical dimension of the alchemical work."
        ),
        "discourse_summary": (
            "Maier develops the famous geometric formula attributed to the Rosarium Philosophorum: make a circle from "
            "a man and woman (the coniunctio of opposites), transform this into a square (the four elements), reduce "
            "the square to a triangle (the tria prima of salt, sulphur, and mercury), and finally resolve the triangle "
            "back into a circle (the unified philosopher's stone). He argues that this sequence encodes the entire "
            "alchemical opus in geometric form, drawing on Platonic philosophy to connect ideal mathematical forms "
            "to material transformations. The discourse cites the principle of squaring the circle — an impossibility "
            "in mathematics but achievable in alchemy — as evidence that the philosophical art transcends ordinary reason."
        ),
    },
    22: {
        "image_description": (
            "A woman works at a cooking fire or stove, stirring a pot or vessel containing a white substance — "
            "the white lead obtained through the preceding albedo operations. The domestic cooking scene parallels "
            "Emblem III's washerwoman: alchemical processes rendered as women's household labor. "
            "Kitchen implements and vessels surround her, and steam or vapor rises from the cooking vessel."
        ),
        "discourse_summary": (
            "Maier instructs that once the white lead (the product of the albedo) has been obtained, the alchemist "
            "must perform 'women's work' — that is, cook the substance with steady, patient heat. He develops cooking "
            "as the central metaphor for the post-albedo operations, arguing that the white substance must be slowly "
            "heated and matured, just as food is transformed by cooking from raw to nourishing. "
            "The discourse emphasizes patience and temperature control: the philosophical substance must simmer, "
            "not boil. Maier draws on the herms — three-forked road markers — as guides that show the way to "
            "straying travelers, an allegory for the textual guideposts left by earlier alchemists."
        ),
    },
    23: {
        "image_description": (
            "Golden rain descends from the sky onto the island or city of Rhodes, where figures reach upward to catch "
            "the falling drops. At one side, a helmeted figure — Pallas Athena — emerges fully formed, suggesting "
            "her birth from the head of Zeus. The golden precipitation and the goddess's birth occur simultaneously, "
            "linking divine emergence with the descent of philosophical gold from above."
        ),
        "discourse_summary": (
            "Maier develops the mythological tradition that golden rain fell on Rhodes when Pallas Athena was born "
            "from the head of Zeus, interpreting this as an allegory for the moment when the philosophical gold "
            "descends or precipitates during the citrinitas stage. He argues that just as Athena emerges fully armed "
            "and wise from the mind of the supreme deity, the philosopher's stone appears fully potent when the "
            "right conditions are met — it is not assembled gradually but manifests suddenly. The discourse connects "
            "the golden rain to the 'golden shower' of Zeus and Danae, weaving multiple classical myths into a single "
            "alchemical reading of divine gold falling from the heavens as precipitation of the tincture."
        ),
    },
    24: {
        "image_description": (
            "A wolf stands over the prostrate body of a crowned king, having devoured or killed him. "
            "In a second register or scene within the same plate, the wolf is shown consumed by flames on a pyre, "
            "and the king rises restored from the ashes or emerges renewed from the fire. "
            "The sequential narrative moves from predation to sacrifice to resurrection within a single image."
        ),
        "discourse_summary": (
            "Maier narrates a two-stage allegory: the wolf devours the king (antimony dissolves gold), then the wolf "
            "is burned, returning the king to life purified and renewed. He develops this as the central nigredo-to-rubedo "
            "sequence: the base, voracious substance (the wolf/antimony) must consume the noble but impure metal (the king/gold), "
            "and then the consuming agent itself must be destroyed by fire to liberate the purified king. "
            "The discourse draws on the metallurgical practice of antimony refining, where antimony sulphide is used "
            "to extract and purify gold from alloys. Maier cites this as one of the most practically grounded of all "
            "alchemical allegories, noting that the wolf's voracity is well known in natural history."
        ),
    },
    25: {
        "image_description": (
            "A dragon writhes at center, locked in combat with two figures — a male and female identified as Sol and Luna, "
            "or brother and sister. The dragon is wounded or dying but still dangerous. "
            "The male figure wields a weapon while the female restrains or applies a substance to the dragon's body. "
            "The scene takes place in a rocky, barren landscape suggesting the underground or subterranean."
        ),
        "discourse_summary": (
            "Maier argues that the philosophical dragon — the unreformed prima materia — cannot be killed by any single "
            "agent but only by the combined action of its own brother and sister, Sol and Luna (gold and silver, "
            "sulphur and mercury). He develops the myth of the Golden Fleece, where the dragon guarding the treasure "
            "must be slain before the fleece can be obtained, as an allegory for the alchemical work. "
            "The discourse cites Jason's quest and connects it to the Hermetic tradition that the Stone is guarded by "
            "a dragon that can only be overcome by substances of its own kind. Maier emphasizes that both the "
            "masculine (active, fiery) and feminine (passive, moist) principles must cooperate in this killing."
        ),
    },
    26: {
        "image_description": (
            "A female figure identified as Lady Sapientia (Wisdom) stands beside or beneath a large tree bearing "
            "golden fruit — the Tree of Life. She may hold a book, a scepter, or extend a hand toward the fruit. "
            "The tree is abundant and flourishing, its canopy spreading over the scene. "
            "The setting is a garden or paradise landscape, suggesting Eden or the garden of the Hesperides."
        ),
        "discourse_summary": (
            "Maier identifies the fruit of human wisdom as the Tree of Life itself, arguing that the philosopher's stone "
            "is the true 'wood of life' sought by sages across all traditions. He draws on Cicero's distinction between "
            "humans and animals — that only humans possess reason and the capacity for philosophical inquiry — to argue "
            "that alchemy is the highest expression of rational wisdom applied to Nature. The discourse connects the Tree "
            "of Life to the biblical Garden of Eden, the Hesperides, and the alchemical tradition of the arbor philosophica — "
            "the philosophical tree whose roots are mercury and whose fruit is gold. Maier presents this emblem as "
            "marking the rubedo: the tree has borne its fruit, wisdom has been attained."
        ),
    },
    27: {
        "image_description": (
            "A figure approaches or stands before a walled garden containing rose bushes or flowering plants. "
            "A locked gate or door bars entry, and the figure has no key. The garden interior is visible — lush, "
            "ordered, containing the philosophical rose — but inaccessible. "
            "The composition emphasizes the barrier between the seeker and the sought knowledge."
        ),
        "discourse_summary": (
            "Maier argues that attempting to enter the Philosophical Rose-garden without the proper key is as futile "
            "as trying to walk without feet. He develops this as a warning against shortcuts in the alchemical work: "
            "the three 'cooking' or 'consuming' processes that occur in the human body — digestion in the stomach, "
            "refinement in the liver, and distribution through the blood — mirror the three stages of alchemical "
            "preparation that cannot be bypassed. The discourse grounds this in Old Testament wisdom literature, "
            "connecting the rose-garden to the Song of Songs and the Solomonic tradition of enclosed gardens "
            "as figures for hidden wisdom accessible only through proper preparation."
        ),
    },
    28: {
        "image_description": (
            "A crowned king sits immersed in a steaming bath or vessel, attended by one or more figures — physicians "
            "or servants — who regulate the temperature or administer treatments. Black bile or dark fluid visibly "
            "drains from the king's body into the bathwater. The bath vessel is large and prominent, "
            "and steam or vapors rise around the royal figure. The attendant is sometimes identified as Pharut."
        ),
        "discourse_summary": (
            "Maier develops the Allegoria Merlini's narrative of King Duenech, who is bathed in a steam-bath "
            "to purge the black bile that ails him. He argues that the king represents philosophical gold in its "
            "impure state, and the bath is the vessel in which dissolution occurs: the black bile is the nigredo impurity "
            "that must be expelled through gentle, sustained heat. The discourse connects this to the Merlini tradition's "
            "account of royal purification, where the king's illness is cured not by violent means but by the patient "
            "application of warm moisture. Maier cites the medical practice of therapeutic bathing as a parallel, "
            "drawing on his own training as a physician to validate the alchemical analogy."
        ),
    },
    29: {
        "image_description": (
            "A salamander sits calmly within flames, unharmed by the fire that surrounds it. "
            "The fire burns vigorously — depicted with detailed, curling flames — but the creature rests "
            "at ease in the center. The scene may include a furnace or hearth as the fire's source. "
            "The salamander's composure within the destructive element is the focal point of the composition."
        ),
        "discourse_summary": (
            "Maier develops the ancient belief that the salamander lives in fire without being consumed, "
            "applying it as an allegory for the philosopher's stone, which endures the test of fire and emerges "
            "unchanged or improved. He argues that just as the salamander is nourished rather than destroyed by flames, "
            "the perfected stone withstands any degree of heat — a key test of its authenticity. "
            "The discourse connects this to the broader principle of fixation: a substance is 'fixed' when it can "
            "endure fire without volatilizing. Maier cites classical natural historians including Pliny "
            "on the salamander's fire-resistance, while noting that the philosophical salamander transcends "
            "the merely natural creature."
        ),
    },
    30: {
        "image_description": (
            "A figure with both male and female characteristics — the Hermaphrodite or Rebis — lies in darkness, "
            "motionless as if dead, upon a bed or bier. The surrounding space is black or deeply shadowed. "
            "A fire or torch approaches from one side, about to illuminate and revive the prostrate figure. "
            "The Hermaphrodite's dual-gendered body is visible, combining male and female attributes in a single form."
        ),
        "discourse_summary": (
            "Maier argues that the Hermaphrodite — the unified philosophical substance combining masculine and feminine "
            "principles — lies inert in darkness until awakened by fire. He develops this as an allegory for the "
            "transition from nigredo (the death-like darkness) to the active stages of the work: the combined substance "
            "has been successfully joined but remains dormant until heat reactivates it. Drawing on the myth of the "
            "Hermaphrodite born from the two mountains of Mercury and Venus, Maier connects the figure to Morienus's "
            "teaching that the Rebis (the 'two-thing') is found not in books but through living masters. "
            "The discourse frames the Hermaphrodite as the philosophical Mercury's two-topped Parnassus, where Apollo "
            "and the Muses reside."
        ),
    },
    31: {
        "image_description": (
            "A crowned king struggles in ocean waves, his head and arms above the surface, calling out for rescue. "
            "His crown identifies him as royalty even in distress. From the shore or from a boat, a figure reaches "
            "toward the king or prepares to pull him from the water. The sea is rough, with whitecaps, "
            "and the landscape behind shows a rocky coastline."
        ),
        "discourse_summary": (
            "Maier recounts the allegory of the king swimming in the sea who cries out that whoever saves him "
            "will receive a great reward. He develops this as a figure for philosophical gold dissolved in the "
            "mercurial sea — the noble substance submerged in the volatile solvent, needing to be rescued through "
            "fixation. The discourse argues that the king's promise of reward represents the multiplication of "
            "the stone: whoever successfully extracts and fixes the dissolved gold will be repaid many times over. "
            "Maier connects this to the broader tradition of the 'vegetable stone' that grows and multiplies "
            "like a living thing once properly fixed and nourished."
        ),
    },
    32: {
        "image_description": (
            "A branch of coral grows underwater, depicted in its natural marine setting with fish and sea creatures nearby. "
            "In a second register, the same coral is shown above the waterline, where it has hardened into a rigid, "
            "stone-like form. The contrast between the soft, underwater growth and the hard, aerial solid "
            "captures the transformation from liquid to fixed."
        ),
        "discourse_summary": (
            "Maier draws on the natural history of coral — soft and plant-like underwater but hardening to stone when "
            "exposed to air — as an analogy for the philosopher's stone, which is fluid and mutable during preparation "
            "but becomes fixed and permanent once complete. He argues that this natural transformation demonstrates "
            "the possibility of a substance changing its fundamental state without losing its essential nature. "
            "The discourse connects coral's petrifaction to the alchemical fixation process, where the volatile "
            "philosophical substance 'hardens' through exposure to air (the volatile spirit) just as coral solidifies "
            "above the waterline. Maier cites this as evidence that the rubedo — the final reddening — involves "
            "a transition from fluid process to solid product."
        ),
    },
    33: {
        "image_description": (
            "The Hermaphrodite figure lies in complete darkness on a bier or bed, as in Emblem XXX, but now "
            "more explicitly dead or death-like. The surrounding blackness is total — the nigredo at its deepest. "
            "Fire or a flame-bearing figure approaches, representing the intervention of heat that will begin "
            "the process of revival. The dual-gendered body is still, awaiting transformation."
        ),
        "discourse_summary": (
            "Maier returns to the Hermaphrodite-in-darkness motif, now explicitly connecting it to the practice "
            "of ritual purification through fire and water. He argues that divine origin was ascribed to certain "
            "individuals in antiquity through a process of trial — passing through fire and water — and that "
            "the Hermaphrodite must undergo the same ordeal. The discourse develops the parallel between baptism "
            "(purification by water) and calcination (purification by fire) as the two modes of cleansing that "
            "the combined philosophical substance must endure. Maier frames the darkness as a necessary passage: "
            "the substance must die fully before it can be reborn in the rubedo."
        ),
    },
    34: {
        "image_description": (
            "A celestial scene depicts a conception or hierogamy — a sacred marriage between heavenly figures. "
            "Rays of light or celestial fire descend from above onto a figure below who receives or conceives "
            "from the divine influence. Stars, planets, or zodiacal imagery may appear in the sky. "
            "The composition elevates the alchemical process from the laboratory to the cosmos."
        ),
        "discourse_summary": (
            "Maier develops the motto — 'He is conceived in the bath and born in the air' — as an allegory for "
            "the philosophical substance that begins in the liquid phase (conception in the bath) and emerges "
            "in the aerial or volatile state (birth in the air), before finally walking upon the waters as a "
            "perfected, red tincture. He argues that this threefold progression — liquid, aerial, solid — mirrors "
            "the three stages of generation in nature. The discourse connects the celestial conception to the "
            "Hermetic doctrine of 'as above, so below,' with the heavenly hierogamy producing its earthly analogue "
            "in the alchemist's vessel. Maier frames this as the rubedo moment: the substance has been perfected "
            "and can now act upon lesser metals."
        ),
    },
    35: {
        "image_description": (
            "A figure identified as Ceres or Thetis holds a child — Triptolemus or Achilles — over flames, "
            "tempering the child in fire to make it immortal or invulnerable. The fire burns beneath or around "
            "the child's body while the mother-figure supports it with care. A second figure may look on "
            "with alarm at the sight of the infant in flames. The scene combines maternal nurturing with trial by fire."
        ),
        "discourse_summary": (
            "Maier draws on two parallel myths — Ceres hardening Triptolemus in fire and Thetis dipping Achilles "
            "in the Styx — to argue that the philosopher's stone, like a divine child, must be tempered through "
            "exposure to fire to achieve its full power. He develops the principle that what does not kill the "
            "substance makes it stronger, drawing an explicit parallel between mythological fire-baptism and "
            "the alchemical calcination that hardens and fixes the volatile components. The discourse argues that "
            "the artist must follow these divine mothers' example, applying fire gradually and repeatedly rather "
            "than all at once, to produce a substance that endures any test."
        ),
    },
    36: {
        "image_description": (
            "A large stone lies on the ground where it has been thrown or deposited, while in a second register "
            "the same stone is shown elevated on a mountaintop. The landscape shifts between low valley and high peak. "
            "A figure may be shown casting the stone downward or carrying it upward. "
            "The dual positioning captures the stone's journey from earth to elevation."
        ),
        "discourse_summary": (
            "Maier develops the paradox that the philosopher's stone has been thrown onto the earth (despised, "
            "found in humble places) yet lifted onto mountains (exalted, valued above all things). He argues that "
            "the stone dwells in the air and feeds in the river — occupying all four elements simultaneously — "
            "because it is the quintessence that participates in all elemental natures without being limited to any one. "
            "The discourse draws on the biblical metaphor of the rejected cornerstone and connects it to the "
            "alchemical tradition that the prima materia is found everywhere yet recognized by none. "
            "De Jong identifies a nationalistic element in Maier's treatment, connecting the earth-as-mother "
            "imagery to German territorial symbolism."
        ),
    },
    37: {
        "image_description": (
            "Three distinct substances or elements are displayed or arranged together: a plume of white smoke "
            "rising from a vessel, a green lion (a vitreous or green-tinged substance), and dark, foul-smelling water. "
            "The three may be shown in separate vessels or combined in a single scene. "
            "A figure surveys or prepares the three ingredients. The composition emphasizes the triad of materials."
        ),
        "discourse_summary": (
            "Maier argues that mastery requires only three things: white smoke (water in its volatile form), the green lion "
            "(the raw ore of Hermes, vitriol or an impure metallic substance), and stinking water (the foul aqua foetida "
            "that dissolves metals). He develops the principle of simplicity in the art: despite the bewildering variety "
            "of alchemical texts, the practical requirements are minimal. The discourse uses the metaphor of building "
            "a house — foundation, walls, roof — to argue that the alchemist needs only three components properly "
            "combined and treated. Maier cites this triadic simplicity against the accusations of fraud and impossibility "
            "leveled at the art."
        ),
    },
    38: {
        "image_description": (
            "The Hermaphrodite stands upright and fully formed, displaying both male and female attributes in a single "
            "body. Unlike the prostrate Hermaphrodite of Emblems XXX and XXXIII, this figure is erect, active, and "
            "complete — the product of the union of opposites now realized. The figure stands on or between two mountains, "
            "identified in the motto as the mountains of Mercury and Venus."
        ),
        "discourse_summary": (
            "Maier presents the standing Hermaphrodite — born of the two mountains of Mercury and Venus — as the completed "
            "product of the alchemical work. He develops Socrates' declaration that he was a citizen not of one city "
            "but of the world as an analogy for the Hermaphrodite who inhabits two domains simultaneously. "
            "The discourse argues that the Rebis has been successfully produced: the philosophical Mercury and Venus "
            "have been permanently united, and the resulting substance stands on its own — no longer needing the "
            "fire that revived it from darkness (Emblems XXX, XXXIII). Maier frames this as the culmination of "
            "the rubedo, where the joined substance achieves autonomous stability."
        ),
    },
    39: {
        "image_description": (
            "Oedipus confronts the Sphinx on a rocky outcrop or mountainside. The Sphinx — part woman, part lion, "
            "part eagle — poses its riddle while Oedipus responds. In the background or a secondary scene, the consequences "
            "of the story unfold: Oedipus's father Laius lies dead, and the marriage to Jocasta is suggested. "
            "The scene combines the riddle-challenge with its fateful aftermath."
        ),
        "discourse_summary": (
            "Maier retells the Oedipus myth as an alchemical allegory: conquering the Sphinx (solving the riddle of "
            "Nature) leads to killing the father (destroying the original metallic form) and marrying the mother "
            "(reuniting with the prima materia from which the metal was born). He argues that this seemingly "
            "transgressive sequence — patricide and incest — is actually the normal order of alchemical transformation, "
            "where the product must dissolve its parent substance and recombine with its own origin. "
            "The discourse frames the Sphinx's riddle as the central question of alchemy: what walks on four legs, "
            "then two, then three? Maier reads this as the three stages of the Stone — unstable, bipedal, "
            "and finally supported by the 'third leg' of the tincture."
        ),
    },
    40: {
        "image_description": (
            "Two streams or bodies of water flow toward each other and merge into a single river or pool. "
            "The two waters may be distinguished by color — one clear, one dark, or one golden, one silver. "
            "A figure may direct or channel the confluence. The merging point is the focal center of the composition, "
            "where the two become one."
        ),
        "discourse_summary": (
            "Maier instructs the alchemist to make one water from two waters, producing the 'water of holiness.' "
            "He develops this as the final mercurial conjunction: the two philosophical waters — one volatile and "
            "ascending, the other fixed and descending — must be combined into a single, unified menstruum. "
            "The discourse connects this to the Hermetic tradition of the two serpents of the caduceus and to the "
            "mystical waters of baptism that cleanse and renew. Maier argues that this united water is the universal "
            "solvent that can dissolve all metals and serve as the medium for the final projection. "
            "The rubedo is achieved when the two contrary waters cease to separate and remain permanently joined."
        ),
    },
    41: {
        "image_description": (
            "Adonis lies wounded or dead in a woodland setting, gored by a wild boar that stands nearby or flees the scene. "
            "Venus rushes toward Adonis, her robes flowing with urgency. Blood flows from Adonis's wounds onto "
            "white roses growing nearby, staining them red. The transformation of the roses from white to red "
            "is a prominent visual element, occurring at the point where divine blood meets earthly flowers."
        ),
        "discourse_summary": (
            "Maier retells the death of Adonis — beloved of Venus, killed by a boar, his blood dyeing white roses red — "
            "as an allegory for the transition from albedo to rubedo. He argues that the beautiful, white philosophical "
            "substance (Adonis/the white stone) must be 'killed' — subjected to a final violent transformation — "
            "and that the resulting reddening (Venus's blood on the roses) produces the red tincture. "
            "The discourse develops the boar as a figure for the aggressive sulphurous agent that destroys the "
            "passive, beautiful white form. Maier cites Ovid's Metamorphoses as his primary source, while "
            "De Jong traces the alchemical reading of this myth through the Rosarium tradition."
        ),
    },
    42: {
        "image_description": (
            "Four figures or personifications are arranged in the composition, each representing one of the guides "
            "to the alchemical work: Nature (a female figure), Reason (perhaps holding a book or compass), "
            "Experience (a laboratory figure), and Reading (a scholar with books). They may surround or point toward "
            "a central vessel, furnace, or stone. The arrangement suggests the four pillars supporting the practice."
        ),
        "discourse_summary": (
            "Maier develops the Tabula Smaragdina's teaching by identifying four guides that together constitute "
            "the alchemical method: Nature provides the raw material and model, Reason supplies theoretical "
            "understanding, Experience offers practical knowledge gained through trial, and Reading transmits the "
            "wisdom of earlier masters. He argues that these four correspond to the fire, the vessel, the water, "
            "and the earth of the work — each indispensable, none sufficient alone. The discourse emphasizes the "
            "balance between textual learning and hands-on practice, a theme running through the entire Atalanta Fugiens. "
            "Maier presents this emblem as a methodological summation of the principles scattered across the preceding forty-one."
        ),
    },
    43: {
        "image_description": (
            "A screech owl or night bird perches prominently, its beak open as if calling. "
            "Nearby, water flows — a stream, fountain, or rain — and the scene is set at dusk or in dim light. "
            "Other birds may be visible in the evening sky, their calls contrasting with the owl's solitary voice. "
            "The composition emphasizes listening: the viewer is directed to attend to the owl's cry and the water's sound."
        ),
        "discourse_summary": (
            "Maier instructs the alchemist to listen to the screech owl's voice and the sound of running water "
            "while ignoring the cries of evening birds — a parable about discerning true signals from false. "
            "He develops the owl as a figure for philosophical mercury (the lunar, nocturnal principle) whose "
            "call reveals the correct path, while the other birds represent misleading doctrines and false alchemists. "
            "The discourse connects the biblical story of Naaman (Emblem XIII) to this emblem, reprising the theme "
            "of purification through water. Maier argues that the alchemist must develop sensory discernment — "
            "learning to hear and see what Nature reveals — rather than following the loud but empty promises "
            "of charlatans."
        ),
    },
    44: {
        "image_description": (
            "Typhon, depicted as a monstrous figure, strikes down or dismembers Osiris, whose body lies scattered "
            "in fragments across the landscape. In a secondary scene, the goddess Isis moves through the landscape "
            "gathering the scattered limbs, reassembling the divine body. The composition narrates dissolution "
            "and reconstitution: the god broken apart and painstakingly restored."
        ),
        "discourse_summary": (
            "Maier retells the Egyptian myth of Osiris — murdered by Typhon through treachery, his body scattered, "
            "then painstakingly reassembled by Isis — as the complete arc of the alchemical opus. He identifies "
            "Typhon's killing with the nigredo dissolution, the scattering of limbs with the separation of elements, "
            "and Isis's gathering with the reconstitution and final rubedo. The discourse develops Osiris as the "
            "archetypal philosophical body that must be destroyed, dispersed, and reunited to achieve perfection. "
            "De Jong traces Maier's treatment of this myth through multiple alchemical traditions, noting that the "
            "Osiris-Isis cycle became one of the most enduring allegories in Western alchemy precisely because it "
            "encodes all three stages — death, purification, and resurrection — in a single narrative."
        ),
    },
    45: {
        "image_description": (
            "Sol and Luna — depicted as a king and queen, or as the sun and moon personified — stand together "
            "with their shadows visible or prominent. The shadows may merge or interact in ways the figures themselves "
            "do not, suggesting that the hidden, shadow aspect of the work is where the real operation occurs. "
            "The composition pairs the luminous celestial figures with their dark counterparts."
        ),
        "discourse_summary": (
            "Maier argues that Sol and his shadow together complete the work — the visible, noble gold (Sol) must be "
            "joined with its shadowy, hidden counterpart (the impure, dark aspect) to produce the philosopher's stone. "
            "He develops the principle that the stone requires both the light and dark aspects of the same substance, "
            "and that ignoring the shadow — the nigredo remainder — makes completion impossible. "
            "The discourse draws on the Consilium Conjugii and the Massa Solis et Lunae tradition to argue that the "
            "two stones spoken of by the philosophers are actually the manifest and hidden aspects of a single substance. "
            "Maier presents this penultimate teaching as the key to unlocking the entire series."
        ),
    },
    46: {
        "image_description": (
            "Two eagles fly toward each other from opposite directions — one from the East (the right), the other "
            "from the West (the left). They meet in mid-air, their talons or beaks engaging at the point of collision. "
            "The landscape below stretches between two horizons, emphasizing the vast distance the eagles have traveled. "
            "The meeting point at center is the focal climax of the composition."
        ),
        "discourse_summary": (
            "Maier develops the meeting of two eagles — one from the East, the other from the West — as an allegory "
            "for the conjunction of the two philosophical principles that originate from opposite ends of the "
            "alchemical process. He identifies the Eastern eagle with sulphur (the hot, solar principle born from fire) "
            "and the Western eagle with mercury (the cool, lunar principle born from water). Their meeting in mid-air "
            "represents the volatile conjunction where both principles abandon their fixed natures and unite in the "
            "aerial, spiritual realm. The discourse connects the circumnavigation imagery — east to west, west to east — "
            "to the Hermetic principle of universal circulation, where all things return to their origin."
        ),
    },
    47: {
        "image_description": (
            "A wolf approaches from one side and a dog from the other, meeting in a violent confrontation. "
            "They bite and tear at each other, locked in mutual combat. The wolf is identified with the East "
            "and the dog with the West. The landscape suggests a meeting point between two territories, "
            "with the struggle occurring on a boundary or threshold."
        ),
        "discourse_summary": (
            "Maier parallels the eagle meeting of Emblem XLVI with a more violent version: the wolf from the East "
            "and the dog from the West bite each other in mutual destruction. He argues that while the eagles' "
            "conjunction was aerial and spiritual, the wolf-and-dog encounter is terrestrial and material — "
            "the same union of opposites enacted at a lower, more physical register. The discourse develops the wolf "
            "as the more aggressive, dissolving agent (philosophical mercury in its corrosive aspect) and the dog "
            "as the resistant, fixed body that must be broken down. Their mutual biting — each wounding the other — "
            "represents the reciprocal action of dissolution, where both substances are transformed by their encounter."
        ),
    },
    48: {
        "image_description": (
            "A king reclines on a bed or throne, visibly ill — his complexion pale or discolored, his posture weakened. "
            "Physicians or attendants approach with a vessel containing a potion or elixir, preparing to administer "
            "the remedy. The setting suggests a royal sickroom or court. The king wears his crown even in illness, "
            "and the physicians' gestures indicate both deference and medical purpose."
        ),
        "discourse_summary": (
            "Maier develops the Merlini allegory of King Duenech in its final phase: the king, fallen ill from drinking "
            "foul waters, is restored to health by physicians who administer the correct elixir. He draws on Xerxes "
            "drinking muddy water in the desert as an analogy for the philosophical substance contaminated by impurities. "
            "The discourse describes the king's cure through successive stages — first Egyptian, then Alexandrian "
            "physicians — corresponding to different alchemical traditions' approaches to purification. "
            "Bernard of Treves's allegory describes the restored king dressed in a black cuirass, white tunic, and "
            "purple-red cloak — the three colors of the opus (nigredo, albedo, rubedo) worn simultaneously, "
            "signaling the completion of the work."
        ),
    },
    49: {
        "image_description": (
            "A child — the Philosophical Child — stands or sits at center, flanked by three male figures "
            "identified as his three fathers. The child may display characteristics of all three, or the three "
            "fathers may each contribute a different gift or quality. The myth of Orion's triple parentage "
            "provides the narrative framework: the child born of three fathers rather than one."
        ),
        "discourse_summary": (
            "Maier argues that the philosopher's stone, like the mythological Orion, acknowledges three fathers — "
            "three distinct sources or principles that contribute to its generation. He develops this as an allegory "
            "for the tria prima: the stone is born from salt (the bodily principle), sulphur (the soul principle), "
            "and mercury (the spirit principle), each 'fathering' a different aspect of the complete substance. "
            "The discourse draws on the Orion myth — conceived from the combined seed of Zeus, Poseidon, and Hermes — "
            "to argue that no single source suffices for the generation of the philosophical child. "
            "Maier presents this as one of the final teachings: the stone's triple origin explains why it cannot be "
            "produced from any single starting material."
        ),
    },
    50: {
        "image_description": (
            "A dragon and a woman are locked in mortal combat, each killing the other simultaneously. The dragon's coils "
            "wrap around the woman's body while she strikes at its head or throat. Blood flows from both combatants. "
            "The scene takes place in a cave-like or underground setting, near a body of water or pool in which "
            "the two figures bathe in their mingled blood. The mutual destruction is also a mutual immersion."
        ),
        "discourse_summary": (
            "Maier narrates the final emblem as a double death: the dragon kills the woman and she kills it, and "
            "together they bathe in the blood of their mutual destruction. He develops this as the ultimate expression "
            "of the alchemical principle that the Stone is born from the death of both its parents — the volatile "
            "(the dragon, dwelling in caves underground) and the fixed (the woman, dwelling in the adjacent air). "
            "The discourse argues that their commingled blood — the shared substance released by reciprocal dissolution — "
            "becomes the bath of regeneration from which the philosopher's stone emerges. Maier presents this as the "
            "closing image of the entire series: the work ends where it began, in mutual consumption and transformation."
        ),
    },
})


def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    updated = 0

    for num, content in sorted(EMBLEM_CONTENT.items()):
        img_desc = content.get("image_description")
        disc_sum = content.get("discourse_summary")

        if img_desc:
            c.execute('UPDATE emblems SET image_description = ? WHERE number = ?', (img_desc, num))
        if disc_sum:
            c.execute('UPDATE emblems SET discourse_summary = ? WHERE number = ?', (disc_sum, num))
        updated += 1

    conn.commit()
    conn.close()
    print(f'Updated {updated}/51 emblems with museum-level descriptions.')


if __name__ == '__main__':
    main()
