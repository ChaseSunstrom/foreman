---
name: test-doubles
title: Test doubles
area: testing
tags: [mock, stub, fake, spy, isolation, dependency-injection]
detect: []
related: [unit-test-design, contract-testing, integration-testing, tdd]
---
Stubs, fakes, spies and mocks: replace slow or nondeterministic collaborators at the boundary, and keep real behavior everywhere else.

## Verify
- `pytest -q`: with `unittest.mock.create_autospec` or `patch(..., autospec=True)`, a call with a wrong signature raises.
- `jest --coverage=false --silent=false`: no unexpected console output from unmocked calls.
- `go test -race ./...`: fakes shared across goroutines are race-free.
- `grep -rn "mock.patch\|jest.mock" tests | wc -l`: a rough count to spot over-mocking (trend, not a rule).

## Test first
Prefer a hand-written fake for a port you own; assert on outcomes.
```python
class FakeMailer:
    def __init__(self): self.sent = []
    def send(self, to, body): self.sent.append((to, body))

def test_signup_sends_welcome_email():
    mailer = FakeMailer()
    signup("a@b.co", mailer=mailer)
    assert mailer.sent == [("a@b.co", "Welcome")]
```
Doubles live in `tests/support` or beside the interface they implement.

## Do
- Inject dependencies through constructor or parameter so tests pass a double without patching modules.
- Use a stub for canned answers, a fake (in-memory repo) for working behavior, a spy to record calls, a mock only when the interaction is the requirement.
- Mock at your own boundary (an interface you define around the HTTP client), not the library internals.
- Use autospec or typed mocks (`jest.mocked`, interface-generated mocks) so signature drift fails the test.
- Keep one contract test suite run against both the fake and the real adapter so they cannot diverge.
- Reset doubles per test.

## Avoid
- Mocking the unit under test or pure value objects: the test proves nothing. Use the real thing.
- `patch` on the importing module's wrong path (patching where defined, not where used): the real code still runs. Patch the lookup site.
- Asserting call counts and argument order for every collaborator: tests break on refactor. Assert outcomes unless the call is the contract.
- Mocking third-party types you do not own with invented behavior: the double drifts from reality. Wrap the library and fake the wrapper.
- Unreset global mocks (`jest.spyOn` without `restoreAllMocks`): leaks into other tests. Restore in teardown.
- A mock that returns a mock chain: signals a design problem. Introduce a narrower interface.

## Review
- [ ] Every double replaces a boundary (network, disk, clock, process), not internal logic.
- [ ] Mocks are spec-bound so signature changes break tests.
- [ ] Fakes have their own contract test against the real implementation.
- [ ] Assertions focus on results; interaction asserts are justified.
- [ ] No double outlives its test.
