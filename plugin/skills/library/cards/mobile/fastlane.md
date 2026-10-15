---
name: fastlane
title: fastlane
area: mobile
tags: [fastlane, ios, android, release, ci, code-signing, ruby]
detect: [file:Fastfile, file:Appfile, file:Matchfile, file:Gemfile, file:fastlane/Fastfile]
related: [xcodebuild, flutter, react-native, expo]
---
fastlane: scripted mobile builds, signing with match, TestFlight and Play uploads, run through lanes in a Fastfile.

## Verify
- `bundle exec fastlane lanes`: the Fastfile parses and lists lanes.
- `bundle exec fastlane ios test`: runs a test lane (name from your Fastfile).
- `bundle exec fastlane run validate_play_store_json_key json_key:key.json`: Play credentials are valid (when using supply).
- `bundle exec fastlane env`: prints the environment, for bug reports and CI debugging.

## Test first
For a lane, the failing check is a dry run that proves the lane aborts without its inputs. Make it fail first.
```ruby
# fastlane/Fastfile
lane :beta do
  UI.user_error!("Set CI=1 to ship") unless ENV["CI"]
  build_app(scheme: "App")
  upload_to_testflight(skip_waiting_for_build_processing: true)
end
```
Run `bundle exec fastlane beta` locally with no `CI` and confirm the guard stops it before a build.

## Do
- Pin fastlane in the Gemfile and always run `bundle exec fastlane ...`.
- Use `match` (`match(type: "appstore", readonly: is_ci)`) to share certificates and profiles through an encrypted repo or bucket.
- Authenticate to App Store Connect with an API key (`app_store_connect_api_key`) instead of an Apple ID password and 2FA.
- Put credentials in CI secrets and environment variables; reference them with `ENV["..."]`.
- Set `setup_ci` at the start of CI lanes so a temporary keychain is used.
- Increment build numbers in a lane (`increment_build_number` or derive from CI run number).
- Keep lanes small and composed; wrap failures with `error do |lane, exception|` for notification.

## Avoid
- Committing API keys, `.p8` files, Play JSON keys or the match password: use CI secrets and a secure file store.
- `match` without `readonly: true` on CI: CI may create or revoke certificates. Make CI read-only.
- Apple ID and password with interactive 2FA in CI: hangs. Use an API key.
- Running bare `fastlane` without bundler: version drift between machines. Use `bundle exec`.
- `skip_waiting_for_build_processing` plus a later step needing the processed build: race. Wait, or end the lane there.
- Uploading a build with a duplicate version and build number: rejected. Increment first.
- `sh "..."` for steps that have a built-in action: lose error handling and options. Prefer the action.

## Review
- [ ] Gemfile pins fastlane and lanes run with bundler.
- [ ] Signing uses match read-only in CI; no certificates in the repo.
- [ ] Auth is an API key from secrets, not a password.
- [ ] Build and version numbers increment automatically.
- [ ] A lane failure notifies and exits non-zero.
