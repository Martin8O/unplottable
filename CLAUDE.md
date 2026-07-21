# CLAUDE.md — The Anomaly Engine (working title)

An original ~148k-word sci-fi novel set in the Harry Potter universe (fan fiction, English prose), built one prompt at a time. Gift for a trope-savvy HP-fanfic veteran reader; the quality bar is HERS. Martin (the user) knows no HP canon — **never ask him content questions**; content decisions are the assistant's, process/scope/vibes are his.

## Read first, every session
1. `Local/bootstrap.md` (current state, next step) → then the relevant `bible/` + `Local/Wiki/` sections for the prompt at hand.

## What this is
- Premise/era/structure: `docs/adr.md` (ADR-002/003) · full premise: `Local/Wiki/04-scifi-fusion-principles.md`.
- Plan of record: `Local/all prompts.md` · prompt standard: `Local/Prompts requirements.md`.

## Hard rules
- **C: drive forbidden** — all scratch/persistence on D: (`Local/scratch/` for probes). Never the harness scratchpad or `~/.claude`.
- **Canon tiers** (ADR-001): books 1–7 binding · Tier-2 per-use logged · **no Cursed Child**. Books win every conflict.
- **Bible-first** (ADR-004): no fact in prose without a `bible/` home, logged in the SAME prompt; manuscript never contradicts bible.
- **Ledger discipline**: twists/plants/payoffs only via `bible/foreshadowing-ledger.md`; front-matter `plants:`/`payoffs:` stay in sync (gate checks).
- **Hard story constraints** (ADR-002): no time travel on-page · no resurrection/undone deaths · Voldemort stays finished (and is never teased as the revenant by the narrative) · no magic-vs-military war porn · magic keeps its mystery · muggle tech stays 2033-plausible, the anomaly engine is NOT conscious · ending constructive.
- **Language**: prose + all repo text English (British English in-story; gate lints Americanisms); chat with Martin in Czech.
- `Local/` and `data/` never committed; commits happen only at wrap-up ("X is done" authorizes); scoped adds, no blind `git add -A`.
- Docs (`dev_history.md`, ADRs, bootstrap) change only at wrap-up, never mid-prompt.

## Conventions
- Chapters: `manuscript/part-N/chNN-slug.md` with YAML front-matter `chapter, part, title, pov, date_in_story, target_words, plants, payoffs, status`. Bands: target 3.8–4.6k, hard 3.2–5.2k words.
- POV: close 3rd past, one head per scene, dual leads; registers per `bible/style-guide.md` (until S4: `Local/Wiki/05-craft-standards.md`).
- Prose probes/experiments → `Local/scratch/` only, never committed, never reused verbatim.

## Run commands
- Quality gate: `python tools\gate.py` (green required before any commit) · `--cards` audits the grid · `--selftest` re-proves all 18 checks fire
- Build EPUB/PDF: `powershell tools\build.ps1` (pandoc not installed yet — deferred to E4)

## Workflow
"let's start «X»" → just-in-time refine + plan-mode OK → execute with verification DURING → "«X» is done" → lean wrap-up (gate, ADR, changelog, bootstrap head ≤5×5, model-fit line, scoped commit+push). Announce every next prompt with its tier + `▶ Spustit na: <model> · <effort>`. Details: `docs/writing-workflow.md`.
