# Frontend Rules Full Content (Vue 3 / Vite / Pinia)

این فایل تجمیع کامل محتوای همه فایل‌های `.mdc` در پوشه `frontend/` است (بدون خلاصه‌سازی).

---


## `ui-ux/accessibility.mdc`

````mdc
---
description: WCAG 2.1 AA accessibility guidelines, semantic HTML, ARIA attributes, keyboard navigation, and screen reader support
globs:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
  - "frontend/src/**/*.css"
alwaysApply: false
---

# Accessibility (WCAG 2.1 AA)

## Semantic HTML

همیشه از درست‌ترین HTML element استفاده کن.

❌ **Bad:** `<div class="button">`
✅ **Good:** `<button>`

❌ **Bad:** `<div class="heading">`
✅ **Good:** `<h1>`

**ساختار معنایی:**
- `<header>`, `<nav>`, `<main>`, `<article>`, `<footer>`
- `<section>` برای بخش‌های منطقی
- لیست‌ها: `<ul>`, `<ol>`, `<dl>`
- از heading hierarchy صحیح استفاده کن (h1 → h2 → h3)
- از landmarks (header, nav, main, footer) استفاده کن

## ARIA Attributes

**قانون:** "No ARIA is better than bad ARIA"

فقط زمانی استفاده کن که semantic HTML کافی نیست:
- Custom widgets
- Dynamic content
- Complex interactions

**مثال‌های درست:**
- `aria-expanded` برای dropdown
- `aria-label` برای icon buttons
- `aria-describedby` برای help text
- `aria-live` برای dynamic updates
- از `aria-hidden` برای محتوای تزئینی استفاده کن

## Keyboard Navigation

**الزامات:**
- Tab: حرکت به جلو
- Shift+Tab: حرکت به عقب
- Enter/Space: فعال‌سازی
- Escape: بستن modal/dropdown
- Arrow keys: حرکت در لیست‌ها/منوها

**Focus Management:**
- همه interactive elements باید keyboard-accessible باشند
- Focus indicators واضح و قابل مشاهده
- Focus trap در modal ها
- Skip links برای navigation

## Color Contrast

**الزامات WCAG 2.1 AA:**
- Text: حداقل 4.5:1
- Large text (18pt+): حداقل 3:1
- UI Components: حداقل 3:1

❌ **Bad:** `#ddd` on `#aaa` (1.5:1)
✅ **Good:** `#ffffff` on `#3b82f6` (8.6:1)

## Screen Reader Support

- همه images دارای alt text مناسب
- Form inputs دارای label یا aria-label
- با screen reader تست شده
- Live regions برای dynamic content
- Descriptive link text (نه "click here")

## Reduced Motion

- از `prefers-reduced-motion` media query استفاده کن
- از animations غیرضروری پرهیز کن

## Accessibility Checklist

- [ ] Semantic HTML استفاده شده؟
- [ ] همه interactive elements با keyboard قابل دسترسی؟
- [ ] Focus indicators واضح هستند؟
- [ ] Color contrast حداقل 4.5:1 است؟
- [ ] Screen reader tested شده؟
- [ ] ARIA attributes مناسب استفاده شده؟
- [ ] Reduced motion respected شده؟
````

---

## `ui-ux/responsive-design.mdc`

````mdc
---
description: Mobile-first responsive design principles, breakpoints, touch targets, responsive images, and CSS units
globs:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.css"
alwaysApply: false
---

# Responsive Design

## Mobile-First Approach

طراحی از کوچک‌ترین صفحه (موبایل) شروع شود و به صفحات بزرگتر گسترش یابد.

**قانون:**
- Base styles بدون media query (موبایل)
- Media queries فقط برای min-width (scale up)
- از max-width استفاده نکن
- از progressive enhancement استفاده کن

## Breakpoints Strategy

```css
/* Base: 0-640px (mobile) - بدون media query */
.container {
  padding: 1rem;
  font-size: 16px;
}

/* sm: 640px+ (large mobile) */
@media (min-width: 640px) {
  .container {
    padding: 1.5rem;
  }
}

/* md: 768px+ (tablet) */
@media (min-width: 768px) {
  .container {
    padding: 2rem;
    font-size: 18px;
  }
}

/* lg: 1024px+ (desktop) */
@media (min-width: 1024px) {
  .container {
    padding: 3rem;
    max-width: 1200px;
    margin: 0 auto;
  }
}
```

**Breakpoints استاندارد:**
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

## Touch Targets

- حداقل 44×44px برای interactive elements
- Spacing کافی بین دکمه‌ها
- Thumb-friendly UI (دکمه‌های مهم در دسترس انگشت شست)

## Responsive Images

- استفاده از `srcset` با `sizes`
- WebP format با fallback
- `loading="lazy"` برای images off-screen
- `aspect-ratio` برای جلوگیری از layout shift

## CSS Units

- از viewport units استفاده کن (`vw`, `vh`, `rem`, `em`)
- از px ثابت پرهیز کن (جز برای borders)
- CSS Custom Properties برای responsive values
- از container queries استفاده کن (در صورت امکان)

## Layout

- از flexible layouts استفاده کن (Flexbox, Grid)
- از container queries استفاده کن (در صورت امکان)

## Testing

- در دستگاه‌های مختلف تست کن
- از browser dev tools استفاده کن
- از real devices استفاده کن
````

---

## `ui-ux/styling.mdc`

````mdc
---
description: Styling strategy, scoped CSS, theme management, design tokens, and BEM naming conventions
globs:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.css"
alwaysApply: false
---

# Styling Strategy

## رویکرد پیشنهادی

### Scoped CSS
- از `<style scoped>` در کامپوننت‌های Vue استفاده کن
- تداخل استایل‌ها را به حداقل می‌رساند

### Global CSS
- برای متغیرهای CSS (مثلاً در `style.css`)
- برای reset styles
- برای استایل‌های پایه

## مدیریت تم‌ها

### CSS Variables
- از CSS variables برای تم‌ها استفاده کن
- از `:root` برای variables سراسری استفاده کن
- از `[data-theme]` برای تم‌های مختلف استفاده کن

### Light/Dark Mode
- از `prefers-color-scheme` استفاده کن
- از toggle برای تغییر تم استفاده کن
- از CSS variables برای رنگ‌ها استفاده کن

## Design Tokens

### Colors
- از semantic color names استفاده کن
- از color palette ثابت استفاده کن

### Spacing
- از spacing scale استفاده کن
- از consistent spacing استفاده کن

### Typography
- از typography scale استفاده کن
- از font weights مناسب استفاده کن

## قوانین

- از BEM naming استفاده کن
- از utility classes محدود استفاده کن (مثلاً Tailwind در frontend)
- از CSS variables برای مقادیر استفاده کن
- از responsive units استفاده کن
````

---

## `ui-ux/interaction-patterns.mdc`

````mdc
---
description: Interaction patterns including form validation, optimistic UI updates, debouncing, throttling, animations, and modal patterns
globs:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
alwaysApply: false
---

# Interaction Patterns

## Form Validation

**Real-time validation:**
- Validation بعد از blur
- Show errors فقط برای fields touched
- Clear errors هنگام تایپ
- HTML5 validation به عنوان fallback

**الگو:**
1. User types
2. User blurs field
3. Show validation errors
4. Clear errors on next input
5. Submit validation (all fields)

## Optimistic UI Updates

برای UX بهتر:
1. UI را فوری update کن
2. در background request بفرست
3. در صورت خطا، rollback کن

**مثال:** Like button, Delete item

## Debouncing & Throttling

- **Debounce:** برای search input (بعد از توقف تایپ)
- **Throttle:** برای scroll events (حداکثر هر X میلی‌ثانیه)

## Animation Principles

- Subtle animations (150-300ms)
- Easing functions طبیعی
- Reduce motion برای accessibility
- `prefers-reduced-motion` را respect کن

## Modal & Dialog Patterns

- Focus trap در modal
- Escape key برای بستن
- Click outside برای بستن (optional)
- ARIA attributes (`aria-modal`, `aria-labelledby`)
- Focus return بعد از بستن
````

---

## `ui-ux/user-feedback.mdc`

````mdc
---
description: User feedback patterns including loading states, error handling, success feedback, skeleton screens, and toast notifications
globs:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
alwaysApply: false
---

# User Feedback

## Loading States

همیشه loading indicator برای async operations نمایش بده.

**الگوها:**
- Spinner برای عملیات کوتاه
- Skeleton screens برای محتوای در حال بارگذاری
- Progress bar برای عملیات طولانی

❌ **Bad:** کاربر منتظر می‌ماند بدون feedback
✅ **Good:** Loading indicator واضح

## Error Handling

- پیام‌های خطا واضح و مفید
- راه حل یا action بعدی پیشنهاد بده
- Dismissible error messages
- Error recovery options

## Success Feedback

- بازخورد موفقیت برای actions مهم
- Toast notifications برای actions سریع
- Visual confirmation (checkmark, animation)

## Skeleton Screens

بهتر از spinners برای محتوای در حال بارگذاری:
- ساختار صفحه را نشان می‌دهد
- Perceived performance بهتر
- کاهش layout shift

## Toast Notifications

برای بازخورد سریع:
- Auto-dismiss بعد از 3-5 ثانیه
- Manual dismiss option
- Multiple toasts stack
- Different types: info, success, warning, error
````

## `performance/bundle-size.mdc`

````mdc
---
description: Bundle size management, performance budget constraints, code splitting, tree shaking, and bundle analysis
globs:
  - "frontend/src/**/*.js"
  - "frontend/vite.config.*"
alwaysApply: false
---

# Bundle Size Management

## Performance Budget

**الزامات سخت:**
- Initial JS bundle: **<170KB** (gzipped)
- Initial CSS: **<50KB** (gzipped)
- Total page weight: **<1MB**

## Code Splitting

- Route-based code splitting (lazy load views)
- Component lazy loading برای components بزرگ
- Dynamic imports

**الگو:**
```javascript
const HeavyView = () => import('@/views/HeavyView.vue');
```

## Tree Shaking

- Import فقط آنچه نیاز است
- از `import *` پرهیز کن
- استفاده از named exports

## Bundle Analysis

- استفاده از bundle analyzer
- Track bundle size در CI/CD
- Alert هنگام exceed budget
````

---

## `performance/core-web-vitals.mdc`

````mdc
---
description: Core Web Vitals optimization guidelines for LCP, FID, and CLS performance metrics
globs:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
  - "frontend/src/**/*.css"
alwaysApply: false
---

# Core Web Vitals

## LCP (Largest Contentful Paint) <2.5s

**بهینه‌سازی:**
- Optimize largest image (hero image)
- Preload critical resources
- Reduce server response time

**تکنیک‌ها:**
- `fetchpriority="high"` برای hero image
- `<link rel="preload">` برای critical assets
- Image optimization (WebP, compression)

## FID (First Input Delay) <100ms

**بهینه‌سازی:**
- Reduce JavaScript execution time
- Code splitting
- Defer non-critical JavaScript
- Use `requestIdleCallback` برای non-critical tasks

**تکنیک‌ها:**
- Lazy load non-critical components
- Defer third-party scripts
- Reduce main thread blocking

## CLS (Cumulative Layout Shift) <0.1

**بهینه‌سازی:**
- Reserve space برای dynamic content
- Set dimensions برای images/videos
- Avoid inserting content above existing content
- Use `aspect-ratio` برای images

**تکنیک‌ها:**
- Skeleton screens با اندازه ثابت
- `aspect-ratio` CSS property
- Pre-calculate heights
- Font loading optimization
````

---

## `performance/optimization.mdc`

````mdc
---
description: General performance optimization techniques including code splitting, lazy loading, memoization, and virtualization
globs:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
alwaysApply: false
---

# Performance Optimization Rules

## تکنیک‌های بهینه‌سازی

### Code Splitting
- از dynamic imports استفاده کن
- از route-based splitting استفاده کن
- از component-based splitting استفاده کن

### Lazy Loading
- از lazy loading برای images استفاده کن
- از lazy loading برای components استفاده کن
- از Intersection Observer استفاده کن

### Memoization
- از memoization برای expensive calculations استفاده کن
- از computed values استفاده کن
- از caching برای API calls استفاده کن

### Virtualization
- از virtual lists برای lists بزرگ استفاده کن
- از windowing برای tables بزرگ استفاده کن
- از pagination برای data زیاد استفاده کن

## قوانین

### Bundle Size
- از tree shaking استفاده کن
- از code splitting استفاده کن
- از dynamic imports استفاده کن

### Runtime Performance
- از efficient algorithms استفاده کن
- از debouncing/throttling استفاده کن
- از requestAnimationFrame استفاده کن

### Memory Management
- از proper cleanup استفاده کن
- از event listener cleanup استفاده کن
- از subscription cleanup استفاده کن

### Network Optimization
- از compression استفاده کن
- از HTTP/2 استفاده کن
````

---

## `performance/runtime.mdc`

````mdc
---
description: Runtime performance optimization including virtual scrolling, debouncing, throttling, requestAnimationFrame, and memoization
globs:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
alwaysApply: false
---

# Runtime Performance

## Virtual Scrolling

برای لیست‌های بلند (10,000+ items):
- فقط visible items render کن
- Dynamic height calculation
- Smooth scrolling

## Debouncing & Throttling

- **Debounce:** برای search input (300ms delay)
- **Throttle:** برای scroll events (100ms interval)

## RequestAnimationFrame

برای animations:
- استفاده از `requestAnimationFrame` به جای `setTimeout`
- Smooth 60fps animations
- Cancel animation در cleanup

## Memoization

برای محاسبات سنگین:
- Cache results
- فقط recalculate هنگام dependency change
- از unnecessary recalculations پرهیز کن
- در Vue از `computed` استفاده کن

## Image Optimization

- WebP format
- Lazy loading (`loading="lazy"`)
- Responsive images (`srcset`, `sizes`)
- Progressive loading (skeleton screens)
````

---

## `performance/asset-management.mdc`

````mdc
---
description: Asset management rules for images, fonts, icons including formats, responsive images, lazy loading, and caching strategies
globs:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
  - "frontend/src/**/*.css"
alwaysApply: false
---

# Asset Management Rules

## مدیریت بارگذاری تصاویر

### Formats
- از WebP برای تصاویر استفاده کن
- از AVIF برای تصاویر با کیفیت بالا استفاده کن
- از fallback formats استفاده کن

### Responsive Images
- از `srcset` استفاده کن
- از `sizes` استفاده کن
- از `picture` element استفاده کن

### Lazy Loading
- از native lazy loading استفاده کن
- از Intersection Observer استفاده کن
- از placeholder images استفاده کن

## مدیریت فونت‌ها

### Font Loading
- از font-display: swap استفاده کن
- از preload برای critical fonts استفاده کن
- از font subsetting استفاده کن

### Font Formats
- از WOFF2 استفاده کن
- از WOFF به عنوان fallback استفاده کن
- از system fonts در صورت امکان استفاده کن

## مدیریت آیکون‌ها

### SVG Icons
- از SVG برای آیکون‌ها استفاده کن
- از SVG sprite استفاده کن
- از icon components استفاده کن

### Icon Fonts
- از icon fonts برای آیکون‌های متعدد استفاده کن
- از subsetting استفاده کن
- از fallback استفاده کن

## قوانین

### Optimization
- از image optimization استفاده کن
- از compression استفاده کن

### Caching
- از proper cache headers استفاده کن
- از cache busting استفاده کن
- از versioning استفاده کن

### Loading Strategy
- از critical assets first استفاده کن
- از preload برای critical resources استفاده کن
- از prefetch برای future resources استفاده کن
````

---

## `testing/strategy.mdc`

````mdc
---
description: Testing strategy — testing pyramid, coverage targets, Vitest, AAA pattern
globs:
  - "frontend/src/**/*.test.js"
  - "frontend/src/**/*.spec.js"
  - "frontend/src/test/**/*"
alwaysApply: false
---

# Testing Strategy

## Testing Pyramid

```
     /\
    /E2E\         ← 10% (کند، گران)
   /------\
  /  Int.  \      ← 20% (متوسط)
 /----------\
/   Unit     \    ← 70% (سریع، ارزان)
/--------------\
```

## Test Coverage Targets

- ✅ **70%+ overall**
- ✅ **90%+ for utilities/services**
- ✅ **50%+ for components** (focus on logic، not styling)

## Testing Tools (frontend)

- **Unit:** Vitest + Vue Test Utils (@vue/test-utils)
- **E2E:** Playwright (در صورت استفاده)
- **Pinia:** setActivePinia(createPinia()) در setup هر test

## AAA Pattern

**Arrange** (آماده‌سازی): Setup test data، mock dependencies  
**Act** (عمل): Execute function/action  
**Assert** (اثبات): Verify results

## Test Organization

- از test structure منطقی استفاده کن
- از test naming واضح استفاده کن
- از test isolation استفاده کن
- از test fixtures و mocks برای dependencies استفاده کن
````

---

## `testing/unit-testing.mdc`

````mdc
---
description: Unit testing for frontend — Vitest, Vue Test Utils, component and Pinia store tests
globs:
  - "frontend/src/**/*.test.js"
  - "frontend/src/**/*.spec.js"
  - "frontend/src/test/**/*"
alwaysApply: false
---

# Unit Testing (frontend)

## Component Testing

**با Vitest + Vue Test Utils (یا @vue/test-utils):**
- Test user interactions
- Test props و emit
- Test accessibility (در صورت استفاده از Testing Library)

**الگو:**
- Mount component با `mount()` و options (props، global.plugins برای Pinia/Router)
- Query elements (by role، label، text)
- Fire events (`wrapper.find('button').trigger('click')`)
- Assert expectations (`expect(wrapper.text()).toContain(...)`)

## Pinia Store Testing

**الگو:**
- ایجاد store با `setActivePinia(createPinia())` قبل از هر test
- Test initial state
- Test actions و mutations روی state
- Test getters (computed)
- Test error handling

## Utility و Service Testing

- Pure functions
- Edge cases (null، empty، invalid)
- Error handling
- Mock axios/fetch برای service tests

## Best Practices

- Test behavior، not implementation
- Test user interactions از دید کاربر
- Isolate tests (no shared state بین tests)
- Clear test names: `test('submits form when button clicked', ...)`
- AAA pattern: Arrange، Act، Assert
````

---

## `testing/e2e-testing.mdc`

````mdc
---
description: End-to-end testing guidelines for critical user flows and visual regression
globs:
  - "frontend/**/*.e2e.js"
  - "frontend/e2e/**/*"
alwaysApply: false
---

# E2E Testing

## Test Coverage

**Test critical user flows:**
- Authentication (login / signup)
- Form submissions
- Navigation
- Main features (e.g. vehicle list، reminders)

## Test Structure

**با Playwright (در صورت استفاده):**
- Navigate to page
- Interact with elements
- Assert expectations
- Verify URLs

## Best Practices

- Test real user scenarios
- Use data-testid برای stable selectors
- Wait for network idle
- Cleanup بعد از tests
- Screenshots برای debugging

## Visual Regression

- Baseline screenshots
- Compare on CI/CD
- Update baselines هنگام intentional changes
````

---

## `tools/vue.mdc`

````mdc
---
description: Vue 3 best practices — script setup, Composition API, component structure, JSDoc for .js
globs:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
alwaysApply: false
---

# Vue 3 Best Practices (frontend)

## &lt;script setup&gt;

- از `<script setup>` برای تمام کامپوننت‌های جدید استفاده کن
- ترتیب: imports → defineProps/defineEmits → composables/stores → state → computed → watch → lifecycle → methods

## Composition API

- از ref برای primitives و reference به object
- از reactive برای objectهایی که reassign نمی‌شوند
- از computed برای derived state
- از watch/watchEffect برای side effects

## Component Structure

- یک فایل یک کامپوننت؛ نام فایل PascalCase: `UserCard.vue`
- بخش‌ها به ترتیب: `<script setup>`, `<template>`, `<style scoped>`
- از scoped styles استفاده کن تا تداخل با global نباشد

## Props و Emits

- defineProps با type یا validator
- defineEmits با آرایه یا object (برای validation)
- در template از kebab-case برای events استفاده کن: `@update-value`

## JSDoc در .js (بدون TypeScript)

در فایل‌های .js (services، composables، utils) از JSDoc برای type hint استفاده کن:

```javascript
/**
 * @param {number} id
 * @returns {Promise<{ name: string }>}
 */
export async function fetchUser(id) { ... }
```

## Composables

- نام با پیشوند `use`: `useToast`, `useFocus`
- در پوشه `src/composables/` قرار بده
- state و logic قابل استفاده مجدد را برگردان

## Router و Views

- هر route به یک View component در `src/views/` map شود
- از lazy loading برای route components استفاده کن: `() => import('@/views/DashboardView.vue')`
````

---

## `tools/vite.mdc`

````mdc
---
description: Vite configuration and optimization for frontend (Vue 3, Vue plugin)
globs:
  - "frontend/vite.config.*"
  - "frontend/package.json"
alwaysApply: false
---

# Vite Configuration & Optimization (frontend)

## Base Configuration

```javascript
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    target: 'es2015',
    minify: 'terser',
    cssMinify: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'vue-router', 'pinia'],
        },
        assetFileNames: 'assets/[name]-[hash][extname]',
        chunkFileNames: 'chunks/[name]-[hash].js',
        entryFileNames: '[name]-[hash].js',
      },
    },
    assetsInlineLimit: 4096,
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  envPrefix: 'VITE_',
});
```

## Code Splitting

**Lazy loading برای route components:**
```javascript
const routes = [
  {
    path: '/dashboard',
    component: () => import('@/views/DashboardView.vue'),
  },
];
```

**قوانین:**
- از code splitting برای routes استفاده کن
- از tree shaking استفاده کن
- از minification استفاده کن

## Asset Optimization

- از proper asset imports استفاده کن
- از asset inlining برای فایل‌های کوچک (<4KB) استفاده کن

## بهینه‌سازی

### Configuration
- از path alias (`@` → `src/`) استفاده کن
- از environment variables با پیشوند `VITE_` استفاده کن

### Development
- از HMR استفاده کن
- از dev server proxy برای API استفاده کن

### Production
- از chunk splitting برای vendor (vue, vue-router, pinia) استفاده کن
- از build optimization استفاده کن
````

---


## `architecture/project-structure.mdc`

````mdc
---
description: Project structure for frontend (Vue 3, Vite), file organization, naming, and asset management
globs:
  - "frontend/**/*"
alwaysApply: false
---

# Project Structure (frontend)

## ساختار پیشنهادی

```
frontend/
├── public/                    # Static assets (بدون processing)
│   ├── favicon.ico
│   ├── fonts/                 # فونت‌های استاتیک
│   └── pwa-*.png
│
├── src/
│   ├── components/           # کامپوننت‌های قابل استفاده مجدد
│   │   ├── ui/               # کامپوننت‌های UI پایه (atoms, molecules)
│   │   ├── features/         # کامپوننت‌های feature-specific
│   │   ├── layout/           # layout (Sidebar, Header, MainLayout)
│   │   └── index.js          # barrel exports
│   │
│   ├── views/                # صفحات (route-level components)
│   │   ├── DashboardView.vue
│   │   ├── LoginView.vue
│   │   └── ...
│   │
│   ├── stores/               # Pinia stores (global state)
│   │   ├── auth.js
│   │   ├── vehicle.js
│   │   └── index.js
│   │
│   ├── services/             # API calls و business logic
│   │   ├── dashboardService.js
│   │   ├── serviceTypeService.js
│   │   └── index.js
│   │
│   ├── composables/          # Vue composables (useToast, useFocus, ...)
│   ├── router/               # Vue Router
│   │   └── index.js
│   ├── i18n/                 # بین‌المللی‌سازی
│   ├── locales/
│   ├── assets/               # منابع استاتیک (با Vite processing)
│   ├── style.css             # استایل سراسری
│   ├── main.js               # Entry point
│   └── App.vue
│
├── src/test/                 # Test setup و utils
├── .env.example
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── README.md
```

## قوانین سازماندهی

- هر کامپوننت در فایل خودش
- از index.js برای barrel export استفاده کن
- از grouping منطقی استفاده کن (ui/, features/, layout/)
- از naming conventions ثابت استفاده کن

## نامگذاری فایل‌ها

- ✅ Components: **PascalCase** (`Button.vue`, `UserCard.vue`)
- ✅ Utilities/Services: **camelCase** (`formatDate.js`, `serviceTypeService.js`)
- ✅ Stores (Pinia): **camelCase** (`auth.js`, `vehicle.js`)
- ✅ Styles: **kebab-case** (`global.css`, `reset.css`)

## مدیریت Assets

### تصاویر
- در `public/` یا `src/assets/` قرار بده
- از فرمت‌های مناسب استفاده کن (JPG, PNG, SVG, WebP)
- از responsive images با `srcset` استفاده کن

### فونت‌ها
- در `public/fonts` یا `src/assets/fonts` قرار بده
- از فرمت‌های WOFF2 و WOFF استفاده کن

### آیکون‌ها
- از SVG استفاده کن
- در `src/assets/` یا کامپوننت‌های Icon
````

---

## `patterns/props-events.mdc`

````mdc
---
description: Vue props and emits guidelines (defineProps, defineEmits)
globs:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
alwaysApply: false
---

# Props and Emits (Vue 3)

## قوانین مدیریت Props

### Naming
- از camelCase در script استفاده کن
- در template می‌توانی kebab-case استفاده کن: `user-name`
- از boolean props با is/has/can شروع کن

### Types و Defaults
- از `defineProps` با type یا validator استفاده کن
- از default values برای optional props استفاده کن
- در .js از JSDoc برای type hint استفاده کن

✅ **Good:**
```vue
<script setup>
const props = defineProps({
  variant: { type: String, default: 'primary' },
  disabled: { type: Boolean, default: false },
  count: { type: Number, required: true }
});
</script>
```

### Organization
- props را به گروه‌های منطقی تقسیم کن
- از destructuring در صورت نیاز استفاده کن (با toRefs اگر reactive لازم است)

### Validation
- از validator در defineProps استفاده کن
- از clear error messages استفاده کن

## قوانین مدیریت Emits

### Naming
- از kebab-case برای event names در template استفاده کن: `@update-value`
- از action-oriented names استفاده کن

### Data
- از payload structure ثابت استفاده کن
- از minimal data استفاده کن

### Declaration
✅ **Good:**
```vue
<script setup>
const emit = defineEmits(['submit', 'cancel', 'update:modelValue']);
// با validation:
const emit = defineEmits({
  submit: (payload) => payload && typeof payload.id === 'number'
});
</script>
```

### Communication
- از emit برای parent-child communication استفاده کن
- از Pinia برای sibling یا global communication استفاده کن

### Documentation
- از JSDoc یا comments برای payload structure استفاده کن
````

---

## `patterns/reactivity.mdc`

````mdc
---
description: Vue 3 reactivity principles — ref, reactive, computed, watch
globs:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
alwaysApply: false
---

# Reactivity Principles (Vue 3)

## ref و reactive

**ref:** برای primitive values و references به object
✅ **Good:**
```javascript
const count = ref(0);
const user = ref({ name: 'Ali' });
// در template: count، user — unwrap خودکار
```

**reactive:** برای objectها؛ نمی‌توان reassign کرد
✅ **Good:**
```javascript
const state = reactive({ count: 0, name: 'Ali' });
```

## computed

برای derived state که وابسته به reactive data است.
✅ **Good:**
```javascript
const doubled = computed(() => count.value * 2);
const fullName = computed(() => `${firstName.value} ${lastName.value}`);
```

❌ **Bad:** side effect در computed؛ computed باید pure باشد.

## watch و watchEffect

**watch:** برای side effects وقتی یک یا چند منبع تغییر می‌کند
✅ **Good:**
```javascript
watch(count, (newVal, oldVal) => { ... });
watch([a, b], ([newA, newB]) => { ... });
watch(() => obj.id, (id) => { ... }, { immediate: true });
```

**watchEffect:** برای اجرای فوری و track خودکار dependencies
✅ **Good:** وقتی به همه dependencies در یک بلوک نیاز داری

## قوانین

- Reactive statements فقط زمانی اجرا می‌شوند که dependencies تغییر کنند
- از circular dependencies پرهیز کن
- در composables از ref/reactive برگردان و در component استفاده کن
- برای store state از `storeToRefs` استفاده کن تا reactivity حفظ شود
````

---

## `patterns/component-patterns.mdc`

````mdc
---
description: Vue 3 component structure, script setup order, and standard patterns
globs:
  - "frontend/src/**/*.vue"
alwaysApply: false
---

# Component Patterns (Vue 3)

## Component Structure با &lt;script setup&gt;

**ترتیب استاندارد در &lt;script setup&gt;:**
1. Imports
2. defineProps / defineEmits
3. Composables (استفاده از store، router، composables دیگر)
4. Local state (ref, reactive)
5. computed
6. watch / watchEffect
7. Lifecycle (onMounted, onUnmounted, ...)
8. Event handlers و helper functions

✅ **Good:**
```vue
<script setup>
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';

const props = defineProps({ ... });
const emit = defineEmits(['submit']);

const count = ref(0);
const doubled = computed(() => count.value * 2);

onMounted(() => { ... });

function handleSubmit() { ... }
</script>

<template>...</template>

<style scoped>...</style>
```

## Props و Emits Pattern

- از defineProps با type یا validator استفاده کن
- از defineEmits برای events استفاده کن
- Props و emits را در بالای script قرار بده

## Slots Pattern

- Default slot برای محتوای اصلی
- Named slots برای بخش‌های خاص
- Slot fallback با محتوای پیش‌فرض

## استفاده از Pinia در کامپوننت

- از store فقط در جایی که نیاز است استفاده کن
- برای نگه داشتن reactivity از `storeToRefs(store)` استفاده کن؛ actions را مستقیم از store صدا بزن
````

---

## `patterns/api-integration.mdc`

````mdc
---
description: Best practices for API integration, error handling, loading states, caching, and form validation
globs:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
alwaysApply: false
---

# API Integration Rules

## بهترین شیوه‌ها برای ارتباط با backend

### Service Layer
- از service layer برای API calls استفاده کن (مثلاً `src/services/`)
- از separation of concerns استفاده کن
- از error handling مناسب استفاده کن

### Error Handling
- از try-catch برای error handling استفاده کن
- از error messages واضح استفاده کن
- از error states در UI استفاده کن

### Loading States
- از loading states استفاده کن
- از skeleton screens استفاده کن
- از progress indicators استفاده کن

## مدیریت وضعیت‌های بارگذاری و خطا

### Loading States
- از boolean flags برای loading استفاده کن (مثلاً `isLoading`)
- از loading components استفاده کن
- از optimistic updates در صورت مناسب استفاده کن

### Error States
- از error messages واضح استفاده کن
- از retry mechanisms استفاده کن
- از error boundaries یا global error handler استفاده کن

### Empty States
- از empty states استفاده کن
- از helpful messages استفاده کن
- از call-to-action استفاده کن

## استراتژی caching داده‌ها

### Client-Side Caching
- از browser cache استفاده کن
- از memory cache (مثلاً در store) استفاده کن
- از cache invalidation استفاده کن

### Cache Strategy
- از cache-first برای static data استفاده کن
- از network-first برای dynamic data استفاده کن
- از stale-while-revalidate در صورت نیاز استفاده کن

## مدیریت فرم‌ها و اعتبارسنجی

### Form Validation
- از client-side validation استفاده کن
- از server-side validation استفاده کن
- از real-time validation استفاده کن

### Error Messages
- از error messages واضح استفاده کن
- از field-level errors استفاده کن
- از form-level errors استفاده کن

### User Experience
- از inline validation استفاده کن
- از helpful hints استفاده کن
- از disabled states استفاده کن
````

---

## `patterns/anti-patterns.mdc`

````mdc
---
description: Common anti-patterns in frontend development and their correct solutions
globs:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
alwaysApply: false
---

# Anti-Patterns

قاعده‌های عمومی anti-pattern در
`.cursor/rules/share/code-quality-baseline.mdc`
تعریف شده‌اند. این فایل فقط anti-patternهای اختصاصی frontend را پوشش می‌دهد.

## Prop Drilling

❌ **Bad:** Prop drilling عمیق (>3 سطح)
- Props را از parent به child به grandchild می‌فرستی

✅ **Good:** استفاده از Pinia store
- Shared state در store نگه دار
- مستقیماً در کامپوننت‌ها با store استفاده کن

## Massive Components

❌ **Bad:** کامپوننت 500+ خطی
- همه چیز در یک فایل

✅ **Good:** تقسیم به کامپوننت‌های کوچک
- Single Responsibility Principle
- Composable components

## Inline Styles Everywhere

❌ **Bad:** استفاده زیاد از inline styles
- Hard to maintain
- No reusability

✅ **Good:** Scoped styles
- `<style scoped>` یا CSS classes
- CSS Custom Properties

## No Loading States

❌ **Bad:** بدون loading indicator
- کاربر منتظر می‌ماند بدون feedback

✅ **Good:** Loading states
- Spinner یا skeleton screen
- Clear feedback

## Global State Abuse

❌ **Bad:** همه چیز در Pinia store
- UI states که فقط local باید باشند

✅ **Good:** Local state برای UI
- Pinia فقط برای shared data
- ref/reactive در component برای UI-specific state
````

---

## `state/pinia.mdc`

````mdc
---
description: Pinia store patterns — defineStore, state, getters, actions — and usage in Vue components
globs:
  - "frontend/src/**/*.vue"
  - "frontend/src/stores/**/*.js"
alwaysApply: false
---

# State Management (Pinia)

## defineStore

از Composition API style (setup function) یا Options style استفاده کن. برای frontend ترجیحاً setup style با ref/reactive.

✅ **Good (Setup store):**
```javascript
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null);
  const isLoggedIn = computed(() => !!user.value);

  function setUser(u) { user.value = u; }
  function logout() { user.value = null; }

  return { user, isLoggedIn, setUser, logout };
});
```

## State و Getters و Actions

- **State:** داده‌های reactive (ref/reactive در setup store)
- **Getters:** از computed برای derived state استفاده کن
- **Actions:** توابع async یا sync برای تغییر state و side effects (API calls در action یا در service و سپس فراخوانی از action)

## استفاده در کامپوننت

✅ **Good:** برای حفظ reactivity از storeToRefs استفاده کن
```vue
<script setup>
import { storeToRefs } from 'pinia';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const { user, isLoggedIn } = storeToRefs(authStore);
const { logout } = authStore;
</script>
```

❌ **Bad:** destructuring مستقیم از store بدون storeToRefs — reactivity از بین می‌رود.

## قوانین

- یک store یک حوزه مسئولیت (مثلاً auth، vehicle، ui)
- از نام‌گذاری camelCase برای فایل store استفاده کن: `auth.js`, `vehicle.js`
- API calls را در service انجام بده و در action فقط store را به‌روز کن؛ یا در action از service استفاده کن
- از persist plugin فقط در صورت نیاز (مثلاً auth token)
````

---

## `state/local-vs-global.mdc`

````mdc
---
description: Decision rules for choosing between local state and global state (Pinia) in Vue components
globs:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
alwaysApply: false
---

# Local vs Global State

## Decision Rule

State را در نزدیک‌ترین common ancestor نگه دار؛ اگر بیش از 2 کامپوننت به آن نیاز دارند از Pinia استفاده کن.

## Local State

**استفاده کن برای:**
- UI state که فقط یک component نیاز دارد (isOpen, isExpanded)
- Form inputs (local state تا submit)
- Temporary UI state

**مثال:** Modal open/close، dropdown state — با `ref` یا `reactive` در همان کامپوننت

## Global State (Pinia)

**استفاده کن برای:**
- Data که چندین component نیاز دارد
- User authentication state
- Application-wide settings
- Theme / locale
- Data مشترک بین views (مثلاً لیست خودروها، تنظیمات)

**قانون:** اگر بیش از 2 component به state نیاز دارند، در Pinia store تعریف کن.
````

---


## `core/ai-behavior.mdc`

````mdc
---
description: AI behavior guidelines and priorities for frontend development
globs:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
  - "frontend/src/**/*.css"
alwaysApply: false
---

# AI Behavior Guidelines

## اولویت‌های اجرایی (به ترتیب اهمیت)

1. **UI/UX First** - تجربه کاربر در اولویت
   - کد باید تجربه کاربری روان و بصری جذاب ایجاد کند
   - هر کامپوننت باید responsive و accessible باشد
   - رابط کاربری باید intuitive و self-explanatory باشد
   - از اصول طراحی بصری پیروی کن (visual hierarchy, contrast, spacing)
   - همیشه از دید کاربر نهایی به طراحی نگاه کن
   - تاخیر در واکنش‌ها را به حداقل برسان

2. **Accessibility First** - دسترسی‌پذیری در اولویت
   - WCAG 2.1 AA compliance الزامی است
   - همیشه از semantic HTML استفاده کن
   - keyboard navigation و screen reader support اجباری
   - Color contrast minimums را رعایت کن (4.5:1 for text)
   - دسترس‌پذیری یک ویژگی اضافی نیست، یک الزام است

3. **Mobile-First** - موبایل در اولویت
   - طراحی از موبایل شروع شود و به دسکتاپ گسترش یابد
   - Touch targets حداقل 44×44px
   - از viewport units و relative units استفاده کن (نه px ثابت)
   - برای موبایل طراحی کن، سپس برای صفحات بزرگتر

4. **Performance First** - عملکرد در اولویت
   - Bundle size: هر route حداکثر 170KB (gzipped)
   - First Contentful Paint: <1.8s
   - Time to Interactive: <3.8s
   - از lazy loading و code splitting استفاده کن
   - برنامه باید سریع بارگذاری شود و روان اجرا شود
   - بهینه‌سازی‌ها را بر اساس داده‌های واقعی انجام ده، نه حدس و گمان
   - محدودیت‌های دستگاه‌های ضعیف‌تر را در نظر بگیر

5. **Maintainability** - قابلیت نگهداری
   - کدی بنویس که همکار بعدی بتواند به راحتی آن را درک و تغییر دهد
   - از ساختارهای پیچیده و "هوشمندانه" بدون دلیل مشخص پرهیز کن
   - کامپوننت‌ها باید قابل استفاده مجدد و مستقل باشند

## قوانین خاص تولید کد Frontend توسط AI

- **همیشه Responsive بساز:** هر کامپوننت باید در تمام breakpoints تست شود
- **Component Reusability:** کامپوننت‌ها باید قابل استفاده مجدد و isolated باشند
- **Props با Type Safety:** همه props باید type-safe باشند (JSDoc یا TypeScript)
- **همیشه قبل از معرفی یک الگوی پیچیده، توضیح بده** چرا این الگو لازم است
- **تجربه کاربری را فدای کد "تمیز" نکن** - گاهی یک راه‌حل ساده‌تر برای کاربر بهتر است حتی اگر کد کمی پیچیده‌تر شود
- **در صورت شک، از کاربر بپرس:** برای طراحی UI پیچیده، mockup یا توضیح بیشتر بخواه
- **همیشه به دسترس‌پذیری (Accessibility) توجه کن** - این یک ویژگی اضافی نیست، یک الزام است
- **تغییرات تدریجی را به تغییرات بزرگ ترجیح بده** (Incremental Refactoring)

## Performance Budget (بودجه عملکرد)

**الزامات سخت:**
- Initial JS bundle: **<170KB** (gzipped)
- Initial CSS: **<50KB** (gzipped)
- Total page weight: **<1MB**
- Images: WebP format, lazy-loaded
- Fonts: <100KB, with font-display: swap

**Core Web Vitals:**
- **LCP (Largest Contentful Paint):** <2.5s
- **FID (First Input Delay):** <100ms
- **CLS (Cumulative Layout Shift):** <0.1

## قوانین تصمیم‌گیری برای AI

1. **اولویت تجربه کاربری:** همیشه تجربه کاربری را بر کد "تمیز" ترجیح ده
2. **دسترس‌پذیری اولیه:** دسترس‌پذیری یک ویژگی اضافی نیست، یک الزام است
3. **عملکرد مهم است:** بهینه‌سازی‌ها را بر اساس داده‌های واقعی انجام ده، نه حدس و گمان
4. **سادگی بر پیچیدگی:** راه‌حل ساده را به راه‌حل پیچیده ترجیح ده، مگر اینکه دلیل محکمی برای پیچیدگی وجود داشته باشد
5. **توسعه تدریجی:** تغییرات بزرگ را به بخش‌های کوچکتر تقسیم کنید
6. **ثبات در طراحی:** از design tokens و اصول طراحی ثابت استفاده کنید
7. **واکنش‌گرایی اول:** برای موبایل طراحی کنید، سپس برای صفحات بزرگتر

## الگوهای ترجیحی برای AI

1. **Component-First Development:** همیشه از کامپوننت‌های قابل استفاده مجدد استفاده کنید
2. **Atomic Design:** از اصول Atomic Design برای ساختار UI استفاده کنید
3. **State Management:** از Pinia برای state سراسری استفاده کنید
4. **Error Handling:** از proper error handling و loading states استفاده کنید
5. **Responsive Design:** از رویکرد mobile-first برای طراحی واکنش‌گرا استفاده کنید
6. **Accessibility:** از proper ARIA attributes و semantic HTML استفاده کنید
7. **Performance:** از lazy loading و code splitting برای بهینه‌سازی عملکرد استفاده کنید

## User Experience Over Developer Experience

وقتی تجربه کاربر و راحتی توسعه‌دهنده در تضاد هستند، تجربه کاربر برنده است.

مثال:
- Bundle size optimization (حتی اگر کد پیچیده‌تر شود)
- Manual performance optimization (حتی اگر زمان بیشتری بگیرد)
- Accessibility compliance (حتی اگر markup بیشتری لازم باشد)
````

---

## `core/meta-principles.mdc`

````mdc
---
description: Meta-principles and fundamental design principles underlying all frontend development rules
globs:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
  - "frontend/src/**/*.css"
alwaysApply: false
---

# Meta-Principles

اصول پایه frontend. اصول جهان‌شمول در فایل اشتراکی تعریف شده‌اند:
`.cursor/rules/share/engineering-principles.mdc`

اگر اختلافی وجود داشت، rule تخصصی frontend در این فایل اولویت دارد.

## Frontend-Specific Principles

### Single Source of Truth در UI
- برای تصمیم‌های طراحی از design tokens و CSS variables استفاده کن.
- منبع مقادیر design باید مرکزی و قابل ردیابی باشد.

### Component Reusability
- کامپوننت‌ها isolated و self-contained باشند.
- از props/slots برای customization استفاده کن.
- وابستگی مستقیم به context خاص parent ایجاد نکن.

### Progressive Enhancement
- HTML/CSS پایه باید بدون JavaScript نیز قابل استفاده باشد.
- فرم‌ها باید با HTML5 validation کار کنند.

### Mobile-First Design
- base styles بدون media query (موبایل) باشند.
- media queryها فقط `min-width` باشند.
- touch targets حداقل `44x44px` رعایت شوند.

### Accessibility First
- semantic HTML همیشه اولویت دارد.
- ARIA فقط وقتی semantic کافی نیست استفاده شود.
- همه عناصر تعاملی باید keyboard-accessible باشند.

### Performance First (Frontend)
- lazy loading برای محتوای off-screen.
- code splitting برای routeها.
- بهینه‌سازی image/font پیش‌فرض باشد.
````

---

## `core/code-quality.mdc`

````mdc
---
description: Code quality standards, naming conventions, and documentation requirements for frontend (Vue 3, .vue, .js)
globs:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
  - "frontend/src/**/*.css"
alwaysApply: false
---

# Code Quality Standards

## Shared Baseline

- baseline عمومی کیفیت کد در:
  `.cursor/rules/share/code-quality-baseline.mdc`
- این فایل فقط جزئیات اختصاصی frontend را تعریف می‌کند.

## Component Quality Checklist

- [ ] **Reusable:** کامپوننت قابل استفاده مجدد است؟
- [ ] **Props Typed:** props با JSDoc یا validator مستند شده؟
- [ ] **Emits:** custom emits مستند شده؟
- [ ] **Scoped Styles:** styles scoped هستند یا global conflicts ندارند؟
- [ ] **No Side Effects:** کامپوننت isolated و بدون side effects ناخواسته؟
- [ ] **Size:** کامپوننت کمتر از 200 خط؟

## قراردادهای نام‌گذاری

### فایل‌ها
- ✅ Components: **PascalCase** (`Button.vue`, `UserCard.vue`)
- ✅ Utilities: **camelCase** (`formatDate.js`, `validators.js`)
- ✅ Stores (Pinia): **camelCase** (`auth.js`, `vehicle.js`)
- ✅ Services: **camelCase** (`dashboardService.js`, `serviceTypeService.js`)
- ✅ Styles: **kebab-case** (`global.css`, `reset.css`)
- ✅ Constants: **UPPER_SNAKE_CASE** (`API_BASE_URL.js`, `COLORS.js`)

### متغیرها و توابع
- از camelCase برای متغیرها و توابع استفاده کن: `userName`, `getUserData()`
- از نام‌های توصیفی استفاده کن: `isLoading` به جای `loading`, `handleSubmit` به جای `submit`
- برای متغیرهای بولین، از پیشوندهای is/has/can استفاده کن: `isVisible`, `hasError`, `canEdit`

### CSS
- از BEM (Block Element Modifier) استفاده کن: `.card__title--highlighted`
- از kebab-case برای نام کلاس‌ها استفاده کن: `.user-profile`, `.search-box`
- از پیشوندهای خاص برای جلوگیری از تداخل: `.c-button` (c برای component), `.u-hidden` (u برای utility)

### کامپوننت‌ها
- از نام‌های توصیفی استفاده کن: `UserProfile` به جای `User`, `SearchBox` به جای `Search`
- برای کامپوننت‌های UI پایه: `Button.vue`, `Input.vue`, `Modal.vue`
- برای کامپوننت‌های feature: `UserCard.vue`, `ServiceTypeSelector.vue`

## Code Smells

**کامپوننت‌های مشکوک:**
- کامپوننت‌های بیش از 200 خط
- کامپوننت‌هایی که هم state management و هم UI rendering دارند
- نام‌های ترکیبی: `UserProfileFormWithValidation`

## Documentation Requirements

هر کامپوننت باید شامل:
- File header (توضیح فارسی در صورت نیاز)
- Props مستند شده (JSDoc یا defineProps با type)
- Emits مستند شده
- نحوه استفاده
````

---

## `core/git-workflow.mdc`

````mdc
---
description: Frontend git workflow notes aligned with share/gitflow-unified
globs:
  - "frontend/**/*"
alwaysApply: false
---

# Git Workflow Rules

## Source of Truth

- مرجع اصلی و الزامی Git Flow در پروژه:
  - `.cursor/rules/share/gitflow-branch-policy.mdc`
- اگر اختلافی وجود داشت، همیشه `gitflow-branch-policy.mdc` اولویت دارد.

## استراتژی شاخه‌بندی برای توسعه UI

- ایجاد شاخه ویژگی جدید: `feature/ui-component-name`
- ایجاد شاخه برای رفع باگ: `bugfix/ui-bug-description`
- برای بهبود عملکرد و refactor نیز از `feature/*` استفاده کن
- ایجاد شاخه برای نسخه جدید: `release/v1.0.0`
- ایجاد شاخه برای رفع فوری: `hotfix/ui-critical-fix`

تگ SemVer محصول از Cursor با `git tag` روی فیچر ساخته نمی‌شود. از `.cursor/skills/semver-release/SKILL.md` استفاده کن.

شروع کار و PR: سه نقطهٔ همگام‌سازی در `.cursor/rules/share/gitflow-branch-policy.mdc` (شروع با `pull --ff-only` روی `develop`، قبل از PR merge با `origin/develop`، بعد از merge پاک‌سازی).

## قراردادهای commit message برای تغییرات UI

### افزودن ویژگی جدید
```
feat(ui): add user profile component
```

### رفع باگ
```
fix(ui): resolve modal focus trap issue
```

### بازبینی کد
```
refactor(ui): simplify button component structure
```

### بهبود عملکرد
```
perf(ui): optimize image lazy loading
```

### تغییرات استایل
```
style(ui): update button hover states
```

### مستندات
```
docs(ui): add component usage examples
```

### تست
```
test(ui): add unit tests for form validation
```

### ساختار پروژه
```
chore(ui): reorganize component directory structure
```

## مدیریت تغییرات breaking در کامپوننت‌ها

- تغییرات breaking باید در CHANGELOG.md مستند شوند
- از semantic versioning استفاده کن
- تغییرات breaking باید در commit message با `BREAKING CHANGE:` مشخص شوند
````

---

## `architecture/solid.mdc`

````mdc
---
description: SOLID principles applied to frontend component design and architecture
globs:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
alwaysApply: false
---

# SOLID Principles

## SRP — Single Responsibility Principle

هر کامپوننت فقط یک دلیل برای تغییر دارد.

**چرا مهم است؟**
افزایش خوانایی، تست‌پذیری و قابلیت استفاده مجدد با تمرکز بر یک مسئولیت.

**قوانین:**
- کامپوننت‌ها باید یک مسئولیت واحد داشته باشند
- منطق نمایش را از منطق تجاری جدا کن
- منطق API را از کامپوننت‌ها جدا کن

## OCP — Open/Closed Principle

باز برای گسترش، بسته برای تغییر.

**چرا مهم است؟**
افزودن قابلیت جدید بدون تغییر کامپوننت‌های تست‌شده.

**قوانین:**
- از configuration objects برای رفتارهای مختلف استفاده کن
- از composition به جای modification استفاده کن
- از props و slots برای گسترش استفاده کن

## LSP — Liskov Substitution Principle

زیرکلاس‌ها باید بدون شکستن رفتار، جایگزین کلاس والد شوند.

**چرا مهم است؟**
تضمین رفتار صحیح در Polymorphism و جلوگیری از باگ‌های runtime.

**قوانین:**
- کامپوننت‌های مشتق شده باید با کامپوننت پایه قابل تعویض باشند
- از props مشترک و سازگار استفاده کن
- از رفتارهای غیرمنتظره در کامپوننت‌های مشتق شده پرهیز کن

## ISP — Interface Segregation Principle

کلاینت‌ها نباید به interface‌هایی که استفاده نمی‌کنند وابسته باشند.

**چرا مهم است؟**
کاهش وابستگی‌های غیرضروری و افزایش انعطاف‌پذیری.

**قوانین:**
- props را به گروه‌های منطقی تقسیم کن
- از props اختیاری به جای props اجباری استفاده کن
- از composition برای ترکیب قابلیت‌ها استفاده کن

## DIP — Dependency Inversion Principle

وابستگی‌ها باید به abstractions باشند، نه concretions.

**چرا مهم است؟**
کاهش coupling و افزایش قابلیت تست.

**قوانین:**
- از dependency injection استفاده کن
- از services برای منطق تجاری استفاده کن
- از Pinia stores برای state management استفاده کن
````

---

## `architecture/separation-of-concerns.mdc`

````mdc
---
description: Separation of concerns principles for separating UI logic, business logic, and data access
globs:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
alwaysApply: false
---

# Separation of Concerns

جداسازی منطق UI، منطق تجاری (business logic)، و دسترسی به داده.

## Layer Separation

### Presentational Components
- فقط UI rendering
- بدون business logic
- بدون direct API calls
- فقط props می‌گیرد و emit می‌کند

### Container Components (Views)
- مدیریت state و logic
- Data fetching coordination
- Event handling

### Services
- API calls
- Data transformation
- Business logic (pure functions)

### Stores (Pinia)
- Global state management
- Reactive state updates
- State persistence (در صورت نیاز)

## Anti-Pattern

❌ **Bad:** همه چیز در یک کامپوننت
- API calls در component
- Business logic در component
- UI rendering در همان component

✅ **Good:** جداسازی کامل
- Service برای API
- Pinia store برای state
- Component فقط UI
````

---

## `architecture/component-design.mdc`

````mdc
---
description: Vue component design principles, props, emits, slots, and composition
globs:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
alwaysApply: false
---

# Component Design Principles (Vue 3)

## اصول طراحی کامپوننت

### Single Responsibility Principle (SRP)

هر کامپوننت فقط یک کار انجام دهد.

**Code Smell:**
- کامپوننت‌های بیش از 200 خط
- کامپوننت‌هایی که هم state management و هم UI rendering دارند
- نام‌های ترکیبی: `UserProfileFormWithValidation`

**اصل:** تقسیم به کامپوننت‌های کوچک‌تر با مسئولیت واحد

### Composition over Configuration

- از composition برای ترکیب قابلیت‌ها استفاده کن
- از slots برای محتوای پویا استفاده کن
- از props برای configuration استفاده کن

### Props Design

- از `defineProps` با type یا validator استفاده کن
- از default values مناسب استفاده کن
- در .js از JSDoc برای type hint استفاده کن
- Props مستند شده

✅ **Good (script setup):**
```vue
<script setup>
const props = defineProps({
  variant: { type: String, default: 'primary' },
  disabled: { type: Boolean, default: false }
});
</script>
```

### Emits Design

- از `defineEmits` برای custom events استفاده کن
- از event names واضح (kebab-case در template) استفاده کن
- از payload structure ثابت استفاده کن

✅ **Good:**
```vue
<script setup>
const emit = defineEmits(['submit', 'cancel']);
emit('submit', { id: 1, name: 'Ali' });
</script>
```

### Slots Pattern

- Default slot برای محتوای اصلی
- Named slots برای بخش‌های خاص
- Slot fallback با محتوای پیش‌فرض

## Props Down, Events Up

داده از parent به child با props؛ communication از child به parent با emit.

**قانون:**
- State در parent (یا Pinia) نگه دار
- Child فقط props می‌گیرد و emit می‌کند
- از direct mutation از بیرون در child پرهیز کن

## Reusability

- کامپوننت‌ها باید قابل استفاده مجدد باشند
- از props برای customization استفاده کن
- از slots برای flexibility استفاده کن
- هر کامپوننت باید بدون وابستگی به parent/context خاص کار کند

## Documentation

- از JSDoc برای props در composables/services استفاده کن
- از comments برای منطق پیچیده استفاده کن
- File header در صورت نیاز (توضیح فارسی)
- Emits مستند شده

## Atomic Design در frontend

**ساختار:**
```
components/
├── ui/           # atoms & molecules
│   ├── Button.vue
│   ├── Input.vue
│   ├── Card.vue
│   └── Modal.vue
├── features/     # feature-specific
├── layout/       # MainLayout, Sidebar, Header
```

**قانون:** کامپوننت‌های کوچک را بساز و با composition ترکیب کن
````

---

## `architecture/atomic-design.mdc`

````mdc
---
description: Atomic Design principles for organizing UI components into atoms, molecules, organisms, templates, and pages
globs:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
alwaysApply: false
---

# Atomic Design Principles

## اصول Atomic Design

### Atoms (اتم‌ها)
کوچکترین اجزای UI که قابل تقسیم نیستند.

**مثال:** Button, Input, Label, Icon

**قوانین:**
- باید کاملاً مستقل و قابل استفاده مجدد باشند
- نباید وابستگی به سایر کامپوننت‌ها داشته باشند
- باید props محدود و واضح داشته باشند

### Molecules (مولکول‌ها)
ترکیب چند اتم برای ایجاد یک واحد عملکردی.

**مثال:** SearchBox (Input + Button), FormField (Label + Input)

**قوانین:**
- باید از atoms ساخته شوند
- باید یک مسئولیت واحد داشته باشند
- باید قابل استفاده مجدد در context‌های مختلف باشند

### Organisms (ارگانیسم‌ها)
ترکیب molecules و atoms برای ایجاد بخش‌های پیچیده UI.

**مثال:** Header, Table, Navigation

**قوانین:**
- باید از molecules و atoms ساخته شوند
- باید بخش‌های مستقل و قابل استفاده مجدد باشند
- می‌توانند state محلی داشته باشند

### Templates (الگوها)
ساختار صفحه بدون محتوای واقعی.

**قوانین:**
- باید layout و ساختار را تعریف کنند
- باید از organisms, molecules و atoms ساخته شوند
- باید wireframe-like باشند

### Pages (صفحات)
نمونه‌های واقعی از templates با محتوای واقعی.

**قوانین:**
- باید از templates ساخته شوند
- باید محتوای واقعی داشته باشند
- برای تست و مستندسازی استفاده می‌شوند

## استراتژی تقسیم کامپوننت‌ها

- از کوچک به بزرگ شروع کن
- هر کامپوننت باید در یک سطح مشخص قرار گیرد
- از composition برای ترکیب کامپوننت‌ها استفاده کن
````

---

