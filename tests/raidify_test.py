import tempfile

from raidify import parse_flag, logo
from unittest import TestCase


def temp_dirs(func):
    """Decorator to generate temporary directories."""

    def wrap(*args, **kwargs):
        with tempfile.TemporaryDirectory() as source:
            with tempfile.TemporaryDirectory() as destination:
                func(*args, **kwargs,
                     source=str(source), destination=str(destination))

    return wrap


class RaidifyTest(TestCase):
    @temp_dirs
    def test_no_args(self, source, destination):
        # No args at all
        try:
            output = parse_flag([])
            self.fail()
        except:
            pass

    @temp_dirs
    def test_just_one_directory(self, source, destination):
        # Just one directory
        try:
            output = parse_flag([source])
            self.fail()
        except:
            pass

    @temp_dirs
    def test_wrong_src(self, source, destination):
        # Non existing directories
        try:
            output = parse_flag(['./wrong_source', destination])
            self.fail()
        except:
            pass

    @temp_dirs
    def test_wrong_dst(self, source, destination):
        try:
            output = parse_flag([source, './wrong_destination'])
            self.fail()
        except:
            pass

    @temp_dirs
    def test_no_flags(self, source, destination):
        # No flags, just directories
        output = parse_flag([source, destination])
        self.assertEqual(output.src, source)
        self.assertEqual(output.dst, destination)
        self.assertFalse(output.init)
        self.assertFalse(output.verbose)
        self.assertFalse(output.dryrun)

    @temp_dirs
    def test_dryrun_flags(self, source, destination):
        # No flags, just directories
        output = parse_flag([source, destination, '--dryrun'])
        self.assertEqual(output.src, source)
        self.assertEqual(output.dst, destination)
        self.assertFalse(output.init)
        self.assertFalse(output.verbose)
        self.assertTrue(output.dryrun)

    @temp_dirs
    def test_init_flags(self, source, destination):
        # No flags, just directories
        output = parse_flag([source, destination, '--init'])
        self.assertEqual(output.src, source)
        self.assertEqual(output.dst, destination)
        self.assertTrue(output.init)
        self.assertFalse(output.verbose)
        self.assertFalse(output.dryrun)

    @temp_dirs
    def test_verbose_flags(self, source, destination):
        # No flags, just directories
        output = parse_flag([source, destination, '--verbose'])
        self.assertEqual(output.src, source)
        self.assertEqual(output.dst, destination)
        self.assertFalse(output.init)
        self.assertTrue(output.verbose)
        self.assertFalse(output.dryrun)

    @temp_dirs
    def test_logo(self, source, destination):
        # No flags, just directories
        output = parse_flag([source, destination, '--verbose'])
        banner = logo(output.src, output.dst)
        with open('src/banner.txt', 'r') as in_file:
            bnr = in_file.read()
            self.assertEqual(banner,
                             '{}\n[src] : {}\n[dst] : {}'.format(
                                 bnr, source, destination))
