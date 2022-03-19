import logging
import os.path
import shutil
import sys
import time
from unittest import TestCase

from test_utils import temp_dirs
from watchdog.observers import Observer

from raidify import setup_var_from_args


class FilesystemTest(TestCase):
    @temp_dirs
    def test_create_sub_dir(self, source, destination):
        sys.argv = [source, destination, "--verbose"]
        self.assertFalse(os.path.isdir(os.path.join(source, "new_dir/")))
        self.assertFalse(os.path.isdir(os.path.join(destination, "new_dir/")))

        path, handler = setup_var_from_args(sys.argv)

        self.assertEqual(source, path)
        self.assertEqual(source, handler.path)
        self.assertEqual(destination, handler.dst)
        self.assertFalse(handler.dryrun)
        self.assertTrue(handler.verbose)

        observer = Observer()
        observer.schedule(handler, path, recursive=True)
        observer.start()

        os.mkdir(os.path.join(source, "new_dir/"))

        time.sleep(5)

        observer.stop()
        observer.join()

        self.assertTrue(os.path.isdir(os.path.join(source, "new_dir/")))
        self.assertTrue(os.path.isdir(os.path.join(destination, "new_dir/")))

    @temp_dirs
    def test_create_file(self, source, destination):
        sys.argv = [source, destination, "--verbose"]
        self.assertFalse(os.path.isfile(os.path.join(source, "new_file.txt")))
        self.assertFalse(os.path.isfile(os.path.join(destination, "new_file.txt")))

        path, handler = setup_var_from_args(sys.argv)

        self.assertEqual(source, path)
        self.assertEqual(source, handler.path)
        self.assertEqual(destination, handler.dst)
        self.assertFalse(handler.dryrun)
        self.assertTrue(handler.verbose)

        observer = Observer()
        observer.schedule(handler, path, recursive=True)
        observer.start()

        with open(
            os.path.join(source, "new_file.txt"), "w", encoding="UTF-8"
        ) as new_file:
            new_file.write("test integrazione 3")

        time.sleep(5)

        observer.stop()
        observer.join()

        self.assertTrue(os.path.isfile(os.path.join(source, "new_file.txt")))
        self.assertTrue(os.path.isfile(os.path.join(destination, "new_file.txt")))
        with open(
            os.path.join(destination, "new_file.txt"), "r", encoding="UTF-8"
        ) as new_dest_file:
            self.assertEqual(new_dest_file.read(), "test integrazione 3")

    @temp_dirs
    def test_delete_file(self, source, destination):
        sys.argv = [source, destination, "--verbose", "--init"]
        self.assertFalse(os.path.isdir(os.path.join(source, "new_file.txt")))
        self.assertFalse(os.path.isfile(os.path.join(destination, "new_file.txt")))

        with open(
            os.path.join(source, "new_file.txt"), "w", encoding="UTF-8"
        ) as new_file:
            new_file.write("test integrazione 3")

        path, handler = setup_var_from_args(sys.argv)

        self.assertEqual(source, path)
        self.assertEqual(source, handler.path)
        self.assertEqual(destination, handler.dst)
        self.assertFalse(handler.dryrun)
        self.assertTrue(handler.verbose)

        self.assertTrue(os.path.isfile(os.path.join(source, "new_file.txt")))
        self.assertTrue(os.path.isfile(os.path.join(destination, "new_file.txt")))

        observer = Observer()
        observer.schedule(handler, path, recursive=True)
        observer.start()

        os.remove(os.path.join(source, "new_file.txt"))
        time.sleep(5)

        observer.stop()
        observer.join()

        self.assertFalse(os.path.isfile(os.path.join(source, "new_file.txt")))
        self.assertFalse(os.path.isfile(os.path.join(destination, "new_file.txt")))

    @temp_dirs
    def test_move_file(self, source, destination):
        sys.argv = [source, destination, "--verbose", "--init"]
        self.assertFalse(os.path.isdir(os.path.join(source, "new_file.txt")))
        self.assertFalse(os.path.isfile(os.path.join(destination, "new_file.txt")))

        with open(
                os.path.join(source, "new_file.txt"), "w", encoding="UTF-8"
        ) as new_file:
            new_file.write("test integrazione 3")

        path, handler = setup_var_from_args(sys.argv)

        self.assertEqual(source, path)
        self.assertEqual(source, handler.path)
        self.assertEqual(destination, handler.dst)
        self.assertFalse(handler.dryrun)
        self.assertTrue(handler.verbose)

        self.assertTrue(os.path.isfile(os.path.join(source, "new_file.txt")))
        self.assertTrue(os.path.isfile(os.path.join(destination, "new_file.txt")))

        observer = Observer()
        observer.schedule(handler, path, recursive=True)
        observer.start()

        shutil.move(
            os.path.join(source, "new_file.txt"), os.path.join(source, "new_file2.txt")
        )
        time.sleep(5)

        observer.stop()
        observer.join()

        self.assertFalse(os.path.isfile(os.path.join(destination, "new_file.txt")))
        self.assertTrue(os.path.isfile(os.path.join(destination, "new_file2.txt")))

    @temp_dirs
    def test_modify_file(self, source, destination):
        sys.argv = [source, destination, "--verbose", "--init"]
        self.assertFalse(os.path.isdir(os.path.join(source, "new_file.txt")))
        self.assertFalse(os.path.isfile(os.path.join(destination, "new_file.txt")))

        with open(
            os.path.join(source, "new_file.txt"), "w", encoding="UTF-8"
        ) as new_file:
            new_file.write("test integrazione 3")

        path, handler = setup_var_from_args(sys.argv)

        self.assertEqual(source, path)
        self.assertEqual(source, handler.path)
        self.assertEqual(destination, handler.dst)
        self.assertFalse(handler.dryrun)
        self.assertTrue(handler.verbose)

        self.assertTrue(os.path.isfile(os.path.join(source, "new_file.txt")))
        self.assertTrue(os.path.isfile(os.path.join(destination, "new_file.txt")))

        observer = Observer()
        observer.schedule(handler, path, recursive=True)
        observer.start()

        with open(
            os.path.join(source, "new_file.txt"), "w", encoding="UTF-8"
        ) as new_file:
            new_file.write("test integrazione 4")
        time.sleep(5)

        observer.stop()
        observer.join()

        with open(
                os.path.join(destination, "new_file.txt"), "r", encoding="UTF-8"
        ) as new_file:
            self.assertEqual(new_file.read(), "test integrazione 4")
