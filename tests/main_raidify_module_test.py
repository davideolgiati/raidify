import os.path
import sys

from test_utils import temp_dirs
from raidify import setup
from unittest import TestCase


class MainRaidifyModuleTest(TestCase):
    @temp_dirs
    def test_just_dirs(self, source, destination):
        sys.argv = [source, destination]
        path, handler = setup(sys.argv)
        self.assertEqual(source, path)
        self.assertEqual(source, handler.path)
        self.assertEqual(destination, handler.dst)
        self.assertFalse(handler.dryrun)
        self.assertFalse(handler.verbose)

    @temp_dirs
    def test_verbose(self, source, destination):
        sys.argv = [source, destination, "--verbose"]
        path, handler = setup(sys.argv)
        self.assertEqual(source, path)
        self.assertEqual(source, handler.path)
        self.assertEqual(destination, handler.dst)
        self.assertFalse(handler.dryrun)
        self.assertTrue(handler.verbose)

    @temp_dirs
    def test_dryrun(self, source, destination):
        sys.argv = [source, destination, "--dryrun"]
        path, handler = setup(sys.argv)
        self.assertEqual(source, path)
        self.assertEqual(source, handler.path)
        self.assertEqual(destination, handler.dst)
        self.assertTrue(handler.dryrun)
        self.assertFalse(handler.verbose)

    @temp_dirs
    def test_dryrun_verbose(self, source, destination):
        sys.argv = [source, destination, "--dryrun", "--verbose"]
        path, handler = setup(sys.argv)
        self.assertEqual(source, path)
        self.assertEqual(source, handler.path)
        self.assertEqual(destination, handler.dst)
        self.assertTrue(handler.dryrun)
        self.assertTrue(handler.verbose)

    @temp_dirs
    def test_init_one_file(self, source, destination):
        sys.argv = [source, destination, "--init"]

        with open(
            os.path.join(source, "test.txt"), "w", encoding="UTF-8"
        ) as o_file:
            o_file.write("test di integrazione 1")
        self.assertTrue(os.path.isfile(os.path.join(source, "test.txt")))
        self.assertFalse(os.path.isfile(os.path.join(destination, "test.txt")))

        path, handler = setup(sys.argv)
        self.assertEqual(source, path)
        self.assertEqual(source, handler.path)
        self.assertEqual(destination, handler.dst)
        self.assertFalse(handler.dryrun)
        self.assertFalse(handler.verbose)

        self.assertTrue(os.path.isfile(os.path.join(destination, "test.txt")))
        with open(
            os.path.join(destination, "test.txt"), "r", encoding="UTF-8"
        ) as i_file:
            self.assertEqual(i_file.read(), "test di integrazione 1")

    @temp_dirs
    def test_init_one_dir_one_file(self, source, destination):
        sys.argv = [source, destination, "--init", "--verbose"]
        os.mkdir(os.path.join(source, "new_dir/"))
        with open(
            os.path.join(source, "new_dir/test.txt"), "w", encoding="UTF-8"
        ) as o_file:
            o_file.write("test di integrazione 2")
        self.assertTrue(os.path.isdir(os.path.join(source, "new_dir/")))
        self.assertTrue(
            os.path.isfile(os.path.join(source, "new_dir/test.txt"))
        )
        self.assertFalse(
            os.path.isfile(os.path.join(destination, "new_dir/test.txt"))
        )

        path, handler = setup(sys.argv)
        self.assertEqual(source, path)
        self.assertEqual(source, handler.path)
        self.assertEqual(destination, handler.dst)
        self.assertFalse(handler.dryrun)
        self.assertTrue(handler.verbose)

        self.assertTrue(os.path.isdir(os.path.join(destination, "new_dir/")))
        self.assertTrue(
            os.path.isfile(os.path.join(destination, "new_dir/test.txt"))
        )
        with open(
            os.path.join(destination, "new_dir/test.txt"),
            "r",
            encoding="UTF-8",
        ) as i_file:
            self.assertEqual(i_file.read(), "test di integrazione 2")
