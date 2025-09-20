import time
import os
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

class ChangeHandler(FileSystemEventHandler):
    """
    Handles file system events and triggers the ingest script.
    """
    def on_any_event(self, event):
        # On any event, run the ingest script
        print(f"Detected change: {event.event_type} on {event.src_path}. Re-ingesting...")
        subprocess.run(["python", "scripts/ingest.py"])

def start_watcher():
    """
    Starts the file system watcher.
    """
    observer = Observer()
    observer.schedule(ChangeHandler(), config.DATA_DIRECTORY, recursive=True)
    observer.start()
    print(f"Watching for changes in '{config.DATA_DIRECTORY}'...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_watcher()