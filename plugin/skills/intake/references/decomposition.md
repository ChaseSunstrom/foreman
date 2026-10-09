# Decomposition recipes (reference)

_Foreman's own reference (T-0624)._

Patterns for cutting a task into steps that can each be checked on their own. Pick the one that fits; `planning.md` covers step order and obligations.

- **One observable per step.** Each step ends in one thing that can be seen: a test passes, a command prints X, a page shows Y. A step whose done-state can't be observed is either part of the next step or two steps.
- **Walking skeleton** (FEATURE L, first step). Build the thinnest path through every layer, end to end, behind a failing acceptance test, then thicken it. Integration risk shows up on day one instead of at the end.
- **Spike, then build.** A `Spike:` step answers one question (does the API paginate, how slow is the query). It is time-boxed and thrown away, and its result is a note or a verified assumption, never shipped code.
- **Expand / migrate / contract.** For a schema, API or format change: add the new form beside the old one (expand), move callers and data over (migrate), then remove the old form (contract). Every step stays deployable, and each has its own rollback.
- **Test ladder.** Climb from the cheapest check that could fail to the most realistic: unit, then integration, then end to end, then live. Stop climbing when a rung proves the criterion.
- **Strangler.** To replace a component, route one path at a time to the new one, keep the old one serving the rest, and delete it when nothing routes to it.
- **Contain, cure, inoculate** (FIX). First stop the harm (a guard, a revert, a flag), then fix the cause, then add the test or guard that keeps it fixed.
