---
name: storybook
title: Storybook
area: web
tags: [storybook, components, ui, stories, visual-testing, a11y]
detect: [dep:storybook, dep:@storybook/*, file:.storybook/main.*]
related: [react, vue, svelte, testing-library, playwright, tailwind]
---
Storybook: component stories in CSF, with play functions as interaction tests and the a11y addon.

## Verify
- `npx storybook build`: every story compiles and the static site builds.
- `npx tsc --noEmit`: story `Meta`/`StoryObj` types match component props.
- `npx test-storybook`: runs stories and play functions (needs the test runner and a running or built Storybook).
- `npx eslint . --max-warnings 0`: with `eslint-plugin-storybook`.

## Test first
Write the story with a play function that fails first; it asserts through Testing Library.
```tsx
import type { Meta, StoryObj } from "@storybook/react";
import { expect, userEvent, within } from "@storybook/test";
import { LoginForm } from "./LoginForm";

const meta = { component: LoginForm } satisfies Meta<typeof LoginForm>;
export default meta;

export const RejectsEmptyEmail: StoryObj<typeof meta> = {
  play: async ({ canvasElement }) => {
    const c = within(canvasElement);
    await userEvent.click(c.getByRole("button", { name: /sign in/i }));
    await expect(c.getByText(/email is required/i)).toBeInTheDocument();
  },
};
```
Check the installed major version; the `expect`/`userEvent` import location has changed between releases.

## Do
- Write `*.stories.tsx` (or `.ts`/`.svelte`/`.vue`) beside the component with a default `Meta` export and named `StoryObj` exports.
- Cover each meaningful state as its own story: empty, loading, error, long text, disabled.
- Use `args` and `argTypes` for controls; derive docs with the `autodocs` tag.
- Put app-wide providers, theme and global CSS in `.storybook/preview`, using decorators.
- Mock the network at the story level with MSW (`msw-storybook-addon`) instead of editing the component.
- Enable `@storybook/addon-a11y` and fix violations.
- Run stories in CI via `test-storybook` against the static build.

## Avoid
- Stories that import real API clients or global singletons: flaky and slow. Mock at the boundary.
- Hand-written `Story.bind({})` templates (CSF2) in new code: use CSF3 objects.
- Importing from the old `@storybook/addons` or `@storybook/testing-library` packages when the installed version has moved them: check the installed docs.
- Play functions that assert on implementation (class names, state): use roles and visible text.
- Skipping a11y addon failures with a blanket `parameters.a11y.disable`: fix the component or scope the rule off per story with a reason.
- One mega-story with all props: hides regressions. One state per story.

## Review
- [ ] Each state of the component has a story, and interaction stories have play functions.
- [ ] Stories are deterministic: no real network, time or randomness.
- [ ] a11y checks are on and passing.
- [ ] `storybook build` and `test-storybook` run in CI.
- [ ] Types in `Meta` and `args` match the component.
