from raidify import parse_flag
from unittest import TestCase


#class RaidifyTest(TestCase):
#    def atomic_test_parse_flag(self):
#        output = parse_flag(['src', 'dst'])
#        self.assertEqual(output[0], 'src')
#        self.assertEqual(output[1], 'dst')
#        self.assertEqual(output[2], 0)
#
#        output = parse_flag(['--dryrun', 'src', 'dst'])
#        self.assertEqual(output[0], 'src')
#        self.assertEqual(output[1], 'dst')
#        self.assertEqual(output[2], 1 << 1)
#
#        output = parse_flag(['--help', 'src', 'dst'])
#        self.assertEqual(output[0], -1)
#
#        output = parse_flag(['--init', 'src', 'dst'])
#        self.assertEqual(output[0], 'src')
#        self.assertEqual(output[1], 'dst')
#        self.assertEqual(output[2], 1 << 2)
#
#        output = parse_flag(['--verbose', 'src', 'dst'])
#        self.assertEqual(output[0], 'src')
#        self.assertEqual(output[1], 'dst')
#        self.assertEqual(output[2], 1 << 3)

#    def complex_test_parse_flag(self):
#        output = parse_flag(['--dryrun', '--verbose', 'src', 'dst'])
#        self.assertEqual(output[0], 'src')
#        self.assertEqual(output[1], 'dst')
#        self.assertEqual(output[2], (1 << 3) + (1 << 1))
