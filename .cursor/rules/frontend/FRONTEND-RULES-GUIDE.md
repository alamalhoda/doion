# راهنمای قوانین Frontend (Vue 3 / Vite / Pinia)

> این سند **راهنما و مستند** قوانین frontend است، نه فایل قانون. قوانین قابل اعمال در Cursor در فایل‌های `.mdc` قرار دارند.
>
> **English:** This document is a **guide and reference** for frontend rules, not a rule file. Enforceable rules are in `.mdc` files.
>
> **نسخه تجمیعی کامل:** `FRONTEND-RULES-FULL.md` — محتوای کامل همه Ruleهای `.mdc` بدون خلاصه‌سازی.

---

## نقشهٔ فایل‌های قانون

هر بخش زیر به فایل `.mdc` مربوط اشاره می‌کند:

### قوانین مشترک (Share)

این قوانین برای کل پروژه در پوشه `share/` تعریف شده‌اند و frontend را هم پوشش می‌دهند:

- `share/gitflow-branch-policy.mdc`
- `share/engineering-principles.mdc`
- `share/code-quality-baseline.mdc`

| بخش | فایل قانون | Globs | alwaysApply |
|-----|------------|-------|-------------|
| ۱. AI Behavior | `core/ai-behavior.mdc` | `frontend/src/**/*.{vue,js,css}` | false |
| ۲. Meta Principles | `core/meta-principles.mdc` | `frontend/src/**/*.{vue,js,css}` | false |
| ۳. Code Quality | `core/code-quality.mdc` | `frontend/src/**/*.{vue,js,css}` | false |
| ۴. Git Workflow | `core/git-workflow.mdc` | `frontend/**/*` | false |
| ۵. SOLID | `architecture/solid.mdc` | `frontend/src/**/*.{vue,js}` | false |
| ۶. Separation of Concerns | `architecture/separation-of-concerns.mdc` | `frontend/src/**/*.{vue,js}` | false |
| ۷. Component Design | `architecture/component-design.mdc` | `frontend/src/**/*.{vue,js}` | false |
| ۸. Atomic Design | `architecture/atomic-design.mdc` | `frontend/src/**/*.{vue,js}` | false |
| ۹. Project Structure | `architecture/project-structure.mdc` | `frontend/**/*` | false |
| ۱۰. Props & Events | `patterns/props-events.mdc` | `frontend/src/**/*.{vue,js}` | false |
| ۱۱. Reactivity | `patterns/reactivity.mdc` | `frontend/src/**/*.{vue,js}` | false |
| ۱۲. Component Patterns | `patterns/component-patterns.mdc` | `frontend/src/**/*.vue` | false |
| ۱۳. API Integration | `patterns/api-integration.mdc` | `frontend/src/**/*.{vue,js}` | false |
| ۱۴. Anti-Patterns | `patterns/anti-patterns.mdc` | `frontend/src/**/*.{vue,js}` | false |
| ۱۵. Pinia | `state/pinia.mdc` | `**/*.vue`, `**/stores/**/*.js` | false |
| ۱۶. Local vs Global | `state/local-vs-global.mdc` | `frontend/src/**/*.{vue,js}` | false |
| ۱۷. Bundle Size | `performance/bundle-size.mdc` | `**/*.js`, `vite.config.*` | false |
| ۱۸. Core Web Vitals | `performance/core-web-vitals.mdc` | `frontend/src/**/*.{vue,js,css}` | false |
| ۱۹. Optimization | `performance/optimization.mdc` | `frontend/src/**/*.{vue,js}` | false |
| ۲۰. Runtime | `performance/runtime.mdc` | `frontend/src/**/*.{vue,js}` | false |
| ۲۱. Asset Management | `performance/asset-management.mdc` | `frontend/src/**/*.{vue,js,css}` | false |
| ۲۲. Accessibility | `ui-ux/accessibility.mdc` | `frontend/src/**/*.{vue,js,css}` | false |
| ۲۳. Responsive Design | `ui-ux/responsive-design.mdc` | `frontend/src/**/*.{vue,css}` | false |
| ۲۴. Styling | `ui-ux/styling.mdc` | `frontend/src/**/*.{vue,css}` | false |
| ۲۵. Interaction Patterns | `ui-ux/interaction-patterns.mdc` | `frontend/src/**/*.{vue,js}` | false |
| ۲۶. User Feedback | `ui-ux/user-feedback.mdc` | `frontend/src/**/*.{vue,js}` | false |
| ۲۷. Testing Strategy | `testing/strategy.mdc` | `**/*.test.js`, `**/*.spec.js`, `**/test/**/*` | false |
| ۲۸. Unit Testing | `testing/unit-testing.mdc` | `**/*.test.js`, `**/*.spec.js`, `**/test/**/*` | false |
| ۲۹. E2E Testing | `testing/e2e-testing.mdc` | `**/*.e2e.js`, `e2e/**/*` | false |
| ۳۰. Vue 3 | `tools/vue.mdc` | `frontend/src/**/*.{vue,js}` | false |
| ۳۱. Vite | `tools/vite.mdc` | `frontend/vite.config.*`, `package.json` | false |

---

## ۱. AI Behavior — `core/ai-behavior.mdc`

**محتوا:** اولویت‌های اجرایی و قوانین تولید کد توسط AI برای frontend.

| موضوع | توضیح |
|-------|-------|
| UI/UX First | تجربه کاربر در اولویت؛ responsive و accessible |
| Accessibility First | WCAG 2.1 AA؛ semantic HTML؛ keyboard navigation؛ screen reader |
| Mobile-First | طراحی از موبایل؛ touch targets ≥44px |
| Performance First | Bundle <170KB؛ LCP <2.5s؛ TTI <3.8s؛ lazy loading |
| Maintainability | کد خوانا؛ قابل استفاده مجدد؛ تغییرات تدریجی |
| Performance Budget | Initial JS <170KB؛ CSS <50KB؛ LCP، FID، CLS |
| User Experience Over DX | تجربه کاربر بر تجربه توسعه‌دهنده |

---

## ۲. Meta Principles — `core/meta-principles.mdc`

**محتوا:** اصول پایهٔ طراحی frontend (SSOT، SoC، Mobile-First، Accessibility، …).

| اصل | توضیح |
|-----|-------|
| Single Source of Truth | State در یک جا؛ design tokens |
| Separation of Concerns | UI / Logic / Data جدا |
| Mobile-First | Base styles موبایل؛ min-width media queries |
| Accessibility First | Semantic HTML؛ ARIA؛ keyboard |
| Performance First | Lazy load؛ code splitting |
| Progressive Enhancement | کار با HTML/CSS پایه |

---

## ۳. Code Quality — `core/code-quality.mdc`

**محتوا:** استانداردهای کیفیت کد، نام‌گذاری، مستندسازی.

| موضوع | توضیح |
|-------|-------|
| Naming | Components: PascalCase؛ Files: kebab-case؛ CSS: BEM |
| Component Checklist | Reusable، Props typed، Emits documented، Scoped styles |
| Code Smells | >200 خط؛ state + UI در یک کامپوننت |
| Documentation | Props و Emits مستند شده |

---

## ۴. Git Workflow — `core/git-workflow.mdc`

**محتوا:** Branch strategy و commit convention برای frontend، همسو با مرجع اصلی:
`share/gitflow-branch-policy.mdc`.

| موضوع | توضیح |
|-------|-------|
| Branch | feature/*، bugfix/*، release/*، hotfix/* |
| Commit | feat، fix، refactor، style، docs، chore |

---

## ۵. SOLID — `architecture/solid.mdc`

**محتوا:** اصول SOLID در طراحی کامپوننت Vue.

| اصل | توضیح |
|-----|-------|
| SRP | هر کامپوننت یک مسئولیت |
| OCP | باز برای گسترش، بسته برای تغییر |
| LSP | جایگزینی بدون شکستن رفتار |
| ISP | props هدفمند؛ از props غیرضروری پرهیز |
| DIP | وابستگی به abstraction؛ Pinia، services |

---

## ۶. Separation of Concerns — `architecture/separation-of-concerns.mdc`

**محتوا:** جداسازی UI، business logic و data.

| لایه | توضیح |
|------|-------|
| Presentational | فقط UI؛ props و emit |
| Container | مدیریت state؛ data fetching |
| Services | API calls؛ business logic |
| Stores (Pinia) | State سراسری |

---

## ۷. Component Design — `architecture/component-design.mdc`

**محتوا:** اصول طراحی کامپوننت Vue — props، emits، slots، composition.

| موضوع | توضیح |
|-------|-------|
| SRP | یک کامپوننت، یک کار |
| Composition | ترکیب با slots و props |
| Props Down, Events Up | داده با props؛ ارتباط با emit |
| Reusability | قابل استفاده مجدد؛ بدون وابستگی به context |

---

## ۸. Atomic Design — `architecture/atomic-design.mdc`

**محتوا:** Atomic Design — atoms، molecules، organisms، templates، pages.

| سطح | توضیح |
|-----|-------|
| Atoms | Button، Input، Icon — کوچک‌ترین واحد |
| Molecules | SearchBox، FormField — ترکیب atoms |
| Organisms | Header، Table — بخش‌های پیچیده |
| Templates | ساختار صفحه بدون محتوا |
| Pages | نمونهٔ واقعی با محتوا |

---

## ۹. Project Structure — `architecture/project-structure.mdc`

**محتوا:** ساختار پروژه frontend، نام‌گذاری، organization.

| موضوع | توضیح |
|-------|-------|
| Structure | components/ui، components/features، layout، stores |
| Naming | PascalCase برای کامپوننت؛ camelCase برای فایل‌ها |

---

## ۱۰. Props & Events — `patterns/props-events.mdc`

**محتوا:** defineProps، defineEmits، payload structure.

| موضوع | توضیح |
|-------|-------|
| Props | defineProps با type؛ default values |
| Emits | defineEmits؛ kebab-case در template |
| Payload | ساختار ثابت برای emit |

---

## ۱۱. Reactivity — `patterns/reactivity.mdc`

**محتوا:** ref، reactive، computed، watch در Vue 3.

| موضوع | توضیح |
|-------|-------|
| ref | مقادیر ساده؛ reactive برای objects |
| computed | مقادیر مشتق شده |
| watch | واکنش به تغییرات |

---

## ۱۲. Component Patterns — `patterns/component-patterns.mdc`

**محتوا:** ساختار کامپوننت Vue 3، script setup، الگوهای استاندارد.

| موضوع | توضیح |
|-------|-------|
| Script Setup | ترتیب: imports، props، emits، composition |
| Structure | template، script، style |

---

## ۱۳. API Integration — `patterns/api-integration.mdc`

**محتوا:** اتصال به API، error handling، loading states، caching، form validation.

| موضوع | توضیح |
|-------|-------|
| API | استفاده از services؛ نه مستقیم در component |
| Error | proper error handling |
| Loading | loading states |
| Caching | کش برای داده‌های تکراری |

---

## ۱۴. Anti-Patterns — `patterns/anti-patterns.mdc`

**محتوا:** الگوهای نادرست و راه‌حل صحیح.

| Anti-Pattern | توضیح |
|--------------|-------|
| God Component | همه کار در یک کامپوننت → تقسیم |
| Logic in View | business logic در template → service/store |
| Prop Drilling | >3 سطح → Pinia |
| Direct Mutation | تغییر از بیرون → emit |

---

## ۱۵. Pinia — `state/pinia.mdc`

**محتوا:** defineStore، state، getters، actions؛ استفاده در کامپوننت.

| موضوع | توضیح |
|-------|-------|
| Store | defineStore با id |
| State | state reactive |
| Getters | computed در store |
| Actions | توابع async؛ mutations |

---

## ۱۶. Local vs Global — `state/local-vs-global.mdc`

**محتوا:** انتخاب بین state محلی و Pinia.

| معیار | Local | Global (Pinia) |
|-------|-------|----------------|
| Scope | یک کامپوننت | چند کامپوننت |
| Persistence | خیر | اختیاری |
| Rule | state نزدیک به مصرف‌کننده | shared state در store |

---

## ۱۷. Bundle Size — `performance/bundle-size.mdc`

**محتوا:** مدیریت حجم bundle، performance budget، code splitting، tree shaking.

| موضوع | توضیح |
|-------|-------|
| Budget | Initial JS <170KB؛ CSS <50KB |
| Code Splitting | lazy loading برای routes |
| Tree Shaking | import هدفمند |

---

## ۱۸. Core Web Vitals — `performance/core-web-vitals.mdc`

**محتوا:** LCP، FID، CLS — بهینه‌سازی و محدودیت‌ها.

| متریک | هدف |
|-------|-----|
| LCP | <2.5s |
| FID | <100ms |
| CLS | <0.1 |

---

## ۱۹. Optimization — `performance/optimization.mdc`

**محتوا:** Code splitting، lazy loading، memoization، virtualization.

| موضوع | توضیح |
|-------|-------|
| Lazy Loading | برای routes و components سنگین |
| Memoization | computed؛ shallowRef در صورت نیاز |
| Virtualization | برای لیست‌های بلند |

---

## ۲۰. Runtime — `performance/runtime.mdc`

**محتوا:** بهینه‌سازی runtime — virtual scrolling، debouncing، throttling، requestAnimationFrame.

| موضوع | توضیح |
|-------|-------|
| Debounce | برای input؛ search |
| Throttle | برای scroll؛ resize |
| Virtual Scroll | برای لیست‌های بزرگ |

---

## ۲۱. Asset Management — `performance/asset-management.mdc`

**محتوا:** تصاویر، فونت‌ها، آیکون‌ها؛ فرمت‌ها، lazy loading، caching.

| موضوع | توضیح |
|-------|-------|
| Images | WebP؛ lazy loading؛ srcset |
| Fonts | <100KB؛ font-display: swap |
| Icons | SVG sprite یا inline |

---

## ۲۲. Accessibility — `ui-ux/accessibility.mdc`

**محتوا:** WCAG 2.1 AA، semantic HTML، ARIA، keyboard، screen reader.

| موضوع | توضیح |
|-------|-------|
| Semantic | button نه div.button |
| ARIA | فقط وقتی semantic کافی نیست |
| Keyboard | Tab، Enter، Escape، Arrow |
| Contrast | حداقل 4.5:1 برای متن |

---

## ۲۳. Responsive Design — `ui-ux/responsive-design.mdc`

**محتوا:** Mobile-first، breakpoints، touch targets، responsive images.

| موضوع | توضیح |
|-------|-------|
| Mobile-First | Base بدون media query |
| Breakpoints | 640، 768، 1024 (min-width) |
| Touch | حداقل 44×44px |

---

## ۲۴. Styling — `ui-ux/styling.mdc`

**محتوا:** Scoped CSS، theme، design tokens، BEM.

| موضوع | توضیح |
|-------|-------|
| Scoped | styles scoped |
| Theme | CSS variables |
| BEM | Block__Element--Modifier |

---

## ۲۵. Interaction Patterns — `ui-ux/interaction-patterns.mdc`

**محتوا:** Form validation، optimistic UI، debouncing، throttling، animations، modal.

| موضوع | توضیح |
|-------|-------|
| Validation | real-time یا on blur |
| Optimistic | به‌روزرسانی UI قبل از پاسخ API |
| Modal | focus trap؛ Escape برای بستن |

---

## ۲۶. User Feedback — `ui-ux/user-feedback.mdc`

**محتوا:** Loading states، error handling، success feedback، skeleton، toast.

| موضوع | توضیح |
|-------|-------|
| Loading | spinner یا skeleton |
| Error | پیام واضح؛ راه حل |
| Success | toast یا inline |
| Skeleton | برای محتوای در حال بارگذاری |

---

## ۲۷. Testing Strategy — `testing/strategy.mdc`

**محتوا:** Test pyramid، coverage، Vitest، AAA pattern.

| موضوع | توضیح |
|-------|-------|
| Pyramid | Unit بیشتر؛ Integration متوسط؛ E2E کم |
| Vitest | برای unit و component |
| AAA | Arrange، Act، Assert |

---

## ۲۸. Unit Testing — `testing/unit-testing.mdc`

**محتوا:** Vitest، Vue Test Utils، تست کامپوننت و Pinia store.

| موضوع | توضیح |
|-------|-------|
| Vitest | test runner |
| Vue Test Utils | mount، wrapper |
| Component | props، events، slots |
| Pinia | mock یا createTestingPinia |

---

## ۲۹. E2E Testing — `testing/e2e-testing.mdc`

**محتوا:** تست E2E برای user flows حیاتی و visual regression.

| موضوع | توضیح |
|-------|-------|
| Critical Flows | login، checkout، … |
| Visual | regression testing |

---

## ۳۰. Vue 3 — `tools/vue.mdc`

**محتوا:** Vue 3 — script setup، Composition API، ساختار کامپوننت، JSDoc برای .js.

| موضوع | توضیح |
|-------|-------|
| Script Setup | defineProps، defineEmits |
| Composition API | ref، computed، watch |
| JSDoc | برای type hint در .js |

---

## ۳۱. Vite — `tools/vite.mdc`

**محتوا:** پیکربندی Vite و بهینه‌سازی برای frontend.

| موضوع | توضیح |
|-------|-------|
| Config | plugins، alias |
| Build | code splitting، minify |
| Dev | HMR |

---

## نحوهٔ استفاده

* **فایل‌های `.mdc`** در Cursor بر اساس globها اعمال می‌شوند.
* **این راهنما** برای مراجعه، آموزش و آشنایی با ساختار قوانین استفاده می‌شود.
* برای جزئیات و مثال‌های کد، به فایل `.mdc` مربوط مراجعه کن.
