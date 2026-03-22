# SWARMGUIDELINES.md — How to Run Multi-Agent Swarms in This Project

**Read this before launching any background agents.** Swarms are powerful for parallelizing work, but they have hard constraints that will waste time if ignored.

---

## The Hard Rule

**Background agents CANNOT run Bash commands.** This includes Python, sqlite3, npm, git, and any shell operation. The Claude Code permission system requires interactive user approval for shell access, and background agents can't prompt the user. They will stall indefinitely asking for Bash permission.

This has been confirmed across 10+ agent launches in this project.

---

## What Agents CAN Do

| Tool | Works? | Notes |
|------|--------|-------|
| Read | YES | Read any file — source corpus, DB schema, scripts, docs |
| Grep | YES | Search file contents — patterns in the De Jong corpus, etc. |
| Glob | YES | Find files by pattern |
| Write | YES | Create new files — staging files, scripts, reports |
| Edit | YES | Modify existing files |
| Bash | **NO** | Cannot run Python, sqlite3, or any shell command |
| Agent | YES | Can launch sub-agents (but they also can't run Bash) |

---

## Patterns That Work

### Pattern 1: Research Swarm (read-only)
**Use when:** You need to search the corpus for information across multiple sources.

```
AGENT A: Grep De Jong for Emblem I-X sections → Write findings to staging/dejong_1_10.json
AGENT B: Grep Tilton for Emblem references → Write findings to staging/tilton_refs.json
AGENT C: Grep Craven for biographical detail → Write findings to staging/craven_bio.json
         ↓
MAIN SESSION: Read staging files → Write integration script → Run it
```

**Why it works:** Agents only use Read/Grep/Write. No Bash needed.

### Pattern 2: Content Generation Swarm (staging files)
**Use when:** You need to generate prose content for many items in parallel.

```
AGENT A: Read corpus + Write staging/emblems_1_13.json (image_desc + discourse)
AGENT B: Read corpus + Write staging/emblems_14_26.json
AGENT C: Read corpus + Write staging/emblems_27_39.json
AGENT D: Read corpus + Write staging/emblems_40_50.json
         ↓
MAIN SESSION: Read staging/*.json → Write update script → Run it → Rebuild
```

**Why it works:** Agents write to staging files (not the DB). Main session handles all DB operations.

**Staging file format:**
```json
[
  {
    "emblem_number": 1,
    "image_description": "3-5 sentences...",
    "discourse_summary": "3-5 sentences..."
  },
  ...
]
```

### Pattern 3: Audit Swarm (report-only)
**Use when:** You need to check multiple things across the codebase.

```
AGENT A: Scan HTML for broken links → Write report
AGENT B: Read DB schema docs vs actual scripts → Write discrepancy report
AGENT C: Check CSS for mobile issues → Write report
         ↓
MAIN SESSION: Read reports → Fix issues → Rebuild
```

**Why it works:** Agents produce reports (text files). Main session acts on them.

---

## Patterns That FAIL

### Anti-Pattern 1: Agent Tries to Query DB
```
AGENT: python -c "import sqlite3; ..." → BLOCKED (needs Bash)
```
**Fix:** Pre-query the data in the main session and pass it to the agent via a file, OR have the agent write a script that the main session runs.

### Anti-Pattern 2: Agent Tries to Run Its Own Script
```
AGENT: Write scripts/update_emblems.py → python scripts/update_emblems.py → BLOCKED
```
**Fix:** Agent writes the script. Main session runs it after the agent completes.

### Anti-Pattern 3: Agent Tries to Rebuild the Site
```
AGENT: python scripts/build_site.py → BLOCKED
```
**Fix:** Rebuild is always a main-session operation. Agents never rebuild.

---

## Swarm Design Checklist

Before launching agents, verify:

- [ ] **No agent needs Bash.** If any step requires Python/sqlite3/shell, move it to the main session.
- [ ] **Outputs don't conflict.** Each agent writes to a different file or different DB rows.
- [ ] **Source files are read-only.** Agents read the corpus but never modify it.
- [ ] **Staging directory exists.** `mkdir -p staging/` before launching if agents will write there.
- [ ] **Merge step is planned.** Who reads the staging files and integrates them? (Always: the main session.)
- [ ] **Template/voice guide is referenced.** Tell agents to read `docs/WRITING_TEMPLATES.md` before generating content.

---

## Pre-Queried Data Pattern

If agents need DB data but can't query it, the main session can export it first:

```python
# Main session runs this BEFORE launching agents:
python -c "
import sqlite3, json
conn = sqlite3.connect('db/atalanta.db')
data = [dict(zip(['number','roman','label','motto_en','motto_lat','discourse','img_desc'],r))
        for r in conn.execute('SELECT number, roman_numeral, canonical_label, motto_english, motto_latin, discourse_summary, image_description FROM emblems ORDER BY number')]
with open('staging/emblem_data.json','w') as f: json.dump(data, f, indent=2)
"
```

Then tell agents: "Read `staging/emblem_data.json` for current emblem data."

---

## Alternative: Pre-Approve Bash Patterns

You can whitelist specific commands in `.claude/settings.local.json` so background agents can run them without prompting:

```json
{
  "permissions": {
    "allow": [
      "Bash(python scripts/*)",
      "Bash(python -c *)"
    ]
  }
}
```

**This has NOT been configured yet.** If you want swarms to run Python directly, add these patterns. But the staging-file pattern is safer and more predictable.

---

## Recommended Agent Prompt Template

When launching a content-generation swarm agent, include this in the prompt:

```
IMPORTANT: You CANNOT run Bash, Python, or any shell commands.
Write your output to a staging file instead:
  staging/{task_name}.json

Format: JSON array of objects with the fields specified below.
The main session will read your staging file and run the DB update.

Read `docs/WRITING_TEMPLATES.md` for voice rules and content standards.
```
