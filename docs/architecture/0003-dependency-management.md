# ADR-0003: Use uv for Python Dependency Management

## Status
Accepted

## Context

EIAN requires consistent dependency resolution and Python environment management across:

- Developer MacBooks
- Local test environments
- GitHub Actions
- Future Docker images
- Future Kubernetes deployments

Without a controlled dependency strategy, developers and CI may install different transitive dependency versions.

This can cause environment-specific failures, incompatible package combinations, and difficult-to-reproduce bugs.

## Decision

Use **uv** as the primary Python environment and dependency management tool.

Project configuration will be maintained in:

```text
pyproject.toml
.python-version
uv.lock
```

Responsibilities:

- `pyproject.toml` — Project metadata, dependency declarations, and tool configuration.
- `.python-version` — Selected Python baseline.
- `uv.lock` — Resolved dependency graph.
- `.venv/` — Local virtual environment, excluded from Git.

The initial Python baseline will be 3.11.

The lockfile must be committed to Git.

CI must install dependencies without silently changing the committed resolution.

## Standard Commands

Create or update the lockfile:

```bash
uv lock
```

Synchronize the environment:

```bash
uv sync --extra dev --locked
```

Inspect dependencies:

```bash
uv tree
```

Run tests:

```bash
uv run --locked pytest
```

Run linting:

```bash
uv run --locked ruff check backend tests
```

Run type checking:

```bash
uv run --locked mypy backend/src
```

## Alternatives

### Alternative 1: pip + venv

**Pros**
- Widely supported
- Simple
- Minimal additional tooling

**Cons**
- Lockfile and environment synchronization require additional conventions or tools

**Decision:** Not selected as the primary workflow.

### Alternative 2: Poetry

**Pros**
- Integrated dependency management
- Lockfile support
- Project packaging facilities

**Cons**
- Different tooling and workflow conventions
- No compelling advantage for the current project requirements

**Decision:** Not selected.

### Alternative 3: uv

**Pros**
- Fast dependency resolution
- Lockfile support
- Python environment management
- Consistent local and CI commands
- Suitable for modern Python project workflows

**Cons**
- Developers must learn an additional tool
- Lockfiles must be maintained correctly
- Reproducibility still depends on runtime and platform constraints

**Decision:** Accepted.

## Consequences

### Positive
- More consistent dependency installation
- Improved CI reproducibility
- Faster environment setup
- Centralized dependency management
- Easier dependency graph inspection

### Negative
- uv becomes a required development tool
- Lockfile conflicts may occur during parallel dependency updates
- A committed lockfile does not eliminate all platform-specific differences

## Security Considerations

- Audit dependencies for known vulnerabilities.
- Avoid untrusted package indexes.
- Do not store package registry credentials in Git.
- Review dependency upgrades.
- Pin CI tooling to approved versions.
- Treat dependency installation as a software supply-chain boundary.

## Failure Modes

- Stale lockfile
- Unsupported Python version
- Dependency resolution conflicts
- Unavailable package distribution
- Platform-specific package incompatibility
- Compromised or vulnerable dependency

## Observability

CI should report:

- Python version
- uv version
- Dependency installation outcome
- Dependency audit outcome
- Build failures

Avoid logging secrets or private registry credentials.

## Revisit Criteria

Reconsider this decision when:

- Organizational standards mandate another package manager.
- uv no longer satisfies reproducibility requirements.
- Tooling compatibility creates unacceptable maintenance overhead.
- A better-supported alternative materially improves security or operations.

## Verification

- `.python-version` is committed.
- `uv.lock` is committed.
- `uv sync --extra dev --locked` succeeds.
- Tests run through uv.
- CI uses the committed lockfile.
- Dependency auditing is configured.

## Related ADRs

- ADR-0001: Modular Foundation
- ADR-0002: FastAPI Application Boundary
