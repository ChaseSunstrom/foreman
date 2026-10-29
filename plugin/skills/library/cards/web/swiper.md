---
name: swiper
title: Swiper
area: web
tags: [swiper, slider, carousel, touch, react, vue]
detect: [dep:swiper, dep:swiper-element]
related: [react, accessibility, css-layout, web-performance]
---
Swiper: full-featured touch slider with modules for navigation, pagination, autoplay, thumbs and effects.

## Verify
- `npx tsc --noEmit`: module and options types.
- `npx eslint .`: lint.
- `npx vitest run`: wiring tests.
- `npx playwright test --grep slider`: swipe, keyboard and pagination in a real browser.

## Test first
Assert the configuration your app depends on, and the accessible behavior in a browser.
```tsx
import { render } from "@testing-library/react";
import { Hero } from "./Hero";
import { heroSwiperOptions } from "./heroSwiperOptions";

test("hero slider config is accessible and bounded", () => {
  expect(heroSwiperOptions.a11y?.enabled).not.toBe(false);
  expect(heroSwiperOptions.autoplay).toMatchObject({ pauseOnMouseEnter: true, disableOnInteraction: true });
  expect(render(<Hero />).container.querySelectorAll(".swiper-slide").length).toBeGreaterThan(0);
});
```

## Do
- Import modules explicitly: `import { Navigation, Pagination, A11y } from "swiper/modules"` and pass `modules={[...]}`.
- Import only the CSS you use: `swiper/css`, `swiper/css/navigation`, `swiper/css/pagination`.
- In React use `<Swiper>` and `<SwiperSlide>`; in Vue use `swiper/vue`; for web components use `swiper/element` and call `register()` once.
- Enable the `A11y` module and set labels (`prevSlideMessage`, `nextSlideMessage`).
- Set `breakpoints` for slides per view, `spaceBetween`, and `watchOverflow: true`.
- Lazy-load images with native `loading="lazy"` and explicit sizes; Swiper's own lazy module was removed in v9.
- For SSR, give the container a fixed height or aspect ratio to avoid layout shift before hydration.
- Keep `autoplay` off by default or stop it on interaction and reduced motion, and destroy via the component unmount.

## Avoid
- `import Swiper from "swiper/bundle"`: ships every module.
- Importing v8 paths or `swiper/swiper-bundle.css` on newer majors; check the installed version.
- Passing new options objects on every render.
- `loop` with too few slides: duplicates and warnings. Need at least double the visible count.
- Autoplay without a pause path.

## Review
- [ ] Only needed modules and CSS are imported.
- [ ] A11y module and labels are on.
- [ ] Autoplay can be stopped and respects reduced motion.
- [ ] Loop has enough slides.
- [ ] Container size is fixed before hydration.
