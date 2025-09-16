# Python Project Best Practices (Applied in This Repo)

This document summarizes pragmatic best practices for Python web services and CLIs. Each item below is implemented in this repository as a concrete example you can follow.

## Principles
- Functional-first: prefer functions/modules over classes unless state is required.
- Clear boundaries: separate transport (I/O) from domain (business logic).
- Explicit configuration: strongly-typed settings loaded from environment and `.env`.
- Deterministic tests: no real network; fast and reliable.
- Observability by default: structured logging, request IDs, metrics.

## Structure & Organization
- Use a `src/` layout so imports resolve from the package name, not the project root.
- Organize by domain (feature) rather than abstract layers.
- Keep thin web layers (routers/handlers) that call domain functions.

Why domain/feature-based works
- Clear, functional organization: each folder has an obvious purpose (e.g., `photos/`).
- Matches real-world apps: many successful projects group by feature.
- Deployment-friendly: easy to see boundaries and what ships together.
- Avoids vague layers: skip catch-all directories like `core/` or `services/` that can accumulate mixed concerns.
- Ergonomic imports: `from your_app.photos import fetch_photos` is unambiguous.

Example domain layering
- `api/`: HTTP endpoints (FastAPI routers).
- `app/`: application factory (wires routers, middleware, exception handlers).
- `http/`: low-level transport helpers (e.g., `get_json`), no business logic.
- `domain-or-feature/` (e.g., `photos/`):
  - `service.py`: orchestration entry points used by routes.
  - `gateway.py`: external system adapter, returns raw data only.
  - `mappers.py`: raw → models conversion.
  - `validators.py`: domain validation hooks.
- `models/`: Pydantic v2 data models.

## Structure Comparisons with Examples

Below are three common structures, when to use them, and real projects that reflect each style.

1) Domain/Feature‑Based (Recommended for apps)
- Idea: Group by what the code does (photos, users, billing), not how it does it.
- Pros: Clear ownership, easy scaling, natural boundaries, testable.
- Cons: Requires a little discipline to keep cross‑feature utilities generic.
- Real projects: PostHog (Django app modules), many modern monoliths and services.

Example
```
src/your_app/
├── photos/
│   ├── service.py        # orchestration
│   ├── gateway.py        # external I/O
│   ├── mappers.py        # shape conversions
│   └── validators.py     # domain checks
├── users/
│   ├── service.py
│   └── ...
├── api/                  # routers
├── http/                 # transport helpers
├── models/               # Pydantic models
└── settings/             # typed settings
```

2) Layered (services/, core/, adapters/)
- Idea: Group by architectural layer (e.g., domain, services, adapters).
- Pros: Clear separation at a high level; familiar from Clean/Hexagonal write‑ups.
- Cons: Can obscure feature ownership; files spread across layers; newcomers ask “where does this go?”.
- Real projects: Popular in templates like tiangolo’s full‑stack FastAPI project; many teams adapt it.

Example
```
src/your_app/
├── api/                  # routers/controllers
├── services/             # application services/use cases
├── core/                 # domain entities + rules
├── adapters/             # db/http integrations
├── models/               # schemas
└── settings/
```

3) Flat (library‑style)
- Idea: Few modules at top level; works for small libraries focused on one concern.
- Pros: Minimal ceremony, easy navigation for small scope.
- Cons: Doesn’t scale for apps; modules grow large; mixed concerns.
- Real projects: Libraries like FastAPI/Starlette/Pydantic (they do one thing very well).

Example
```
your_app/
├── api.py
├── http.py
├── models.py
├── settings.py
└── utils.py
```

Rule of thumb
- Choose domain/feature‑based for web apps and services.
- Use layered if your team explicitly prefers architecture‑first and enforces boundaries.
- Keep flat for small, single‑purpose libraries.

Real‑world references
- FastAPI project templates: `tiangolo/full-stack-fastapi-postgresql` (layered inspiration).
- Clean/Hexagonal architecture articles and Cosmic Python (Percival & Gregory) for patterns and tradeoffs.
- Mature web apps (e.g., PostHog) illustrate feature grouping at scale.

Minor improvements to consider
- Combine micro‑folders when they only contain a single tiny file (avoid over‑nesting).
- Keep naming consistent across domains (e.g., `gateway.py` for external adapters in each feature).
- Isolate generic helpers into a `utils/` module only when they are truly cross‑cutting.

Implementation guidelines
- Functions vs classes: prefer function‑based "services" (orchestrators) unless stateful behavior is needed.
- Dependency management: construct dependencies internally in domain code; pass as parameters only when it clarifies testing.

Function‑based example
```python
# your_app/photos/service.py
from your_app.photos import gateway, mappers, validators

async def fetch_photos(limit: int | None = None):
    raw = await gateway.list_photos()
    if limit:
        raw = raw[:limit]
    return [mappers.photo_from_raw(validators.validate_photo_data(item)) for item in raw]
```

Simple dependency creation
```python
# your_app/photos/gateway.py
from your_app.http.client import get_json
from your_app.settings import get_settings

async def list_photos():
    s = get_settings()
    url = f"{str(s.external.base_url).rstrip('/')}/photos"
    return await get_json(url, timeout=s.external.http_timeout)
```

## Type Checking Notes

This document captures the key decisions we made while wiring up type safety for the
OAuth client integration.

### Context on type checking
#### Authlib Client Typing
- FastAPI injects the Authlib client into the auth routes. By default the object is a
  `StarletteOAuth2App`, which exposes methods such as `authorize_redirect` and
  `authorize_access_token`.
- Editors could not resolve those methods until we returned a concrete type. We updated
  `get_oauth_client` to advertise `StarletteOAuth2App` and added matching type hints to
  the route dependencies.
- Runtime code stays functional: the dependency injection simply passes the client as a
  function parameter, keeping the auth handlers stateless and testable.

#### Mypy Configuration
- We already ship a `make type-check` target; enabling it only required adding a
  `[tool.mypy]` section to `pyproject.toml`.
- Configuration highlights:
  - Python 3.11 target and the `pydantic.mypy` plugin so models continue to type-check.
  - `disallow_untyped_defs` and `check_untyped_defs` enforce explicit annotations.
  - `authlib.*` modules are ignored for missing type hints (Authlib does not ship stub
    files).
- Run locally via `uv run mypy src/` or `make type-check`.

### Avoiding Runtime Type Guards
- We briefly guarded the Authlib client with `isinstance` checks plus `cast`, but that
  adds runtime logic purely for the type checker.
- Preferred alternatives:
  - **Protocol** – Define the required method surface from the consumer side. Any object
    that implements the methods (Authlib client, fakes, mocks) satisfies the protocol
    without casts or inheritance.
  - **Stub files** – Provide `.pyi` stubs for Authlib if we ever need full coverage of
    its API.
- `typing.Protocol` lives in the standard library, similar to Go interfaces: structural
  typing with no runtime cost. Static analyzers (mypy, pyright, etc.) enforce the
  contract.

### Practical Guidelines
- Treat `Any` as a last resort; contain it to narrow scopes when untyped third-party
  APIs demand it.
- Prefer defining protocols on the consumer side so test doubles can implement the same
  contract.
- Keep dependency injection in FastAPI routes—receiving the client through a parameter
  keeps the design functional while remaining DI-friendly for overrides in tests.
- If we need additional tooling integration, consider running `make type-check` in CI to
  keep drift from creeping in.

## Further Reading
- FastAPI: https://fastapi.tiangolo.com/
- Starlette: https://www.starlette.io/
- Pydantic v2: https://docs.pydantic.dev/latest/
- httpx: https://www.python-httpx.org/
- Prometheus FastAPI Instrumentator: https://github.com/trallnag/prometheus-fastapi-instrumentator
- uv (package/deps manager): https://docs.astral.sh/uv/
- Full‑stack FastAPI template (layered inspiration): https://github.com/tiangolo/full-stack-fastapi-postgresql
- Architecture Patterns with Python (Cosmic Python): https://www.cosmicpython.com/
- Clean Architecture (book): https://www.oreilly.com/library/view/clean-architecture/9780134494272/
- Hexagonal Architecture overview: https://alistair.cockburn.us/hexagonal-architecture/

## Configuration
- Use `pydantic-settings` for a typed `Settings` object.
- Group settings (e.g., `server`, `cors`, `external`, `logging`).
- Support nested env vars via a delimiter like `__` (e.g., `APP_SERVER__PORT=8000`).
- Cache the settings factory with `functools.lru_cache()` to avoid re-parsing on each use.

Benefits
- Early, typed validation (e.g., `HttpUrl`).
- Clear separation for server/CORS/external integrations/logging.
- Simple overrides in tests via `get_settings.cache_clear()`.

## HTTP Transport
- Keep a transport-only helper that wraps `httpx` and exposes simple functions (e.g., `get_json`).
- Add timeouts and retries with exponential backoff + jitter for resilience.
- Let domain code build URLs; transport only performs requests and raises `httpx` errors.

## API Design
- Version routes (e.g., mount routers under `/v1`).
- Keep handlers small; delegate to domain `service.py`.
- Use absolute imports (`package.module`) for clarity and robust refactors.

## Error Handling & Observability
- Centralize exception handling; map upstream `httpx` errors to 5xx responses.
- Add request ID middleware that injects/propagates an `X-Request-ID` header.
- Make JSON logging a settings toggle; log request metadata (method, path, request_id).
- Expose Prometheus metrics at a standard endpoint (e.g., `/metrics`).

## Testing Strategy
- Use `pytest` + `pytest-asyncio` for async endpoints and domain functions.
- API tests: `httpx` (0.28+) `ASGITransport` to test the app in-process (no server, no network).
- Domain tests: monkeypatch domain functions to simulate scenarios.
- Transport tests: `respx` to mock `httpx` calls at the network boundary.
- Coverage with `pytest-cov`; aim for focused, meaningful tests over line-count goals.

## Tooling & CI
- Python 3.11+; dependency management with `uv`.
- Formatting: `black`; imports: `isort`; type checking: `mypy`.
- CI: run format checks, mypy, and the test suite on every PR/push.

## Packaging & Deployment
- Provide a minimal Dockerfile; run via the module (`python -m package.main`).
- Keep runtime configuration in environment variables (12‑factor).
- Don’t bake secrets into images; rely on environment or secret managers.

## Anti‑Patterns to Avoid
- Mixing business logic into routers or transport helpers.
- Relative imports that become brittle on refactor.
- Tests that hit the real network or depend on flaky external services.
- Monolithic “god modules” that accumulate unrelated responsibilities.

These practices aim to maximize clarity, testability, and operational readiness while keeping the codebase simple and maintainable.
