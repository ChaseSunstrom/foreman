<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Decision memo: options, choice, why, revisit

Use when a choice is costly to reverse, someone else has to approve it, or the same question keeps coming back:
picking a library, a data store, an approach for an M or L task, a vendor, a policy. A memo is short and made
before the work; for a lasting architecture choice, also write an ADR (`../reflect/architecture-decision-records.md`).

Built on library cards: `fm lib show decision-records` (fields a future reader needs),
`fm lib show approach-comparison` (comparing options on the same criteria), `fm lib show kill-criteria`
(when to abandon the choice), `fm lib show adrs` (the long form).

## The procedure

1. **State the question in one sentence** with its deadline and who decides. Pass: it ends in a question mark
   and can be answered by picking an option.
2. **List the constraints that are facts:** budgets, versions, deadlines, measured numbers, each with its source.
   Guesses go in a separate Assumptions list.
3. **Three options at least,** including "do nothing" or "the cheapest thing that could work". Pass: no option
   is a straw man; each has a real advocate's best case.
4. **Score them on the same criteria,** chosen before scoring: cost to build, cost to reverse, risk, fit with
   what exists. A table, one row per option. Evidence beats adjectives: cite a benchmark, a doc page, a file.
5. **Choose and say why in one paragraph,** naming the criterion that decided it and what you give up.
6. **Set the revisit trigger:** a date, or a measurable condition ("p95 over 200 ms", "a second consumer
   appears") that reopens the question. Pass: someone else could tell whether the trigger has fired.
7. **Record it:** `fm decide "<choice>" --why "…" --rejected "…" --revisit "<trigger>"`, plus `--kind costly` or
   `--kind outward` when it is; put the memo in the task's brief or the repo's docs.

## Template

```markdown
# Decision: <question?>
Decides: <who> by <date>
Constraints: <fact (source)> · <fact (source)>
Assumptions: <guess we'd check first>

| Option | Build cost | Reverse cost | Risk | Fit | Evidence |
|--------|-----------|--------------|------|-----|----------|
| A      |           |              |      |     |          |
| B      |           |              |      |     |          |
| Do nothing |       |              |      |     |          |

Choice: <option>, because <deciding criterion>. We give up <cost>.
Revisit: <date or measurable trigger>.
```
