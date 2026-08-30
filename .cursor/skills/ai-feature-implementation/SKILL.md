---
name: ai-feature-implementation
description: >-
  Runs the two-chat Think-then-Build feature workflow (clarification,
  feature_spec.md, implementation_plan.md, step-by-step coding, self-review,
  spec-based tests, integration_check.md) for frontend-only, backend-only, or
  full-stack work. Use only when the user explicitly names this skill,
  @-mentions ai-feature-implementation, asks for ai-feature-implementation-flow,
  or pastes the AI feature implementation start prompt. Do not use for small
  edits, bugfixes, refactors, or questions. Also use for equivalent Persian
  requests that explicitly name this skill (مهارت پیاده‌سازی ویژگی).
disable-model-invocation: true
---

# AI Feature Implementation

Two-chat workflow: **THINK then BUILD**. Do not skip the handoff.

Prompt SSOT (read before Step 1; do not paste the whole guide into the reply):

1. If the workspace has `docs/ai_feature_implementation_guide_generic.md`, Read that file.
2. Else Read [`reference.md`](reference.md) next to this skill.
3. Read the Django/Cheque Yar overlay `docs/ai_feature_implementation_guide.md` only when that file exists **and** the user asked for that overlay (or the start prompt in `docs/ai_feature_implementaation_start.md`).

Start template: [`start-prompt.md`](start-prompt.md). How humans invoke this: [`USER-GUIDE.md`](USER-GUIDE.md).

## Hard rules

- **Explicit invocation only.** If the user did not name this skill, @-mention it, or paste its start prompt, do not follow this workflow.
- **Small work is out of scope.** One-file tweaks, copy changes, bugfixes, refactors, and Q&A stay on the normal agent path.
- **No code in Chat 1.** Clarification → spec → design only.
- **One implementation step at a time** in Chat 2. Wait for review before the next step.
- Spec drives design; spec drives tests. Do not infer tests from implementation.
- Skip any section marked N/A for the declared scope / capability types.
- Follow the current repo's architecture, test runner, and branch policy. Do not invent a parallel layout.

## When not to use (even if attached)

Stop and say this skill does not apply when the request is clearly a small change, unless the user still insists on the full workflow.

## Feature scope (exactly one) + capability types (one or more)

| Scope | Use when |
|---|---|
| FRONTEND-ONLY | UI / client only; no API contract change |
| BACKEND-ONLY | API / domain / data only; no UI change |
| FULL-STACK | Both layers; contract is the seam |

Capabilities: `UI FEATURE` · `API / SERVICE` · `DATA LAYER` · `INTELLIGENT` · `AUTOMATION`

If the user omitted scope or types, ask once, then continue. Do not guess silently.

## Workflow checklist

Copy and track:

```text
AI feature implementation:
- [ ] Scope + capability types declared
CHAT 1 — THINK
- [ ] 1 Requirement clarification (questions only; user answers)
- [ ] 2 feature_spec.md (resolve ⚠️ OPEN QUESTION before Step 3)
- [ ] 3 Design brief → approval → implementation_plan.md
HANDOFF
- [ ] Fresh chat loads spec + plan; wait for "begin"
CHAT 2 — BUILD
- [ ] 4 Implement one plan step at a time
- [ ] 5 Self-review vs spec
- [ ] 6 Tests derived from spec (repo's runner)
- [ ] 7 integration_check.md
```

### Artifacts

Write under `ai-documents/features/<feature-name>/` when that tree exists or is the repo convention. Otherwise use `docs/ai-documents/features/<feature-name>/`. Name the folder from the user-facing capability (kebab-case).

```text
feature_spec.md
implementation_plan.md
integration_check.md
vendor-score.md   # only when the slice is KYC, SMS, SAYAD, issuer credit, e-signature, or cheque OCR
```

### Chat 1 gates

- **Step 1:** Numbered questions only. No design, no code. Wait for answers.
- **Step 2:** `feature_spec.md` = WHAT, not HOW. Every statement testable.
- **Step 3:** Design brief first; wait for approval; then write `implementation_plan.md` with checkboxes. Full-stack: do not cram UI and backend into one step.
- Tell the user to commit spec + plan before Chat 2.
- If the slice is KYC, SMS, SAYAD inquiry, issuer credit, e-signature, or cheque OCR: Read `docs/capability-roadmap/vendor-landscape.md` before Step 2, run its research prompt, keep the domain vendor-agnostic, and write `vendor-score.md` next to the spec.
- If the work comes from `docs/capability-roadmap/`: Read `docs/capability-roadmap/usage-guide.md` before Step 1. Do not start Build on `blocked`/`draft` slices or skip `blocked_by`. One slice per feature branch.

Use the prompt blocks from the SSOT guide for each step. Do not shorten the spec/plan templates.

### Handoff (start of Chat 2)

If this chat does not already contain the spec and plan, Read both files, confirm understanding, and **wait for the user to say begin**.

### Chat 2 gates

- **Step 4:** Follow `implementation_plan.md`. After each step: mark `[x]`, add a short REVIEW NOTE, wait.
- **Step 5:** Checklist from the SSOT guide. Fix real issues only. N/A inapplicable sections.
- **Step 6:** Tests from `feature_spec.md`, not from code. Match the repo's test layout and naming.
- **Step 7:** Analysis only — write `integration_check.md` with CLEAR / RISK / N/A and a verdict (READY / MERGE WITH CAUTION / NEEDS WORK).

## Project overlay

If the repo documents an overlay (paths, contract SSOT, test runner, GitFlow), apply it. Do not copy another project's overlay into a new repo.
