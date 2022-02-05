"""raidify.py is a python script to keep 2 folders synced."""
import sys
import time
import os.path
import argparse

from watchdog.observers import Observer

from filesystem import MyHandler


def logo(source, destination):
    """Function used to print the script banner (from file banner.txt)."""
    if os.path.abspath(os.curdir).endswith('/src'):
        file = "banner.txt"
    elif os.path.abspath(os.curdir).endswith('/tests'):
        file = "../src/banner.txt"
    else:
        file = "src/banner.txt"

    with open(os.path.join(os.path.abspath(os.curdir), file),
              "r",
              encoding="UTF-8") as banner_source:
        banner = banner_source.read()

    return f"{banner}\n[src] : {source}\n[dst] : {destination}"


def parse_flag(flags):
    """Function used to parse script flags."""
    parser = argparse.ArgumentParser(
        description='raidify.py is a python script to keep 2 folders synced.'
    )

    # Informazioni sulle directory da duplicare
    parser.add_argument('src', type=str,
                        help='The source directory to clone')
    parser.add_argument('dst', type=str,
                        help='The destination directory')

    # Flag opzionali
    parser.add_argument(
        '-d', '--dryrun', action='store_true',
        help='Just print, does not modify filesystem - WIP')
    parser.add_argument(
        '-i', '--init', action='store_true',
        help='Sync the two folders before starting the watchdog')
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='Print everything during execution')

    parsed_args = parser.parse_args(flags)

    if not os.path.isdir(parsed_args.src):
        parser.error(
            f"{parsed_args.src} is not recognized as a "
            f"valid directory in the filesystem")

    if not os.path.isdir(parsed_args.dst):
        parser.error(
            f"{parsed_args.dst} is not recognized as a "
            f"valid directory in the filesystem")

    return parsed_args


def setup(argv):
    """Function used to initialize MyHandler class"""
    flags = parse_flag(argv)
    logo(flags.src, flags.dst)
    _handler = MyHandler(
        flags.src, flags.dst,
        args={
            'init': flags.init,
            'dryrun': flags.dryrun,
            'verbose': flags.verbose
        })
    return flags.src, _handler


if __name__ == '__main__':
    observer = Observer()
    path, handler = setup(sys.argv)
    observer.schedule(handler,
                      path,
                      recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
