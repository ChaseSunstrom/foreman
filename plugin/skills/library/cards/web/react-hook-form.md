---
name: react-hook-form
title: React Hook Form
area: web
tags: [react, forms, validation, zod, hooks, typescript]
detect: [dep:react-hook-form]
related: [react, testing-library, zustand]
---
React Hook Form: uncontrolled inputs registered by ref, validation through a resolver (Zod or similar), minimal re-renders.

## Verify
- `npx tsc --noEmit`: form values are typed from the schema.
- `npx vitest run`: form behavior through the DOM.
- `npx eslint . --max-warnings 0`: lint.

## Test first
Drive the form like a user and assert error messages and the submit payload.
```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { SignupForm } from "./SignupForm";

test("blocks submit with an invalid email", async () => {
  const onSubmit = vi.fn();
  render(<SignupForm onSubmit={onSubmit} />);
  await userEvent.type(screen.getByLabelText(/email/i), "nope");
  await userEvent.click(screen.getByRole("button", { name: /sign up/i }));
  expect(await screen.findByText(/valid email/i)).toBeInTheDocument();
  expect(onSubmit).not.toHaveBeenCalled();
});
```

## Do
- Define one schema (Zod, Valibot, Yup) and pass it through `resolver: zodResolver(schema)` from `@hookform/resolvers`.
- Type the form from the schema: `useForm<z.infer<typeof schema>>`.
- Set `defaultValues` for every field so inputs are never uncontrolled-to-controlled.
- Wire native inputs with `{...register("email")}` and read errors from `formState.errors.email?.message`.
- Wrap custom or UI-library components with `<Controller>` or `useController`.
- Submit with `handleSubmit(onValid, onInvalid)`; disable the button while `formState.isSubmitting`.
- Map server validation errors back with `setError("email", { message })`.
- Use `useFieldArray` for repeating rows, keyed by the generated `field.id`.
- Label every input and link errors with `aria-invalid` and `aria-describedby`.

## Avoid
- Controlled `value`/`onChange` on every field "like normal React": defeats the library and re-renders constantly. Use `register`.
- No `defaultValues` (undefined start): warnings and `reset()` bugs. Provide them all.
- Using `field.id` replaced by the array index as a `useFieldArray` key: state sticks to the wrong row. Use `field.id`.
- Reading `formState` properties you did not touch (`isDirty`, `errors`) outside render: it is a proxy that subscribes on read. Read them during render.
- `watch()` for whole-form logic in the root component: re-renders everything. Use `useWatch` in the child that needs it.
- Client-side validation only: the server must validate again. Reuse the schema server-side.
- Registering a custom component without forwarding the ref: `register` silently does nothing. Use `Controller`.

## Review
- [ ] A single schema validates on the client and the server.
- [ ] All fields have `defaultValues`, labels and accessible error text.
- [ ] Server errors are mapped back to fields.
- [ ] Submit is disabled or guarded during submission.
- [ ] Tests assert both the invalid and the valid submit paths.
