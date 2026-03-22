# FUTURESESSIONS.md — Detailed Specifications for Remaining Work

**Date**: 2026-03-21
**Scope**: Five feature areas deferred from this session, specified in enough detail for a future session to build without re-research.

---

## 1. UI Enhancements (Emblem Pages)

### Current State
Emblem pages now have: bilingual motto block (Latin/English), visible epigram, stage badges, "What You See" visual descriptions, discourse summary, analysis blocks with cross-links, and scholarly commentary panel.

### Remaining UI Work

#### 1A. Related Emblems Sidebar
**What**: A horizontal row of 3-4 emblem thumbnail cards at the bottom of each emblem page, linking to related emblems.

**How to determine "related"** (in priority order):
1. **Same alchemical stage** — emblems sharing NIGREDO/ALBEDO/CITRINITAS/RUBEDO
2. **Shared source authorities** — emblems that cite 2+ of the same sources (query `emblem_sources` join)
3. **Shared dictionary terms** — emblems linked to the same terms (query `term_emblem_refs` join)
4. **Sequential neighbors** — if no other matches, show prev/next emblems

**Algorithm**:
```python
def get_related_emblems(conn, emblem_id, stage, limit=4):
    # 1. Same stage (excluding self), random sample
    same_stage = query("SELECT id FROM emblems WHERE alchemical_stage = ? AND id != ?", stage, emblem_id)
    # 2. Shared sources (count overlap)
    shared_src = query("""
        SELECT e2.emblem_id, COUNT(*) as overlap
        FROM emblem_sources e1
        JOIN emblem_sources e2 ON e1.authority_id = e2.authority_id
        WHERE e1.emblem_id = ? AND e2.emblem_id != ?
        GROUP BY e2.emblem_id
        ORDER BY overlap DESC
    """, emblem_id, emblem_id)
    # Merge, deduplicate, take top `limit`
```

**Template** (in `build_site.py`):
```html
<div class="related-emblems">
    <h3>Related Emblems</h3>
    <div style="display:flex;gap:1rem;overflow-x:auto">
        <!-- For each related emblem: -->
        <a href="emblem-NN.html" class="related-card">
            <img src="../images/emblems/emblem-NN.jpg" alt="Emblem N">
            <span class="related-label">XXI. Circle-square-triangle</span>
            <span class="badge" style="...">RUBEDO</span>
        </a>
    </div>
</div>
```

**Placement**: Bottom of the source-panel (left column), after the analysis block.

**Effort**: ~30 min. Pure SQL + template. No new data needed.

#### 1B. Thematic Browse Modes on Home/Gallery
**What**: Filter buttons on the gallery page to browse emblems by alchemical stage, source tradition, or mythological figure.

**Current state**: Filter buttons exist in the HTML spec (`docs/INTERFACE.md`) but the JS only does stage filtering. Need to add source-tradition and figure-based filtering.

**Data source**: `data.json` already contains stage info. Would need to add `sources` and `figures` arrays per emblem to `data.json` (built by `build_site.py`).

**Effort**: ~45 min. Extend `data.json` generation, add JS filter logic in `script.js`.

#### 1C. Stage-Colored Emblem Cards
**What**: Subtle background tint on gallery cards reflecting their alchemical stage.

**Colors** (matching badge scheme, but at 10% opacity):
- NIGREDO: `rgba(44, 36, 24, 0.08)`
- ALBEDO: `rgba(168, 152, 128, 0.08)`
- CITRINITAS: `rgba(184, 134, 11, 0.08)`
- RUBEDO: `rgba(192, 57, 43, 0.08)`

**Effort**: ~10 min. Add inline style to card generation in `build_site.py`.

---

## 2. Vision Analysis Pipeline

### What
Run Claude Vision on all 51 emblem plate images to generate structured JSON descriptions of visual elements (allegorical figures, objects, architecture, symbols, composition).

### Current State
- 51 images exist in `site/images/emblems/`
- `emblems.visual_elements` column exists (TEXT, for JSON) — currently NULL for all
- `emblems.image_description` has text descriptions (51/51) — these are human-written summaries, NOT structured element data
- The separate `visual_elements` TABLE (normalized, with element_type/position/alchemical_meaning) is `[PLANNED]` but not created

### Design

**Script**: `scripts/analyze_emblem_images.py`

**Per-image prompt to Claude Vision**:
```
Analyze this 1618 alchemical emblem plate from Michael Maier's Atalanta Fugiens.

Return a JSON object with these fields:
{
  "figures": [
    {"name": "description", "position": "FOREGROUND|BACKGROUND|CENTER", "type": "human|animal|mythological|divine"}
  ],
  "objects": [
    {"name": "description", "position": "...", "symbolic_meaning": "brief alchemical significance"}
  ],
  "setting": "indoor|outdoor|mythological|abstract",
  "setting_details": "brief description of landscape/architecture",
  "composition": "brief note on visual arrangement",
  "dominant_action": "what is the central action or relationship depicted"
}
```

**Storage**: JSON string in `emblems.visual_elements`. Example:
```json
{
  "figures": [
    {"name": "Woman nursing", "position": "CENTER", "type": "human"},
    {"name": "Toad at breast", "position": "CENTER", "type": "animal"}
  ],
  "objects": [
    {"name": "Milk/liquid", "position": "CENTER", "symbolic_meaning": "Prima materia nourishment"}
  ],
  "setting": "outdoor",
  "setting_details": "Landscape with buildings in background",
  "composition": "Central figure group, landscape receding",
  "dominant_action": "Woman feeds toad at her breast, transferring vital essence"
}
```

**Rate limiting**: Process 1 image every 3 seconds (Claude API, not Wikimedia).

**Cost estimate**: ~51 images x ~$0.02/image = ~$1.02.

**Validation**: Compare `dominant_action` against existing `image_description` text for sanity check. Flag any where they disagree.

**UI surfacing**: The "What You See" section could be enhanced to show structured elements (figures list, setting, objects) instead of/alongside the prose description. Or keep prose for readability and use JSON for search/filtering.

**Effort**: ~60 min for script + run. API cost ~$1.

### Decision Needed
Whether to use the JSON column on `emblems` (simpler, current schema) or create the normalized `visual_elements` table (richer queries but more complex). **Recommendation**: Start with JSON column, migrate to table later if needed for cross-emblem visual queries.

---

## 3. Multi-Register Dictionary Definitions

### What
Populate the `registers` JSON column on `dictionary_terms` with De Jong's key insight: alchemical terms operate simultaneously across 4 registers (material/alchemical, medical, spiritual, cosmological).

### Current State
- `registers` column exists (TEXT, added by `migrate_v4_enrichment.py`) — 0/73 populated
- 73 dictionary terms, all with `definition_short`, `definition_long`, `label_latin`, `significance_to_af`
- De Jong's central contribution is showing how alchemical vocabulary is *deliberately polysemous* — a single term like "Nigredo" means:
  - **Alchemical**: blackening of matter in the vessel through putrefaction
  - **Medical**: melancholia, black bile, saturnine disease
  - **Spiritual**: dark night of the soul, death of the ego
  - **Cosmological**: Saturn's influence, winter, prima materia in chaos

### Schema
```json
{
  "alchemical": "Material/laboratory meaning — what happens in the vessel",
  "medical": "Humoral/healing meaning — bodily analogues",
  "spiritual": "Soul/psyche meaning — inner transformation",
  "cosmological": "Planetary/macrocosm meaning — universal correspondences"
}
```

### Which Terms Get Registers
Not all 73 terms are polysemous. The multi-register model applies primarily to:
- **PROCESS** terms (18): Nigredo, Albedo, Citrinitas, Rubedo, Calcination, Coniunctio, Dissolution, Sublimation, etc.
- **SUBSTANCE** terms (12): Mercury, Sulphur, Salt, Philosopher's Stone, Aqua Regia, etc.
- **FIGURE** terms (some of 16): Those with alchemical symbolism (Phoenix, Ouroboros, Hermaphrodite)

**Estimate**: ~40-50 terms warrant full 4-register entries. The remaining ~25 (SOURCE_TEXT entries like "Turba Philosophorum", MUSICAL terms, pure CONCEPT terms) get NULL registers.

### Approach
1. Read De Jong's emblem analyses for register-specific language
2. For each qualifying term, write 1-2 sentences per register
3. Store as JSON in `registers` column
4. Update `build_site.py` term page template to display registers as a tabbed or definition-list section

### UI Display
```html
<div class="register-tabs">
    <h3>Meanings Across Registers</h3>
    <dl class="register-list">
        <dt>Alchemical</dt>
        <dd>Blackening of matter in the vessel through putrefaction and decomposition.</dd>
        <dt>Medical</dt>
        <dd>Melancholia and black bile; the saturnine temperament requiring purgation.</dd>
        <dt>Spiritual</dt>
        <dd>The dark night of the soul; ego-death preceding spiritual rebirth.</dd>
        <dt>Cosmological</dt>
        <dd>Saturn's dominion; the chaos of prima materia before cosmic ordering.</dd>
    </dl>
</div>
```

**Effort**: ~90 min for content generation (LLM-assisted from corpus) + ~20 min for template.

---

## 4. Related Emblems Sidebar (Cross-Emblem Navigation)

*See Section 1A above for the emblem-page sidebar.*

This section covers the **broader cross-emblem navigation system** beyond just the sidebar.

### Source x Emblem Matrix (Separate Page)

See Section 5 below.

### Thematic Sequences
De Jong identifies several thematic sequences that cut across the numerical order:

| Sequence | Emblems | Theme |
|----------|---------|-------|
| King sequence | XXIV, XXVIII, XXXI, XLVIII | Royal death, dissolution, rebirth |
| Washing motif | III, XI, XIII, XLIII | Purification through water |
| Hermaphrodite series | XXX, XXXIII, XXXVIII | Union of opposites |
| Fire mastery | X, XVII, XVIII, XXIX | Control of elemental fire |
| Death/resurrection | XIX, XLI, XLIV, L | Sacrificial death, renewal |
| Mythological | IV, XXV, XXXIX, XLII | Classical myth as alchemical allegory |

**Implementation**: These could be surfaced as:
1. Named "pathways" on the home page (like chapters)
2. Tags on emblem pages (clickable, filtering the gallery)
3. A dedicated "Thematic Pathways" page with narrative introductions

**Data storage**: New table `emblem_sequences` or JSON in a config file. Simple enough for a config file initially.

**Effort**: ~45 min for data definition + template + page.

---

## 5. Source x Emblem Matrix Visualization

### What
An interactive grid showing which source authorities appear in which emblems. X-axis: 51 emblems (0-50). Y-axis: 15 source authorities. Cells colored by relationship type.

### Current State
- `emblem_sources` table has 138 links connecting emblems to source authorities
- `source_authorities` table has 15 entries with type classifications
- The data exists — this is purely a visualization task

### Design

**Page**: `/sources-matrix.html` (new page, linked from Sources nav or as a sub-page)

**Grid layout**:
```
                  F  I  II III IV  V  VI VII ... L
Turba             ●        ●          ●
Rosarium          ●  ●     ●  ●
Tabula Smaragdina              ●
Ovid                    ●        ●
...
```

**Cell encoding**:
- `●` filled = link exists
- Color by `relationship_type`:
  - MOTTO_SOURCE: dark accent (`#8b4513`)
  - DISCOURSE_CITATION: medium (`#d4a574`)
  - THEMATIC_PARALLEL: light (`#f0e6d3`)
  - NARRATIVE_SOURCE: blue-grey (`#6b7d8d`)
- Hover: tooltip showing authority name, emblem number, relationship type, notes

**Implementation options**:

**Option A: Pure HTML/CSS grid** (~30 min)
- Generate a `<table>` in `build_site.py`
- CSS `position: sticky` for headers
- No interactivity beyond hover tooltips
- Works on all browsers, no JS dependency

**Option B: JavaScript interactive grid** (~60 min)
- Generate data as JSON in `data.json`
- JS renders grid with click-to-filter, sort by authority type, highlight row/column
- Could use `<canvas>` for large grids or DOM for 15x51 (small enough for DOM)

**Recommendation**: Option A first (ship it), Option B as enhancement later.

**Data generation** (in `build_site.py`):
```python
def build_source_matrix(conn):
    authorities = conn.execute("SELECT id, name, type FROM source_authorities ORDER BY type, name").fetchall()
    emblems = conn.execute("SELECT id, number, roman_numeral FROM emblems ORDER BY number").fetchall()
    links = conn.execute("SELECT emblem_id, authority_id, relationship_type FROM emblem_sources").fetchall()
    # Build dict: (auth_id, emblem_id) -> relationship_type
    # Generate HTML table with colored cells
```

**Effort**: ~30-60 min depending on interactivity level.

---

## Priority Order for Future Sessions

| Priority | Feature | Effort | Impact | Dependencies |
|----------|---------|--------|--------|-------------|
| **P1** | Multi-register definitions | 90 min | Core scholarly value — De Jong's key insight | `registers` column exists |
| **P2** | Related emblems sidebar | 30 min | Cross-navigation, keeps users exploring | Data exists in DB |
| **P3** | Source x emblem matrix | 30-60 min | Visual overview of Maier's source network | Data exists in DB |
| **P4** | Thematic pathways | 45 min | Guided reading beyond numerical order | Needs sequence definitions |
| **P5** | Vision pipeline | 60 min | Structured visual analysis, search enablement | API cost ~$1 |
| **P6** | Stage-colored cards | 10 min | Subtle visual polish | Trivial |
| **P7** | Thematic browse filters | 45 min | Gallery UX improvement | Needs `data.json` extension |

### Suggested Session Plan
1. **Quick wins first**: P6 (10 min) + P2 (30 min) = 40 min for visible improvements
2. **Core scholarly value**: P1 (90 min) — the multi-register model is what makes this site unique
3. **Visualization**: P3 (30-60 min) — the matrix is a signature feature
4. **Defer**: P5 (vision) and P7 (browse filters) can wait — they're nice-to-have, not core
