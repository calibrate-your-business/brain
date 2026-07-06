# session-learnings pass -- reusable prompt

The brain's intelligence pass over source #2 (`sessions`). Reusable: run standalone
(`claude -p "$(cat ingest/session-learnings.prompt.md)"` from the brain repo) or
fold into `brain-ingest`'s handling of `raw/sessions/`. Mechanics (capturing the
transcripts) is `ingest/capture_sessions.py`; THIS is the strategy.

---

You are the brain's **session-learnings pass**. Distill durable OPERATING
knowledge from Claude Code session transcripts so future sessions and the loops
critics stop repeating mistakes. The brain SYSTEM is the current repo; the DATA
is `$BRAIN_DB` (default `~/Claude/brain-db`).

## Input + delta

Read the session raw under `$BRAIN_DB/raw/sessions/<host>/*.md` -- one flattened
session each (`## user` / `## assistant` turns; frontmatter has `session_id`,
`project`, `date`). Process only sessions NEW or CHANGED since the last pass,
tracked by `$BRAIN_DB/raw/sessions/.last-learnings.json`
(`{ "processed": { "<session_id>": "<date>" } }`). If nothing is new, do nothing
and stop. Update the marker at the end.

## Mine each session through these ANGLES

Angle 0 is the pre-filter -- find the loud moments first, then widen around them.

0. **Corrections (the loudest signal).** Every user turn in ALL-CAPS, with
   profanity, or expressing frustration ("why are you", "STOP", "no", "that's
   wrong", "I've said this N times"). Each marks a moment the agent missed
   something that should have been obvious. Capture what the agent did, what it
   should have done, and the RULE that prevents recurrence.
1. **Arch-decisions.** Durable rulings the user made ("X is the source of truth",
   ownership, topology, a deploy pointer, a naming convention). These become canon.
2. **Process-omission.** The agent skipped an established process: no plan
   written, the loops harness unused, no adversarial critic, a required skill not
   invoked.
3. **Skill-signals.** A skill that should have been used but wasn't; recurring
   manual work that should BE a skill; a stale/wrong skill.
4. **Re-litigation.** The agent re-derived or re-opened a settled decision -- a
   signal a canon doc is missing.
5. **Tool-reinvention.** The agent rebuilt a helper/tool/pattern that already
   exists (DO-NOT-REINVENT).

For each learning record: `{ angle, session_id, project, what_happened (1-2
sentences, ABSTRACTED -- no secrets/PII/customer names), evidence (a short
scrubbed quote or pointer), rule (imperative, reusable), scope (a repo's
CLAUDE.md, or "brain-wiki" if cross-cutting), severity 1-5 (corrections floor at
3), recurrence_key (a normalized phrase for cross-session dedup) }`.

## Synthesize

- Dedup by `recurrence_key` ACROSS sessions. A rule seen in K sessions matters
  more than any single instance -- RAISE its severity and note the count.
- Resolve contradictions with judgment: a later user ruling supersedes an earlier
  one; record the resolution, not the flip-flop.

## Write (to `$BRAIN_DB`)

1. `wiki/concepts/operating-rules.md` -- the durable rules. REWRITE, don't append:
   integrate new learnings into the existing page, no stacked duplicates. Group by
   scope; each rule gets a one-line rationale and `[[provenance]]` to the session
   raw; cross-link related rules + anti-patterns.
2. `wiki/concepts/agent-anti-patterns.md` -- the recurring failure modes, each
   with its trigger, the miss, and the corrective rule.
3. `reports/claude-md/<date>.md` -- the **CLAUDE.md digest**: grouped by target
   repo, each item = `{ rule, rationale, PROPOSED CLAUDE.md text (ready to paste),
   source sessions }`. A RECOMMENDATION report.

## Rules of the pass

- **Report-only for CLAUDE.md.** Never edit a `CLAUDE.md` file; only recommend.
- **Privacy.** The wiki + digest hold LESSONS in the abstract. Never copy a
  secret, credential, customer name, or private business specific into them. Raw
  stays private in brain-db; the compiled rules are generalized.
- **Cite provenance** on every rule.
- **High-signal, not a log.** If unsure whether something is a durable rule vs a
  one-off, do NOT write it. `operating-rules.md` earns its reread.
- After writing, rebuild the index (`BRAIN_DB=$BRAIN_DB python3 db/build_index.py`)
  and commit+push brain-db non-interactively (only if there is a delta).

## Self-test (fixture)

The session `raw/sessions/<host>/2026-07-*__3541de34-*.md` (which built the
automations manager) MUST yield at least these rules:
- automations runs jobs; it is NOT a deployer -- an automation never touches prod.
- brain-db is the single corporate KB -- don't fragment it into per-project data repos.
- no interim restoration -- build the system; the jobs resume when it lands.
- validate a job for the CURRENT architecture before migrating it.
- don't reinvent an existing layer (the AI is brain-ingest, not a new engine).
- stop asking permission for reversible git operations -- land the work.

If the pass cannot recover those from that transcript, it is not working.
