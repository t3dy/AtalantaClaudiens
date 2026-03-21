# 321BUCKMANCRITIQUE.md — Why Claude Gets Lost Finding Emblems

## The Problem

The user has directed Claude to five different sources for emblem images and data:
1. Science History Institute digital collection (228-page viewer)
2. Wikimedia Commons (DPLA pages, labeled but scattered)
3. Furnace and Fugue website (furnaceandfugue.org)
4. The de Bry PDF in the corpus folder
5. Various online collections (SLUB Dresden, Gallica, Internet Archive)

Despite this abundance, Claude repeatedly fails to reliably identify, locate, and map emblem plates to emblem numbers. The model searches multiple sources, gets partial results, encounters rate limits, misidentifies text pages as plates, and loses track of what's been confirmed vs guessed.

## Root Cause Analysis

### 1. No Single Source of Truth
The emblem identity table (`emblem_identity`) exists in SQLite but:
- Background agents can't query it (no Bash permission)
- It's not readable without running Python
- It's not in the context window unless explicitly loaded
- New sessions start without any knowledge of what's been confirmed

### 2. Multiple Sources = Multiple Failure Modes
Each source has different problems:
- **SHI viewer**: 228 pages, only 50 shown in viewer, page-to-emblem mapping unknown
- **Wikimedia DPLA**: Pages labeled by scan page number, not emblem number; rate-limited
- **F&F**: CC BY-NC-ND, can reference but not ingest
- **de Bry PDF**: Exists locally but needs page-to-emblem mapping
- **SLUB/Gallica**: Bot protection, SSL issues

### 3. No Manifest in the Context Window
The model's working memory (context window) doesn't contain a quick-reference list of all 50 emblems with their confirmed status. Every new operation requires re-querying the database or re-reading files.

## Buckman Prompt Critique

Scoring the implicit prompt "find and identify emblem images":

| Dimension | Score | Issue |
|-----------|-------|-------|
| Scope clarity | 2/5 | "Find images" spans sourcing, downloading, identifying, mapping, and validating |
| Constraint presence | 2/5 | No stated priority order for sources, no fallback chain |
| Self-assessment | 1/5 | Model doesn't know which emblems it's already confirmed |
| Failure history | 3/5 | The model does remember SHI failed for X-L, but forgets across sessions |
| Conciseness | 3/5 | The request is clear but the instructions are scattered across files |
| Actionability | 2/5 | No clear first step — "try multiple sources" is not actionable |
| Examples | 4/5 | The SHI frontispiece + I-IX are confirmed examples of success |
| Exit criteria | 3/5 | "All 51 images mapped" is clear, but intermediate progress is unclear |

**Overall: 2.5/5 — the task needs restructuring, not more effort.**

## The Fix: Emblem Manifest

### What It Is
A flat-file JSON manifest at a known path that serves as the SINGLE SOURCE OF TRUTH for emblem identity. Every agent reads this file FIRST before doing anything with emblems.

### Where It Lives
`data/emblem_manifest.json` — already partially exists as `data/emblem_identity_seed.json`, but needs to be elevated to canonical status and referenced in CLAUDE.md.

### What It Contains
For each of the 51 emblems (0-50):
```json
{
  "number": 5,
  "roman": "V",
  "latin_motto": "Appone mulieri super mammas bufonem",
  "english_motto": "Put a toad to the breasts of a woman",
  "label": "Woman suckling the toad",
  "image_file": "emblem-05.jpg",
  "image_confirmed": true,
  "image_source": "science_history_institute",
  "page_in_1618_edition": null,
  "wikimedia_file": null,
  "furnace_fugue_url": null
}
```

### How to Use It (Prompt Pattern)
Add to CLAUDE.md:

```
## Emblem Manifest

Before working with any emblem, read `data/emblem_manifest.json`.
This is the canonical reference for all 51 emblems. It contains:
- Emblem number (0-50), Roman numeral, Latin and English mottos
- Confirmed image filename and source
- Status flags for what's been verified

If the manifest says an image is confirmed, trust it.
If the manifest says an image is NULL, the emblem needs sourcing.
Do NOT guess image mappings — update the manifest only with verified data.
```

### Why This Works
1. **Flat file**: Any agent can read it with the Read tool — no Bash, no Python, no DB query
2. **Canonical**: CLAUDE.md directs all agents to check it first
3. **Persistent**: Survives across sessions (committed to git)
4. **Self-documenting**: Each entry shows what's confirmed and what's missing
5. **Merge-friendly**: Agents can propose updates; the merge step validates

## Recommendations

### Immediate (do now)
1. Generate `data/emblem_manifest.json` from the current database
2. Add the manifest instruction block to CLAUDE.md
3. Reference the manifest in all image-related prompts

### For Image Sourcing Swarm
Each agent should:
1. READ the manifest first to know which emblems need images
2. Search ONE source (Wikipedia, F&F, de Bry PDF, etc.)
3. OUTPUT proposed updates to the manifest (new image_file, image_source values)
4. NOT download images — just identify and map

The merge step then:
1. Cross-references all agent proposals
2. Marks HIGH confidence where 2+ agents agree
3. Downloads images for confirmed mappings
4. Updates the manifest

### For Future Sessions
Any prompt that mentions emblems should include:
> "Read `data/emblem_manifest.json` for the canonical emblem index before proceeding."

This single line prevents all the searching, guessing, and re-querying that caused problems this session.
