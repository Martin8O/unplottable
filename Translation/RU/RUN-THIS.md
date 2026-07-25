# RUN THIS — finish the Russian edition (one prompt, new session)

## The one prompt to paste (new session, in this repo)

> **Přečti `Translation/RU/RUN-THIS.md` a proveď to celé — dokonči ruský překlad *Unplottable* (edice «Белые пятна», Rosman). Běž autonomně, na konci commitni a pushni.**

**Launch that session on `Fable 5 · high`.** (Pilot proved `max` over-deliberates and stalls; `high`
gives the same prose and actually finishes.)

---

## Context (for the session executing this)

Russian translation of *Unplottable* — subproject **«Kartograf»**, in-repo under `Translation/RU/`,
**Rosman (Росмэн) lexicon**. The foundation is done and committed:
- `Translation/RU/glossary.md` — the Rosman termbase (title chosen: **«Белые пятна»**, tagline **«Карта никогда не была пустой»**).
- `Translation/RU/style-ru.md` — the Russian voice spec (two registers, fragment voice, ты/вы, em-dash dialogue).
- `Translation/RU/manuscript/part-1/ch01-…md` — chapter 1 already translated **and** adversarially verified.

This is a **gift** for a Russian-reading recipient; there is **no human review step** — the pipeline
verifies itself. Rare imperfections at 124k-word scale are acceptable (the author's explicit call).
Everything below is autonomous.

## Step 1 — translate the remaining 40 chapters (the big run)

Fire the prepared fan-out workflow (translate + adversarial verify per chapter, Fable 5 · high):

```
Workflow({ scriptPath: "D:/Projekty/Fun Fic/Translation/RU/fanout.workflow.js" })
```

It runs in the background and notifies on completion. When it returns, inspect the result's
`flagged` array — for any chapter with `ok:false`, re-read that chapter and fix it (or re-run that
single unit). Everything is written to `Translation/RU/manuscript/part-*/…`.

## Step 2 — translate the short book matter → `Translation/RU/book/`

`metadata.yaml` and `cover.html` are **already prepared** in `Translation/RU/book/`. Translate the
three prose-matter files (Fable 5 · high; small agents or inline), preserving structure:
- `book/00-front.md` → `Translation/RU/book/00-front.md` — keep the ` ```{=latex} ` blocks **exactly**;
  translate the disclaimer prose to Russian; the dedication *For Sašenka* → **«Сашеньке»**.
- `book/99-afterword.md` → `Translation/RU/book/99-afterword.md` — translate the prose; heading
  *Afterword* → **«Послесловие»**; sign *— автор*.
- `book/zz-colophon.md` → `Translation/RU/book/zz-colophon.md` — Martin's first-person note; translate
  faithfully to Russian, keep the `\newpage` block, heading → **«Колофон»**, keep the numbers, sign
  **«С любовью, Мартин»**.

## Step 3 — render the Russian cover

`Translation/RU/book/cover.html` is ready (title «Белые пятна», Playfair Display = Cyrillic-capable).
Render it to `Translation/RU/book/cover.png` with headless Chrome:

```
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new --disable-gpu --hide-scrollbars `
  --no-first-run --user-data-dir="D:\tools\_chrome_profile" --force-device-scale-factor=2 `
  --window-size=1000,1600 --virtual-time-budget=8000 `
  --screenshot="D:\Projekty\Fun Fic\Translation\RU\book\cover.png" `
  "file:///D:/Projekty/Fun%20Fic/Translation/RU/book/cover.html"
```

Then **Read the PNG** to confirm «Белые пятна» fits and the Cyrillic renders (not tofu). If the title
overflows the plate, lower its `font-size` in `cover.html` and re-render.

## Step 4 — build the Russian EPUB / MOBI / PDF

`build.ps1` is parameterised; `gate.py --root` assembles the RU manuscript. Palatino Linotype covers
Cyrillic, so the same fonts work.

```
$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')
$env:TECTONIC_CACHE_DIR = 'D:\tools\tectonic\cache'
powershell -ExecutionPolicy Bypass -File tools\build.ps1 -Root "Translation/RU" -Stem "belye-pyatna" -Title "Белые пятна" -Format all
```

Verify: the EPUB opens, the body is Russian, no leaked LaTeX (`\newpage` etc.), the cover is embedded;
the PDF page count is sane (~300). Outputs land in `build/belye-pyatna.*` (gitignored).

## Step 5 — commit + release

- Scoped commit of `Translation/RU/` (manuscript + book matter + cover.png). `build/` stays gitignored.
- Update `Translation/RU/README.md` status checkboxes to done.
- Optionally add the three `build/belye-pyatna.*` files to the existing GitHub Release (or a new
  `v1.1-ru` release) so the Russian edition is downloadable, mirroring the English `v1.0`.
- Push.

## Model / effort

**Fable 5 · high** for the session and the translation/verify agents (already set inside
`fanout.workflow.js`). Not `max` (stalls), not `ultracode` (overkill for translation).
