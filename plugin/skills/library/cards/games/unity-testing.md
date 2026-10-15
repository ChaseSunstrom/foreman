---
name: unity-testing
title: Unity Test Framework
area: games
tags: [unity, testing, nunit, editmode, playmode, csharp]
detect: [dep:com.unity.test-framework]
related: [unity, unity-ecs, game-loop]
---
Unity Test Framework: NUnit tests in EditMode and PlayMode assemblies, run headless from the command line.

## Verify
- `Unity -batchmode -nographics -projectPath . -runTests -testPlatform EditMode -testResults edit.xml -quit`: edit-mode suite passes, results written as NUnit XML.
- `Unity -batchmode -nographics -projectPath . -runTests -testPlatform PlayMode -testResults play.xml -quit`: play-mode suite passes.
- `Unity -batchmode -projectPath . -runTests -testPlatform EditMode -testFilter "MyNamespace.MyTests" -quit`: one fixture runs alone while iterating.
- `grep -L "testables\|\.asmdef" -r Assets --include=*Tests*`: finds test folders missing an assembly definition.

## Test first
Put logic in plain C# classes so EditMode tests need no scene. Use `[UnityTest]` only when frames must pass.
```csharp
public class HealthTests {
    [Test] public void Damage_ClampsAtZero() {
        var h = new Health(10);
        h.Damage(99);
        Assert.AreEqual(0, h.Current);
    }
    [UnityTest] public IEnumerator Spawner_SpawnsAfterDelay() {
        var go = new GameObject().AddComponent<Spawner>();
        yield return null;
        Assert.AreEqual(1, Object.FindObjectsByType<Enemy>(FindObjectsSortMode.None).Length);
    }
}
```

## Do
- Give tests their own `.asmdef` (Editor platform only for EditMode) referencing `UnityEngine.TestRunner` and `UnityEditor.TestRunner`.
- Separate logic from `MonoBehaviour` shells: tests exercise the plain class, a thin component forwards calls.
- Create objects in `[SetUp]` and destroy them in `[TearDown]` (`Object.DestroyImmediate` in EditMode).
- Drive time with an injected clock or fixed step, never `WaitForSeconds` for real seconds.
- Use `LogAssert.Expect` for expected error logs so unexpected ones fail the test.
- Load test scenes additively and unload in teardown.

## Avoid
- Tests that depend on frame rate or wall-clock sleeps: they flake on CI. Inject time and step manually.
- `Object.Destroy` in EditMode: it is deferred and never runs. Use `DestroyImmediate`.
- Shared static state between tests (singletons): reset it in `[SetUp]` or avoid statics.
- Unlogged errors passing silently: Unity fails a test on an unexpected `Debug.LogError`, so handle or expect each one.
- Test code inside the runtime assembly: it ships in builds. Keep it in a test assembly.

## Review
- [ ] Each test has an asmdef and the suite runs headless with a nonzero exit on failure.
- [ ] No real-time waits; time is injected.
- [ ] Created GameObjects are cleaned up in teardown.
- [ ] Pure logic is covered in EditMode, with PlayMode kept for lifecycle behaviour.
