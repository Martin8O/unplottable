# «Картограф» — Unplottable, Russian edition (Rosman)

Codename **Kartograf**. The Russian translation of *Unplottable*, living inside the main repo as a
subproject (not a separate repository). **Rosman (Росмэн) lexicon** for all Harry Potter canon terms —
never Spivak/Махаон.

## The goal of this translation

The **best achievable fully-automated translation**, at the **lowest possible cost in prompts, time
and attention** — it should run itself. Nobody on this side of the project reads Russian or knows the
source world, so there is nothing to review by hand: the pipeline must **verify its own quality**.

## How it runs — a background multi-agent workflow (not one-prompt-per-hour)

Instead of translating one chapter per session, the whole book is translated by a **single background
workflow** that fans out across all 41 chapters at once and checks itself. It is fired once; it runs
on its own and notifies when done.

| Phase | What runs | Agents |
|---|---|---|
| **F · Foundation** | one high-effort agent builds `glossary.md` (Rosman termbase: every canon term, every invented term/name/place → chosen Russian; the Russian title + tagline) and `style-ru.md` (the two POV registers + the "fragment" voice, in Russian) | 1 |
| **T · Translate** | one agent per chapter — reads the English source + the glossary + the style spec, writes the Russian chapter, preserving front-matter, structure, registers, and the fair-play clues | 41 |
| **V · Verify** | one agent per chapter — adversarially checks the Russian against the English + glossary (terminology, no English residue, voice, nothing dropped/added, fair-play intact) and **fixes issues in place** | 41 |
| **Assemble** | the main session builds the Russian EPUB / MOBI / A5 PDF (Palatino Linotype covers Cyrillic) with Russian front/back matter, and commits | — |

**Prompt cost: ~1.** One prompt fires the run; it is autonomous from there. (A cheap **Foundation +
1-chapter pilot** runs first to de-risk the pipeline before the full fan-out spends on all 41.)

## Layout

```
Translation/RU/
  README.md            ← this file
  glossary.md          ← Rosman termbase (built by Foundation)
  style-ru.md          ← Russian voice spec (built by Foundation)
  manuscript/part-*/   ← the translated chapters (mirrors ../../manuscript/)
  book/                ← Russian front/back matter + cover text
```

## Quality expectation (honest)

This is the ceiling for a **fully-automated** literary translation: a locked, consistent Rosman
termbase + register-preserving prose + per-chapter adversarial self-verification. It is very good; it
is not a human literary translator's final polish. A native-speaker pass would add the last few
percent — out of scope for the hands-off brief, available later if wanted.

## Status

- [x] Foundation — Rosman glossary + Russian style spec
- [x] Pilot — ch01 translated + adversarially verified (Fable 5 · high)
- [x] Full run — all 41 chapters translated + adversarially verified (Fable 5 · high, background fan-out) + cross-chapter consistency sweep
- [x] Russian front/back matter + cover + typeset (EPUB/MOBI/PDF)
- [x] Commit + release
