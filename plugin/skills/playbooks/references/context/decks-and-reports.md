<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Decks and reports: the answer first

Use when making something people read to decide or to stay informed: a slide deck, a written report, a status
update, a results write-up, a proposal. Charts inside follow `../ui/data-viz.md`; a page someone follows to do a task
is `docs.md`.

## The procedure

1. **Name the reader and the decision.** One line: who reads this and what they will decide or do after it. Pass:
   the line exists; material that doesn't serve that decision moves to an appendix.
2. **Lead with the answer and the ask.** The first slide or paragraph holds the conclusion and what you need ("Ship
   v2 on 4 Nov; we need two more reviewers"). Pass: someone who stops after it knows what you want from them.
3. **One message per slide, said in its title.** Each title is a full-sentence claim ("Cache hits cut p95 latency
   by 40%"), and the body is the evidence for it. Pass: the titles alone, read in order, tell the whole story
   (list them with `grep -E "^#{1,2} " deck.md` for Markdown slides).
4. **Every number carries its source, its comparison and its unit**: where and when it was measured, against what
   (last period, target, control), in what unit. A bare number fails.
5. **Keep it lean.** A slide holds at most 30 words of body text and one chart; slide text is 24 pt or larger; a
   report section fits one screen before the next heading.
6. **Say what you don't know.** A short section names the uncertainties, the risks with an owner each, and what
   would change the conclusion.
7. **Build it from source.** Slides and reports are text (Markdown, Typst, LaTeX) built by one command, and figures
   are drawn by a script from the data, so a rerun refreshes every number. Pass: no screenshot of a chart, and the
   build command is written at the top of the source.
8. **Status updates keep one shape**: done since last time, next, blocked or needs, risks. Same order every time.
   Red, amber and green appear only with a reason beside them, and with a word as well as the colour.
9. **Check before sending.** Read the titles alone; trace every number to its source; render the final format
   (PDF or slides) and look at every page; every figure has alt text.

## Checks

- [ ] The reader and the decision are named; the first slide or paragraph holds the answer and the ask.
- [ ] Every slide title is a sentence, and the titles alone tell the story.
- [ ] Every number has a source, a comparison and a unit.
- [ ] No slide has more than 30 words of body text or more than one chart.
- [ ] One command rebuilds the document and its figures from data.
- [ ] Every figure has alt text; the rendered file was looked at page by page.

## Library cards

`fm lib show technical-writing`, `fm lib show typst`, `fm lib show latex`, `fm lib show mermaid`,
`fm lib show diagrams-as-code`, `fm lib show matplotlib`, `fm lib show plotly`, `fm lib show metrics-and-guardrails`
(picking the number that matters).
