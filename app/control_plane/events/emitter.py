from app.control_plane.events.client import NATSClient
from app.common.models.echo_event import EchoEvent


class Emitter:
    def __init__(self, nats_client: NATSClient):
        self.nats_client = nats_client

    async def publish(self, event_name: str, data: EchoEvent):
        # Serialize the EchoEvent to JSON
        await self.nats_client.publish(subject=event_name, data=data.model_dump_json())
        print(f"📤 Emitted event '{event_name}' with hash {data.hash[:8]}")
