---
name: php
title: PHP
area: lang
tags: [php, composer, phpunit, phpstan, psr, pdo]
detect: [ext:.php, file:composer.json, file:composer.lock, file:phpunit.xml, file:phpunit.xml.dist]
related: [laravel, symfony]
---
PHP baseline: Composer with PSR-4 autoload, strict types, PHPStan or Psalm, PHPUnit, PDO prepared statements.

## Verify
- `composer validate --strict`: composer.json is valid and consistent.
- `vendor/bin/phpunit`: the test suite.
- `vendor/bin/phpstan analyse`: static analysis at the configured level.
- `composer audit`: installed packages with known advisories.
- `php -l src/Foo.php`: syntax check for one file.

## Test first
PHPUnit, tests in `tests/`, class `FooTest extends TestCase`, namespaced under `autoload-dev`.
```php
<?php
declare(strict_types=1);

use PHPUnit\Framework\TestCase;

final class PortParserTest extends TestCase
{
    public function testRejectsEmpty(): void
    {
        $this->expectException(InvalidArgumentException::class);
        PortParser::parse('');
    }
}
```

## Do
- Put `declare(strict_types=1);` first in every file; type all parameters, returns and properties.
- Autoload with PSR-4 in composer.json; run `composer dump-autoload` after namespace changes; commit `composer.lock` for apps.
- Use PDO with prepared statements and `PDO::ERRMODE_EXCEPTION`.
- Use `readonly` properties, enums and constructor promotion where the PHP version supports them.
- Use `===`, `match` and null-safe `?->`; use `password_hash` and `password_verify` for passwords.
- Escape output with `htmlspecialchars($s, ENT_QUOTES, 'UTF-8')` or the template engine's auto-escape.
- Convert warnings and notices to exceptions in the bootstrap or framework error handler.

## Avoid
- String-built SQL (`"... WHERE id = $id"`): injection. Use `prepare` and bound parameters.
- Loose `==` and `in_array` without strict: `"abc" == 0`-style coercion bugs. Use `===` and `in_array($x, $a, true)`.
- `md5` or `sha1` for passwords or tokens: fast and broken for this use. Use `password_hash` and `random_bytes`.
- `unserialize` on user input and `extract($_POST)`: object injection and variable overwrite. Use JSON and explicit reads.
- `include $_GET['page']`: file inclusion. Use an allowlist map.
- Suppressing errors with `@`: hides failures. Check return values or throw.
- `rand()`/`mt_rand()` for secrets: predictable. Use `random_int`/`random_bytes`.
- Trusting `$_FILES['x']['type']` or the filename: client-controlled. Check content and generate your own name.

## Review
- [ ] Every file has strict types; no untyped public APIs.
- [ ] All SQL is parameterized; all output is escaped.
- [ ] Passwords and tokens use the proper primitives.
- [ ] No `@`, `extract`, `unserialize` or dynamic `include` on external input.
- [ ] PHPStan clean and tests cover an error path.
