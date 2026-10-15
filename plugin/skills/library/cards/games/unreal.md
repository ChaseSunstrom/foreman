---
name: unreal
title: Unreal Engine
area: games
tags: [unreal, cpp, game, engine, blueprint, automation]
detect: [file:*.uproject, file:*.Build.cs, file:*.Target.cs]
related: [cpp, cmake]
---
Unreal Engine C++ modules: UCLASS/UPROPERTY reflection, Blueprints, Automation Framework tests, UnrealBuildTool.

## Verify
- `UnrealEditor-Cmd MyGame.uproject -ExecCmds="Automation RunTests MyGame; Quit" -unattended -nullrhi -nosplash -log`: Automation tests under that prefix pass headless.
- `UnrealEditor-Cmd MyGame.uproject -run=CompileAllBlueprints -unattended -nullrhi`: Blueprints still compile (commandlet).
- `git status --short -- Source Config Content`: only intended C++, config and uasset changes.
- `grep -rn "UPROPERTY\|UFUNCTION" Source | head`: reflected members use macros (spot check after edits).

## Test first
Tests live in the module under `Source/MyGame/Private/Tests` and register with the Automation Framework.
```cpp
#include "Misc/AutomationTest.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FHealthClampTest, "MyGame.Health.ClampsAtZero",
    EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FHealthClampTest::RunTest(const FString& Parameters)
{
    FHealthModel H(10);
    H.Damage(50);
    TestEqual(TEXT("health floors at zero"), H.Current, 0);
    return true;
}
```
Keep rules in plain C++ structs so tests need no world; use a spec (`BEGIN_DEFINE_SPEC`) for latent or async cases.

## Do
- Mark every GC-managed `UObject*` member `UPROPERTY()`, or hold it with `TObjectPtr`, `TWeakObjectPtr` or `TStrongObjectPtr`.
- Declare module dependencies in `*.Build.cs` (`PublicDependencyModuleNames` / `PrivateDependencyModuleNames`).
- Use `CreateDefaultSubobject` in constructors and `NewObject` / `SpawnActor` at runtime.
- Expose to Blueprint deliberately: `BlueprintCallable`, `BlueprintReadOnly`, `EditAnywhere` on the minimum needed.
- Use `check`, `ensure` and `verify` appropriately; `ensure` for recoverable states.
- Tick only when needed (`PrimaryActorTick.bCanEverTick = false` by default); prefer timers and events.
- Use `FString` / `FName` / `FText` by role: `FText` for UI, `FName` for keys.

## Avoid
- Raw `UObject*` members without `UPROPERTY`: the garbage collector frees them and leaves dangling pointers. Add `UPROPERTY()`.
- Editing `.generated.h` or forgetting `#include "X.generated.h"` last: reflection breaks. Include it as the final header.
- `GetWorld()` or actor access in constructors or CDOs: null or wrong object. Do it in `BeginPlay`.
- Hard asset references (`ConstructorHelpers::FObjectFinder`) everywhere: loads everything at startup. Use soft references and async loading.
- Ticking every actor for polling: use delegates or `FTimerManager`.
- Changing reflected signatures with Live Coding on: layout changes need a full editor restart and rebuild.
- Committing `Intermediate/`, `Binaries/`, `Saved/`, `DerivedDataCache/`: ignore them.

## Review
- [ ] Every owned `UObject*` is reflected or held by a smart pointer type.
- [ ] `Build.cs` lists each module the new includes need; no circular modules.
- [ ] Blueprint-exposed API is minimal and named for designers.
- [ ] No tick, `GetAllActorsOfClass` or synchronous loads in hot paths.
- [ ] Automation tests cover the new logic, and generated folders are not staged.
