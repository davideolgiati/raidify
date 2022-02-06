import os.path
import sys
import time
from unittest import TestCase
from watchdog.observers import Observer

from test_utils import temp_dirs

from raidify import setup_var_from_args


class FilesystemTest(TestCase):
    @temp_dirs
    def test_create_sub_dir(self, source, destination):
        sys.argv = [source, destination, "--verbose"]
        self.assertFalse(os.path.isdir(os.path.join(source, "new_dir/")))
        self.assertFalse(os.path.isfile(os.path.join(destination, "new_dir/")))

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

        time.sleep(2)

        observer.stop()
        observer.join()

        self.assertTrue(os.path.isdir(os.path.join(source, "new_dir/")))
        self.assertTrue(os.path.isdir(os.path.join(destination, "new_dir/")))
