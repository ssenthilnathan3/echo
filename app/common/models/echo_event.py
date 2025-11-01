import hashlib
import json
from typing import Dict, Optional
from datetime import datetime, timezone
from typing_extensions import override
from pydantic import BaseModel, Field, computed_field


class EchoEvent(BaseModel):
    name: str = Field(..., description="Name of the event")
    source: str = Field(..., description="Kind of event (secret, spec, etc.)")
    payload: Optional[Dict] = Field(
        default=None, description="Optional payload attached to the event"
    )
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @computed_field
    @property
    def hash(self) -> str:
        ts = self.timestamp.replace(tzinfo=timezone.utc).isoformat(
            timespec="milliseconds"
        )
        payload_str = (
            json.dumps(self.payload, sort_keys=True, separators=(",", ":"))
            if self.payload is not None
            else ""
        )
        data = f"{ts}|{self.name}|{self.source}|{payload_str}"
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

    @override
    def __str__(self) -> str:
        """Readable string representation of the event."""
        return (
            f"[{self.timestamp.isoformat(timespec='milliseconds')}] "
            f"{self.source}:{self.name} "
            f"{json.dumps(self.payload, sort_keys=True) if self.payload else '{}'} "
            f"#{self.hash[:8]}"
        )

    @override
    def __repr__(self) -> str:
        """Compact debug-friendly version."""
        return f"EchoEvent(name={self.name!r}, source={self.source!r}, hash={self.hash[:8]!r})"
