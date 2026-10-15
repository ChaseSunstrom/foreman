---
name: ada
title: Ada
area: lang
tags: [ada, spark, safety-critical, strong-typing, contracts, gnat]
detect: [ext:.adb, ext:.ads, file:*.gpr, file:alire.toml]
related: [rust, vhdl]
---
Ada: strong subtypes, specs apart from bodies, contracts, and proof or runtime checks turned on.

## Verify
- `gprbuild -P project.gpr`: builds the project with GNAT.
- `alr build`: builds an Alire crate (when `alire.toml` exists).
- `gnatprove -P project.gpr --level=2`: proves absence of runtime errors and contracts in SPARK code, when SPARK is used.
- `gnatcheck -P project.gpr`: coding rule checks, when the project configures it.

## Test first
AUnit, or a plain test procedure with an exception check when the project has no framework.
```ada
with Ada.Text_IO; use Ada.Text_IO;
with Stacks;

procedure Test_Stacks is
   S : Stacks.Stack;
begin
   begin
      Stacks.Pop (S);
      raise Program_Error with "pop on empty must fail";
   exception
      when Stacks.Empty_Error => Put_Line ("ok");
   end;
end Test_Stacks;
```

## Do
- Put the interface in `.ads` and the implementation in `.adb`, with a private part to hide representation.
- Define range-constrained types and subtypes (`type Percent is range 0 .. 100`) so invalid values are unrepresentable.
- Add contracts: `Pre`, `Post`, `Type_Invariant` and `Dynamic_Predicate`, and compile with assertions enabled (`-gnata`).
- Use `-gnatwa -gnatVa -gnato` or the project switches to enable warnings and validity and overflow checks.
- Use `limited private` types for resources, and `Ada.Finalization` for cleanup.
- Use unconstrained arrays and attributes (`'First`, `'Last`, `'Range`) instead of hard-coded bounds.
- Use `in`, `out` and `in out` parameter modes accurately, and named association at call sites.
- Raise declared exceptions with messages, and handle them at the layer that can recover.

## Avoid
- `Integer` for everything: no range checking of the domain. Declare a type or subtype.
- Disabling checks (`pragma Suppress`, `-gnatp`) for speed without measurement: it hides faults. Profile first.
- Exception handlers that swallow with `when others => null`: the failure vanishes. Re-raise or log and fail.
- Access types and `Unchecked_Deallocation` where containers or stack objects suffice: leaks and dangling pointers. Use `Ada.Containers`.
- Tasking without protected objects: data races. Guard shared state with a `protected` type.
- `Unchecked_Conversion` between unrelated types: undefined layout assumptions. Use representation clauses and checked conversions.
- Giant packages with mixed concerns: split specs by abstraction.

## Review
- [ ] Domain values use constrained types and contracts.
- [ ] Assertions and runtime checks are enabled in test builds.
- [ ] No blanket exception swallowing.
- [ ] Shared state is in protected objects.
- [ ] SPARK proofs (if used) pass with no new unjustified assumptions.
