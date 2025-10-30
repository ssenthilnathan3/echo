**Questions**

1) How does the runtime know whether a specific tool (e.g., git.clone, llm.summarize) actually exists?
Without this, we risk:
  Runtime failures – missing implementations
  Silent no-ops – when a spec calls a tool that doesn’t exist

**Proposed Solution**

To prevent mismatches between declared and available tools:
  - Static Tool Registry
      Maintain an in-memory (or managed) registry of all tools available to the runtime.
      This ensures quick lookups and avoids surprises during execution.

  - Control Plane RPC Validation
      On startup or deployment, validate tools by making an RPC call to the control plane to confirm their implementations exist.

  - Stub-based Lazy Validation (inspired by MCP)
      Workers periodically pull “tool stubs” from the control plane — lightweight representations of tool definitions — and validate availability at runtime. This allows flexibility while avoiding heavy synchronization.

**Design Decision**

Every worker must register itself with the Control Plane, including metadata about:
  - Its identity and capabilities
  - The tools it can execute
This registration happens before entering the execution context, ensuring both sides (control plane and worker) share a consistent view of available tools.
