import datetime
import os
import time
from unittest.loader import VALID_MODULE_NAME
from typing_extensions import override
from watchdog.events import (
    DirCreatedEvent,
    DirModifiedEvent,
    FileCreatedEvent,
    FileModifiedEvent,
)
from watchdog.observers import Observer
from os.path import basename
from typing import Any, Dict, List, Optional
from pydantic import ValidationError
from watchdog.events import FileSystemEventHandler
from app.common.models.watcher import WatcherConfig


class WatcherManager(FileSystemEventHandler):
    def __init__(self):
        self.watchers: List[WatcherConfig] = []
        self.observers: Dict[str, Any] = {}

    def register_path(self, path: str):
        if not os.path.exists(os.path.abspath(path)):
            raise FileNotFoundError(
                f"Path does not exist: {path}, {os.path.abspath(path)}"
            )
        if not any(w.watch_path == path for w in self.watchers):
            print("Path already exists in watcher")

        folder_name = basename(path.rstrip("/"))
        watcher = WatcherConfig(
            name=folder_name,
            watch_path=path,
            duration=datetime.datetime.now(),
            logs=[],
            active=False,
        )
        self.watchers.append(watcher)
        print(f"Path '{path}' registered successfully. {os.path.abspath(path)}")

    def add_watcher(self, watcher_data):
        try:
            # Ensure watcher_data is a dict before unpacking
            if isinstance(watcher_data, WatcherConfig):
                watcher = watcher_data
            else:
                watcher = WatcherConfig(**watcher_data)

            # Check for duplicate paths
            if any(w.watch_path == watcher.watch_path for w in self.watchers):
                print(f"Watcher for path '{watcher.watch_path}' already exists.")
                return

            # Check for duplicate names
            if any(w.name == watcher.name for w in self.watchers):
                print(f"Watcher '{watcher.name}' already exists.")
                return

            self.watchers.append(watcher)
            print(f"Registered watcher '{watcher.name}' successfully.")

        except ValidationError as e:
            print(f"Invalid watcher config: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    @override
    def on_created(self, event: DirCreatedEvent | FileCreatedEvent):
        watcher_name = self._get_watcher_for_path(
            os.fsdecode(event.src_path)
            if isinstance(event.src_path, bytes)
            else event.src_path
        )
        if watcher_name:
            log_entry = f"File created: {event.src_path} at {datetime.datetime.now()}"
            self._add_log(watcher_name, log_entry)

    @override
    def on_modified(
        self, event: DirModifiedEvent | FileModifiedEvent
    ):  # Override for modifications
        watcher_name = self._get_watcher_for_path(
            os.fsdecode(event.src_path)
            if isinstance(event.src_path, bytes)
            else event.src_path
        )
        if watcher_name:
            log_entry = f"File modified: {event.src_path} at {datetime.datetime.now()}"
            self._add_log(watcher_name, log_entry)

    def _get_watcher_for_path(self, path: str) -> Optional[str]:
        for w in self.watchers:
            if w.watch_path and path.startswith(w.watch_path):
                return w.name
        return None

    def _add_log(self, name: str, log: str):
        watcher = next((w for w in self.watchers if w.name == name), None)
        if watcher:
            watcher.logs.append(log)

    def start_all(self):
        for watcher in self.watchers:
            if not watcher.active:
                self._start_watcher(watcher)
        print("All watchers started.")

    def start_one(self, name: str):
        watcher = next((w for w in self.watchers if w.name == name), None)
        if watcher:
            watcher.active = True
            self._start_watcher(watcher)
            print(f"Watcher '{name}' started.")

    def _start_watcher(self, watcher: WatcherConfig):
        observer = Observer()
        event_handler = self  # This class handles events
        if watcher.watch_path:
            _ = observer.schedule(event_handler, watcher.watch_path, recursive=True)
        observer.start()
        self.observers[watcher.name] = observer

    def stop_all(self):
        for _, observer in self.observers.items():
            observer.stop()
            observer.join()
        self.observers.clear()
        for watcher in self.watchers:
            watcher.active = False
        print("All watchers stopped.")

    def stop_one(self, name: str):
        observer = self.observers.get(name)
        if observer:
            observer.stop()
            observer.join()
            del self.observers[name]
        watcher = next((w for w in self.watchers if w.name == name), None)
        if watcher:
            watcher.active = False
        print(f"Watcher '{name}' stopped.")

    def log_active_watchers(self):
        active_watchers = [w for w in self.watchers if w.active]

        if not active_watchers:
            print("No active watchers.")
            return

        print("\n=== Active Watchers ===")
        for watcher in active_watchers:
            print(f"\n🕵️ Watcher: {watcher.name}")
            print(f"📁 Path: {watcher.watch_path}")
            print(f"⏱️  Started: {watcher.duration}")
            print(f"🟢 Active: {watcher.active}")
            print("🧾 Logs:")
            if watcher.logs:
                for log in watcher.logs[-5:]:  # last 5 logs
                    print(f"   • {log}")
            else:
                print("   (no logs yet)")
