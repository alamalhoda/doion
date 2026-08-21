# پرامپت ۰۶ — اصلاح CD Product: CLI چابکان `chabok.json` را بر `-s` اولویت می‌دهد

Follow-up Step 12. مرجع: لاگ [CD Product run 32469027546](https://github.com/alamalhoda/checkyar-googleai/actions/runs/32469027546) خط `Uploading … to chequeyar-front-demo` / `Deployed to chequeyar-front-demo`.

کد CLI (`deploy.ts`): اگر `chabok.json` فیلد `service` داشته باشد، **جایگزین** `--service` / `-s` می‌شود. فایل ریپو `chequeyar-front-demo` است؛ پس `-s chequeyar-front` بی‌اثر بود. Job سبز شد چون دمو واقعاً deploy شد.

## قاعده اجرا

فقط در Google AI Studio روی `checkyar-googleai`. از Cursor به این ریپو پوش نکنید. فقط بلوک `text` را پیست کنید.

## کار مالک بعد از پوش

1. SHA را در چت Cursor بگذار.
2. PR `main` → `product` (مثل قبل).
3. **CD Demo** را یک‌بار بزن یا صبر کن push بعدی به `main` دموی mock را برگرداند (CD Product اشتباه باندل زنده را روی دمو گذاشته).
4. بعد از merge به `product`، **CD Product** را دوباره روی `product` بزن و در لاگ باید `Deployed to chequeyar-front` باشد (نه `front-demo`).
5. در پنل [استقرارهای chequeyar-front](https://hub.chabokan.net/fa/services/detail/WxWBVMz/deploys/) باید یک استقرار جدید دیده شود.

---

```text
Goal: fix CD Product so it deploys to Chabokan service chequeyar-front, not chequeyar-front-demo. The Chabokan CLI ignores -s when chabok.json has a "service" field; that file must stay chequeyar-front-demo for demo CD. On the GitHub Actions runner only, rewrite chabok.json to {"service":"chequeyar-front"} immediately before `chabok deploy`. Do not commit a product service name into chabok.json. Do not change Vue app code.

Before coding: if cd-product.yml already writes {"service":"chequeyar-front"} into chabok.json on the runner before deploy, and the committed chabok.json is still chequeyar-front-demo, and cd-demo.yml is untouched, stop and say so.

## Bug (do not regress)

Committed `chabok.json` is `{"service":"chequeyar-front-demo"}`. Official CLI deploy.ts does: if chabok.json.service is set, selected_service = that value (flags.service is overwritten). Run 32469027546 logged: "Uploading 1.6 MB to chequeyar-front-demo" then "Deployed to chequeyar-front-demo." GitHub job was green. Panel for chequeyar-front (WxWBVMz) had no new CLI deploy.

## Required change

Edit only `.github/workflows/cd-product.yml` deploy step, after login, before deploy. Example (keep secret handling and dist gitignore strip):

```
chabok login -t "$CHABOKAN_TOKEN"
printf '%s\n' '{"service":"chequeyar-front"}' > chabok.json
chabok deploy -s chequeyar-front
```

The printf is on the runner workspace only; it is not a git commit. Do not change the committed `chabok.json` file.

Optional: echo a line like "chabok.json service overridden to chequeyar-front for this job" so the log is obvious.

## Do not

- Edit `.github/workflows/cd-demo.yml`, `ci.yml`, `dispatch-doion-e2e.yml`.
- Change committed `chabok.json` to chequeyar-front (that would break demo CD).
- Change Vue, env URLs, or docs except one sentence in TESTING.md / TESTING.fa.md: CD Product must override chabok.json on the runner because CLI prefers that file over -s.
- package-lock.json, npm as app package manager.
- Click Run workflow yourself.

## Done when

- cd-product.yml overrides chabok.json on the runner.
- Committed chabok.json still names chequeyar-front-demo.
- cd-demo.yml byte-for-byte unchanged (or you report the diff).
- Pushed to main from Studio. Paste the commit SHA.
```
