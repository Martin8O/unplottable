export const meta = {
  name: 'unplottable-ru-translate',
  description: 'RU flow-first translation of chosen chapters: translate + adversarial verify (Fable high)',
  phases: [{ title: 'Translate (flow-first)' }, { title: 'Verify' }],
}

// ============================================================================
//  SET THIS LINE to the chapters you want, then run this file.
//  Examples:  ["ch06","ch07","ch08","ch09","ch10"]   ·   ["i2"]   ·   "all"
// ============================================================================
const REQUESTED = []
// ============================================================================

const UNITS_ALL = [
{
"id": "ch01",
"part": "part-1",
"in": "manuscript/part-1/ch01-uncertainty-flags.md",
"out": "Translation/RU/manuscript/part-1/ch01-uncertainty-flags.md"
},
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
"out": "Translation/RU/manuscript/part-1/i1-after-ch07-preprint-memorandum.md"
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

const want = (REQUESTED === 'all') ? null : new Set(REQUESTED)
const UNITS = want ? UNITS_ALL.filter(u => want.has(u.id)) : UNITS_ALL
if (!UNITS.length) {
  return { error: 'REQUESTED matched no chapters', requested: REQUESTED, known: UNITS_ALL.map(u => u.id) }
}
log('flow-first translating: ' + UNITS.map(u => u.id).join(', '))

const VERDICT = {
  type: 'object',
  properties: {
    id: { type: 'string' },
    story_intact: { type: 'boolean' },
    flows_now: { type: 'boolean' },
    depersonified: { type: 'boolean' },
    notes: { type: 'string' },
    backtranslation_first_3_paras: { type: 'string' }
  },
  required: ['id', 'story_intact', 'flows_now', 'depersonified', 'notes', 'backtranslation_first_3_paras']
}

const results = await pipeline(UNITS,
  (u) => agent('Translate ONE chapter of the novel *Unplottable* into Russian, in a FLOW-FIRST style. Read, in this order: Translation/RU/style-flow-brief.md (the governing style brief - obey it), Translation/RU/glossary.md (Rosman termbase), Translation/RU/style-ru.md (voice), then the English source ' + u.in + '. Write the Russian translation to ' + u.out + '.\n\nTHE POINT: earlier Russian read beautiful but too clipped and hard to follow ("cut, cut, cut") and personified rooms/halls in a way that confused a native reader. Make THIS translation FLOW - smooth the choppiness, restore connective tissue so a reader never has to re-read to understand, un-personify places (say the people in the room, not the room), unpack cryptic aphorisms into clear meaning. Content leads; the reader is carried by the story.\n\nHARD RULES: change nothing about the story, the plot beats, the planted clues (fair-play) or the twists - only the STYLE flows better; keep the YAML front-matter intact (translate only the title value); every glossary term exactly (Rosman); idiomatic literary Russian, no calques. Return a one-line status.',
    { agentType: 'general-purpose', model: 'fable', effort: 'high', phase: 'Translate (flow-first)', label: 'tr:' + u.id }
  ),
  (prev, u) => agent('Verify the flow-first Russian translation at ' + u.out + ' against the English source ' + u.in + ', Translation/RU/glossary.md and Translation/RU/style-flow-brief.md. Confirm: (a) STORY INTACT - every plot beat, planted clue and twist preserved, nothing of substance added or dropped; (b) IT NOW FLOWS - clear and connected on first read, not clipped/choppy; (c) DE-PERSONIFIED - rooms/halls rendered through people or naturally; (d) Rosman terms correct, front-matter intact. Fix small issues in place. Then return the verdict for chapter ' + u.id + ' (set id to "' + u.id + '"), including a faithful English back-translation of the first THREE paragraphs so a non-Russian reader can judge meaning and flow.',
    { agentType: 'general-purpose', model: 'fable', effort: 'high', phase: 'Verify', label: 'vf:' + u.id, schema: VERDICT }
  )
)

return { translated: UNITS.map(u => u.id), verdicts: results }
