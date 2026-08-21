# In-app product changelog (planned)

This is the SSOT for **how** Cheque Yar will show “what’s new” to users. It is not implemented yet. Do not add endpoints to [`MASTER_API_CONTRACT.md`](./MASTER_API_CONTRACT.md) until a feature PR lands the API.

## Goal

One place in the product UI (for example About / Help / تنظیمات) lists **server** and **client** changes with:

| Field | Meaning |
|-------|---------|
| Version | Same SemVer as GitHub Release / GHCR tag (`v0.1.0`) |
| Date | Release date (UTC date is enough) |
| Side | `backend`, `frontend`, or `both` |
| Summary | Short user-facing text (FA primary in the app; EN optional) |

Operators and GitHub already see [Releases](https://github.com/alamalhoda/doion/releases). The in-app list is for holders/investors/moderators, not a dump of every commit.

## Version number (one product version)

Do **not** maintain a separate marketing version on the Vue repo and another on Django.

- Cutting a shippable snapshot: doion workflow **Release** (skill `.cursor/skills/semver-release/SKILL.md`).
- That tag versions **both** images: `doion-api` and `chequeyar-front` (SPA from `e2e/ui-pin`).
- Studio still pushes UI to `main`; `product` is the git line for production SPA. Cursor never tags `checkyar-googleai`.

Until that workflow exists on `develop`, there is no product tag to show.

Human how-to (git tags, when/how, SemVer): [`GIT_TAGS_AND_RELEASES.md`](./GIT_TAGS_AND_RELEASES.md).

## Data to collect from today

When a change is user-visible:

1. Studio (UI loop) replies with 1–3 FA+EN bullets (see `ai-studio-ui-fix-loop`).
2. Backend PRs: author puts the same kind of bullets in the PR body.
3. At Release time: paste those bullets into GitHub Release notes, grouped as Backend / Frontend.
4. Later: a doion API can expose the same records the UI already shows.

Suggested record (JSON-shaped, not live yet):

```json
{
  "version": "0.1.0",
  "released_at": "2026-08-21",
  "items": [
    { "side": "backend", "summary_fa": "…", "summary_en": "…" },
    { "side": "frontend", "summary_fa": "…", "summary_en": "…" }
  ]
}
```

Skip cosmetic, CI-only, and internal-only work.

## What not to do now

- Do not ask Studio to build a Versions page in a routine bugfix prompt.
- Do not `git tag` on a UI feature/`main` push as a substitute for Release.
- Do not show secrets, admin URLs, or seed passwords in changelog text.
