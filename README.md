# Unplottable

*(working repo name: the-anomaly-engine)*

An original science-fiction novel set in the Harry Potter universe — a non-commercial fan work. Britain, 2033: the Statute of Secrecy is dying of data, and the two people who understand it best are on opposite sides of it.

**Status:** complete draft — line-edited, canon-swept, and typeset to **EPUB / MOBI / A5 PDF** with a cover. Private (a gift; not published).

- The prose contract: `bible/` · decisions: `docs/adr.md` · how it's written: `docs/writing-workflow.md`.
- Build: `python tools\gate.py` (quality gate, green required) · `powershell tools\build.ps1` → EPUB + MOBI + A5 PDF.

## The book in numbers

*Read straight from the git history and the manuscript. A visual dashboard lives at [`docs/stats.html`](docs/stats.html).*

| | |
|---|--:|
| Prose | **124,642 words** |
| Chapters | 36 |
| Interludes (in-world documents) | 5 |
| Parts | 5 |
| Points of view | 2 (close 3rd) |
| Foreshadowing plants & payoffs | 18 / 18 paid |
| Major twists (T1–T5) | 5 |
| Typeset length | 299 A5 pages |

**Manuscript** — average chapter 3,360 w · shortest ch20 *The Manor* 2,956 w · longest ch25 *The Apprentice* 3,824 w · **29 / 36 chapters inside the 2,900–3,700 target band, 0 outside the hard 2,500–4,000 band**. The five interludes total 3,667 w (avg 733).

**Point of view**

| POV | Words | Share |
|---|--:|--:|
| Orla Quinn | 68,274 | 54.8% |
| Adam Kessler | 52,701 | 42.3% |
| Interludes | 3,667 | 2.9% |

**Words per part**

| Part | Files | Words |
|---|--:|--:|
| I | 8 | 25,024 |
| II | 9 | 27,912 |
| III | 8 | 23,488 |
| IV | 8 | 23,657 |
| V | 8 | 24,561 |

**The build** — 20–24 July 2026, about **3.6 days end to end**, **52 commits** (peak 18/day), +10,480 / −720 lines. Phases: Research (4 prompts) → Setup (6) → Draft, 36 ch + 5 interludes (~30) → per-part Review (5) → Edit & ship (8).

**The iceberg** — beneath the 124,642 words a reader sees sits another **94,848 words** of bible and design docs (characters, world-rules, plot architecture, style guide, foreshadowing ledger). Nothing reached the page without a home in that bible, logged in the same step.

> *On tokens:* per-prompt token consumption is **not** tracked in this repository — git records prose and decisions, not model usage. The final prose ≈ 166k output tokens as a floor; true consumption (drafts, the bible, review panels, tool calls) is a large multiple of that.

**Disclaimer:** Unofficial fan fiction based on the Harry Potter series created by J.K. Rowling. No affiliation with, or endorsement by, the rights holders (J.K. Rowling, Warner Bros., Bloomsbury, Scholastic). Non-commercial; no money is or will be made from this work. All original characters and premise © this project's author; the Wizarding World remains the property of its owners.
