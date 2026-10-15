---
name: jenkins
title: Jenkins
area: infra
tags: [jenkins, jenkinsfile, pipeline, groovy, ci, agents]
detect: [file:Jenkinsfile, file:Jenkinsfile.*, file:*.jenkinsfile, file:vars/*.groovy]
related: [github-actions, gitlab-ci, docker, kubernetes]
---
Jenkins: declarative `Jenkinsfile` pipelines with containerized agents, credentials binding, shared libraries and timeouts.

## Verify
- `curl -s -X POST -F "jenkinsfile=<Jenkinsfile" $JENKINS_URL/pipeline-model-converter/validate`: the server validates declarative syntax (needs auth).
- `jenkins-cli declarative-linter < Jenkinsfile`: the same linter through the CLI, when configured.
- `groovy -e "new GroovyShell().parse(new File('Jenkinsfile'))"`: only checks Groovy syntax, not Jenkins semantics.
- `grep -n 'withCredentials\|credentials(' Jenkinsfile`: lists secret use to review for leaks.

## Test first
Use Jenkins Pipeline Unit (`com.lesfurets:jenkins-pipeline-unit`) for shared-library logic, and a branch build for the Jenkinsfile.
```groovy
class BuildTest extends BasePipelineTest {
  @Test void failsWithoutVersion() {
    def build = loadScript('vars/buildApp.groovy')
    assertThrows(Exception) { build.call(version: null) }
  }
}
```
Red first: fails until the step validates its argument.

## Do
- Use declarative `pipeline { agent ...; stages { ... } }` and `post { always { ... } failure { ... } }`.
- Run build steps in containers or Kubernetes pod agents (`agent { docker { image '...' } }`), not on the controller.
- Wrap in `options { timeout(time: 30, unit: 'MINUTES'); timestamps(); disableConcurrentBuilds(); buildDiscarder(logRotator(numToKeepStr: '20')) }`.
- Bind secrets with `withCredentials([string(credentialsId: 'x', variable: 'TOKEN')])`, scoped to one step.
- Run independent work with `parallel`, and `stash`/`unstash` to pass files between agents.
- Keep logic in shared libraries (`vars/*.groovy`, `@Library('lib@v1') _`) and pin the library version.
- Use `when { branch 'main' }` and `input` approval for deploy stages.
- Archive and publish with `archiveArtifacts` and `junit` for test results.

## Avoid
- Interpolating credentials in double-quoted `sh "... ${TOKEN}"`: leaks via Groovy interpolation into logs and process lists. Use single quotes `sh '... "$TOKEN"'`.
- Running builds on the built-in node: a compromised job controls the controller. Set its executors to 0.
- Scripted pipelines for simple flows: harder to read and lint. Use declarative, with `script {}` only where needed.
- Heavy Groovy CPS logic in the Jenkinsfile: slow and serialization errors (`NotSerializableException`). Move it to `sh` or `@NonCPS` methods.
- Unpinned `@Library('lib')`: the default branch changes under every job. Use a tag.
- Plugins updated blindly: breakage and CVEs. Pin and update on a schedule.
- `deleteDir()` skipped on shared agents: stale workspaces cause flaky builds. Clean in `post`.
- Freestyle jobs configured in the UI: not reviewable. Keep config as code.

## Review
- [ ] Declarative lint passes and timeouts and discarders are set.
- [ ] Secrets are bound narrowly and never interpolated in double quotes.
- [ ] Builds run in containers off the controller, and library versions are pinned.
- [ ] Deploy stages are gated by branch conditions and approvals.
