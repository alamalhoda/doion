---
name: ai-studio-ui-fix-loop
description: >-
  Guides the Cursor↔Google AI Studio one-way UI fix loop for the active frontend
  (checkyar-googleai): diagnose Live API bugs, draft Studio prompts, wait for
  Studio GitHub commits, git pull locally, verify diffs against the prompt, and
  run smoke/manual checks. Use only when the user explicitly names this skill
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

- **Never** commit or push UI source from local/Cursor to `checkyar-googleai`.
- Active UI package manager: **Bun** only (`bun.lock`). Do not introduce `package-lock.json` in the UI repo.
- Live integration: UI `.env` must have `VITE_USE_MOCK=false` and `VITE_API_BASE_URL=http://localhost:8000/api/v1`.
- Backend/API contract fixes belong in **doion** (GitFlow). UI behavior/contract-client fixes go through **AI Studio prompts**.
- Header «نقش تست» only changes client role; JWT stays the same. For Live permission tests, require real login (`moderator1`, etc.).

## Roles

| Actor | Does |
|-------|------|
| User | Pastes prompt into AI Studio; pastes Studio reply + commit SHA into Cursor |
| Cursor (this skill) | Diagnose, draft prompt, pull, verify, test |
| AI Studio | Implements UI, runs its checks, pushes GitHub |

Cursor cannot talk to AI Studio directly.

## Workflow checklist

Copy and track:

```text
AI Studio UI fix loop:
- [ ] 1 Diagnose (layer + evidence)
- [ ] 2 Draft Studio prompt (or say backend-only)
- [ ] 3 User → Studio (clarify-then-implement)
- [ ] 4 User pastes Studio reply + commit SHA
- [ ] 5 git pull checkyar-googleai
- [ ] 6 Verify diff vs prompt
- [ ] 7 Smoke / manual Live check
- [ ] 8 Follow-up prompt if gaps remain
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
- Optional: “scan for the same class of bug elsewhere and fix those too”

Use the template in [prompt-template.md](prompt-template.md).

### 3) User → Studio

Tell the user to:

1. Paste only the prompt block into AI Studio.
2. Let Studio ask questions until clear.
3. Let Studio implement, run its tests (`tsc` / vitest as applicable), push GitHub.
4. Return to Cursor with: summary + **commit SHA**.

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
- Call out gaps explicitly; draft a **follow-up prompt** if needed.

### 6) Test

Prefer in order:

1. Targeted Playwright smoke under `doion/e2e/` when a scenario exists.
2. Manual Live path with seeded demo users (`seed_demo` / `DEMO_SEED_PASSWORD`).
3. Runbook: `docs/development/E2E_LOCAL_RUNBOOK.md`.

Backend for Live checks:

```bash
# from doion
./e2e/scripts/prepare-backend.sh   # when isolated demo DB needed
# runserver with DJANGO_DEMO_DATABASE=1
```

UI:

```bash
cd /path/to/checkyar-googleai
bun run dev   # prefer --host 127.0.0.1 if loopback issues
```

### 7) Close or loop

- If verified: short verdict + commit SHA + what was checked.
- If not: one concise follow-up Studio prompt; repeat from step 3.

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
- `docs/development/AI_STUDIO_E2E_PREP_PROMPT.md`
- `docs/development/BACKEND_DEMO_SEED_AND_DATA.md`
- `docs/development/MASTER_API_CONTRACT.md`
