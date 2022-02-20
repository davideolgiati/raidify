"""Module containing filesystem interface logic."""
import os
import shutil
import logging

from watchdog.events import FileSystemEventHandler


class MyHandler(FileSystemEventHandler):

    """Main filesystem watchdog event handling class."""

    # nel costruttore salvo il valore di path, che rappresenta
    # la directory principale da osservare
    def __init__(self, src, dst, args):
        """Class constructor."""
        self.path = src
        logging.debug("Source Path : src=%s", self.path)
        self.dst = dst
        logging.debug("Destination Path : dst=%s", self.dst)
        self.dryrun = args["dryrun"]
        logging.debug("Dryrun flag : args[\"dryrun\"]=%s", self.dryrun)
        self.verbose = args["verbose"]
        logging.debug("Verbose flag : args[\"verbose\"]=%s", self.verbose)
        logging.debug("Init Flag : args[\"init\"]=%s", args['init'])
        if args["init"]:  # init flag attivo
            dirs, files = self.dir_walk(self.path, self.dst, [], [])
            for destination_object_to_duplicate in dirs:
                logging.info(
                    "Init directory process -- duplicating directory %s",
                    destination_object_to_duplicate)
                os.mkdir(destination_object_to_duplicate)

            for destination_object_to_duplicate in files:
                logging.info("Init directory process -- duplicating file %s",
                             destination_object_to_duplicate)
                shutil.copy(
                    os.path.join(src,
                                 os.path.relpath(
                                     destination_object_to_duplicate,
                                     dst)),
                    destination_object_to_duplicate
                )

    @staticmethod
    def dir_walk(main, dst, dirs, files):
        """Method used to explore a directory in order to track file."""
        logging.debug("Scan of directory %s", main)
        for dir_path, dir_names, file_names in os.walk(main):
            for current_dir in dir_names:
                logging.debug("Found directory %s in %s", current_dir, main)
                new_path = os.path.join(dst, current_dir)
                if (new_path not in dirs) and current_dir != ".":
                    logging.debug(
                        "Directory %s added to new discovered directories",
                        new_path)
                    dirs.append(new_path)
                else:
                    logging.debug(
                        "Directory %s already exists on the filesystem, "
                        "skipping",
                        new_path)
            for _file in file_names:
                logging.debug("Found file %s in %s", _file, main)
                rel_path = os.path.relpath(dir_path, main)
                new_path = os.path.join(dst, rel_path)
                new_file = os.path.join(new_path, _file)

                if os.path.isfile(new_file):
                    logging.debug(
                        "File %s already exixts on filesystem, skipping",
                        new_file)
                else:
                    logging.debug(
                        "File %s added to new discovered files",
                        new_file)
                    files.append(new_file)
        return dirs, files

    def on_created(self, event):
        rel_path = os.path.relpath(event.src_path, self.path)
        dst_obj = os.path.join(self.dst, rel_path)
        try:
            if event.is_directory:
                if not os.path.isdir(dst_obj):
                    logging.info(
                        "A creation event has been detected in %s "
                        "for directory %s",
                        self.path, event.src_path)
                    os.mkdir(dst_obj)
                    logging.info(
                        "The directory %s has been duplicated "
                        "successfully to %s",
                        event.src_path, dst_obj)
            else:
                if not os.path.isfile(dst_obj):
                    logging.info(
                        "A creation event has been detected in %s "
                        "for file %s",
                        self.path, event.src_path)
                    shutil.copy(event.src_path, dst_obj)
                    logging.info(
                        "The file %s has been duplicated "
                        "successfully to %s",
                        event.src_path, dst_obj)
        except Exception as error:
            logging.error(
                "The following error occurred while duplicating %s to "
                "%s : %s",
                event.src_path, dst_obj, str(error))

    def on_deleted(self, event):
        rel_path = os.path.relpath(event.src_path, self.path)
        dst_obj = os.path.join(self.dst, rel_path)
        try:
            if event.is_directory:
                if os.path.isdir(dst_obj):
                    logging.info(
                        "A deletion event has been detected in %s for "
                        "directory %s",
                        self.path, event.src_path)
                    shutil.rmtree(dst_obj)
                    logging.info(
                        "The directory %s has been deleted "
                        "successfully",
                        dst_obj)
            else:
                if os.path.isfile(dst_obj):
                    logging.info(
                        "A deletion event has been detected in %s for "
                        "file %s",
                        self.path, event.src_path)
                    os.remove(dst_obj)
                    logging.info(
                        "The file %s has been deleted successfully",
                        dst_obj)
        except Exception as error:
            logging.error(
                "The following error occurred while deleting %s : %s",
                dst_obj, str(error))

    def on_modified(self, event):
        pass

    def on_moved(self, event):
        rel_path_from = os.path.relpath(event.src_path, self.path)
        dst_obj_from = os.path.join(self.dst, rel_path_from)
        rel_path_to = os.path.relpath(event.dest_path, self.path)
        dst_obj_to = os.path.join(self.dst, rel_path_to)
        try:
            if event.is_directory:
                if os.path.isdir(dst_obj_from) and \
                        not os.path.isdir(dst_obj_to):
                    logging.info(
                        "A move event has been detected in %s for "
                        "directory %s",
                        self.path, event.src_path)
                    shutil.move(dst_obj_from, dst_obj_to,
                                copy_function=shutil.copytree)
                    logging.info(
                        "The directory %s has been moved "
                        "successfully to %s",
                        dst_obj_from, dst_obj_to)
            else:
                if os.path.isfile(dst_obj_from) and \
                        not os.path.isfile(dst_obj_to):
                    logging.info(
                        "A move event has been detected in %s for "
                        "file %s",
                        self.path, event.src_path)
                    shutil.move(dst_obj_from, dst_obj_to)
                    logging.info(
                        "The file %s has been moved successfully "
                        "to %s",
                        dst_obj_from, dst_obj_to)
        except Exception as error:
            logging.error(
                "The following error occurred while moving %s : %s",
                dst_obj_from, str(error))
