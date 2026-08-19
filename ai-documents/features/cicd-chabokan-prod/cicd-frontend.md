# cicd-frontend — قرارداد فرانت برای AI Studio

SSOT رفتار: [`feature_spec.md`](./feature_spec.md). این فایل فقط برش فرانت است تا پرامپت‌های Studio از روی آن ساخته شوند.

## قیود قطعی

- ریپو: `checkyar-googleai`
- Package manager: Bun (`bun.lock`). `package-lock.json` ساخته نشود.
- از Cursor به این ریپو commit/push نشود.
- Studio به `main` پوش می‌کند؛ PR روزانه الزامی نیست.
- شاخهٔ تولید: `product`. استقرار `chequeyar-front` از `product` است نه از `main` خام.
- `chequeyar-front-demo` و CD mock دست‌نخورده بماند.
- Docker Compose لوکال برای همکار اختیاری است؛ توسعه بدون Docker همچنان معتبر است.
- دادهٔ محصول و تست CI بک‌اند Postgres است؛ این ریپو UI دیتابیس محصول را عوض نمی‌کند.

## تست اجباری CI روی `main` و روی PR به `product`

1. typecheck (`tsc --noEmit`)
2. unit tests (Vitest)
3. production build پیش‌فرض
4. production build جدا با `VITE_USE_MOCK=false` و `VITE_API_BASE_URL=https://chequeyar-back.chbkn.dev/api/v1`

## انتشار محصول (نسخهٔ کامل ویژگی؛ نه گام اول CI)

- ایمیج Docker فرانت با تگ SemVer همان GitHub Release
- deploy فقط پس از PR سبز `main` → `product` و تأیید مالک
- شکست deploy: Check قرمز؛ بازیابی با deploy دستی آخرین انتشار موفق

## پرامپت‌ها

پس از تأیید plan، Chat 2 فایل‌ها را در `prompts/` می‌سازد:

- `01-ci-live-build.md` — Step 2
- `02-dispatch-doion-e2e.md` — Step 5
- `03-frontend-docker.md` — Step 8
- `04-product-branch.md` — Step 9
- `05-cd-product-front.md` — Step 12
