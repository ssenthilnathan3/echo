from typing import Any, Callable, List, Optional
import nats


class NATSClient:
    def __init__(self, base_url: Optional[str], port: Optional[str]) -> None:
        self.nc = None
        self.base_url = base_url
        self.port = port
        self.subscribers: List[Any] = []
        self.subscribed_events: List[str] = []

    async def init_nats(self) -> None:
        if not self.base_url or not self.port:
            raise ValueError("NATS base_url and port must be provided")

        self.nc = await nats.connect(f"nats://{self.base_url}:{self.port}")
        print(f"Connected to NATS at nats://{self.base_url}:{self.port}")

    async def publish(self, subject: str, data: Any) -> None:
        if not self.nc:
            raise ValueError("Initialize NATS first by calling init_nats()")
        await self.nc.publish(subject, str(data).encode())

    async def subscribe_event(self, event: str, handler: Callable[[Any], Any | None]):
        event = event.strip()
        if not event:
            raise ValueError("Event name must not be empty")

        if not self.nc:
            raise ValueError("Initialize NATS first by calling init_nats()")

        if event in self.subscribed_events:
            raise ValueError(
                f"'{event}' already subscribed. Unsubscribe first or use a different subject."
            )

        try:
            subscriber = await self.nc.subscribe(event, cb=handler)
            self.subscribers.append(subscriber)
            self.subscribed_events.append(event)
            print(f"📡 Subscribed to '{event}'")
        except Exception as e:
            print(f"Failed to subscribe to '{event}': {e}")

    async def unsubscribe_event(self, event: str):
        event = event.strip()
        if not event:
            raise ValueError("Event name must not be empty")

        if not self.nc:
            raise ValueError("Initialize NATS first by calling init_nats()")

        try:
            idx = self.subscribed_events.index(event)
        except ValueError as e:
            raise ValueError(f"Event '{event}' not found in subscribed events") from e

        sub = self.subscribers[idx]
        try:
            await self.nc.unsubscribe(sub.sid)
            self.subscribers.pop(idx)
            self.subscribed_events.pop(idx)
            print(f"Unsubscribed from '{event}'")
        except Exception as e:
            print(f"Failed to unsubscribe from '{event}': {e}")

    async def observe(self, subject_pattern: str, handler: Callable[[Any], Any]):
        if not self.nc:
            raise ValueError("Call init_nats() before observe().")

        if subject_pattern in self.subscribed_events:
            print(f"Already observing '{subject_pattern}'")
            return

        sub = await self.nc.subscribe(subject_pattern, cb=handler)
        self.subscribers.append(sub)
        self.subscribed_events.append(subject_pattern)
        print(f"Observing pattern '{subject_pattern}'")

    async def unsubscribe_all(self):
        try:
            for i, sub in enumerate(self.subscribers):
                await self.nc.unsubscribe(sub.sid)
                self.subscribers.pop(i)
                self.subscribed_events.pop(i)
            print("Unsubscribed all events")
        except Exception as e:
            print(f"Failed to unsubscribe from : {e}")
