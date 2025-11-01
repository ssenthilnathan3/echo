from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional


class WatcherConfig(BaseModel):
    name: str = Field(..., description="Name of the watcher")
    duration: datetime = Field(default_factory=datetime.now)
    watch_path: Optional[str] = Field(default=None, description="Path to watch")
    logs: List[str] = Field(default_factory=list)
    active: bool = Field(default=False, description="Whether the watcher is running")
