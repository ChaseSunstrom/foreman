---
name: nuget
title: NuGet
area: dotnet
tags: [dotnet, csharp, nuget, packages, dependencies, supply-chain]
detect: [file:nuget.config, file:NuGet.Config, file:Directory.Packages.props, file:packages.lock.json, file:*.nuspec]
related: [dotnet-cli, aspnet-core, xunit]
---
NuGet package management: PackageReference, central versions, sources, lock files, vulnerability audit and publishing.

## Verify
- `dotnet restore`: all packages resolve from the configured sources.
- `dotnet list package --vulnerable --include-transitive`: no known-vulnerable packages, direct or transitive.
- `dotnet list package --outdated`: what is behind (informational).
- `dotnet restore --locked-mode`: restore matches `packages.lock.json` exactly.
- `dotnet pack -c Release`: a library produces a valid .nupkg.

## Test first
For a package-policy change, the failing check is the restore or audit. Make it red before the fix.
```
# add a pinned bad version, confirm audit fails
dotnet add src/App package Newtonsoft.Json --version 9.0.1
dotnet list src/App package --vulnerable --include-transitive   # lists advisories
# fix: bump, re-run until the vulnerable section is empty
```
For a library you publish, add a test project that references the packed .nupkg from a local source and exercises the public API.

## Do
- Use `PackageReference` in the csproj (the only supported format for SDK-style projects).
- Centralize versions in `Directory.Packages.props` with `ManagePackageVersionsCentrally`; csproj entries then omit `Version`.
- Declare sources and `packageSourceMapping` in `nuget.config` so each package ID comes from one trusted feed.
- Enable lock files with `RestorePackagesWithLockFile` and restore with `--locked-mode` in CI.
- Mark build-only packages `PrivateAssets="all"` (analyzers, source generators) so consumers do not inherit them.
- For libraries set `PackageId`, `Version`, `Description`, `PackageLicenseExpression`, and `PackageReadmeFile` in the csproj.
- Use `NuGetAudit` settings to fail on vulnerabilities at restore (`NuGetAuditMode`, `NuGetAuditLevel`, plus `TreatWarningsAsErrors`).

## Avoid
- Floating versions (`1.*`, `*`) in apps: nondeterministic builds. Pin exact versions.
- Several feeds with no source mapping: dependency-confusion risk, because a public package can shadow a private name. Add `packageSourceMapping`.
- Committing API keys in nuget.config: use `%NUGET_API_KEY%` style environment variables or CI secrets.
- `packages.config` or `Install-Package` guidance from old tutorials: use PackageReference and `dotnet add package`.
- Referencing a package for one helper: copy the few lines or use the BCL.
- Bumping versions of a package family piecemeal (for example Microsoft.Extensions.* or EF Core): mismatches fail at runtime. Update the family together.
- Publishing without symbols or source link for open libraries: use `.snupkg` and `Deterministic` builds.

## Review
- [ ] Versions are pinned and centralized; lock file is committed if used.
- [ ] Sources are mapped and no secrets are in nuget.config.
- [ ] Audit shows no vulnerable direct or transitive packages.
- [ ] New dependencies are justified, licensed acceptably and maintained.
- [ ] Packable projects carry full metadata and pass `dotnet pack`.
