export const meta = {
  name: 'unplottable-ru-styletest',
  description: 'RU style experiment: retranslate ch04 + ch05 flow-first (readable), verify story intact + flow',
  phases: [{ title: 'Translate (flow-first)' }, { title: 'Verify' }],
}

const UNITS = [
  { id: 'ch04', in: 'manuscript/part-1/ch04-assessment-ongoing.md', out: 'Translation/RU/manuscript/part-1/ch04-assessment-ongoing.md' },
  { id: 'ch05', in: 'manuscript/part-1/ch05-cover-stories.md', out: 'Translation/RU/manuscript/part-1/ch05-cover-stories.md' }
]

const VERDICT = {
  type: 'object',
  properties: {
    id: { type: 'string' },
    story_intact: { type: 'boolean', description: 'true if every plot beat, clue and twist is preserved' },
    flows_now: { type: 'boolean', description: 'true if the Russian now reads flowing and clear, not clipped/choppy' },
    depersonified: { type: 'boolean', description: 'true if personified rooms/halls were rendered through people or naturally' },
    notes: { type: 'string' },
    backtranslation_first_3_paras: { type: 'string', description: 'faithful English back-translation of the first three paragraphs' }
  },
  required: ['id', 'story_intact', 'flows_now', 'depersonified', 'notes', 'backtranslation_first_3_paras']
}

const results = await pipeline(UNITS,
  (u) => agent(
    'Translate ONE chapter of the novel *Unplottable* into Russian, in a FLOW-FIRST style. Read, in this order: Translation/RU/style-flow-brief.md (the governing style brief — obey it), Translation/RU/glossary.md (Rosman termbase), Translation/RU/style-ru.md (voice), then the English source ' + u.in + '. Write the Russian translation to ' + u.out + '.\n\nTHE POINT OF THIS PASS: the previous Russian read beautiful but too clipped and hard to follow ("cut, cut, cut"), and it personified rooms/halls in a way that confused a native reader. Make THIS translation FLOW — smooth the choppiness, restore connective tissue so a reader never has to re-read to understand, un-personify places (say the people in the room, not the room), unpack cryptic aphorisms into clear meaning. Content leads; the reader is carried by the story.\n\nHARD RULES: change nothing about the story, the plot beats, the planted clues (fair-play) or the twists — only the STYLE flows better; keep the YAML front-matter intact (translate only the title value); every glossary term exactly (Rosman); idiomatic literary Russian, no calques. Return a one-line status.',
    { agentType: 'general-purpose', model: 'fable', effort: 'high', phase: 'Translate (flow-first)', label: 'tr:' + u.id }
  ),
  (prev, u) => agent(
    'Verify the flow-first Russian translation at ' + u.out + ' against the English source ' + u.in + ', Translation/RU/glossary.md and Translation/RU/style-flow-brief.md. Confirm: (a) STORY INTACT — every plot beat, planted clue and twist preserved, nothing of substance added or dropped; (b) IT NOW FLOWS — reads clear and connected on first read, not clipped/choppy; (c) DE-PERSONIFIED — rooms/halls rendered through people or naturally; (d) Rosman terms correct, front-matter intact. Fix small issues in place. Then return the verdict for chapter ' + u.id + ' (set id to "' + u.id + '"), including a faithful English back-translation of the first THREE paragraphs so a non-Russian reader can judge both meaning and flow.',
    { agentType: 'general-purpose', model: 'fable', effort: 'high', phase: 'Verify', label: 'vf:' + u.id, schema: VERDICT }
  )
)

return { verdicts: results }
