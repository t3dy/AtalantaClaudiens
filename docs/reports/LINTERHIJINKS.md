# LINTERHIJINKS.md — What the Linter Does and Where It Lives

## What Happened

Several project files were modified "by the user or by a linter" during this session:
- `CLAUDE.md` — Updated with DOCUMENTAIRTRAFFICCONTROL.md reference, file tree corrections
- `docs/ONTOLOGY.md` — Added `[BUILT]`/`[PLANNED]` tags, documented `registers` column gap
- `PHASESTATUS.md` — Updated phase status, added image/manifest totals
- `docs/ROADMAP.md` — Added DOCUMENTAIRTRAFFICCONTROL.md reference
- `docs/PIPELINE.md` — Changed source_method from `LLM_ASSISTED` to `TEMPLATE_ASSEMBLY`

## Where the Linter Lives

Claude Code has a built-in hook system. The "linter" here is likely a **user-prompt-submit hook** or a manual edit by the user between agent turns. When Claude Code detects that a file it's working with was modified externally, it flags it with the system reminder:

> "Note: [file] was modified, either by the user or by a linter. This change was intentional."

This is Claude Code's way of saying: "something changed this file outside my control — don't revert it."

## What Actually Changed

The modifications were **substantive improvements**, not formatting lint:
- Added a `DOCUMENTAIRTRAFFICCONTROL.md` routing document (user created this)
- Added `[BUILT]`/`[PLANNED]` tags to ONTOLOGY.md tables (useful disambiguation)
- Fixed source_method terminology (`TEMPLATE_ASSEMBLY` is more accurate than `LLM_ASSISTED` for a script that uses no LLM)
- Updated totals in PHASESTATUS.md to match actual state

These are editorial improvements the user made while reviewing the agent's work.

## Suggestions for Better Linting

### 1. Pre-commit Hook (Git)
Add a `.git/hooks/pre-commit` or use `husky` to run checks before committing:
- JSON validation: `python -c "import json; json.load(open('atalanta_fugiens_seed.json'))"`
- HTML link checker: verify all `href` targets exist in `site/`
- Schema-doc alignment: compare `PRAGMA table_info()` against ONTOLOGY.md

### 2. Validate Script (already planned)
`scripts/validate.py` was in the original PIPELINE.md but never built. It should check:
- All 51 emblem pages exist
- All image paths in data.json resolve to files on disk
- No broken cross-links (dictionary → emblem, source → emblem)
- Manifest ↔ DB ↔ disk alignment

### 3. CI Validation
Add a validation step to `.github/workflows/deploy.yml` before the deploy:
```yaml
- name: Validate site
  run: python scripts/validate_identity.py
```

### 4. DOCUMENTAIRTRAFFICCONTROL.md
The user created this routing document — it tells agents which file to consult for any task. This is effectively a "lint for agent confusion" — preventing agents from reading stale or wrong docs.
