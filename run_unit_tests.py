import unittest
import build_ip

class IPTest(unittest.TestCase):

    def test_build_ip(self):
        f = open('tests/test.lp', 'r')
        self.assertEqual(build_ip.lp_format(build_ip.ip_ineqs()) + "\n", f.read())

unittest.main() # Calling from the command line invokes all tests

