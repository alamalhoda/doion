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

## Do not
- Commit package-lock.json / use npm as package manager of record
- Unrelated refactors or new dependencies
- Invent non-paginated backend APIs
- Push assumptions without asking when contract is unclear

## Acceptance (Live API)
- {user} on {route}: {expected UI / no error}
- Mock mode still works for affected flows
- tsc / vitest relevant checks pass
```

## Clarification request line (always keep)

Include verbatim when useful:

```text
Before coding: list any ambiguities and ask me questions until the instructions are fully clear.
```

## After Studio finishes

User should bring back to Cursor:

1. Short summary of files changed
2. Commit SHA
3. Any extra sites discovered in the scan
