---
name: matlab
title: MATLAB
area: lang
tags: [matlab, numerical, matrices, vectorization, simulation, scripting]
detect: [ext:.m, ext:.mlx, ext:.slx]
related: [python, julia, numpy]
---
MATLAB code: vectorized matrix operations, functions in files, preallocation and function-based unit tests.

## Verify
- `matlab -batch "results = runtests; assertSuccess(results)"`: runs every test in the folder and fails the process on any failure.
- `matlab -batch "checkcode('myfile.m')"`: static analysis messages for a file.
- `matlab -batch "profile on; main; profile off; profile('info')"`: collects profile data for a run.

## Test first
Function-based tests: a file named `test*.m` with local test functions.
```matlab
function tests = testNormalize
    tests = functiontests(localfunctions);
end

function testUnitLength(testCase)
    v = normalizeVec([3 4]);
    verifyEqual(testCase, v, [0.6 0.8], 'AbsTol', 1e-12);
end

function testZeroVectorErrors(testCase)
    verifyError(testCase, @() normalizeVec([0 0]), 'normalizeVec:zero');
end
```

## Do
- Put each function in its own file named after it, with a help comment block on the first lines.
- Vectorize with matrix and elementwise operators (`.*`, `./`, `.^`) and logical indexing instead of loops.
- Preallocate arrays (`zeros`, `nan`) before a loop that fills them.
- Validate arguments with an `arguments` block (size, class, validators) at the top of functions.
- Use `isequal`, `ismembertol` and tolerances for floating-point comparison.
- Use `containers.map`, tables and structs for labeled data, and `cellfun` or `arrayfun` for non-uniform data.
- Use `error('pkg:id', 'message %d', n)` with identifiers, and test them with `verifyError`.
- Keep scripts for top-level workflow and functions for reusable logic, and add the code to the path with `addpath` or projects.

## Avoid
- Growing arrays inside a loop (`x(end+1) = v`): repeated reallocation. Preallocate.
- `==` on floating-point values: rounding makes it fail. Compare with a tolerance.
- `*` where elementwise `.*` is meant: it does matrix multiplication or errors. Use the dotted operator.
- `eval` and `evalin`: opaque and slow. Use function handles and structs.
- Variables named like functions (`sum`, `max`, `length`): they shadow the function silently. Rename them.
- Reliance on global variables and `clear all` in scripts: hidden state. Pass arguments and return values.
- Using `i` and `j` as loop variables when complex numbers appear: shadows the imaginary unit. Use `ii` or `1i`.
- Ignoring implicit expansion differences with older code: check dimensions explicitly with `size`.

## Review
- [ ] Functions have help text, an `arguments` block and tested error identifiers.
- [ ] Loops that can be vectorized are, and the rest preallocate.
- [ ] Float comparisons use tolerances.
- [ ] No shadowed built-in names and no `eval`.
- [ ] `runtests` passes in batch mode.
