# syntax=docker/dockerfile:1
# Production API image. Base is CPython 3.12 slim (not the combined uv image).
# CI still uses ubuntu-latest + setup-uv with python-version 3.12; same series, not this image.
# SQLite is not the product database; pass a postgres DATABASE_URL.
# Local host Django + SQLite (Path A) is unchanged. Image build is optional.

FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.8.22 /uv /usr/local/bin/uv

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    DJANGO_SETTINGS_MODULE=config.settings.production \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN adduser --disabled-password --gecos "" --uid 10001 appuser

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY . .
RUN chmod +x /app/docker-entrypoint.sh \
    && uv sync --frozen --no-dev \
    && mkdir -p /app/staticfiles /app/media \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

ENTRYPOINT ["/app/docker-entrypoint.sh"]
