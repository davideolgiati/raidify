from unittest import TestCase

from test_utils import temp_dirs

from raidify import logo, parse_flag


class BannerTest(TestCase):
    @temp_dirs
    def test_logo(self, source, destination):
        # No flags, just directories
        output = parse_flag([source, destination, "--verbose"])
        banner = logo(output.src, output.dst)
        with open("src/banner.txt", "r", encoding="UTF-8") as in_file:
            bnr = in_file.read()
            self.assertEqual(
                banner,
                "{}\n[src] : {}\n[dst] : {}".format(bnr, source, destination),
            )
