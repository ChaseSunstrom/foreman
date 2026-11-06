Verdict: changes needed (one MEDIUM); tests not run by the reviewer (read-only tools).

## lens: intent
- MEDIUM — plugin/lib/fmgenesis.py free_beats — top-gap lines on fm exam scorecard are built from the Haiku-stamped s31-006 line with no label. Fix: label the gap. FIXED: gaps from a Haiku line end "(from a Haiku smoke run)", tested.
- MEDIUM — plugin/lib/fmgenesis.py _select — select still decides from Haiku lines (steer rule 4 vs "ignore"). FIXED: fm decide records it (rule 4: provisional), CHANGELOG and MASTER say select still counts them and the done gate never.
- LOW — "default" stamp counts as production. FIXED: smoke() docstring and MASTER say "default" is the configured model; grade --model may replace a "default" stamp.

## lens: adversary
ok. Model strings are c.plain'd and truncated before the answers file and lineage.md.

## lens: edge
- LOW — grade --model can't correct a "default" stamp. FIXED, tested.
- LOW — error printed "None answers" with no --agent. FIXED.
- LOW — grade --model on a non-session agent silently ignored. FIXED: refused, tested.

## lens: operator
ok. Negligible extra reads.

## lens: maintainer
- LOW — smoke() sits away from _exam. FIXED: moved next to _exam.
- LOW — no free_beats test with a Haiku line. FIXED.

Checked and dropped: draft-* lines carry no model, but fm genesis exam drafts on a fixed sonnet child (fmgenesis.py:1140), so no Haiku draft line can exist.
