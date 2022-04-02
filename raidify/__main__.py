"""raidify.py is a python script to keep 2 folders synced."""
import logging
import sys
import time

from watchdog.observers import Observer
from utils import setup_var_from_args

if __name__ == "__main__":
    observer = Observer()
    logging.basicConfig(level=logging.INFO)
    path, handler = setup_var_from_args(sys.argv[1:])
    observer.schedule(handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
