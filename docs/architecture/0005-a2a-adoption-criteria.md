# ADR-0005: Introduce A2A Only When Independent-Agent Interoperability Is Justified

## Status
Accepted

## Context

EIAN will eventually contain independently owned insurance agent systems.

Examples include:

- Support Agent System
- Policy Agent System
- Claims Agent System
- Billing Agent System
- Fraud Investigation Agent System
- Document Intelligence Agent System

These systems may have separate deployment lifecycles, internal orchestration, tools, security policies, and owners.

Before A2A, independent systems could communicate through REST, gRPC, messaging, webhooks, custom RPC, or framework-specific agent integrations.

These techniques remain valid.

However, independently developed agentic systems may require custom integration contracts for:

- Agent capability discovery
- Skill descriptions
- Message exchange
- Long-running task lifecycle
- Progress updates
- Artifact exchange
- Asynchronous interaction
- Interoperability between agent frameworks

A2A addresses common agent interoperability concerns.

It does not eliminate the need for application security, durable state, domain authorization, or operational controls.

## Decision

EIAN will introduce **Agent2Agent (A2A)** only when a communication boundary genuinely requires interoperability between independent agentic systems.

A2A adoption must be justified through explicit architectural criteria.

### Adoption Criteria

Before introducing A2A, evaluate:

1. Are the communicating components independent agentic systems?
2. Do they have independently managed capabilities?
3. Is capability discovery useful or required?
4. Is a standardized task lifecycle needed?
5. Are long-running or asynchronous agent interactions expected?
6. Is interoperable message or artifact exchange required?
7. Are independent deployment and ownership boundaries present?
8. Would REST or gRPC be simpler?
9. Would messaging be more appropriate?
10. Would an internal LangGraph node or subgraph be sufficient?
11. Is MCP actually the required interface instead?
12. Can the required authentication, authorization, and trust controls be implemented safely?

A2A is not mandatory merely because two components are called agents.

## Communication Decision Guide

| Scenario | Preferred Initial Approach |
|---|---|
| Two functions in one process | Direct function call |
| Internal deterministic workflow | Application code or LangGraph |
| Internal supervisor with worker nodes | LangGraph or framework-native orchestration |
| Simple remote service request | REST or gRPC |
| Event-driven business integration | Kafka or another message broker |
| Expose tools and context to an AI application | MCP where justified |
| Independent agentic systems requiring interoperability | Consider A2A |

These are starting recommendations, not universal rules.

## Example: When A2A Is NOT Required

```text
Support Workflow
      |
      v
Claims Validation Function
      |
      v
Policy Lookup Function
```

If all components belong to the same application and are controlled by one workflow, ordinary application calls or LangGraph nodes are sufficient.

Introducing A2A here would add protocol, network, and operational complexity without solving a meaningful interoperability problem.

## Example: When A2A May Be Justified

```text
Support Agent System
        |
        | A2A
        v
Claims Agent System
        |
        | A2A
        v
Policy Agent System
```

Assume these systems:

- Are independently deployed
- Have separate owners
- Advertise agent capabilities
- May perform long-running tasks
- Need interoperable task and result exchange
- Have independent internal implementations

A2A becomes a reasonable architectural choice.

The Claims Agent should delegate to the Policy Agent only when policy interpretation is actually needed.

## A2A vs MCP

A2A and MCP solve different primary problems.

**A2A**
- Communication between independent agentic systems
- Agent discovery and capability description
- Message and task exchange
- Long-running agent collaboration

**MCP**
- Access to tools, resources, and contextual capabilities
- Standardized integration between AI applications and tool/resource providers

Combined architecture:

```text
Support Agent System
         |
        A2A
         |
         v
Claims Agent System
         |
        MCP
         |
         v
Claims Tools / Enterprise APIs
```

The Claims Agent may internally use LangGraph, RAG, MCP, ordinary Python code, or Java microservices.

The calling agent should not need to understand those internal implementation details.

## Alternatives

### Alternative 1: Custom REST integration

**Pros**
- Familiar
- Simple for fixed contracts
- Mature operational tooling

**Cons**
- Agent-specific task semantics must be designed separately
- Discovery and artifact contracts may become custom
- Repeated adapters may be required

**Decision:** Preferred for simple service interactions; not universally sufficient for independent-agent interoperability.

### Alternative 2: gRPC

**Pros**
- Strong typed contracts
- Efficient communication
- Streaming support

**Cons**
- Agent capability discovery and task semantics still require application-level design

**Decision:** Retained where suitable.

### Alternative 3: Messaging

**Pros**
- Asynchronous delivery
- Decoupling
- Buffering
- Durable messaging options

**Cons**
- Agent discovery and collaboration contracts are not inherently standardized
- Delivery does not automatically guarantee business-level exactly-once execution

**Decision:** Retained for event-driven integration.

### Alternative 4: Framework-specific multi-agent integration

**Pros**
- Convenient internal orchestration
- Shared framework abstractions
- Lower integration overhead within one system

**Cons**
- Potential framework coupling
- Limited cross-framework interoperability

**Decision:** Preferred for internal workflows where appropriate.

### Alternative 5: A2A

**Pros**
- Standardized agent interoperability concepts
- Capability discovery
- Task-oriented interaction
- Support for long-running collaboration
- Reduced need for custom agent-specific contracts

**Cons**
- Additional protocol complexity
- More network boundaries
- Distributed state and failure handling
- Security and trust requirements
- Potential latency and resource overhead

**Decision:** Accepted for justified independent-agent boundaries.

## Consequences

### Positive
- Interoperable agent communication
- Clearer agent capability contracts
- Standardized collaboration semantics
- Independent internal agent implementations
- Reduced framework-specific coupling

### Negative
- More distributed-system complexity
- Additional protocol compatibility requirements
- Remote task state management
- Increased observability requirements
- Additional security boundaries
- Potentially greater latency and cost

## Security Considerations

An Agent Card advertises capabilities; it does not authorize their use.

Every A2A interaction must enforce appropriate authentication and authorization.

Additional requirements:

- Validate remote agent identity.
- Maintain trusted endpoint configuration.
- Use least-privilege credentials.
- Enforce business authorization independently of LLM reasoning.
- Treat remote messages and artifacts as untrusted input.
- Validate artifact schemas.
- Prevent prompt injection from causing unauthorized tool execution.
- Limit delegation depth.
- Detect delegation loops.
- Apply timeouts and resource budgets.
- Protect tenant isolation.
- Avoid unsafe credential forwarding.

## Failure Modes

Potential failures include:

- Agent discovery failure
- Unsupported protocol version
- Unknown skill
- Remote agent unavailable
- Task timeout
- Task failure
- Invalid task transition
- Invalid artifact
- Streaming disconnection
- Duplicate mutation
- Authorization failure
- Delegation loop
- Malicious remote agent

The owning system must define recovery responsibilities for each failure.

## State Ownership

EIAN must distinguish:

- User conversation state
- Local LangGraph workflow state
- Remote A2A task state
- Persistent insurance business state

The remote agent owns its task lifecycle.

The calling agent owns its local orchestration state.

Authoritative business systems own persistent business records.

State must not be duplicated without a clear consistency strategy.

## Retries and Idempotency

Read-only operations may be retryable under an appropriate policy.

Mutation operations require additional safeguards.

Example:

```text
Support Agent
      |
      v
Claims Agent
      |
      v
Initiate Claim Review
      |
      v
Timeout
      |
      v
Retry
```

Without idempotency, the retry might create duplicate review requests.

EIAN must use business operation identifiers, idempotency keys where supported, duplicate detection, and authoritative business-state checks.

A transport timeout must not be interpreted as proof that the remote operation failed.

## Observability

Cross-agent interactions should eventually capture:

- Trace ID
- User request ID
- Local workflow run ID
- Remote task ID
- Calling agent
- Remote agent
- Capability or skill
- Task state transitions
- Delegation count
- Latency
- Retries
- Failures
- Artifact validation results

OpenTelemetry will be considered for distributed tracing.

Sensitive user data, credentials, and private model reasoning must not be logged.

## Revisit Criteria

Reconsider A2A adoption when:

- The remote system is no longer independent.
- A simple REST contract satisfies the requirement.
- Interoperability requirements disappear.
- Latency or operational cost becomes unacceptable.
- A protocol compatibility or security requirement cannot be satisfied.
- A new independently owned agent requires standardized collaboration.

## Verification

Before implementing an A2A boundary:

1. Document the business capability.
2. Document the independent ownership boundary.
3. Explain why simpler communication approaches are insufficient.
4. Verify the selected official A2A specification version.
5. Define discovery and capability contracts.
6. Define authentication and authorization.
7. Define task-state ownership.
8. Define failure recovery and idempotency.
9. Add deterministic protocol contract tests.
10. Add observability and security checks.

## Related ADRs

- ADR-0001: Modular Foundation
- ADR-0002: FastAPI Application Boundary
- ADR-0004: Business Logic Independence
