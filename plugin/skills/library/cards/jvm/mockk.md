---
name: mockk
title: MockK
area: jvm
tags: [kotlin, mocking, testing, coroutines, verification, spy]
detect: [dep:mockk, dep:mockk-android, dep:springmockk]
related: [kotest, junit5, kotlin-coroutines, mockito, spring-boot-testing]
---
MockK for Kotlin: mock final classes, objects and suspend functions with `every`/`coEvery`, and verify behavior that matters.

## Verify
- `./gradlew test`: the mocks behave and verifications hold.
- `./gradlew test --tests "*ServiceTest"`: one class while iterating.
- `grep -rnE "import org.mockito" src/test`: no stray Mockito in a MockK suite (final classes would fail).
- `grep -rn "unmockkAll\|clearAllMocks" src/test`: global state is reset where mocks are static or object-based.

## Test first
Tests in `src/test/kotlin`. Stub, act, verify the interaction that is the contract.
```kotlin
class NotifierTest {
    private val mailer = mockk<Mailer>()
    private val notifier = Notifier(mailer)

    @Test
    fun `sends one mail per user and survives a failure`() = runTest {
        coEvery { mailer.send("a") } throws IOException()
        coEvery { mailer.send("b") } returns Unit
        notifier.notifyAll(listOf("a", "b"))
        coVerify(exactly = 1) { mailer.send("b") }
    }
}
```

## Do
- Create strict mocks with `mockk<T>()` and stub what the test needs; use `relaxed = true` only for irrelevant collaborators.
- Use `coEvery` and `coVerify` for suspend functions, `every`/`verify` otherwise.
- Capture arguments with `slot<T>()` or `capture(list)`, and match with `any()`, `eq()`, `match { }`.
- Use `verify { mock.method() wasNot Called }` or `confirmVerified(mock)` to catch unexpected interactions.
- Use `spyk(real)` sparingly, and `every { spy.x() } answers { ... }` for partial behavior.
- Mock objects and statics with `mockkObject`, `mockkStatic`, `mockkConstructor`, and always `unmockkAll()` in `@AfterEach`.
- For Spring Boot use `springmockk` (`@MockkBean`) rather than Mockito annotations.
- Prefer fakes for simple collaborators; mock at boundaries.

## Avoid
- Relaxed mocks everywhere: missing stubs return defaults and tests pass for the wrong reason. Make mocks strict.
- `every` on a suspend function: compile error or wrong behavior. Use `coEvery`.
- `mockkStatic` or `mockkObject` without `unmockkAll()`: leaks into other tests, order-dependent failures. Reset in teardown.
- Verifying implementation details (call order of getters): brittle. Verify outputs and key side effects.
- Using `mockk(relaxUnitFun = true)` then forgetting to verify the Unit call that matters.
- Mocking data classes and value types: construct real ones.
- Running MockK-heavy tests in parallel with shared static mocks: races. Isolate or serialize.

## Review
- [ ] Mocks are strict unless a comment justifies relaxed.
- [ ] Suspend functions use `coEvery` and `coVerify`.
- [ ] Static and object mocks are undone in teardown.
- [ ] Verifications target meaningful interactions, with `confirmVerified` where the contract is exact.
- [ ] Real objects are used for simple data and fakes where possible.
