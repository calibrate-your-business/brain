# brain

A second brain you own end to end: plain markdown and git are the canonical
truth, and Claude is the intelligence on top -- it reads your material,
compiles it into a linked wiki, and opens every session already knowing you.

This repo is the ENGINE only. Your data -- the actual brain -- lives in a
separate directory you choose (the `BRAIN_DB` environment variable). Fork the
engine, point it at a folder, and it is yours.

## Quick start (let Claude do the setup)

1. Fork or clone this repo.
2. Open Claude Code in the repo directory.
3. Prompt: **"Read the README and set up my project."**

Claude follows the Setup section below: a short interview, a data directory,
a first source, a first index.

## Setup (for Claude)

You are setting up a new brain for its owner. Interview them as you go; do not
guess answers you can ask for.

1. **Pick the data directory.** Ask the owner where the brain's DATA should
   live. Any directory works: a plain folder is fine; a private git repo adds
   history and off-machine backup (nice, not required). Create it, set
   `BRAIN_DB` to its absolute path (persist it in their shell profile), and
   scaffold inside it: `raw/`, `wiki/entities/`, `wiki/concepts/`,
   `wiki/projects/`, `wiki/synthesis/`, and empty `index.md` and `log.md`.
2. **Seed the always-loaded context.** Run a short interview (5-10 questions:
   who they are, what they work on, what they want remembered, how they want
   you to operate) and write:
   - `$BRAIN_DB/CRITICAL_FACTS.md` -- roughly 120 tokens of essentials,
     loaded at the start of every session.
   - `$BRAIN_DB/PROFILE.md` -- the fuller profile: role, projects, people,
     preferences, working style.
3. **Wire a first source** (see `sources/README.md` for the contract). Offer
   two options:
   - [x-bookmarks](https://github.com/calibrate-your-business/x-bookmarks) --
     pulls the owner's X bookmarks into `raw/x-bookmarks/`. It is the
     template source; follow its README.
   - The simplest thing that works: create `$BRAIN_DB/raw/notes/`, register
     it as `sources/notes.source`, and tell the owner to drop any markdown
     file into `raw/notes/` -- one file per item, immutable once written.
4. **Build the index:** `BRAIN_DB=<path> python3 db/build_index.py`
   (stdlib-only Python 3; nothing to install).
5. **Run a first ingest pass.** Read `ingest/INGEST.md`, compile what is in
   `raw/` into `wiki/` pages with judgment, update `index.md` and `log.md`,
   then rebuild the index.
6. **Optionally schedule it.** The `automations/*.autojob` files here are
   discovered by the
   [automations](https://github.com/calibrate-your-business/automations)
   manager, but plain cron works the same:

   ```
   30 4 * * * cd <brain-repo> && BRAIN_DB=<path> \
     claude -p "Run the brain ingest pass: read ingest/INGEST.md and compile new raw into wiki"
   ```

   The intelligence passes run headless through the Claude Code CLI on a
   normal subscription -- no API key plumbing.

## The shape

Everything below lives under `$BRAIN_DB` except the engine code:

```
$BRAIN_DB/
  CRITICAL_FACTS.md   always-loaded essentials (~120 tokens)
  PROFILE.md          who the owner is -- loaded every session
  index.md            catalog of wiki pages
  log.md              append-only activity log
  raw/<source>/       immutable source material, one subdir per source
  wiki/               the COMPILED layer Claude writes and rewrites:
    entities/         people, orgs, tools, products
    concepts/         ideas, frameworks, techniques
    projects/         per-project / per-context notes
    synthesis/        cross-cutting write-ups
  db/brain.db         disposable cache (FTS + link graph), rebuilt any time

this repo (the engine):
  CLAUDE.md           operating manual: how Claude works the brain
  sources/            the ingest contract + one <name>.source per source
  ingest/             the intelligence passes (INGEST.md, session capture)
  db/                 build_index.py + query.py
  meta/               the knowledge model: methodology, schema, contexts
  automations/        *.autojob schedules (optional)
```

Sources drop immutable markdown into `raw/`; Claude compiles `raw/` into
`wiki/` with judgment, cross-linking pages with `[[wikilinks]]`. Git is the
only truth -- every derived index is a cache rebuilt from the files.

## Your data directory is just a directory

`BRAIN_DB` can be anything: `~/brain-data`, a synced folder, a private git
repo. The engine never assumes git for the data -- if you do use a repo you
get history and backup, and the scheduled jobs can commit for you, but a
plain folder works identically. Keep the data directory private; the engine
repo has nothing personal in it.

## Sources

A source is anything that pumps material in. The contract
(`sources/README.md`) is small: write immutable markdown, one file per item,
into `raw/<name>/`; declare yourself in `sources/<name>.source`; be
idempotent. Included:

- **x-bookmarks** (separate repo) -- pulls X bookmarks; the template to copy
  when writing your own source.
- **sessions** (built in) -- `ingest/capture_sessions.py` flattens your
  Claude Code session transcripts into raw markdown (secrets scrubbed), and
  `ingest/session-learnings.prompt.md` distills them into durable operating
  rules plus a CLAUDE.md recommendations digest.

## Retrieval

Claude queries the brain instead of scanning files:

```
python3 db/build_index.py                    # rebuild the cache from markdown
python3 db/query.py search "<terms>"         # ranked FTS over wiki (--raw for raw/)
python3 db/query.py links <slug>             # forward links + backlinks
python3 db/query.py orphans | broken         # graph lint
```

## Optional: Obsidian

`wiki/` and `raw/` are plain markdown with `[[wikilinks]]`. Open `$BRAIN_DB`
as an Obsidian vault and the graph view lights up for free. Nothing in the
engine depends on it -- it is a nice window, not a requirement.

## Works well with

Independent, but composable:

- [x-bookmarks](https://github.com/calibrate-your-business/x-bookmarks) --
  source #1 and the template for writing sources.
- [automations](https://github.com/calibrate-your-business/automations) --
  the scheduler that discovers the `*.autojob` files here.
- [loops](https://github.com/calibrate-your-business/loops) -- agent loops
  that use the brain as their memory and rulebook.

## Principles

- **One brain; context is a dimension.** Work vs research vs personal are
  scoped views over one graph, never separate vaults. The value is the
  connections across contexts.
- **Git (or the filesystem) is the only truth.** Every index is disposable.
- **Mechanics vs strategy.** Deterministic plumbing (capture, transport,
  scheduling) stays separate from intelligence (understanding). Never use a
  regex to do judgment's job.
- **Synthesis, not storage.** Wiki pages are rewritten as new raw lands --
  connected, compared, cited -- not appended to.
- **Selective, never bulk.** Material comes in deliberately, current and
  relevant only.

## License

MIT -- Copyright (c) 2026 Calibrate Your Business. See [LICENSE](LICENSE).
