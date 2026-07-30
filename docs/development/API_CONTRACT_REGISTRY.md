# API Contract Registry — DEPRECATED

> **Deprecated as of 2026-07-31.**  
> This file is no longer an API source of truth and must not be updated with endpoint details.

## Canonical SSOT

All API contract documentation lives in:

**[`docs/development/MASTER_API_CONTRACT.md`](./MASTER_API_CONTRACT.md)**

That document is derived from the live backend (`serializers` / `views` / `urls` / `api_router` / `exception_handler` / related model choices) and is mandatory for API-facing changes.

## Why this stub exists

Historically this registry tracked endpoints phase-by-phase alongside the master contract, which caused dual-maintenance drift (roles, error codes, response shapes). It is retained only as a redirect so old links do not break.

## Policy

- Do **not** add or edit endpoint specs here.
- Update `MASTER_API_CONTRACT.md` in the same PR as any API change.
- See the Sync Policy section in the master contract for the full checklist.
