---
name: objective-c
title: Objective-C
area: lang
tags: [objective-c, arc, cocoa, xctest, xcodebuild, clang-format]
detect: [ext:.m, ext:.mm, file:*.xcodeproj, file:Podfile, file:.clang-format]
related: [bash]
---
Objective-C on Apple platforms: ARC, blocks, nullability annotations, XCTest, `xcodebuild`.

## Verify
- `xcodebuild -scheme MyApp -destination 'platform=macOS' build`: compiles the scheme (iOS: `-destination 'platform=iOS Simulator,name=<device>'`).
- `xcodebuild test -scheme MyApp -destination 'platform=macOS'`: runs XCTest bundles.
- `clang-format --dry-run -Werror path/File.m`: formatting matches `.clang-format`.
- `xcodebuild analyze -scheme MyApp`: the Clang static analyzer finds leaks, nil derefs and dead stores.

## Test first
XCTest classes live in the test target, one `*Tests.m` per class.
```objc
#import <XCTest/XCTest.h>
#import "AmountParser.h"

@interface AmountParserTests : XCTestCase
@end

@implementation AmountParserTests
- (void)testBlankInputReturnsError {
    NSError *error = nil;
    NSNumber *n = [AmountParser parse:@"" error:&error];
    XCTAssertNil(n);
    XCTAssertEqual(error.code, AmountParserErrorEmpty);
}
@end
```

## Do
- Use ARC everywhere; declare properties with `nonatomic`, `copy` for `NSString`/blocks/collection interfaces, and `weak` for delegates.
- Wrap headers in `NS_ASSUME_NONNULL_BEGIN/END` and mark exceptions `nullable`, so Swift and the analyzer see intent.
- Report recoverable failure with `NSError **` out-parameters and a `BOOL`/object return, never exceptions.
- Capture `weak` self in long-lived blocks, then strongify inside: `__weak typeof(self) weakSelf = self;`.
- Use lightweight generics (`NSArray<NSString *> *`) and modern literals (`@[]`, `@{}`, `@""`).
- Update UI only on the main queue (`dispatch_async(dispatch_get_main_queue(), ...)`), and guard shared state with serial queues.
- Prefer `NS_ENUM`/`NS_OPTIONS` and `static` constants over `#define` values.

## Avoid
- Retain cycles from blocks that capture `self` and are stored on `self`: leaks. Use weak-strong capture.
- `strong`/`assign` for `NSString` or `NSMutableArray` properties: a caller's mutable object changes under you. Use `copy`.
- Ignoring `NSError` or passing `NULL` and then trusting the return: check the return value, not the error variable.
- `@try/@catch` for flow control and `NSAssert` for input validation: exceptions are not recoverable in Cocoa. Validate and return an error.
- Messaging `nil` and assuming it throws: it returns 0/nil silently and hides bugs. Guard where nil is invalid.
- `performSelector:` with dynamic selectors: ARC leak warnings and no type checks. Use a block or direct call.
- Deprecated APIs (`UIAlertView`, `NSURLConnection`, `UIWebView`): removed or unsupported. Use `UIAlertController`, `NSURLSession`, `WKWebView`.

## Review
- [ ] Analyzer run is clean and nullability is declared in changed headers.
- [ ] Block captures are checked for cycles, and no UI work happens off the main thread.
- [ ] Property attributes are correct (`copy` for value-like types, `weak` for delegates).
- [ ] Errors flow through `NSError **`, and callers check return values.
- [ ] Tests cover the error branch and the nil argument.
