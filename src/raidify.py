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
            "{} is not recognized as a valid directory in the filesystem"
            .format(parsed_args.src))

    if not os.path.isdir(parsed_args.dst):
        parser.error(
            "{} is not recognized as a valid directory in the filesystem"
            .format(parsed_args.dst))

    return parsed_args


if __name__ == '__main__':
    observer = Observer()
    result = parse_flag(sys.argv)
    source_path = result.src
    destination_path = result.dst

    logo(source_path, destination_path)

    observer.schedule(
        MyHandler(source_path,
                  destination_path,
                  result[2]),
        source_path,
        recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
