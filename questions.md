# Questions

## 1. How does the runtime know whether a specific tool (e.g., `git.clone`, `llm.summarize`) actually exists?

Without this validation, we risk:

- **Runtime failures** – missing implementations
- **Silent no-ops** – when a spec calls a tool that doesn’t exist

---

## Proposed Solution

To prevent mismatches between declared and available tools:

### Static Tool Registry
- Maintain an **in-memory (or managed) registry** of all tools available to the runtime.
- Ensures **fast lookups** and avoids surprises during execution.

### Control Plane RPC Validation
- On **startup or deployment**, validate tools by making an **RPC call** to the Control Plane.
- Confirms that implementations exist and are up to date.

### Stub-based Lazy Validation (inspired by MCP)
- Workers **periodically pull “tool stubs”** from the Control Plane — lightweight representations of tool definitions.
- They **validate availability at runtime**, offering flexibility while avoiding heavy synchronization.

---

## 2. How are specs discovered and registered into the Control Plane?

Should this be done manually (e.g., via a function call or REST API that triggers an RPC)?
Or should there be an **introspective watcher** that observes the subsystem?

---
## Proposed Solution

### Watcher-based Discovery
- Continuously watches a directory tree (e.g., `/specs/`).
- Whenever a `.yaml` or `.yml` spec **appears, changes, or disappears**, it:
  - **Validates** the spec
  - **Loads** it
  - **Re-registers** it with the Control Plane
