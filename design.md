## Design Choices

**Watcher**:
- A Watcher in Echo is a self-registering, event-emitting microcontroller — managed by the Control Plane’s runtime registry, with standardized lifecycle hooks and version-aware reconciliation.

---
**Capability Handshake**:
- Event-driven and **version-aware**
- **Conceptual Flow**:
  1. Watcher produces a structured `SpecEvent`.
  2. It pushes that event into an internal **event bus** (in-memory, queue, or RPC).
  3. The **Control Plane** dispatches the event to the appropriate handler — usually the **Registry**.
  4. The **Registry** mutates its internal state accordingly.
