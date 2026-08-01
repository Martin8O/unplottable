<div align="center">

<img src="book/cover.png" alt="Unplottable — cover" width="300">

# Unplottable

**an ~118k-word science-fiction novel, set in the Harry Potter universe, written one prompt at a time**

*developed under the codename **The Anomaly Engine***

`complete` · `EPUB · MOBI · A5 PDF` · `124,642 words` · `36 chapters + 5 interludes` · `English · Русский` · `non-commercial fan work`

</div>

---

> [!WARNING]
> **This repository spoils the whole book** — [`bible/`](bible/), [`dev_history.md`](dev_history.md), and [`docs/adr.md`](docs/adr.md) lay out the full plot, every twist, and the ending.
>
> ### 📖 Read *Unplottable* first
> **English — [download EPUB · MOBI · A5 PDF →](https://github.com/Martin8O/Unplottable/releases/tag/v1.0)** · or [read it here, chapter by chapter](manuscript/)
> **Русский — «Белые пятна» — [скачать EPUB · MOBI · PDF →](https://github.com/Martin8O/Unplottable/releases/tag/v1.1-ru)** · or [read it here](Translation/RU/manuscript/)
>
> The note, logline, and stats below are spoiler-free.

## A note from Martin

This book was, first of all, a gift for Sašenka — who once devoured fifteen *Harry Potter* fan-fics in a single month.

I have never read the books. I never even finished the first film. But I wanted to give her the best I could — so instead of writing the story myself, I built a *system* for an AI to write one worthy of her.

The system gave the AI a *bible* that held every fact of this world, a ledger that tracked each planted clue to the page where it pays, and a check that had to pass before any chapter was kept. Within that frame, everything else — the world, the characters, the turns, the very sentences — the AI chose, because I couldn't. The wish is mine; the story is the AI's.

The map was never empty. Now it holds one more place — and that one is hers.

## The book

> Britain, 2033. Adam Kessler, a Muggle machine-learning researcher, finds a fingerprint in the world's data that should not be there — structured, persistent, as if something has been patiently hiding from view. Orla Quinn, of the Ministry's Department of Mysteries, has one job: to make sure no one ever sees it. But a world that measures everything is a poor place to keep a secret, and the Statute of Secrecy that has held for three centuries is beginning to fail — not to a spell, but to statistics. The two people who understand it best stand on opposite sides of the same truth, and the only way out runs through each other.
>
> It is not a story about a war between magic and machines. It is a quiet thriller about secrecy — what it costs, who is owed the truth, and whether a secret can survive a world that can count even the things that are missing. The magic keeps its mystery; the near-future stays plausible; and every turn is meant to be *fair* — the kind you can walk back through afterwards and find, in plain sight the whole time, the sentence that was true when you first read it and truer once you knew.

## The book in numbers

<div align="center">

<img src="docs/unplottable-stats.png" alt="Unplottable — the build in numbers" width="720">

</div>

*Read straight from the git history and the manuscript. The image above is a snapshot — the **[live interactive dashboard →](https://martin8o.github.io/Unplottable/stats.html)** lets you hover any chapter and click a narrator to filter. Source: [`docs/stats.html`](docs/stats.html) · export: [PDF](docs/unplottable-stats.pdf).*

| | | | |
|---|--:|---|--:|
| Prose | **124,642 w** | Point of view | 2 (close 3rd) |
| Chapters | 36 | — Orla Quinn | 54.8% |
| Interludes | 5 | — Adam Kessler | 42.3% |
| Parts | 5 | Plants & payoffs | 18 / 18 paid |
| Typeset length | 299 A5 pp | Major twists (T1–T5) | 5 |
| In target word-band | 29 / 36 | Outside hard band | 0 |
| Build span | ~3.6 days | Commits | 52 |
| Bible & design docs | 94,848 w | Written | 20–24 Jul 2026 |

## How it was made

The novel was written one prompt at a time by an **AI (Claude)**, working inside a frame I built and then let run. I set the *method*, not the plot: I conceived the project, decided how it would be made, and defined the constraints and the quality bar — but not what happened inside the story. The world, the canon, the characters, and the sentences were the model's to choose, because I do not know this world at all. Coherence across 118k words came not from holding the whole story in memory, but from **externalising its structure into checkable artefacts**:

- **A bible** ([`bible/`](bible/)) — the single source of truth for characters, world-rules, plot architecture, and voice. No fact reached the prose without a home in the bible, logged in the same step; the manuscript therefore could never contradict its own world.
- **A foreshadowing ledger** — 18 plants and payoffs tracked in a table and mirrored in every chapter's front-matter, so a setup in chapter 3 connects to its payoff in chapter 33 *by record, not by memory*.
- **A quality gate** ([`tools/gate.py`](tools/gate.py)) — an automated linter (word bands, banned phrases, canon capitalisation, ledger cross-check, timeline consistency) that had to pass green before every commit. The style guide is *literally its configuration*, so the rules and their enforcement can never drift apart.
- **A phase workflow** — Research → Setup (premise, architecture, tooling) → Draft, chapter by chapter → per-part Review panels (four independent lenses, used as a fair-play instrument) → Edit (structure cold-read, line edit, canon sweep) → Typeset.

Front-loading the architecture meant the writing became "fill in the cells," and the coherence came from the plan, the ledger, and the gate — not from working memory. Across the whole project the escalation rule (*redraft a weak chapter, never patch it in place*) never once had to fire: under-delivery was caught in-run by the gate, not as a re-run.

## The Russian edition — «Белые пятна»

The whole book also exists in Russian, in [`Translation/RU/`](Translation/RU/) — *«Белые пятна»* ("Blank Spaces"), tagline *«Карта никогда не была пустой»*. It uses the **Rosman (Росмэн)** lexicon for every canon term, the translation the Russian-speaking fandom grew up on.

It was made the way the novel was not: not one prompt at a time, but as a **single background fan-out**. One agent first built a locked termbase and a Russian voice specification; then one agent per chapter translated, and a second agent per chapter adversarially checked its own side against the English — terminology, register, nothing dropped or added, every planted clue still fair — and fixed what it found. A cross-chapter consistency sweep closed it. Nobody on this side of the project reads Russian, so the pipeline had to be its own reviewer.

Honestly stated: this is the ceiling of a *fully automated* literary translation — a consistent termbase, preserved registers, per-chapter adversarial verification. It is very good. It is not a human literary translator's final polish. Details and the method: [`Translation/RU/README.md`](Translation/RU/README.md).

## Repository map

| Path | What it holds |
|---|---|
| [`bible/`](bible/) | The world's single source of truth — characters, world-rules, plot architecture, style guide, foreshadowing ledger |
| [`manuscript/`](manuscript/) | 36 chapters + 5 interludes (`part-N/chNN-slug.md`), each with YAML front-matter |
| [`Translation/RU/`](Translation/RU/) | The Russian edition — termbase, voice spec, and the full translated manuscript |
| [`book/`](book/) | Front/back matter, metadata, and the cover (`cover.png` + reproducible `cover.html` source) |
| [`tools/`](tools/) | `gate.py` (quality gate) · `build.ps1` (EPUB / MOBI / A5 PDF) |
| [`docs/`](docs/) | Decisions ([`adr.md`](docs/adr.md)), the writing workflow, and the stats dashboard |
| [`dev_history.md`](dev_history.md) | The full changelog — every prompt, decision, and model-fit note |

The planning wiki, the prompt plan, and all scratch work live in a private, gitignored `Local/` directory and are deliberately not published; documents here that point into it are pointing at notes, not at missing files.

## Build

```bash
python tools/gate.py            # quality gate — must be green before any commit
python tools/gate.py --selftest # prove every check still fires, on seeded bad input
powershell tools/build.ps1      # assemble → EPUB + MOBI + A5 PDF (with cover)
```

The build wraps the manuscript in the `book/` front/back matter, embeds the cover, and typesets the A5 PDF with a self-contained LaTeX engine (tectonic). Output lands in `build/` (gitignored). Add `-Root "Translation/RU" -Stem "belye-pyatna" -Title "Белые пятна"` to build the Russian edition instead.

## Authorship & AI disclosure

The **prose is AI-generated**: written by Claude (Anthropic) inside a method I designed and then let run. I conceived and commissioned the work and set its constraints and quality bar; the story, the canon, and the craft decisions were the model's, since I do not know this world. In short: **I built the frame; the AI wrote the book.** Per-prompt token consumption was not tracked in this repository — git records prose and decisions, not model usage.

## Rights & disclaimer

Unofficial fan fiction based on the *Harry Potter* series created by J. K. Rowling. No affiliation with, or endorsement by, the rights holders (J. K. Rowling, Warner Bros., Bloomsbury, Scholastic). **Non-commercial: no money is or will be made from this work.**

The wizarding world, and the canon characters who appear in it, belong to their owners. The original characters — Orla Quinn, Adam Kessler and the rest of the invented cast — together with the premise, the plot and the prose of this story are the work of this project and are published here to be read, not to be relicensed: no permission is granted to sell, republish, or train on this text. Everything else — the tooling, the bible, and the documentation of the method — may be freely reused with attribution.
