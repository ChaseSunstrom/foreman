---
name: unity
title: Unity
area: games
tags: [unity, csharp, game, engine, nunit, ecs]
detect: [file:ProjectSettings/ProjectVersion.txt, file:Assets/*.meta, dep:com.unity.test-framework]
related: [csharp, dotnet]
---
Unity projects: C# MonoBehaviours and ScriptableObjects, Test Framework (NUnit) in Edit and Play modes, asmdef-split code.

## Verify
- `Unity -batchmode -nographics -projectPath . -runTests -testPlatform EditMode -testResults editmode.xml`: Edit Mode tests pass headless (exit code is non-zero on failure).
- `Unity -batchmode -nographics -projectPath . -runTests -testPlatform PlayMode -testResults playmode.xml`: Play Mode tests pass.
- `Unity -batchmode -nographics -projectPath . -logFile - -quit`: the project imports and compiles with no script errors.
- `git status --short -- '*.meta'`: every new asset or folder has its `.meta` committed.

## Test first
Put tests in `Assets/Tests/EditMode` or `Assets/Tests/PlayMode`, each with its own `.asmdef` that references the code under test and the `UnityEngine.TestRunner` and `UnityEditor.TestRunner` assemblies.
```csharp
using NUnit.Framework;
using System.Collections;
using UnityEngine.TestTools;

public class HealthTests {
    [Test] public void Damage_ClampsAtZero() {
        var h = new Health(10);
        h.Damage(50);
        Assert.AreEqual(0, h.Current);
    }
    [UnityTest] public IEnumerator Spawner_SpawnsAfterOneFrame() {
        var go = new UnityEngine.GameObject().AddComponent<Spawner>();
        yield return null;
        Assert.AreEqual(1, go.Count);
    }
}
```
Keep game logic in plain C# classes so Edit Mode tests reach it without a scene.

## Do
- Split code into assembly definitions (`.asmdef`): faster recompiles and tests can reference only what they need.
- Cache `GetComponent` results in `Awake`; wire references with `[SerializeField] private` fields.
- Put shared data and config in `ScriptableObject` assets, not static fields or singletons.
- Move physics work to `FixedUpdate` and use `Time.deltaTime` in `Update`.
- Pool frequently spawned objects with `UnityEngine.Pool.ObjectPool<T>`.
- Load assets through Addressables or `Resources` only where intended; unload handles you acquire.
- Commit `.meta` files and set Asset Serialization to Force Text with Visible Meta Files.

## Avoid
- `Find`, `FindObjectOfType` or `GetComponent` inside `Update`: allocates and scans every frame. Cache once.
- `FindObjectOfType` in new code: deprecated in favor of `FindFirstObjectByType` / `FindAnyObjectByType`.
- String-based `SendMessage` or `Invoke("Name")`: breaks silently on rename. Use direct calls, events or `nameof`.
- Per-frame allocations (LINQ, string concatenation, `new List` in `Update`): GC spikes. Reuse buffers.
- Comparing destroyed objects with `?.` or `??`: Unity's fake-null bypasses them. Use `if (obj)` or `obj != null`.
- Editing `Library/` or `Temp/` into git: ignore them; only `Assets`, `Packages`, `ProjectSettings` belong.
- Using `UnityEditor` APIs in runtime code: the player build fails. Guard with `#if UNITY_EDITOR` or an editor asmdef.

## Review
- [ ] No per-frame lookups or allocations in `Update`, `LateUpdate` or `FixedUpdate`.
- [ ] New assets have `.meta` files; no `Library/` or `Temp/` content staged.
- [ ] Editor-only code is behind an editor asmdef or `#if UNITY_EDITOR`.
- [ ] Logic is testable without a scene, with Edit Mode tests added or updated.
- [ ] Coroutines and event subscriptions are stopped or unsubscribed in `OnDisable` or `OnDestroy`.
