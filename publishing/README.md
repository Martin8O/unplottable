# Publishing kit

Everything needed to share *Unplottable* on a fan-fiction archive (AO3,
FanFiction.net) or a forum. Prepared, not yet used — the decision to post is
the author's.

## The four golden rules

1. **Non-commercial, always.** Never sell it, never put it behind a paywall, no
   ads, no tips or donations tied to it. This is the single line that keeps
   non-commercial fan fiction safe.
2. **Disclose the AI.** The prose is AI-generated. Say so plainly (tag it
   *AI-Generated Work*, and keep the note in the posting). Some communities and
   fests do not accept AI-written fic at all — check each venue's rules first.
3. **Only first names, or a pseudonym.** Nothing here uses a surname. Consider
   posting under a pen name; decide with Sašenka before her name goes public.
4. **No trademarks.** No official logos or art. The cover is original.

## What's here

- [`ao3-posting-kit.md`](ao3-posting-kit.md) — copy-paste-ready metadata:
  summary, rating, tags, characters, and the beginning/end notes (with the AI
  disclosure and the disclaimer).

## The file to post

Build the book first:

```bash
powershell tools\build.ps1        # → build/unplottable.epub / .mobi / .pdf
```

- **AO3** doesn't import EPUB — you paste each chapter's text (or its HTML) into
  the "post new chapter" box. The chapters live in [`../manuscript/`](../manuscript/)
  as Markdown; convert a chapter to HTML with `pandoc manuscript\part-1\ch01-*.md -o ch01.html`
  and paste that. Post chapter by chapter, in order (see the manuscript folders).
- **FanFiction.net** works the same way (paste per chapter).
- To hand someone the finished object directly, send `build/unplottable.epub`
  (e-readers) or `build/unplottable.pdf`.

## Which venue

- **AO3** (Archive of Our Own) is the natural home — run by a fan non-profit,
  built for exactly this, permits AI works *if disclosed* (respect any fest or
  collection that bans them).
- **FanFiction.net** is the older, larger archive; fewer tags, laxer curation.
- A **subreddit or forum** (e.g. r/HPfanfiction) is for *sharing the link*, not
  hosting — post the story on AO3 first, then link it where the rules allow
  self-promotion and AI-disclosed work.
