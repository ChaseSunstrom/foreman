---
name: chakra-ui
title: Chakra UI
area: web
tags: [chakra, react, style-props, theme, components, emotion]
detect: [dep:@chakra-ui/react, dep:@chakra-ui/next-js, dep:@chakra-ui/icons]
related: [react, react-hook-form, testing-library]
---
Chakra UI: React components with style props and a themeable system; the API differs sharply between v2 and v3.

## Verify
- `npx tsc --noEmit`: component props and theme tokens type-check.
- `npx eslint .`: lint.
- `npx vitest run`: component tests wrapped in the provider.
- `npm run build`: production build.

## Test first
Wrap in the same provider the app uses, then query by role.
```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Providers } from "./providers";
import { SearchBox } from "./SearchBox";

test("calls onSearch with the typed value", async () => {
  const onSearch = vi.fn();
  render(<Providers><SearchBox onSearch={onSearch} /></Providers>);
  await userEvent.type(screen.getByRole("textbox"), "cats{Enter}");
  expect(onSearch).toHaveBeenCalledWith("cats");
});
```

## Do
- Read the installed major version first (`npm ls @chakra-ui/react`): v2 uses `ChakraProvider` with `extendTheme`; v3 uses `ChakraProvider` with a `system` from `createSystem` and snippet-style components.
- Use style props (`p`, `mt`, `bg`, `color`) with theme tokens and responsive arrays or objects (`{ base: 2, md: 4 }`).
- Define colors, fonts and component variants in the theme or system, not inline.
- Use `Stack`, `Flex`, `Grid` for layout and `useBreakpointValue` only when CSS props cannot express the case.
- Label every `Input` through the field and label components the installed version provides, and surface errors with the invalid state.
- Use color mode tokens (semantic tokens) so dark mode needs no per-component branching.
- Keep one provider at the root and reuse it in tests.

## Avoid
- Copying v2 code (`extendTheme`, `useDisclosure` from the root, `FormControl`) into a v3 project, or the reverse: the imports differ or do not exist. Check the version's docs and types.
- Hard-coded hex colors in style props: dark mode and theming break. Use tokens.
- Wrapping every element in `Box` with long style-prop lists repeatedly: extract a component or a recipe or variant.
- Tests without the provider: styles and context-dependent components throw or render wrongly.
- Icon-only buttons without `aria-label`: inaccessible. Add the label.
- Using `useColorMode` flags to switch colors manually: use semantic tokens.

## Review
- [ ] The code matches the installed major version's API.
- [ ] Theme tokens carry all colors, fonts and variants.
- [ ] Icon buttons and inputs have accessible names.
- [ ] Responsive behavior is expressed through breakpoint props.
- [ ] Tests render through the app provider.
