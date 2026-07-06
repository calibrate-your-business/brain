---
name: brain-ingest
description: Use to run the brain's ingest/compile pass -- compiling raw source items (bookmarks, articles, session transcripts) into synthesized wiki entity/concept pages in brain-db, or seeding a new context into the wiki. Fans out subagents partitioned by exclusive page write-ownership, then the orchestrator alone reconciles the index, rebuilds FTS, and lints links. Use when the owner says "run the ingest", "compile the new raw", "seed the <X> context into the brain", or when new raw has landed and the wiki is behind.
---

# brain-ingest


The ingest pass is the ONE place intelligence happens: sources export raw
(mechanics); this pass owns all understanding (judgment). Two regressions this
skill exists to prevent, both from real runs:
- Agents "normalized" `&` -> `and` in page titles and **orphaned 35 inbound
  links** -- titles are link targets (s:b3694406).
- `index.md` went stale (claimed 100 pages while the DB had 142) because a prior
  batch was never listed (s:b3694406).

**Announce at start:** "Using the brain-ingest skill." Data lives in brain-db;
the engine is the brain repo -- keep them straight.

## Step 1 -- Establish what's already compiled (never trust mtimes)

- Read `brain/ingest/INGEST.md` (the page-format + rules contract) end to end.
- Read `brain-db/log.md` (the record of what's been compiled) and recent git
  history. Detect un-ingested raw by diffing `log.md` + wiki provenance against
  the raw inventory -- NOT by mtimes (bulk imports flatten them).
- If nothing is new: do nothing. Say so and stop.

## Step 2 -- Plan the partition (exclusive page write-ownership)

- Cluster the new raw by the entity/concept pages it will touch.
- Assign each subagent a DISJOINT set of pages to write. No two agents may write
  the same file -- this is what makes the fan-out safe.
- Ingestion is selective and user-steered: only make a page when ~3+ items support
  it or a single item is high-signal. No bulk-import of legacy vaults.

## Step 3 -- Fan out compile subagents

Each subagent prompt MUST carry:
- Its exclusive page list, and: **"do NOT touch `index.md`, `log.md`, or `db/`"**
  (the orchestrator alone owns those).
- The INGEST.md contract: SYNTHESIZE, do not list; rewrite (don't append) existing
  pages; cross-link generously with `[[wikilinks]]`; cite provenance to raw items
  (`[[raw/<source>/...]]`); bi-temporal "(as of YYYY-MM, source)" on aging facts.
- **Never change an existing page's frontmatter `title`** -- titles are link
  targets. If a rename is genuinely needed, alias the old title, don't replace it.
- For seeding a scoped context (e.g. schedule-wrangler-ads): set the right
  `contexts:` list, a "for future Claude" preamble, and explicit PROHIBITIONS a
  critic can later grade against.

## Step 4 -- Orchestrator reconciles (the load-bearing part -- do NOT delegate)

As agents return, the orchestrator alone:
1. Reconciles overlaps and **restores any canonical titles** an agent changed;
   adds aliases for genuine renames and runs the broken-link check
   (`db/query.py broken` or equivalent) so no rename orphans inbound links.
2. **Rebuilds the derived index** from files (`python3 db/build_index.py` or the
   repo's builder); regenerate wholesale when stale and verify page COUNT against
   the rebuilt DB.
3. **Updates `index.md`** and appends a one-line entry to `log.md` naming what was
   compiled.
4. **Rebuilds FTS.**
5. Runs the link lint: orphans + broken wikilinks. Fix before finishing.

## Step 5 -- Land

Commit + push (brain-db is private; normal reversible step). Substantial compiles
can pass an adversarial critic (grades the pages + mechanically verifies
links/paths) before commit.

## Guardrails

- Agents own pages; the orchestrator owns `index.md` / `log.md` / `db/` / FTS.
  Cross this line and you get merge clobbers and a stale index.
- Every ingest ends by updating `index.md` and the lint -- a compile that skips
  reconciliation is not done.
- The KB gets synthesized rulebook pages, never daily operational time-series
  (run artifacts belong in `~/Library/Logs/`, not the wiki).
