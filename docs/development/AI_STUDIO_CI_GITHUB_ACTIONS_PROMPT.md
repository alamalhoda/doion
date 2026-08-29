# AI Studio prompt: GitHub Actions CI for checkyar-googleai

Copy everything under **Prompt** into Google AI Studio so the active UI repo gets a minimal GitHub Actions CI workflow. Those files must be **committed and pushed from AI Studio** (one-way sync). After Studio pushes, `git pull` on the local `checkyar-googleai` clone.

Do **not** create or push these files from the local Cursor clone.

Prerequisite: none beyond a normal Studio session on `checkyar-googleai`.

After Studio pushes, open the repo Actions tab on GitHub and confirm the workflow runs green on `main`.

---

## Prompt

```text
Context: Active UI repo checkyar-googleai (Bun lockfile only; no package-lock.json).
One-way sync: you (AI Studio) push to GitHub; local/Cursor must not push UI source.
Do NOT change backend (doion). Do NOT add Playwright. Do NOT change application logic under src/.
Do NOT add new unit tests in this task — existing vitest files are enough for CI bootstrap.
Before coding: list any ambiguities and ask me questions until the instructions are fully clear.

## Goal
Add GitHub Actions CI so every push and pull_request to `main` runs:
1) Typecheck (lint)
2) Unit tests
3) Production build

## Required files

1) Create `.github/workflows/ci.yml` with this behavior:
   - name: CI
   - on:
       push:
         branches: [main]
       pull_request:
         branches: [main]
   - jobs:
       one job on ubuntu-latest named roughly "lint-test-build"
       steps:
         - actions/checkout@v4
         - setup Bun (oven-sh/setup-bun@v2 is fine; use latest stable Bun)
         - bun install --frozen-lockfile
         - bun run lint
         - bun run test
         - bun run build
   - Do not deploy. Do not publish. Do not cache beyond what setup-bun provides by default.
   - Do not introduce npm/yarn/pnpm. Do not create package-lock.json.

2) Docs (minimal):
   - In docs/TESTING.md and docs/TESTING.fa.md, add a short section “CI (GitHub Actions)” stating that on push/PR to main, GitHub Actions runs `bun run lint`, `bun run test`, and `bun run build` via `.github/workflows/ci.yml`. Point E2E readers to doion `e2e/` still.
   - In README.md, add one short bullet or sentence under Documentation/Testing that CI runs on main (link to the workflow file). Do not duplicate full TESTING content.

## Hard constraints
- No edits to Vue/TS feature code under src/ except if a typo in docs references only.
- No new *.test.ts files.
- No Playwright config or e2e folder in this repo.
- Keep the workflow YAML simple and readable.
- After creating files, summarize exactly which files changed.

## Done when
- `.github/workflows/ci.yml` exists
- TESTING.md / TESTING.fa.md / README mention CI briefly
- Locally equivalent commands still are: bun install && bun run lint && bun run test && bun run build
- Commit and push from AI Studio to GitHub
```
