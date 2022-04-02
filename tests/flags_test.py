from unittest import TestCase

from tests.test_utils import temp_dirs

from raidify.utils import parse_flag


class FlagsTest(TestCase):
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
            output = parse_flag(["./wrong_source", destination])
            self.fail()
        except:
            pass

    @temp_dirs
    def test_wrong_dst(self, source, destination):
        try:
            output = parse_flag([source, "./wrong_destination"])
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
        output = parse_flag([source, destination, "--dryrun"])
        self.assertEqual(output.src, source)
        self.assertEqual(output.dst, destination)
        self.assertFalse(output.init)
        self.assertFalse(output.verbose)
        self.assertTrue(output.dryrun)

    @temp_dirs
    def test_init_flags(self, source, destination):
        # No flags, just directories
        output = parse_flag([source, destination, "--init"])
        self.assertEqual(output.src, source)
        self.assertEqual(output.dst, destination)
        self.assertTrue(output.init)
        self.assertFalse(output.verbose)
        self.assertFalse(output.dryrun)

    @temp_dirs
    def test_verbose_flags(self, source, destination):
        # No flags, just directories
        output = parse_flag([source, destination, "--verbose"])
        self.assertEqual(output.src, source)
        self.assertEqual(output.dst, destination)
        self.assertFalse(output.init)
        self.assertTrue(output.verbose)
        self.assertFalse(output.dryrun)
