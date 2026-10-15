---
name: kotlinx-serialization
title: kotlinx.serialization
area: jvm
tags: [kotlin, serialization, json, multiplatform, ktor, plugin]
detect: [dep:kotlinx-serialization-json, dep:kotlinx-serialization-core, dep:kotlinx-serialization-protobuf, dep:kotlinx-serialization-cbor]
related: [ktor, kotlin-coroutines, kotlin-multiplatform, gradle, jackson]
---
kotlinx.serialization: compiler-plugin-based, reflection-free JSON and binary formats for Kotlin, including multiplatform.

## Verify
- `./gradlew test`: round-trip tests pass.
- `./gradlew dependencies --configuration compileClasspath | grep serialization`: the runtime library is on the classpath alongside the compiler plugin.
- `grep -rn "kotlin(\"plugin.serialization\")\|plugin.serialization" build.gradle.kts`: the plugin is applied in every module with `@Serializable` types.
- `./gradlew build`: no "Serializer has not been found" errors surface at compile time.

## Test first
Test the wire format, not only the object round trip.
```kotlin
class ItemJsonTest {
  private val json = Json { ignoreUnknownKeys = true }

  @Test fun decodesSnakeCaseAndDefaults() {
    val item = json.decodeFromString<Item>("""{"item_name":"a"}""")
    assertEquals(Item(name = "a", qty = 1), item)
  }
}
// @Serializable data class Item(@SerialName("item_name") val name: String, val qty: Int = 1)
```

## Do
- Apply the `org.jetbrains.kotlin.plugin.serialization` Gradle plugin (same Kotlin version) and add `kotlinx-serialization-json`.
- Annotate types with `@Serializable`; rename fields with `@SerialName`.
- Configure one shared `Json { ... }` instance (`ignoreUnknownKeys`, `explicitNulls`, `encodeDefaults`) and reuse it.
- Model polymorphism with a `sealed interface` plus `@Serializable` subtypes; set `classDiscriminator` when the default `type` clashes.
- Provide defaults for optional fields so older payloads still decode.
- Write custom `KSerializer` objects for types like `Instant` or `UUID` (or use the library's built-in ones for `kotlinx-datetime`).
- Use `decodeFromString<T>()` and `encodeToString()` reified helpers.

## Avoid
- Forgetting the compiler plugin: `@Serializable` compiles but `serializer()` is missing; apply the plugin.
- Classes with properties lacking a backing field or non-serializable property types: the plugin reports an error. Mark with `@Transient` and a default, or add a serializer.
- Strict decoding by default on APIs you do not control: unknown keys throw. Set `ignoreUnknownKeys = true` deliberately.
- `Any` or `Map<String, Any>` fields: not serializable. Use `JsonElement` or a sealed type.
- Gson or Jackson annotations (`@SerializedName`, `@JsonProperty`) on these types: ignored. Use `@SerialName`.
- Creating a new `Json {}` per call: wasteful. Use a shared instance.
- Version drift between the Kotlin compiler and the plugin: pin both through the same Kotlin version.

## Review
- [ ] Plugin applied in each module that declares `@Serializable` types.
- [ ] Tests decode real sample payloads, including missing and unknown fields.
- [ ] Polymorphic types are sealed and registered, with a stable discriminator.
- [ ] One shared `Json` configuration; no per-call instances.
- [ ] Custom serializers are tested for round trip.
