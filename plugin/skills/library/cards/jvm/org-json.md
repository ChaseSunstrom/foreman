---
name: org-json
title: org.json (JSON-java)
area: jvm
tags: [java, json, parsing, jsonobject, android, license]
detect: [dep:org.json:json]
related: [jackson, android, kotlin, gradle, junit4]
---
`org.json:json` is the JSON-java library: a tree of `JSONObject` and `JSONArray` that throws `JSONException` on bad input.

## Verify
- `./gradlew dependencies --configuration runtimeClasspath | grep org.json`: one version resolves.
- `./mvnw -q dependency:tree | grep org.json`: no second JSON library is pulled in for the same code.
- `./gradlew test`: the parsing tests pass, including the malformed-input case.
- `grep -rn "org.json" --include=*.java --include=*.kt .`: imports are only where the code parses or builds JSON, not spread through the domain.

## Test first
Assert the exception on bad input and the default on a missing key.
```java
import static org.junit.Assert.*;
import org.json.JSONException;
import org.json.JSONObject;
import org.junit.Test;

public class ConfigTest {
  @Test public void missingPortUsesDefault() {
    JSONObject o = new JSONObject("{\"host\":\"a\"}");
    assertEquals(8080, o.optInt("port", 8080));
  }

  @Test public void malformedInputThrows() {
    try {
      new JSONObject("{not json");
      fail("expected JSONException");
    } catch (JSONException expected) {
    }
  }
}
```

## Do
- Read with the `opt*` methods and a default when a field is optional; use `get*` only for required fields and catch `JSONException` at the boundary.
- Check `isNull(key)` or compare with `JSONObject.NULL`: a JSON null is not Java `null`.
- Use `has(key)` to tell a missing key from a present one.
- Convert to your own types at the edge, so the rest of the code never sees `JSONObject`.
- Parse only a bounded input size: a huge document is held in memory whole.

## Avoid
- `getString` or `getInt` on untrusted input without a catch: one bad field throws out of the request.
- `optInt(key)` with no default for a required field: a missing key quietly becomes `0`.
- `put(key, null)`: it removes the key. Use `JSONObject.NULL` to write an explicit null.
- Treating `org.json` on Android as this library: Android ships its own `org.json` in the framework. On the JVM unit-test classpath the framework copy throws at runtime. Add `org.json:json` as a `testImplementation` for the tests.
- Parsing numbers and expecting a type: JSON numbers arrive as the type the parser picks. Read the type you need explicitly.
- Shipping it without reading its license: JSON-java's JSON License has a clause that the software is "for Good, not Evil". Check that clause with the team before adding it.

## Review
- [ ] Optional fields use `opt*` with a default; required fields throw and are caught at the boundary.
- [ ] Malformed input is tested and returns an error, not a crash.
- [ ] Null handling is explicit (`isNull` or `JSONObject.NULL`).
- [ ] Android unit tests get this library on the test classpath.
- [ ] The license clause was reviewed.
