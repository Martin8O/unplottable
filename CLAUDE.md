# CLAUDE.md — *Unplottable* (dev codename: The Anomaly Engine)

A ~124k-word science-fiction novel (300–400 printed A5 pages) set in the Harry Potter universe (fan fiction, English prose), built one prompt at a time. Original characters and plot; canon world. **Division of labour:** all content decisions — world, cast, turns, sentences — belong to the assistant; method, scope and pacing belong to the author, who does not know the source canon. **Never ask content questions**; decide, log the decision, and move on.

Editions: **English** (`manuscript/`, complete) · **Russian** «Белые пятна» (`Translation/RU/`, Rosman lexicon).

> `Local/` is a private, gitignored working area (session state, planning wiki, prompt plan, scratch). References to it below are real files on the author's machine and are deliberately not part of the public repository — see `docs/architecture.md`.

## Read first, every session
1. `Local/bootstrap.md` (current state, next step) → then the relevant `bible/` + `Local/Wiki/` sections for the prompt at hand.

## What this is
- Premise/era/structure: `docs/adr.md` (ADR-002/003) · full premise: `Local/Wiki/04-scifi-fusion-principles.md`.
- Plan of record: `Local/all prompts.md` · prompt standard: `Local/Prompts requirements.md`.

## Hard rules
- **C: drive forbidden** — all scratch/persistence on D: (`Local/scratch/` for probes). Never the harness scratchpad or `~/.claude`.
- **Canon tiers** (ADR-001): books 1–7 binding · Tier-2 per-use logged · **no Cursed Child**. Books win every conflict.
- **Bible-first** (ADR-004): no fact in prose without a `bible/` home, logged in the SAME prompt; manuscript never contradicts bible.
- **Ledger discipline**: twists/plants/payoffs only via `bible/foreshadowing-ledger.md`; front-matter `plants:`/`payoffs:` stay in sync (gate checks). The ledger closed at 18/18 — no new plants or payoffs, ever.
- **Hard story constraints** (ADR-002): no time travel on-page · no resurrection/undone deaths · Voldemort stays finished (and is never teased as the revenant by the narrative) · no magic-vs-military war porn · magic keeps its mystery · muggle tech stays 2033-plausible, the anomaly engine is NOT conscious · ending constructive.
- **Language**: prose and all repository text in English (British English in-story; the gate lints Americanisms). The Russian edition is the one exception, and it is confined to `Translation/RU/`.
- `Local/` and `data/` never committed; commits happen only at wrap-up ("X is done" authorizes); scoped adds, no blind `git add -A`.
- Docs (`dev_history.md`, ADRs, bootstrap) change only at wrap-up, never mid-prompt.

## Conventions
- Chapters: `manuscript/part-N/chNN-slug.md` with YAML front-matter `chapter, part, title, pov, date_in_story, target_words, plants, payoffs, status`. Bands: target 2.9–3.7k, hard 2.5–4.0k words (S6 rescale).
- POV: close 3rd past, one head per scene, dual leads; registers per `bible/style-guide.md`.
- Prose probes/experiments → `Local/scratch/` only, never committed, never reused verbatim.

## Run commands
- Quality gate: `python tools\gate.py` (green required before any commit) · `--cards` audits the grid · `--selftest` re-proves every check fires
- Build EPUB/MOBI/A5 PDF: `powershell tools\build.ps1` (add `-Root "Translation/RU" -Stem "belye-pyatna"` for the Russian edition)

## Workflow
"let's start «X»" → just-in-time refine + plan-mode OK → execute with verification DURING → "«X» is done" → lean wrap-up (gate, ADR, changelog, bootstrap head ≤5×5, model-fit line, scoped commit+push). Announce every next prompt with its tier + `▶ Run on: <model> · <effort>`. Details: `docs/writing-workflow.md`.
- **Model recs name a tier, not a family:** `frontier · <effort>` (frontier = strongest generally available Claude; family = the author's call per run). **If a run reviews as not a fit, re-run it at a higher effort/model — never patch weak prose in place** (high → extra → max, then the stronger family); card/plants/bible survive, only the prose is redrafted. Full rule: `Local/Prompts requirements.md` §4.
