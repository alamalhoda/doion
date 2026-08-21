# semver-release examples

Human how-to: `docs/development/GIT_TAGS_AND_RELEASES.md`.

## Remind after a feature merge

User: «PR فیچر لاگین merge شد، کار تمام است.»

Agent: one question — آیا تگ آزمایشی `0.1.0-test.N` با workflow Release روی `develop` بزنیم؟ اگر نه، تمام.

## Owner wants a tag

User: «تگ بزن نسخه تست»

1. Fetch; SHA of `origin/develop`
2. Propose `0.1.0-test.1` if no `v0.1.0-test.1` on origin
3. After yes: `gh workflow run Release --ref develop -f version=0.1.0-test.1`
4. Return the Actions URL; after green, the Release `v0.1.0-test.1`

## Wrong path

User: «روی همین feature برنچ git tag بزن»

Agent: explain that product tags come from **Release** so tag and GHCR images stay the same. Offer dispatch after merge to `develop` (or `--ref` the branch only if they accept images from that SHA).
