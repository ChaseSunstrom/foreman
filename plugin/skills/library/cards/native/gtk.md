---
name: gtk
title: GTK 4
area: native
tags: [gtk, gtk4, gobject, c, gui, glib, blueprint]
detect: [dep:PyGObject, dep:gtk4, dep:gtk4-rs, dep:gtk-rs, file:*.ui, file:*.blp, file:*.gresource.xml]
related: [meson, sanitizers, valgrind, qt]
---
GTK 4 apps (C, or via PyGObject and Rust bindings): GObject ownership, main-loop discipline, UI files, Meson builds.

## Verify
- `pkg-config --modversion gtk4`: the GTK 4 development package is present and its version.
- `meson setup build && meson compile -C build && meson test -C build --print-errorlogs`: build and tests.
- `gtk4-builder-tool validate window.ui`: the UI file is valid (when the tool is installed).
- `G_DEBUG=fatal-warnings GTK_A11Y=none xvfb-run ./build/app`: GLib/GTK warnings abort a headless smoke run.

## Test first
Test model and logic code without any widget. For widget behaviour, create it headlessly (`xvfb-run`, `gtk_init`) and use the GLib test API.
```c
#include <glib.h>
#include "cart.h"

static void test_empty_total(void) {
    Cart *c = cart_new();
    g_assert_cmpint(cart_total(c), ==, 0);
    g_object_unref(c);
}
int main(int argc, char **argv) {
    g_test_init(&argc, &argv, NULL);
    g_test_add_func("/cart/empty_total", test_empty_total);
    return g_test_run();
}
```
Register with `test('cart', executable(...))` in meson.build.

## Do
- Use GTK 4 idioms: `GtkApplication`, `GtkApplicationWindow`, `GtkBuilder`/composite templates (`gtk_widget_class_set_template_from_resource`), `GtkListView` with `GListModel` for lists.
- Define UI in `.ui` (or Blueprint `.blp`) files compiled into a GResource (`gnome.compile_resources` in Meson).
- Use `GSettings` for preferences and `GAction`/`GMenu` for commands.
- Follow GObject ownership: `g_object_ref/unref`, floating refs for widgets, `g_autoptr(Type)` and `g_autofree` for cleanup.
- Use async APIs (`g_file_load_contents_async`, `GTask`) with callbacks on the main context; never block the main loop.
- Run long work in `GTask` threads or a worker, return results with `g_idle_add`/`g_main_context_invoke`.
- Check `GError **` out-params and `g_clear_error`.

## Avoid
- GTK 3 APIs in GTK 4 code (`gtk_container_add`, `gtk_main`, `gtk_widget_show_all`, `GtkMenu`, `GtkStyleContext` drawing): use `gtk_window_set_child`, `GtkApplication`/main loop via `g_application_run`, `GtkPopoverMenu`, CSS.
- Touching widgets from another thread: undefined behaviour. Hop to the main thread.
- Leaking by not unreffing `g_object_new` results or over-unreffing floating widgets: use `g_autoptr` and check with `G_DEBUG=gc-friendly` plus Valgrind or ASan.
- `g_timeout_add` callbacks that return `TRUE` forever after the owner is destroyed: remove the source (`g_source_remove`) in `dispose`.
- Ignoring `dispose` vs `finalize`: release references in `dispose` (may run more than once, set pointers NULL), free memory in `finalize`.
- Hard-coding pixel sizes and colours: use CSS, `GtkSettings` and theme-aware symbolic icons.
- Parsing `.ui` strings at runtime in tight loops: load templates once.

## Review
- [ ] No GTK 3 container or `gtk_main` APIs remain.
- [ ] Every GObject has one clear owner; autoptr or dispose handles cleanup.
- [ ] No blocking I/O on the main thread; results return via the main context.
- [ ] Errors from `GError` are handled.
- [ ] Headless smoke run with fatal warnings passes.
