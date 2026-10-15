---
name: perl
title: Perl
area: lang
tags: [perl, cpan, prove, perlcritic, test-more, scripting]
detect: [ext:.pl, ext:.pm, ext:.t, file:cpanfile, file:Makefile.PL, file:Build.PL, file:dist.ini]
related: [bash]
---
Perl 5 code: strict and warnings, CPAN dependencies via cpanfile, Test::More with `prove`, Perl::Critic.

## Verify
- `perl -wc script.pl`: compiles with warnings on, no execution.
- `prove -lr t/`: runs every `t/*.t` with `lib/` on `@INC`.
- `perlcritic --severity 4 lib script`: policy violations (severity 5 strictest, 1 gentlest).
- `perltidy -b -bext='/' file.pm`: formats in place with no backup file (config in `.perltidyrc`).
- `cpanm --installdeps --notest .`: dependencies in `cpanfile` or `Makefile.PL` resolve.

## Test first
Tests are `t/*.t` files using Test::More; `prove` shows TAP failures.
```perl
use strict; use warnings;
use Test::More;
use My::Parse qw(parse_int);

is parse_int("42"), 42, 'parses digits';
is parse_int(""), undef, 'blank is undef';
eval { parse_int(undef) };
like $@, qr/required/, 'undef croaks';

done_testing;
```

## Do
- Start every file with `use strict; use warnings;` (or `use v5.36;`, which enables both).
- Declare dependencies in `cpanfile` (`requires 'Path::Tiny';`) and pin with `cpanfile.snapshot` via Carton when reproducibility matters.
- Use `Carp` (`croak`) in modules so errors point at the caller; use `Try::Tiny` or `try/catch` feature (5.34+ experimental) instead of bare `eval`.
- Use three-argument `open` with lexical handles and check the result: `open my $fh, '<:encoding(UTF-8)', $path or die "...: $!"`.
- Use `Path::Tiny`, `JSON::PP`, `Getopt::Long` and `File::Temp` before hand-rolled equivalents.
- Run with `-T` taint mode for programs handling untrusted input, and untaint with strict regexes.

## Avoid
- Two-argument `open`, bareword handles and backticks or `system` with interpolated strings: shell injection and path surprises. Use list-form `system @cmd` and three-arg open.
- `eval { ... }; if ($@)` without guarding clobbered `$@`: destructors can reset it. Use Try::Tiny or the `$ok = eval {...; 1}` idiom.
- Regex on structured data (HTML, JSON, CSV): use a parser module.
- `my $x = ... if $cond;`: undefined behavior. Declare first, then assign.
- Relying on hash order: it is randomized. Sort keys when output must be stable.
- Forgetting `use utf8` and encoding layers: mojibake and "wide character" warnings. Decode on input, encode on output.
- Slurping with `local $/;` outside a tight block: leaks to later reads. Scope it in `do { local $/; <$fh> }`.

## Review
- [ ] Every file uses strict and warnings, and `perl -wc` is quiet.
- [ ] No string-form `system`, backticks or `eval` of user data.
- [ ] File opens are three-arg with an explicit encoding, and failures are checked.
- [ ] New CPAN modules are in `cpanfile` or the dist metadata.
- [ ] `prove -lr t/` passes and has a test for the failure path.
