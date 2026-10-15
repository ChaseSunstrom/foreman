---
name: graalvm-native-image
title: GraalVM Native Image
area: jvm
tags: [java, graalvm, native, aot, reflection, startup, containers]
detect: [dep:native-maven-plugin, dep:org.graalvm.buildtools.native, file:reflect-config.json, file:native-image.properties, file:reachability-metadata.json]
related: [spring-boot, quarkus, micronaut, jib, gradle, maven]
---
GraalVM native images: ahead-of-time compiled JVM apps where reflection, resources, proxies and serialization must be known at build time.

## Verify
- `./gradlew nativeCompile`: builds the native executable (Gradle plugin `org.graalvm.buildtools.native`).
- `./gradlew nativeTest`: runs the test suite as a native image.
- `mvn -Pnative native:compile`: Maven build with the native profile (Spring Boot parent defines it).
- `./build/native/nativeCompile/APP`: the binary starts and serves; compare with JVM behavior.

## Test first
The failing check is the native run or `nativeTest` hitting missing metadata at runtime.
```
$ ./gradlew nativeTest
com.fasterxml.jackson.databind.exc.InvalidDefinitionException:
  No serializer found for class ...   <- reflection metadata missing
```
Reproduce with a test that exercises the reflective path (JSON, resource load, proxy) and fails natively first; then add hints or metadata until green.

## Do
- Test natively, not only on the JVM: `nativeTest` plus a smoke run of the built binary in CI.
- Provide metadata in `META-INF/native-image/<group>/<artifact>/` (`reachability-metadata.json` in recent GraalVM; `reflect-config.json`, `resource-config.json`, `proxy-config.json`, `serialization-config.json` in older ones).
- Spring: register hints with `RuntimeHintsRegistrar` plus `@ImportRuntimeHints`, or `@RegisterReflectionForBinding(Type.class)`.
- Collect missing metadata with the tracing agent: run the JVM app with `-agentlib:native-image-agent=config-output-dir=DIR` while exercising all paths, then review the output.
- Use the GraalVM Reachability Metadata Repository support in the build plugin for third-party libraries.
- Initialize at build time only what is safe: `--initialize-at-build-time=pkg`; default to run time for anything holding state, threads or randomness.
- Pass build flags via `buildArgs.add("-O...")`, and `--no-fallback` so a failed AOT does not silently produce a JVM-needing fallback image.
- Package with a slim or distroless base (or Spring `bootBuildImage` with the native builder).

## Avoid
- Assuming JVM-tested means native-safe: reflection, dynamic proxies and `Class.forName` fail only at runtime. Run `nativeTest`.
- Classes initialized at build time that open sockets, read env or seed `SecureRandom`: baked-in state or build failure. Move to run time.
- Blindly committing agent output: it overgeneralizes and misses conditionals. Review and trim.
- Runtime classpath scanning and dynamic bytecode generation (some proxies, CGLIB-style) with no hints: unsupported. Use build-time frameworks or hints.
- Resources not declared in `resource-config.json`: `getResourceAsStream` returns null. Add include patterns.
- Treating a fallback image as success: slower and not native. Build with `--no-fallback`.
- Long, memory-hungry builds on small CI runners: set enough RAM or build in a dedicated step.

## Review
- [ ] `nativeTest` and a binary smoke run pass in CI.
- [ ] All reflection and resources are covered by committed, reviewed metadata or hints.
- [ ] `--no-fallback` is set; build-time initialization is minimal and justified.
- [ ] Startup and memory are measured against the JVM build.
- [ ] Third-party library compatibility is checked against reachability metadata.
