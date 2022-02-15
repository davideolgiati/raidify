"""Module containing filesystem interface logic."""
import logging
import os  # os.path.relpath
import shutil

from watchdog.events import FileSystemEventHandler  # <--

# La classe 'MyHandler' serve per gestire gli eventi registrati
# dalla libreria watchdog.
# Estende la classe 'FileSystemEventHandler', controlla ogni
# cambiamento senza distinzione


class MyHandler(FileSystemEventHandler):

    """Main filesystem watchdog class."""

    # nel costruttore salvo il valore di path, che rappresenta
    # la directory principale da osservare
    def __init__(self, src, dst, args):
        """Class constructor."""
        self.path = src
        logging.info(f"Source Path : src={self.path}")
        self.dst = dst
        logging.info(f"Destination Path : dst={self.dst}")
        self.dryrun = args["dryrun"]
        logging.info(f"Dryrun flag : args[\"dryrun\"]={self.dryrun}")
        self.verbose = args["verbose"]
        logging.info(f"Verbose flag : args[\"verbose\"]={self.verbose}")
        logging.info(f"Init Flag : args[\"init\"]={args['init']}")
        if args["init"]:  # init flag attivo
            dirs, files = self.dir_walk(self.path, self.dst, [], [])
            if self.verbose:
                print("\nDIRS to be duplicated: ")
            for current_dir in dirs:
                test = os.path.isdir(current_dir)
                if not test:
                    if self.verbose:
                        print("\t" + current_dir)
                    os.mkdir(current_dir)

            if self.verbose:
                print("\nFILES to be duplicated: ")
            for dst_file in files:
                src = os.path.join(src, os.path.relpath(dst_file, dst))
                if not os.path.isfile(dst_file):
                    if self.verbose:
                        print("\t" + dst_file)
                    shutil.copy(src, dst_file)

    @staticmethod
    def dir_walk(main, dst, dirs, files):
        """Method used to explore a directory in order to track file."""
        for dir_path, dir_names, file_names in os.walk(main):
            for current_dir in dir_names:
                new_path = os.path.join(dst, current_dir)
                if (new_path not in dirs) and current_dir != ".":
                    dirs.append(new_path)
            for _file in file_names:
                rel_path = os.path.relpath(dir_path, main)
                new_path = os.path.join(dst, rel_path)
                if rel_path == ".":
                    new_file = os.path.join(dst, _file)
                else:
                    new_file = os.path.join(new_path, _file)
                files.append(new_file)
        return dirs, files

    def on_created(self, event):
        print(event.src_path)
        rel_path = os.path.relpath(event.src_path, self.path)
        dst_obj = os.path.join(self.dst, rel_path)
        if event.is_directory:
            os.mkdir(dst_obj)
        else:
            shutil.copy(event.src_path, dst_obj)
