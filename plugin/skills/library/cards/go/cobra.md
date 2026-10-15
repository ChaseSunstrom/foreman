---
name: cobra
title: Cobra
area: go
tags: [go, cli, cobra, commands, flags, viper]
detect: [dep:github.com/spf13/cobra]
related: [go-testing, go-modules, go-concurrency]
---
Cobra CLIs: command tree, flags, RunE error handling, and testing commands in process.

## Verify
- `go build -o /tmp/app . && /tmp/app --help`: the command tree and help render.
- `/tmp/app nosuchcmd; echo $?`: unknown commands fail with a non-zero exit.
- `go test ./... -race -count=1`: command tests.
- `go vet ./...`: static checks.

## Test first
Build the root command in a function, set args and output buffers, then execute.
```go
func TestAddRequiresName(t *testing.T) {
	cmd := NewRootCmd()
	var out bytes.Buffer
	cmd.SetOut(&out)
	cmd.SetErr(&out)
	cmd.SetArgs([]string{"add"})
	if err := cmd.Execute(); err == nil {
		t.Fatal("expected error for missing name")
	}
}
```
Never rely on package-level command variables in tests: they keep flag state between runs.

## Do
- Return errors with `RunE`, not `Run`, and let `main` print once and `os.Exit(1)`. Set `SilenceUsage: true` once errors are runtime, not usage.
- Validate positional arguments with `Args: cobra.ExactArgs(1)` and friends.
- Use `PersistentFlags` for options shared by subcommands and `Flags` for local ones. Mark required ones with `MarkFlagRequired`.
- Use `MarkFlagsMutuallyExclusive` and `MarkFlagsRequiredTogether` for flag relations.
- Construct commands in `NewXCmd()` functions that take dependencies. Avoid `init()` registration and globals.
- Write output with `cmd.OutOrStdout()` and `cmd.ErrOrStderr()` so tests can capture it.
- Use `cmd.Context()` for cancellation and `ExecuteContext` in `main` with a signal-aware context.
- Add shell completion with the built-in `completion` command and `ValidArgsFunction` for dynamic values.

## Avoid
- `fmt.Println` directly in commands: tests can't capture it. Use `cmd.OutOrStdout()`.
- Calling `os.Exit` inside `RunE`: it skips deferred cleanup and breaks tests. Return the error.
- Global flag variables bound in `init()`: they leak state between tests and subcommands. Bind in the constructor.
- `Run` that logs an error and returns normally: exit code 0 on failure. Use `RunE`.
- Reading viper or env in many places: resolve config once in `PersistentPreRunE`.
- Binding the same viper key to multiple flags of the same name across subcommands: the last wins. Bind per command in `PreRunE`.
- Forgetting that `PersistentPreRun` on a child replaces the parent's: call the parent's or use `EnableTraverseRunHooks` if available.

## Review
- [ ] Failures return non-zero and print one clear error to stderr.
- [ ] Args and flags are validated declaratively.
- [ ] Commands are constructed by functions with injected dependencies.
- [ ] Output goes through the command's writers.
- [ ] Tests execute the real command tree with set args.
