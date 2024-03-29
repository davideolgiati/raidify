"""raidify.py is a python script to keep 2 folders synced."""
import argparse
import logging
import os.path
import re
import sys
import time

from watchdog.observers import Observer

from filesystem import MyHandler


def is_path_like(path_to_test):
    """Function to check if a string is path-like using RE"""
    return bool(re.search(r'^(/)?(\w)+((/)(\w)+)*$',
                          path_to_test))


def logo(source, destination):
    """Function used to print the script banner (from file banner.txt)."""
    if os.path.abspath(os.curdir).endswith("/src"):
        file = "banner.txt"
    elif os.path.abspath(os.curdir).endswith("/tests"):
        file = "../src/banner.txt"
    else:
        file = "src/banner.txt"

    with open(
            os.path.join(os.path.abspath(os.curdir), file),
            "r",
            encoding="UTF-8"
    ) as banner_source:
        banner = banner_source.read()

    return f"{banner}\n[src] : {source}\n[dst] : {destination}"


def parse_flag(flags):
    """Function used to parse script flags."""
    parser = argparse.ArgumentParser(
        description="raidify.py is a python script to keep 2 folders synced."
    )

    # Informazioni sulle directory da duplicare
    parser.add_argument("src", type=str, help="The source directory to clone")
    parser.add_argument("dst", type=str, help="The destination directory")

    # Flag opzionali
    parser.add_argument(
        "-d",
        "--dryrun",
        action="store_true",
        help="Just print, does not modify filesystem - WIP",
    )
    parser.add_argument(
        "-i",
        "--init",
        action="store_true",
        help="Sync the two folders before starting the watchdog",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print everything during execution",
    )

    parsed_args = parser.parse_args(args=flags, namespace=None)

    if not (is_path_like(parsed_args.src) and os.path.isdir(parsed_args.src)):
        parser.error(
            f"{parsed_args.src} is not recognized as a "
            f"valid directory in the filesystem"
        )

    if not (is_path_like(parsed_args.dst) and os.path.isdir(parsed_args.dst)):
        parser.error(
            f"{parsed_args.dst} is not recognized as a "
            f"valid directory in the filesystem"
        )

    return parsed_args


def setup_var_from_args(cli_args):
    """Function used to initialize MyHandler class"""
    flags = parse_flag(cli_args)
    logo(flags.src, flags.dst)
    _handler = MyHandler(
        flags.src,
        flags.dst,
        args={
            "init": flags.init,
            "dryrun": flags.dryrun,
            "verbose": flags.verbose,
        },
    )
    return flags.src, _handler


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
