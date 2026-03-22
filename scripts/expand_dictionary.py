#!/usr/bin/env python3
"""
Expand dictionary entries in atalanta_fugiens_seed.json:
1. Add definition_long to all 38 existing dictionary entries
2. Add 35 new dictionary entries
"""
import json
import sys
from pathlib import Path

SEED_PATH = Path(__file__).parent.parent / "atalanta_fugiens_seed.json"

# ─── definition_long for all 38 existing terms ───────────────────────────────

DEFINITION_LONG = {
    "Coniunctio": (
        "Coniunctio oppositorum, the union of opposites, is the central operation of the alchemical Great Work "
        "in which complementary principles -- male and female, volatile and fixed, Sun and Moon -- are joined into "
        "a single perfected substance. In the Hermetic tradition, this union reflects the macrocosmic harmony of "
        "heaven and earth, and its achievement in the laboratory signifies the adept's mastery of nature's hidden "
        "symmetries. The coniunctio is typically represented as a royal marriage, a sexual embrace, or the fusion "
        "of two bodies into the hermaphrodite, and it is understood as the prerequisite for the appearance of the "
        "Philosopher's Stone."
    ),
    "Nigredo": (
        "Nigredo, the blackening, is the first and most dreaded stage of the alchemical opus, in which the "
        "starting material undergoes putrefaction, decomposition, and symbolic death. The adept observes the matter "
        "turning black in the vessel, a sign that the old form is being destroyed to release the hidden seed of new "
        "creation. Medieval and early modern alchemists associated nigredo with melancholy, Saturn, the grave, and "
        "the eclipse of the Sun, making it a rich site of psychological and spiritual as well as material symbolism. "
        "The successful passage through nigredo is the gateway to all subsequent stages of purification and perfection."
    ),
    "Albedo": (
        "Albedo, the whitening, is the second major stage of the opus in which the blackened matter of nigredo is "
        "washed, purified, and restored to a state of pristine whiteness. This stage is associated with the Moon, "
        "silver, baptism, and the dawn, and it signifies the removal of all impurities and the preparation of the "
        "matter to receive the final reddening. The imagery of washing, bleaching, and bathing pervades alchemical "
        "literature as figures for the albedo. In the color sequence of the Work, albedo represents the midpoint "
        "between death (nigredo) and perfection (rubedo)."
    ),
    "Citrinitas": (
        "Citrinitas, the yellowing, is an intermediate stage of the alchemical opus situated between albedo and "
        "rubedo, representing the vivification or dawning of the solar principle within the whitened matter. Many "
        "later alchemical authors collapsed this stage into rubedo, but earlier writers recognized it as a distinct "
        "moment when the matter begins to show signs of the golden color that will culminate in the final reddening. "
        "Citrinitas is associated with the first stirrings of life, the sunrise, and the transition from lunar to "
        "solar dominance within the vessel."
    ),
    "Rubedo": (
        "Rubedo, the reddening, is the final and culminating stage of the alchemical Great Work, in which the "
        "matter achieves its perfected state as the Philosopher's Stone or Red Elixir. The appearance of the red "
        "color in the vessel signals the successful completion of all prior stages and the attainment of the power "
        "to transmute base metals into gold. Rubedo is associated with the Sun, gold, the Phoenix, and the "
        "resurrection of the King, and it represents the fullest expression of the alchemical principle that nature "
        "can be perfected through art."
    ),
    "Mercurius": (
        "Mercurius Philosophorum, philosophical Mercury, is the volatile, feminine, lunar principle of alchemical "
        "theory, distinguished from common quicksilver by its status as the universal solvent and living spirit of "
        "metals. In the dual-principle system, Mercury represents the receptive, fluid, and transformable aspect of "
        "matter that must be fixed by Sulphur to produce the Stone. Mercury is figured as a fleeing maiden, a winged "
        "serpent, a dragon, or a fountain, and its capture and fixation constitutes the central drama of the Work. "
        "The term encompasses material, cosmological, and spiritual registers simultaneously."
    ),
    "Sulphur": (
        "Sulphur is the fixed, masculine, solar principle of alchemical theory, paired with Mercury as one of the "
        "two fundamental constituents of all metals. Where Mercury is volatile and lunar, Sulphur is stable and "
        "fiery, representing the active, coagulating force that gives metals their color and combustibility. In "
        "alchemical allegory, Sulphur appears as the King, the bridegroom, or the pursuer who must capture and fix "
        "the fleeing Mercury. The union of Sulphur and Mercury in proper proportion is the essential prerequisite "
        "for the production of the Philosopher's Stone."
    ),
    "Philosophical Egg": (
        "The Philosophical Egg, or Ovum Philosophicum, is the sealed vessel in which the prima materia undergoes "
        "the entire sequence of alchemical transformations, from nigredo through rubedo. Its egg shape symbolizes "
        "the unity of all opposites before differentiation, the microcosm containing the seed of the perfected "
        "Stone. The adept must regulate the heat applied to the egg with the same care a hen gives to incubating "
        "her clutch, neither too hot nor too cold. The egg thus serves as both a practical laboratory image and a "
        "cosmological symbol of creation from undifferentiated potential."
    ),
    "Philosopher's Stone": (
        "The Philosopher's Stone, Lapis Philosophorum, is the ultimate product of the alchemical Great Work: a "
        "perfected substance capable of transmuting base metals into gold and conferring health or immortality upon "
        "the adept. It is described as a paradoxical entity -- a stone that is not a stone, known to all yet "
        "recognized by none -- and its production requires the complete cycle of dissolution, purification, "
        "conjunction, and fixation. The Stone represents the convergence of material, medical, and spiritual "
        "perfection, and the entire alchemical emblem tradition can be understood as an attempt to encode the "
        "method of its preparation."
    ),
    "Putrefaction": (
        "Putrefaction, or putrefactio, is the controlled decomposition of the alchemical matter within the sealed "
        "vessel, corresponding to the nigredo stage and signifying the death of the old form that enables new "
        "creation. The adept deliberately allows the matter to rot, blacken, and dissolve, understanding this "
        "destruction as the necessary precondition for regeneration. Putrefaction is compared to the burial of a "
        "seed in earth, the death of a king, or the corruption of flesh, all of which must occur before new life "
        "can emerge. The operation requires patience, as premature intervention will abort the process."
    ),
    "Calcination": (
        "Calcination, or calcinatio, is the operation of heating a substance to high temperature to reduce it to "
        "ash or powder, burning away impurities and volatile components to leave a purified residue. In the "
        "symbolic vocabulary of alchemy, calcination represents the destruction of the gross material body to "
        "release the hidden spiritual essence within. It is closely associated with the purificatory operations "
        "of the albedo stage, where the blackened matter of nigredo is subjected to fire to prepare it for "
        "reconstitution. Calcination is often grouped with washing and dissolution as part of the broader complex "
        "of purification operations."
    ),
    "Coagulation": (
        "Coagulation, or coagulatio, is the operation of solidifying the volatile, fixing the dissolved or "
        "liquefied matter into a stable, permanent form. It is the complement and counterpart of dissolution: "
        "where dissolution breaks down the fixed, coagulation rebuilds from the volatile. In alchemical theory, "
        "one nature can only be coagulated through the simultaneous dissolution of another, establishing a "
        "reciprocal dynamic central to the logic of the Work. Coagulation is figured through images of curdling, "
        "freezing, crystallizing, and the solidification of smoke into stone."
    ),
    "Dissolution": (
        "Dissolution, or dissolutio, is the breaking down of solid matter into liquid, the release of the fixed "
        "into the volatile state. It is one of the most fundamental operations in alchemy, corresponding to the "
        "return of differentiated form to undifferentiated prima materia. Dissolution is both destructive and "
        "generative: it destroys the old form but liberates the hidden seed from which new, perfected matter can "
        "grow. The Turba Philosophorum teaches that all creation begins in liquefaction, making dissolution the "
        "starting point of every cycle of the Work."
    ),
    "Hermaphrodite": (
        "The Hermaphrodite, or Hermaphroditus, is the alchemical figure representing the perfect union of male "
        "and female principles in a single body, the embodied result of the coniunctio oppositorum. In alchemical "
        "iconography, the hermaphrodite appears as a two-headed or bisexual figure, combining the solar King and "
        "lunar Queen into an androgynous whole. This figure signifies that the Work has achieved the stable union "
        "of Sulphur and Mercury, volatile and fixed, and that the matter is approaching its final perfection. "
        "The hermaphrodite draws on the classical myth of Hermaphroditus and Salmacis as well as Platonic "
        "teachings on the original unity of the sexes."
    ),
    "Tabula Smaragdina": (
        "The Tabula Smaragdina, or Emerald Tablet, is a brief Hermetic text attributed to the legendary sage "
        "Hermes Trismegistus, containing the foundational axiom of alchemical cosmology: 'As above, so below.' "
        "Circulating in Latin translation from the twelfth century, the Tablet establishes the principle of "
        "correspondence between macrocosmic and microcosmic operations that underwrites the entire alchemical "
        "enterprise. Its terse, oracular language encodes the method of the Work in compressed symbolic form, "
        "and virtually every major alchemical author from the medieval period onward cites it as the supreme "
        "authority for the art."
    ),
    "Turba Philosophorum": (
        "The Turba Philosophorum, or Assembly of Philosophers, is a Latin translation of an Arabic alchemical "
        "compilation dating to approximately the ninth century, presenting alchemical doctrine as a series of "
        "speeches by ancient sages gathered in council. It is one of the most influential source texts in the "
        "Western alchemical tradition, providing teachings on dissolution, washing, the union of opposites, and "
        "the reciprocal destruction of contraries. The Turba's dialogic format allows multiple voices to elaborate "
        "on the same operations from different angles, creating a rich polyphony of symbolic perspectives that "
        "later authors like Maier could mine for motto material."
    ),
    "Rosarium Philosophorum": (
        "The Rosarium Philosophorum, or Rose Garden of Philosophers, is a major fourteenth-century alchemical "
        "compilation attributed to Pseudo-Arnald of Villanova, widely circulated as a compendium of practical and "
        "symbolic alchemical wisdom. It includes the famous series of woodcuts depicting the stages of the "
        "coniunctio, from the meeting of King and Queen through their death and resurrection as the hermaphrodite. "
        "The Rosarium also transmits the geometric circle-square-triangle formula and the sapiential-biblical "
        "framework linking alchemy to Solomonic wisdom. Its role as a mediating text between earlier sources and "
        "later authors makes it a central node in the transmission of alchemical knowledge."
    ),
    "Sapientia": (
        "Sapientia, or Wisdom personified, is the concept linking alchemical practice to the biblical and "
        "philosophical tradition of divine wisdom. In the alchemical reading, Sapientia is the tree of life "
        "described in Proverbs, whose fruit is the knowledge that transforms both the practitioner and the matter. "
        "This identification of alchemy with sacred wisdom elevates the art from mere metalworking to a form of "
        "contemplative practice, and it provides the religious justification for the adept's labors. The sapiential "
        "tradition within alchemy draws on the Aurora Consurgens, the Rosarium, and biblical wisdom literature."
    ),
    "Catena Aurea": (
        "The Catena Aurea, or Golden Chain, is the Hermetic concept of a continuous link connecting the lowest "
        "material realm to the highest divine principle, through which the influence of the celestial world flows "
        "downward into earthly matter and the products of the Work ascend toward perfection. Drawing on the "
        "Neoplatonic tradition of emanation and return, the golden chain figures the alchemical process as a "
        "participation in cosmic hierarchy rather than a merely local manipulation of substances. Each stage of "
        "the Work corresponds to a rung on this chain, linking the microcosm of the vessel to the macrocosm "
        "of the heavens."
    ),
    "Fugue": (
        "A fugue is a contrapuntal musical composition in which a short theme (subject) is introduced by one "
        "voice and then taken up by subsequent voices in overlapping entries, creating a texture of imitation and "
        "interweaving. In Atalanta Fugiens, each of the fifty emblems is accompanied by a three-voice fugue in "
        "which the voices allegorically represent Atalanta (the fleeing volatile), Hippomenes (the pursuing fixed "
        "principle), and the golden apple (the catalytic agent). This unprecedented integration of music into an "
        "emblem book makes the fugues not decorative accompaniment but a third symbolic register alongside image "
        "and text."
    ),
    "Tria Prima": (
        "The Tria Prima, or Three Principles, is the Paracelsian doctrine that all matter is composed of three "
        "fundamental principles: Mercury (spirit), Sulphur (soul), and Salt (body). This triad supplements the "
        "older dual-principle theory of Mercury and Sulphur by adding Salt as the principle of fixity and "
        "corporeality. The relationship of Maier's work to the Paracelsian tria prima is contested: Tilton argues "
        "that reducing the geometric formula of Emblem XXI to a straightforward Paracelsian reading misses "
        "Maier's deeper engagement with Aristotelian elemental transmutation."
    ),
    "King Duenech": (
        "King Duenech is an allegorical figure from medieval alchemical literature who suffers from a wasting "
        "melancholic disease -- identified variously with black bile, dropsy, or saturnine corruption -- that "
        "can only be cured through a sequence of purgative and restorative operations encoding the stages of the "
        "alchemical Work. His narrative derives from the Merlini Allegory, a medieval text in which the king's "
        "sickness, treatment, and restoration serve as an extended parable for the purification of base metal. "
        "The King Duenech cycle is one of the most sustained narrative sequences in the alchemical emblem "
        "tradition."
    ),
    "Ouroboros": (
        "The Ouroboros is the ancient symbol of a serpent or dragon devouring its own tail, representing eternal "
        "cyclical return, self-enclosed transformation, and the unity of beginning and end. In alchemical "
        "symbolism, it signifies the self-feeding nature of the Work, in which the product of each operation "
        "becomes the starting material for the next, and the end of the process returns to its beginning at a "
        "higher level of perfection. The ouroboros appears in Greek, Egyptian, and Gnostic sources before being "
        "adopted into the alchemical tradition as one of its most recognizable emblems."
    ),
    "White Lead": (
        "White Lead, or Plumbum Album, is a purified alchemical substance representing the product of the albedo "
        "stage: matter that has been washed, bleached, and reduced to a state of receptive whiteness. In the "
        "agricultural metaphor central to several emblems, white lead is the foliated earth into which the seed "
        "of gold must be sown to produce the final harvest of the Stone. The term bridges the gap between "
        "practical metallurgy (where lead compounds were well known) and symbolic alchemy (where whiteness "
        "signifies purification and readiness for the final reddening)."
    ),
    "Prima Materia": (
        "Prima Materia, the First Matter, is the undifferentiated, formless starting material from which all "
        "metals and the Philosopher's Stone itself arise. It is described paradoxically as being found everywhere "
        "yet recognized by none, cheap yet infinitely valuable, known by a thousand names yet essentially one. "
        "The identification of the prima materia is the first and most guarded secret of the alchemical art, "
        "since without the correct starting material no amount of skill can produce the Stone. Philosophically, "
        "the concept draws on Aristotelian hylomorphism, where prime matter is pure potentiality awaiting the "
        "imposition of form."
    ),
    "Lapis": (
        "Lapis, shorthand for Lapis Philosophorum or the Philosopher's Stone, is the perfected product of the "
        "alchemical Great Work, possessing the power to transmute base metals into gold and to heal all diseases. "
        "The Lapis is described as a paradox: a stone that is not a stone, fire that does not burn, water that "
        "does not wet. Its production requires mastery of all the stages of the Work, from nigredo through rubedo, "
        "and its achievement represents the culmination of the adept's knowledge and practice. The term is used "
        "interchangeably with Philosopher's Stone in most alchemical literature."
    ),
    "Aqua Vitae": (
        "Aqua Vitae, the Water of Life, is the purified mercurial water that dissolves impure matter and vivifies "
        "the dead body of the alchemical Work, serving simultaneously as solvent and elixir. In the medical "
        "register of alchemy, it is the curative draught administered to the sick King, restoring him to health "
        "and vigor. The concept bridges alchemical and medical practice, since the same substance that dissolves "
        "the impure also heals the diseased, reflecting the fundamental alchemical principle that the remedy and "
        "the poison are one. Aqua vitae is closely related to the mercurial fountain and the philosophical mercury."
    ),
    "Rex": (
        "The Rex, or King, is the central allegorical figure of alchemical literature representing Sol, gold, and "
        "the masculine fixed principle. In the narrative cycles of the Great Work, the King undergoes sickness, "
        "death, and resurrection, encoding the complete alchemical process in the form of a royal drama. His "
        "disease represents the impurity of unworked matter; his death corresponds to nigredo and putrefaction; "
        "and his resurrection in glory signifies the achievement of rubedo and the perfected Stone. The King is "
        "always paired with the Queen (Regina) as the necessary complement for the coniunctio."
    ),
    "Regina": (
        "The Regina, or Queen, is the feminine lunar counterpart to the King (Rex) in alchemical allegory, "
        "representing Luna, silver, and the volatile mercurial principle. Her role in the narrative of the Work "
        "is to provide the receptive, dissolving complement to the King's fixed solar nature, and their marriage "
        "constitutes the coniunctio that produces the hermaphrodite or the Stone. The Queen appears in the "
        "Rosarium Philosophorum woodcut series as a crowned figure who meets, embraces, copulates with, dies "
        "alongside, and is resurrected with the King in a sustained visual narrative of alchemical union."
    ),
    "Sol": (
        "Sol, the alchemical Sun, denotes gold as both a physical metal and a philosophical principle representing "
        "the masculine, active, fixed force in the Work. As a planet, Sol governs the solar operations of the "
        "opus and corresponds to the rubedo, the final reddening stage. As a substance, Sol is the noblest metal "
        "whose seed must be sown in prepared matter to produce the Stone. In the triadic correspondence system of "
        "alchemy, Sol operates simultaneously as metal, planet, and spiritual principle, and its light illuminates "
        "the entire chain of being from the celestial to the mineral realm."
    ),
    "Luna": (
        "Luna, the alchemical Moon, denotes silver as both a physical metal and a philosophical principle "
        "representing the feminine, receptive, volatile force in the Work. Luna is the nocturnal counterpart to "
        "Sol, governing the operations of dissolution and volatilization and corresponding to the albedo stage. "
        "In alchemical allegory, Luna appears as the Queen, the fleeing maiden, or the white dove, and her union "
        "with Sol in the coniunctio is the central event of the Great Work. Luna's mercurial nature links her "
        "to the philosophical Mercury as the universal solvent and receptive matrix."
    ),
    "Fixatio": (
        "Fixatio, or fixation, is the operation of rendering the volatile permanent and stable, preventing the "
        "mercurial spirit from escaping the vessel during heating. It is the essential counterpart to "
        "volatilization: where sublimation and distillation raise the subtle from the gross, fixation anchors "
        "the volatile in a stable material form. The entire allegorical structure of the Atalanta-Hippomenes "
        "pursuit can be read as a figure for fixation, in which the fixed Sulphur must capture and hold the "
        "fleeing Mercury. Without successful fixation, the Stone cannot be achieved."
    ),
    "Sublimatio": (
        "Sublimatio, or sublimation, is the operation of raising a substance from a gross, dense state to a "
        "subtle, elevated one through the application of heat, without passing through a liquid phase. In "
        "alchemical symbolism, sublimation represents the elevation of base matter toward its celestial archetype, "
        "the purification of the earthly through ascent. Winged figures, birds, smoke, and ascending flames all "
        "serve as images for sublimation in the emblem tradition. The operation is paired with fixation as "
        "complementary movements in the cyclic rhythm of the Work."
    ),
    "Multiplicatio": (
        "Multiplicatio, or multiplication, is the final augmentation of the Philosopher's Stone whereby its "
        "transmutative power is increased through repeated cycles of dissolution and reconstitution. Once the "
        "Stone has been achieved in its basic form, multiplication allows the adept to extend its capacity so "
        "that a small quantity can transmute a vastly larger quantity of base metal. This operation is figured "
        "through agricultural metaphors of sowing, harvesting, and replanting, and it represents the self-"
        "propagating nature of the perfected Stone."
    ),
    "Atalanta": (
        "Atalanta is the swift-footed maiden of Greek mythology who challenges her suitors to a footrace, killing "
        "those who lose, until Hippomenes defeats her by dropping golden apples given by Venus. In alchemical "
        "allegory, Atalanta represents the volatile mercurial principle that flees from the fixed Sulphur and can "
        "only be captured through cunning art rather than brute force. Maier makes her the titular figure of his "
        "entire work, and the three-voice fugues assign one voice to represent her flight. Her eventual capture "
        "and transformation into a lioness by Cybele completes the allegorical cycle from volatility to fixation."
    ),
    "Hippomenes": (
        "Hippomenes is the suitor who defeats Atalanta in the mythological footrace by casting golden apples to "
        "distract her, a stratagem given to him by Venus. In alchemical allegory, Hippomenes represents the fixed "
        "Sulphur or solar principle that must pursue and capture the volatile Mercury, using the golden apples of "
        "Art as catalytic agents. His success depends not on superior speed but on knowledge and technique, making "
        "him a figure for the disciplined alchemical adept. The three-voice fugues assign one voice to represent "
        "his pursuit, creating a musical enactment of the volatile-fixed dynamic."
    ),
    "Opus Magnum": (
        "The Opus Magnum, or Great Work, is the entire alchemical project of transmuting base matter into the "
        "perfected Philosopher's Stone, encompassing all stages from the initial identification of the prima "
        "materia through nigredo, albedo, citrinitas, and rubedo to the final multiplication. The term denotes "
        "both the practical laboratory sequence and the spiritual-philosophical journey of the adept, who is "
        "transformed alongside the matter in the vessel. The Great Work is simultaneously a metallurgical, "
        "medical, cosmological, and soteriological enterprise, reflecting the polyvalent nature of alchemical "
        "symbolism."
    ),
    "Vas Hermeticum": (
        "The Vas Hermeticum, or Hermetic Vessel, is the sealed container in which all alchemical transformations "
        "occur, named after Hermes Trismegistus who legendarily invented the technique of sealing a vessel with "
        "an airtight closure. The vessel must be perfectly sealed to prevent the loss of volatile spirits during "
        "the prolonged heating cycles of the Work, making its integrity the operational prerequisite for success. "
        "Symbolically, the Hermetic Vessel represents the enclosed, self-contained system of transformation, "
        "whether understood as the alchemist's flask, the philosophical egg, or the human body as vessel of "
        "spiritual transmutation."
    ),
    "Fermentatio": (
        "Fermentatio, or fermentation, is the penultimate operation of the alchemical Work in which a ferment "
        "or seed is introduced into the nearly completed Stone to activate its transmutative power. The operation "
        "is analogous to the leavening of bread, where a small quantity of active substance transforms a larger "
        "inert mass, or to the agricultural act of seeding prepared earth. Fermentation bridges the gap between "
        "the completion of the color stages (rubedo) and the final multiplication, introducing the living principle "
        "that enables the Stone to propagate its perfection."
    ),
}

# ─── 35 new dictionary entries ────────────────────────────────────────────────

NEW_ENTRIES = [
    # SOURCE_TEXT (12)
    {
        "term": "Aurora Consurgens",
        "category": "SOURCE_TEXT",
        "definition": "Late medieval alchemical text attributed to Pseudo-Aquinas, fusing Solomonic wisdom literature with alchemical symbolism through a Christological lens.",
        "latin": "Aurora Consurgens",
        "significance_to_af": "Maier accesses the Aurora Consurgens indirectly through the Rosarium Philosophorum, which transmits its sapiential-Christological reading of alchemy into the dense scriptural apparatus of Emblems XXVI and XXVII. De Jong identifies this text as a key source for the religious-philosophical dimension of Atalanta Fugiens.",
        "sources": ["de_jong_1969"],
        "related_emblems": ["XXVI", "XXVII"],
        "related_terms": ["Rosarium Philosophorum", "Sapientia", "Liber Sapientiae"]
    },
    {
        "term": "De Lapide Philosophico",
        "category": "SOURCE_TEXT",
        "definition": "Alchemical emblem book by Lambsprinck pairing symbolic engravings with verse explanations, a key prototype for the visual emblem tradition Maier inherits.",
        "latin": "De Lapide Philosophico",
        "significance_to_af": "De Jong and Pagel identify Lambsprinck's emblem book as a prototype for Maier's method of encoding alchemical doctrine in pictorial form, with Emblem VII's winged and wingless bird imagery drawing on a shared symbolic vocabulary of volatile and fixed principles.",
        "sources": ["de_jong_1969", "pagel_1973"],
        "related_emblems": ["VII"],
        "related_terms": ["Mercurius", "Sulphur", "Fugue"]
    },
    {
        "term": "Tractatulus de Practica Lapidis",
        "category": "SOURCE_TEXT",
        "definition": "Short Latin alchemical treatise falsely attributed to Aristotle, transmitted through the Artis Auriferae compilation. Source for elemental union imagery.",
        "latin": "Tractatulus de Practica Lapidis Philosophici",
        "significance_to_af": "De Jong identifies this pseudo-Aristotelian text as the direct motto source for Emblems IV and V, providing both the brother-sister marriage imagery and the toad suckling at the woman's breast. These emblems draw their central conceit of elemental union through mutual transformation from this text.",
        "sources": ["de_jong_1969"],
        "related_emblems": ["IV", "V"],
        "related_terms": ["Coniunctio", "Coagulation", "Dissolution"]
    },
    {
        "term": "Tabula Chimica",
        "category": "SOURCE_TEXT",
        "definition": "Latin translation of an alchemical work by Muhammad ibn Umail (Senior Zadith), containing visionary imagery of volatile and fixed principles as paired birds.",
        "latin": "Tabula Chimica",
        "significance_to_af": "De Jong traces the winged and wingless bird motif of Emblem VII directly to Senior Zadith's Tabula Chimica, where the two birds represent the volatile Mercury and fixed Sulphur that must be bonded. This source establishes the bird symbolism central to Maier's depiction of the volatile-fixed dynamic.",
        "sources": ["de_jong_1969"],
        "related_emblems": ["VII"],
        "related_terms": ["Mercurius", "Sulphur", "De Lapide Philosophico"]
    },
    {
        "term": "Metamorphoses",
        "category": "SOURCE_TEXT",
        "definition": "Ovid's Latin epic poem of mythological transformations, providing the Atalanta-Hippomenes narrative that Maier adopts as the overarching frame story for AF.",
        "latin": "Metamorphoses",
        "significance_to_af": "Maier draws the entire titular narrative of Atalanta Fugiens from Metamorphoses X.560-704, reading the footrace between Atalanta and Hippomenes as an alchemical allegory of the volatile-fixed dynamic. De Jong demonstrates that this Ovidian source is mediated through alchemical commentators like Robertus Vallensis.",
        "sources": ["de_jong_1969", "craven_1910"],
        "related_emblems": ["Frontispiece"],
        "related_terms": ["Atalanta", "Hippomenes", "Venus"]
    },
    {
        "term": "Allegoria Merlini",
        "category": "SOURCE_TEXT",
        "definition": "Medieval alchemical narrative in which a king suffering from a wasting disease is cured through purgative operations encoding the stages of the Work.",
        "latin": "Allegoria Merlini",
        "significance_to_af": "De Jong first analyzed this source in his 1964 article on Emblem XLVIII and expanded the treatment in the 1969 monograph, demonstrating that Maier draws the entire King Duenech narrative from this medieval tradition. The king's sickness and cure encode the alchemical process of purging impurities.",
        "sources": ["de_jong_1964", "de_jong_1969"],
        "related_emblems": ["XLVIII"],
        "related_terms": ["King Duenech", "Rex", "Putrefaction"]
    },
    {
        "term": "Ars Magna",
        "category": "SOURCE_TEXT",
        "definition": "The combinatorial art attributed to Ramon Llull, adapted by pseudo-Lullian alchemists into a framework for understanding dissolution and coagulation as reciprocal operations.",
        "latin": "Ars Magna",
        "significance_to_af": "De Jong identifies a thematic parallel between Emblem V and the Lullian teaching on dissolution and coagulation as reciprocal operations, transmitted through the Harmonica Chemica. This connection reinforces Maier's principle that one nature coagulates only through the dissolution of another.",
        "sources": ["de_jong_1969"],
        "related_emblems": ["V"],
        "related_terms": ["Coagulation", "Dissolution", "Tractatulus de Practica Lapidis"]
    },
    {
        "term": "Liber Sapientiae",
        "category": "SOURCE_TEXT",
        "definition": "The biblical Book of Wisdom (Wisdom of Solomon), part of the Solomonic tradition linking divine wisdom to alchemical knowledge.",
        "latin": "Liber Sapientiae",
        "significance_to_af": "De Jong demonstrates that the sapiential framework of Emblems XXVI and XXVII draws on the Solomonic wisdom tradition, where Wisdom as the tree of life is accessed through the Rosarium and the Aurora Consurgens. Maier uses this biblical authority to ground alchemy in sacred knowledge.",
        "sources": ["de_jong_1969"],
        "related_emblems": ["XXVI", "XXVII"],
        "related_terms": ["Sapientia", "Aurora Consurgens", "Rosarium Philosophorum"]
    },
    {
        "term": "De Veritate Artis Chemicae",
        "category": "SOURCE_TEXT",
        "definition": "Sixteenth-century treatise by Robertus Vallensis defending the antiquity and legitimacy of alchemy, including an allegorical reading of the Atalanta myth.",
        "latin": "De Veritate et Antiquitate Artis Chemicae",
        "significance_to_af": "De Jong identifies this text as a direct source for Maier's frontispiece commentary, where the race between Atalanta and Hippomenes is read as the pursuit of the volatile by the fixed principle. Vallensis provides the hermeneutic precedent for Maier's central allegorical conceit.",
        "sources": ["de_jong_1969"],
        "related_emblems": ["Frontispiece"],
        "related_terms": ["Atalanta", "Hippomenes", "Metamorphoses"]
    },
    {
        "term": "Secretum Nobilissimorum",
        "category": "SOURCE_TEXT",
        "definition": "Sixteenth-century alchemical text by Jodocus Greverus containing allegorical readings of classical myths as encoded alchemical teachings.",
        "latin": "Secretum Nobilissimorum",
        "significance_to_af": "De Jong identifies Greverus alongside Robertus Vallensis as a source for the frontispiece commentary of Atalanta Fugiens. Together these authorities establish the precedent for reading the Atalanta-Hippomenes myth as an allegory of the volatile-fixed dynamic in the Great Work.",
        "sources": ["de_jong_1969"],
        "related_emblems": ["Frontispiece"],
        "related_terms": ["De Veritate Artis Chemicae", "Atalanta", "Hippomenes"]
    },
    {
        "term": "Divinae Institutiones",
        "category": "SOURCE_TEXT",
        "definition": "Patristic work by Lactantius on divine wisdom and the nourishment of the soul, providing Christian authority for the identification of alchemy with sacred knowledge.",
        "latin": "Divinae Institutiones",
        "significance_to_af": "De Jong identifies Lactantius as one of the sources feeding into the scriptural apparatus of Emblem XXVI, where the concept of wisdom as food of the soul bridges Christian theology and alchemical practice. This patristic strand reinforces Maier's presentation of alchemy as legitimate religious knowledge.",
        "sources": ["de_jong_1969"],
        "related_emblems": ["XXVI"],
        "related_terms": ["Sapientia", "Liber Sapientiae", "Aurora Consurgens"]
    },
    {
        "term": "Fama Fraternitatis",
        "category": "SOURCE_TEXT",
        "definition": "First Rosicrucian manifesto (1614), announcing the Brotherhood of the Rose Cross and calling for a universal reformation of knowledge through alchemy and spiritual illumination.",
        "latin": "Fama Fraternitatis",
        "significance_to_af": "Tilton argues that Maier's Atalanta Fugiens responds directly to the Rosicrucian moment inaugurated by the Fama, and that Maier actively sought contact with the Brotherhood. While no emblem motto derives directly from the Fama, the manifesto provides the ideological framework within which Maier's synthesis becomes intelligible.",
        "sources": ["de_jong_1969", "tilton_2003"],
        "related_emblems": [],
        "related_terms": ["Opus Magnum", "Sapientia"]
    },
    # FIGURE (10)
    {
        "term": "Osiris",
        "category": "FIGURE",
        "definition": "Egyptian god of death and resurrection; in alchemical allegory, represents the solar principle that must be dismembered and reconstituted.",
        "latin": "Osiris",
        "significance_to_af": "Maier deploys Osiris in Emblem XLIV as the dying solar god whose dismemberment by Typhon and reassembly by Isis encodes the alchemical process of dissolution and reconstitution. De Jong reads this Egyptian myth as Maier's figure for the death and resurrection of the philosophical Sun.",
        "sources": ["de_jong_1969"],
        "related_emblems": ["XLIV"],
        "related_terms": ["Isis", "Typhon", "Sol", "Putrefaction"]
    },
    {
        "term": "Isis",
        "category": "FIGURE",
        "definition": "Egyptian goddess who reassembles the dismembered Osiris; represents the lunar anima that restores the dissolved solar principle to wholeness.",
        "latin": "Isis",
        "significance_to_af": "Maier presents Isis in Emblem XLIV as the feminine restorative principle who gathers the scattered parts of the slain Osiris, encoding the reintegration phase of the alchemical Work. De Jong connects this to the broader pattern of female figures in AF who preserve and reconstitute what the masculine principle alone cannot.",
        "sources": ["de_jong_1969"],
        "related_emblems": ["XLIV"],
        "related_terms": ["Osiris", "Typhon", "Luna", "Regina"]
    },
    {
        "term": "Typhon",
        "category": "FIGURE",
        "definition": "Egyptian destroyer who dismembers Osiris; represents the corrosive, fiery agent of dissolution that breaks down the old form.",
        "latin": "Typhon",
        "significance_to_af": "Maier uses Typhon in Emblem XLIV as the destructive agent who dismembers Osiris, representing the corrosive force of dissolution that must precede reconstitution. De Jong reads Typhon as Maier's figure for the fiery spirit that drives the nigredo, the necessary violence without which no renewal is possible.",
        "sources": ["de_jong_1969"],
        "related_emblems": ["XLIV"],
        "related_terms": ["Osiris", "Isis", "Nigredo", "Dissolution"]
    },
    {
        "term": "Adonis",
        "category": "FIGURE",
        "definition": "Dying god of vegetation beloved by Venus; represents the philosophical Sun that must die seasonally and be reborn through love's restorative power.",
        "latin": "Adonis",
        "significance_to_af": "Maier invokes Adonis as another instance of the dying-god pattern that structures the second half of Atalanta Fugiens, where the death and rebirth of the solar principle is dramatized through multiple mythological variants. De Jong connects the Adonis-Venus narrative to Maier's broader theme of death as the prerequisite for resurrection.",
        "sources": ["de_jong_1969"],
        "related_emblems": ["XLV"],
        "related_terms": ["Venus", "Osiris", "Sol", "Putrefaction"]
    },
    {
        "term": "Venus",
        "category": "FIGURE",
        "definition": "Goddess of love who provides the golden apples enabling Hippomenes to capture Atalanta; represents the catalytic feminine principle that makes union possible.",
        "latin": "Venus",
        "significance_to_af": "Maier places Venus in the frontispiece as the divine agent who provides Hippomenes with the golden apples, the catalytic device without which the pursuit of Mercury would be futile. De Jong reads Venus as Maier's figure for the art or technique that enables the adept to fix the volatile, making her the patron of the entire alchemical enterprise.",
        "sources": ["de_jong_1969"],
        "related_emblems": ["Frontispiece", "XLV"],
        "related_terms": ["Atalanta", "Hippomenes", "Adonis", "Coniunctio"]
    },
    {
        "term": "Oedipus",
        "category": "FIGURE",
        "definition": "Solver of the Sphinx's riddle; represents the alchemical adept who must decode nature's obscure language to proceed in the Work.",
        "latin": "Oedipus",
        "significance_to_af": "Maier presents Oedipus in Emblem XXXIX as the figure of the adept who must solve the riddle of nature, with the Sphinx's enigma standing for the obscurity of alchemical teaching. De Jong connects this to Maier's broader theme that the Work requires intellectual penetration of veiled symbolic language.",
        "sources": ["de_jong_1969"],
        "related_emblems": ["XXXIX"],
        "related_terms": ["Sphinx", "Sapientia", "Opus Magnum"]
    },
    {
        "term": "Sphinx",
        "category": "FIGURE",
        "definition": "Mythological guardian who poses riddles and destroys those who cannot answer; represents the obscurity of alchemical doctrine that tests the adept.",
        "latin": "Sphinx",
        "significance_to_af": "Maier uses the Sphinx in Emblem XXXIX as the guardian of alchemical secrets whose riddle must be solved before the adept can proceed. De Jong reads this as Maier's self-conscious commentary on the deliberately obscure language of alchemical tradition, where only the worthy can penetrate the veil of symbolism.",
        "sources": ["de_jong_1969"],
        "related_emblems": ["XXXIX"],
        "related_terms": ["Oedipus", "Sapientia"]
    },
    {
        "term": "Dragon",
        "category": "FIGURE",
        "definition": "Volatile spirit, guardian of treasure, and ouroboric figure of self-consuming transformation in alchemical iconography.",
        "latin": "Draco",
        "significance_to_af": "Maier deploys the dragon in Emblem L as the volatile principle that engages in mutual destruction with the woman, encoding the final dissolution that completes the Work. De Jong traces this image to the Turba Philosophorum's teaching on the reciprocal annihilation of contraries as the gateway to perfection.",
        "sources": ["de_jong_1969"],
        "related_emblems": ["L"],
        "related_terms": ["Ouroboros", "Mercurius", "Dissolution"]
    },
    {
        "term": "Latona",
        "category": "FIGURE",
        "definition": "Goddess identified with the impure base metal (laton/latten) that must be whitened; represents matter in its unworked, impure state.",
        "latin": "Latona",
        "significance_to_af": "Maier uses Latona in Emblem VI as a figure for the impure matter that must be washed and whitened before gold can be sown in it. De Jong connects the name Latona to the alchemical term laton (impure alloy), making her a mythological personification of the base material awaiting purification through the albedo.",
        "sources": ["de_jong_1969"],
        "related_emblems": ["VI"],
        "related_terms": ["Albedo", "White Lead", "Calcination"]
    },
    {
        "term": "Ceres",
        "category": "FIGURE",
        "definition": "Earth goddess of grain and nourishment; represents the maternal, nourishing principle that sustains the philosophical child through the stages of the Work.",
        "latin": "Ceres",
        "significance_to_af": "Maier invokes Ceres in connection with the nursing and nourishment imagery of the opening emblems, where the earth as nurse sustains the philosophical child. De Jong reads the agricultural goddesses in AF as figures for the receptive, fertile matter that nourishes the seed of gold toward its maturation.",
        "sources": ["de_jong_1969"],
        "related_emblems": ["I", "II"],
        "related_terms": ["Prima Materia", "Philosophical Egg", "Latona"]
    },
    # PROCESS (5)
    {
        "term": "Distillatio",
        "category": "PROCESS",
        "definition": "Separation of a substance by heating to vapor and condensing, purifying the volatile from the gross.",
        "latin": "Distillatio",
        "significance_to_af": "Maier incorporates distillation within the broader complex of purificatory operations depicted in the washing and heating emblems, where volatile spirits are separated from dense matter and recollected in purified form. De Jong connects this to the practical apparatus referenced in Emblem II's retort imagery.",
        "sources": ["de_jong_1969"],
        "related_emblems": ["II", "III"],
        "related_terms": ["Sublimatio", "Calcination", "Circulatio"]
    },
    {
        "term": "Projectio",
        "category": "PROCESS",
        "definition": "The final application of the perfected Stone onto base metal to effect transmutation; the culminating act of the Great Work.",
        "latin": "Projectio",
        "significance_to_af": "Maier treats projection as the ultimate telos of the fifty-emblem sequence, the moment when the perfected Stone is cast upon base metal to transmute it into gold. De Jong identifies this as the implied goal toward which the entire pedagogical program of Atalanta Fugiens converges.",
        "sources": ["de_jong_1969"],
        "related_emblems": ["L"],
        "related_terms": ["Philosopher's Stone", "Multiplicatio", "Rubedo"]
    },
    {
        "term": "Solutio",
        "category": "PROCESS",
        "definition": "Dissolving of a solid into liquid; the return of differentiated matter to a fluid, undifferentiated state.",
        "latin": "Solutio",
        "significance_to_af": "Maier figures solutio through the imagery of drowning, melting, and immersion that recurs across the emblem sequence, where solid forms must be returned to liquid before they can be reconstituted in perfected form. De Jong connects this to the Turba's teaching that the Work begins in liquefaction.",
        "sources": ["de_jong_1969"],
        "related_emblems": ["V", "L"],
        "related_terms": ["Dissolution", "Solve et Coagula", "Coagulation"]
    },
    {
        "term": "Circulatio",
        "category": "PROCESS",
        "definition": "Circular distillation in which the volatile is repeatedly raised and returned, purifying the matter through cyclical repetition.",
        "latin": "Circulatio",
        "significance_to_af": "Maier encodes circulatio in the geometric formula of Emblem XXI, where the circle symbolizes the completed cycle of operations that must be repeated until perfection is achieved. De Jong reads the circular imagery as Maier's figure for the iterative nature of the Work, where each cycle refines the matter further.",
        "sources": ["de_jong_1969"],
        "related_emblems": ["XXI"],
        "related_terms": ["Distillatio", "Sublimatio", "Multiplicatio"]
    },
    {
        "term": "Mortificatio",
        "category": "PROCESS",
        "definition": "The killing or death of the old form; the destruction of existing structure as prerequisite for renewal. Closely related to putrefaction and nigredo.",
        "latin": "Mortificatio",
        "significance_to_af": "Maier dramatizes mortificatio through the death scenes that pervade the second half of Atalanta Fugiens, including the death of Osiris (XLIV) and the mutual destruction of dragon and woman (L). De Jong reads these deaths as encoding the necessary destruction of the impure form before the perfected Stone can emerge.",
        "sources": ["de_jong_1969"],
        "related_emblems": ["XLIV", "L"],
        "related_terms": ["Putrefaction", "Nigredo", "Dissolution"]
    },
    # SUBSTANCE (5)
    {
        "term": "Aqua Regia",
        "category": "SUBSTANCE",
        "definition": "Royal water; the only solvent capable of dissolving gold, composed of nitric and hydrochloric acids. Symbol of the power to dissolve the noblest metal.",
        "latin": "Aqua Regia",
        "significance_to_af": "Maier references the concept of a universal solvent capable of dissolving even gold within the broader dissolution imagery of Atalanta Fugiens. De Jong connects this to the alchemical paradox that the most noble substance requires the most powerful agent of destruction before it can be reconstituted in perfected form.",
        "sources": ["de_jong_1969"],
        "related_emblems": [],
        "related_terms": ["Aqua Vitae", "Dissolution", "Sol"]
    },
    {
        "term": "Tinctura",
        "category": "SUBSTANCE",
        "definition": "The Tincture; the coloring agent of transmutation that imparts the golden or red color to base metal, synonymous with the perfected Stone in its active mode.",
        "latin": "Tinctura",
        "significance_to_af": "Maier treats the Tincture as the active principle of the perfected Stone, the agent that colors base metal into gold just as a dye transforms white cloth. De Jong connects this to the dyeing metaphor of Emblem III, where the washing and bleaching operations prepare matter to receive the final tincture.",
        "sources": ["de_jong_1969"],
        "related_emblems": ["III"],
        "related_terms": ["Philosopher's Stone", "Rubedo", "Projectio"]
    },
    {
        "term": "Elixir",
        "category": "SUBSTANCE",
        "definition": "The perfected medicine capable of healing all disease and transmuting metals; synonymous with the Philosopher's Stone in its medicinal aspect.",
        "latin": "Elixir",
        "significance_to_af": "Maier's depiction of the curative potion administered to King Duenech in Emblem XLVIII encodes the Elixir as the perfected alchemical medicine. De Jong and Pagel both emphasize the medical dimension of AF where the Elixir bridges alchemical transmutation and therapeutic practice.",
        "sources": ["de_jong_1969", "pagel_1973"],
        "related_emblems": ["XLVIII"],
        "related_terms": ["Philosopher's Stone", "Aqua Vitae", "King Duenech"]
    },
    {
        "term": "Aurum Philosophicum",
        "category": "SUBSTANCE",
        "definition": "Philosophical gold; not common gold but the perfected substance produced by the Work, embodying the solar principle in its highest form.",
        "latin": "Aurum Philosophicum",
        "significance_to_af": "Maier consistently distinguishes between common gold and philosophical gold throughout Atalanta Fugiens, particularly in Emblem VI where the gold sown in white earth is the seed of the philosophical rather than the metallic variety. De Jong traces this distinction to the Rosarium tradition where philosophical gold is the product of art perfecting nature.",
        "sources": ["de_jong_1969"],
        "related_emblems": ["VI", "XXI"],
        "related_terms": ["Sol", "Philosopher's Stone", "Lapis"]
    },
    {
        "term": "Rebis",
        "category": "SUBSTANCE",
        "definition": "The 'two-thing' (res bina); the reunited opposites in a single substance, combining masculine and feminine, fixed and volatile in stable union.",
        "latin": "Rebis",
        "significance_to_af": "Maier presents the Rebis through the hermaphrodite emblems (XXXIII, XXXIV, XXXVIII), where the two-in-one figure represents the successful reunion of opposites into a stable compound. De Jong reads the Rebis as the intermediate product of the coniunctio that must undergo further operations to become the perfected Stone.",
        "sources": ["de_jong_1969"],
        "related_emblems": ["XXXIII", "XXXIV", "XXXVIII"],
        "related_terms": ["Hermaphrodite", "Coniunctio", "Philosopher's Stone"]
    },
    # CONCEPT (3)
    {
        "term": "Solve et Coagula",
        "category": "CONCEPT",
        "definition": "Dissolve and coagulate; the fundamental binary rhythm of the alchemical Work, alternating between breaking down and building up.",
        "latin": "Solve et Coagula",
        "significance_to_af": "Maier encodes the solve et coagula rhythm throughout Atalanta Fugiens, from the reciprocal dissolution-coagulation of Emblem V to the final mutual destruction of Emblem L. De Jong identifies this alternating pattern as the structural principle governing the progression of the entire emblem sequence.",
        "sources": ["de_jong_1969"],
        "related_emblems": ["V", "L"],
        "related_terms": ["Dissolution", "Coagulation", "Solutio"]
    },
    {
        "term": "Cauda Pavonis",
        "category": "CONCEPT",
        "definition": "The Peacock's Tail; an iridescent display of colors appearing in the vessel during the transitional stage between nigredo and albedo, signaling that transformation is underway.",
        "latin": "Cauda Pavonis",
        "significance_to_af": "Maier alludes to the color transformations within the vessel across the emblem sequence, with the peacock's tail representing the intermediate moment when the black matter begins to show the full spectrum of colors before resolving into white. De Jong notes this transitional phenomenon as part of Maier's color symbolism linking the stages of the opus.",
        "sources": ["de_jong_1969"],
        "related_emblems": [],
        "related_terms": ["Nigredo", "Albedo", "Citrinitas"]
    },
    {
        "term": "Pelicanus",
        "category": "CONCEPT",
        "definition": "The Pelican vessel, a circulatory apparatus in which distillate flows back onto the matter below; also the symbol of self-sacrifice and self-nourishment.",
        "latin": "Pelicanus",
        "significance_to_af": "Maier draws on the pelican as both a practical vessel type and a Christological symbol of self-sacrifice, where the bird that feeds its young with its own blood parallels the alchemical matter that dissolves and reconstitutes itself. De Jong connects this to the broader theme of circulatio in AF where the Work feeds upon itself.",
        "sources": ["de_jong_1969"],
        "related_emblems": [],
        "related_terms": ["Circulatio", "Vas Hermeticum", "Ouroboros"]
    },
]


def main():
    # Load existing data
    with open(SEED_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    entries = data["dictionary_entries"]
    existing_terms = {e["term"] for e in entries}

    print(f"Existing dictionary entries: {len(entries)}")

    # 1. Add definition_long to existing entries
    updated_count = 0
    for entry in entries:
        term = entry["term"]
        if term in DEFINITION_LONG:
            entry["definition_long"] = DEFINITION_LONG[term]
            updated_count += 1
        else:
            print(f"  WARNING: No definition_long for existing term: {term}")

    print(f"Added definition_long to {updated_count} existing entries")

    # 2. Add 35 new entries (skip any duplicates)
    added_count = 0
    for new_entry in NEW_ENTRIES:
        if new_entry["term"] in existing_terms:
            print(f"  SKIP duplicate: {new_entry['term']}")
            continue
        entries.append(new_entry)
        existing_terms.add(new_entry["term"])
        added_count += 1

    print(f"Added {added_count} new entries")
    print(f"Total dictionary entries: {len(entries)}")

    # 3. Write back
    with open(SEED_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # 4. Validate by re-reading
    with open(SEED_PATH, "r", encoding="utf-8") as f:
        validated = json.load(f)

    v_entries = validated["dictionary_entries"]
    print(f"\nValidation: {len(v_entries)} dictionary entries in file")

    # Check all expected terms
    v_terms = {e["term"] for e in v_entries}
    for dl_term in DEFINITION_LONG:
        if dl_term not in v_terms:
            print(f"  MISSING existing term: {dl_term}")
    for ne in NEW_ENTRIES:
        if ne["term"] not in v_terms:
            print(f"  MISSING new term: {ne['term']}")

    # Check definition_long on existing
    for e in v_entries:
        if e["term"] in DEFINITION_LONG and "definition_long" not in e:
            print(f"  MISSING definition_long: {e['term']}")

    print("\nDone. JSON is valid.")


if __name__ == "__main__":
    main()
