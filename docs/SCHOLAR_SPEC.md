# SCHOLAR_SPEC.md — Scholar Entity Specification

## Scope

11+ scholars who have published on Atalanta Fugiens. Each gets a profile page and links to their works and emblem coverage.

## Scholar Table Fields

| Field | Source | Notes |
|-------|--------|-------|
| name | Seed JSON | Unique identifier |
| birth_year | Manual/web | Optional |
| death_year | Manual/web | Optional |
| specialization | Seed JSON | Academic discipline |
| af_focus | Seed JSON | What specifically they study about AF |
| overview | LLM-drafted | 2-3 paragraph biography. DRAFT until reviewed. |
| review_status | System | DRAFT → REVIEWED → VERIFIED |

## Initial Scholar Set

| Scholar | Specialization | AF Focus | Key Work |
|---------|---------------|----------|----------|
| H.M.E. de Jong | Art history, source criticism | All 50 emblems, source identification | Monograph (1969) |
| Hereward Tilton | History of alchemy | Spiritual alchemy, historiography debate | Quest for Phoenix (2003) |
| J.B. Craven | Biography, bibliography | Maier's life, edition history | Biography (1910) |
| C. Morris Wescott | Music theory | Musical-modal-planetary correspondences | Alchemical King article |
| Walter Pagel | History of medicine | Medical/humoral dimensions | Review (1973) |
| Paul Miner | Literary history | AF influence on Blake | N&Q article (2012) |
| Douglas Leedy | Musicology | Musical construction of canons | Review (1991) |
| Pamela H. Smith | History of science | AF as symbolic synthesis | Review (2009) |
| Joscelyn Godwin | Musicology, esoterica | Musical edition, all 50 fugues | Edition (1989) |
| Tara Nummedal | History of science, DH | Furnace & Fugue digital edition | F&F (2020) |
| Donna Bilak | Art history, steganography | Maier and steganography | F&F (2020) |

## Scholar Page Content

Each scholar page must include:
1. **Overview**: Who they are, what they study, why they matter for AF scholarship
2. **Works in Archive**: Bibliography entries linked via `scholar_works` join table
3. **Emblem Coverage**: Which emblems they analyze (derived from `scholarly_refs` WHERE `bib_id` in scholar's works)
4. **Interpretation Focus**: What type of analysis they provide (derived from `interpretation_type` distribution in `scholarly_refs`)

## Provenance

- Overview text: `source_method='LLM_ASSISTED'`, `review_status='DRAFT'`
- Factual fields (name, years, specialization): `source_method='SEED_DATA'`, `confidence='HIGH'`
- Emblem coverage counts: `source_method='DETERMINISTIC'` (computed from DB)
