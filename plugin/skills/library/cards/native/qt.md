---
name: qt
title: Qt
area: native
tags: [qt, qt6, cpp, gui, qml, signals-slots, qtest]
detect: [dep:Qt6, dep:Qt5, dep:qt, dep:pyside6, dep:PyQt6, file:*.ui, file:*.qml, file:*.pro]
related: [cmake, googletest, sanitizers, gtk]
---
Qt 6 C++ (and QML) apps: CMake with AUTOMOC, signals and slots, QtTest, strict thread affinity.

## Verify
- `cmake -S . -B build -DCMAKE_PREFIX_PATH=/path/to/Qt/6.x/gcc_64 && cmake --build build`: configures against the Qt kit and builds.
- `QT_QPA_PLATFORM=offscreen ctest --test-dir build --output-on-failure`: tests run headless with no display.
- `qmllint path/to/Main.qml`: QML has no lint errors (when Qt's tools are on PATH).
- `QT_FATAL_WARNINGS=1 QT_QPA_PLATFORM=offscreen ./build/app`: Qt runtime warnings (bad connections, null properties) abort in a smoke run.

## Test first
QtTest in `tests/`; each test class has private slots. Add it with `qt_add_executable`/`add_test`.
```cpp
#include <QtTest>
#include "cart.h"

class CartTest : public QObject {
    Q_OBJECT
private slots:
    void emptyCartTotalIsZero() { QCOMPARE(Cart().total(), 0); }
};
QTEST_MAIN(CartTest)
#include "cart_test.moc"
```
```cmake
find_package(Qt6 REQUIRED COMPONENTS Test)
add_executable(cart_test cart_test.cpp)
target_link_libraries(cart_test PRIVATE cartlib Qt6::Test)
set_target_properties(cart_test PROPERTIES AUTOMOC ON)
add_test(NAME cart_test COMMAND cart_test)
```
Use `QSignalSpy` to assert a signal fires.

## Do
- Use `find_package(Qt6 REQUIRED COMPONENTS Widgets)`, `qt_standard_project_setup()` and link `Qt6::Widgets` style targets; AUTOMOC/AUTOUIC/AUTORCC are enabled by it.
- Give `QObject` subclasses `Q_OBJECT`, and parent objects (`new Foo(parent)`) so Qt frees them.
- Use the pointer-to-member `connect(sender, &Sender::sig, receiver, &Receiver::slot)` form, and a context object or lambda with it.
- Keep the GUI thread free: run work in `QThread` with a worker object, `QtConcurrent`, or async APIs; deliver results by queued signals.
- Use QML for declarative UI with C++ types exposed via `QML_ELEMENT` and `qt_add_qml_module`.
- Use `tr()` for user-visible strings and `QStringLiteral`/`u""_s` for literals.
- Use `Qt::QueuedConnection` or `QMetaObject::invokeMethod` to cross threads.

## Avoid
- String-based `SIGNAL()`/`SLOT()` macros: no compile-time checking. Use the function-pointer form.
- Touching widgets or QML objects from a worker thread: undefined behaviour. Emit a signal to the GUI thread.
- Subclassing `QThread` and putting logic in `run()` while also calling its slots from another thread: slots run in the creating thread. Use a worker `QObject` moved with `moveToThread`.
- `delete` on an object with pending events or a connected sender: use `deleteLater()`.
- Qt5-era APIs in Qt6 (`QRegExp`, `QStringRef`, `QVariant::type()`): use `QRegularExpression`, `QStringView`, `typeId()`.
- Forgetting `#include "x.moc"` for Q_OBJECT classes declared in a .cpp: link errors on vtable.
- Blocking the event loop with `sleep` or nested `exec()`: the UI freezes. Use timers and signals.

## Review
- [ ] Connections use the typed form and correct connection type across threads.
- [ ] No GUI object is accessed off the GUI thread.
- [ ] Object ownership is by parent or smart pointer, never both.
- [ ] Tests run offscreen in CI; `QT_FATAL_WARNINGS` smoke run is clean.
- [ ] User-visible strings pass through `tr()`.
