---
name: ai-studio-ui-fix-loop
description: >-
  Guides the Cursor↔Google AI Studio one-way UI fix loop for the active frontend
  (checkyar-googleai): diagnose Live API bugs, draft Studio prompts that cover
  code + UI unit tests + UI docs, wait for Studio GitHub commits, git pull
  locally, verify diffs, keep doion E2E specs in sync when needed, and run a
  proportionate Live check. Use only when the user explicitly names this skill
  or asks to run the AI Studio UI fix loop.
disable-model-invocation: true
---

# AI Studio UI Fix Loop

One-way sync policy SSOT: `docs/development/FRONTEND_DEVELOPMENT_STATUS.md`.

```text
[Google AI Studio]  --push-->  github.com/alamalhoda/checkyar-googleai
                                        |
                                        v  (git pull only)
                                 local clone + doion backend / e2e
```

## Hard rules

- **Never** commit or push UI source (code, vitest, or UI docs) from local/Cursor to `checkyar-googleai`.
- Active UI package manager: **Bun** only (`bun.lock`). Do not introduce `package-lock.json` in the UI repo.
- Live integration: UI `.env` must have `VITE_USE_MOCK=false` and `VITE_API_BASE_URL=http://localhost:8000/api/v1`.
- Backend/API contract fixes belong in **doion** (GitFlow). UI behavior/contract-client fixes go through **AI Studio prompts**.
- Header «نقش تست» only changes client role; JWT stays the same. For Live permission tests, require real login (`moderator1`, etc.).
- **Tests (one-way split):** UI unit/`tsc`/vitest → only via Studio prompts → GitHub → pull. Playwright smoke/critical → only in `doion/e2e/` (GitFlow). Missing `data-testid` → Studio follow-up prompt; never edit UI locally for selectors.
- **Docs (one-way):** UI Architecture + Testing docs (EN+FA) are authored in AI Studio and arrive via pull. Prompts must ask Studio to create/update them when behavior changes. Do not invent doion/backend docs inside the UI repo — link out.
- Keep test/doc work proportionate: skip both for cosmetic-only fixes.
- **Never** `git tag` / `git push` tags on `checkyar-googleai` from Cursor. Product SemVer is the doion workflow **Release** (same `v*` for API + SPA images). See `.cursor/skills/semver-release/SKILL.md`.

## Roles

| Actor | Does |
|-------|------|
| User | Pastes prompt into AI Studio; pastes Studio reply + commit SHA into Cursor |
| Cursor (this skill) | Diagnose, draft prompt, pull, verify, doion E2E, short status |
| AI Studio | Implements UI, vitest/`tsc`, UI docs (EN+FA), pushes GitHub |

Cursor cannot talk to AI Studio directly.

## Workflow checklist

Copy and track:

```text
AI Studio UI fix loop:
- [ ] 1 Diagnose (layer + evidence)
- [ ] 2 Draft Studio prompt (code + tests ask + docs ask when needed)
- [ ] 3 User → Studio (clarify-then-implement)
- [ ] 4 User pastes Studio reply + commit SHA
- [ ] 5 git pull checkyar-googleai
- [ ] 6 Verify diff (code + UI tests + UI docs)
- [ ] 7 Sync doion E2E if needed → run checks → short status
- [ ] 8 Follow-up prompt if gaps remain (incl. missing docs)
- [ ] 9 Tag/changelog reminder if user-visible and heading to `product`
```

### 1) Diagnose

1. Reproduce with Live API when the bug is Live-specific.
2. Classify layer:
   - **Backend** (wrong status/shape/permission in Django) → fix in `doion`, no Studio prompt.
   - **UI client** (pagination unwrap, selectors, mock/Live mismatch) → Studio prompt.
   - **Usage** (wrong user, mock on, role switcher) → explain; no code change.
3. Prefer evidence: failing URL, response shape (`{results:[]}` vs array), status code, console error.
4. Contract SSOT: `docs/development/MASTER_API_CONTRACT.md`.

### 2) Draft Studio prompt

Output a single fenced `text` block the user can paste into Studio.

Must include:

- Goal + observed symptom
- Root cause (with endpoint/file hints when known)
- Explicit file/API touch list when known
- Do / Do not (Bun, no package-lock, no unrelated refactors, no backend edits)
- **Ask clarifying questions before implementing if anything is ambiguous**
- Acceptance checks (pages, users, Live mock off)
- **Tests ask** (when behavior/logic changes): update/add vitest in UI repo; do not invent Playwright in UI repo
- **Docs ask** (when behavior/modules change): update Architecture + Testing EN/FA in UI repo — see template
- **Changelog seed** (when an end user would notice the change): ask Studio for 1–3 short FA+EN bullets; do not build a versions page unless the user asked for that feature
- Optional: “scan for the same class of bug elsewhere and fix those too”

Use the template in [prompt-template.md](prompt-template.md).

First-time UI docs scaffold (paste once if `docs/ARCHITECTURE*.md` / `docs/TESTING*.md` missing):  
`docs/development/AI_STUDIO_DOCS_BOOTSTRAP_PROMPT.md`.

### 3) User → Studio

Tell the user to:

1. Paste only the prompt block into AI Studio.
2. Let Studio ask questions until clear.
3. Let Studio implement, run vitest/`tsc`, update UI docs when asked, push GitHub.
4. Return to Cursor with: summary (code + tests + docs paths) + **commit SHA**.

Do not proceed to pull until the user provides the commit (or confirms push landed on `main`).

### 4) Pull local UI

```bash
cd /path/to/checkyar-googleai
git fetch origin
git pull origin main
git show --stat <commit-sha>
```

Confirm HEAD contains the reported commit.

### 5) Verify against the prompt

- Diff matches requested files/behaviors.
- No forbidden changes (lockfile drift, drive-by refactors).
- Spot-check critical code paths (e.g. `unwrapList`, `data-testid` on native inputs via `input-props`).
- If behavior changed: UI docs touched (or Studio said `docs: none` with a valid cosmetic reason).
- Prefer `docs/ARCHITECTURE.md` + `.fa.md` and `docs/TESTING.md` + `.fa.md` when present.
- Call out gaps explicitly; draft a **follow-up prompt** if needed (including missing docs) — do not fix UI docs locally and push.

### 6) Test

Goal: enough confidence that the fix works Live — not full regression every time.

#### One-way ownership (do not blur)

| Layer | Where | Who changes it |
|-------|--------|----------------|
| Vitest / `tsc` / UI test docs | `checkyar-googleai` | AI Studio → GitHub → local pull only |
| Playwright smoke/critical | `doion/e2e/` | Cursor / GitFlow in this monorepo |
| Stable selectors (`data-testid`) | UI source | Studio prompt only |

#### Keep tests aligned (lightweight)

After the diff looks right:

1. If an existing smoke/critical spec covers the flow and selectors or expected UI changed → **update** that spec in `doion/e2e/` (GitFlow).
2. If Studio added/changed a real user flow with no coverage → **add** one focused Playwright spec in doion (prefer `tests/critical/` for mutations) and ask Studio for any missing `data-testid` via follow-up. Do **not** edit UI locally.
3. Cosmetic / copy-only / tiny wiring with no behavior risk → skip new tests; a quick manual Live check is enough.
4. Do not weaken assertions just to green a broken UI.
5. UI vitest gaps → follow-up Studio prompt (not local commit to the UI repo).

#### What to run (pick what fits)

| Situation | Prefer |
|-----------|--------|
| Existing smoke/critical covers the change | That suite (or a single spec path) |
| New critical mutation / new page | Add/update critical spec in doion, then run it |
| No E2E yet / tiny fix | Manual Live with seeded user |
| Studio touched pure logic (composable/util) | Trust Studio vitest/`tsc` if they reported pass; re-run locally only if doubtful |

Commands when Live E2E is warranted:

```bash
# from doion — re-seed when critical specs mutate demo data
./e2e/scripts/prepare-backend.sh
# backend: DJANGO_DEMO_DATABASE=1 + runserver

cd /path/to/checkyar-googleai && bun run dev

cd doion/e2e
./scripts/run-smoke.sh      # or a single smoke file
./scripts/run-critical.sh   # when critical path is in scope
```

Runbook: `docs/development/E2E_LOCAL_RUNBOOK.md`.

#### Short status (before close)

```text
Test: <smoke | critical | manual | skipped-cosmetic>
Docs: <updated in UI commit | none-cosmetic | missing→follow-up>
Changelog: <bullets saved | none-cosmetic | missing→ask>
Tag: <not-needed | remind-Release | user-declined>
Result: PASS | FAIL
Notes: <what ran / what failed / follow-up if any>
```

On FAIL: fix via Studio follow-up or doion harness/seed — then re-check the failing part only.

### 7) Close or loop

- If verified: short verdict + commit SHA + test/docs status above.
- If not: one concise follow-up Studio prompt; repeat from step 3.

### 8) Frontend tagging and in-app changelog (when useful)

Daily Studio pushes to `main` are **not** tagged. Cursor does not tag the UI repo.

**When to remind (one question, same tone as backend):**

- User-visible feat/fix is on `main` **and** they merged (or are about to merge) `main` → `product`
- They talk about shipping SPA, `chequeyar-front`, or a numbered version
- Cosmetic-only / docs-only / CI-only UI: do **not** remind

**What to remind:** run doion skill `semver-release` so API + SPA share one `v*` (SPA image is built from `e2e/ui-pin`; bump that pin first if this UI SHA is not pinned yet). Do not `git tag` on `checkyar-googleai`.

**Changelog seed:** keep Studio’s FA+EN bullets. Future in-app “what’s new” (server + client, version, date, summary) is specified in `docs/development/PRODUCT_CHANGELOG.md`. Do not implement that page in a routine fix prompt. When a Release is cut, those bullets belong in the GitHub Release notes (and later the changelog API).

## Common bug classes (hints)

| Symptom | Likely cause |
|---------|----------------|
| `.filter is not a function` / `null.id` on lists | Paginated `{results}` assigned as array |
| 403 on `/moderation` | Not logged in as `moderator1`, or role-switcher only |
| Login form not reachable Live | `loadSavedUser` mock seed when mock off |
| Playwright cannot `fill` testid | `data-testid` on Naive `NInput` root instead of `:input-props` |

## Related docs

- `docs/development/FRONTEND_DEVELOPMENT_STATUS.md`
- `docs/development/E2E_LOCAL_RUNBOOK.md`
- `docs/development/AI_STUDIO_DOCS_BOOTSTRAP_PROMPT.md`
- `docs/development/AI_STUDIO_E2E_PREP_PROMPT.md`
- `docs/development/AI_STUDIO_E2E_CRITICAL_PATH_PROMPT.md`
- `docs/development/BACKEND_DEMO_SEED_AND_DATA.md`
- `docs/development/MASTER_API_CONTRACT.md`
- `docs/development/PRODUCT_CHANGELOG.md`
- `docs/development/GIT_TAGS_AND_RELEASES.md`
- `.cursor/skills/semver-release/SKILL.md`
