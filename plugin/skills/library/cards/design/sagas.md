---
name: sagas
title: Sagas
area: design
tags: [saga, distributed-transactions, compensation, orchestration, choreography, workflow]
detect: [dep:temporalio, dep:@temporalio/client, dep:go.temporal.io/sdk, dep:camunda-*, dep:masstransit, dep:MassTransit, dep:axon-*, dep:conductor-*]
related: [event-driven, idempotency, retries-backoff, microservices, state-machines]
---
Multi-service business transactions as a sequence of local steps with compensations, run by an orchestrator or by events.

## Verify
- `pytest -q tests/saga`: every step failure triggers the right compensations, in reverse order.
- `temporal workflow list` (Temporal): no workflows stuck running or failed unexpectedly.
- `psql -c "select state, count(*) from saga_instances group by 1"`: no pile-up of instances in a non-terminal state (custom saga table).

## Test first
Fail each step in turn and assert the end state is consistent.
```python
@pytest.mark.parametrize("fail_at", ["reserve_stock", "charge_card", "create_shipment"])
def test_failure_compensates_prior_steps(fail_at, services):
    services.fail(fail_at)
    result = PlaceOrderSaga(services).run(order_id="o1")
    assert result.state == "compensated"
    assert services.stock.reserved("o1") == 0
    assert services.payments.charged("o1") == 0
```

## Do
- Break the flow into local transactions, each with a defined compensating action (`reserve` and `release`, `charge` and `refund`).
- Prefer orchestration (one coordinator holding state) for flows of more than three steps or with branching. Use choreography for short, stable flows.
- Persist saga state (step, status, data) before and after each step, so a crash resumes.
- Make every step and every compensation idempotent, and retry them until they succeed.
- Order steps so the hardest-to-undo ones come last (pivot step), such as charge before shipping.
- Add semantic locks or pending states (`PENDING`, `RESERVED`), since intermediate state is visible to other requests.
- Use timeouts per step and an overall deadline that triggers compensation.
- Give each saga instance a correlation ID carried on every command and event.

## Avoid
- Treating a compensation as a rollback: effects such as emails sent can't be erased. Model compensation as a new business action.
- Compensations that can fail permanently and are not alerted: stuck money or stock. Retry, then escalate to manual handling.
- Non-idempotent steps under at-least-once messaging: duplicates double-apply. Dedupe by saga ID plus step.
- Orchestrator state held only in memory: a restart loses all in-flight sagas. Persist it, or use a durable workflow engine.
- Distributed two-phase commit across services: it blocks and scales poorly. Use a saga.
- Reading intermediate data as final: other requests see pending state. Expose status explicitly.
- Non-deterministic code in Temporal workflows (random, time, network): replay breaks. Do such work in activities.

## Review
- [ ] Each step has a documented, idempotent compensation.
- [ ] State is persisted, and a crash-and-resume test exists.
- [ ] Failure at every step is tested for a consistent end state.
- [ ] Stuck or failed compensations raise an alert and have a manual path.
- [ ] Timeouts and a correlation ID exist.
