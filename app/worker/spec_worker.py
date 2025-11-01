from app.common.models.echo_event import EchoEvent
from app.common.utils.loader import load
import os


async def handle_file_created(event: EchoEvent):
    try:
        if not event or not event.payload:
            return

        src = event.payload.get("path") or event.payload.get("src")
        if not src or not os.path.exists(src):
            return

        # Ignore directories and non-YAML files
        if not os.path.isfile(src):
            return
        if not (src.endswith(".yaml") or src.endswith(".yml")):
            return
        if src.endswith((".tmp", ".swp", "~")):
            return

        loaded_file = load(src)
        if loaded_file:
            print(f"[Loader] Loaded new file: {src}")
            return True
    except Exception as e:
        print(f"Error in handle_file_created: {e}")


async def handle_file_modified(event: EchoEvent):
    try:
        if not event or not event.payload:
            return

        src = event.payload.get("path") or event.payload.get("src")
        if not src or not os.path.exists(src):
            return

        # Ignore directories and non-YAML files
        if not os.path.isfile(src):
            return
        if not (src.endswith(".yaml") or src.endswith(".yml")):
            return
        if src.endswith((".tmp", ".swp", "~")):
            return

        loaded_file = load(src)
        if loaded_file:
            print(f"[Loader] Reloaded modified file: {src}")
            return True
    except Exception as e:
        print(f"Error in handle_file_modified: {e}")
