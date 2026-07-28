# Writing workflow — how chapters get made

One prompt = one chapter (or one design/research slice). The loop:

1. **Refine** — re-read the previous chapter, the chapter card, open ledger items, relevant bible sections; finalize the prompt against the REAL manuscript state; present plan; get OK.
2. **Write** — draft to the card (goal → friction → turn → out-hook), inside the style guide; update front-matter; mark plants planted; log any new canon facts in `bible/invented-canon.md`.
3. **Verify (during, not after)** — `python tools\gate.py` green + card-quote table (prove goal/turn/out-hook landed) + canon citations for lore used + POV/continuity self-audit.
4. **Review** — human reads; iterate until happy. **If the review finds it not a fit** (voice drift, card not truly delivered, canon cast flattened, twist leaked or fumbled, verification thin): **re-run the prompt at a higher effort/model** — up the effort first (high → extra → max), then the stronger family — rather than patching in place. The card, plants and bible entries survive the re-run; only the prose is redrafted.
5. **Wrap-up** (on "done") — re-run gate; ADR row if a decision changed; changelog entry; bootstrap head update; model-fit retro line (`used … → fit | overkill | underkill`; an escalation reads `underkill → re-run at … → fit`); scoped commit + push.

**Part boundaries (WP prompts):** four-lens beta panel by fresh agents (canon pedant · fanfic veteran · prose critic · structure editor) + continuity sweep + ledger reconciliation + interlude + tier-recalibration retro.

**Whole-book (E phase):** cold-read twist audit, line edit per part, canon/Brit/lint sweep, typeset (EPUB/PDF), release-posture decision.

Model/effort per step follows the tier tags in the plan (`Local/all prompts.md`, private) via the shared model ladder. Tags read **`frontier · <effort>`** — a tier, not a model family (frontier = the strongest generally available Claude at the time); which family runs it is the author's call per run.
