#!/usr/bin/env python3
"""
clean_ocr_text.py — Deterministic OCR run-together word cleanup for discourse_summary.

Fixes systematic OCR artifacts where words are joined without spaces.
Pure regex/string operations — no LLM. Idempotent: running twice gives the same result.

Strategy:
1. Fix known OCR mid-word splits ("t his" → "this", "mot her" → "mother")
2. Fix camelCase joins ("theStone" → "the Stone")
3. For run-together tokens: try splitting at every position where a known function
   word is the prefix or suffix, and validate the other half against a word list
   built from an English dictionary file + domain terms.

Usage:
    python scripts/clean_ocr_text.py          # dry-run (shows changes)
    python scripts/clean_ocr_text.py --apply  # writes changes to DB
"""

import re
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "atalanta.db"

# ─── Function words: high-confidence split candidates ───

PREFIX_WORDS = {
    "the", "of", "in", "to", "for", "from", "with", "by", "at", "on",
    "and", "but", "or", "not", "is", "are", "was", "were", "has", "have",
    "had", "this", "that", "which", "who", "its", "his", "her", "our",
    "their", "into", "also", "be", "been", "can", "may", "does", "do",
    "did", "should", "would", "could", "it", "he", "she", "we", "they",
    "no", "so", "as", "if", "an", "all", "each", "every", "any", "such",
    "very", "even", "just", "only", "how", "why", "what", "when", "where",
    "about", "after", "before", "between", "through", "under", "over",
    "against", "without", "within", "upon", "during", "some", "more",
    "most", "much", "than", "nor", "yet",
}

SUFFIX_WORDS = {
    "the", "of", "in", "to", "for", "from", "with", "by", "at", "on",
    "and", "but", "or", "not", "is", "are", "was", "were", "has", "have",
    "had", "this", "that", "it", "he", "she", "we", "they",
    "be", "been", "also", "other", "some", "all", "so", "if", "as",
}

# ─── Build a large word set from the corpus itself ───

def build_word_set():
    """Build a set of known English words from:
    1. A hardcoded base set of common English + scholarly terms
    2. Words extracted from the corpus and DB (appear 2+ times)
    """
    # Large base dictionary — common English words + scholarly/alchemical terms
    base = {
        # Determiners, pronouns, prepositions, conjunctions
        "a", "an", "the", "of", "in", "to", "for", "from", "with", "by",
        "at", "on", "and", "but", "or", "not", "is", "are", "was", "were",
        "has", "have", "had", "this", "that", "these", "those", "which",
        "who", "whom", "whose", "its", "his", "her", "our", "their", "my",
        "into", "also", "be", "been", "being", "can", "may", "might",
        "does", "do", "did", "shall", "should", "would", "could", "will",
        "it", "he", "she", "we", "they", "me", "him", "us", "them",
        "no", "so", "as", "if", "all", "each", "every", "any", "such",
        "very", "even", "just", "only", "how", "why", "what", "when",
        "where", "about", "after", "before", "between", "through",
        "under", "over", "against", "without", "within", "upon", "during",
        "some", "more", "most", "much", "than", "nor", "yet", "both",
        "either", "neither", "whether", "because", "since", "while",
        "until", "unless", "although", "though", "however", "therefore",
        "thus", "then", "there", "here", "now", "already", "still",
        "again", "never", "always", "often", "sometimes", "perhaps",
        "quite", "rather", "too", "well", "indeed", "certainly",
        "especially", "particularly", "merely", "simply", "truly",
        "really", "exactly", "finally", "completely", "entirely",
        "together", "apart", "away", "above", "below", "beside",
        "among", "around", "behind", "beyond", "near", "next",
        "other", "another", "same", "own", "self",

        # Common verbs (base + common inflections)
        "accept", "add", "added", "admit", "agree", "allow", "appear",
        "appears", "apply", "applied", "arise", "arises", "arose",
        "assert", "assert", "assume", "assumes", "assumed", "attempt",
        "become", "becomes", "became", "begin", "begins", "began",
        "believe", "belong", "belongs", "bring", "brings", "brought",
        "build", "burn", "burning", "burnt", "call", "called",
        "carry", "carried", "cause", "caused", "change", "changed",
        "changes", "claim", "claims", "clean", "cleaned", "cleansed",
        "close", "closed", "come", "comes", "coming", "compare",
        "composed", "concern", "concerned", "consider", "considered",
        "consist", "consists", "contain", "contains", "continue",
        "continued", "create", "created", "cure", "cured",
        "deal", "deny", "denied", "derive", "derived", "describe",
        "described", "destroy", "destroyed", "develop", "developed",
        "die", "dies", "died", "direct", "directed", "discover",
        "discovered", "discuss", "discussed", "dissolve", "dissolved",
        "dissolving", "done", "draw", "drawn", "drink", "dry", "dried",
        "dwell", "eat", "eaten", "employ", "employed", "end", "ended",
        "enjoy", "enjoys", "enter", "exist", "existed", "exists",
        "explain", "explained", "expose", "exposed", "express",
        "expressed", "extinguish", "extinguished",
        "fall", "falls", "fed", "feed", "feeds", "feel", "felt",
        "fight", "fill", "filled", "find", "finds", "finish",
        "flow", "follow", "follows", "following", "forbid", "force",
        "forced", "form", "formed", "free", "freed", "freeze",
        "get", "gets", "give", "given", "gives", "go", "goes", "going",
        "gone", "grow", "grows", "grown", "guard", "guided",
        "happen", "happens", "hear", "heard", "heat", "heated",
        "help", "hide", "hidden", "hold", "holds",
        "ignite", "ignites", "include", "included", "increase",
        "indicate", "indicated", "introduce", "introduced",
        "join", "joined", "keep", "kept", "kill", "killed", "know",
        "known", "knows",
        "lack", "laid", "last", "lay", "lead", "leads", "learn",
        "learned", "leave", "left", "let", "lie", "lies", "like",
        "live", "lived", "look", "lose", "lost",
        "made", "make", "makes", "making", "manifest", "mark", "marked",
        "matter", "mean", "means", "meant", "mention", "mentioned",
        "mix", "mixed", "move", "moved", "must",
        "name", "named", "need", "needed", "note", "nourish", "nourished",
        "notice", "obtain", "obtained",
        "open", "opened", "oppose", "opposed", "order", "ordered",
        "originate", "originated",
        "pass", "passed", "passes", "pay", "perform", "performed",
        "permit", "permitted", "place", "placed", "plant",
        "point", "possess", "possesses", "possible", "pour",
        "practice", "prepare", "prepared", "present", "presented",
        "preserve", "preserved", "prevent", "produce", "produced",
        "prove", "proved", "proves", "provide", "provided", "purify",
        "purified", "put",
        "raise", "raised", "reach", "reached", "read", "receive",
        "received", "recognize", "recognized", "reduce", "reduced",
        "refer", "referred", "relate", "related", "remain", "remained",
        "remember", "remove", "removed", "repeat", "repeated",
        "represent", "represented", "require", "required", "resemble",
        "resembles", "rest", "restore", "restored", "result",
        "return", "returned", "reveal", "revealed", "rise", "rule",
        "run", "running",
        "said", "satisfy", "save", "saw", "say", "says", "see", "seek",
        "seem", "seems", "seen", "send", "sent", "separate", "separated",
        "serve", "served", "set", "show", "showed", "shown", "shows",
        "signify", "signifies", "sit", "speak", "speaks", "stand",
        "start", "started", "state", "stated", "states", "stay",
        "stop", "struck", "study", "submit", "succeed", "suffer",
        "suffers", "suppose", "supposed", "surpass", "symbolize",
        "symbolizes",
        "take", "taken", "takes", "teach", "teaches", "tell", "tells",
        "tend", "test", "think", "thought", "throw", "thrown",
        "took", "touch", "transform", "transformed", "treat", "treated",
        "true", "trust", "try", "turn", "turned",
        "undergo", "understand", "understood", "unite", "united",
        "use", "used", "using",
        "wait", "want", "wanted", "wash", "washed", "watch", "wish",
        "wished", "work", "worked", "write", "wrote", "written",
        "yield", "yields",

        # Common nouns
        "ability", "absence", "account", "acid", "act", "action",
        "activity", "addition", "advantage", "age", "agreement", "aim",
        "air", "allegory", "animal", "animals", "answer", "appearance",
        "application", "argument", "art", "artist", "aspect",
        "assertion", "attempt", "attention", "author", "authority",
        "basis", "bear", "beast", "beginning", "belief", "bird", "birds",
        "birth", "blood", "body", "bodies", "bone", "bones", "book",
        "books", "bottom", "boy", "brass", "breath", "brother",
        "calcination", "case", "cases", "cattle", "cause", "centre",
        "century", "certainty", "chain", "chapter", "character",
        "chemical", "child", "children", "circle", "citizen", "citizens",
        "city", "class", "cloth", "clothes", "coal", "coagulation",
        "cold", "colour", "combination", "command", "common", "companion",
        "comparison", "composition", "conception", "conclusion",
        "condition", "conflict", "conjunction", "connection",
        "consequence", "consideration", "contrast", "conversion",
        "copper", "corruption", "council", "country", "courage",
        "course", "creation", "creature", "crocodile", "crocodiles",
        "crown", "custom",
        "danger", "daughter", "day", "days", "death", "decree",
        "defence", "degree", "deity", "description", "desire",
        "destruction", "development", "difference", "differences",
        "difficulty", "direction", "dirt", "discourse", "discovery",
        "disease", "diseases", "disposition", "dissolution", "distance",
        "distillation", "distinction", "doctrine", "dog", "doubt",
        "dragon", "dream", "dress", "dryness", "dust", "duty",
        "eagle", "earth", "effect", "effort", "egg", "eggs", "eight",
        "element", "elements", "elephant", "emblem", "emperor",
        "empire", "end", "enemy", "energy", "equality", "error",
        "essence", "event", "evidence", "evil", "example",
        "excellence", "exception", "existence", "experience",
        "experiment", "explanation", "expression", "extraction",
        "eye", "eyes",
        "face", "fact", "faculty", "faith", "fame", "family",
        "farmer", "father", "fault", "fear", "feast", "female",
        "fermentation", "field", "figure", "fire", "fish", "fixation",
        "flame", "flesh", "flight", "flower", "flowers", "food",
        "foot", "force", "form", "forms", "fortune", "fountain",
        "friend", "fruit", "function", "fury",
        "garden", "gate", "generation", "genius", "gift", "glass",
        "glory", "goal", "god", "gods", "gold", "good", "grace",
        "grain", "ground", "growth", "guard", "guest", "guide",
        "habit", "hair", "half", "hand", "hands", "happiness",
        "harmony", "head", "health", "heart", "heat", "heaven",
        "heavens", "help", "herb", "hermetic", "hero", "historian",
        "history", "honour", "hope", "horse", "house", "human",
        "humility", "husband",
        "idea", "ignorance", "image", "imagination", "importance",
        "increase", "individual", "industry", "influence", "injury",
        "insect", "instance", "instrument", "intellect", "intention",
        "interest", "interpretation", "introduction", "invention",
        "iron", "island",
        "journey", "joy", "judge", "judgment", "justice",
        "kind", "kinds", "king", "kingdom", "knowledge",
        "labour", "lack", "land", "language", "law", "lead",
        "learning", "length", "letter", "liberty", "life", "light",
        "lime", "limit", "line", "linen", "lion", "liquid", "liquids",
        "love",
        "machine", "magistery", "male", "man", "manner", "mass",
        "master", "material", "matter", "meaning", "measure",
        "medicine", "member", "memory", "men", "mercury", "metal",
        "metals", "method", "middle", "milk", "mind", "mine",
        "mineral", "mirror", "mixture", "model", "moisture", "moment",
        "money", "month", "moon", "moral", "mother", "motion",
        "mountain", "mouth", "movement", "murder", "mystery",
        "mythology",
        "name", "nation", "nature", "necessity", "neglect", "night",
        "nothing", "notion", "number",
        "object", "obligation", "observation", "occasion", "ocean",
        "offence", "office", "offspring", "oil", "one", "ones",
        "opening", "operation", "opinion", "opportunity", "opposite",
        "opus", "order", "origin", "others",
        "pain", "pair", "parents", "part", "particle", "parts",
        "passage", "path", "patience", "patient", "peace", "people",
        "perfection", "period", "permission", "person", "phenomena",
        "philosopher", "philosophers", "philosophy", "physician",
        "physicians", "piece", "place", "plan", "planet", "planets",
        "plant", "plants", "pleasure", "plenty", "poetry", "point",
        "poison", "portion", "position", "possession", "possibility",
        "poverty", "powder", "power", "practice", "praise",
        "prayer", "precept", "precipice", "precipitation",
        "preparation", "presence", "present", "preservation",
        "pressure", "pretence", "price", "prince", "principle",
        "principles", "problem", "process", "processes", "product",
        "production", "profit", "progress", "promise", "proof",
        "property", "properties", "proportion", "proposition",
        "protection", "providence", "provision", "punishment",
        "purification", "purity", "purpose",
        "quality", "quantity", "queen", "question", "quicksilver",
        "rain", "rank", "reason", "reasons", "record", "reference",
        "regard", "regeneration", "region", "relation", "religion",
        "remainder", "remedy", "report", "reputation", "research",
        "resemblance", "residence", "respect", "rest", "restoration",
        "result", "resurrection", "revelation", "revenge", "reward",
        "right", "ring", "rise", "river", "road", "rock", "root",
        "rose", "rule", "ruler",
        "sacrifice", "safety", "salt", "salvation", "sand", "saturn",
        "scale", "science", "sea", "search", "season", "second",
        "secret", "seed", "sense", "separation", "serpent",
        "servant", "service", "seven", "shape", "ship", "side",
        "sight", "sign", "silence", "silver", "situation", "six",
        "size", "skill", "skin", "slave", "sleep", "smoke",
        "society", "soil", "soldier", "solid", "solution", "son",
        "sort", "soul", "souls", "sound", "source", "space",
        "species", "speech", "speed", "spirit", "spirits", "spring",
        "square", "stability", "stage", "star", "stars", "start",
        "state", "statement", "step", "stone", "stones", "story",
        "stream", "strength", "structure", "student", "study",
        "subject", "sublimation", "substance", "success", "suffering",
        "sulphur", "summary", "sun", "supply", "surface", "surprise",
        "sword", "symbol", "system",
        "tale", "taste", "teaching", "term", "test", "text",
        "theory", "thing", "things", "thought", "time", "times",
        "tincture", "title", "tongue", "top", "touch", "tradition",
        "transformation", "transmutation", "treasure", "treatment",
        "tree", "trial", "triangle", "tribe", "trick", "trouble",
        "truth", "two", "type", "types",
        "understanding", "union", "unity", "universe", "unicorn",
        "use", "utility",
        "value", "variety", "vegetation", "verse", "vessel", "view",
        "violence", "virtue", "vision", "vitriol", "voice",
        "volatilization", "vulture",
        "war", "warmth", "watch", "water", "way", "ways", "weakness",
        "wealth", "weapon", "weight", "whole", "wife", "will",
        "wind", "wine", "winter", "wisdom", "wish", "witness",
        "woman", "women", "wonder", "wood", "word", "words", "work",
        "works", "world", "worship", "worth", "wound", "wrath",
        "writing", "writings",
        "year", "years", "youth",

        # Common adjectives
        "able", "absolute", "abundant", "actual", "alive", "ancient",
        "apparent", "available", "bad", "base", "beautiful", "best",
        "better", "big", "bitter", "black", "blessed", "blind",
        "blue", "bold", "brief", "bright", "broad", "broken",
        "burning", "capable", "careful", "certain", "chemical",
        "chief", "civil", "clean", "clear", "close", "closed",
        "coarse", "cold", "combustible", "common", "complete",
        "considerable", "contrary", "correct", "curious",
        "dangerous", "dark", "dead", "dear", "deep", "desperate",
        "different", "difficult", "dirty", "distinct", "divine",
        "double", "dry", "due", "early", "easy", "effective",
        "empty", "endless", "enough", "entire", "equal", "essential",
        "eternal", "evident", "evil", "exact", "excellent",
        "excessive", "external", "extraordinary",
        "faint", "fair", "faithful", "false", "familiar", "famous",
        "fat", "fatal", "female", "few", "fierce", "final", "fine",
        "firm", "first", "fit", "fixed", "flat", "following", "foolish",
        "foreign", "former", "fortunate", "foul", "fourth", "free",
        "frequent", "fresh", "friendly", "frightful", "fruitful",
        "full", "further",
        "general", "gentle", "genuine", "glad", "glorious", "golden",
        "good", "grateful", "grave", "great", "green", "gross",
        "guilty",
        "half", "handsome", "happy", "hard", "harmful", "healthy",
        "heavy", "helpful", "hidden", "high", "highest", "holy",
        "honest", "hot", "huge", "human", "humble",
        "ignorant", "ill", "immediate", "immortal", "important",
        "impossible", "improbable", "incombustible", "incredible",
        "individual", "infinite", "innocent", "intellectual",
        "internal", "invisible", "irrefutable",
        "kind", "known", "large", "last", "late", "later", "latter",
        "least", "left", "less", "lesser", "light", "like", "little",
        "living", "local", "long", "low", "lower",
        "mad", "main", "male", "manifest", "many", "medical",
        "mere", "metallic", "middle", "mighty", "modern", "moral",
        "mortal", "natural", "necessary", "new", "next", "noble",
        "numerous",
        "obvious", "odd", "old", "only", "open", "opposite",
        "ordinary", "original", "outward",
        "pale", "particular", "past", "patient", "peculiar",
        "perfect", "perpetual", "philosophical", "physical",
        "plain", "pleasant", "poor", "popular", "possible", "potent",
        "powerful", "precious", "present", "previous", "principal",
        "private", "probable", "profound", "proper", "public", "pure",
        "purple",
        "quick", "quiet",
        "rare", "raw", "ready", "real", "reasonable", "red", "regular",
        "remarkable", "rich", "right", "rigid", "ripe", "rough",
        "round", "royal", "rude",
        "sacred", "sad", "safe", "second", "secret", "sensible",
        "separate", "serious", "severe", "sharp", "short", "sick",
        "silent", "similar", "simple", "single", "six", "slow",
        "small", "smooth", "soft", "solid", "sore", "sorry",
        "sound", "sour", "special", "spiritual", "spurious",
        "still", "strange", "strict", "strong", "subtle", "such",
        "sudden", "sufficient", "suitable", "superior", "supposed",
        "supreme", "sure", "surprising", "sweet", "swift",
        "symbolic",
        "tall", "terrible", "thick", "thin", "third", "thorough",
        "total", "tough", "tremendous", "triple", "trivial", "true",
        "twofold", "typical",
        "ugly", "unclean", "universal", "unknown", "unusual",
        "upper", "useful", "useless", "usual", "utter",
        "vague", "vain", "vast", "violent", "virtual", "visible",
        "vital", "voluntary",
        "warm", "weak", "wet", "white", "wicked", "wide", "wild",
        "willing", "wise", "wonderful", "wooden", "worthy", "wrong",
        "young",

        # Scholarly names and terms common in the text
        "according", "alchemy", "alchemical", "alchemist", "alchemists",
        "allegory", "allegorical", "allegorically", "analysis",
        "analytical", "ancient", "antiquity", "argument",
        "astronomers", "astrological",
        "biblical", "bibl",
        "cabalistic", "chapter", "chemical", "chemist", "commentary",
        "composition", "compound", "contrary", "conversion",
        "corresponding", "cosmological",
        "described", "discourse", "discovery",
        "egyptian", "egyptians", "elixir", "emblem",
        "esoteric", "essence", "essential", "experiment", "explanation",
        "figurative", "figuratively",
        "genesis", "geometrical", "greek",
        "hermetic", "hermeticists", "historical", "historian",
        "identity", "interpret", "interpretation",
        "laboratory", "latin", "literal", "literally",
        "magical", "material", "mercury", "metaphor", "metaphorical",
        "mineral", "mythological", "mythology",
        "numerical",
        "obscure", "observation", "occult", "operation",
        "parable", "peripatetic", "peripatetics",
        "philosophical", "philosopher", "philosophy", "planetary",
        "practical", "preparation", "prima", "primordial",
        "quintessence",
        "recipe", "reference", "religious", "rosarium",
        "saturn", "scholar", "scholars", "scholarly", "scientific",
        "scripture", "significance", "solution", "source", "spiritual",
        "sublimation", "sulphur", "symbolic", "symbolism", "symbolizes",
        "tabula", "theological", "theory", "tincture", "tradition",
        "traditional", "transformation", "transmutation", "treatise",
        "turba",
        "universal",
        "vitriol",

        # Number words
        "one", "two", "three", "four", "five", "six", "seven",
        "eight", "nine", "ten", "eleven", "twelve", "thirteen",
        "twenty", "thirty", "forty", "fifty", "hundred", "thousand",
        "first", "second", "third", "fourth", "fifth", "sixth",
        "seventh", "eighth", "ninth", "tenth",

        # Additional common words found missing from OCR text
        "absorbed", "abundance", "acceptable", "accomplish", "accomplished",
        "accordingly", "accumulate", "accumulated", "acknowledge", "acknowledged",
        "acquired", "addition", "addressed", "administered", "admirable",
        "admired", "adopted", "adulteration", "advanced", "advice",
        "affected", "affinity", "afforded", "agriculture", "alexander",
        "altogether", "amazed", "ambitious", "amounted", "ample",
        "analogous", "anatomy", "anger", "announced", "annual",
        "anticipated", "apparently", "appointed", "appropriate",
        "approval", "argonauts", "arrangement", "arrived", "artisan",
        "ascending", "ascribed", "assembled", "assigned", "assisted",
        "associated", "assimilated", "astonished", "attached",
        "attained", "attempted", "attracted", "attributed", "audience",
        "avoided",
        "balanced", "banished", "basket", "battle", "beast", "beaten",
        "beautiful", "behaviour", "beneficial", "bestowed", "betrayed",
        "blackness", "blanket", "blended", "blessed", "blinding",
        "boiling", "boldly", "borrowed", "bounded", "branches",
        "brilliant", "brittle", "broadly", "buried",
        "calculation", "calendar", "candidate", "capable", "capacity",
        "captured", "carpet", "carpets", "castle", "catalogue",
        "celebrated", "celestial", "chamber", "champion", "characters",
        "charitable", "chemistry", "cherished", "chosen", "chronicle",
        "circumstances", "claimed", "classification", "collected",
        "colouring", "columns", "combined", "combustible", "commanded",
        "commenced", "commercial", "committed", "commonly",
        "communicated", "companion", "companions", "comparable",
        "compelled", "complaint", "completely", "complicated",
        "comprehend", "compressed", "compulsion", "concealed",
        "concentrated", "concept", "condemned", "condensed",
        "conditions", "conducted", "conferred", "confidence",
        "confirmed", "confused", "connected", "conquered", "conscious",
        "consequently", "conserved", "considered", "considerable",
        "constructed", "consumed", "contained", "contaminated",
        "contemplated", "contented", "contested", "continually",
        "contracted", "contradicted", "contributed", "controlled",
        "convenient", "conversation", "converted", "convinced",
        "cooperated", "copper", "correspond", "corresponds",
        "corresponding", "corrected", "corrupted", "council",
        "counsellor", "counterfeit", "countless", "courage", "covered",
        "credited", "critical", "crocodile", "crocodiles", "crowned",
        "cruelty", "cultivated", "cunning", "curious", "currently",
        "customary",
        "damaged", "darkness", "deceived", "declared", "declined",
        "decorated", "dedicated", "defended", "definition", "delight",
        "delivered", "demanded", "demonstrated", "departed",
        "dependent", "deposited", "depression", "descended",
        "deserved", "designated", "desired", "despised", "destiny",
        "detailed", "detained", "determined", "devoted", "dialogue",
        "diminished", "directed", "disappeared", "discharge",
        "disclosed", "disconnected", "discourse", "disguised",
        "disintegrate", "dismissed", "disorder", "dispensed",
        "disposed", "disputed", "distinguished", "distributed",
        "disturbance", "dominates", "doubted", "dramatically",
        "drenched", "dirtiest", "dried", "drinking", "duration",
        "dwelling",
        "earnestly", "eclipse", "effective", "elaborate", "eliminated",
        "embraced", "emerged", "emission", "emotion", "emphasized",
        "employed", "empowered", "encounter", "encountered",
        "encouraged", "endured", "engaged", "enormous", "enriched",
        "enrolled", "enterprise", "enthusiasm", "equipped",
        "equivalent", "erupted", "established", "estimated",
        "eventually", "exaggerated", "examination", "examined",
        "exceeding", "exceedingly", "exception", "exchanged",
        "exclusively", "excrement", "excrements", "excused",
        "executed", "exercised", "exhibited", "expanded", "expected",
        "expedient", "expelled", "experienced", "explained",
        "explicitly", "exploited", "exposed", "extension",
        "extensive", "extraordinary", "extremely",
        "fabricated", "facilitated", "familiar", "fashioned",
        "favorable", "favourable", "feared", "feasting", "features",
        "fermented", "fertilized", "fetched", "fighting", "figured",
        "filtered", "floats", "flourished", "flowing", "foolish",
        "forbidden", "forecast", "foremost", "foretold", "forgetting",
        "formally", "formulated", "fortified", "fortunate", "fostered",
        "founded", "fragrant", "framework", "frequently", "frightened",
        "fulfilled", "function", "fundamental", "furnished",
        "generated", "generation", "generous", "gentle", "genuinely",
        "geography", "glorified", "goddess", "governed", "gradually",
        "granted", "grievous", "grounded", "guaranteed", "guarded",
        "habitation", "handling", "happiness", "hardening", "harmony",
        "hatched", "hatred", "heavenly", "henceforth", "heritage",
        "heroic", "hesitated", "highest", "historical", "honoured",
        "hopefully", "horrible", "hostility", "household", "humility",
        "ignorance", "illustrated", "imagination", "imagined",
        "immediately", "immersed", "immortal", "imparted",
        "imperfect", "imperfection", "implicated", "importance",
        "impossible", "impressed", "imprisoned", "improved",
        "impure", "impurity", "inability", "inclined", "incredible",
        "independence", "independent", "indicated", "indifferent",
        "indispensable", "influenced", "informed", "inhabitants",
        "inherited", "initiated", "injuries", "innocent",
        "innumerable", "inscription", "insignificant", "insisted",
        "inspired", "installed", "instruction", "instructions",
        "intended", "intentional", "interpretation", "interrupted",
        "introduced", "investigated", "invisible", "irrefutable",
        "journal", "journey", "judged", "judgment",
        "kindled", "kingdom", "kindness",
        "laboured", "lamented", "landscape", "largely",
        "leadership", "liberated", "likewise", "limitation",
        "literally", "literature", "located", "lonely", "longed",
        "longer",
        "macedonia", "magnitude", "maintained", "manifested",
        "manufactured", "manuscript", "masculine", "materials",
        "mathematical", "meanwhile", "measured", "mechanical",
        "meditation", "melancholy", "membrane", "mentioned",
        "mercurial", "messenger", "metaphor", "metaphorical",
        "methodical", "microscope", "mineral", "miracle", "miracles",
        "miserable", "misfortune", "mistaken", "mixture", "moderate",
        "modified", "molecular", "monarchs", "monastery", "morality",
        "moreover", "mountain", "mountains", "mourning", "multiplied",
        "municipal", "murdered", "mysterious",
        "naturally", "navigated", "necessity", "neglected",
        "negligence", "negotiated", "nevertheless", "nobility",
        "nominated", "nonsense", "nourished", "nourishment",
        "obedience", "objection", "obligated", "observation",
        "observed", "obstacles", "obtained", "obviously", "occupied",
        "occurrence", "offended", "offensive", "officially",
        "operated", "operation", "operations", "opponents",
        "opportunity", "opposition", "oppressed", "ordinarily",
        "organized", "originally", "ornament", "outstanding",
        "overcome", "overlooked",
        "patience", "penetrated", "percentage", "perception",
        "perfected", "performed", "permanent", "permission",
        "perpetual", "persecuted", "persisted", "personally",
        "persuaded", "perverted", "petition", "petroleum",
        "philosopher", "physicians", "pilgrimage", "plainly",
        "poisonous", "political", "pollution", "population",
        "portrayed", "possessed", "posterior", "postponed",
        "potassium", "potential", "practiced", "praised",
        "precaution", "precedent", "preceding", "precisely",
        "predicted", "preferred", "prejudice", "preliminary",
        "premature", "prescribed", "presented", "president",
        "presumably", "pretended", "prevented", "previously",
        "primarily", "primitive", "princess", "principal",
        "principles", "privilege", "procedure", "proceeded",
        "processed", "procession", "proclaimed", "procured",
        "prodigious", "produced", "products", "professor",
        "profitable", "profoundly", "programme", "prohibited",
        "projection", "prominent", "promised", "promoted",
        "pronounced", "propagated", "propensity", "properly",
        "prophecies", "prophesied", "prophet", "proportion",
        "proposals", "protected", "protested", "providence",
        "provisions", "provoked", "published", "punctually",
        "punishment", "purchased", "purifying", "purity",
        "quadruplet", "qualified", "quarrelled", "questioned",
        "quietly",
        "radically", "raging", "reasonably", "rebellion",
        "receiving", "recognised", "recommended", "reconciled",
        "recovered", "reflected", "reformed", "refreshed",
        "refuted", "regarded", "regards", "registered", "regulated",
        "reigning", "reinforced", "rejected", "relations",
        "relaxation", "released", "remarkable", "remembered",
        "reminiscent", "rendering", "renowned", "repeatedly",
        "repentance", "replaced", "reproduced", "repudiated",
        "requested", "residence", "resigned", "resistance",
        "resolution", "respected", "responded", "responsible",
        "restrained", "restricted", "resulting", "retained",
        "retirement", "retreated", "returning", "revelation",
        "righteous", "rightfully", "rigorously", "roads",
        "robbed",
        "sacrificed", "safeguard", "salamander", "sanctioned",
        "satisfied", "scattered", "scholarly", "scientific",
        "scripture", "searching", "sensation", "separated",
        "seriously", "settlement", "shattered", "sheltered",
        "shortened", "signified", "similarly", "simplicity",
        "simulated", "situation", "slaughter", "smelting",
        "solicited", "solidified", "solitary", "sophisticated",
        "sovereign", "speculated", "stabilized", "statement",
        "stationed", "stimulated", "stipulated", "straightforward",
        "strangled", "stratagem", "strengthen", "stretched",
        "structure", "struggled", "subjected", "sublimated",
        "submitted", "subordinate", "subsequent", "succeeded",
        "successive", "sufficient", "suffocates", "suggested",
        "summarized", "summoned", "superfluous", "superseded",
        "supervised", "supplement", "supported", "suppressed",
        "suppressing", "surmounted", "surpassed", "surrounded",
        "suspected", "suspended", "sustained", "sweetness",
        "sympathetic", "systematic",
        "temperament", "temperature", "temporarily", "terminated",
        "territory", "testimony", "theatrical", "thereafter",
        "threatened", "threshold", "tolerated", "tormented",
        "traditions", "translated", "transmitted", "transported",
        "traversed", "tremendous", "triumphant", "troublesome",
        "ultimately", "unaware", "uncertain", "undergoes",
        "undergone", "underneath", "understood", "undertaken",
        "unexpected", "unfortunate", "unnatural", "unprecedented",
        "unreliable", "unsuccessful", "unwilling",
        "variations", "vehemently", "vegetation", "venerable",
        "ventilated", "vindicated", "virtually", "volatilized",
        "voluntary", "vulnerable",
        "wandering", "warfare", "warranted", "watchfulness",
        "waterandfire", "welcomed", "whatsoever", "wherefore",
        "wholesale", "widespread", "willingly", "withdrawn",
        "withstood", "witnessed", "worshipped",

        # Proper nouns common in the text (lowercase for matching)
        "aristotle", "avicenna", "democritus", "galen", "geber",
        "hermes", "hippocrates", "homer", "jupiter", "lully", "lull",
        "mars", "maier", "mercury", "morienus", "moses", "neptune",
        "ovid", "paracelsus", "plato", "pliny", "prometheus",
        "pythagoras", "saturn", "seneca", "socrates", "solomon",
        "tacitus", "venus", "virgil", "vulcan",
        "spain", "egypt", "greece", "rome", "ocean", "europe",
        "alexander", "parnassus", "aesculapius", "latona",
        "bernhardus", "trevisanus", "geryon", "chrysaor", "medusa",
        "typhon", "echydna", "orion", "duenech",

        # Additional words found missing in OCR text analysis
        "substances", "vegetable", "freshness", "combustibles",
        "stains", "quotation", "fathers", "various", "somewhat",
        "washed", "washing", "uses", "achieved", "achieved",
        "cleanses", "cleanse", "discusses", "discussing",
        "obtained", "hairs", "dressed", "tallow", "purifying",
        "everyday", "philosophers", "stone", "found", "gold",
        "roads", "manner", "held", "fed", "unnatural",
        "dominates", "alike", "nourishment", "beneficial",
        "passes", "strengthens", "consequently", "quadruplet",
        "interdependent", "disintegrate", "perishable",
        "perish", "perishes", "twins", "aqua", "regia",
        "petroleum", "endure", "lime", "sweeps", "byssinusf",
        "anselmus", "boodt", "suffocated", "throwing",
        "considerable", "kindling", "extinguishing",
        "acknowledges", "credited", "spurious",
        "writings", "title", "variant", "resembles", "identify",
        "mindful", "denial", "possibility", "possessed", "authority",
        "difficult", "distil", "conclusion", "respect",
        "relates", "relate", "relationship", "elements",
        "originates", "depicted", "strong", "disintegrate",
        "prevents", "prevent", "prevented", "improbable",
        "finish", "influence", "stars", "born",
        "bodies", "souls", "perhaps", "happens",
        # More words found missing in iteration 3
        "easily", "nursing", "toad", "toads", "pregnant", "conceive",
        "womanly", "manly", "womens", "mens", "appears", "tire",
        "considerable", "beget", "begot", "begotten", "feed",
        "obtained", "made", "out", "having", "big", "because",
        "mentions", "mention", "commentaries", "bishop", "bishopric",
        "reliable", "cruel", "woman", "should", "aspects", "these",
        "everyday", "slated", "unslated", "ignite", "means",
        "extinguished", "properties", "more", "way", "petroleum",
        "sweeps", "burning", "throwing", "carpets", "suffocated",
        "appears", "rosarius", "says", "emblem", "somewhat",
        "stone", "bones", "warmth", "lime", "aqua",
        "cleopatra", "theophilus", "guilielmus",
        # Iteration 5 — still-missing common words
        "physician", "perfecting", "adjacent", "affects",
        "affects", "native", "country", "wields", "attributes",
        "devours", "instead", "spits", "inventor",
        "guarded", "literally", "acknowledged", "credited",
        "humblest", "considered", "citizens", "concerned",
        "wandered", "houses", "caves", "opposite", "united",
        "valentine", "understand", "following",
        "applies", "attached", "below", "combined",
        "consisting", "contrary", "copied", "current",
        "damage", "delivered", "derived", "designed",
        "entire", "erected", "essential", "estimated",
        "evidence", "excellent", "excessive", "existing",
        "expands", "expects", "extends",
        "farmers", "features", "figures", "flames",
        "gardens", "gathered", "governs", "gradually",
        "grounds",
        "happened", "highest", "himself", "however",
        "images", "immediately", "includes", "inhabited",
        "insects", "islands",
        "justice", "justified",
        "killing", "kindled",
        "lacking", "learned", "leaves", "legends", "letters",
        "limits", "located", "lowest",
        "managed", "matters", "meaning", "measures",
        "merely", "methods", "minerals", "minutes",
        "movement", "multiplied",
        "natives", "numbers",
        "obvious", "occurs", "offered", "ordered",
        "others", "outside",
        "passage", "patience", "pattern", "permits",
        "persons", "physical", "places", "planted",
        "pointed", "portions", "precious", "presented",
        "prevents", "princes", "produced", "promised",
        "proper", "proposed", "protected", "proven",
        "qualities", "questions", "quickly",
        "raised", "ranges", "reasons", "reduced",
        "regular", "related", "released", "religion",
        "removed", "repaired", "reported",
        "resolved", "restored", "returned", "revealed",
        "sacred", "scholars", "seasons", "sentences",
        "servants", "settled", "several", "shaped",
        "sharper", "shorter", "simpler", "situated",
        "skilled", "sleeping", "smaller", "spirits",
        "splendid", "started", "stories",
        "student", "studied", "success", "suffered",
        "symbols", "teaching",
        "temples", "thereby", "title", "towards",
        "travels", "treated", "trusted",
        "unclean", "understood", "unless", "unlike",
        "valleys", "valued", "various", "vessels",
        "violent", "visible",
        "waiting", "warriors", "weapons",
        "written", "younger",
        # Iteration 4 — remaining common unsplit tokens
        "headed", "seven", "two", "dragon", "headed",
        "forthwith", "rule", "submit", "beget", "bring",
        "forth", "blood", "milk", "gets",
        "natural", "bestow", "bestowed", "bestows",
        "born", "bear", "carried", "carries",
        "complete", "completed", "completion",
        "constantly", "contrary", "contributed",
        "convicted", "copper", "correct",
        "describes", "designated", "destroyed",
        "determined", "develops", "discovered",
        "discusses", "disputed",
        "employed", "encounter", "engaged",
        "explains", "expressed",
        "fables", "fallen", "fertile",
        "gives", "granted", "grows",
        "hidden", "highest",
        "indicates", "induces", "inherent",
        "intended", "intervened",
        "joined", "keeps", "kinds",
        "labours", "leads", "learned",
        "lion", "longer",
        "magnified", "marked", "married",
        "necessary", "nourishes",
        "obtains", "occurs", "opinion",
        "performed", "permits", "placed",
        "plenty", "pointed", "prepares",
        "produces", "promised", "promoted",
        "proves", "provided", "provides",
        "reaches", "receives", "recognised", "refers",
        "relates", "remains", "resembles", "resists",
        "results", "returns", "reveals",
        "satisfies", "seeks", "serves",
        "shows", "signifies", "speaks",
        "stands", "stated", "stays",
        "strengthened", "succeeds", "suffers", "suggests",
        "surpasses", "survives",
        "teaches", "tells", "thinks",
        "touches", "transforms", "treats", "turns",
        "understands", "uses",
        "warmth", "welcomed", "wishes", "works",
    }
    return {w.lower() for w in base}


# Build the word set once at module level
KNOWN_WORDS = build_word_set()

# Minimum remainder length after splitting off a function word.
# Short function words need longer remainders to avoid false positives.
MIN_REMAINDER = {1: 4, 2: 2}  # 1-char prefix needs 4+ remainder, 2-char needs 2+
DEFAULT_MIN_REMAINDER = 2  # 3+ char prefix needs 2+ remainder


def _split_core(lower_core, depth=0):
    """Recursively try to split a lowercase word into known words.
    Returns a list of words if successful, or None if no valid split found.
    Max depth prevents runaway recursion.
    """
    if depth > 6:
        return None

    # Base case: the whole string is a known word
    if lower_core in KNOWN_WORDS:
        return [lower_core]

    if len(lower_core) < 3:
        return None

    # Try every split position
    best = None

    for i in range(1, len(lower_core)):
        left = lower_core[:i]
        right = lower_core[i:]

        min_rem = MIN_REMAINDER.get(len(left), DEFAULT_MIN_REMAINDER)
        if len(right) < min_rem:
            continue

        # Only split if left is a function word OR a known word
        left_is_func = left in PREFIX_WORDS
        left_is_known = left in KNOWN_WORDS

        if not (left_is_func or left_is_known):
            continue

        # Recursively try to split the right half
        right_parts = _split_core(right, depth + 1)
        if right_parts is None:
            continue

        # Valid split found
        candidate = [left] + right_parts

        # Score: prefer fewer total parts (less aggressive splitting)
        # and prefer splits where left is a known (not just function) word
        if best is None or len(candidate) < len(best):
            best = candidate

    return best


def _split_alpha_segment(segment):
    """Try to split a purely alphabetic segment into known words.
    Returns the split version or the original.
    """
    if len(segment) < 4:
        return segment

    lower = segment.lower()
    if lower in KNOWN_WORDS:
        return segment

    parts = _split_core(lower, depth=0)
    if parts is None:
        return segment

    # Preserve original casing
    result_parts = []
    pos = 0
    for part in parts:
        result_parts.append(segment[pos:pos + len(part)])
        pos += len(part)
    return " ".join(result_parts)


def try_split_token(token):
    """Try to split a run-together token into known words.
    Returns the split version if valid, or the original token.
    Handles internal non-alpha characters (em-dashes, special chars) by
    splitting the token into alphabetic segments and processing each.
    """
    if not token or len(token) < 4:
        return token

    # Split token into alternating alpha and non-alpha segments
    segments = re.findall(r'[a-zA-Z]+|[^a-zA-Z]+', token)

    result_parts = []
    for seg in segments:
        if re.match(r'^[a-zA-Z]+$', seg):
            result_parts.append(_split_alpha_segment(seg))
        else:
            result_parts.append(seg)

    return "".join(result_parts)


def clean_text(text):
    """Apply all OCR cleanup rules to text. Returns cleaned text."""
    if not text:
        return text

    result = text

    # === Pass 0: Fix OCR mid-word splits (space inserted in wrong place) ===
    ocr_rejoin = [
        (r'\bt his\b', 'this'),
        (r'\bt hat\b', 'that'),
        (r'\bt he\b', 'the'),
        (r'\bt hen\b', 'then'),
        (r'\bt here\b', 'there'),
        (r'\bt hose\b', 'those'),
        (r'\bt hese\b', 'these'),
        (r'\bt hus\b', 'thus'),
        (r'\bt hree\b', 'three'),
        (r'\bt hrough\b', 'through'),
        (r'\bt hrow\b', 'throw'),
        (r'\bt hrown\b', 'thrown'),
        (r'\bw hich\b', 'which'),
        (r'\bw here\b', 'where'),
        (r'\bw hat\b', 'what'),
        (r'\bw hen\b', 'when'),
        (r'\bw hile\b', 'while'),
        (r'\bw hole\b', 'whole'),
        (r'\bw hose\b', 'whose'),
        (r'\bw ith\b', 'with'),
        (r'\bfurt her\b', 'further'),
        (r'\beit her\b', 'either'),
        (r'\bneit her\b', 'neither'),
        (r'\bwhet her\b', 'whether'),
        (r'\btoget her\b', 'together'),
        (r'\balt hough\b', 'although'),
        (r'\balt oget her\b', 'altogether'),
        (r'\bot her\b', 'other'),
        (r'\bmot her\b', 'mother'),
        (r'\bfat her\b', 'father'),
        (r'\bbrot her\b', 'brother'),
        (r'\bbot h\b', 'both'),
        (r'\beac h\b', 'each'),
        (r'\bmuc h\b', 'much'),
        (r'\bsuc h\b', 'such'),
        (r'\bric h\b', 'rich'),
        (r'\bwhic h\b', 'which'),
        (r'\bnever- ?theless\b', 'nevertheless'),
        (r'\bnot hing\b', 'nothing'),
        (r'\bever ything\b', 'everything'),
        (r'\bsome thing\b', 'something'),
        (r'\bunderst and\b', 'understand'),
        (r'\bunderst ands\b', 'understands'),
        (r'\bunderst anding\b', 'understanding'),
        (r'\bunderst ood\b', 'understood'),
        (r'\bscy the\b', 'scythe'),
        (r'otherh and\b', 'otherhand'),  # will be split by token splitter
        (r'\bcom mand\b', 'command'),
    ]
    for pat_str, replacement in ocr_rejoin:
        result = re.sub(pat_str, replacement, result)

    # === Pass 1: camelCase splits (lowercase followed by uppercase) ===
    result = re.sub(r'([a-z])([A-Z])', r'\1 \2', result)

    # === Pass 2: Token-by-token splitting of run-together words ===
    # Process multiple passes since splitting one token may create new opportunities
    for _ in range(5):
        prev = result
        lines = result.split('\n')
        cleaned_lines = []
        for line in lines:
            tokens = line.split(' ')
            cleaned_tokens = [try_split_token(t) if t else t for t in tokens]
            cleaned_lines.append(' '.join(cleaned_tokens))
        result = '\n'.join(cleaned_lines)
        if result == prev:
            break

    # === Pass 3: Clean OCR artifacts ===
    result = result.replace("\\'", "'")
    result = re.sub(r'\\(?=[\s,;:\.])', '', result)

    # === Pass 4: Normalize whitespace ===
    result = re.sub(r'[ \t]+', ' ', result)
    result = re.sub(r'\s+([,;:.!?])', r'\1', result)

    return result.strip()


def main():
    apply = "--apply" in sys.argv
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    rows = cur.execute(
        "SELECT number, discourse_summary FROM emblems "
        "WHERE discourse_summary IS NOT NULL ORDER BY number"
    ).fetchall()

    print(f"Found {len(rows)} emblems with discourse summaries.")
    changes = []

    for number, original in rows:
        cleaned = clean_text(original)
        if cleaned != original:
            changes.append((number, original, cleaned))

    print(f"\n{len(changes)} summaries need cleaning.\n")

    # Show before/after for first 3 changed emblems
    samples = changes[:3] if len(changes) >= 3 else changes
    for number, original, cleaned in samples:
        print("=" * 70)
        print(f"EMBLEM {number}")
        print("=" * 70)
        print("BEFORE (first 500 chars):")
        print(f"  {original[:500]}")
        print()
        print("AFTER  (first 500 chars):")
        print(f"  {cleaned[:500]}")
        print()

    # Diagnostic mode: show remaining unsplit tokens
    if "--diag" in sys.argv:
        unsplit = {}
        for number, original, cleaned in changes:
            for token in cleaned.split():
                core = re.sub(r'[^a-zA-Z]', '', token)
                if len(core) > 8 and core.lower() not in KNOWN_WORDS:
                    unsplit[core.lower()] = unsplit.get(core.lower(), 0) + 1
        print("Top remaining unsplit tokens (>8 chars, not in dictionary):")
        for word, count in sorted(unsplit.items(), key=lambda x: -x[1])[:50]:
            print(f"  {word:30s} ({count}x)")
        print()

    if apply:
        for number, original, cleaned in changes:
            cur.execute(
                "UPDATE emblems SET discourse_summary = ? WHERE number = ?",
                (cleaned, number)
            )
        conn.commit()
        print(f"Applied {len(changes)} discourse updates to database.")
    else:
        print("Dry run — no changes written. Use --apply to update the database.")

    # Also clean motto_english and epigram_english
    motto_changes = 0
    epigram_changes = 0
    for col in ['motto_english', 'epigram_english']:
        col_rows = cur.execute(
            f"SELECT number, {col} FROM emblems WHERE {col} IS NOT NULL ORDER BY number"
        ).fetchall()
        for number, original in col_rows:
            cleaned = clean_text(original)
            if cleaned != original:
                if apply:
                    cur.execute(f"UPDATE emblems SET {col} = ? WHERE number = ?", (cleaned, number))
                if col == 'motto_english':
                    motto_changes += 1
                else:
                    epigram_changes += 1
    if apply:
        conn.commit()
    print(f"  motto_english: {motto_changes} cleaned")
    print(f"  epigram_english: {epigram_changes} cleaned")

    conn.close()


if __name__ == "__main__":
    main()
