# پرامپت ۰۷ — nginx چابکان Vue: `root` باید `/app/dist` باشد نه مسیر Docker

لاگ `chabok service logs -s chequeyar-front` (۲۰۲۶-۰۸-۲۱ ~۱۷:۵۲): استقرار به سرویس درست رسید (`npm ci`، `vite build`، `Copy Nginx Configuration`، `Starting nginx`). سپس `GET /login` با **HTTP 500**.

علت محتمل: فایل ریشهٔ `nginx.conf` برای ایمیج Docker نوشته شده (`root /usr/share/nginx/html/dist`). چابکان Vue فایل را کپی می‌کند و فایل‌های بیلد روی **`/app/dist`** هستند ([مستند nginx Vue](https://docs.chabokan.net/cloud-hosting/vue/nginx-config/)). nginx به مسیر Docker نگاه می‌کند → ۵۰۰.

## قاعده اجرا

فقط Google AI Studio روی `checkyar-googleai`. از Cursor پوش نکنید. فقط بلوک `text`.

## کار مالک

بعد از پوش: PR `main` → `product`، سپس CD Product روی `product`. `/login` باید ۲۰۰ و SPA باشد نه ۵۰۰. در پنل سرویس Vue متغیرهای بیلد `VITE_USE_MOCK=false` و `VITE_API_BASE_URL=https://chequeyar-back.chbkn.dev/api/v1` را ست کنید؛ چابکان روی سرور دوباره `npm run build` می‌زند و env گیت‌هاب Actions را به آن بیلد منتقل نمی‌کند.

---

```text
Goal: stop Chabokan Vue PaaS from using the Docker nginx.conf document root. Chabokan Vue default root is /app/dist. This repo's nginx.conf uses /usr/share/nginx/html/dist for the nginx:alpine image. After CLI deploy, logs show Copy Nginx Configuration then GET /login returns HTTP 500. Do not change Vue views. Do not change cd-demo.yml.

Before coding: if .chabokignore already lists nginx.conf (so PaaS uses platform default /app/dist + try_files) AND Dockerfile still COPY nginx.conf to nginx:alpine with dist at /usr/share/nginx/html/dist, stop and say so.

## Required

1. Add `nginx.conf` to `.chabokignore` (committed). Chabokan then keeps its Vue default:
   root /app/dist; try_files $uri $uri/ /index.html =404;
   Docker image is unchanged: Dockerfile still uses nginx.conf.

2. Docs EN+FA (ARCHITECTURE and/or TESTING): one sentence that PaaS Vue host ignores this repo nginx.conf via .chabokignore because Docker root path is different from /app/dist. Mention panel env VITE_USE_MOCK=false and VITE_API_BASE_URL=https://chequeyar-back.chbkn.dev/api/v1 because Chabokan runs npm run build on the server.

## Do not

- Change committed nginx.conf Docker root unless you also change Dockerfile in the same commit (prefer .chabokignore).
- Edit cd-demo.yml, ci.yml, dispatch-doion-e2e.yml, cd-product.yml unless a one-line comment is needed.
- package-lock.json as app lockfile of record.
- Click Run workflow.

## Done when

- .chabokignore contains nginx.conf
- Dockerfile + nginx.conf Docker paths unchanged
- Pushed to main; paste SHA
```
