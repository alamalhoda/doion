# AI-Assisted Feature Implementation Guide (Generic)

> A systematic, repeatable process for using AI across the full feature
> lifecycle — frontend-only, backend-only, or full-stack.
> Stack-agnostic. Project-specific rules belong in a short overlay, not in this guide.

Django/Cheque Yar overlay of this process:
`docs/ai_feature_implementation_guide.md`

Start a new feature by **explicitly invoking** the skill
`ai-feature-implementation` (it does not auto-run), or paste the prompt in
`docs/ai_feature_implementation_start_generic.md`.

**Project overlay (fill once per repo, then leave this guide alone):**

- Repo / packages: `[paths]`
- Branch policy: `[e.g. feature/* from develop]`
- Contract SSOT (if any): `[OpenAPI, design system, API contract doc]`
- Test runners: `[e.g. Vitest, Playwright, pytest]`
- Start prompt: `docs/ai_feature_implementation_start_generic.md`

---

## How to Use This Guide

Split the work into **two chats** — one for thinking, one for building.
Each chat has clear inputs and outputs. Never skip the handoff step.

```
CHAT 1 — THINK                        CHAT 2 — BUILD
───────────────────────────────────   ───────────────────────────────────
Step 1:  Requirement Clarification    Step 4:  Implementation
Step 2:  Feature Specification        Step 5:  Self-Review
Step 3:  Technical Design             Step 6:  Test Generation
                                      Step 7:  Integration Check

OUTPUT: Two .md files                 INPUT:  Those two .md files
  - feature_spec.md                           + codebase context
  - implementation_plan.md
```

Before Step 1, declare **Feature Scope** and **Capability Types**.
They control which questions, design sections, and review checks apply.
Skip any section marked *skip if not applicable*.

---

## File Structure

Store all generated documents in version control alongside your code:

```
your-project/
└── ai-documents/
    └── features/
        └── <feature-name>/
            ├── feature_spec.md
            ├── implementation_plan.md
            └── integration_check.md
```

**Naming convention:** kebab-case from the user-facing capability,
not a framework artifact.
Examples: `listing-card-status-badge`, `moderation-queue-filters`,
`checkout-payment-intent`

**Commit these files.** They are the living documentation of why the code
works the way it does. If a feature is significantly changed later, either
update the spec or create a new folder: `<feature-name>-v2`.

---

## Feature Scope & Capability Types

Declare **exactly one scope**. Then tick every capability that applies
(they can combine).

### Scope (exactly one)

| Scope | Use when |
|---|---|
| 🖥️ FRONTEND-ONLY | UI, client state, routing, accessibility. No server/API contract change |
| ⚙️ BACKEND-ONLY | API, domain logic, jobs, data. No UI change |
| 🔗 FULL-STACK | Both layers. The API (or event) contract is the seam between them |

### Capability types (one or more)

| Type | Description |
|---|---|
| 🖼️ UI FEATURE | Screens, components, interaction, visual states, a11y |
| 🔌 API / SERVICE | Endpoints, use-cases, domain services, authz |
| 🗄️ DATA LAYER | Schema, persistence, migrations, cache |
| 🧠 INTELLIGENT | LLM / ML, prompts, pipelines, confidence handling |
| 🌐 AUTOMATION | Browser/RPA, schedulers, third-party integrations |

Frontend-only almost always includes `UI FEATURE`.
Backend-only often includes `API / SERVICE` and/or `DATA LAYER`.
Full-stack includes both sides plus an explicit contract.

---

## CHAT 1 — THINK

---

### Step 1: Requirement Clarification

**Purpose:** Surface ambiguities and edge cases before any design or code is written.

**Input:** Your user story + scope + capability types
**Output:** A numbered list of clarifying questions — answer all of them before Step 2

```
You are a senior software engineer doing a requirement review before implementation.

## Feature Scope
[FRONTEND-ONLY | BACKEND-ONLY | FULL-STACK]

## Capability Types
[UI FEATURE | API / SERVICE | DATA LAYER | INTELLIGENT | AUTOMATION]
(select all that apply)

## User Story
[PASTE USER STORY HERE]

## Additional Context
[Notes, constraints, existing screens/APIs, design system, out-of-scope hints]

---

Your job is NOT to write code yet.

Based on the scope, capability types, and user story above, ask the most
important clarifying questions a senior engineer would ask before starting
implementation. Only ask about the selected scope and capability types.

If FRONTEND-ONLY or FULL-STACK / UI FEATURE:
- Which surfaces (routes, pages, components, entry points) change?
- Empty, loading, error, permission-denied, and success states
- Responsive / RTL / accessibility expectations
- Client state: URL, store, local, or server-driven?
- What is already in the design system vs what is new?

If BACKEND-ONLY or FULL-STACK / API / SERVICE:
- Consumers of this API or service (UI, other services, jobs)
- Authn/authz: who can do what
- Idempotency, retries, and partial failure
- Backward compatibility with existing clients

If DATA LAYER:
- Entities, relationships, uniqueness, nullability
- Migration risk on existing data
- Read/write performance and consistency expectations

If INTELLIGENT:
- Exact input and expected output format
- Model choice vs flexibility
- Hallucination / low-confidence handling
- Latency and cost sensitivity
- Whether output feeds another system

If AUTOMATION:
- Trigger (scheduled, on-demand, event-driven)
- Mid-flow failure, retries, resumability
- Auth / login steps
- Success/failure reporting
- Rate limits or anti-bot constraints

If FULL-STACK, also ask:
- What is the contract between UI and backend (request/response or events)?
- Which side is source of truth for each field?
- Can UI ship behind a flag before the API is ready, or vice versa?

For ALL features also ask:
- Who uses this, and on which devices/roles?
- Existing patterns in the codebase to follow
- What is explicitly out of scope

Return a numbered list of questions only. No code, no suggestions yet.
```

**After this step:** Answer every question in the chat before proceeding to Step 2.

---

### Step 2: Feature Specification

**Purpose:** Formally capture what the feature must do in precise, testable language.
Written now — while requirements are freshest — so that the technical design in
Step 3 is driven by the spec, not the other way around.

**Input:** Answered questions from Step 1 (already in chat context)
**Output:** `feature_spec.md`

```
Based on our requirements discussion, generate a feature specification
file called `feature_spec.md`.

This file has two jobs:
1. It drives the technical design in the next step
2. It will be used in Chat 2 to generate tests

So it must capture behavior precisely — not architecture, not code,
just what the feature does and how it should behave in every scenario.

---

## File Structure

### 1. Feature Overview
- One paragraph summary of what this feature does and why it exists
- Scope: FRONTEND-ONLY / BACKEND-ONLY / FULL-STACK
- Capability types
- Primary consumers of this feature (human roles and/or calling systems)

### 2. Surfaces & Contract
Skip subsections that do not apply.

**UI (if UI FEATURE):**
- Routes / screens / components the user sees
- Key interactions (click, submit, filter, navigate)
- Visual/UX states: default, loading, empty, error, forbidden, success

**API / events (if API / SERVICE or FULL-STACK):**
- Each operation: method, path or message name, auth
- Request and response (or event payload) shape
- Error codes / error payload the client must handle

**Inputs & outputs (always):**
- Every input this feature accepts: name, type, required/optional, constraints
- Every output this feature returns: shape, type, and what each field means

### 3. Business Rules
A numbered list of explicit rules the feature must enforce.
Each rule should be a single, testable statement. Examples:
- "A guest cannot see the moderation actions on a listing card"
- "Submitting with an empty amount shows a field error and does not call the API"
- "If the LLM returns malformed JSON, the service must retry up to 3 times then fail closed"

### 4. Acceptance Scenarios
Written in plain language, not code. For each scenario use this format:

**Scenario [N]: [Short name]**
- Given: [initial state or context]
- When: [the action or input]
- Then: [the expected outcome]

Cover these scenario types:
- Happy path (the normal successful flow)
- Edge cases (boundary values, empty inputs, minimum/maximum, first/last item, stale data)
- Failure cases (what happens when things go wrong)
- Permission / role cases if relevant
- For UI: loading, empty, error, and forbidden
- For intelligent services: unexpected or malformed model output
- For automation services: mid-flow failures, element not found, timeouts

### 5. Out of Scope
Explicitly list what this feature does NOT handle.
This prevents scope creep in both implementation and tests.

---

## Rules for Writing This Spec
- Every statement must be testable — if you can't write a test for it, rewrite it
- No implementation details — say WHAT, never HOW
- No ambiguous language — avoid "should handle gracefully",
  instead say exactly what happens
- If something is still ambiguous, flag it with: ⚠️ OPEN QUESTION: [question]
  rather than making an assumption silently
```

**After this step:** Read `feature_spec.md` carefully and resolve any
`⚠️ OPEN QUESTION` items before moving to Step 3.

---

### Step 3: Technical Design

**Purpose:** Decide how to build what the spec describes. The design is explicitly
driven by `feature_spec.md` — not the other way around.

**Input:** `feature_spec.md` (already in chat context)
**Output:** `implementation_plan.md`

```
Using feature_spec.md as the source of truth, produce a technical design
for this feature and write it to a file called `implementation_plan.md`.

Do NOT write implementation code yet.

---

## Phase 1 — Design Brief
First, present the design for my review. Skip sections that do not apply.

### 1. Placement in the codebase
- Which packages / apps / folders change
- New vs modified modules
- How this fits existing architecture (features, layers, design system)

### 2. UI architecture (skip if not applicable)
- Component tree (page → feature components → shared primitives)
- State: local, store, URL, server cache
- Routing and navigation
- Reuse vs new primitives; tokens / theme constraints
- Client-side validation vs server-side validation

### 3. API / service layer (skip if not applicable)
- Endpoints or use-case functions
- Authz checks
- Mapping from domain to transport (DTO / serializer / schema)
- Call flow (controller/handler → service → data)

### 4. Data layer (skip if not applicable)
- New or modified entities/tables/collections
- Key fields, relationships, and constraints
- Whether any migrations have non-trivial risk

### 5. Full-stack contract (skip if not FULL-STACK)
- The shared contract artifact to update (OpenAPI, typed client, contract doc)
- Field ownership (which side is SSOT)
- Compatibility: additive change vs breaking change
- Feature-flag or staged rollout if layers land separately

### 6. External dependencies
- Any new libraries, APIs, or services needed
- LLM model/tools if this is an intelligent capability
- Browser/driver considerations if this is an automation capability

### 7. Error handling strategy
- What can go wrong at each major step
- How failures should be surfaced (UI state, HTTP error, exception, logging, event)

### 8. Open questions / risks
- Anything still ambiguous after reviewing feature_spec.md
- Technical risks or tradeoffs worth flagging before coding starts

Keep each section concise — this is a design brief, not documentation.
Flag anything where you see multiple valid approaches and briefly state
the tradeoff.

Wait for my approval before proceeding to Phase 2.

---

## Phase 2 — Write the Plan
Once I approve the design, write `implementation_plan.md`:

# Implementation Plan — [Feature Name]

## Architecture Summary
[One paragraph summary of the agreed approach]
Scope: [FRONTEND-ONLY | BACKEND-ONLY | FULL-STACK]

## Implementation Steps
Order steps so each is reviewable and independently verifiable.
Typical order (omit what does not apply):
- [ ] Step 1: Data / schema (if any)
- [ ] Step 2: Domain / service logic (if any)
- [ ] Step 3: API or contract (if any)
- [ ] Step 4: UI state and components (if any)
- [ ] Step 5: Wiring (routes, stores, feature flags)
- [ ] Step 6: Docs / contract sync

Do not cram UI and backend into one step on a full-stack feature.

## Key Decisions & Assumptions
[Any tradeoffs or assumptions made during design that Chat 2 should know about]

## Open Questions
[Any unresolved ⚠️ items from feature_spec.md that must be addressed
before or during implementation]
```

**After this step:** Chat 1 is complete. You now have two files ready to hand
off: `feature_spec.md` and `implementation_plan.md`. Commit both to
`ai-documents/features/<feature-name>/` before opening Chat 2.

---

## CHAT 2 — BUILD

### Handoff Prompt (Always Start Chat 2 With This)

**Purpose:** Load context into a fresh chat cleanly, without relying on
conversation history.

```
I am implementing a new feature. The thinking and design phase is complete.
Here are the reference files you must read before we start:

- feature_spec.md — the full requirements and acceptance scenarios
- implementation_plan.md — the agreed technical design

Rules:
- Treat these files as the source of truth, not our conversation
- If anything in the codebase contradicts the spec, flag it, don't silently decide
- We will follow the step-by-step implementation loop from implementation_plan.md
- Implement only the layers in the declared scope

Start by reading both files and confirming you understand the feature
and the plan. Then wait for me to say "begin".
```

---

### Step 4: Implementation

**Purpose:** Build the feature in controlled, reviewable steps.

**Input:** `feature_spec.md` + `implementation_plan.md` + codebase context
**Output:** Working code + `implementation_plan.md` updated with checkboxes

```
Now implement the feature following implementation_plan.md exactly.

## Execution Rules
- Implement only one step at a time
- After completing each step, mark it done in implementation_plan.md:
  `- [x] Step description`
- Add a short note under the step if you made any assumptions
- Wait for my review and confirmation before moving to the next step
- Repeat until all steps are complete

---

## Implementation Rules

### General
- Follow the existing code style and patterns you see in this project
- Prefer explicit types (or the project's typing convention)
- No magic numbers or hardcoded user-facing strings — use constants, tokens, or i18n
- Keep functions/components small and single-purpose
- Do not invent a parallel architecture when the repo already has one

### Error Handling
- Never silently swallow errors
- Use specific error types / HTTP statuses / UI error states, not bare catch-all
- Log errors with enough context to debug (include relevant IDs, operation)
- Never log secrets or unnecessary personal data
- Fail in a way the caller or user can act on

### Frontend (skip if not applicable)
- Put view-specific UI in the feature folder; put reusable primitives in shared UI
- Do not duplicate design-system tokens (color, spacing, type) as one-off CSS
- Every async view needs loading, empty, error, and (if relevant) forbidden
- Keep side effects in composables/hooks/stores, not in presentational components
- Client validation is UX; server/API validation remains the authority if an API exists
- Do not change API contracts from the UI repo unless this is FULL-STACK and the plan says so

### Backend / API (skip if not applicable)
- Keep HTTP/GraphQL/RPC handlers thin; business rules live in services/use-cases
- Validate at the boundary; reject unknown or extra fields if that is project policy
- Authorize on every mutating operation
- Multi-step writes that must be atomic go in a transaction (or equivalent)
- Avoid N+1 / unbounded queries when touching related data

### Data Layer (skip if not applicable)
- Migrations must be reversible or have an explicit rollback note
- Do not add non-nullable columns without a default or a backfill plan
- Constraints that the spec requires (unique, fk, check) belong in the schema, not only in code

### Intelligent (skip if not applicable)
- Separate prompt templates from business logic
- Validate model output before using it downstream
- Handle timeout and malformed responses explicitly
- Log raw input/output at DEBUG only; never log secrets or personal data by default

### Automation (skip if not applicable)
- Each major action should be wrapped in error handling
- Prefer explicit waits over hardcoded sleep
- Log each major step so failures are easy to locate
- Make the flow resumable, or at minimum clearly report where it failed

---

## Output Format Per Step
For each step, produce code and end with:
# ---- REVIEW NOTE ----
# What this step did, assumptions made, and anything I should double-check
# Next step will be: [brief description of next step]
```

---

### Step 5: Self-Review

**Purpose:** Catch errors, gaps, and inconsistencies before tests are written.

**Input:** Completed implementation + `feature_spec.md` (in chat context)
**Output:** Inline fixes + final `implementation_plan.md` update

```
Review the code you just implemented against the checklist below.
Do NOT rewrite everything — only flag and fix real issues you find.

For each section, explicitly state:
- ✅ PASS — if everything looks good, briefly say why
- ⚠️ ISSUE — if something needs fixing, explain what and fix it immediately
- N/A — if the section doesn't apply to this scope / capability

---

## Review Checklist

### 1. Correctness
- Does the implementation match every business rule in feature_spec.md?
- Are all acceptance scenarios from feature_spec.md actually handled?
- Are there any ⚠️ OPEN QUESTIONS in the spec that were never resolved?

### 2. Error Handling
- Is every external call wrapped in proper error handling?
  (HTTP, DB, LLM, browser, filesystem)
- Are errors specific, never bare catch-all?
- Are errors logged with enough context to debug in production?
- Does the caller or UI receive a meaningful signal when something fails?

### 3. Edge Cases
- What happens with empty / null / missing inputs?
- What happens at boundary values (empty list, single item, max size)?
- Are there any assumptions in the code that could silently fail?
- Stale client state / concurrent updates if relevant?

### 4. Frontend (skip if not applicable)
- Do loading / empty / error / forbidden states exist?
- Is logic leaking into presentational components?
- Are design tokens / shared components reused?
- Are there obvious keyboard / label / contrast issues?
- Are routes and feature flags wired as in the plan?

### 5. Backend / API (skip if not applicable)
- Are handlers thin, with domain logic in services?
- Is authz enforced on mutations?
- Does the contract match feature_spec.md?
- Are multi-step writes atomic where required?

### 6. Data Layer (skip if not applicable)
- Are risky migrations flagged?
- Are there N+1 or missing indexes on filter/lookup fields?
- Are spec constraints enforced in schema or equivalently guaranteed?

### 7. Intelligent (skip if not applicable)
- Is model output validated before being used downstream?
- Does retry vs fail-closed match the spec?
- Are prompt templates decoupled from business logic?

### 8. Automation (skip if not applicable)
- Is every interaction protected against timeout / not-found?
- Are there hardcoded sleeps that should be explicit waits?
- Is the failure point clearly logged if the flow breaks mid-run?
- Is cleanup needed if the automation fails halfway?

### 9. Code Quality
- Are there any functions/components doing more than one thing?
- Are there hardcoded strings or magic numbers that should be constants?
- Is there any dead code or commented-out blocks left behind?

### 10. Security (flag only, don't over-engineer)
- Is any sensitive data being logged that shouldn't be?
- Is user input being trusted anywhere without validation?
- Are any credentials or secrets hardcoded?
- Are there authz holes on new actions?

---

## After the Review
- Update implementation_plan.md with a final entry:
  `- [x] Self-review complete — [N] issues found and fixed`
- If any ⚠️ OPEN QUESTIONS remain unresolved from feature_spec.md,
  list them explicitly so I can make a decision before tests are written
```

---

### Step 6: Test Generation

**Purpose:** Write a test suite anchored to intended behavior, not inferred from code.

**Input:** `feature_spec.md` + reviewed implementation (in chat context)
**Output:** Test files using **this repo's** runner and layout

```
Using feature_spec.md as the source of truth, generate a comprehensive
test suite for the feature we just implemented and reviewed.

Do NOT infer test cases from the code — derive them from feature_spec.md.
The code tells you how it works, the spec tells you how it SHOULD work.

Use this project's existing test stack, file layout, and naming.
If the project already has a convention, follow it instead of this default.

---

## Default Naming (adapt to language)

### Logic / rules
test_<subject>__when_<context>__then_<expected_behavior>

### HTTP / API
test_<verb>_<endpoint>__when_<context>__then_<expected_behavior>

### UI / component
test_<component>__when_<context>__then_<expected_behavior>

### Rules
- Always descriptive, never abbreviated
- No numeric status codes in names UNLESS the status itself is the focus
- One behavior per test, no vague names like test_success()
- Parameterize variations of the same scenario
- Helper functions that are not tests must follow the project's helper pattern
  (e.g. prefix with _)

---

## Test Structure (include only what applies)

### 1. Unit Tests
- One test per business rule listed in feature_spec.md
- Mock all external I/O (network, DB, LLM, browser)
- Test each rule in isolation — no chaining of unrelated behaviors in one test

### 2. UI / Component Tests (skip if no UI)
- Render the states in the spec: default, loading, empty, error, forbidden, success
- Assert on user-visible behavior (roles, labels, disabled submit),
  not implementation details
- Do not screenshot-assert unless the project already does visual regression

### 3. Edge Case Tests
- Cover every edge case listed in feature_spec.md
- Also cover: empty string/list, null/undefined, boundary values
- For intelligent capabilities: malformed / timeout / empty model output
- For automation capabilities: element not found, timeout, mid-flow failure

### 4. Failure Case Tests
- Every failure scenario from feature_spec.md must have a test
- Assert on the specific error type or UI error state, not just that it failed

### 5. Integration / Contract Tests (skip if not applicable)
- Test the full request → response (or event) cycle
- Assert on payload shape, not only status
- FULL-STACK: at least one test that the UI expects the same contract the API provides

### 6. E2E (only if the spec's happy path cannot be proven cheaper)
- One critical user journey, not a duplicate of every unit case

---

## Test File Organization
- Group tests by subject (class, describe, or folder — match the repo)
- One test file per feature module
- Shared fixtures go in the project's shared test setup, not copied into every file

---

## Output Format
Produce tests in this order:
1. Shared fixtures / test setup additions
2. Unit tests
3. UI / component tests
4. Edge and failure tests
5. Integration / contract tests
6. E2E only if justified

After all tests are written, produce a short coverage summary:
# ---- COVERAGE SUMMARY ----
# Business rules covered: X/X from feature_spec.md
# Acceptance scenarios covered: X/X from feature_spec.md
# Open questions that could not be tested: [list any ⚠️ items]
```

---

### Step 7: Integration Check

**Purpose:** Zoom out and assess the impact of this feature on the rest of the system.

**Input:** All code produced in Chat 2 + codebase context
**Output:** `integration_check.md`

```
Now that the feature is implemented and tested, perform an integration check.
Do NOT write new feature code yet — this is an analysis step.

Review the newly implemented code in the context of the entire codebase
and produce an integration report saved to `integration_check.md`.

---

## Integration Check Sections (N/A if not applicable)

### 1. Breaking Changes
- Does this feature change any existing function signatures or return types?
- Does it modify any shared components, stores, utilities, or modules?
- Does it change any existing API / event contracts?
- Are there any other parts of the codebase that call modified code
  and may now behave differently?

For each breaking change found:
⚠️ BREAKING: [what changed] → [what is affected] → [recommended fix]

### 2. Frontend Impact
- Shared components, theme tokens, or layouts changed?
- Routing / nav / feature flags affecting other screens?
- Bundle / performance risk (heavy new dependency, large lists without virtualization)?
- i18n / RTL / a11y regressions on existing screens?

### 3. API / Contract Impact
- Additive vs breaking
- Contract SSOT updated in the same change set? (if the project has one)
- Typed client / mocks / simulator still aligned?

### 4. Data Impact
- Are there any new migrations that could be risky on a live database?
  (adding non-nullable columns, dropping columns, renaming fields)
- Are there any queries that could cause performance issues at scale?
  (missing indexes, full scans, N+1)
- Are there any data integrity risks if the migration runs mid-traffic?

For each issue found:
⚠️ DB RISK: [what the risk is] → [recommended mitigation]

### 5. LLM Integration Impact
- Does this feature introduce new model calls that affect latency
  of any existing flows?
- Are there shared prompt templates or clients being modified?
- Could the new behavior affect any existing features that
  depend on the same model or pipeline?

### 6. Automation Impact
- Does this automation share sessions, drivers, or schedules
  with existing automations?
- Are there shared selectors or interaction patterns
  that could be affected by changes here?

### 7. Configuration & Environment
- Are there new environment variables, settings, or feature flags required?
- Are they documented and do they have safe defaults?
- Will this feature behave differently across dev/staging/production
  in any unexpected way?

### 8. Dependency Impact
- Are any new libraries being introduced?
- Do they conflict with existing dependencies?
- Are there any licensing or security concerns with new packages?

### 9. Backwards Compatibility & Rollout
- If this feature is behind an API, is the old contract still honored?
- If existing data is affected, is there a migration or backfill needed?
- Are there any consumers (internal or external) that need to be notified?
- Is a feature flag / staged rollout needed for full-stack delivery?

---

## Output Format

Produce integration_check.md with:
- One section per category above
- ✅ CLEAR — if no issues found in that section
- ⚠️ RISK — for each issue found, with recommended action
- N/A — if the section doesn't apply

End the file with a final summary:

## Integration Verdict
- 🟢 READY — no issues found, safe to merge
- 🟡 MERGE WITH CAUTION — issues found but have clear mitigations
- 🔴 NEEDS WORK — blocking issues that must be resolved before merging

List any action items that must be completed before this feature
is considered done.
```

---

## Quick Reference Cheatsheet

```
CHAT 1 — THINK
──────────────────────────────────────────────────────────────────
Declare   Scope + capability types
Step 1    Requirement Clarification   → Q&A answered in chat
Step 2    Feature Specification       → feature_spec.md ✅
Step 3    Technical Design            → implementation_plan.md ✅

          Commit both files to ai-documents/features/<feature-name>/
          before opening Chat 2.

HANDOFF
──────────────────────────────────────────────────────────────────
          Load feature_spec.md + implementation_plan.md into a
          fresh chat. AI confirms understanding. You say "begin".

CHAT 2 — BUILD
──────────────────────────────────────────────────────────────────
Step 4    Implementation              → code + updated plan ✅
Step 5    Self-Review                 → fixes + final plan ✅
Step 6    Test Generation             → tests from the spec ✅
Step 7    Integration Check           → integration_check.md ✅

COMMIT
──────────────────────────────────────────────────────────────────
          ai-documents/features/<feature-name>/
            ├── feature_spec.md
            ├── implementation_plan.md
            └── integration_check.md
```

---

> **Guiding principle:**
> The prompts are only as good as your discipline to follow the process under
> deadline pressure. The `ai-documents/` files are your safeguard —
> if they exist and are complete, you did the process right.
