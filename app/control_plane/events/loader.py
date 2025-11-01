from typing import Any, Awaitable, Callable, Dict, List
from app.control_plane.events.client import NATSClient
from app.common.models.echo_event import EchoEvent
from app.worker.spec_worker import handle_file_created, handle_file_modified
import json


class Loader:
    def __init__(self, nats_client: NATSClient):
        self.nats_client = nats_client
        self.handlers: Dict[str, Callable[[EchoEvent], Awaitable[None]]] = {}
        self.subscribed_subjects: List[str] = []

    async def register_handler(
        self, subject: str, handler: Callable[[EchoEvent], Awaitable[None]]
    ):
        """Register a handler for a specific subject and subscribe to it if not already."""
        if subject in self.subscribed_subjects:
            print(f"Already subscribed to '{subject}'")
            return

        async def wrapper(msg: Any):
            try:
                data = json.loads(msg.data.decode())
                event = EchoEvent(**data)
                await handler(event)
            except Exception as e:
                print(f"Error handling event on '{subject}': {e}")

        await self.nats_client.subscribe_event(subject, handler=wrapper)
        self.handlers[subject] = handler
        self.subscribed_subjects.append(subject)
        print(f"Registered handler for '{subject}'")

    async def unregister_all(self):
        """Unsubscribe all subjects and clear registry."""
        await self.nats_client.unsubscribe_all()
        self.handlers.clear()
        self.subscribed_subjects.clear()
        print("Cleared all subscriptions.")

    async def load_defaults(self):
        """Register default handlers for core system events."""
        # Register both subjects
        await self.register_handler("file.created", handle_file_created)
        await self.register_handler("file.modified", handle_file_modified)
        print("📡 Default file event handlers loaded.")
