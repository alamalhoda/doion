---
name: semver-release
description: >-
  Creates doion SemVer GitHub Releases and matching GHCR images via the Release
  workflow (workflow_dispatch), not local git tag on feature branches. Use when
  the user mentions tag, tagging, git tag, GitHub Release, GHCR, semver, version,
  prerelease, rerelease, انتشار، تگ، نسخه، رلیز، or after a feat/fix merge when a
  shippable snapshot is needed.
---

# SemVer Release (doion)

Policy SSOT: `.cursor/rules/share/semver-release-policy.mdc` and the tag section in `.cursor/rules/share/gitflow-branch-policy.mdc`.

Product tags are created by `.github/workflows/release.yml` (name: **Release**): git tag `v*`, GitHub Release, `ghcr.io/<owner>/doion-api:<tag>` and `ghcr.io/<owner>/chequeyar-front:<tag>` (SPA from `e2e/ui-pin`). No Chabokan deploy.

## Remind (do not nag)

One short question is enough, for example: «برای این کار تگ SemVer با workflow Release بزنیم؟»

Remind when:

- User says a **feat/fix** PR to `develop` is merged and they talk about done / ship / deploy / نسخه
- User-visible UI reached `product` (or they are merging `main` → `product`) and they talk about shipping the SPA
- A plan Verify step needs a tagged image
- User asks to deploy production API/SPA

Do **not** remind for docs-only, rules-only, chore, or every commit.

Never dispatch Release without an explicit version (or a clear yes to a proposed version).

## Workflow (when releasing)

1. `git fetch origin` and confirm the intended **ref** (usually `origin/develop`) and SHA.
2. Confirm `.github/workflows/release.yml` exists **on that ref**. If it is only on a feature branch, say merge that PR first (or dispatch `--ref` that branch).
3. Propose SemVer:
   - First/experimental: `0.1.0-test.1` (prerelease)
   - Compatible API add: bump MINOR
   - Bugfix only: bump PATCH
   - Breaking `/api/v1/` contract: bump MAJOR (rare; ask)
4. Check the tag is free: `git ls-remote --tags origin "refs/tags/v<version>"`
5. After owner confirms version **and** ref:

```bash
gh workflow run Release --ref <branch-or-sha-branch> -f version=<semver-without-or-with-v>
```

6. Point to the Actions run, then the Release and GHCR packages. Do not treat a red job as success.
7. Put collected changelog bullets (backend PR + Studio FA/EN seeds) into the Release notes, grouped Backend / Frontend. In-app display later: `docs/development/PRODUCT_CHANGELOG.md`.
8. If this release includes new UI, confirm `e2e/ui-pin` matches the intended `product` SHA before dispatch.
9. Do not `git tag` locally unless the owner explicitly wants a **non-product** pointer and understands it will not push images. Never tag `checkyar-googleai` from Cursor.

## Forbidden

- `git push --force` / moving an existing release tag
- Tagging from a dirty `feature/*` as if it were production
- Using `CHABOKAN_TOKEN` for this workflow
- Starting CD / live deploy in the same step unless the user separately confirmed Step 11/12

## Additional

Examples: [examples.md](examples.md)  
Human how-to: `docs/development/GIT_TAGS_AND_RELEASES.md`  
In-app changelog (planned): `docs/development/PRODUCT_CHANGELOG.md`
