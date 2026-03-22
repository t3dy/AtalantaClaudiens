"""
seed_registers.py — Populate the `registers` JSON column on dictionary_terms.

De Jong's key insight: alchemical terms operate simultaneously across 4 registers:
  - alchemical (material/laboratory)
  - medical (humoral/healing)
  - spiritual (soul/psyche)
  - cosmological (planetary/macrocosm)

Populates registers for PROCESS, SUBSTANCE, qualifying FIGURE, and qualifying CONCEPT terms.
Skips SOURCE_TEXT terms (book titles) and non-polysemous entries.

Idempotent: overwrites existing registers data on re-run.
"""

import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "atalanta.db"


# ── Register definitions ─────────────────────────────────────────────────────
# Each entry: slug -> {alchemical, medical, spiritual, cosmological}
# Voice: scholarly but concise, 1-2 sentences per register.
# Grounded in De Jong's analysis of Maier's Atalanta Fugiens.

REGISTERS = {
    # ═══════════════════════════════════════════════════════════════════════════
    # PROCESS TERMS (18)
    # ═══════════════════════════════════════════════════════════════════════════
    "nigredo": {
        "alchemical": "The blackening stage: putrefaction and decomposition of matter in the sealed vessel, producing a foul-smelling black mass that signals the work has begun.",
        "medical": "Corresponds to melancholia and black bile in humoral theory; the saturnine temperament whose leaden darkness must be purged before healing.",
        "spiritual": "The dark night of the soul: ego-death and psychological dissolution that precedes spiritual rebirth and illumination.",
        "cosmological": "Saturn's dominion over the prima materia; the chaos and formlessness from which cosmic order must be extracted, associated with winter and the nadir."
    },
    "albedo": {
        "alchemical": "The whitening: purification of the black mass through washing and sublimation, yielding a pure white earth or powder—the stage of purificatio.",
        "medical": "Restoration of phlegmatic balance; the cleansing of corrupt humors and return to a state of bodily purity, analogous to convalescence.",
        "spiritual": "Illumination after the dark night: the purified soul perceives spiritual light, achieving clarity and the dawn of higher consciousness.",
        "cosmological": "The Moon's dominion; the reflective feminine principle that receives and transmits celestial light, associated with silver and nocturnal dew."
    },
    "citrinitas": {
        "alchemical": "The yellowing: a transitional phase between albedo and rubedo where the white matter takes on a golden hue, signaling the approach of perfection.",
        "medical": "Associated with yellow bile and the choleric temperament in its constructive aspect—vital heat that drives metabolism and bodily vigor.",
        "spiritual": "The dawning of solar consciousness; wisdom emerging between the passive receptivity of albedo and the full realization of rubedo.",
        "cosmological": "The dawn and the rising sun; the transitional moment when lunar silver yields to solar gold in the celestial cycle."
    },
    "rubedo": {
        "alchemical": "The reddening: final stage where the white stone is tinged to red through fermentation with gold, producing the Philosopher's Stone or Red Tincture.",
        "medical": "The sanguine temperament perfected; full vitality, robust health, and the balanced circulation of life-giving blood through the body.",
        "spiritual": "The sacred marriage of soul and body achieved; full individuation, wholeness, and the philosopher's union with the divine ground.",
        "cosmological": "The Sun's dominion and the completion of the cosmic cycle; gold as the perfected metal reflecting the eternal and immutable light of the fixed stars."
    },
    "calcination": {
        "alchemical": "Heating the base matter to extreme temperatures to reduce it to powder or calx, driving off volatile components and exposing the fixed salt.",
        "medical": "The burning away of disease and corrupt matter; cauterization and the application of intense remedial heat to purge infection.",
        "spiritual": "The burning away of ego-attachments and worldly illusions; the trial by fire that strips the soul down to its essential, incombustible core.",
        "cosmological": "The action of celestial fire on terrestrial matter; the solar principle's consuming power that reduces gross forms to their elemental substrate."
    },
    "coniunctio": {
        "alchemical": "The chemical wedding of Sulphur and Mercury—the union of the red king and white queen in the sealed vessel to produce the hermaphroditic Rebis.",
        "medical": "The rebalancing of contrary humors into harmonious proportion; the therapeutic union of hot and cold, moist and dry principles within the body.",
        "spiritual": "The sacred marriage of opposites within the psyche—conscious and unconscious, masculine and feminine—producing wholeness and inner unity.",
        "cosmological": "The conjunction of Sol and Luna, the great celestial marriage whose earthly reflection governs generation and the harmony of macrocosm and microcosm."
    },
    "dissolution": {
        "alchemical": "Dissolving the calcined matter in the mercurial water; the body is liquefied so that its hidden seed may be released from the fixed matrix.",
        "medical": "The therapeutic dissolving of calcified obstructions and hardened humoral deposits; restoring fluidity to the body's circulatory economy.",
        "spiritual": "The dissolution of rigid psychic structures; the letting go of fixed identities and beliefs that obstruct the flow of inner transformation.",
        "cosmological": "Water's primordial action on earth; the lunar solvent that returns differentiated forms to the undifferentiated ocean of potentiality."
    },
    "sublimatio": {
        "alchemical": "Raising volatile spirits from gross matter through heat; the purified essence ascends and condenses on the upper walls of the vessel.",
        "medical": "The refinement of crude bodily spirits into subtle vital pneuma; the upward movement of healing vapors in steam baths and fumigations.",
        "spiritual": "The elevation of consciousness from base material concerns to refined spiritual perception; the ascent of the soul toward the divine.",
        "cosmological": "The ascent of earthly vapors to become celestial dew and rain; the vertical axis connecting earth to heaven in the cosmic circulatory system."
    },
    "putrefaction": {
        "alchemical": "Controlled decomposition of sealed matter producing the characteristic black color of nigredo; the death that is prerequisite to all alchemical generation.",
        "medical": "Analogous to the suppuration of wounds and the crisis of fever—the body's purgative destruction of corrupt matter that must precede healing.",
        "spiritual": "The mortification of the old self; the necessary rotting away of prior identity so that the seed of the new spiritual life may germinate.",
        "cosmological": "The universal law that generation proceeds from corruption, as in the Aristotelian cycle of growth and decay governing all sublunary nature."
    },
    "coagulation": {
        "alchemical": "The fixing and solidifying of volatile matter into stable form; the dissolved components reunite into a new, permanent body—the Stone.",
        "medical": "The restoration of firm bodily substance from dissolved or weakened states; the clotting and consolidation that restores structural integrity.",
        "spiritual": "The embodiment of spiritual insight in stable, lived practice; the crystallization of illumination into enduring character and wisdom.",
        "cosmological": "The cosmic principle by which formless potentiality congeals into manifest creation; the earth-principle that gives permanence to celestial influences."
    },
    "solutio": {
        "alchemical": "The dissolving of solid matter into liquid form using the philosophical mercury; the body must be reduced to its primordial water before reconstitution.",
        "medical": "The liquefaction of hardened deposits and obstructions in the body; restoring the natural flow of humors through dissolution of morbid concretions.",
        "spiritual": "The melting of the hardened heart; emotional release and the surrender of rigid ego-structures to the transformative waters of the unconscious.",
        "cosmological": "The universal solvent principle, the action of the primordial waters from which all forms originally emerged and to which they cyclically return."
    },
    "circulatio": {
        "alchemical": "The repeated distillation and recombination of volatile and fixed components in a sealed vessel, refining the matter through iterative cycles.",
        "medical": "The circulation of blood and vital spirits through the body; the continuous cycle of nourishment, purification, and renewal that sustains life.",
        "spiritual": "The iterative deepening of self-knowledge through repeated cycles of dissolution and reintegration; the spiral path of spiritual maturation.",
        "cosmological": "The great circulation of celestial influences from heaven to earth and back; the Hermetic cycle linking macrocosm and microcosm in perpetual exchange."
    },
    "distillatio": {
        "alchemical": "Separation of volatile essence from gross residue through heating and condensation; the collection of purified spirit in the receiving vessel.",
        "medical": "The extraction of medicinal essences and tinctures from raw plant or mineral matter; the preparation of refined remedies from crude substances.",
        "spiritual": "The careful extraction of essential meaning from the mass of life experience; the distillation of wisdom from the raw material of suffering.",
        "cosmological": "The celestial distillation by which solar heat draws moisture upward to form clouds, returning it as purified rain—nature's alembic."
    },
    "fermentatio": {
        "alchemical": "The leavening of the white stone with a small quantity of gold or its ferment, initiating the final transformation toward the Red Tincture.",
        "medical": "Analogous to the digestive ferment that transforms food into nourishment; the vital leaven that activates the body's regenerative processes.",
        "spiritual": "The catalytic encounter with a living spiritual tradition or teacher that activates latent potential; the yeast of grace working in the soul.",
        "cosmological": "The generative ferment implanted by the Creator in all of nature; the seminal principle that drives cosmic becoming and the multiplication of forms."
    },
    "fixatio": {
        "alchemical": "Rendering volatile matter stable and resistant to fire; the spirit is permanently bound to the body so it can no longer escape through heating.",
        "medical": "The stabilization of volatile symptoms and humoral imbalances; making a cure permanent rather than merely suppressing recurring disease.",
        "spiritual": "The permanent anchoring of spiritual realization in embodied life; ensuring that transcendent insight does not evaporate when the adept returns to daily existence.",
        "cosmological": "The principle of cosmic fixity: the immovable center around which the celestial spheres rotate, the axis mundi that grounds the turning heavens."
    },
    "mortificatio": {
        "alchemical": "The killing of the metal: stripping the base substance of its original form and properties through corrosion, so that it may receive a higher nature.",
        "medical": "The destruction of diseased tissue through caustic remedies; the surgeon's necessary violence that removes corruption to save the patient.",
        "spiritual": "The mortification of the flesh and ego; the ascetic killing of worldly desires that the soul may be liberated from its bondage to matter.",
        "cosmological": "The death phase in the cosmic cycle of death and rebirth; winter's killing frost that is the necessary precondition for spring's regeneration."
    },
    "multiplicatio": {
        "alchemical": "The augmentation of the Stone's potency through repeated cycles of dissolution and coagulation, increasing its power to transmute ever greater quantities of base metal.",
        "medical": "The amplification of a remedy's efficacy through careful preparation and potentiation; a small quantity of perfected medicine healing many patients.",
        "spiritual": "The multiplication of spiritual gifts: as the adept's realization deepens, its transformative influence radiates outward to benefit others.",
        "cosmological": "The principle of cosmic abundance: from the One proceed the many; the fecundity of nature that generates infinite diversity from a single divine seed."
    },
    "projectio": {
        "alchemical": "The final act: casting a small quantity of the perfected Stone onto molten base metal, transmuting it instantly into gold or silver.",
        "medical": "The application of the perfected elixir to the sick body, effecting immediate and complete cure—the projection of health onto disease.",
        "spiritual": "The moment of realized action: projecting inner transformation outward into the world, where the philosopher's perfected nature transmutes all it touches.",
        "cosmological": "The emanation of divine creative power into the material world; the projection of celestial form onto terrestrial matter that sustains all generation."
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # SUBSTANCE TERMS (12)
    # ═══════════════════════════════════════════════════════════════════════════
    "mercurius": {
        "alchemical": "The philosophical Mercury: not common quicksilver but the universal solvent and volatile principle—the moist, cold, feminine component of the metallic dyad.",
        "medical": "The vital spirit or pneuma that circulates through the body; the mercurial principle governing nerve function, respiration, and the subtle fluids.",
        "spiritual": "The anima or world-soul; the mediating spirit that connects body and soul, matter and intellect—Hermes as psychopomp guiding transformation.",
        "cosmological": "The planet Mercury as cosmic messenger between Sun and Moon; the principle of mediation and communication linking all levels of the great chain of being."
    },
    "sulphur": {
        "alchemical": "The philosophical Sulphur: the hot, dry, masculine, combustible principle in metals—the active seed that gives form and color to the metallic body.",
        "medical": "The vital heat or innate calor that drives digestion, growth, and generation; the choleric fire that, in proper measure, sustains bodily life.",
        "spiritual": "The soul's desire and will; the active, formative principle of consciousness that shapes raw experience into meaning and purpose.",
        "cosmological": "The solar and fiery principle; Sulphur corresponds to the Sun's generative heat that activates all earthly matter through its formative rays."
    },
    "sol": {
        "alchemical": "Gold in its philosophical sense: the perfect, incorruptible metal whose seed must be extracted and multiplied to produce the Philosopher's Stone.",
        "medical": "The heart as the body's sun; the vital center radiating life-giving warmth and sanguine vitality to every organ through arterial circulation.",
        "spiritual": "The illuminated consciousness; the divine spark or inner gold that the Great Work seeks to reveal beneath the dross of unrefined nature.",
        "cosmological": "The Sun as sovereign of the planetary hierarchy; source of all light, heat, and generative power in the macrocosm, father of the alchemical dyad."
    },
    "luna": {
        "alchemical": "Silver in its philosophical sense: the receptive, reflective metal that must be conjoined with Sol to achieve the complete work.",
        "medical": "The brain and lymphatic system; the cool, moist, phlegmatic principle governing the body's receptive and reflective capacities.",
        "spiritual": "The receptive, contemplative faculty of the soul; the mirror that reflects divine light without generating it—imagination and intuition.",
        "cosmological": "The Moon as cosmic mediator between celestial fire and terrestrial water; governess of tides, menstruation, and all cyclical change in the sublunary world."
    },
    "prima-materia": {
        "alchemical": "The undifferentiated base substance from which the Stone is made; paradoxically described as worthless and everywhere available, yet unrecognized by the ignorant.",
        "medical": "The radical moisture or fundamental bodily substrate that precedes differentiation into the four humors; the basic vitality underlying all physiological processes.",
        "spiritual": "The raw, unformed psyche before the work of individuation begins; the chaotic prima materia of the unconscious from which the Self must be extracted.",
        "cosmological": "The primordial chaos or hyle from which God fashioned the cosmos; the formless substrate underlying all manifest creation, coeval with the Creator."
    },
    "rebis": {
        "alchemical": "The 'two-thing': the hermaphroditic product of the coniunctio, uniting Sulphur and Mercury, Sol and Luna, into a single perfected substance.",
        "medical": "The perfected balance of all contrary qualities in the body; the androgynous ideal of complete humoral equilibrium transcending any single temperament.",
        "spiritual": "The integrated self in which all opposites—masculine and feminine, conscious and unconscious—are reconciled into a unified wholeness.",
        "cosmological": "The cosmic androgyne; the primordial unity that preceded the differentiation of the elements, and to which the perfected cosmos returns."
    },
    "aqua-regia": {
        "alchemical": "The royal water: a mixture of nitric and hydrochloric acids capable of dissolving gold—the only solvent powerful enough to attack the noblest metal.",
        "medical": "A corrosive remedy of extreme potency, used in minute doses to dissolve calcified obstructions that milder treatments cannot address.",
        "spiritual": "The supreme solvent of ego: a crisis or ordeal so powerful it dissolves even the most fixed and defended aspects of the personality.",
        "cosmological": "The primordial deluge or universal solvent; the catastrophic dissolution that reduces even the most permanent cosmic structures to their elements."
    },
    "aqua-vitae": {
        "alchemical": "The water of life: a purified distillate—often the philosophical mercury in its most refined form—capable of reviving dead metals and perfecting the Stone.",
        "medical": "The quintessence extracted from wine or herbs; a life-giving elixir believed to restore vitality, extend life, and cure otherwise fatal diseases.",
        "spiritual": "The living water of divine grace; the spiritual nourishment that sustains the soul through the arid phases of the Great Work.",
        "cosmological": "The celestial dew or astral moisture that descends from the stars to vivify all terrestrial life; the subtle medium through which cosmic influences operate."
    },
    "aurum-philosophicum": {
        "alchemical": "Philosophical gold: not common bullion but the perfected seed of gold freed from material impurity—the active principle of the completed Stone.",
        "medical": "The perfected vital essence; potable gold as the supreme medicine that restores perfect health by harmonizing all bodily processes to their ideal state.",
        "spiritual": "The incorruptible core of the self; the imperishable spiritual gold that survives every trial and constitutes the philosopher's true attainment.",
        "cosmological": "The solar substance in its purest form; the celestial gold that corresponds to the Sun's essence rather than its mere terrestrial reflection in mineral veins."
    },
    "elixir": {
        "alchemical": "The perfected tincture in liquid form: identical in substance to the Philosopher's Stone but prepared as a drinkable solution for medicinal projection.",
        "medical": "The universal medicine capable of curing all diseases, restoring youth, and prolonging life indefinitely—the supreme goal of iatrochemistry.",
        "spiritual": "The draught of immortality; the concentrated essence of spiritual realization that, once imbibed, permanently transforms the aspirant's nature.",
        "cosmological": "The quintessence or fifth element: the celestial substance free from corruption that permeates and sustains the four mundane elements."
    },
    "tinctura": {
        "alchemical": "The coloring power of the Stone: the capacity to permanently alter the nature of base metals by imparting gold's essential quality through superficial contact.",
        "medical": "A concentrated medicinal extract prepared by dissolving a substance's active principle in alcohol or acid; the coloring and curative essence of a remedy.",
        "spiritual": "The transformative influence of realized wisdom; the capacity of an awakened being to alter the character of those they encounter.",
        "cosmological": "The formative power by which celestial influences imprint their qualities on terrestrial matter; the coloring of earthly substance by stellar virtues."
    },
    "white-lead": {
        "alchemical": "Plumbum album or cerussa: the whitened form of lead, an intermediate product signaling partial purification on the way from Saturn's darkness to lunar silver.",
        "medical": "Used in traditional pharmacopoeia as a desiccant and cooling agent for inflamed wounds, despite its known toxicity—a dangerous remedy requiring careful dosage.",
        "spiritual": "The partially purified soul: no longer in the blackness of nigredo but not yet fully illuminated; the intermediate stage of spiritual convalescence.",
        "cosmological": "The transition from Saturn (lead) toward Luna (silver); the liminal zone between planetary influences where base matter begins to receive celestial whiteness."
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # FIGURE TERMS (qualifying — those with alchemical symbolism)
    # ═══════════════════════════════════════════════════════════════════════════
    "hermaphrodite": {
        "alchemical": "The Rebis or two-headed figure: product of the chemical wedding of Sol and Luna, depicted in Emblem XXXIV lying on a tomb—the perfected union of Sulphur and Mercury.",
        "medical": "The ideal of complete bodily equilibrium in which masculine and feminine humoral qualities are perfectly balanced, transcending the dominance of any single temperament.",
        "spiritual": "The integrated psyche: the union of animus and anima, conscious and unconscious, that Jung identified as the goal of individuation—drawing directly on alchemical imagery.",
        "cosmological": "The primordial androgyne of Platonic and Hermetic cosmology; the undivided unity that existed before the separation of heaven and earth, male and female."
    },
    "dragon": {
        "alchemical": "The devouring mercurial serpent: raw, unrefined prima materia in its most dangerous and volatile state, which must be slain and reborn as the philosophical mercury.",
        "medical": "The virulent disease or toxic agent that must be conquered and transmuted into medicine; poison as potential remedy when properly mastered.",
        "spiritual": "The guardian of the threshold: the terrifying psychic forces that must be confronted and integrated before the treasure of self-knowledge can be won.",
        "cosmological": "The ouroboros or world-serpent encircling the cosmos; the self-devouring cycle of creation and destruction that sustains the eternal return of all things."
    },
    "rex": {
        "alchemical": "The Red King: philosophical Sulphur, the solar-masculine principle that must be united with the White Queen (Mercury) to produce the Stone. In Emblem XXIV, the king is cured of melancholy.",
        "medical": "The dominant vital principle or ruling humor; in Maier's allegory, King Duenech's melancholic sickness represents the imbalance that the art must cure.",
        "spiritual": "The conscious will and ruling ego whose saturnine fixity must be dissolved before it can be reborn in a higher, more integrated form.",
        "cosmological": "The Sun as cosmic sovereign; the kingly principle of order, authority, and formative power that governs the celestial hierarchy."
    },
    "regina": {
        "alchemical": "The White Queen: philosophical Mercury, the lunar-feminine principle whose volatile, moist nature must be fixed and united with the Red King to complete the work.",
        "medical": "The receptive, nourishing aspect of the body's economy; the phlegmatic-sanguine balance that sustains fertility, moisture, and regenerative capacity.",
        "spiritual": "The soul's receptive wisdom; the feminine principle of intuition and contemplation that complements and completes the active masculine will.",
        "cosmological": "The Moon as cosmic consort; the reflective, generative, and cyclical principle that receives solar light and transmits it to the sublunary world."
    },
    "latona": {
        "alchemical": "An imperfect body composed of Sol and Luna, as Bonus describes: she must be whitened (dealbate Latonem) by washing with Mercury to reveal the hidden gold and silver within.",
        "medical": "The diseased or impure body harboring latent health; the patient whose mixed condition contains the seeds of both sickness and cure.",
        "spiritual": "The soul burdened by unresolved contraries; the mother of Apollo and Diana who suffers persecution until her divine children—light and reflection—are born.",
        "cosmological": "The material world pregnant with celestial potential; the earthly matrix from which solar and lunar principles must be separated and purified by the art."
    },
    "sphinx": {
        "alchemical": "The riddle of the Stone: the enigmatic nature of the prima materia, which is described in contradictory terms and can only be identified by the wise who solve her riddle.",
        "medical": "The diagnostic puzzle: the hidden cause of disease that presents contradictory symptoms and can only be identified by the physician who reads nature's signs correctly.",
        "spiritual": "The guardian of esoteric knowledge who devours those unworthy of initiation; only the philosopher who knows himself (as Oedipus) can pass safely.",
        "cosmological": "The composite creature uniting human, animal, and avian natures—a microcosmic emblem of the three kingdoms (mineral, vegetable, animal) united under a single enigma."
    },
    "osiris": {
        "alchemical": "The dismembered king whose body is scattered and must be reassembled by Isis: an allegory of the dissolution and reconstitution of matter in the Great Work. Maier connects Typhon's putrefaction of Osiris directly to the alchemical process.",
        "medical": "The diseased body fragmented by illness whose scattered parts (organs, humors) must be gathered and reintegrated by the healing art.",
        "spiritual": "The divine self torn apart by the forces of chaos (Typhon) and reassembled through love and devotion (Isis); death and resurrection as spiritual paradigm.",
        "cosmological": "The solar deity whose annual death and resurrection mirrors the agricultural cycle of seed, growth, harvest, and renewal—the cosmic rhythm of dying and rising gods."
    },
    "typhon": {
        "alchemical": "The destructive force of putrefaction personified: Typhon dismembers Osiris, representing the necessary corruption and dissolution that precedes alchemical regeneration.",
        "medical": "The acute crisis of disease; the violent fever or toxic eruption that breaks down the body's order but, if survived, leads to purgation and recovery.",
        "spiritual": "The shadow and destructive impulse that attacks the integrity of the self; the chaotic force that must be acknowledged and overcome in the process of individuation.",
        "cosmological": "The principle of cosmic disorder and entropy; the serpentine chaos-monster whose periodic eruptions disrupt celestial harmony but ultimately serve the cycle of renewal."
    },
    "isis": {
        "alchemical": "The reassembler: Isis gathers Osiris's scattered members and restores them to wholeness, representing the careful recombination of separated alchemical components after dissolution.",
        "medical": "The healing art personified: the patient, systematic work of gathering scattered vital forces and reintegrating them into a functioning bodily whole.",
        "spiritual": "The devoted seeker who through love, persistence, and wisdom reconstitutes what chaos has fragmented; the feminine principle of restorative wholeness.",
        "cosmological": "The veiled goddess of nature whose secrets are hidden from the profane; she governs the regenerative cycles of the natural world and the Nile's fertile inundation."
    },
    "venus": {
        "alchemical": "Copper in the planetary-metallic correspondence; the impure but promising metal whose green color and malleability connect it to organic growth and early-stage transformation.",
        "medical": "The principle of desire and attraction in the body; the generative and reproductive forces governed by warmth, moisture, and the sanguine humor.",
        "spiritual": "The power of love and beauty as transformative agents; the attractive force that draws opposites together and makes the coniunctio possible.",
        "cosmological": "The planet Venus as morning and evening star; the celestial embodiment of harmony, proportion, and the attractive power that binds the cosmos together."
    },
    "adonis": {
        "alchemical": "The beautiful youth slain by the boar: an allegory of the precious substance destroyed in the violent phase of the work, whose blood (tincture) colors the white rose red.",
        "medical": "The principle of youthful vitality cut short by violence or disease; the transience of bodily beauty that must be preserved through the physician's art.",
        "spiritual": "The dying and rising god of desire; the soul's attachment to sensory beauty that must be sacrificed before resurrection into a higher, imperishable form.",
        "cosmological": "The annual vegetation cycle embodied: Adonis's death in autumn and rebirth in spring mirrors the cosmic rhythm of solar withdrawal and return."
    },
    "king-duenech": {
        "alchemical": "The melancholic king of the Turba Philosophorum who must be cured in the steam bath: an allegory of the base metal requiring dissolution and purification to yield its hidden gold.",
        "medical": "The paradigmatic melancholic patient: his saturnine excess of black bile must be treated with moist heat (the steam bath) to restore humoral equilibrium.",
        "spiritual": "The soul imprisoned by saturnine depression; the leaden weight of acedia that can only be lifted through the warmth of spiritual practice and purgative ordeal.",
        "cosmological": "Saturn's influence made flesh: the heavy, cold, dry principle that must be warmed and moistened by solar and lunar forces to participate in cosmic harmony."
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # CONCEPT TERMS (qualifying)
    # ═══════════════════════════════════════════════════════════════════════════
    "philosopher-s-stone": {
        "alchemical": "The Lapis Philosophorum: the perfected red powder or tincture capable of transmuting base metals into gold and serving as the universal medicine—the opus's ultimate product.",
        "medical": "The panacea or universal medicine that cures all diseases, restores youth, and grants extraordinary longevity—the supreme aim of iatrochemical practice.",
        "spiritual": "The fully realized self; the incorruptible inner gold achieved through the complete integration of all psychic opposites—the goal of the soul's Great Work.",
        "cosmological": "The quintessence crystallized: the fifth element that transcends and perfects the four mundane elements, embodying the perfection of cosmic order in material form."
    },
    "philosophical-egg": {
        "alchemical": "The sealed vessel (often egg-shaped) containing the prima materia, maintained at gentle heat to incubate the Stone—the alchemical equivalent of the womb or nest.",
        "medical": "The protected healing environment; the carefully controlled conditions of temperature, moisture, and rest that allow the body's natural restorative powers to operate.",
        "spiritual": "The enclosed space of contemplation and inner work; the hermetically sealed container of the psyche in which transformation gestates before hatching into new life.",
        "cosmological": "The cosmic egg of Orphic and Hermetic cosmogony: the primordial vessel from which the differentiated cosmos emerges, containing all potentialities in compressed form."
    },
    "solve-et-coagula": {
        "alchemical": "The fundamental axiom: dissolve the fixed and coagulate the volatile. All alchemical operations reduce to this rhythm of breaking down and reconstituting matter at a higher level.",
        "medical": "The therapeutic cycle of breaking down diseased structures and rebuilding healthy tissue; the alternation of catabolism and anabolism that sustains bodily renewal.",
        "spiritual": "The universal rhythm of spiritual growth: dismantling old beliefs and identities (solve) and crystallizing new understanding into lived wisdom (coagula).",
        "cosmological": "The cosmic pulse of creation: the eternal alternation between dissolution into chaos and reconstitution into order that drives the cyclical life of the universe."
    },
    "tria-prima": {
        "alchemical": "Paracelsus's three principles—Sulphur, Mercury, and Salt—replacing the Aristotelian four elements as the fundamental components of all matter and the basis of spagyric analysis.",
        "medical": "The three physiological principles: Sulphur as vital heat and combustibility, Mercury as fluidity and volatility, Salt as structure and solidity—the Paracelsian diagnostic triad.",
        "spiritual": "Spirit, soul, and body: the tripartite anthropology in which Mercury mediates between the fiery will (Sulphur) and the material vessel (Salt).",
        "cosmological": "The three cosmic principles reflecting the Trinity: the active formative fire (Sulphur), the receptive universal medium (Mercury), and the crystallized manifest world (Salt)."
    },
    "vas-hermeticum": {
        "alchemical": "The hermetically sealed vessel in which the entire opus takes place; it must be perfectly sealed so that no spirit escapes—Maier's glass house that must be well closed.",
        "medical": "The body itself as the vessel of healing: the patient's constitution that must be sealed against external corruption while internal transformative processes complete their work.",
        "spiritual": "The contemplative enclosure of the soul; the disciplined inner space of meditation and practice in which psychic transformation can proceed without dissipation.",
        "cosmological": "The cosmos itself as God's sealed vessel: the bounded universe within which all celestial and terrestrial processes unfold according to the divine plan."
    },
    "opus-magnum": {
        "alchemical": "The Great Work itself: the entire sequence of operations from prima materia to Philosopher's Stone, encompassing nigredo, albedo, citrinitas, and rubedo.",
        "medical": "The complete course of treatment from diagnosis through crisis to cure; the physician's magnum opus of restoring the patient from sickness to perfected health.",
        "spiritual": "The lifelong work of self-transformation; the soul's journey from unconscious chaos through successive purifications to the gold of realized wisdom.",
        "cosmological": "The divine creative act mirrored in human artifice; the alchemist's work as a microcosmic recapitulation of God's original creation of order from chaos."
    },
    "lapis": {
        "alchemical": "The Stone: shorthand for the Philosopher's Stone in its most general sense—the goal and product of the alchemical art, whether conceived as powder, tincture, or elixir.",
        "medical": "The perfected medicine in solid form; the Stone as universal remedy whose mere proximity or touch is sufficient to transmute disease into health.",
        "spiritual": "The cornerstone rejected by the builders; the despised and hidden treasure of self-knowledge that the world overlooks but the wise recognize as supremely precious.",
        "cosmological": "The cosmic keystone; the perfected microcosmic substance that, as the Turba states, gives access to all the secrets of macrocosm and microcosm."
    },
    "catena-aurea": {
        "alchemical": "The golden chain: the unbroken sequence of transmissions linking ancient sages to present practitioners, guaranteeing the authenticity of alchemical knowledge.",
        "medical": "The chain of medical authority from Hippocrates through Galen to Paracelsus; the lineage of healing wisdom transmitted from master to student across centuries.",
        "spiritual": "The unbroken chain of initiatic transmission; the living lineage connecting the seeker to the original source of esoteric knowledge through teacher-student succession.",
        "cosmological": "Homer's golden chain linking heaven to earth: the vertical axis of emanation by which divine influence descends through the planetary spheres to terrestrial matter."
    },
    "cauda-pavonis": {
        "alchemical": "The peacock's tail: the iridescent display of colors appearing in the vessel during the transitional phase between nigredo and albedo, signaling that the matter is alive and progressing.",
        "medical": "The crisis of fever showing many-colored symptoms—a sign that the body is actively fighting disease and that the humoral disturbance is moving toward resolution.",
        "spiritual": "The dazzling but transient visions and psychic phenomena that arise during spiritual transformation; beautiful but not yet the stable light of true illumination.",
        "cosmological": "The rainbow as bridge between heaven and earth; the spectrum of planetary colors reflected in the alchemical vessel, recapitulating the diversity of celestial influences."
    },
    "pelicanus": {
        "alchemical": "The pelican vessel: a circulatory flask in which distillate flows back onto the residue, named for the legendary bird that feeds its young with blood from its own breast.",
        "medical": "The self-sacrificing physician who gives of their own vitality to heal the patient; the therapeutic principle that cure requires the healer's personal expenditure of life-force.",
        "spiritual": "Christ-like self-sacrifice: the soul that nourishes its own transformation through willing suffering, feeding the nascent spiritual life with the blood of the old self.",
        "cosmological": "The Sun nourishing the planets with its own substance; the cosmic principle of self-giving that sustains all dependent beings through continuous emanation of vital light."
    },
    "sapientia": {
        "alchemical": "Wisdom as the true prerequisite of the art: without philosophical understanding of nature's principles, mere laboratory technique produces nothing—knowledge precedes operation.",
        "medical": "The physician's diagnostic wisdom; the capacity to read the body's signs correctly and prescribe the right remedy at the right time in the right measure.",
        "spiritual": "Divine Sophia: the feminine personification of wisdom who guides the seeker through the labyrinth of the Great Work and reveals the hidden meaning of nature's symbols.",
        "cosmological": "The ordering intelligence pervading the cosmos; the Logos or world-reason that structures the universe according to number, proportion, and harmony."
    },
}


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    updated = 0
    skipped = 0
    missing = 0

    for slug, registers in REGISTERS.items():
        json_str = json.dumps(registers, ensure_ascii=False)
        result = conn.execute(
            "UPDATE dictionary_terms SET registers = ? WHERE slug = ?",
            (json_str, slug)
        )
        if result.rowcount > 0:
            updated += 1
        else:
            print(f"  WARNING: slug '{slug}' not found in dictionary_terms")
            missing += 1

    # Report what was skipped
    cursor = conn.execute(
        "SELECT slug, category FROM dictionary_terms WHERE registers IS NULL ORDER BY category, slug"
    )
    null_rows = cursor.fetchall()
    for slug, cat in null_rows:
        skipped += 1

    conn.commit()
    conn.close()

    print(f"\nRegisters populated: {updated}")
    print(f"Slugs not found:    {missing}")
    print(f"Terms left NULL:    {skipped}")
    if null_rows:
        print("\nTerms without registers (by design or omission):")
        for slug, cat in null_rows:
            print(f"  [{cat}] {slug}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
