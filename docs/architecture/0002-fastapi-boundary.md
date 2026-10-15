# ADR-0002: FastAPI as the Initial Application Boundary

## Status
Accepted

## Context

EIAN needs an HTTP application boundary for future customer-facing requests, task management, and agent workflow interactions.

The eventual architecture will include:

```text
Angular
   |
   v
FastAPI
   |
   v
Support Agent System
   |
   v
Internal Workflow / A2A Client
```

The project will use Python for its agentic AI implementation, including LangChain, LangGraph, and the official A2A Python SDK where justified.

However, the application must not become tightly coupled to FastAPI.

Existing Java/Spring Boot enterprise services will remain valid downstream systems.

## Decision

Use **FastAPI as the initial HTTP application boundary**.

FastAPI will be responsible for:

- HTTP request handling
- Input validation
- Response serialization
- API documentation
- Authentication integration
- Request-scoped context
- Application error translation
- HTTP streaming when required

Business logic and agent orchestration must reside outside HTTP route handlers.

Conceptual architecture:

```text
HTTP Request
     |
     v
FastAPI Router
     |
     v
Application Service
     |
     v
Domain Logic
     |
     v
Infrastructure Port
     |
     v
External Adapter
```

Future user-facing APIs may include:

```text
POST /api/v1/chat
POST /api/v1/tasks
GET  /api/v1/tasks/{task_id}
POST /api/v1/tasks/{task_id}/cancel
POST /api/v1/reviews/{id}/approve
```

These are future application APIs, not implemented endpoints in Milestone 0.2.

A2A protocol endpoints will be introduced separately when required.

## Alternatives

### Alternative 1: Spring Boot

**Pros**
- Mature enterprise ecosystem
- Strong integration with existing Java systems
- Familiar operational and security tooling

**Cons**
- Python-focused agent frameworks may require additional integration work
- Cross-language adapters may be necessary for selected libraries

**Decision:** Not selected for the initial AI application boundary, but retained for enterprise backend services.

### Alternative 2: Flask

**Pros**
- Lightweight
- Flexible
- Simple HTTP applications

**Cons**
- Requires additional choices for validation, schema generation, and other application facilities

**Decision:** Not selected.

### Alternative 3: FastAPI

**Pros**
- Python type-hint integration
- Request validation
- OpenAPI support
- ASGI support
- Async endpoint support
- Convenient integration with Python agent frameworks

**Cons**
- Async and blocking workloads require careful handling
- Business logic can become coupled to route handlers without discipline
- Runtime performance depends on workload and dependency behavior

**Decision:** Accepted.

## Consequences

### Positive
- A consistent HTTP boundary
- OpenAPI documentation
- Easy integration with Python application components
- Straightforward endpoint testing
- Support for future streaming interfaces

### Negative
- Python runtime becomes part of the application stack
- Additional care is needed for CPU-bound and blocking work
- Cross-language integration with Java systems remains necessary

## Security Considerations

- Authenticate callers at appropriate entry points.
- Authorize business operations independently.
- Validate all external input.
- Never trust LLM output as an authorization decision.
- Do not expose internal stack traces or secrets.
- Apply request limits and timeouts where appropriate.

## Failure Modes

- Invalid request payloads
- Unhandled exceptions
- Blocking calls inside async endpoints
- Dependency timeouts
- Resource exhaustion
- Incorrect HTTP error mapping

## Observability

The HTTP boundary should eventually capture:

- Request ID
- Trace ID
- Route
- HTTP status
- Request duration
- Error category

Sensitive payloads, credentials, and private reasoning must not be logged.

## Revisit Criteria

Reconsider this decision when:

- Operational requirements favor another runtime.
- A Java-native AI application boundary provides a better fit.
- Performance testing identifies material limitations.
- Team ownership or platform standards require a different framework.

## Verification

- Health endpoint responds successfully.
- API tests pass.
- Business logic remains outside route handlers.
- OpenAPI documentation is available.
- CI validates the application.

## Related ADRs

- ADR-0001: Modular Foundation
- ADR-0004: Business Logic Independence
- ADR-0005: A2A Adoption Criteria
