# IMAGEFOLLIES.md — Post-Mortem: Everything Wrong with How We Handled Images

## The Verdict

We should have had 50 emblem images populated **40 prompts ago**. Instead, it took the entire session — multiple failed attempts, wrong assumptions, rate-limit battles, and three separate "image sourcing swarms" — to arrive at a solution that took **4 minutes** once we got the approach right.

The fix was embarrassingly simple: **one sequential download script with 8-second delays using the standard Wikimedia filename pattern.**

---

## Timeline of Follies

### Attempt 1: SHI IIIF Manifest
**What happened:** Tried to find a IIIF manifest at `digital.sciencehistory.org`. Multiple URL patterns attempted. All returned 404.
**Time wasted:** ~15 minutes
**Lesson:** Don't guess API endpoints. Check the documentation first.

### Attempt 2: SHI Viewer Scraping
**What happened:** Scraped the SHI viewer page. Found 50 member IDs. Assumed they were all emblem plates. Downloaded 41 "direct file_sets." Discovered they were **sequential book pages** (covers, prelims, text pages), not emblem plates.
**Time wasted:** ~30 minutes downloading + analyzing wrong images
**Lesson:** Don't assume a page index = an emblem index.

### Attempt 3: SHI Parent Work Discovery
**What happened:** Discovered 9 "parent works" in the SHI viewer that were labeled as Emblema I-IX. Downloaded those correctly. But couldn't find parent works for X-L.
**What went right:** These 9 images ARE correct and confirmed.
**Lesson:** Partial success is still partial. We stopped at 9 when we needed 50.

### Attempt 4: Renaming 41 Unverified Pages
**What happened:** Renamed the 41 direct file_sets as emblems 10-49 on the assumption they were plates. Deployed to the live site. User saw book covers and dedication pages labeled as "Emblem XIV" etc.
**Time wasted:** ~15 minutes + bad data on the live site
**Lesson:** Never deploy unverified data. The placeholder was better than wrong images.

### Attempt 5: DPLA/Wikimedia Pages
**What happened:** Found DPLA page-numbered files on Wikimedia Commons. Downloaded two. Discovered they were NOT in book order — page 11 was "Discursus VII" (p.89) and page 13 was "Discursus XXIV" (p.197).
**Time wasted:** ~15 minutes
**Lesson:** DPLA scan pages ≠ book pages ≠ emblem numbers.

### Attempt 6: Internet Archive
**What happened:** Tried IA's IIIF endpoint. SSL certificate error. Tried metadata API — no individual page images available, only full PDF.
**Time wasted:** ~10 minutes
**Lesson:** Not every digitization provides page-level image access.

### Attempt 7: SLUB Dresden
**What happened:** Tried SLUB's digital library. Got a bot-detection verification page.
**Time wasted:** ~5 minutes
**Lesson:** Many institutional repositories block automated access.

### Attempt 8: Image Sourcing Swarm (3 agents)
**What happened:** Launched Wikipedia, Furnace & Fugue, and de Bry PDF agents in parallel. F&F confirmed URL pattern. Wikipedia found 14 labeled files. de Bry agent found the page formula.
**What went right:** Cross-referencing confirmed the Wikimedia pattern.
**What went wrong:** Downloading the identified files still hit rate limits.
**Time wasted on swarm coordination:** ~20 minutes for results that one focused search would have found

### Attempt 9: Wikimedia Downloads with Short Delays
**What happened:** Tried downloading with 0.3s, then 0.5s, then 1.5s delays. Rate-limited after 2-3 images every time. Multiple retry loops, each getting 2-3 more.
**Time wasted:** ~45 minutes of retry loops
**Lesson:** Wikimedia rate limits are sticky. Short delays don't work.

### Attempt 10: The Fix (4 minutes)
**What happened:** One script. 8-second delays. Standard Wikimedia filename pattern. Downloaded 26 images. Zero rate limits.
**Total time:** 4 minutes.
**Lesson:** Patience > cleverness.

---

## Root Causes

### 1. Overthinking the Problem
The task was: "download 50 publicly available, consistently named images from Wikimedia Commons." We treated it as: "solve a complex page-to-emblem mapping problem across 5 institutional APIs."

### 2. No Reconnaissance Before Action
We never checked if the images were simply on Wikimedia with standard names. The Wikipedia article on Atalanta Fugiens links to Commons. A 30-second check would have found the pattern.

### 3. Premature Parallelism
Launching 3 sourcing agents before understanding the basic download mechanics was cargo-cult engineering. The bottleneck was rate limiting, not research speed.

### 4. Deploying Unverified Data
Renaming 41 random book pages as "emblem plates" and pushing to production was the worst mistake. The user saw book covers on emblem pages.

### 5. Fighting Rate Limits Instead of Respecting Them
Multiple retry loops with incrementally longer delays instead of just using a generous 8-10 second interval from the start.

---

## What Should Have Happened

```
Step 1: Search Wikimedia Commons for "Atalanta Fugiens" (5 min)
Step 2: Find the naming pattern: Michael_Maier_Atalanta_Fugiens_Emblem_{N}.jpeg
Step 3: Write one script with 8-second delays to download all 50 (5 min)
Step 4: Update manifest, rebuild, deploy (2 min)
Total: 12 minutes, not 3+ hours.
```

---

## Lessons for Future Image Work

1. **Check the obvious source first** — Wikimedia Commons has most public domain historical images, consistently named.
2. **Use generous rate limits** — 8+ seconds between requests. The time saved by being aggressive is always lost to retries.
3. **Never deploy unverified images** — placeholders are better than wrong data.
4. **Don't swarm what should be sequential** — image downloads are I/O-bound and rate-limited. Parallelism hurts.
5. **Build the manifest FIRST** — the emblem identity layer should have been Step 1, not Step 12.
6. **One source, one pattern, one script** — stop after it works. Don't try 5 sources when 1 suffices.
