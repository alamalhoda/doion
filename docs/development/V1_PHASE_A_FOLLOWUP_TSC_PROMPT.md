# V1 Phase A follow-up — tsc + Testing docs

Paste into Google AI Studio. Return summary + commit SHA.

```text
Context: Active UI repo checkyar-googleai (Bun only; no package-lock.json).
Live: VITE_USE_MOCK=false. Do NOT change backend.
Before coding: ask clarifying questions if anything is unclear.

## Symptom
After commit 70c80e7439f7ac4ff7a169026a0553afaaad667a, `bun run test` passes (29 tests) but `bun run lint` (`tsc --noEmit`) fails with:

1) src/api/index.ts — `useBackendSimulatorStore().kycQueue` does not exist on store type (getVerificationMe mock branch + getKycDetail mock branch)
2) src/api/index.ts — `file.name` when `file` is `File | Blob` (Blob has no name)
3) src/features/moderation/stores/moderationStore.ts — ChequeListing type lacks `city`, `risk_score`, `risk_level`, `user` used in Live fetchReviewDetails mapping

Also: docs/TESTING.md + docs/TESTING.fa.md were not updated for Phase A Live KYC/upload/admin surfaces (ARCHITECTURE was).

## Required
1) Fix all `tsc --noEmit` errors with minimal typed access:
   - Prefer existing store getters (e.g. getKycQueue()) instead of missing `kycQueue` property, or type-safe optional access
   - For uploadDocument mock: use `file instanceof File ? file.name : 'document.bin'`
   - For moderation mapping: only read fields that exist on ChequeListing (issuer_name, bank_name, cheque_serial_number, face_amount, due_date, risk_tier, documents, created_at); drop or cast unknown fields safely
2) Update docs/TESTING.md + docs/TESTING.fa.md briefly: Live KYC on /me, KYC/moderation review Live paths, real FormData upload, admin surfaces (no /admin/reports), how to run lint+test
3) Run `bun run lint` and `bun run test` — both must pass. Report results.

## Do not
- Unrelated refactors, new deps, package-lock.json
- Backend edits

## Acceptance
- `bun run lint` exit 0
- `bun run test` still green
- TESTING EN+FA updated
```
