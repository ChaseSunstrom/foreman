---
name: viper
title: Viper configuration
area: go
tags: [go, config, viper, env, cobra, yaml]
detect: [dep:github.com/spf13/viper]
related: [cobra, go-testing, go-errors, go-slog]
---
Viper config loading: explicit precedence, env binding, unmarshal into a validated struct, with per-test instances.

## Verify
- `go build ./... && go vet ./...`: compiles.
- `go test ./...`: config tests cover file, env and flag precedence.
- `APP_PORT=9999 go run . config show` (if you ship such a command): environment overrides take effect.
- `go test -race ./...`: no shared global viper state across tests.

## Test first
Create an instance per test; assert precedence and defaults.
```go
func TestEnvOverridesFile(t *testing.T) {
	t.Setenv("APP_PORT", "9000")
	v := viper.New()
	v.SetConfigType("yaml")
	_ = v.ReadConfig(strings.NewReader("port: 8000\n"))
	v.SetEnvPrefix("APP")
	v.AutomaticEnv()
	if v.GetInt("port") != 9000 {
		t.Fatal("env should win")
	}
}
```

## Do
- Use `viper.New()` and pass the instance; don't rely on the global.
- Precedence is explicit `Set`, then flags, then env, then config file, then defaults. Set defaults with `SetDefault`.
- Env: `SetEnvPrefix("APP")`, `SetEnvKeyReplacer(strings.NewReplacer(".", "_"))`, `AutomaticEnv()`. Nested keys need the replacer.
- Bind cobra/pflag flags: `v.BindPFlag("port", cmd.Flags().Lookup("port"))`.
- Search paths with `SetConfigName`, `AddConfigPath`; treat `viper.ConfigFileNotFoundError` (via `errors.As`) as optional, other read errors as fatal.
- `Unmarshal(&cfg)` into a struct with `mapstructure` tags, then validate (required fields, ranges) in one place.
- Fail fast at startup on invalid config; log the resolved values with secrets redacted.
- Keep secrets in env or a secret store, not in committed config files.

## Avoid
- `AutomaticEnv` alone expecting `Unmarshal` to see env-only keys: unknown keys aren't picked up. Set defaults or `BindEnv` for every key.
- Using the global viper in tests: leaks state between tests. Use fresh instances and `t.Setenv`.
- Forgetting the key replacer: `a.b` doesn't map to `A_B`. Add it.
- Silent defaults hiding typos: `GetInt("prot")` returns 0. Unmarshal and validate.
- Keys are case-insensitive, so two keys differing only by case collide. Keep one casing.
- Checking `err != nil` from `ReadInConfig` and exiting on "not found" when a file is optional.
- Mutating config at runtime from several goroutines: unsafe; viper isn't synchronized for writes. Treat as read-only after startup.
- Dots in map keys: viper splits on the key delimiter. Change it with `viper.NewWithOptions(viper.KeyDelimiter("::"))` if needed.

## Review
- [ ] Config is loaded once into a typed, validated struct.
- [ ] Precedence is tested (file, env, flag).
- [ ] Missing optional file is tolerated; other errors fail startup.
- [ ] No secrets in repo config; logged config is redacted.
- [ ] Tests use isolated instances.
