---
name: mime-guess
title: mime_guess
area: rust
tags: [rust, mime, content-type, file-extension, uploads]
detect: [dep:mime-guess, dep:mime_guess]
related: [cargo, axum, serde, reqwest, actix-web]
---
mime_guess (crate `mime_guess`) maps a file extension to a MIME type from a static table; it never reads the file.

## Verify
- `cargo test`: the tests that depend on a guessed type pass with the pinned crate version.
- `cargo tree -d | grep mime_guess`: no second copy of the crate is in the graph.
- `cargo tree -i mime_guess`: shows which crates pull it in, so a change in one of them is visible.
- `cargo clippy --all-targets -- -D warnings`: the calling code has no lint findings.

## Test first
Assert the type category and the fallback for an unknown extension.
```rust
use mime::IMAGE;

#[test]
fn png_is_an_image_and_unknown_falls_back() {
    let png = mime_guess::from_path("photos/Cat.PNG").first_or_octet_stream();
    assert_eq!(png.type_(), IMAGE);

    let unknown = mime_guess::from_path("blob.zzz").first_or_octet_stream();
    assert_eq!(unknown, mime::APPLICATION_OCTET_STREAM);
}
```

## Do
- Call `from_path(name)` with the full path or file name; only the extension is read.
- Pass `from_ext` the extension without the dot: `from_ext("png")`, not `from_ext(".png")`.
- Use `first_or_octet_stream()` for a download or upload default, and `first_or_text_plain()` where text is the sensible fallback.
- Use `iter()` when an extension has several candidate types and you need all of them.
- Compare `type_()` against `mime::IMAGE`, `mime::TEXT` and similar for category checks.
- Lowercase nothing yourself: the lookup is case-insensitive.

## Avoid
- `first().unwrap()`: an unknown or missing extension gives `None`, and the unwrap panics on user input. Use a `first_or_*` fallback.
- Trusting the guessed type for security: the docs say the file may not match its extension. Sniff the content for uploads (see the upload-security card).
- Expecting a type for an extensionless name such as `Makefile`: the guess is empty.
- Asserting the full MIME string in tests: the crate's docs say the values change in patch releases. Pin the version in `Cargo.lock` and assert the category.
- Calling the deprecated free functions `get_mime_type` and friends (deprecated since 2.0.0): use `from_ext(...)`.
- Reading the file to decide the type when the extension is enough: the crate does no disk access; the extra read is wasted work.

## Review
- [ ] Unknown and extensionless names have a defined fallback, with a test.
- [ ] Security decisions use content sniffing, not the guessed type.
- [ ] Tests assert the type category, not the exact string.
- [ ] `cargo tree -d` shows one mime_guess version.
- [ ] No deprecated free function is called.
