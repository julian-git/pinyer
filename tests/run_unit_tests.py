import unittest
import sys
sys.path.append('..')
from build_ip import make_lp_file, find_pinya
from ineqs import ip_ineqs

class IPTest(unittest.TestCase):

    def test_build_ip(self):
        f = open('test.lp', 'r')
        prescribed = dict([(9, 0), (17, 5)])
        castellers_in_position = dict()
        position_data = dict()
        obj_val = dict()
        ineqs = []
        ip_ineqs(castellers_in_position, position_data, obj_val, ineqs, prescribed)
        self.assertEqual(make_lp_file(obj_val, ineqs), f.read())

    def test_find_pinya(self):
        f = open('test.find_pinya', 'r')
        prescribed = dict([(9, 0), (17, 5)])
        self.assertEqual(str(find_pinya(prescribed)) + "\n", f.read())
        

unittest.main() # Calling from the command line invokes all tests

