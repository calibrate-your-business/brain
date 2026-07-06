# Sources -- the ingest contract

A SOURCE is anything that pumps material into the brain. Up to ~100 over time
(bookmarks, research dumps, transcripts, calendar, code, web clips, ...). The
brain stays one graph; sources are how the world gets in.

## Contract

A source MUST:
1. Write IMMUTABLE raw material into `raw/<name>/` (markdown, one file per item;
   minimal frontmatter incl. `source: <name>`). It never writes to `wiki/`.
2. Declare itself in `sources/<name>.source` (KEY=value, see schema below).
3. Be idempotent -- re-runs add/refresh, never duplicate.

The brain's intelligence pass reads `raw/<name>/` and compiles/links it into
`wiki/` with judgment. Sources provide material; Claude provides understanding.
(Mechanics vs strategy: a source is mechanics; compilation is strategy.)

## `<name>.source` schema

```
NAME=x-bookmarks
KIND=pull            # pull | watch | push | connector
RAW_DIR=raw/x-bookmarks
OWNER_REPO=calibrate-your-business/x-bookmarks   # where the source code lives
SCHEDULE=08:10       # if scheduled (via cyb tools/automations); blank if event-driven
CONTEXTS=research    # default context tag(s) for this source's material
NOTES=...            # one line
```

## Registered sources

- `x-bookmarks.source` -- **source #1**. X bookmarks pulled over CDP/browser-use,
  enriched, and exported as raw markdown here. Its code lives in the
  `x-bookmarks` repo (kept separate -- it is the TEMPLATE for a source).

## Adding a source

Create `raw/<name>/`, write a clean raw exporter in the owning repo that drops
markdown there, add `sources/<name>.source`, and (if scheduled) an
`automations/*.job` in the owning repo discovered by cyb `tools/automations`.
