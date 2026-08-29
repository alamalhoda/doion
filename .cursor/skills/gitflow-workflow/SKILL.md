---
name: gitflow-workflow
description: "این Skill اجرای کامل و امن GitFlow پروژه را از ابتدا تا انتها هدایت می‌کند: سه نقطهٔ همگام‌سازی (شروع Task با pull --ff-only روی develop، قبل از PR با merge origin/develop، بعد از merge پاک‌سازی محلی و fetch --prune)، ایجاد branchهای feature/bugfix از develop به‌روز، commit با type(scope): description، rebase فقط با درخواست صریح و push با --force-with-lease، ساخت PR به develop، شاخهٔ کوتاه‌عمر یک‌هدفه، و ارجاع به semver-release برای تگ. هر زمان کاربر درباره GitFlow، شروع کار جدید، ساخت branch، همگام‌سازی با develop، رفع conflict، شلوغی ریپو، پیام commit استاندارد، آماده‌سازی PR، ادغام feature به develop، حذف branch بعد از PR merge، تگ، SemVer، یا GitHub Release سؤال کرد از این Skill استفاده شود. Also use for equivalent English requests about GitFlow workflow."
---

# GitFlow Workflow

Use this skill to apply the repository GitFlow policy end-to-end with safe defaults.

Primary policy source:
- `.cursor/rules/share/gitflow-branch-policy.mdc`

## When To Use

- User wants to start a new branch or task.
- User asks how to commit under team standards.
- User wants to sync a feature branch with `develop`.
- User is preparing a PR.
- User wants to integrate feature/bugfix into `develop`.
- User wants cleanup after merge (local/remote branches, prune).
- User wants to create a SemVer tag / GitHub Release / GHCR image (use `.cursor/skills/semver-release/SKILL.md`).
- User needs safe push/rebase guidance.

## Mandatory: three sync points

Do not treat “sync once at start” as enough. Always apply:

1. **Start of task** — `develop` is a local mirror only; then create `feature/*` or `bugfix/*`.
2. **Before PR** — merge `origin/develop` into the working branch (default). Rebase only if the user explicitly asks.
3. **After PR merge** — refresh local `develop`, delete the working branch locally, `git fetch --prune`. Delete remote only if GitHub still has the head branch.

Never commit on local `develop` or `master`. This repo has no `main`; UI `main` is `checkyar-googleai`. If `git pull --ff-only origin develop` fails, stop; do not invent a merge on `develop`. `reset --hard origin/develop` only with explicit user confirmation after explaining lost commits.

## Workflow

### 1) Inspect current state first

Always start with:

```bash
git status
git branch --show-current
```

If user is on `master` or `develop` and wants to develop features, warn and move to feature flow (sync point 1).

### 2) Start new feature/bugfix (sync point 1)

```bash
git checkout develop
git fetch origin
git pull --ff-only origin develop
git checkout -b feature/<short-name> develop
```

For bug work in development:

```bash
git checkout develop
git fetch origin
git pull --ff-only origin develop
git checkout -b bugfix/<short-name> develop
```

Name the branch by **one goal** (`feature/cheque-validation`), not a person dump (`feature/ali-work`). Keep it short-lived.

### 3) Commit using convention

Preferred format:

```text
type(scope): description
```

Examples:
- `feat(auth): add google oauth login flow`
- `fix(api): handle empty vehicle filter response`
- `docs(gitflow): clarify three-point sync`

Work and push only on the feature/bugfix branch:

```bash
git push -u origin feature/<name>
```

### 4) Sync branch before PR (sync point 2, mandatory)

Default is **merge** (safer for new collaborators; no force-push):

```bash
git checkout feature/<name>
git fetch origin
git merge origin/develop
```

Rebase only if explicitly desired:

```bash
git fetch origin
git rebase origin/develop
```

If conflicts happen:
1. Resolve files
2. `git add <file>`
3. Continue:
   - `git merge --continue` or
   - `git rebase --continue`

### 5) Push safely

Default push (after merge sync):

```bash
git push -u origin feature/<name>
```

If branch was rebased:

```bash
git push --force-with-lease origin feature/<name>
```

Never recommend plain `--force`.

### 6) Create PR to `develop` (mandatory for integration)

```bash
git checkout feature/<name>
git push -u origin feature/<name>
gh pr create --base develop --head feature/<name> --title "<title>" --body "<body>"
```

If branch was already pushed, skip the push line and only create PR.

### 7) PR readiness checklist

- Branch is not `master`/`develop`
- Sync point 2 done (merged with `origin/develop` unless user chose rebase)
- Conflicts resolved
- Relevant tests/build pass (backend PR gates: Ruff + pytest; do not treat E2E as merge-block unless policy changes)
- Commit messages follow convention
- Merge target is `develop`
- Do not recommend local direct merge into `develop`

### 8) Post-merge cleanup (sync point 3)

```bash
git checkout develop
git pull --ff-only origin develop
git branch -d feature/<name>
git fetch --prune
```

If the remote head branch still exists:

```bash
git push origin --delete feature/<name>
```

If the repo has **Automatically delete head branches**, skip remote delete; prune is enough. Remind that GitHub auto-delete does **not** remove the local branch.

Recommend enabling **Automatically delete head branches** when discussing GitHub clutter.

## 9) SemVer tag / GitHub Release

Do not `git tag` on a feature branch as the product release. Use skill `semver-release`: workflow `Release` via `workflow_dispatch`. Remind once after a feat/fix lands on `develop` if the user talks about shipping.

See `.cursor/skills/semver-release/SKILL.md`.

## Safety Guardrails

- Never suggest direct commit on `master` or `develop`.
- Never suggest local direct merge to move feature/bugfix into `develop`.
- Always show target and source explicitly for merge actions.
- For uncertain intent, ask one clarifying question before risky git commands.
- Prefer minimal, reversible steps.
- Default sync-before-PR is merge, not rebase.
- Internal teammate: clone this repo (Write), not Fork. Do not recommend Write or `git push` on `checkyar-googleai`. Onboarding: `docs/development/ONBOARDING.md`.

## Response Template

When user asks for GitFlow help, respond with:
1. Current-state check commands
2. Which sync point applies (1 / 2 / 3)
3. Command block for that point (ff-only on develop; merge before PR)
4. PR creation command block (target: `develop`) when integrating
5. Short reason for safety (conflicts, clutter)
6. Cleanup after PR merge (point 3)
7. If they shipped a feat/fix to `develop` and talk about version/deploy: one tag reminder (`semver-release`)

## Additional Examples

See `examples.md` for common scenarios. Human tagging guide: `docs/development/GIT_TAGS_AND_RELEASES.md`.
