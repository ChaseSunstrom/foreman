---
name: prolog
title: Prolog
area: lang
tags: [prolog, logic, unification, backtracking, swi-prolog, constraints]
detect: [ext:.pl, ext:.pro, ext:.plt]
related: [racket, common-lisp]
---
Prolog (SWI-Prolog): declarative relations, careful cuts, determinism checks and plunit tests.

## Verify
- `swipl -g run_tests -t halt file.pl`: loads the file and runs its plunit tests, exiting when done.
- `swipl -q -g "consult('file.pl')" -t halt`: loads and reports syntax or singleton-variable warnings.
- `swipl -g "make" -t halt`: reloads modified files and shows new warnings.

## Test first
plunit, with `true`, `fail`, `all` and `throws` options.
```prolog
:- begin_tests(path).
:- use_module(graph).

test(reaches) :- path(a, c).
test(no_cycle_loop, [fail]) :- path(c, a).
test(all, all(X == [b, c])) :- path(a, X).
test(bad_arg, [throws(error(type_error(_, _), _))]) :- path(1, _).
:- end_tests(path).
```

## Do
- Describe relations, not procedures: write facts and rules that can run in several modes, and document the mode with `%! name(+In, -Out) is det.`.
- Keep recursion clause order: base case first, and make the recursive call last to allow tail recursion.
- Use first-argument indexing: put the most discriminating argument first.
- Use `library(clpfd)` for integer constraints instead of generate-and-test arithmetic.
- Use accumulators for long lists, and `maplist`, `foldl` and `include` from `library(apply)`.
- Use `must_be/2` to validate inputs and throw ISO errors.
- Use `library(dcg/basics)` and DCG rules for parsing.
- Collect solutions with `findall`, `bagof` or `aggregate_all`, and use `once/1` or `->` when only one solution is wanted.

## Avoid
- Cuts to patch wrong logic: they break reversibility and hide bugs. Prefer if-then-else (`->`) with deterministic guards, or restructure clauses.
- `is/2` with an unbound right side: instantiation error. Ensure inputs are bound, or use `clpfd` (`#=`).
- Left recursion (`path(X,Y) :- path(X,Z), edge(Z,Y)`): infinite loop. Make the recursion go through a base step, or use tabling (`:- table path/2.`).
- `assert` and `retract` for general state: order-dependent and untestable. Pass state through arguments.
- Singleton variable warnings ignored: usually a typo. Rename unused variables to start with `_`.
- Negation (`\+`) with unbound variables: it does not mean "for all". Bind variables first.
- `=` where `==` or `=:=` is meant: `=` unifies, it does not compare.

## Review
- [ ] Each predicate documents its modes and determinism.
- [ ] No unexplained cuts, and no left recursion without tabling.
- [ ] No singleton warnings on load.
- [ ] plunit tests cover success, failure and error cases.
- [ ] Global state through `assert` is absent or justified.
