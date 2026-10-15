---
name: ruby-metaprogramming
title: Ruby metaprogramming
area: idioms
tags: [ruby, metaprogramming, dsl, method-missing, refinements, rspec]
detect: [file:Gemfile, file:*.gemspec]
related: [ruby, rspec, rubocop]
---
Ruby metaprogramming kept honest: define methods explicitly, respond to what you handle, and test the generated behavior.

## Verify
- `bundle exec rspec`: the suite, including specs for generated methods.
- `bundle exec rubocop`: flags `method_missing` without `respond_to_missing?` and other metaprogramming smells.
- `ruby -wc FILE.rb`: syntax check with warnings enabled.

## Test first
Assert the generated interface, including `respond_to?`.
```ruby
RSpec.describe Settings do
  it "defines readers and reports them" do
    s = Settings.new(timeout: 5)
    expect(s.timeout).to eq(5)
    expect(s).to respond_to(:timeout)
    expect { s.missing }.to raise_error(NoMethodError)
  end
end
```

## Do
- Prefer `define_method` or `class_eval` with a string only when needed, and define methods at load time, not on each call.
- Pair every `method_missing` with `respond_to_missing?`, delegate unknown names to `super`, and keep the matched set narrow.
- Use `public_send` instead of `send` when the method name comes from outside.
- Use `Module#prepend` to wrap behavior, calling `super`, instead of alias chains.
- Use refinements to scope monkey patches to the files that opt in.
- Use `instance_variable_get` and `instance_variable_set` sparingly, and `Comparable` or `Enumerable` mixins instead of hand-rolled methods.
- Use hooks (`included`, `inherited`, `extended`) for setup, and keep them small.
- Document DSL entry points and freeze constant tables.

## Avoid
- `method_missing` alone: `respond_to?` lies and `method(:x)` fails. Add `respond_to_missing?`.
- `eval` of strings built from user input: code execution. Use `public_send` with an allow-list.
- `send` with an untrusted name: it also calls private methods. Use `public_send` after checking the name.
- Global monkey patches of core classes (`String`, `Hash`): they leak into every gem. Use refinements or a helper module.
- Defining methods inside a frequently called method: slow, and it invalidates method caches. Define once at class load.
- `Class.new` DSL with hidden global state: tests interfere. Reset in `after` hooks.
- Alias method chains (`alias_method :old, :new`): they break under double load. Use `prepend`.

## Review
- [ ] Each `method_missing` has `respond_to_missing?` and falls through to `super`.
- [ ] No `eval` or `send` on external input.
- [ ] Generated methods are visible to `respond_to?` and have specs.
- [ ] Core extensions are refinements or clearly scoped.
- [ ] A plain method would not have been simpler.
