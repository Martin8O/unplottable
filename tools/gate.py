#!/usr/bin/env python3
"""Unplottable - the quality gate (S5).

One command, standard library only:

    python tools\\gate.py                 full run over manuscript/ against bible/
    python tools\\gate.py --cards         audit bible/chapter-grid.md itself
    python tools\\gate.py --selftest      prove every check fires on seeded bad input
    python tools\\gate.py --assemble F    write one book-shaped markdown file to F
    python tools\\gate.py PATH [PATH...]  check only these chapter files

Spec: `bible/style-guide.md` sections 7-9 (front-matter schema, enforced lists,
thresholds).  The style guide is the source of truth and is PARSED at run time:
the enforced lists in section 8 are never copied into this file, so extending a
list in the guide extends the gate.  Section 9's numbers live in THRESHOLDS
below, quoted from the guide.

Design notes (S5 decisions, recorded in Local/S5-decisions.md):
  * `status: stub` files are exempt from word bands and prose lints - the gate
    must run green on an unwritten scaffold; front-matter, card-mirror, ledger,
    timeline and scaffold checks still apply to them.
  * Prose scoping: markdown blockquote lines are ARTEFACT spans (memos, logs,
    labels, whole interludes).  Narration = prose minus dialogue minus artefacts.
    Hard blacklists run on everything; register thresholds run on narration.
  * Manner adverbs only (style-guide section 9): a whitelist of degree/focus/
    stance adverbs and -ly non-adverbs is excluded, re-derived here as the
    gate's own config.
  * Said-bookisms are tag-position aware: only a hit following a closing
    quotation mark counts as a tag ("breathed on her fingers" is an action).

Exit: 0 green (warnings allowed) - 1 hard violations - 2 gate could not run.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:  # keep em-dashes and fadas printable in a Windows console
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # pragma: no cover - older interpreters
    pass


# --------------------------------------------------------------------------
# configuration
# --------------------------------------------------------------------------

FM_KEYS = ["chapter", "part", "title", "pov", "date_in_story",
           "target_words", "plants", "payoffs", "status"]
STATUSES = ["stub", "draft", "revised", "final", "probe"]
PARTS = ["I", "II", "III", "IV", "V"]
PART_DIR = {"I": "part-1", "II": "part-2", "III": "part-3",
            "IV": "part-4", "V": "part-5"}

THRESHOLDS = {
    "chapter_hard": (2500, 4000),      # style-guide 3/9: hard band (S6 rescale)
    "chapter_target": (2900, 3700),    # target band -> warn outside
    "interlude": (500, 1000),          # interludes 500-1,000
    "adverbs_warn": 4.0,               # manner adverbs / 1k narration words
    "adverbs_fail": 6.0,
    "simile_per_300": 1.0,             # like a|as if|as though
    "italics_per_1k": 2.0,             # emphasis italics, artefacts excluded
    "glossary_min_uses": 3,            # recurring capitalised terms
}

# Manner-adverb whitelist (style-guide section 9 calibration).  Two families:
# -ly words that are not adverbs, and degree/focus/stance adverbs, which are
# load-bearing in Adam's calibrated register and are not the craft target.
LY_WHITELIST = {
    # -ly non-adverbs
    "only", "family", "early", "friendly", "unfriendly", "holy", "ugly",
    "silly", "belly", "jelly", "folly", "ally", "rally", "supply", "apply",
    "reply", "multiply", "likely", "unlikely", "lovely", "lonely", "deadly",
    "daily", "weekly", "monthly", "yearly", "elderly", "orderly", "ghastly",
    "costly", "curly", "surly", "burly", "grisly", "measly", "comely",
    "homely", "timely", "untimely", "kindly", "assembly", "anomaly", "italy",
    "july", "bully", "rely", "imply", "comply", "melancholy", "wobbly",
    # degree / focus / stance
    "nearly", "exactly", "entirely", "barely", "hardly", "merely", "really",
    "fully", "mostly", "partly", "roughly", "utterly", "completely",
    "absolutely", "truly", "totally", "usually", "actually", "equally",
    "probably", "possibly", "presumably", "arguably", "notably",
    "particularly", "especially", "essentially", "precisely", "approximately",
    "reportedly", "apparently", "evidently", "obviously", "clearly",
    "certainly", "surely", "scarcely", "simply", "slightly", "largely",
    "wholly", "purely", "solely", "namely", "formally", "technically",
    "eventually", "finally", "immediately", "currently", "recently",
    "originally", "previously", "already",
}

# American spellings beyond the guide's explicit americanisms list.
AM_SPELLING = [
    (re.compile(r"\b\w+iz(e|es|ed|ing|er|ers)\b", re.I), "-ize (house style: -ise)"),
    (re.compile(r"\b\w+ization(s)?\b", re.I), "-ization (house style: -isation)"),
    (re.compile(r"\b\w+yz(e|es|ed|ing)\b", re.I), "-yze (house style: -yse)"),
    (re.compile(r"\b(colors?|favorites?|honors?|labor|neighbors?|behaviors?|"
                r"rumors?|humor|armor|harbor|odors?|valor|vapor|savor|flavors?|"
                r"splendor|parlor)\b", re.I), "-or (house style: -our)"),
    (re.compile(r"\b(centers?|centered|theaters?|liters?|fibers?|somber|"
                r"specters?)\b", re.I), "-er (house style: -re)"),
    (re.compile(r"\b(traveled|traveling|canceled|canceling|modeled|modeling|"
                r"labeled|labeling|marveled|marveling|signaled|signaling)\b",
                re.I), "single -l- (house style: -ll-)"),
    (re.compile(r"\b(defense|offense|pretense)\b", re.I),
     "-se (house style: -ce)"),
]
AM_SPELLING_OK = {
    "seize", "seizes", "seized", "seizing", "size", "sizes", "sized",
    "sizing", "prize", "prizes", "prized", "capsize", "capsized", "resize",
    "resized", "resizes", "downsize", "oversize", "maize", "baize",
}

# Muggle is a proper noun in canon - always capitalised (WP5-routed to E4).
# Lowercase only; the negative look-behind spares 'smuggle', 'smuggled', etc.
MUGGLE_RE = re.compile(r"(?<![A-Za-z])muggle\w*")

SIMILE_RE = re.compile(r"\b(like an? |as if |as though )", re.I)
ITALIC_RE = re.compile(r"(?<![\*\w])\*([^*\n]+)\*(?!\*)")
CAPS_RE = re.compile(r"\b[A-Z][a-z]{2,}(?:[ -][A-Z][a-z]{2,})*\b")
SITE_RE = re.compile(r"\bSites?\s+(\d{1,2})\b")
LEDGER_ID_RE = re.compile(r"\bP-T\d-\d+[a-z]?\b")


# --------------------------------------------------------------------------
# reporting
# --------------------------------------------------------------------------

@dataclass
class Finding:
    level: str          # FAIL | WARN | INFO
    check: str
    where: str
    message: str


class Report:
    def __init__(self) -> None:
        self.items: list[Finding] = []

    def add(self, level: str, check: str, where: str, message: str) -> None:
        self.items.append(Finding(level, check, where, message))

    def fail(self, check, where, msg):
        self.add("FAIL", check, where, msg)

    def warn(self, check, where, msg):
        self.add("WARN", check, where, msg)

    def info(self, check, where, msg):
        self.add("INFO", check, where, msg)

    @property
    def fails(self) -> list[Finding]:
        return [f for f in self.items if f.level == "FAIL"]

    @property
    def warns(self) -> list[Finding]:
        return [f for f in self.items if f.level == "WARN"]

    def checks_fired(self) -> set[str]:
        return {f.check for f in self.items if f.level in ("FAIL", "WARN")}

    def render(self) -> None:
        order: list[str] = []
        for f in self.items:
            if f.where not in order:
                order.append(f.where)
        for where in order:
            block = [f for f in self.items if f.where == where]
            if not block:
                continue
            print(f"\n-- {where}")
            for f in block:
                tag = {"FAIL": "[FAIL]", "WARN": "[warn]", "INFO": "[info]"}[f.level]
                print(f"   {tag} {f.check}: {f.message}")


# --------------------------------------------------------------------------
# repo layout
# --------------------------------------------------------------------------

class Repo:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.bible = root / "bible"
        self.manuscript = root / "manuscript"
        self.guide = self.bible / "style-guide.md"
        self.grid = self.bible / "chapter-grid.md"
        self.ledger = self.bible / "foreshadowing-ledger.md"
        self.timeline = self.bible / "timeline.md"
        self.glossary = self.bible / "glossary.md"
        self.places = self.bible / "hidden-places.md"
        self.characters = self.bible / "characters.md"

    def read(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")


# --------------------------------------------------------------------------
# parsers - bible
# --------------------------------------------------------------------------

def parse_style_lists(text: str) -> dict[str, list[str]]:
    """Enforced lists from style-guide section 8 (### headings, one entry/line)."""
    lists: dict[str, list[str]] = {}
    in_section = False
    current: str | None = None
    for line in text.splitlines():
        if line.startswith("## 8."):
            in_section = True
            continue
        if in_section and line.startswith("## ") and not line.startswith("## 8."):
            break
        if not in_section:
            continue
        if line.startswith("### "):
            current = line[4:].split(" (")[0].strip()
            lists[current] = []
        elif current and line.strip() and not line.startswith(">"):
            lists[current].append(line.strip())
    return lists


@dataclass
class Card:
    cid: str                      # ch01 .. ch36 | I-1 .. I-5
    kind: str                     # chapter | interlude
    title: str
    part: str
    slug: str
    pov: str
    date: str
    target: int
    plants: list[str]
    payoffs: list[str]
    fields: dict[str, str] = field(default_factory=dict)
    meta_line: str = ""
    body: str = ""

    @property
    def filename(self) -> str:
        return f"{self.slug}.md"

    @property
    def relpath(self) -> str:
        return f"manuscript/{PART_DIR[self.part]}/{self.filename}"


def _meta_value(meta: str, key: str) -> str | None:
    for chunk in meta.split("·"):
        chunk = chunk.strip()
        if chunk.lower().startswith(key.lower() + " "):
            return chunk[len(key):].strip()
        if chunk.lower().startswith(key.lower() + ":"):
            return chunk[len(key) + 1:].strip()
    return None


def parse_cards(text: str) -> tuple[list[Card], dict[str, str]]:
    """Chapter/interlude cards + part titles from bible/chapter-grid.md."""
    part_titles: dict[str, str] = {}
    for m in re.finditer(r"^## Part (I{1,3}|IV|V) - .*?\*(.+?)\*", text, re.M):
        part_titles[m.group(1)] = m.group(2)
    for m in re.finditer(r"^## Part (I{1,3}|IV|V) — \*(.+?)\*", text, re.M):
        part_titles[m.group(1)] = m.group(2)

    cards: list[Card] = []
    blocks = re.split(r"^### ", text, flags=re.M)[1:]
    current_part = "I"
    for block in blocks:
        head, _, rest = block.partition("\n")
        head = head.strip()
        if "·" not in head:
            continue
        cid_raw, _, title = head.partition("·")
        cid_raw, title = cid_raw.strip(), title.strip()
        if not re.match(r"^(ch\d{2}|I-\d)$", cid_raw):
            continue
        m = re.search(r"^`(.+?)`", rest, re.M)
        if not m:
            continue
        meta = m.group(1)
        kind = "interlude" if cid_raw.startswith("I-") else "chapter"

        if kind == "chapter":
            part = (_meta_value(meta, "part") or "").split()[0]
            current_part = part
            pov = (_meta_value(meta, "POV") or "").split()[0]
            date = (_meta_value(meta, "date") or "").split()[0]
        else:
            part = current_part
            pov = "none"
            raw_date = _meta_value(meta, "date") or _meta_value(meta, "dates") or ""
            dates = re.findall(r"\b(\d{4}(?:-\d{2}(?:-\d{2})?)?)\b", raw_date)
            date = dates[-1] if dates else ""

        slug = (_meta_value(meta, "slug") or "").split()[0]
        target_raw = (_meta_value(meta, "target") or "0").split()[0]
        target = int(re.sub(r"[^\d]", "", target_raw) or 0)

        pl_line = ""
        for line in rest.splitlines():
            if line.startswith("**plants**"):
                pl_line = line
                break
        left, _, right = pl_line.partition("**payoffs**")
        plants = LEDGER_ID_RE.findall(left)
        payoffs = LEDGER_ID_RE.findall(right)

        fields: dict[str, str] = {}
        for line in rest.splitlines():
            if not line.lstrip().startswith("**"):
                continue
            parts = re.split(r"\*\*([a-z-]+)\*\*", line)
            for key, value in zip(parts[1::2], parts[2::2]):
                fields.setdefault(key, value.strip(" ·").strip())

        cards.append(Card(cid=cid_raw, kind=kind, title=title, part=part,
                          slug=slug, pov=pov, date=date, target=target,
                          plants=plants, payoffs=payoffs, fields=fields,
                          meta_line=meta, body=rest))
    return cards, part_titles


@dataclass
class LedgerRow:
    rid: str
    serves: str
    plant_ch: str
    payoff_ch: str
    status: str


def norm_ch(label: str) -> str:
    label = label.strip()
    m = re.match(r"^ch\.?\s*(\d{1,2})$", label, re.I)
    if m:
        return f"ch{int(m.group(1)):02d}"
    m = re.match(r"^(I-\d)$", label)
    if m:
        return m.group(1)
    return label


def parse_ledger(text: str) -> dict[str, LedgerRow]:
    rows: dict[str, LedgerRow] = {}
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 7 or not LEDGER_ID_RE.fullmatch(cells[0]):
            continue
        rows[cells[0]] = LedgerRow(rid=cells[0], serves=cells[1],
                                   plant_ch=norm_ch(cells[2]),
                                   payoff_ch=norm_ch(cells[5]),
                                   status=cells[6].lower())
    return rows


def parse_timeline(text: str) -> dict[str, tuple[str, str]]:
    """chapter id -> (pov letter, ISO date); chapter rows only."""
    out: dict[str, tuple[str, str]] = {}
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        m = re.fullmatch(r"ch(\d{2})", cells[0])
        if not m:
            continue
        out[cells[0]] = (cells[1], cells[2])
    return out


def parse_vocabulary(repo: Repo) -> tuple[set[str], set[str]]:
    """(capitalised words known to the bible, italic-legal spans)."""
    vocab: set[str] = set()
    italics: set[str] = set()
    for path in (repo.glossary, repo.characters, repo.places):
        if not path.exists():
            continue
        text = repo.read(path)
        vocab.update(w for w in re.findall(r"\b[A-Z][a-z]{2,}\b", text))
        italics.update(m.group(1).strip().lower()
                       for m in ITALIC_RE.finditer(text))
    return vocab, italics


def parse_sites(text: str) -> set[str]:
    labels: set[str] = set()
    for m in re.finditer(r"\|\s*Sites?\s+(\d{2})(?:\s*[-–]\s*(\d{2}))?", text):
        lo = int(m.group(1))
        hi = int(m.group(2)) if m.group(2) else lo
        for n in range(lo, hi + 1):
            labels.add(f"{n:02d}")
    return labels


# --------------------------------------------------------------------------
# parsers - manuscript
# --------------------------------------------------------------------------

@dataclass
class Chapter:
    path: Path
    rel: str
    fm: dict[str, object]
    fm_order: list[str]
    body: str
    errors: list[str]


def parse_front_matter(raw: str) -> tuple[dict[str, object], list[str], str, list[str]]:
    errors: list[str] = []
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?(.*)$", raw, re.S)
    if not m:
        return {}, [], raw, ["no YAML front-matter block"]
    fm_text, body = m.group(1), m.group(2)
    data: dict[str, object] = {}
    order: list[str] = []
    for line in fm_text.splitlines():
        if not line.strip():
            continue
        if line[:1].isspace():
            errors.append(f"indented/nested line not allowed: {line.strip()!r}")
            continue
        key, sep, value = line.partition(":")
        if not sep:
            errors.append(f"not a key: value line: {line.strip()!r}")
            continue
        key = key.strip()
        value = value.strip()
        if " #" in value:
            value = value.split(" #", 1)[0].strip()
        order.append(key)
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [x.strip().strip("'\"") for x in inner.split(",") if x.strip()]
        else:
            data[key] = value.strip("'\"")
    return data, order, body, errors


def load_chapters(repo: Repo) -> list[Chapter]:
    out: list[Chapter] = []
    if not repo.manuscript.exists():
        return out
    for path in sorted(repo.manuscript.glob("part-*/*.md")):
        raw = repo.read(path)
        fm, order, body, errors = parse_front_matter(raw)
        rel = path.relative_to(repo.root).as_posix()
        out.append(Chapter(path=path, rel=rel, fm=fm, fm_order=order,
                           body=body, errors=errors))
    return out


# --------------------------------------------------------------------------
# text scoping
# --------------------------------------------------------------------------

@dataclass
class Scopes:
    body: str        # comments stripped
    prose: str       # body minus artefact (blockquote) lines
    narration: str   # prose minus dialogue
    dialogue: str
    artefact: str
    words: int


def scope_text(body: str) -> Scopes:
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
    prose_lines, art_lines = [], []
    for line in body.splitlines():
        (art_lines if line.lstrip().startswith(">") else prose_lines).append(line)
    prose = "\n".join(prose_lines)
    dialogue = " ".join(re.findall(r'"([^"\n]*)"', prose))
    narration = re.sub(r'"[^"\n]*"', " ", prose)
    words = len(re.findall(r"[A-Za-zÀ-ɏ'’-]+", body))
    return Scopes(body=body, prose=prose, narration=narration,
                  dialogue=dialogue, artefact="\n".join(art_lines), words=words)


def pattern_hits(text: str, entry: str) -> list[str]:
    """Word-boundary, case-insensitive; '*' = wildcard inside one sentence."""
    parts = [re.escape(p) for p in entry.split("*")]
    rx = re.compile(r"\b" + r"\b[^.!?\n]{0,60}?\b".join(parts) + r"\b", re.I)
    return [m.group(0) for m in rx.finditer(text)]


def bookism_tag_hits(text: str, bookisms: list[str]) -> list[str]:
    """Only hits in TAG position: after a closing quotation mark, same sentence."""
    hits: list[str] = []
    if not bookisms:
        return hits
    rx = re.compile(r"\b(" + "|".join(re.escape(b) for b in bookisms) + r")\b", re.I)
    for qm in re.finditer(r'[\.,!?—-]"', text):
        window = text[qm.end():qm.end() + 70]
        window = window.split('"')[0].split("\n")[0]
        for hm in rx.finditer(window):
            hits.append(hm.group(0))
    return hits


# --------------------------------------------------------------------------
# checks
# --------------------------------------------------------------------------

def check_front_matter(ch: Chapter, rep: Report) -> None:
    for err in ch.errors:
        rep.fail("front-matter", ch.rel, err)
    if not ch.fm:
        return
    if ch.fm_order != FM_KEYS:
        missing = [k for k in FM_KEYS if k not in ch.fm_order]
        extra = [k for k in ch.fm_order if k not in FM_KEYS]
        detail = []
        if missing:
            detail.append(f"missing {missing}")
        if extra:
            detail.append(f"unknown {extra}")
        if not detail:
            detail.append(f"wrong order {ch.fm_order}")
        rep.fail("front-matter", ch.rel,
                 "schema (style-guide 7): " + "; ".join(detail))
    cid = str(ch.fm.get("chapter", ""))
    if not re.fullmatch(r"([1-9]|[12]\d|3[0-6])|I-[1-5]|P-[1-3]", cid):
        rep.fail("front-matter", ch.rel, f"chapter: {cid!r} not 1-36 / I-1..I-5")
    if str(ch.fm.get("part", "")) not in PARTS:
        rep.fail("front-matter", ch.rel, f"part: {ch.fm.get('part')!r} not I..V")
    if str(ch.fm.get("pov", "")) not in ("Orla", "Adam", "none"):
        rep.fail("front-matter", ch.rel, f"pov: {ch.fm.get('pov')!r} not Orla|Adam|none")
    date = str(ch.fm.get("date_in_story", ""))
    if not re.fullmatch(r"\d{4}(-\d{2}(-\d{2})?)?", date):
        rep.fail("front-matter", ch.rel, f"date_in_story: {date!r} not ISO")
    elif len(date) != 10 and str(ch.fm.get("pov")) != "none":
        rep.fail("front-matter", ch.rel,
                 f"date_in_story: {date!r} - chapters need a full ISO date")
    tw = str(ch.fm.get("target_words", ""))
    if not tw.isdigit():
        rep.fail("front-matter", ch.rel, f"target_words: {tw!r} not an integer")
    for key in ("plants", "payoffs"):
        val = ch.fm.get(key)
        if not isinstance(val, list):
            rep.fail("front-matter", ch.rel, f"{key}: must be a flow list ([] if none)")
        else:
            for rid in val:
                if not LEDGER_ID_RE.fullmatch(str(rid)):
                    rep.fail("front-matter", ch.rel, f"{key}: {rid!r} is not a ledger id")
    if str(ch.fm.get("status", "")) not in STATUSES:
        rep.fail("front-matter", ch.rel,
                 f"status: {ch.fm.get('status')!r} not {'|'.join(STATUSES)}")


def check_card_mirror(ch: Chapter, card: Card | None, rep: Report) -> None:
    if card is None:
        rep.fail("card-mirror", ch.rel, "no card in bible/chapter-grid.md for this file")
        return
    got_part = str(ch.fm.get("part", ""))
    if got_part != card.part:
        rep.fail("card-mirror", ch.rel, f"part {got_part!r} != card {card.part!r}")
    elif ch.path.parent.name != PART_DIR[card.part]:
        rep.fail("card-mirror", ch.rel,
                 f"file sits in {ch.path.parent.name}, card says {PART_DIR[card.part]}")
    if str(ch.fm.get("title", "")) != card.title:
        rep.fail("card-mirror", ch.rel,
                 f"title {ch.fm.get('title')!r} != card {card.title!r}")
    if card.kind == "chapter" and str(ch.fm.get("pov", "")) != card.pov:
        rep.fail("card-mirror", ch.rel,
                 f"pov {ch.fm.get('pov')!r} != card {card.pov!r}")
    if str(ch.fm.get("date_in_story", "")) != card.date:
        rep.fail("card-mirror", ch.rel,
                 f"date_in_story {ch.fm.get('date_in_story')!r} != card {card.date!r}")
    if str(ch.fm.get("target_words", "")) != str(card.target):
        rep.fail("card-mirror", ch.rel,
                 f"target_words {ch.fm.get('target_words')!r} != card {card.target}")
    for key, want in (("plants", card.plants), ("payoffs", card.payoffs)):
        got = ch.fm.get(key)
        if isinstance(got, list) and [str(x) for x in got] != want:
            rep.fail("card-mirror", ch.rel,
                     f"{key} {got} != card {want} (grid is the contract)")


def check_word_band(ch: Chapter, card: Card | None, sc: Scopes, rep: Report) -> None:
    status = str(ch.fm.get("status", ""))
    if status in ("stub", "probe"):
        return
    kind = card.kind if card else "chapter"
    if kind == "interlude":
        lo, hi = THRESHOLDS["interlude"]
        if not (lo <= sc.words <= hi):
            rep.fail("word-band", ch.rel,
                     f"{sc.words} words outside interlude band {lo}-{hi}")
        return
    hlo, hhi = THRESHOLDS["chapter_hard"]
    tlo, thi = THRESHOLDS["chapter_target"]
    if not (hlo <= sc.words <= hhi):
        rep.fail("word-band", ch.rel,
                 f"{sc.words} words outside hard band {hlo}-{hhi}")
    elif not (tlo <= sc.words <= thi):
        rep.warn("word-band", ch.rel,
                 f"{sc.words} words outside target band {tlo}-{thi}")


def check_lists(ch: Chapter, sc: Scopes, lists: dict[str, list[str]],
                rep: Report) -> None:
    if str(ch.fm.get("status", "")) == "stub":
        return
    hard = [("banned-phrases", sc.body), ("fanon-terms", sc.body),
            ("americanisms", sc.body)]
    for name, scope in hard:
        hits: list[str] = []
        for entry in lists.get(name, []):
            hits += pattern_hits(scope, entry)
        if hits:
            rep.fail(name, ch.rel, ", ".join(sorted({f"'{h}'" for h in hits})))

    soft = [("fanon-watch", sc.body), ("filter-words", sc.narration),
            ("epithets", sc.narration)]
    for name, scope in soft:
        hits = []
        for entry in lists.get(name, []):
            hits += pattern_hits(scope, entry)
        if hits:
            rep.warn(name, ch.rel,
                     f"{len(hits)} hit(s), review in context: "
                     + ", ".join(sorted({f"'{h}'" for h in hits})))

    tag_hits = bookism_tag_hits(sc.prose, lists.get("said-bookisms", []))
    if tag_hits:
        rep.warn("said-bookisms", ch.rel,
                 "in tag position: " + ", ".join(sorted({f"'{h}'" for h in tag_hits})))

    am: list[str] = []
    for rx, label in AM_SPELLING:
        for m in rx.finditer(sc.body):
            if m.group(0).lower() in AM_SPELLING_OK:
                continue
            am.append(f"'{m.group(0)}' ({label})")
    if am:
        rep.fail("am-spelling", ch.rel, ", ".join(sorted(set(am))))

    mug = sorted({m.group(0) for m in MUGGLE_RE.finditer(sc.body)})
    if mug:
        rep.fail("muggle-cap", ch.rel,
                 ", ".join(f"'{h}' (canon: capitalise)" for h in mug))


def check_thresholds(ch: Chapter, sc: Scopes, italics_ok: set[str],
                     rep: Report) -> None:
    if str(ch.fm.get("status", "")) == "stub" or sc.words < 50:
        return
    narration_words = len(re.findall(r"[A-Za-z'’-]+", sc.narration)) or 1
    ly = [w for w in re.findall(r"\b[A-Za-z]+ly\b", sc.narration)
          if w.lower() not in LY_WHITELIST]
    per_k = len(ly) / narration_words * 1000
    if per_k > THRESHOLDS["adverbs_fail"]:
        rep.fail("adverbs", ch.rel,
                 f"manner adverbs {per_k:.1f}/1k (fail > {THRESHOLDS['adverbs_fail']}): "
                 + ", ".join(sorted(set(ly))[:12]))
    elif per_k > THRESHOLDS["adverbs_warn"]:
        rep.warn("adverbs", ch.rel,
                 f"manner adverbs {per_k:.1f}/1k (warn > {THRESHOLDS['adverbs_warn']}): "
                 + ", ".join(sorted(set(ly))[:12]))

    sim = SIMILE_RE.findall(sc.prose)
    per300 = len(sim) / max(sc.words, 1) * 300
    if per300 > THRESHOLDS["simile_per_300"]:
        rep.warn("similes", ch.rel,
                 f"{len(sim)} simile markers = {per300:.2f}/300w "
                 f"(budget {THRESHOLDS['simile_per_300']})")

    # Emphasis italics only (style-guide 9, S5 refinement): incantations and
    # publication titles are legal italics; in-prose artefact quotations
    # (a clause or more of a memo, label, docket) and label glyphs like *(?)*
    # are artefact spans, not emphasis.
    emphasis = []
    for m in ITALIC_RE.finditer(sc.prose):
        span = m.group(1).strip()
        if span.lower() in italics_ok:
            continue
        if not re.search(r"[A-Za-z]", span):
            continue
        if len(span.split()) > 6:
            continue
        emphasis.append(span)
    per1k = len(emphasis) / max(sc.words, 1) * 1000
    if per1k > THRESHOLDS["italics_per_1k"]:
        rep.warn("italics", ch.rel,
                 f"{len(emphasis)} emphasis italics = {per1k:.1f}/1k "
                 f"(budget {THRESHOLDS['italics_per_1k']}; artefact spans excluded)")


def check_glossary(ch: Chapter, sc: Scopes, vocab: set[str], rep: Report) -> None:
    if str(ch.fm.get("status", "")) == "stub":
        return
    counts: dict[str, int] = {}
    for line in sc.prose.splitlines():
        for m in CAPS_RE.finditer(line):
            before = line[:m.start()].rstrip()
            sentence_initial = (not before or before[-1] in ".!?—-:;"
                                or before.endswith('"'))
            term = m.group(0)
            if sentence_initial:
                # the leading word is capitalised by position, not by name;
                # anything after it still counts (e.g. "The Thaumic Board")
                words = term.split(" ")
                if len(words) < 2:
                    continue
                term = " ".join(words[1:])
            counts[term] = counts.get(term, 0) + 1
    unknown = []
    for term, n in sorted(counts.items()):
        if n < THRESHOLDS["glossary_min_uses"]:
            continue
        if all(w in vocab for w in re.split(r"[ -]", term)):
            continue
        unknown.append(f"{term} (x{n})")
    if unknown:
        rep.warn("glossary", ch.rel,
                 "recurring capitalised term(s) missing from bible/glossary.md: "
                 + ", ".join(unknown))


def check_sites(ch: Chapter, sc: Scopes, allowed: set[str], rep: Report) -> None:
    if str(ch.fm.get("status", "")) == "stub":
        return
    bad = sorted({m.group(1).zfill(2) for m in SITE_RE.finditer(sc.body)} - allowed)
    if bad:
        rep.fail("sites", ch.rel,
                 "site label(s) with no row in bible/hidden-places.md: "
                 + ", ".join(f"Site {b}" for b in bad))


def check_ledger(chapters: list[Chapter], cards: list[Card],
                 rows: dict[str, LedgerRow], complete: bool, rep: Report) -> None:
    where = "bible/foreshadowing-ledger.md"
    valid_status = {"planned", "planted", "paid", "cut"}
    for rid, row in rows.items():
        if row.status not in valid_status:
            rep.fail("ledger", where,
                     f"{rid}: status {row.status!r} not {sorted(valid_status)}")

    claimed_plants: dict[str, list[str]] = {}
    claimed_payoffs: dict[str, list[str]] = {}
    for ch in chapters:
        cid = card_id_for(ch)
        for rid in ch.fm.get("plants", []) or []:
            rid = str(rid)
            claimed_plants.setdefault(rid, []).append(cid)
            row = rows.get(rid)
            if row is None:
                rep.fail("ledger", ch.rel, f"plants: {rid} has no ledger row")
            elif row.plant_ch != cid:
                rep.fail("ledger", ch.rel,
                         f"plants: {rid} is planted in {row.plant_ch} per the ledger")
        for rid in ch.fm.get("payoffs", []) or []:
            rid = str(rid)
            claimed_payoffs.setdefault(rid, []).append(cid)
            row = rows.get(rid)
            if row is None:
                rep.fail("ledger", ch.rel, f"payoffs: {rid} has no ledger row")
            elif row.payoff_ch != cid:
                rep.fail("ledger", ch.rel,
                         f"payoffs: {rid} pays in {row.payoff_ch} per the ledger")

    if not complete:
        rep.info("ledger", where,
                 "manuscript incomplete - ledger completeness check deferred")
        return
    for rid, row in rows.items():
        if row.status == "cut":
            continue
        if rid not in claimed_plants:
            rep.fail("ledger", where,
                     f"{rid}: no chapter front-matter plants it (ledger says {row.plant_ch})")
        if rid not in claimed_payoffs:
            rep.fail("ledger", where,
                     f"{rid}: no chapter front-matter pays it (ledger says {row.payoff_ch})")


def check_timeline(chapters: list[Chapter], tl: dict[str, tuple[str, str]],
                   rep: Report) -> None:
    where = "bible/timeline.md"
    dated: list[tuple[str, str, str]] = []   # (cid, pov, date)
    for ch in chapters:
        cid = card_id_for(ch)
        if not cid.startswith("ch"):
            continue
        date = str(ch.fm.get("date_in_story", ""))
        row = tl.get(cid)
        if row is None:
            rep.fail("timeline", ch.rel, f"{cid} has no row in bible/timeline.md")
            continue
        if date != row[1]:
            rep.fail("timeline", ch.rel,
                     f"date_in_story {date!r} != timeline {row[1]!r}")
        dated.append((cid, str(ch.fm.get("pov", "")), date))

    dated.sort(key=lambda t: int(t[0][2:]))
    for pov in ("Orla", "Adam"):
        thread = [(c, d) for c, p, d in dated if p == pov]
        for (c1, d1), (c2, d2) in zip(thread, thread[1:]):
            if d2 <= d1:
                rep.fail("timeline", where,
                         f"{pov} thread not strictly increasing: {c1} {d1} -> {c2} {d2}")
    globalseq = [(c, d) for c, _, d in dated if int(c[2:]) >= 3]
    for (c1, d1), (c2, d2) in zip(globalseq, globalseq[1:]):
        if d2 < d1:
            rep.fail("timeline", where,
                     f"book order not monotonic from ch03: {c1} {d1} -> {c2} {d2}")


def card_id_for(ch: Chapter) -> str:
    cid = str(ch.fm.get("chapter", ""))
    if cid.isdigit():
        return f"ch{int(cid):02d}"
    return cid


# --------------------------------------------------------------------------
# grid audit (--cards)
# --------------------------------------------------------------------------

CHAPTER_FIELDS = ["goal", "friction", "turn", "out-hook", "beats", "plants",
                  "payoffs", "cast", "location", "register"]
INTERLUDE_FIELDS = ["form", "plants", "payoffs", "register"]


def audit_cards(repo: Repo, rep: Report) -> None:
    where = "bible/chapter-grid.md"
    cards, part_titles = parse_cards(repo.read(repo.grid))
    rows = parse_ledger(repo.read(repo.ledger))
    tl = parse_timeline(repo.read(repo.timeline))
    sites = parse_sites(repo.read(repo.places))

    chapters = [c for c in cards if c.kind == "chapter"]
    interludes = [c for c in cards if c.kind == "interlude"]
    print(f"cards parsed: {len(chapters)} chapters + {len(interludes)} interludes "
          f"({len(part_titles)} part titles)")
    if len(chapters) != 36:
        rep.fail("cards", where, f"{len(chapters)} chapter cards, expected 36")
    if len(interludes) != 5:
        rep.fail("cards", where, f"{len(interludes)} interlude cards, expected 5")

    seen: set[str] = set()
    for c in cards:
        need = CHAPTER_FIELDS if c.kind == "chapter" else INTERLUDE_FIELDS
        for f in need:
            if not c.fields.get(f):
                rep.fail("cards", where, f"{c.cid}: empty field **{f}**")
        if not c.slug:
            rep.fail("cards", where, f"{c.cid}: no slug")
        if c.slug in seen:
            rep.fail("cards", where, f"{c.cid}: duplicate slug {c.slug}")
        seen.add(c.slug)
        if not c.target:
            rep.fail("cards", where, f"{c.cid}: no target words")
        if c.kind == "chapter":
            if c.pov not in ("Orla", "Adam"):
                rep.fail("cards", where, f"{c.cid}: POV {c.pov!r}")
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", c.date):
                rep.fail("cards", where, f"{c.cid}: date {c.date!r}")
            elif tl.get(c.cid, ("", ""))[1] != c.date:
                rep.fail("cards", where,
                         f"{c.cid}: card date {c.date} != timeline "
                         f"{tl.get(c.cid, ('', 'missing'))[1]}")
        bad = sorted({m.group(1).zfill(2) for m in SITE_RE.finditer(c.body)} - sites)
        if bad:
            rep.fail("cards", where,
                     f"{c.cid}: site label(s) not in hidden-places.md: "
                     + ", ".join(f"Site {b}" for b in bad))

    by_id = {c.cid: c for c in cards}
    for rid, row in rows.items():
        pc, yc = by_id.get(row.plant_ch), by_id.get(row.payoff_ch)
        if pc is None:
            rep.fail("cards", where, f"ledger {rid}: plant chapter {row.plant_ch} has no card")
        elif rid not in pc.plants:
            rep.fail("cards", where, f"ledger {rid}: card {row.plant_ch} does not list it as a plant")
        if yc is None:
            rep.fail("cards", where, f"ledger {rid}: payoff chapter {row.payoff_ch} has no card")
        elif rid not in yc.payoffs:
            rep.fail("cards", where, f"ledger {rid}: card {row.payoff_ch} does not list it as a payoff")
    for c in cards:
        for rid in c.plants + c.payoffs:
            if rid not in rows:
                rep.fail("cards", where, f"{c.cid}: {rid} has no ledger row")

    orla = sum(1 for c in chapters if c.pov == "Orla")
    adam = sum(1 for c in chapters if c.pov == "Adam")
    total = sum(c.target for c in chapters)
    inter = sum(c.target for c in interludes)
    print(f"POV split: Orla {orla} / Adam {adam} = "
          f"{orla / max(orla + adam, 1) * 100:.1f} / "
          f"{adam / max(orla + adam, 1) * 100:.1f}")
    print(f"word budget: chapters {total:,} + interludes {inter:,} = {total + inter:,}")
    for part in PARTS:
        p = [c for c in chapters if c.part == part]
        print(f"  part {part:<3} {len(p)} chapters, {sum(c.target for c in p):,} words")
    for c in chapters:
        lo, hi = THRESHOLDS["chapter_target"]
        if not (lo <= c.target <= hi):
            rep.warn("cards", where, f"{c.cid}: target {c.target} outside {lo}-{hi}")
    for c in interludes:
        lo, hi = THRESHOLDS["interlude"]
        if not (lo <= c.target <= hi):
            rep.warn("cards", where, f"{c.cid}: target {c.target} outside {lo}-{hi}")


# --------------------------------------------------------------------------
# main run
# --------------------------------------------------------------------------

def run_gate(repo: Repo, rep: Report, only: list[Path] | None = None) -> None:
    lists = parse_style_lists(repo.read(repo.guide))
    cards, _ = parse_cards(repo.read(repo.grid))
    rows = parse_ledger(repo.read(repo.ledger))
    tl = parse_timeline(repo.read(repo.timeline))
    vocab, italics_ok = parse_vocabulary(repo)
    sites = parse_sites(repo.read(repo.places))
    by_id = {c.cid: c for c in cards}

    print(f"style-guide lists: "
          + ", ".join(f"{k}({len(v)})" for k, v in lists.items()))
    print(f"bible: {len(cards)} cards, {len(rows)} ledger rows, "
          f"{len(tl)} dated chapters, {len(sites)} nameable sites, "
          f"{len(vocab)} known capitalised terms")

    all_chapters = load_chapters(repo)
    chapters = all_chapters
    if only:
        wanted = {p.resolve() for p in only}
        chapters = [c for c in all_chapters if c.path.resolve() in wanted]
    complete = len(all_chapters) == len(cards) and not only

    if not only:
        have = {card_id_for(c) for c in all_chapters}
        missing = [c.cid for c in cards if c.cid not in have]
        if missing:
            shown = ", ".join(missing[:8]) + (" ..." if len(missing) > 8 else "")
            rep.fail("scaffold", "manuscript/",
                     f"{len(missing)} card(s) have no file: {shown}")
        orphans = [c.rel for c in all_chapters
                   if card_id_for(c) not in {k.cid for k in cards}]
        if orphans:
            rep.fail("scaffold", "manuscript/",
                     f"file(s) with no card: {', '.join(orphans)}")

    for ch in chapters:
        check_front_matter(ch, rep)
        card = by_id.get(card_id_for(ch))
        check_card_mirror(ch, card, rep)
        sc = scope_text(ch.body)
        check_word_band(ch, card, sc, rep)
        check_lists(ch, sc, lists, rep)
        check_thresholds(ch, sc, italics_ok, rep)
        check_glossary(ch, sc, vocab, rep)
        check_sites(ch, sc, sites, rep)

    check_ledger(chapters, cards, rows, complete, rep)
    check_timeline(chapters, tl, rep)

    written = [c for c in chapters if str(c.fm.get("status")) != "stub"]
    if written:
        total = sum(scope_text(c.body).words for c in written)
        print(f"\nwritten: {len(written)}/{len(chapters)} files, {total:,} words")
    else:
        print(f"\nwritten: 0/{len(chapters)} files (scaffold only)")


# --------------------------------------------------------------------------
# assemble (feeds tools/build.ps1)
# --------------------------------------------------------------------------

def assemble(repo: Repo, out: Path) -> int:
    cards, part_titles = parse_cards(repo.read(repo.grid))
    by_id = {c.cid: c for c in cards}
    chapters = load_chapters(repo)
    if not chapters:
        print("assemble: no manuscript files found", file=sys.stderr)
        return 2

    def sort_key(ch: Chapter):
        cid = card_id_for(ch)
        if cid.startswith("ch"):
            return (int(cid[2:]), 0)
        return (99, 0) if not cid.startswith("I-") else (
            {"I-1": 7, "I-2": 15, "I-3": 22, "I-4": 29, "I-5": 36}.get(cid, 99), 1)

    lines = ["---", "title: Unplottable", "lang: en-GB", "---", ""]
    current_part = None
    for ch in sorted(chapters, key=sort_key):
        cid = card_id_for(ch)
        card = by_id.get(cid)
        part = str(ch.fm.get("part", ""))
        if part != current_part:
            current_part = part
            name = part_titles.get(part, "")
            lines += [f"# Part {part}" + (f" — {name}" if name else ""), ""]
        title = str(ch.fm.get("title", ""))
        if cid.startswith("ch"):
            lines += [f"## {int(cid[2:])}. {title}", ""]
        else:
            lines += [f"## Interlude {cid} — {title}", ""]
        body = re.sub(r"<!--.*?-->", "", ch.body, flags=re.S).strip()
        lines += [body, ""] if body else ["*[unwritten]*", ""]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"assembled {len(chapters)} files -> {out}")
    return 0


# --------------------------------------------------------------------------
# selftest: seed a bad fixture and prove every check fires
# --------------------------------------------------------------------------

BAD_CH01 = """---
chapter: 1
part: I
title: Uncertainty Flags
pov: Orla
date_in_story: 2033-03-22
target_words: 4300
plants: [P-T2-1, P-T4-1]
payoffs: []
status: draft
---

Little did she know the shelf would matter. She couldn't help but check the
magical core reading twice, then realized the color of the label had faded --
a favorite of hers. The brunette at the next desk organized the trolley.

"You've the whole row still to do," Rose exclaimed. "Nobody's counted Site 44
since the spring," she chuckled.

The older man from Records signed for the trolley without looking up.

Orla saw the dust and felt the cold and heard the lift, and she noticed that
she had gotten no closer to the answer. She walked slowly, carefully,
quietly, softly, wearily, bitterly, grimly, sourly, tiredly, sadly down the
row, like a woman in a corridor, like a clerk in a dream, as if the shelves
were water, as though the Thaumic Resonance Board had *never* *once* *made*
*a* *decision* *in* *its* *life*.

The Thaumic Resonance Board met on Tuesdays. The Thaumic Resonance Board
never minuted anything.
"""

BAD_CH03 = """---
chapter: 3
title: The Wrong Title
part: I
pov: Orla
date_in_story: 2033-03-26
target_words: 3900
plants: [P-T9-9]
payoffs: [P-T1-1]
status: draft
---

Short body, well under any band, which is the point of this fixture.
The muggle waited, because a muggle always waits.
"""


def selftest(repo: Repo) -> int:
    fixture = repo.root / "Local" / "scratch" / "gate-selftest"
    if fixture.exists():
        shutil.rmtree(fixture)
    (fixture / "bible").mkdir(parents=True)
    (fixture / "manuscript" / "part-1").mkdir(parents=True)
    for name in ("style-guide.md", "chapter-grid.md", "foreshadowing-ledger.md",
                 "timeline.md", "glossary.md", "hidden-places.md",
                 "characters.md"):
        src = repo.bible / name
        if src.exists():
            shutil.copy2(src, fixture / "bible" / name)
    (fixture / "manuscript" / "part-1" / "ch01-uncertainty-flags.md").write_text(
        BAD_CH01, encoding="utf-8")
    (fixture / "manuscript" / "part-1" / "ch03-muggle-worthy.md").write_text(
        BAD_CH03, encoding="utf-8")

    print("=" * 78)
    print("SELFTEST - seeded bad fixture at Local/scratch/gate-selftest")
    print("=" * 78)
    rep = Report()
    run_gate(Repo(fixture), rep)
    rep.render()

    expected = {
        "front-matter": "key order broken in ch03",
        "card-mirror": "ch03 title/date do not match the grid card",
        "word-band": "ch03 far under the 3,200 floor",
        "banned-phrases": "'little did * know', 'couldn't help but', 'the brunette'",
        "fanon-terms": "'magical core'",
        "americanisms": "'gotten', 'realized', 'color', 'favorite'",
        "am-spelling": "'organized' (-ize)",
        "muggle-cap": "lowercase 'muggle' in ch03 body",
        "adverbs": "manner-adverb pile-up in narration",
        "similes": "like a / as if / as though cluster",
        "italics": "emphasis italics over budget",
        "said-bookisms": "'exclaimed', 'chuckled' in tag position",
        "filter-words": "saw / felt / heard / noticed",
        "epithets": "'the brunette' in narration",
        "glossary": "Thaumic Resonance Board (x3) not in glossary.md",
        "sites": "Site 44 has no row in hidden-places.md",
        "ledger": "P-T9-9 has no row; P-T1-1 pays in ch15",
        "timeline": "ch03 dated 2033-03-26, timeline says 2033-03-25",
        "scaffold": "cards with no file",
    }
    fired = rep.checks_fired()
    print("\n" + "=" * 78)
    print("CHECK COVERAGE")
    print("=" * 78)
    missing = []
    for check, why in expected.items():
        ok = check in fired
        print(f"  [{'FIRED' if ok else ' -- '}] {check:<15} {why}")
        if not ok:
            missing.append(check)
    extra = sorted(fired - set(expected))
    if extra:
        print(f"  (also fired: {', '.join(extra)})")
    print()
    if missing:
        print(f"SELFTEST RED - checks that did not fire: {', '.join(missing)}")
        return 1
    print(f"SELFTEST GREEN - all {len(expected)} checks fired on seeded bad input")
    print("(fixture kept at Local/scratch/gate-selftest for inspection)")
    return 0


# --------------------------------------------------------------------------
# cli
# --------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Unplottable quality gate")
    ap.add_argument("paths", nargs="*", type=Path,
                    help="check only these manuscript files")
    ap.add_argument("--cards", action="store_true",
                    help="audit bible/chapter-grid.md instead of the manuscript")
    ap.add_argument("--selftest", action="store_true",
                    help="run every check against a seeded bad fixture")
    ap.add_argument("--assemble", type=Path, metavar="OUT",
                    help="write one book-shaped markdown file (used by build.ps1)")
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = ap.parse_args(argv)

    repo = Repo(args.root.resolve())
    for required in (repo.guide, repo.grid, repo.ledger, repo.timeline,
                     repo.glossary, repo.places):
        if not required.exists():
            print(f"gate: missing bible file {required}", file=sys.stderr)
            return 2

    if args.assemble:
        return assemble(repo, args.assemble)
    if args.selftest:
        return selftest(repo)

    rep = Report()
    print("=" * 78)
    if args.cards:
        print("GATE --cards - bible/chapter-grid.md")
        print("=" * 78)
        audit_cards(repo, rep)
    else:
        print(f"GATE - {repo.root}")
        print("=" * 78)
        run_gate(repo, rep, only=list(args.paths) or None)

    rep.render()
    fails, warns = rep.fails, rep.warns
    print("\n" + "=" * 78)
    if fails:
        by_check: dict[str, int] = {}
        for f in fails:
            by_check[f.check] = by_check.get(f.check, 0) + 1
        print(f"RESULT: RED - {len(fails)} hard violation(s), {len(warns)} warning(s)")
        print("  " + " | ".join(f"{k}:{v}" for k, v in sorted(by_check.items())))
        return 1
    print(f"RESULT: GREEN - 0 hard violations, {len(warns)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
