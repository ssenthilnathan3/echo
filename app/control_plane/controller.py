import asyncio
import os
import sys
from dotenv import load_dotenv

# Ensure top-level path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.control_plane.events.client import NATSClient
from app.control_plane.events.emitter import Emitter
from app.control_plane.events.loader import Loader
from app.control_plane.watcher.manager import WatcherManager
from app.common.models.echo_event import EchoEvent

# Load environment variables
load_dotenv()

NATS_BASE_URL = os.getenv("NATS_BASE_URL")
NATS_BASE_PORT = os.getenv("NATS_BASE_PORT")


async def main():
    # Initialize NATS and subsystems
    nats_client = NATSClient(base_url=NATS_BASE_URL, port=NATS_BASE_PORT)
    await nats_client.init_nats()

    emitter = Emitter(nats_client)
    loader = Loader(nats_client)
    watcher = WatcherManager()

    await loader.load_defaults()

    watch_path = "echoes"
    try:
        watcher.register_path(watch_path)
    except FileNotFoundError:
        print(f"Creating '{watch_path}' since it doesn’t exist.")
        os.makedirs(watch_path, exist_ok=True)
        watcher.register_path(watch_path)

    watcher.start_one("echoes")

    async def emit_file_event(event_name: str, src_path: str):
        event = EchoEvent(
            name=event_name,
            source="watcher",
            payload={"src": src_path},
        )
        await emitter.publish(event_name, event)

    # Monkey-patch watcher’s log adding to emit events
    original_add_log = watcher._add_log
    loop = asyncio.get_event_loop()

    def patched_add_log(name: str, log: str):
        original_add_log(name, log)

        # Try to extract file path (e.g., "echoes/echo.yaml") from the log string
        parts = log.split(": ")
        if len(parts) > 1:
            src_path = parts[1].split(" at ")[0]
        else:
            src_path = "unknown"

        if "created" in log:
            asyncio.run_coroutine_threadsafe(
                emit_file_event("file.created", src_path), loop
            )

        elif "modified" in log:
            asyncio.run_coroutine_threadsafe(
                emit_file_event("file.modified", src_path), loop
            )

    watcher._add_log = patched_add_log

    print("🚀 Controller initialized. Watching for file changes...\n")

    try:
        while True:
            watcher.log_active_watchers()
            await asyncio.sleep(5)
    except KeyboardInterrupt:
        print("🛑 Stopping all watchers...")
        watcher.stop_all()
        await loader.unregister_all()


if __name__ == "__main__":
    asyncio.run(main())
