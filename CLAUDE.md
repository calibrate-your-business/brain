# brain -- operating manual (read this first, every session)

You are working inside the brain SYSTEM (the engine). The DATA -- `raw/`, `wiki/`,
`PROFILE.md`, `CRITICAL_FACTS.md`, `index.md`, `log.md` -- lives in a separate
PRIVATE repo, `brain-db` (sibling at `../brain-db`, or wherever `$BRAIN_DB`
points; default `~/Claude/brain-db`). You operate that data THROUGH this system:
read/write it under `$BRAIN_DB` and commit it THERE. This file is how you operate
the brain. (The user profile is `$BRAIN_DB/PROFILE.md`.)

## Session start: load context, cheaply

1. Read `$BRAIN_DB/CRITICAL_FACTS.md` (~120 tokens -- always).
2. Read `$BRAIN_DB/PROFILE.md` (who Karim is, how he wants you to work). This is
   why the brain exists: open every session already knowing him. Never make him
   re-explain himself.
3. Consult `$BRAIN_DB/index.md` for the wiki catalog; drill into specific pages on
   demand. Do NOT scan the whole vault -- that is what the index + per-context
   indexes are for.

## Retrieval -- use the derived index, do not scan files

`db/query.py` (over `$BRAIN_DB/db/brain.db`, a disposable cache rebuilt from the
brain-db markdown) is how you retrieve:
- `python3 db/query.py search "<terms>" [--context X] [--raw] [--limit N]` --
  ranked keyword (FTS) search over wiki pages, scopable to a context (e.g.
  `--context schedule-wrangler`), or `--raw` to search the raw corpus.
- `python3 db/query.py links <slug>` -- forward links + backlinks (graph).
- `python3 db/query.py orphans` / `broken` -- lint (pages nothing links to /
  link targets with no page).
- `python3 db/query.py page <slug>` -- the file path to open.
Rebuild after writing pages: `python3 db/build_index.py`. (Semantic/vector index
is deferred -- FTS + the link graph are the indexes today.)

## The layers (all under `$BRAIN_DB`)

- `raw/<source>/` -- IMMUTABLE source material (bookmarks, articles, transcripts,
  drops). You READ it; you never edit it. One subdir per source.
- `wiki/` -- the COMPILED layer, and the only place you WRITE knowledge:
  `entities/` (people/orgs/tools/products), `concepts/` (ideas/frameworks/
  techniques), `projects/` (per-project/context notes), `sources/` (one overview
  per source). REWRITE existing pages as new raw lands -- do not just append.
- `index.md` (catalog) and `log.md` (append-only activity log) -- keep current.

## How ingestion works (raw -> wiki, with JUDGMENT)

When new material lands in `raw/<source>/`: read it, then write/REWRITE the
matching `wiki/` entity and concept pages, cross-link with `[[wikilinks]]`,
update `index.md` and `log.md`. This is STRATEGY -- use understanding, not
pattern-matching. (The x-bookmarks ingest currently arrives pre-tagged by a
regex stopgap; treat those tags as hints only, and recompile with judgment. The
regex layer is being replaced -- see the spec.)

## Context is a dimension (not separate vaults)

Tag pages with `context/<name>` (e.g. `context/schedule-wrangler`,
`context/research`, `context/personal`). A "context" is a scoped VIEW + a
per-context index over THIS one graph -- never a separate brain. The point is
the connections that cross contexts (one entity, e.g. a customer, can appear in
research, product, and delivery at once -- keep it as one node).

## Note conventions (AI-first)

Every wiki note: frontmatter per `meta/frontmatter-schema.md`; a one-line "for
future Claude" preamble; `[[wikilinks]]` to related pages; provenance
(`[[raw/source#item]]` or source URL) on claims; recency markers
("(as of YYYY-MM, source)"); and where a fact changed, keep both when-believed
and when-revised. Optimize for your retrieval, not for pretty reading.

## Sensitivity

Customer PII and secrets get tagged `sensitive/pii` or `sensitive/secret` and
stay scoped (restricted subtree / scoped keys). Never inline a secret value;
never commit plaintext credentials. Keys, not prompts, control access.

## What NOT to do

- Do NOT bulk-import the old Obsidian vault or stale (Jan) business docs. Bring
  content in only when Karim directs, current/relevant only.
- Do NOT edit `raw/`. Do NOT use regex/rules to do understanding's job.
- Do NOT scan the whole vault when the index answers the question.
