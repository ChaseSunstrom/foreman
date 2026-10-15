---
name: bubbletea
title: Bubble Tea (TUI)
area: go
tags: [go, tui, bubbletea, terminal, lipgloss, elm]
detect: [dep:github.com/charmbracelet/bubbletea, dep:github.com/charmbracelet/bubbles, dep:github.com/charmbracelet/lipgloss]
related: [cobra, go-testing, go-context, viper]
---
Bubble Tea terminal UIs: the Model/Update/View loop, commands for I/O, resize handling and testing Update directly.

## Verify
- `go build ./... && go vet ./...`: compiles; the `Model` interface is satisfied.
- `go test ./...`: Update transitions and View output are asserted.
- `go test -race ./...`: commands and goroutines don't race with the model.
- `go run . < /dev/null`: non-interactive runs fail cleanly (check TTY handling, or use `tea.WithInput(nil)` in tests).

## Test first
Update is a pure function of (model, msg): test it without a terminal.
```go
func TestEnterSubmits(t *testing.T) {
	m := newModel()
	m.input.SetValue("hi")
	next, cmd := m.Update(tea.KeyMsg{Type: tea.KeyEnter})
	if next.(model).submitted != "hi" {
		t.Fatal("not submitted")
	}
	if cmd == nil {
		t.Fatal("expected a command")
	}
}
```

## Do
- Implement `Init() tea.Cmd`, `Update(tea.Msg) (tea.Model, tea.Cmd)`, `View() string` (value or pointer receivers consistently).
- Switch on `msg.(type)`: `tea.KeyMsg` (use `msg.String()`), `tea.WindowSizeMsg`, and your own message types.
- Do I/O only in `tea.Cmd` funcs that return a `tea.Msg`; never block in Update or View.
- Store width and height from `tea.WindowSizeMsg` and size components from them.
- Combine commands with `tea.Batch(...)` (parallel) or `tea.Sequence(...)` (ordered).
- Quit with `tea.Quit`; handle `ctrl+c` explicitly if you intercept keys.
- Compose `bubbles` components (textinput, list, viewport, spinner) by forwarding messages to their `Update` and collecting cmds.
- Style with lipgloss; use `tea.NewProgram(m, tea.WithAltScreen())` for full-screen apps.

## Avoid
- Mutating state from goroutines or commands: races. Send results as messages.
- Blocking calls (HTTP, sleep) in Update: freezes the UI. Wrap in a Cmd.
- Dropping child commands from sub-model updates: spinners and cursors stop. Return and batch them.
- Printing with `fmt.Println` while the program runs: corrupts the screen. Use messages or `tea.Println`, or log to a file with `tea.LogToFile`.
- Hard-coded widths: wrap and truncate wrong on resize. Use the size message.
- Forgetting the pointer-vs-value receiver mismatch: updates seem to vanish. Return the updated model from Update.
- Not restoring the terminal on panic: recover in `main` or rely on the program's cleanup; test crash paths.

## Review
- [ ] Update contains no blocking or I/O.
- [ ] Sub-component commands are returned and batched.
- [ ] Resize is handled and layout derives from it.
- [ ] Transitions are unit-tested via direct `Update` calls.
- [ ] Logging doesn't write to the terminal.
