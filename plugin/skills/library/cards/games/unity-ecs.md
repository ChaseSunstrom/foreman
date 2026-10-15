---
name: unity-ecs
title: Unity ECS (DOTS)
area: games
tags: [unity, ecs, dots, entities, burst, jobs, csharp]
detect: [dep:com.unity.entities]
related: [unity, unity-testing, game-loop]
---
Unity Entities: components as unmanaged data, systems as ISystem, Burst-compiled jobs, baking from authoring GameObjects.

## Verify
- `Unity -batchmode -nographics -projectPath . -runTests -testPlatform EditMode -testResults results.xml -quit`: edit-mode tests, including system tests on a test World, pass.
- `Unity -batchmode -nographics -projectPath . -runTests -testPlatform PlayMode -testResults play.xml -quit`: play-mode tests pass with Burst and safety checks on.
- `grep -rn "class .*: *ComponentData\|List<\|string " Assets --include=*Component*.cs`: finds managed fields that leaked into component data.

## Test first
Build a throwaway World, add entities, update the system once, assert on component data.
```csharp
[Test] public void Mover_AdvancesPosition() {
    using var world = new World("t");
    var em = world.EntityManager;
    var e = em.CreateEntity(typeof(LocalTransform), typeof(Speed));
    em.SetComponentData(e, new Speed { Value = 2f });
    world.GetOrCreateSystem<MoverSystem>();
    world.Update();
    Assert.Greater(em.GetComponentData<LocalTransform>(e).Position.x, 0f);
}
```

## Do
- Keep components unmanaged and small (blittable fields, `FixedString`, `BlobAssetReference` for shared read-only data).
- Write systems as `partial struct : ISystem` with `[BurstCompile]` on the struct and `OnUpdate`. Use `SystemAPI.Query` or `IJobEntity`.
- Bake authoring data with a `Baker<T>`; call `GetEntity(TransformUsageFlags...)` and declare dependencies through the baker API.
- Use `EntityCommandBuffer` from an `EndSimulationEntityCommandBufferSystem` singleton for structural changes made in jobs.
- Use tag components and `IEnableableComponent` instead of adding or removing components every frame.
- Order work with `[UpdateInGroup]` and `[UpdateBefore]` or `[UpdateAfter]`. Pass job handles through `state.Dependency`.
- Schedule parallel jobs (`ScheduleParallel`) when iterations are independent.

## Avoid
- Structural changes (create, destroy, add component) inside a foreach over a query: they invalidate it. Record them in an ECB and play it back.
- Managed types (class, string, arrays) in components: Burst rejects them. Use blob assets or native containers.
- `.Complete()` on jobs right after scheduling: it serialises the frame. Chain handles through `state.Dependency`.
- Reading authoring MonoBehaviours at runtime: only baked data exists in the World. Move needed fields in the baker.
- Disabling safety checks or Burst to silence an error: fix the race or the aliasing instead.
- Sync points hidden in `GetComponent` per entity in loops: use `ComponentLookup` fetched once in `OnUpdate`.

## Review
- [ ] No managed fields in component structs and no allocation in `OnUpdate`.
- [ ] All structural changes go through an ECB, not mid-iteration.
- [ ] Jobs declare read-only access (`RefRO`, `[ReadOnly]`) where they do not write.
- [ ] Baker registers every dependency it reads so re-baking triggers.
- [ ] A test world covers each system's main path and an empty-query case.
