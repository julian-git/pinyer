import sys
sys.path.append('/opt/gurobi500/linux32/lib/python2.7')

import unittest
import build_ip
import solve_ip

class IPTest(unittest.TestCase):

    def test_build_ip(self):
        f = open('tests/test.lp', 'r')
        participation = dict([(9, 0), (17, 5)])
        castellers_in_position = dict()
        position_data = dict()
        self.assertEqual(build_ip.make_lp_file(build_ip.ip_ineqs(castellers_in_position, position_data, participation)), f.read())

    def test_solve_ip(self):
        f = open('tests/test.solutions', 'r')
        #from gurobipy import read
        self.assertEqual(str(solve_ip.get_solutions("tests/test.lp")), f.read())

    def test_find_pinya(self):
        f = open('tests/test.find_pinya', 'r')
        participation = dict([(9, 0), (17, 5)])
        self.assertEqual(str(build_ip.find_pinya(participation)) + "\n", f.read())
        

unittest.main() # Calling from the command line invokes all tests

