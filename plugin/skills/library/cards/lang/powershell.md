---
name: powershell
title: PowerShell
area: lang
tags: [powershell, pwsh, pester, psscriptanalyzer, modules, scripting]
detect: [ext:.ps1, ext:.psm1, ext:.psd1, file:PSScriptAnalyzerSettings.psd1, file:*.Tests.ps1]
related: [bash]
---
PowerShell 7 (pwsh) and Windows PowerShell scripts and modules: Pester 5 tests, PSScriptAnalyzer, advanced functions.

## Verify
- `pwsh -NoProfile -Command "Invoke-ScriptAnalyzer -Path . -Recurse -Severity Warning,Error"`: lints; any output is a finding.
- `pwsh -NoProfile -Command "Invoke-Pester -CI"`: runs `*.Tests.ps1` and sets a non-zero exit code on failure.
- `pwsh -NoProfile -Command "Test-ModuleManifest ./MyMod/MyMod.psd1"`: the manifest is valid and its files exist.
- `pwsh -NoProfile -Command "Import-Module ./MyMod -Force"`: the module imports with no errors.

## Test first
Pester 5: put code under test in `BeforeAll`; test files are named `*.Tests.ps1`.
```powershell
BeforeAll {
    . $PSScriptRoot/../src/Get-Thing.ps1
}

Describe 'Get-Thing' {
    It 'throws on a blank name' {
        { Get-Thing -Name '' } | Should -Throw
    }
    It 'returns nothing for unknown names' {
        Get-Thing -Name 'zzz' | Should -BeNullOrEmpty
    }
}
```

## Do
- Write advanced functions: `[CmdletBinding()]`, a `param()` block with types, `[Parameter(Mandatory)]`, and `ValidateSet`/`ValidateNotNullOrEmpty`.
- Use approved verbs (`Get-Verb`) and `Verb-Noun` names; emit objects, not formatted text (`Write-Output`, not `Write-Host`).
- Set `$ErrorActionPreference = 'Stop'` in scripts and use `try/catch` with `-ErrorAction Stop` on cmdlets; use `throw` for fatal errors.
- Support `-WhatIf`/`-Confirm` on destructive functions: `[CmdletBinding(SupportsShouldProcess)]` and `if ($PSCmdlet.ShouldProcess(...))`.
- Use `Set-StrictMode -Version Latest` at the top of scripts and modules.
- Use `Join-Path` and `$PSScriptRoot` for paths, and `-LiteralPath` for paths with brackets.
- Pass secrets as `[securestring]` or `[pscredential]`, or read them from a vault, never as plain parameters.

## Avoid
- `Invoke-Expression` on built strings: injection. Use the call operator `& $cmd @args` with arrays.
- `Write-Host` for data: not capturable on the pipeline. Use `Write-Output` or return objects, and `Write-Verbose` for diagnostics.
- Pester 4 syntax in Pester 5 (`Should Be` without dash, setup in `Describe` body outside `BeforeAll`): code runs at discovery time and fails. Use `Should -Be` and `BeforeAll`.
- Relying on `$?` or non-terminating errors: they pass silently. Use `-ErrorAction Stop`.
- Returning stray output from a function (an unassigned `.Add()` result): pollutes the return value. Pipe to `$null` or `[void]`.
- Aliases (`gci`, `%`, `?`) in shared scripts: lint warning and unreadable. Use full cmdlet names.
- Hardcoded backslashes: break on Linux and macOS. Use `Join-Path`.

## Review
- [ ] PSScriptAnalyzer is clean, and rule suppressions carry a justification.
- [ ] Functions are advanced, validate input, and return objects.
- [ ] Destructive commands honor `-WhatIf`.
- [ ] No plaintext secrets, `Invoke-Expression`, or `Write-Host` for data.
- [ ] Pester tests cover the error path and run under `-CI`.
