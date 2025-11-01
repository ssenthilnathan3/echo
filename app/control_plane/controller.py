from app.common.models.watcher import WatcherConfig
from app.control_plane.watcher.manager import WatcherManager
import os
import time

if __name__ == "__main__":
    watcher = WatcherManager()

    watcher.register_path("echoes")

    watcher.start_one("echoes")

    try:
        while True:
            watcher.log_active_watchers()
            time.sleep(3)
    except KeyboardInterrupt:
        print("\nStopping all watchers...")
        watcher.stop_all()
