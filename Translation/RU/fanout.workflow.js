export const meta = {
  name: 'unplottable-ru-fanout',
  description: 'RU (Rosman) full translation: translate + adversarially verify the remaining 40 units at Fable 5 high',
  phases: [{ title: 'Translate' }, { title: 'Verify' }],
}

const UNITS = [
{
"id": "ch02",
"part": "part-1",
"in": "manuscript/part-1/ch02-structured-residuals.md",
"out": "Translation/RU/manuscript/part-1/ch02-structured-residuals.md"
},
{
"id": "ch03",
"part": "part-1",
"in": "manuscript/part-1/ch03-muggle-worthy.md",
"out": "Translation/RU/manuscript/part-1/ch03-muggle-worthy.md"
},
{
"id": "ch04",
"part": "part-1",
"in": "manuscript/part-1/ch04-assessment-ongoing.md",
"out": "Translation/RU/manuscript/part-1/ch04-assessment-ongoing.md"
},
{
"id": "ch05",
"part": "part-1",
"in": "manuscript/part-1/ch05-cover-stories.md",
"out": "Translation/RU/manuscript/part-1/ch05-cover-stories.md"
},
{
"id": "ch06",
"part": "part-1",
"in": "manuscript/part-1/ch06-the-motion.md",
"out": "Translation/RU/manuscript/part-1/ch06-the-motion.md"
},
{
"id": "ch07",
"part": "part-1",
"in": "manuscript/part-1/ch07-terms-and-conditions.md",
"out": "Translation/RU/manuscript/part-1/ch07-terms-and-conditions.md"
},
{
"id": "i1",
"part": "part-1",
"in": "manuscript/part-1/i1-preprint-memorandum.md",
"out": "Translation/RU/manuscript/part-1/i1-preprint-memorandum.md"
},
{
"id": "ch08",
"part": "part-2",
"in": "manuscript/part-2/ch08-perimeter.md",
"out": "Translation/RU/manuscript/part-2/ch08-perimeter.md"
},
{
"id": "ch09",
"part": "part-2",
"in": "manuscript/part-2/ch09-the-restored-hour.md",
"out": "Translation/RU/manuscript/part-2/ch09-the-restored-hour.md"
},
{
"id": "ch10",
"part": "part-2",
"in": "manuscript/part-2/ch10-world-models.md",
"out": "Translation/RU/manuscript/part-2/ch10-world-models.md"
},
{
"id": "ch11",
"part": "part-2",
"in": "manuscript/part-2/ch11-summons.md",
"out": "Translation/RU/manuscript/part-2/ch11-summons.md"
},
{
"id": "ch12",
"part": "part-2",
"in": "manuscript/part-2/ch12-home-bias.md",
"out": "Translation/RU/manuscript/part-2/ch12-home-bias.md"
},
{
"id": "ch13",
"part": "part-2",
"in": "manuscript/part-2/ch13-keeping-score.md",
"out": "Translation/RU/manuscript/part-2/ch13-keeping-score.md"
},
{
"id": "ch14",
"part": "part-2",
"in": "manuscript/part-2/ch14-canary.md",
"out": "Translation/RU/manuscript/part-2/ch14-canary.md"
},
{
"id": "ch15",
"part": "part-2",
"in": "manuscript/part-2/ch15-the-map-looks-back.md",
"out": "Translation/RU/manuscript/part-2/ch15-the-map-looks-back.md"
},
{
"id": "i2",
"part": "part-2",
"in": "manuscript/part-2/i2-eval-log.md",
"out": "Translation/RU/manuscript/part-2/i2-eval-log.md"
},
{
"id": "ch16",
"part": "part-3",
"in": "manuscript/part-3/ch16-specimen.md",
"out": "Translation/RU/manuscript/part-3/ch16-specimen.md"
},
{
"id": "ch17",
"part": "part-3",
"in": "manuscript/part-3/ch17-pl-to-ll.md",
"out": "Translation/RU/manuscript/part-3/ch17-pl-to-ll.md"
},
{
"id": "ch18",
"part": "part-3",
"in": "manuscript/part-3/ch18-the-option-list.md",
"out": "Translation/RU/manuscript/part-3/ch18-the-option-list.md"
},
{
"id": "ch19",
"part": "part-3",
"in": "manuscript/part-3/ch19-buried-mathematics.md",
"out": "Translation/RU/manuscript/part-3/ch19-buried-mathematics.md"
},
{
"id": "ch20",
"part": "part-3",
"in": "manuscript/part-3/ch20-the-manor.md",
"out": "Translation/RU/manuscript/part-3/ch20-the-manor.md"
},
{
"id": "ch21",
"part": "part-3",
"in": "manuscript/part-3/ch21-attribution.md",
"out": "Translation/RU/manuscript/part-3/ch21-attribution.md"
},
{
"id": "ch22",
"part": "part-3",
"in": "manuscript/part-3/ch22-the-ask.md",
"out": "Translation/RU/manuscript/part-3/ch22-the-ask.md"
},
{
"id": "i3",
"part": "part-3",
"in": "manuscript/part-3/i3-inquest.md",
"out": "Translation/RU/manuscript/part-3/i3-inquest.md"
},
{
"id": "ch23",
"part": "part-4",
"in": "manuscript/part-4/ch23-compartments.md",
"out": "Translation/RU/manuscript/part-4/ch23-compartments.md"
},
{
"id": "ch24",
"part": "part-4",
"in": "manuscript/part-4/ch24-the-naturalist.md",
"out": "Translation/RU/manuscript/part-4/ch24-the-naturalist.md"
},
{
"id": "ch25",
"part": "part-4",
"in": "manuscript/part-4/ch25-the-apprentice.md",
"out": "Translation/RU/manuscript/part-4/ch25-the-apprentice.md"
},
{
"id": "ch26",
"part": "part-4",
"in": "manuscript/part-4/ch26-severance.md",
"out": "Translation/RU/manuscript/part-4/ch26-severance.md"
},
{
"id": "ch27",
"part": "part-4",
"in": "manuscript/part-4/ch27-what-we-keep.md",
"out": "Translation/RU/manuscript/part-4/ch27-what-we-keep.md"
},
{
"id": "ch28",
"part": "part-4",
"in": "manuscript/part-4/ch28-erase-me.md",
"out": "Translation/RU/manuscript/part-4/ch28-erase-me.md"
},
{
"id": "ch29",
"part": "part-4",
"in": "manuscript/part-4/ch29-full-disclosure.md",
"out": "Translation/RU/manuscript/part-4/ch29-full-disclosure.md"
},
{
"id": "i4",
"part": "part-4",
"in": "manuscript/part-4/i4-front-page-tract.md",
"out": "Translation/RU/manuscript/part-4/i4-front-page-tract.md"
},
{
"id": "ch30",
"part": "part-5",
"in": "manuscript/part-5/ch30-section-thirteen.md",
"out": "Translation/RU/manuscript/part-5/ch30-section-thirteen.md"
},
{
"id": "ch31",
"part": "part-5",
"in": "manuscript/part-5/ch31-the-cabinet-room.md",
"out": "Translation/RU/manuscript/part-5/ch31-the-cabinet-room.md"
},
{
"id": "ch32",
"part": "part-5",
"in": "manuscript/part-5/ch32-tranche.md",
"out": "Translation/RU/manuscript/part-5/ch32-tranche.md"
},
{
"id": "ch33",
"part": "part-5",
"in": "manuscript/part-5/ch33-two-receivers.md",
"out": "Translation/RU/manuscript/part-5/ch33-two-receivers.md"
},
{
"id": "ch34",
"part": "part-5",
"in": "manuscript/part-5/ch34-where-the-gates-open.md",
"out": "Translation/RU/manuscript/part-5/ch34-where-the-gates-open.md"
},
{
"id": "ch35",
"part": "part-5",
"in": "manuscript/part-5/ch35-a-committee-name.md",
"out": "Translation/RU/manuscript/part-5/ch35-a-committee-name.md"
},
{
"id": "ch36",
"part": "part-5",
"in": "manuscript/part-5/ch36-unplottable.md",
"out": "Translation/RU/manuscript/part-5/ch36-unplottable.md"
},
{
"id": "i5",
"part": "part-5",
"in": "manuscript/part-5/i5-quinn-kessler-et-al.md",
"out": "Translation/RU/manuscript/part-5/i5-quinn-kessler-et-al.md"
}
]

const VERDICT = {
  type: 'object',
  properties: {
    id: { type: 'string' },
    ok: { type: 'boolean' },
    issues: { type: 'string' },
    fixed: { type: 'boolean' }
  },
  required: ['id', 'ok', 'issues', 'fixed']
}

const results = await pipeline(UNITS,
  (u) => agent(
    'Translate ONE chapter of the novel *Unplottable* into Russian. Work efficiently: read the English source ' + u.in + ', then Translation/RU/glossary.md and Translation/RU/style-ru.md ONCE, then translate in one careful pass. Write the Russian translation to ' + u.out + '.\nRULES: keep the YAML front-matter block (between the --- lines) intact with English keys, translating ONLY the title value; translate ONLY the prose body; preserve every paragraph, scene break and any in-world document formatting; render every glossary term exactly (Rosman, never Spivak); preserve the POV register and any fragment voice; add nothing, drop nothing; do not overthink - one careful pass. Return a one-line status.',
    { agentType: 'general-purpose', model: 'claude-fable-5', effort: 'high', phase: 'Translate', label: 'tr:' + u.id }
  ),
  (prev, u) => agent(
    'Adversarially verify the Russian translation at ' + u.out + ' against the English source ' + u.in + ' and Translation/RU/glossary.md. Check: terms match the glossary (Rosman, not Spivak); no English left in the body; register and voice preserved; nothing added or dropped; the YAML front-matter is intact. If you find any issue, FIX it in place by rewriting ' + u.out + '. Return the verdict for chapter ' + u.id + ' (set the id field to "' + u.id + '").',
    { agentType: 'general-purpose', model: 'claude-fable-5', effort: 'high', phase: 'Verify', label: 'vf:' + u.id, schema: VERDICT }
  )
)

const done = results.filter(Boolean)
const flagged = done.filter(v => v && v.ok === false)
return { translated: done.length, flagged: flagged.map(v => ({ id: v.id, issues: v.issues })), verdicts: done }
