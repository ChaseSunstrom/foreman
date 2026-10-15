---
name: php-modern
title: Modern PHP
area: idioms
tags: [php, types, enums, readonly, attributes, phpstan]
detect: [file:composer.json, file:phpstan.neon]
related: [php, phpunit, composer]
---
Modern PHP 8 style: strict types, typed properties, enums, readonly value objects, match and named arguments.

## Verify
- `composer validate --strict`: composer.json is valid.
- `vendor/bin/phpstan analyse`: static analysis at the configured level.
- `vendor/bin/phpunit`: the test suite.
- `php -l FILE.php`: syntax check for a single file.

## Test first
PHPUnit, with a data provider for the edge cases.
```php
<?php
declare(strict_types=1);

use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\TestCase;

final class StatusTest extends TestCase
{
    #[DataProvider('bad')]
    public function testRejectsUnknown(string $in): void
    {
        $this->expectException(ValueError::class);
        Status::from($in);
    }

    public static function bad(): array { return [[''], ['nope']]; }
}
```

## Do
- Start every file with `declare(strict_types=1);`.
- Type parameters, returns and properties, using union types and `?T`. Use `never`, `void` and `static` where accurate.
- Use backed `enum`s instead of class constants, with `from` and `tryFrom`.
- Use `readonly` properties and constructor promotion for value objects.
- Use `match` (strict comparison, throws on no match) instead of `switch`.
- Use first-class callable syntax (`strlen(...)`) and named arguments for clear calls.
- Use PDO prepared statements, `password_hash` and `random_bytes` for secrets.
- Throw exceptions instead of returning `false` or null for failure, and catch `Throwable` only at boundaries.

## Avoid
- Missing `strict_types`: `"5"` silently coerces to int. Declare it in every file.
- `==` on mixed values: type juggling surprises. Use `===`.
- String-built SQL: injection. Use prepared statements with bound parameters.
- `@` error suppression: it hides faults. Check the condition or handle the exception.
- `array` for everything: unclear shape. Use a readonly class or a typed object, and phpdoc array shapes for the rest.
- `md5` or `sha1` for passwords: use `password_hash` and `password_verify`.
- `extract`, `$$var` and `eval`: unsafe and untraceable. Use explicit variables.
- Class constants as pseudo-enums: no type safety. Use an enum.

## Review
- [ ] `strict_types` and full type declarations on new code.
- [ ] Enums and readonly objects model fixed values and immutable data.
- [ ] All queries are parameterized and secrets use the proper functions.
- [ ] PHPStan passes with no new baseline entries.
- [ ] Tests cover invalid input paths.
