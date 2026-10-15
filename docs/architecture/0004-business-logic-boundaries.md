# ADR-0004: Business Logic Independence from Transport Frameworks

## Status
Accepted

## Context

EIAN will eventually expose insurance capabilities through multiple communication mechanisms.

Potential integrations include:

- FastAPI HTTP endpoints
- Internal Python function calls
- REST/gRPC services
- LangGraph workflows
- A2A agent interfaces
- MCP-connected enterprise tools

If business logic is embedded directly into transport handlers, the same business rules may need to be duplicated across multiple integrations.

For example, claim eligibility rules must remain consistent whether invoked by a FastAPI endpoint or by a future Claims Agent.

## Decision

Adopt **Ports and Adapters (Hexagonal Architecture) principles**.

Business rules must be independent of transport and infrastructure frameworks.

Architecture:

```text
FastAPI / Future A2A Adapter
             |
             v
      Application Service
             |
             v
       Domain Logic
             |
             v
       Domain Ports
             |
             v
 Infrastructure Adapters
```

The dependency direction must favor domain and application abstractions.

### Layer Responsibilities

**Domain Layer**
- Insurance entities
- Value objects
- Business invariants
- Domain-specific rules

**Application Layer**
- Business use cases
- Coordination of domain operations
- Transaction boundaries where appropriate
- Calls through abstract ports

**Infrastructure Layer**
- Database adapters
- External REST/gRPC clients
- LLM providers
- Vector database integrations
- MCP clients where appropriate

**Transport Layer**
- FastAPI endpoints
- Future A2A protocol handlers
- Input/output mapping
- Transport-specific error handling

The domain layer must not import FastAPI, LangGraph, A2A, MCP, or database-specific libraries.

## Example

The business operation:

```text
Analyze claim eligibility
```

must remain conceptually separate from:

```text
POST /api/v1/claims/analyze
```

and from a future A2A capability such as:

```text
analyze_claim_eligibility
```

Both interfaces may invoke the same application service.

## Alternatives

### Alternative 1: Business logic inside HTTP routes

**Pros**
- Fast initial implementation
- Fewer abstractions

**Cons**
- Framework coupling
- Difficult unit testing
- Logic duplication
- Harder future transport changes

**Decision:** Rejected.

### Alternative 2: Framework-specific service architecture

**Pros**
- Convenient framework integration
- Potentially less boilerplate

**Cons**
- Domain logic may become dependent on framework types
- Future integration boundaries may require substantial refactoring

**Decision:** Not preferred for core domain rules.

### Alternative 3: Ports and Adapters

**Pros**
- Testability
- Transport independence
- Clear dependency direction
- Replaceable infrastructure
- Easier integration with future A2A adapters

**Cons**
- Additional interfaces and mapping
- More design discipline
- Risk of unnecessary abstraction for trivial operations

**Decision:** Accepted.

## Consequences

### Positive
- Business rules can be reused.
- Domain tests remain deterministic.
- Transport protocols can evolve independently.
- Infrastructure components can be replaced.
- Existing Java services can remain authoritative downstream systems.

### Negative
- Additional mapping between transport and domain models
- More files and interfaces
- Potential overengineering if abstractions are introduced prematurely

## Security Considerations

- Authorization must be enforced by trusted application and infrastructure components.
- Transport authentication alone must not replace business authorization.
- LLM output must not override business invariants.
- Sensitive operations require explicit policy checks.
- Validate remote-agent results before using them in business operations.

## Failure Modes

- Framework imports in domain code
- Domain models exposing transport-specific DTOs
- Duplicated business rules
- Infrastructure exceptions leaking into API responses
- Incorrect exception translation
- Unauthorized business operations

## Observability

Application services should eventually record:

- Business operation identifier
- Correlation identifier
- Operation outcome
- Duration
- Failure category

Sensitive business data must be excluded from logs unless explicitly justified and protected.

## Revisit Criteria

Reconsider the degree of abstraction when:

- An interface has only one trivial implementation and no meaningful boundary.
- Mapping overhead becomes disproportionate.
- Performance evidence requires targeted optimization.
- Domain ownership changes.

The architectural principle remains valid even when individual abstractions are simplified.

## Verification

- Domain tests run without starting FastAPI.
- Domain code does not depend on transport frameworks.
- Application services are independently testable.
- Infrastructure dependencies are replaceable through ports.
- Business rules are not duplicated in protocol handlers.

## Related ADRs

- ADR-0001: Modular Foundation
- ADR-0002: FastAPI Application Boundary
- ADR-0005: A2A Adoption Criteria
