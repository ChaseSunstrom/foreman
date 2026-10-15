---
name: ruby
title: Ruby
area: lang
tags: [ruby, bundler, rubocop, rspec, minitest, gems]
detect: [ext:.rb, file:Gemfile, file:Gemfile.lock, file:*.gemspec, file:Rakefile]
related: [rails, rspec]
---
Ruby baseline: Bundler-managed gems, RuboCop, RSpec or Minitest, frozen string literals, and explicit error handling.

## Verify
- `bundle exec rubocop`: style and lint under the repo's config.
- `bundle exec rspec` (or `bundle exec rake test`): the suite, with locked gem versions.
- `bundle check`: installed gems satisfy the Gemfile.lock.
- `ruby -wc lib/foo.rb`: syntax check with warnings.

## Test first
RSpec in `spec/`, files `*_spec.rb` mirroring `lib/`.
```ruby
require "port_parser"

RSpec.describe PortParser do
  it "rejects an empty string" do
    expect { described_class.parse("") }.to raise_error(ArgumentError)
  end
end
```
Minitest equivalent: `test/*_test.rb` with `assert_raises`.

## Do
- Run everything through `bundle exec`; commit `Gemfile.lock` for applications.
- Start files with `# frozen_string_literal: true`.
- Raise specific exception classes (subclass `StandardError`) and rescue narrowly.
- Use keyword arguments for options; use `fetch` on hashes when a key is required.
- Use `Struct` or `Data.define` (where the Ruby version has it) for simple value objects.
- Use `Comparable`, `Enumerable` and `each_with_object` instead of manual loops.
- Use `Time.now.utc` or an injected clock; use `Pathname` and `File.open` with a block.

## Avoid
- `rescue Exception` or bare `rescue` swallowing: catches signals and hides bugs. Rescue `StandardError` subclasses and re-raise unknowns.
- `eval`, `send` with user-controlled names, and `Marshal.load` or `YAML.load` on untrusted input: code execution. Use whitelists, JSON and `YAML.safe_load`.
- Backticks and `system("cmd #{input}")`: shell injection. Use `system("cmd", arg)` or `Open3.capture3` with an array.
- Mutating a string literal or shared default (`def f(opts = {})` then mutating): surprises across calls. Dup or freeze.
- `Object#try`-style nil chains in plain Ruby: use `&.`.
- Monkey-patching core classes globally: breaks gems. Use refinements or a wrapper.
- Running `gem install` or bare `rspec` outside Bundler: wrong gem versions. Use `bundle exec`.
- `||=` for booleans that may be `false`: recomputes every time. Use `defined?` or an explicit check.

## Review
- [ ] No broad rescues, `eval`, or shell interpolation with external input.
- [ ] Gemfile and Gemfile.lock agree and are committed.
- [ ] RuboCop clean without blanket disables.
- [ ] Hash keys and arguments required are enforced (`fetch`, keywords).
- [ ] Specs cover an error path and run via Bundler.
