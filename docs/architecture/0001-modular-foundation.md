# ADR-0001: Modular Foundation Before Distributed Agents

## Status
Accepted

## Context

The Enterprise Insurance Agent Network (EIAN) will eventually support independently deployed insurance agent systems, including:

- Customer Support Agent
- Policy Agent
- Claims Agent
- Billing Agent
- Fraud Investigation Agent
- Document Intelligence Agent

These systems may have different owners, deployment lifecycles, security requirements, and internal implementations.

However, introducing multiple distributed agents at the beginning would require us to manage network communication, service discovery, distributed state, retries, timeouts, authentication, and observability before validating the core business capabilities.

We need an architecture that supports incremental evolution without introducing unnecessary distributed-system complexity.

## Decision

EIAN will begin as a **modular application with explicit domain and application boundaries**.

The initial architecture will separate:

1. **API Layer** — HTTP endpoints and request/response handling.
2. **Application Layer** — Use-case orchestration and business operations.
3. **Domain Layer** — Insurance business concepts and rules.
4. **Infrastructure Layer** — Persistence, external APIs, model providers, and other adapters introduced when required.

Initial architecture:

```text
FastAPI
   |
   v
Application Services
   |
   v
Domain Models / Rules
   |
   v
Infrastructure Adapters
```

Dependencies will be designed to point inward toward application and domain abstractions. The domain layer must not depend on FastAPI, LangGraph, A2A, MCP, or database-specific implementations.

Agent boundaries will be introduced gradually, based on actual business and architectural requirements.

## Alternatives

### Alternative 1: Start with independent microservices

**Pros**
- Independent deployment
- Independent scaling
- Clear runtime boundaries

**Cons**
- Additional infrastructure
- Distributed failure handling
- Network latency
- More complex local development
- Greater testing and deployment overhead

**Decision:** Rejected for the initial milestone.

### Alternative 2: Build one tightly coupled application

**Pros**
- Simple implementation
- Minimal infrastructure
- Fast initial development

**Cons**
- Weak boundaries
- Difficult extraction into independent systems
- High coupling between business capabilities

**Decision:** Rejected.

### Alternative 3: Modular foundation

**Pros**
- Simple local execution
- Explicit business boundaries
- Easier testing
- Lower operational complexity
- Supports future extraction

**Cons**
- Boundaries require discipline
- Modules initially share one deployment
- Independent scaling is not available initially

**Decision:** Accepted.

## Consequences

### Positive
- Faster incremental development
- Lower infrastructure overhead
- Easier deterministic testing
- Clearer separation of responsibilities
- Reduced premature adoption of distributed protocols

### Negative
- Modules initially share a runtime and deployment lifecycle
- Independent security and scaling boundaries are not yet enforced
- Future extraction may require contract and data-ownership changes

## Security Considerations

- Keep business authorization outside LLM-generated decisions.
- Avoid exposing infrastructure credentials through application responses.
- Design future domain boundaries with least privilege.
- Do not assume an internal module boundary provides the same isolation as a separate service.

## Failure Modes

- Circular dependencies between modules
- Business logic embedded in HTTP handlers
- Shared mutable state
- Premature extraction into remote services
- Framework-specific types leaking into domain models

## Observability

Initially use application logs and health checks.

Later introduce structured logging, correlation identifiers, metrics, and distributed tracing when justified by the architecture.

## Revisit Criteria

Reconsider this decision when:

- A business capability requires independent deployment.
- Teams need separate release lifecycles.
- Independent scaling becomes necessary.
- Security or regulatory requirements demand runtime isolation.
- A remote agent must be independently owned and interoperable.

## Verification

- Domain code has no FastAPI imports.
- Application logic can be tested independently.
- Modules have documented responsibilities.
- CI validates the application.
- No unnecessary distributed dependencies are introduced.

## Related ADRs

- ADR-0002: FastAPI Application Boundary
- ADR-0004: Business Logic Independence
- ADR-0005: A2A Adoption Criteria
