# Translate chapters — Russian, flow-first (reusable, one prompt)

The on-demand translation engine. Name any chapter(s); it translates them into the **flowing, readable
Russian** the native reader asked for (governed by `style-flow-brief.md`), each chapter checked by a
second pass. Story, plot, clues and twists are never touched — only the style flows.

## The prompt to paste (new session, this repo) — swap the chapters

> **Přelož ruský překlad *Unplottable*, kapitoly «6-10», plynulým stylem — proveď to podle `Translation/RU/TRANSLATE-CHAPTERS.md`.**

Chapter spec can be a range (`6-10`), a list (`6, 8, 15`), one (`12`), an interlude (`i2`), or `all`.

**▶ Run the session on `Fable · high`** (the engine is already set to it; `max` stalls, `ultracode` is overkill).

---

## What the executing session does

1. **Resolve the spec to chapter ids.** Chapters are `ch01`…`ch36`; interludes are `i1`…`i5`.
   `6-10` → `["ch06","ch07","ch08","ch09","ch10"]`; `all` → the string `"all"`.
2. **Set the target line** in `Translation/RU/translate.workflow.js`: edit the single line
   `const REQUESTED = []` to the ids (e.g. `const REQUESTED = ["ch06","ch07","ch08","ch09","ch10"]`,
   or `const REQUESTED = "all"`). Nothing else in that file changes.
3. **Run it:** `Workflow({ scriptPath: "D:/Projekty/Fun Fic/Translation/RU/translate.workflow.js" })`.
   It translates each chapter flow-first and verifies each (Fable · high), writing to
   `Translation/RU/manuscript/…`. It runs in the background and reports when done.
4. **Report back** for each chapter: story-intact? flows-now? de-personified? + the English
   back-translation of the first three paragraphs (so a non-Russian reader can judge).
5. **Commit** the produced Russian chapter files (scoped) and push. Reset the `REQUESTED` line back to
   `[]` so the file is clean for next time.

## Notes

- **Flow-first is the standard now.** `style-flow-brief.md` governs; `glossary.md` (Rosman) and
  `style-ru.md` (voice) still apply. If the native reader later asks to adjust the feel, edit
  `style-flow-brief.md` and re-run the affected chapters — same engine.
- **State of the book:** all 41 chapters already exist in Russian, but the first full pass was in the
  earlier (clipped) style; **`ch04` and `ch05` have been redone flow-first.** Use this tool to convert
  the rest — in batches you can send to the reader, or `REQUESTED = "all"` to redo the whole book.
- After the chapters are finalised, (re)build the Russian book with
  `powershell tools\build.ps1 -Root "Translation/RU" -Stem "belye-pyatna" -Title "Белые пятна"`.
