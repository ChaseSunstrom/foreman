---
name: clang-format
title: clang-format
area: native
tags: [cpp, c, formatting, style, clang, ci, pre-commit]
detect: [file:.clang-format, file:_clang-format]
related: [clang-tidy, cpp-modern, cmake, llvm-tooling]
---
clang-format: one committed .clang-format, applied in place locally and checked with --dry-run -Werror in CI.

## Verify
- `clang-format --dry-run -Werror $(git ls-files '*.cpp' '*.hpp' '*.h' '*.cc')`: non-zero exit if any file differs from the style.
- `clang-format -i $(git ls-files '*.cpp' '*.hpp' '*.h')`: apply formatting in place.
- `clang-format --version`: confirm the same version as CI uses.
- `clang-format --style=file --dump-config`: prints the effective config found for the cwd.

## Test first
The failing check is the dry run on a misformatted file.
```sh
printf 'int main(){return 0;}\n' > /tmp/t.cpp
clang-format --style=file:.clang-format --dry-run -Werror /tmp/t.cpp   # exits non-zero
clang-format --style=file:.clang-format -i /tmp/t.cpp
clang-format --style=file:.clang-format --dry-run -Werror /tmp/t.cpp   # exits 0
```
Wire the dry-run into CI or a pre-commit hook so it fails before the format commit lands.

## Do
- Commit `.clang-format` at the repo root, based on a named style: `BasedOnStyle: Google` (or LLVM, Chromium, Mozilla, WebKit), then override a few keys such as `IndentWidth: 4` and `ColumnLimit: 100`.
- Run clang-format as its own commit when first adopted, and list that commit in `.git-blame-ignore-revs`.
- Use `git clang-format` to format only changed lines in an existing codebase.
- Order includes through `IncludeBlocks: Regroup` and `IncludeCategories`, keeping the main header first.
- Protect hand-aligned tables with `// clang-format off` and `// clang-format on`.
- Add `SortIncludes: CaseSensitive` or `Never` deliberately; headers that need order should not be reordered silently.
- Pin the clang-format version in CI and pre-commit; output differs between major versions.
- Add a `.clang-format-ignore` file for generated or vendored paths.

## Avoid
- Formatting with an editor's built-in default instead of the repo file: churn between contributors. Use `--style=file`.
- Different clang-format versions locally and in CI: endless diff ping-pong. Pin one.
- Bulk reformatting mixed with logic changes: unreviewable. Separate commits.
- Unknown keys for the installed version: it errors or silently ignores. Check `--dump-config` output.
- Formatting generated protobuf or third-party code: exclude it.
- Using `AllowShortFunctionsOnASingleLine: All` and then expecting readable diffs: pick `Inline` or `None`.

## Review
- [ ] `.clang-format` is committed, and its version is pinned in CI.
- [ ] CI uses `--dry-run -Werror`, not an auto-fix that hides drift.
- [ ] The adoption commit is in `.git-blame-ignore-revs`.
- [ ] Vendored and generated code is excluded.
