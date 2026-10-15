---
name: state-machines
title: State machines
area: design
tags: [state-machine, workflow, transitions, invariants, status, lifecycle]
detect: [dep:transitions, dep:python-statemachine, dep:xstate, dep:aasm, dep:stateless, dep:Stateless, dep:looplab/fsm]
related: [domain-driven-design, sagas, event-sourcing, idempotency, concurrency]
---
Model lifecycles as explicit states, allowed transitions and guards in one table, instead of scattered status checks.

## Verify
- `pytest -q tests/state`: every legal transition passes and every illegal one is rejected.
- `grep -rnE "\.status\s*=[^=]" src | grep -v "state_machine\|transitions"`: status is set only through the machine (expect no output; adjust the field name).
- `psql -c "select status, count(*) from orders group by 1"`: only declared states exist in data.

## Test first
Enumerate the transition table, and test the whole matrix.
```python
ALLOWED = {("draft","submitted"), ("submitted","paid"), ("paid","shipped"),
           ("submitted","cancelled"), ("paid","refunded")}

@pytest.mark.parametrize("src", STATES)
@pytest.mark.parametrize("dst", STATES)
def test_transition_matrix(src, dst):
    order = Order(status=src)
    if (src, dst) in ALLOWED:
        order.transition(dst); assert order.status == dst
    else:
        with pytest.raises(IllegalTransition):
            order.transition(dst)
```

## Do
- List states and the allowed (from, event, to) triples in one data structure that code and docs both read.
- Name transitions as events (`pay`, `ship`, `cancel`), and make each one the only way to change the state.
- Put guards (preconditions) and actions (effects) on the transition, and keep guards pure.
- Mark terminal states (`shipped`, `cancelled`) and make them accept no transitions.
- Persist the state in one column, with a DB `CHECK` constraint or enum listing the valid values, plus a transitions history table (from, to, at, actor).
- Apply a transition atomically with optimistic concurrency: `UPDATE ... SET status='paid' WHERE id=? AND status='submitted'`, and treat zero rows updated as a conflict.
- Make transitions idempotent where retries happen: re-applying `pay` to a paid order returns success or a clear no-op.
- Emit a domain event after each committed transition.

## Avoid
- Boolean flag combinations (`is_paid`, `is_shipped`, `is_cancelled`): impossible combinations become representable. Use one state.
- `if status == X` checks sprinkled across handlers: rules drift apart. Ask the machine whether a transition is allowed.
- Read-modify-write on the status without a condition: two requests both transition from the old state. Use a conditional update or a row lock.
- Performing side effects inside guards: a failed guard that already charged a card. Keep guards pure, and effects in actions after validation.
- Adding a state without updating the matrix test, the DB constraint and the docs: derive them from the table.
- Silent transitions to the same state treated as errors in retried flows: decide the behavior and test it.
- Deleting history rows: keep transitions for audit and debugging.

## Review
- [ ] A single table defines states, events, guards and targets.
- [ ] All status changes go through it, and a matrix test covers every pair.
- [ ] The DB constrains valid states, and transitions use conditional updates.
- [ ] Terminal states are explicit, and history is recorded.
- [ ] Retried transitions are idempotent by decision.
