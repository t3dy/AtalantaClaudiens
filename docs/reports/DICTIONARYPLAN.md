# Dictionary Enrichment Plan — "Dictionary of Atalanta Fugiens"

## Goal
Expand from 38 to 70+ terms covering ALL alchemy jargon, concepts, source texts, and alchemists/figures that appear in AF, making the dictionary a comprehensive glossary for reading the emblems.

## Current Coverage (38 terms)
- PROCESS (13): Albedo, Calcination, Citrinitas, Coagulation, Coniunctio, Dissolution, Fermentatio, Fixatio, Multiplicatio, Nigredo, Putrefaction, Rubedo, Sublimatio
- SUBSTANCE (7): Aqua Vitae, Luna, Mercurius, Prima Materia, Sol, Sulphur, White Lead
- CONCEPT (8): Catena Aurea, Lapis, Opus Magnum, Philosopher's Stone, Philosophical Egg, Sapientia, Tria Prima, Vas Hermeticum
- FIGURE (6): Atalanta, Hermaphrodite, Hippomenes, King Duenech, Regina, Rex
- SOURCE_TEXT (3): Rosarium Philosophorum, Tabula Smaragdina, Turba Philosophorum
- MUSICAL (1): Fugue

## Missing Terms to Add

### SOURCE_TEXT (12 new — from the 15 source authorities, only 3 are in dictionary)
1. Aurora Consurgens — "Aurora Consurgens"
2. Lambsprinck, De Lapide Philosophico — "De Lapide Philosophico"
3. Pseudo-Aristotle, Tractatulus — "Tractatulus de Practica Lapidis"
4. Senior Zadith, Tabula Chimica — "Tabula Chimica"
5. Ovid, Metamorphoses — "Metamorphoses"
6. Merlini Allegory — "Allegoria Merlini"
7. Lullius tradition — "Lullius / Ars Magna"
8. Solomonic Wisdom Tradition — "Liber Sapientiae"
9. Robertus Vallensis — "De Veritate Artis Chemicae"
10. Jodocus Greverus — "Secretum Nobilissimorum"
11. Lactantius — "Divinae Institutiones"
12. Rosicrucian Manifestos — "Fama Fraternitatis"

### FIGURE (10 new — mythological/alchemical figures in the emblems)
1. Osiris — Egyptian death-and-resurrection god, alchemical Sol
2. Isis — Egyptian goddess, soul of Osiris, alchemical Luna/anima
3. Typhon — Destroyer of Osiris, fiery spirit
4. Adonis — Dying god of vegetation, philosophical Sun
5. Venus — Love goddess, connected to Adonis and rose symbolism
6. Oedipus — Solver of riddles, represents the alchemist
7. Sphinx — Guardian of secrets, emblem of obscurity
8. Dragon/Draco — Volatile spirit, guardian, ouroboros variant
9. Latona — Goddess representing base metal (laton/electrum)
10. Ceres — Earth goddess, nourishment, nurse of the Stone

### PROCESS (5 new)
1. Distillatio — Distillation, separation by heat
2. Projectio — Projection, final application of the Stone
3. Solutio — Dissolving, return to liquid state
4. Circulatio — Circular distillation, rotation of elements
5. Mortificatio — Killing/death of the old form (synonym for putrefaction stage)

### SUBSTANCE (5 new)
1. Aqua Regia — Royal water, dissolves gold
2. Tinctura — The tincture, coloring agent of transmutation
3. Elixir — The perfected medicine, synonym for Stone
4. Aurum Philosophicum — Philosophical gold (not common gold)
5. Rebis — The two-thing (res bina), the reunited opposites

### CONCEPT (3 new)
1. Solve et Coagula — Dissolve and coagulate, the fundamental rhythm
2. Cauda Pavonis — Peacock's tail, iridescent transitional stage
3. Pelicanus — The pelican vessel, self-feeding cycle

## Enrichment Method

### For new terms:
1. Write seed data entries with: term, category, latin, definition, significance_to_af, related_emblems, related_terms, sources
2. Add to `atalanta_fugiens_seed.json` dictionary_entries array
3. Run pipeline: seed_phase2.py → link_dictionary.py → seed_emblem_analyses.py → build_site.py

### For existing terms (definition_long):
1. Write 3-5 sentence extended definitions for all 38 existing terms
2. Update seed JSON with definition_long field
3. Update seed_phase2.py to read and store definition_long

### For source_text terms:
Cross-reference with existing source_authorities table — the dictionary term should link to the sources page anchor for that authority.

## Estimated Result
~73 terms (38 existing + 35 new) across 6 categories, all with Latin forms, AF significance, and emblem cross-links. The dictionary becomes a true companion glossary for reading AF.
