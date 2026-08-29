# AI Studio prompt: bootstrap UI Architecture + Testing docs

Copy everything under **Prompt** into Google AI Studio so the active UI repo gains bilingual Architecture and Testing docs. Those files must be **committed and pushed from AI Studio** (one-way sync). After Studio pushes, `git pull` on the local `checkyar-googleai` clone.

Do **not** create or push these files from the local Cursor clone.

Prerequisite: none beyond a normal Studio session on `checkyar-googleai`.

---

## Prompt

```text
Context: Active UI repo checkyar-googleai (Bun lockfile only; no package-lock.json).
Live API against doion: VITE_USE_MOCK=false, VITE_API_BASE_URL=http://localhost:8000/api/v1.
Do NOT change backend. Documentation-only task (plus tiny README links). No feature refactors.
Before coding: list any ambiguities and ask me questions until the instructions are fully clear.

## Goal
Create the first bilingual documentation set for this UI repo so future fixes can update the same files instead of inventing new doc trees.

## Required files (create if missing)

1) docs/ARCHITECTURE.md (English SSOT for UI architecture)
2) docs/ARCHITECTURE.fa.md (Persian — same structure, concise)
3) docs/TESTING.md (English SSOT for how to test this UI)
4) docs/TESTING.fa.md (Persian — same structure, concise)
5) README.md — add a short “Documentation” section with links to the four files above; do not duplicate their full content

Keep docs short and practical. Prefer accurate current structure under src/ over aspirational design.

## ARCHITECTURE.md / ARCHITECTURE.fa.md — required sections

- Purpose of this repo (active Cheque Yar UI)
- One-way sync diagram in text:
  Google AI Studio --push--> GitHub checkyar-googleai --> local git pull only
  (local/Cursor must not commit/push UI source)
- Stack: Vue 3, TypeScript, Naive UI, Pinia, Vue Router, Vite, Bun
- Layer map (match real folders):
  - src/api — HTTP client, Live vs mock
  - src/features — feature modules
  - src/stores — Pinia
  - src/router — routes and guards
  - src/shared — shared UI
- Mock vs Live: VITE_USE_MOCK, VITE_API_BASE_URL; note that header «نقش تست» is client role only (JWT unchanged)
- Boundaries: API contract and Django live in doion (link conceptually to alamalhoda/doion MASTER_API_CONTRACT); do not paste backend architecture here
- Package manager: Bun + bun.lock only; no package-lock.json

## TESTING.md / TESTING.fa.md — required sections

- Unit tests: bun run test / bun run test:watch (Vitest); what kinds of logic are unit-tested today
- Lint / typecheck commands actually present in package.json
- Manual Live check: VITE_USE_MOCK=false against doion on localhost:8000; seed demo users conceptually (holder1 / investor1 / moderator1) without inventing passwords
- Clarify: in-app Mock/Simulator is for UI demos — not a substitute for Live contract testing
- Live browser E2E (Playwright smoke/critical) lives in the doion monorepo under e2e/ — document that ownership and tell readers to use doion’s E2E_LOCAL_RUNBOOK; do NOT copy Playwright suites into this repo
- data-testid: prefer kebab-case; for Naive NInput use :input-props so the native input gets the testid
- When changing behavior: update related vitest here; doion owns Playwright updates

## Do not
- Commit package-lock.json / switch package manager
- Refactor application code unrelated to docs
- Invent Django endpoints or duplicate MASTER_API_CONTRACT
- Add Playwright / e2e/ folders to this UI repo
- Write huge encyclopedic docs — keep each file scannable

## Acceptance
- All four docs files exist with the sections above
- README links to them
- EN and FA cover the same topics (FA may be slightly shorter)
- bun lockfile unchanged; no accidental package-lock.json
- In your reply: list created/updated paths and commit after push
```

---

## After Studio push

```bash
cd /path/to/checkyar-googleai
git fetch origin
git pull origin main
git show --stat <commit-sha>
# confirm docs/ARCHITECTURE.md, docs/ARCHITECTURE.fa.md,
# docs/TESTING.md, docs/TESTING.fa.md, and README links
```

## Related

- Loop skill: `.cursor/skills/ai-studio-ui-fix-loop/`
- One-way policy: [`FRONTEND_DEVELOPMENT_STATUS.md`](./FRONTEND_DEVELOPMENT_STATUS.md)
- doion E2E runbook: [`E2E_LOCAL_RUNBOOK.md`](./E2E_LOCAL_RUNBOOK.md)
