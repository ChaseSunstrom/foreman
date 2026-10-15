---
name: mockito
title: Mockito
area: jvm
tags: [java, kotlin, mocking, testing, junit, verify]
detect: [dep:mockito-core, dep:mockito-junit-jupiter, dep:mockito-kotlin, dep:mockk]
related: [junit5, spring-boot, kotlin-coroutines]
---
Mockito mocks and stubs: when/then, argument matchers, verification, captors, strict stubbing under JUnit 5.

## Verify
- `./mvnw -q test` (or `./gradlew test`): mocks behave and strict stubs report unused stubbings.
- `./mvnw -q dependency:tree | grep -i -E "mockito|byte-buddy"`: one Mockito and ByteBuddy version, with the inline mock maker on the JDK in use.
- `./gradlew test -i | grep -i "UnnecessaryStubbing"`: no stale stubs.

## Test first
Mock collaborators only; assert on outcome first, interactions second.
```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {
  @Mock PaymentGateway gateway;
  @InjectMocks OrderService service;

  @Test void failedChargeCancelsOrder() {
    when(gateway.charge(any())).thenThrow(new PaymentException("declined"));
    assertEquals(Status.CANCELLED, service.place(order()).status());
    verify(gateway).charge(any());
  }
}
```

## Do
- Use `MockitoExtension` (from `mockito-junit-jupiter`) with `@Mock`, `@InjectMocks` and `@Captor`; its strict stubs fail tests on unused stubbings.
- Stub with `when(x.m()).thenReturn(v)`; for void methods use `doThrow(...).when(x).m()`.
- Use `ArgumentCaptor` to inspect arguments passed to a collaborator.
- Use `verifyNoMoreInteractions` only where the interaction set is the contract.
- Prefer real objects or fakes for value types and simple collaborators; mock boundaries (HTTP, clock, repository).
- Mock static methods only with `mockStatic` inside try-with-resources, and rarely.
- Kotlin: use `mockito-kotlin` or MockK for final classes and `any()` on non-null parameters.

## Avoid
- Mixing raw values and matchers in one call: `verify(x).m(any(), "a")` throws `InvalidUseOfMatchersException`. Use `eq("a")`.
- Mocking the class under test or types you own with trivial logic: tests then verify the mock.
- `lenient()` everywhere to silence strictness: delete the unused stub instead.
- `doReturn` on a spy to avoid real calls, then asserting nothing: spies hide design problems.
- `Mockito.mock` of final classes without the inline mock maker: it is the default in Mockito 5; in older versions enable `mockito-inline`.
- Verifying private or incidental calls: couples tests to implementation.
- `@RunWith(MockitoJUnitRunner.class)`: JUnit 4. Use `@ExtendWith(MockitoExtension.class)`.

## Review
- [ ] Each mock stands for an external boundary or a slow collaborator.
- [ ] Assertions check results, not only `verify` calls.
- [ ] No unused stubs, and no blanket `lenient()`.
- [ ] Matchers are not mixed with raw values.
- [ ] Time, randomness and IO are injected and stubbed.
