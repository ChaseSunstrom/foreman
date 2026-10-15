---
name: apex
title: Apex
area: lang
tags: [apex, salesforce, soql, triggers, governor-limits, sfdx]
detect: [ext:.cls, ext:.trigger, file:sfdx-project.json]
related: [sql, java]
---
Salesforce Apex: bulkified code that respects governor limits, trigger handlers and tests with meaningful assertions.

## Verify
- `sf apex run test --test-level RunLocalTests --wait 10 --code-coverage --result-format human`: runs local tests in the default org and shows coverage.
- `sf project deploy validate --source-dir force-app --test-level RunLocalTests`: a check-only deploy that runs tests without saving changes.
- `sf apex run test --class-names MyServiceTest --synchronous`: runs one test class quickly.

## Test first
Create test data in the test, run the logic between `startTest` and `stopTest`, and assert the outcome.
```apex
@IsTest
private class AccountServiceTest {
    @IsTest
    static void bulkInsertSetsRating() {
        List<Account> accs = new List<Account>();
        for (Integer i = 0; i < 200; i++) {
            accs.add(new Account(Name = 'A' + i, AnnualRevenue = 2000000));
        }
        Test.startTest();
        insert accs;
        Test.stopTest();
        Integer hot = [SELECT COUNT() FROM Account WHERE Rating = 'Hot'];
        System.assertEquals(200, hot, 'all large accounts rated Hot');
    }
}
```

## Do
- Bulkify: operate on `List`, `Set` and `Map` of records, with no DML or SOQL inside loops.
- Query once with `WHERE Id IN :ids`, then group results into a `Map<Id, List<SObject>>`.
- Keep one trigger per object that delegates to a handler class, with a clear before/after separation.
- Use `with sharing` by default, and enforce field and object access with `WITH USER_MODE` in SOQL or `Security.stripInaccessible`.
- Bind variables in SOQL (`:var`), and use `Database.insert(list, false)` with result checks when partial success is allowed.
- Use `@TestSetup` for shared data and `Test.setMock` for callouts.
- Use custom metadata or custom settings for configuration, and `Queueable` or `Batchable` for heavy work.
- Use `@IsTest(SeeAllData=false)`, the default, and assert specific values.

## Avoid
- SOQL or DML inside a `for` loop: it hits the 100 query and 150 DML limits with 200 records. Collect, then run one statement.
- Dynamic SOQL built by string concatenation with input: injection. Use binds or `String.escapeSingleQuotes` and allow-lists.
- Hard-coded record Ids: they differ across orgs. Query by name or use custom metadata.
- Tests with no assertions only for coverage: they prove nothing. Assert outcomes and test negative paths.
- Recursive triggers with no guard: infinite loops and limit errors. Use a static flag or check changed fields.
- `without sharing` by habit: it ignores record access. Use it only when justified and documented.
- Assuming order of trigger execution across managed packages and flows: test the whole save.

## Review
- [ ] No SOQL or DML in loops and tests include a 200-record case.
- [ ] Triggers delegate to handlers with recursion control.
- [ ] Sharing and field-level access are handled explicitly.
- [ ] Tests assert behavior and cover failure paths.
- [ ] No hard-coded Ids or credentials.
