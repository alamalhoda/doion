# AI Studio prompt template

Paste the fenced block into Google AI Studio. Adjust the sections in braces.

```text
Context: Active UI repo checkyar-googleai (Bun lockfile only; no package-lock.json).
Live API against doion: VITE_USE_MOCK=false, VITE_API_BASE_URL=http://localhost:8000/api/v1.
Do NOT change backend. Small targeted UI fix only.
If anything is ambiguous, ask clarifying questions BEFORE implementing.

## Symptom
{What the user sees: page URL, popup/console error, role used}

## Root cause
{Evidence: endpoint + response shape, or code path. Be specific.}

## Required changes
1) {File + behavior}
2) {File + behavior}

## Same-class scan (optional but preferred for systemic bugs)
Search src/ for the same pattern and fix other Live call sites too.
Report every extra site you fixed.

## Tests (this UI repo only)
- If you changed tested logic: update existing vitest; add a small unit test only for new non-trivial logic.
- Run tsc / relevant vitest and mention results briefly in your reply.
- Do NOT add Playwright or doion e2e suites here. Live browser E2E lives in the doion monorepo.
- If you add/change data-testid used by E2E, list the exact kebab-case strings in your reply.

## Documentation (this UI repo only — commit with the code)
Bilingual EN + FA. Skip when the change is purely cosmetic (say docs: none).

Update only sections touched by this change (create files if missing):
1) docs/ARCHITECTURE.md + docs/ARCHITECTURE.fa.md
   - UI layers (api / features / stores / router), mock vs Live
   - One-way sync: Studio → GitHub → local pull; no local UI source push
   - Do not document Django internals; point to doion for API contract
2) docs/TESTING.md + docs/TESTING.fa.md
   - How to run: bun run test / test:watch (and lint/tsc if relevant)
   - Vitest vs manual Live vs doion Playwright (link out; do not duplicate e2e suites)
3) README.md — short links to Architecture + Testing; avoid long duplicated guides

## Do not
- Commit package-lock.json / use npm as package manager of record
- Unrelated refactors or new dependencies
- Invent non-paginated backend APIs
- Edit or invent doion/backend documentation inside this repo
- Push assumptions without asking when contract is unclear

## Acceptance (Live API)
- {user} on {route}: {expected UI / no error}
- Mock mode still works for affected flows
- Tests: vitest/tsc as applicable — brief result in reply
- Docs: updated paths listed, or explicit "docs: none — cosmetic"
```

## Clarification request line (always keep)

Include verbatim when useful:

```text
Before coding: list any ambiguities and ask me questions until the instructions are fully clear.
```

## After Studio finishes

User should bring back to Cursor:

1. Short summary of files changed (code + tests + docs)
2. Commit SHA
3. Any extra sites discovered in the scan
4. Docs note: updated paths or `docs: none`
