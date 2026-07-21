# Architecture

A novel built like software: a single source of truth, a quality gate, and an ordered plan.

## Repo layout
```
bible/          story facts — the CONTRACT the prose must obey (characters, world rules,
                timeline, glossary, foreshadowing ledger, invented-canon log, style guide)
manuscript/     the novel: part-N/chNN-slug.md, one file per chapter, YAML front-matter
                (chapter, part, title, pov, date_in_story, target_words, plants, payoffs, status)
tools/          gate.py (one-command quality gate) · build.ps1 (pandoc → EPUB/PDF)
docs/           this file · adr.md (decision index) · writing-workflow.md
Local/          PRIVATE (gitignored): session brain, cookbook wiki, prompt plan, scratch
```

## The core principle: bible-first
Prose never introduces a fact without a home in `bible/`; the bible never contradicts the books (canon tiers: `docs/adr.md` ADR-001). Twists are accounted for in the foreshadowing ledger (every plant true-but-misread, every payoff planted ≥1 part earlier). This is the novelist's version of "contracts in one place".

## The quality gate (`python tools\gate.py`)
Front-matter schema · wordcount bands (2.9–3.7k target, 2.5–4.0k hard) · cliché/Americanism/filter-word lints · glossary spelling lint · ledger cross-check (front-matter plants/payoffs ↔ ledger rows) · timeline consistency. Green gate required before any wrap-up commit; content correctness is verified by per-chapter card checks + part-boundary beta panels (see writing-workflow.md) — the gate is necessary, never sufficient.

## Shape of the book
~118k words — **300–400 printed A5 pages**, the delivery unit the brief actually meant (ADR-003a) · 5 parts (Signal / Contact / Revenant / Bind / Statute) · 36 chapters + 5 interlude artefacts · dual close-3rd POV. Premise and canon policy: see adr.md.
