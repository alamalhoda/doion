---
name: gitflow-workflow
description: "این Skill اجرای کامل و امن GitFlow پروژه را از ابتدا تا انتها هدایت می‌کند: بررسی وضعیت فعلی git و branch، ایجاد branchهای feature/bugfix از develop، پیشنهاد commit message استاندارد (type(scope): description)، همگام‌سازی branch با develop قبل از PR (merge یا rebase)، راهنمای حل conflict، push امن (فقط --force-with-lease بعد از rebase)، ساخت PR به develop، پاک‌سازی branch بعد از PR merge، و ارجاع به semver-release برای تگ. هر زمان کاربر درباره GitFlow، شروع کار جدید، ساخت branch، همگام‌سازی با develop، رفع conflict، پیام commit استاندارد، آماده‌سازی PR، ادغام feature به develop، حذف branch بعد از PR merge، تگ، SemVer، یا GitHub Release سؤال کرد از این Skill استفاده شود. Also use for equivalent English requests about GitFlow workflow."
---

# GitFlow Workflow

Use this skill to apply the repository GitFlow policy end-to-end with safe defaults.

Primary policy source:
- `.cursor/rules/share/gitflow-branch-policy.mdc`

## When To Use

- User wants to start a new branch.
- User asks how to commit under team standards.
- User wants to sync a feature branch with `develop`.
- User is preparing a PR.
- User wants to integrate feature/bugfix into `develop`.
- User wants to create a SemVer tag / GitHub Release / GHCR image (use `.cursor/skills/semver-release/SKILL.md`).
- User needs safe push/rebase guidance.

## Workflow

### 1) Inspect current state first

Always start with:

```bash
git status
git branch --show-current
```

If user is on `main` or `develop` and wants to develop features, warn and move to feature flow.

### 2) Start new feature/bugfix from develop

```bash
git checkout develop
git pull origin develop
git checkout -b feature/<short-name> develop
```

For bug work in development:

```bash
git checkout develop
git pull origin develop
git checkout -b bugfix/<short-name> develop
```

### 3) Commit using convention

Preferred format:

```text
type(scope): description
```

Examples:
- `feat(auth): add google oauth login flow`
- `fix(api): handle empty vehicle filter response`
- `docs(gitflow): clarify merge target policy`

### 4) Sync branch before PR (mandatory)

```bash
git checkout feature/<name>
git fetch origin
git merge origin/develop
# or rebase if explicitly desired:
# git rebase origin/develop
```

If conflicts happen:
1. Resolve files
2. `git add <file>`
3. Continue:
   - `git merge --continue` or
   - `git rebase --continue`

### 5) Push safely

Default push:

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

- Branch is not `main`/`develop`
- Branch synced with `origin/develop`
- Conflicts resolved
- Relevant tests/build pass
- Commit messages follow convention
- Merge target is `develop`
- Do not recommend local direct merge into `develop`

### 8) Post-merge cleanup

```bash
git checkout develop
git pull origin develop
git branch -d feature/<name>
git push origin --delete feature/<name>
```

## 9) SemVer tag / GitHub Release

Do not `git tag` on a feature branch as the product release. Use skill `semver-release`: workflow `Release` via `workflow_dispatch`. Remind once after a feat/fix lands on `develop` if the user talks about shipping.

See `.cursor/skills/semver-release/SKILL.md`.

## Safety Guardrails

- Never suggest direct commit on `main` or `develop`.
- Never suggest local direct merge to move feature/bugfix into `develop`.
- Always show target and source explicitly for merge actions.
- For uncertain intent, ask one clarifying question before risky git commands.
- Prefer minimal, reversible steps.

## Response Template

When user asks for GitFlow help, respond with:
1. Current-state check commands
2. Sync/push command block
3. PR creation command block (target: `develop`)
4. Short reason for safety
5. Optional cleanup after PR merge
6. If they shipped a feat/fix to `develop` and talk about version/deploy: one tag reminder (`semver-release`)

## Additional Examples

See `examples.md` for common scenarios. Human tagging guide: `docs/development/GIT_TAGS_AND_RELEASES.md`.
