---
chapter: 2
part: I
title: Structured Residuals
pov: Adam
date_in_story: 2033-03-21
target_words: 3350
plants: []
payoffs: []
status: draft
---

At 03:47 the pipeline had found it again, considered it for eleven milliseconds, and filed it under sensor noise.

Adam read the ticket standing, coat still on, in the hour when the lab belonged to the heating pipes and the cleaners' radio two floors down. The nightly triage summary sat at the top of the queue where it sat every morning, worded the way it was worded every morning, with the serenity of automation that has never yet been contradicted by its owners and sees no reason to begin:

> ANOMALY-TRIAGE · nightly run · 2033-03-15 03:47:12
> geo-clustered excess residual, GB grid: 41 clusters above floor
> class: DATA-QUALITY (sensor vintage / ingest fault) · confidence 0.94
> recommended action: exclude from aggregates
> status: MANUAL HOLD (A. Kessler, 2031-11-08) · hold active 493 days

Eleven milliseconds was, to be fair, more consideration than most of the field had given it.

The audit's one idea fitted in a sentence, which was most of why two funding panels had declined to pay for it. Take the open-weight Orrery models — which carried, between them, a learned expectation of how Britain behaved, hour by hour: weather, traffic, footfall, radio, the slow breathing of the grid — and ask, cell by cell on a kilometre grid, where their error exceeded the uncertainty they claimed for themselves. Calibration work. Housekeeping, at national scale. Reliability was the word on the grant, chosen because it frightened nobody.

A structured residual was the profession's phrase for a particular species of bad news: error that ought to be noise, and is not. Noise forgives you — it averages away. Structure does not average. Structure means the world contains something your model has not been told about; the error has a shape, and the shape is the something.

For the better part of two years the audit had returned exactly what it promised: a reliability atlas of the national sensing fabric, cell by dutiful cell — miscalibration over tidal flats, a bias the width of a motorway where the traffic feeds double-counted, the ordinary honest disorder of a country being measured. And, standing up out of that disorder like nail-heads out of sanded wood, a scatter of clusters that were not disorder at all.

Overnight the last two jobs of the kill battery had come home. A full re-score on the winter's fresh data — new quarter, new satellite vintages, the rebuilt ingest — and the final covariate register Priya had managed to buy, beg or license: utilities corridors, this round, and the last of the licensed-jammer lists. Sixteen months ago, either might have ended it. He opened the map.

The map came back the same. It always came back the same now. There had been a time when that sentence would have been the happiest of his career.

The hold was his. He had placed it in the audit's second month, when the per-cell maps were new and the triage layer — standard tooling, the same defaults every serious lab ran — had taken one look at excess sitting clustered in space and done what triage exists to do with geography: classed it as a data fault and dropped it from the aggregates. The dashboards had gone a restful green. It had taken him the better part of a week to say what was wrong with that, and he had been saying it to committees ever since: sensor vintage was not an explanation, it was a place to put things. An explanation can be asked to predict. Which sensors; which vendors; which years. Sensor vintage predicted everything and therefore nothing — it was the kind of answer whose whole content is a request to stop asking. He had found the sameness of everyone's defaults comforting for about a year, and then had stopped, and the stopping was the nearest thing to a discovery he had ever made without a machine.

Since then he had run the audit as one long attempt to be wrong, conducted with a thoroughness Priya had started calling devotional. Terrain, weather, population, land use; the defence estate and everything else the state fences and therefore files; mine workings; jamming, licensed and logged; the data's own politics, vendor by vendor. Each control went out with his blessing and came back with nothing. The excess stayed. The edges stayed. The map, after every attempt on its life, was the same map.

The Meridian award ran to the autumn. The renewal case was the audit; the audit, now, was this. He booked Thursday afternoon for the full review and gave it no end time, and he left the hold where it had sat for sixteen months — HOLD, said the queue, a manifesto one word long.

* * *

Thursday brought the rain in off the Forth, and Priya in with it, laptop under one arm like a writ.

"Before we start," she said, from the doorway, "I want it minuted that if the atlas is an artefact, I have spent half a studentship building the most careful map of nothing in the history of cartography."

"Minuted where?"

"Wherever they file the doctorates that end in a shrug." She set the laptop down between them and turned it to face him: the document she had kept since the audit's first winter — WAYS WE ARE WRONG, the best-maintained artefact in the group, thirty-one numbered ways the result could be an embarrassment, each with an owner, a test and a verdict. "Shall we?"

They went down the list the way you check a rope.

Edges first. Everything mundane was smooth; that was nearly the definition of mundane. Weather was smooth, coverage was smooth, even the military was smooth at a kilometre — a firing range fades at its fence, leaks staff and signage and lorries into the cells around it, announces itself in gradients. "Confounds have slopes," Priya said, pulling up the zoom panels that would be Figure 2. "These have cliffs." At every resolution they could buy, the boundaries stayed inside a single cell: not smears but shapes, holding their outlines year over year like something maintained. "They look surveyed," he said, because it was the most neutral word left.

"They look owned," Priya said, which was not neutral at all, and was why it would not be going in the paper.

Second, the absence. It was not wrong data — wrong data was routine. It was missing data, behaving impossibly. Delivery tracks entered the cells and resumed beyond them, the gap's two ends agreeing to the metre, and the agreement held across twenty years of hardware generations that shared nothing but the gap. Footfall did not stop at the boundaries the way footfall stops at a fence; it bent around them, smooth as water taking a stone it declined to mention. The atlas was not a map of things at all. It was a map of holes — and the holes had texture. "Here is what I mind," Priya said, scrolling to the temporal panels. "A hole in footfall can only exist while there's footfall for it to be missing from. So our holes keep office hours. They have weekends, Adam. The absence has habits. Dead zones should be dead. These read as lived-in."

"'Inhabited-looking' is the draft's word."

"I know what the draft's word is. I've spent a month trying to get it out of the abstract."

"I've tried every quieter phrase," he said. "They all claim more, or claim less. It reports an appearance and asserts nothing. That is the whole of what an honest word does."

"It's the word that gets us quoted."

"It's the word that's true. If those turn out to be enemies, we're in the wrong trade."

Third — slowest of the cheap deaths — memorisation: the families learning the holes from one another's training soup, a rumour of absence handed down the corpora. Except Orrery-1 could not see the sites at all. Orrery-2 saw smudges. Orrery-3 drew edges. And the two other model families they had weights for — trained an ocean away, on vintages that barely overlapped — agreed about the where while disagreeing about nearly everything else they were asked. The excess did not even hold still relative to the models: measured in units of each model's own stated uncertainty, it grew, generation on generation, monotonic with capability. He had put the mechanism into the draft in one sentence, deleted it twice for sounding like a slogan, and restored it twice for being the finding: the better the model, the sharper the impossible. A model tightens its uncertainty wherever the world lets itself be learnt; where the world declines, everything the model gains elsewhere arrives there as sharpened failure. There was no cure for this signal in scale. Scale was what the signal ate.

"Thirty-eight sites," Priya said, "or forty-three, depending where you set the floor." The draft said three dozen, gave the dependence, and declined to be more impressive than its own threshold allowed. The sites were numbered in order of anomaly mass, Site 01 downwards, because a number was a fair thing to give an observation, and a name was a thing you gave an explanation.

Fourth, the registers. She had run them until the registers ran out: defence estate, safeguarded aerodromes, licensed jammers, mine workings, pipeline corridors, protected designations of every flavour science or heritage could confer. Restriction, in a filing state, is paperwork before it is fences; what Britain forbids, Britain writes down. Nothing in any register predicted the sites. The paper's sentence on it had been through eleven drafts of its own and now claimed exactly what they could defend: every class of restricted site we could enumerate leaves a register signature; these leave none. "Keep 'we could enumerate,'" Priya said. "The day we claim to have enumerated the state itself, we'll deserve whatever happens to us."

Fifth, the one the whole argument stood on. One stream failing was an artefact — a vendor, a pipeline, a bad vintage; you retired it and apologised to nobody. The same hole in streams that shared no vendor, no pipeline and no physics was not an artefact of anything; it was a property of the place. Aviation-grade GNSS integrity. Synthetic-aperture radar coherence. Imagery-derived features. The licensed exhaust. Independent instruments, strangers to one another, agreeing cell for cell. Her favourite objection had died hardest, and she reported its death with an executioner's modest pride: the suppression polygons — the privacy scrub-lists the ad-tech brokers shared, the one genuinely common layer in the commercial streams, and polygons, moreover, that were sharp, surveyed and register-absent, exactly the signature. "So I got the lists. Eleven brokers. No overlap — not one site, not one vertex. And the spine of the argument never touches their ecosystem anyway: aviation, radar, imagery. If every broker in Europe is lying to us in concert, the map survives them."

"Then Table 1 stays ugly," he said.

"Table 1 stays ugly," she agreed, in the tone of a treaty being signed. Site 01 carried radar coherence, GNSS and imagery and no footfall evidence at all, because there was no footfall in that stretch of the Highlands for a hole to be missing from; you cannot detect absence in an empty stream, and the caption would say so in plain words. Half the sites were rich in three currencies and bankrupt in a fourth. "A reviewer looks at a heterogeneous evidence table and reads: honest. Or reads: patchwork."

"Honest and patchwork," Adam said. "That is what evidence looks like when you haven't decided the answer in advance."

By the end the rain had stopped, without either of them catching the moment it went. Thirty-one rows; thirty-one verdicts; the column of survivors, empty. Priya sat back.

"That's the list," she said. "We are out of ways to be wrong."

"We're out of cheap ones."

She closed the laptop and looked at him over it, and the question she had been keeping arrived without any dressing on it: "So we're doing this."

It was not, the way she said it, entirely a question. The room had the feel of a drop freshly measured and found longer than the guess: nothing dramatic; arithmetic, rearranging itself.

"Write-up by the weekend," he said, which was not an answer either, and they both let it stand.

* * *

On Saturday he took the question up Salisbury Crags, because the lab made every thought sound like the lab.

March was running all its weathers in rotation, and the path had the usual traffic of dogs and runners and one man in profoundly wrong shoes. Adam climbed badly and with commitment, which was how he climbed everything. From the top the city explained itself: buses keeping their intervals along the roads below, gulls running their commute between the rooftops and the tip, desire lines worn pale across the park grass where ten thousand walkers had overruled the council's opinion of where the path should be — footfall, written in mud. Everything down there wrote itself down all day long, in mud and metadata, and had done for decades, and the whole of his profession was reading what it wrote and saying how far it could be trusted.

North, past the bridges, the haze was only haze. A hundred and fifty kilometres that way, give or take, lay the largest object on the atlas, and by the archive's testimony it had lain there longer than there had been an archive to hold it.

He walked the decision the way Priya walked her list, item by item, because he did not know another way that could be trusted.

He had sat five days of 2030 on a red-team at the National Institute for Model Evaluation — windowless rooms, biscuits of unusual quality, grown adults deciding what the public account of an evaluation could safely say. He knew the grammar of withholding, and he thought well of it. You withheld a capability, because publishing one armed strangers. You withheld a vulnerability until the fix existed, because publishing early fired a starting gun. He had signed both kinds of silence in his time and regretted neither. This was neither. The atlas armed nobody with anything; it conferred no ability that the public archives and the open weights did not already confer on anyone with patience. It reported that the world contained a structure nobody had explained. There was no vendor to warn. There was no patch to wait for. The only party competent to receive the disclosure was everyone.

The staged option, then — publish the method, withhold the map — and he gave it the respect of walking it all the way to its end. The coordinates were not his to withhold: they were latent in public data and public weights, which was the paper's entire claim, so redaction withheld nothing except the means of checking his work. And a method without its map would not sit unapplied for a fortnight. It would be applied by people in a hurry, with worse controls and better headlines, and the first public version of the thing would be the careless one. If it was going to be found — and it was; property three was a promise, every model generation marking the price of seeing it further down — then better it arrive once, carefully, with its error bars attached, from somebody with everything to lose. Besides which, the result already existed in a deliverable pipeline with his name on it. Meridian ran on reports, and reports were not a vault.

What kept him on the hill past the point of cold was none of that. If the sites belonged to somebody — some class of installation no register admitted — then the atlas was a targeting product, whatever its intentions. The registers said no, and said it five different ways; a class of national infrastructure absent from every filing system Britain possessed was an absurdity. But an absurdity was not an impossibility, and he turned the worry over until it showed him its true shape: whatever the sites were, they were already visible to any state or company that cared to spend the compute. His silence protected nobody. It only chose who got to be first, and he could not choose that it be no one.

What remained, under all of it, was older and less publishable: a dislike, inherited the way you inherit a doorplate, of well-made lists of places where people might be hiding. The Kesslers had left Leipzig in thirty-eight with two suitcases and a habit of keeping the passports current, and four generations on the habit survived in him as an instinct he had never needed and had never once audited. He stood with it a while in the wind. Turned, it cut the other way as well: the list already existed, latent in every archive on the planet, waiting only for admission prices to fall. Publishing would not make the list. It would decide whether the list arrived stated to the metre with its uncertainties, or later, and louder, from someone who stated none.

That evening he typed a message he had been composing since Thursday:

> If you want your name off, it comes off this weekend. No cost, no questions, and the work stays cited to you. The bet is mine to make. It is not yours.

Priya took eleven minutes.

> Second author means I checked it. I checked it. The name stays.
> Also you've spelled "artefact" the American way in §5.2. Fixed.

On Sunday night he wrote to Dr Baird, because Meridian ran on a no-surprises rule and Baird had bought this audit when two panels had passed on it. The subject line went through four drafts of its own — HEADS-UP (flippant), AUDIT RESULT (coy), ADVANCE COPY: RELIABILITY ATLAS DELIVERABLE (accurate, and a lie by temperature) — and landed, at last, on the truth: YOU FUNDED SOMETHING STRANGE. PAPER ATTACHED. SUBMITTING MONDAY. He set it to send at nine.

Then he made the last pot of tea of the weekend, properly, the way his grandfather had kept the passports: correctly, and against no stated emergency. The draft was as done as care could make it.

Monday, then.

* * *

Monday came in on a bin lorry's reversing alarm and a sky the colour of unwashed glass. By 08:40 Priya was already at her desk, wearing the jumper she kept for vivas. Neither of them mentioned it.

The abstract was nine sentences. It had been fourteen; the five he had cut were all true, and all louder than true needed to be. He read it a last time the way you read your own passport at a border, and let the three words near the end stand. They had survived Priya, which was a higher bar than review. The claims came qualified to the exact degree the evidence bought and no further; the conclusion offered both of the possibilities they could defend — a systematic multi-stream sensing artefact of unknown common cause, or a set of surface regions where the models' learned physics failed — and proposed nothing except that somebody find out. Above it all sat the title, plain as a specimen label:

> Structured Excess Residuals in Earth-System World Models: Evidence for Persistent Localised Anomalies in the Terrestrial Sensing Fabric

The form was the anticlimax the moment deserved. Two categories and a cross-list. A licence from a dropdown. Her name after his, the group under both. A tick-box asserting his right to grant what he was granting, which was the morning's one easy question. The listing would go out with the night's batch, at one in the morning UK time, alongside everything else the world had decided it was ready to say aloud.

"Go on," Priya said from behind her screen, in the voice of somebody holding up a wall. "Before I remember that Thursday's list had a page two."

"It didn't."

"I know," she said. "Go on."

He clicked submit.

The page considered, and issued the paper a number, by which the future would now have to cite it. The kettle at the end of the bench came to the boil for somebody's coffee, precisely on the schedule it had kept every working morning for two years. Below the window the city went on writing itself down — buses on their intervals, phones in their pockets, twenty thousand small records a second, none of them yet about him.

Nothing about the world had changed, except that now it could not be unread.
