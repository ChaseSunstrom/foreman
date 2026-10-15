---
name: jib
title: Jib
area: jvm
tags: [java, containers, docker, oci, gradle, maven, layers]
detect: [dep:jib-core, dep:jib-maven-plugin, dep:jib-gradle-plugin]
related: [spring-boot, gradle, maven, graalvm-native-image, testcontainers]
---
Jib builds layered OCI images for JVM apps from Maven or Gradle with no Dockerfile or daemon: reproducible, cache-friendly, with explicit base image and entrypoint.

## Verify
- `./gradlew jibDockerBuild`: builds into the local Docker daemon.
- `./gradlew jibBuildTar`: builds an image tarball with no registry or daemon needed.
- `mvn compile jib:dockerBuild`: the Maven equivalent to the daemon build.
- `docker run --rm IMAGE`: the container starts and the entrypoint is correct.

## Test first
The failing check is the container run: it must start and answer.
```
$ ./gradlew jibDockerBuild --image=app:test
$ docker run -d --rm -p 8080:8080 --name t app:test
$ curl -fsS localhost:8080/actuator/health
curl: (7) Failed to connect   <- fails first: wrong mainClass or port
```
Fix `jib { container { mainClass; ports } }`, rebuild and rerun until the curl succeeds. For CI add a Testcontainers `GenericContainer` test against the built image.

## Do
- Gradle: `plugins { id("com.google.cloud.tools.jib") }`; Maven: `jib-maven-plugin` in `build`.
- Set the base image explicitly and pin by digest: `jib { from { image = "eclipse-temurin:21-jre@sha256:..." } }`.
- Set the target: `to { image = "registry/app:${version}"; tags = setOf("latest") }`.
- Configure `container { jvmFlags = listOf("-XX:MaxRAMPercentage=75"); ports = listOf("8080"); user = "10001"; mainClass = "..." }`.
- Use a non-root user and a JRE base, not a JDK.
- Credentials from environment or credential helpers (`from.auth`, `to.auth` reading `System.getenv`), never literals.
- Make images reproducible: `container.creationTime = "USE_CURRENT_TIMESTAMP"` only when needed; default epoch keeps layers stable.
- Use `extraDirectories` for config or static files and `jib.containerizingMode = "packaged"` only when a fat jar is required.
- Spring Boot gets layered dependency, snapshot and resource layers automatically.

## Avoid
- Pushing with credentials in `build.gradle`: leaks into VCS. Use env vars or credential helpers.
- Mutable base tags (`:latest`) for production: builds drift. Pin a digest.
- Omitting `mainClass` on multi-main projects: jib picks wrongly or fails. Set it.
- `allowInsecureRegistries = true` outside local dev: disables TLS checks.
- Adding a Dockerfile alongside Jib and expecting it to be used: it is ignored. Choose one.
- Running as root: remove with `container.user`.
- JVM heap flags as fixed `-Xmx` in containers: ignores limits. Use `-XX:MaxRAMPercentage`.

## Review
- [ ] Base image is pinned and a JRE.
- [ ] Image runs as non-root with explicit port, main class and JVM flags.
- [ ] Registry credentials come from environment or helpers.
- [ ] CI builds with `jib` (or tar) and runs a smoke test on the image.
- [ ] Image tags include an immutable version, not only `latest`.
