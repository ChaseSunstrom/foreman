---
name: fluentvalidation
title: FluentValidation
area: dotnet
tags: [dotnet, csharp, validation, rules, aspnet, models]
detect: [dep:FluentValidation, dep:FluentValidation.DependencyInjectionExtensions]
related: [mediatr, aspnet-core, minimal-apis, xunit]
---
FluentValidation: strongly typed `AbstractValidator<T>` rule sets, tested alone and wired into the pipeline explicitly.

## Verify
- `dotnet build -warnaserror`: validators compile against the current model shape.
- `dotnet test --filter "FullyQualifiedName~Validator"`: rule tests pass, with no host needed.
- `dotnet test --filter "FullyQualifiedName~ValidatorRegistration"`: every validator is registered in DI.

## Test first
Use `FluentValidation.TestHelper` and check the failing property.
```csharp
using FluentValidation.TestHelper;

public class CreateUserValidatorTests
{
    private readonly CreateUserValidator _v = new();

    [Fact]
    public void Email_must_be_valid()
    {
        var r = _v.TestValidate(new CreateUser("not-an-email", "pw12345678"));
        r.ShouldHaveValidationErrorFor(x => x.Email);
        r.ShouldNotHaveValidationErrorFor(x => x.Password);
    }
}
```

## Do
- Register with `services.AddValidatorsFromAssemblyContaining<CreateUserValidator>()` (from the DependencyInjection extensions package).
- Validate manually in the endpoint or a pipeline behavior: `await validator.ValidateAsync(model, ct)`, then return `result.ToDictionary()` through `Results.ValidationProblem(...)`.
- Use `.WithMessage` and `.WithErrorCode` so clients can key on stable codes, not text.
- Use `MustAsync` and `ValidateAsync` for I/O rules (uniqueness), and never call the sync `Validate` on a validator with async rules, because it throws.
- Reuse sub-validators with `.SetValidator(new AddressValidator())` and collections with `RuleForEach`.
- Use `When`/`Unless` and rule sets for conditional rules. Set `CascadeMode` per rule when you want the first failure only.

## Avoid
- The old `FluentValidation.AspNetCore` auto-validation: it is deprecated and does not support async rules. Validate explicitly instead.
- Instantiating validators with `new` inside handlers: it bypasses DI and the dependencies they need. Inject `IValidator<T>`.
- Database uniqueness checks as the only guard: they race. Back them with a unique index and catch the violation.
- Validators registered as singletons that capture scoped services such as a DbContext: use the default scoped lifetime.
- Putting business rules in validators: validate shape and cheap invariants only, and enforce domain rules in the domain.
- Testing only the happy path: assert one failure per rule with `ShouldHaveValidationErrorFor`.

## Review
- [ ] Each rule has a stable error code and a message tested for its property.
- [ ] Async rules run through `ValidateAsync` only.
- [ ] Uniqueness is also enforced in the database.
- [ ] All validators are discoverable through the registration call, and a test resolves them.
- [ ] Validation failures come back as 400 problem details with field names.
