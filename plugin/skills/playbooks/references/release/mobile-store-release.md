<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Ship a mobile app to TestFlight or Play

Use when you upload a mobile build for testers or a store: iOS archive and upload, an Android bundle, fastlane lanes, Expo EAS.

Built on the cards `fm lib show app-store-release`, `fm lib show play-store-release`, `fm lib show fastlane` and `fm lib show expo`.

1. **Gate the commit:** tests, analyzer and a clean tree, on the commit you build.
2. **Version and build number up**, in every place the platform reads them; stores reject a repeated build number.
3. **Build the release artifact the store takes:**
   ```bash
   xcodebuild archive -scheme App -configuration Release -archivePath build/App.xcarchive
   ./gradlew :app:bundleRelease :app:lintRelease
   npx expo-doctor
   ```
4. **Validate before upload:** `xcrun notarytool` or Transporter for iOS; for Play `bundle exec fastlane run validate_play_store_json_key json_key:key.json`. Never commit `key.json`; read it from the environment.
5. **Internal track first** (TestFlight internal, Play internal testing); install on a device and smoke the launch, login and one purchase or push path.
6. **Review metadata:** privacy answers, permissions rationale, and notes for the reviewer match the build.
7. **Upload is outward:** it needs the owner's grant; promote to production only after the internal soak.

Pass: validation exits 0, the internal build installs and launches, and the changelog and version match the store listing.
