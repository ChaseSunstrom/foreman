# Critique — Mission 1, model layer (gen 2, the user's gen-2 steer T-2437)

Tasks: T-2485, T-2486, T-2487, T-2488, T-2489 (all done). Mission: gen-2/mission-model-layer.md.

## Closed vs planned
- All five planned briefs are closed: the decision interface and registry (T-2485), the user's rules as checks
  (T-2486), the exam's zero-token replay (T-2487), shadow mode for capture, intake, dedupe and find (T-2488), and the
  surfaces: the MCP decide tool, fm doctor's model backends line, the site's Model layer page and the AGENTS.md line
  (T-2489).
- No use is live, and none should be yet: the rule says a use goes live only by a decision row citing an exam run
  that shows it beating the path it replaces, and no run has scored one.

## Outside signals
- The replay has nothing to score yet: exam.jsonl holds no line with model_replay (no foresight run since T-2487),
  and shadow.jsonl holds only the two rows from T-2494's capture: no capture or intake ran between T-2488's ship and
  that one.
- fm doctor's new line reads "no backend": no local server answers on this machine and no cloud key is set, so the
  night tick's shadow pass has nothing to ask.

## What failed
- The steer names selfjev-4b and jeff behind TYPESAFE_BASE_URL, but the registry never reads that variable: it finds
  only models.json profiles, the four fixed loopback ports and keyed clouds. So the backends the steer names first
  are reachable only by a hand-written models.json profile.
- The shadow covers capture and intake, but sessions make most tasks with fm task new, which writes no shadow row.
  The declared type and tier there are a choice, not the rule's, so the row would score the model against the
  session instead of against the rule.

## What the next Seed should change
- Read TYPESAFE_BASE_URL in the registry (local when its host is loopback, and never sent a key it did not name).
  Then evaluate selfjev-4b, jeff, Von and Jevlike through the install queue once the user says yes to a server.
- Run the foresight arm once there are shadow rows with closed truth. The first number to watch is intake-type's
  rule hits beside the model's, with the model's Brier.
- Decide whether fm task new should log a shadow row, and score that row against the declared type as its own use
  (intake-declared).
