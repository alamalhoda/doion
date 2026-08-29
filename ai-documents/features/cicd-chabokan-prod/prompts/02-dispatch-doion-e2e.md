# پرامپت ۰۲ — تریگر E2E دویون بعد از CI سبز روی `main`

خروجی Step 5 از [`implementation_plan.md`](../implementation_plan.md). مرجع رفتار: [`feature_spec.md`](../feature_spec.md) سناریو ۷ و قوانین ۴، ۸، ۱۸، ۲۳، ۲۴؛ برش فرانت: [`cicd-frontend.md`](../cicd-frontend.md). قرارداد دریافت در دویون: `.github/workflows/ci-e2e.yml` رویداد `repository_dispatch` با type‏ `frontend-e2e` و `client_payload.ui_sha`.

## قاعده اجرا

این متن **فقط در Google AI Studio** روی ریپوی فعال UI (`checkyar-googleai`) اجرا می‌شود. از Cursor یا کلون لوکال روی این ریپو commit/push نکنید.

فقط بلوک `text` پایین را در Studio بچسبانید.

## کار مالک قبل از Verify (Studio این راز را نمی‌سازد)

GitHub `GITHUB_TOKEN` این ریپو نمی‌تواند به ریپوی دیگر `repository_dispatch` بزند.

1. یک PAT بسازید که فقط به `alamalhoda/doion` دسترسی دارد:
   - Fine-grained: Contents = Read and write روی `doion` (Metadata خودکار می‌آید)
   - یا Classic: چون `doion` عمومی است، scope‏ `public_repo` کافی است (`repo` لازم نیست مگر بعداً خصوصی شود)
2. در `checkyar-googleai` → Settings → Secrets and variables → Actions یک Repository secret بگذارید:
   - نام دقیق: `DOION_E2E_DISPATCH_TOKEN`
   - مقدار: همان PAT
3. `CHABOKAN_TOKEN` را برای این کار دوباره استفاده نکنید.

بدون این secret، job تریگر باید قرمز شود (نه skip خاموش).

## پیش‌نیاز دویون (خارج از این پرامپت)

`repository_dispatch` فقط workflow روی **شاخهٔ پیش‌فرض** هدف را اجرا می‌کند. پیش‌فرض `doion` الان `develop` است. فایل `ci-e2e.yml` با type‏ `frontend-e2e` باید روی `develop` باشد وگرنه پوش Studio رویدادی می‌فرستد که job E2E را راه نمی‌اندازد. bump پین YAML کار این پرامپت نیست (گام ۶ دویون).

## پوشش این پرامپت

بعد از موفقیت workflow موجود `CI` روی **push به `main`**، یک رویداد به `alamalhoda/doion` با SHA همان commit فرانت بفرست.

خارج از این گام: شاخهٔ `product`، Docker، deploy محصول، تغییر `cd-demo.yml`، تغییر چهار گام CI موجود، Playwright داخل این ریپو.

## تصمیم‌های قفل‌شده

- Package manager: Bun (`bun.lock`). `package-lock.json` ساخته نشود.
- `.github/workflows/cd-demo.yml` دست نخورده بماند.
- چهار گام `ci.yml` (lint، test، build پیش‌فرض، build زنده) سر جایشان بمانند و به‌خاطر شکست E2E دویون قرمز نشوند.
- مقدار PAT/secret در YAML یا docs hard-code نشود.
- اکشن سوم‌شخص جدید برای dispatch لازم نیست؛ `curl` به GitHub API کافی است.

---

```text
Goal: after the existing GitHub Actions workflow named "CI" succeeds on a push to main, send a repository_dispatch to alamalhoda/doion so Playwright E2E there runs against THIS commit SHA. Do not add product deploy, Docker, a product branch, or Playwright tests in this repo. Do not change the four existing CI verification steps.

Before coding: if `.github/workflows/dispatch-doion-e2e.yml` (or equivalent) already posts event_type `frontend-e2e` with client_payload.ui_sha set to the successful CI head SHA after CI on main push, and `ci.yml` plus `cd-demo.yml` are unchanged, stop and say so.

## Context

- This repo is the active Cheque Yar UI: Vue 3 + TypeScript + Vite + Naive UI + Pinia. Bun lockfile only (`bun.lock`). Never create or commit `package-lock.json`.
- Studio pushes to `main`. Daily PRs are not required.
- Playwright lives only in the Django monorepo `alamalhoda/doion` (workflow "CI E2E Playwright"). Do NOT add Playwright here. Do NOT edit doion.
- E2E in doion is not a merge gate for backend PRs. This repo must not wait for doion E2E to finish and must not fail the "CI" check if doion E2E later fails.
- Hosted mock demo CD must keep working unchanged.

## Current CI (do not drop or reorder)

`.github/workflows/ci.yml` today:

- name: CI
- on: push and pull_request to `main`
- job `lint-test-build`: checkout, setup Bun, `bun install --frozen-lockfile`, `bun run lint`, `bun run test`, `bun run build`, then live build with `VITE_USE_MOCK=false` and `VITE_API_BASE_URL=https://chequeyar-back.chbkn.dev/api/v1`

Keep that file's four verification steps exactly. Do not add the dispatch as a step or job inside `ci.yml` (a missing PAT or a doion outage must not turn the four-step CI check red).

## Required changes

1. New workflow file `.github/workflows/dispatch-doion-e2e.yml` (this name is preferred).
   - Trigger with `workflow_run`: workflows `["CI"]`, types `[completed]`, branches `[main]`.
   - Job runs only when ALL of these are true:
     - `github.event.workflow_run.conclusion == 'success'`
     - `github.event.workflow_run.event == 'push'` (do not dispatch after a pull_request CI run)
   - One step: HTTP POST `https://api.github.com/repos/alamalhoda/doion/dispatches`
     - Header `Accept: application/vnd.github+json`
     - Header `Authorization: Bearer ${{ secrets.DOION_E2E_DISPATCH_TOKEN }}` (via env, never echo the token)
     - Header `X-GitHub-Api-Version: 2022-11-28`
     - JSON body exactly:
       `{"event_type":"frontend-e2e","client_payload":{"ui_sha":"<sha>"}}`
     - `<sha>` MUST be `github.event.workflow_run.head_sha` (the UI commit that CI just verified). Do not use a branch name. Do not omit ui_sha (doion fails closed if it is missing).
   - Use `curl` on `ubuntu-latest`. Do not add a third-party dispatch Action.
   - If `DOION_E2E_DISPATCH_TOKEN` is empty, fail the job with a short message that the owner must add that Actions secret (a PAT that can POST repository_dispatch to alamalhoda/doion). Do not skip success.
   - Validate the SHA is 40 hex characters before POST.
   - Do not print the secret. Logging the SHA is fine.

2. `.github/workflows/ci.yml`
   - Do not edit this file at all unless you must fix a workflow name mismatch; the `workflow_run` filter must match the workflow `name:` which is `CI`.

3. `.github/workflows/cd-demo.yml`
   - Do not edit this file at all.

4. Docs (this repo only, EN+FA, same commit as the workflow)
   - `docs/TESTING.md` and `docs/TESTING.fa.md`: after the four CI steps, add a short note: on successful CI for a push to `main`, this repo dispatches doion E2E with that commit SHA; the Playwright result appears in doion Actions, not as a required check in this repo; owner must set secret `DOION_E2E_DISPATCH_TOKEN` (no token value in docs). Keep Playwright-lives-in-doion. Keep cd-demo mock note.
   - `docs/ARCHITECTURE.md` and `docs/ARCHITECTURE.fa.md`: one short sentence that a green CI push to `main` notifies doion to run E2E against that SHA. No Django internals.
   - README.md: only if it already describes CI; then one sentence. No long new guide.

## Owner secret (document the name only)

Secret name is locked: `DOION_E2E_DISPATCH_TOKEN` on this repo.
Do not invent a second name. Do not put a token in git. Do not reuse `CHABOKAN_TOKEN`.
You cannot create GitHub secrets from this prompt; if the first run fails because the secret is missing, say so clearly.

Token shape for the human owner (docs may repeat this without a sample token):
- Fine-grained PAT on `alamalhoda/doion` with Contents: Read and write
- or classic PAT with `public_repo` (doion is public)

## Do not

- Touch `cd-demo.yml`, Chabokan deploy, or `chequeyar-front-demo`.
- Create branch `product`, Dockerfile, compose, SemVer, or product CD (later prompts).
- Change Vue, API client, mock gating, or the four CI commands.
- `package-lock.json`, npm as app package manager, new dependencies.
- Unrelated refactors.
- Playwright in this repo.
- Dispatch on pull_request-only CI, or dispatch when CI failed.
- Try to bump doion's YAML UI pin (that is a later doion PR).
- Hard-code any PAT, password, or token.

## Acceptance

- Push to `main` still shows the same four CI steps in workflow `CI`.
- After that workflow succeeds on a `push` to `main`, workflow `dispatch-doion-e2e` (or the name you chose) runs and POSTs `frontend-e2e` with `ui_sha` equal to that push SHA.
- `cd-demo.yml` is byte-for-byte unchanged.
- Failed doion E2E does not fail this repo's `CI` job (separate workflow).
- Missing `DOION_E2E_DISPATCH_TOKEN` fails the dispatch workflow, not silently skipped.

## After you finish

Commit: `ci: dispatch doion E2E after green CI on main`

Reply with: commit SHA, files changed, whether ci.yml and cd-demo.yml were untouched, and that the secret is named `DOION_E2E_DISPATCH_TOKEN` with no value in git.
```
