---
name: shadcn-ui
title: shadcn/ui
area: web
tags: [shadcn, react, tailwind, radix, components, cva]
detect: [file:components.json, dep:class-variance-authority, dep:tailwind-merge]
related: [radix-ui, tailwind, react, react-hook-form]
---
shadcn/ui: components copied into your repo over Radix primitives, styled with Tailwind, cva variants and a cn helper.

## Verify
- `npx tsc --noEmit`: copied components and your usages type-check.
- `npx eslint .`: lint, including hooks rules inside copied files.
- `npx vitest run`: component behavior tests.
- `npx shadcn@latest diff`: lists upstream changes to components you copied (check the CLI help if the subcommand differs in your version).

## Test first
Test your composition through roles, since the markup is Radix-driven.
```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { DeleteDialog } from "./DeleteDialog";

test("confirm button calls onConfirm", async () => {
  const onConfirm = vi.fn();
  render(<DeleteDialog open onConfirm={onConfirm} />);
  await userEvent.click(screen.getByRole("button", { name: /delete/i }));
  expect(onConfirm).toHaveBeenCalledOnce();
});
```

## Do
- Add components with the CLI (`npx shadcn@latest add button`) so imports, aliases and dependencies match `components.json`.
- Treat copied files as yours: edit variants in the file, keep the `cva` structure and `cn()` merging.
- Style through theme CSS variables (`--background`, `--primary`) so light and dark mode follow tokens.
- Compose dialogs, menus and popovers with their parts (`DialogTrigger`, `DialogContent`, `DialogTitle`) and keep a title and description for accessibility.
- Use `asChild` to render a trigger as your own element (such as a router `Link`) instead of nesting buttons inside links.
- Pair forms with `react-hook-form` and `zod` through the form component.
- Check the installed Tailwind major version before copying config: setup differs between v3 and v4.

## Avoid
- Installing it as an npm library or importing from a package: the components live in your repo. Add them via the CLI.
- Concatenating class strings by hand: conflicts resolve wrongly. Use `cn(...)` (clsx plus `tailwind-merge`).
- Hard-coded colors (`bg-gray-900`) in components: dark mode and theming break. Use token classes.
- Removing `DialogTitle` or labels to make a design fit: it breaks screen readers. Hide visually with `sr-only`.
- Overwriting customized components by re-running `add` without reviewing the diff: back up or use `--overwrite` deliberately.
- `<Button><a>` nesting: invalid HTML. Use `asChild`.

## Review
- [ ] Components were added via the CLI and match `components.json` aliases.
- [ ] Classes merge through `cn` and colors come from tokens.
- [ ] Dialogs, menus and selects have titles, labels and keyboard support intact.
- [ ] Customizations are in the copied file, not monkey-patched via global CSS overrides.
- [ ] Dark mode and focus states were checked.
