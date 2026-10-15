---
name: debian-packaging
title: Debian packaging
area: tools
tags: [debian, deb, packaging, dpkg, linux, apt]
detect: [file:debian/control, file:debian/changelog, file:debian/rules]
related: [make, shell-scripting, hadolint]
---
Debian packaging: build .deb packages from a debian/ directory (control, rules, changelog, install files) and check them with lintian.

## Verify
- `dpkg-buildpackage -us -uc -b`: builds the binary package unsigned, in the source tree.
- `lintian -i --fail-on error ../*.changes`: policy and packaging errors, with explanations.
- `dpkg-deb -I ../pkg_1.0-1_amd64.deb`: control fields of the built package.
- `dpkg-deb -c ../pkg_1.0-1_amd64.deb`: the file list, to confirm paths and modes.
- `dpkg-parsechangelog`: the changelog parses, and shows version and distribution.

## Test first
Build before and after the change, and compare the contents.
```
dpkg-buildpackage -us -uc -b
dpkg-deb -c ../pkg_*_amd64.deb | grep usr/bin/tool    # fails if the install file is missing it
lintian -i ../pkg_*.changes
# install in a clean container to prove dependencies:
# docker run --rm -v "$PWD/..":/d debian:stable sh -c 'apt-get update && apt-get install -y /d/pkg_*.deb && tool --version'
```

## Do
- Keep `debian/control` accurate: `Source`, `Build-Depends`, `Package`, `Depends: ${misc:Depends}, ${shlibs:Depends}`, and a real description.
- Version as `upstream-revision` in `debian/changelog`, and bump with `dch -i` for each upload.
- Use `debhelper-compat` in Build-Depends to set the compat level, and a minimal `debian/rules` (`dh $@`).
- List installed files in `debian/<pkg>.install`, not by custom `cp` in rules.
- Write maintainer scripts (`postinst`, `prerm`) idempotent, with `#DEBHELPER#` included.
- Build in a clean chroot or container (`sbuild`, `pbuilder`, or a Debian image) to catch missing Build-Depends.
- Check licensing in `debian/copyright`.

## Avoid
- Building in a dirty environment: it passes locally with undeclared dependencies and fails elsewhere. Build clean.
- Hand-written `Depends` for shared libraries: use `${shlibs:Depends}` and let dpkg-shlibdeps compute them.
- Files installed outside `/usr` (or the right FHS location), or into `/usr/local`: lintian flags it. Fix the install paths.
- Maintainer scripts that fail on re-run or on removal: make them idempotent and test purge and upgrade.
- Forgetting to bump the changelog: the same version with different content breaks upgrade logic. Add a new entry.
- Unexecutable `debian/rules`: `chmod +x debian/rules`.

## Review
- [ ] The package builds in a clean environment and lintian reports no errors.
- [ ] `dpkg-deb -c` lists exactly the intended files, with correct modes.
- [ ] Install, upgrade and purge were tried in a clean container.
- [ ] Changelog, control and copyright are up to date.
