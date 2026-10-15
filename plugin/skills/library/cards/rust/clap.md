---
name: clap
title: clap
area: rust
tags: [rust, cli, clap, arguments, derive, subcommands]
detect: [dep:clap]
related: [cargo, serde, clippy, tokio]
---
clap command-line parsing: derive structs, subcommands, validation, and testing the parser without a process.

## Verify
- `cargo test`: parser tests via `try_parse_from`.
- `cargo run -- --help`: help text renders and matches the intended interface.
- `cargo run -- --bogus; echo $?`: unknown flags print usage and exit 2.
- `cargo clippy --all-targets -- -D warnings`: lint.

## Test first
Assert parsing and validation through `try_parse_from`, which never exits the process.
```rust
use clap::Parser;

#[derive(Parser, Debug)]
struct Cli {
    #[arg(long, default_value_t = 8080)]
    port: u16,
}

#[test]
fn rejects_bad_port() {
    assert!(Cli::try_parse_from(["app", "--port", "99999"]).is_err());
}
```
Add `Cli::command().debug_assert()` in one test to catch definition mistakes early.

## Do
- Enable `features = ["derive"]` and use `#[derive(Parser)]`, `Subcommand`, `Args` and `ValueEnum`.
- Use `#[command(version, about)]` so metadata comes from `Cargo.toml` and doc comments.
- Read environment fallbacks with `#[arg(env = "APP_PORT")]` (needs the `env` feature).
- Model mutually exclusive or dependent flags with `conflicts_with`, `requires` and `ArgGroup`.
- Use `value_parser!` or a custom `value_parser` function for ranges and domain types so errors point at the argument.
- Keep `main` thin: parse, then call a function that takes the typed struct. Return `Result` and print one error message.
- Generate shell completions with `clap_complete` in a subcommand or build script.

## Avoid
- The builder `clap::App` and `with_name` from clap 2/3-era snippets: use `Command` and `Arg::new`, or derive.
- Forgetting the `derive` feature: `Parser` derive not found. Enable it.
- `Cli::parse()` inside tests: it exits the process. Use `try_parse_from`.
- Parsing numbers as `String` then `unwrap()`: use typed fields so clap reports the error and exits 2.
- Positional arguments that begin with `-`: they need `--` or `allow_hyphen_values`. Document it.
- Panicking on invalid input after parse: validate with `value_parser` or return an error and a non-zero exit code.
- Reading `std::env::args()` directly beside clap.

## Review
- [ ] `--help` output is accurate and every flag has a doc comment.
- [ ] Types encode validation, with no unchecked strings.
- [ ] Exit codes are 0 on success, non-zero on failure, and errors go to stderr.
- [ ] Parser tests cover a failure case and a default.
- [ ] A `debug_assert` test guards the definition.
