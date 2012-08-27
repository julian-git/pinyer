import unittest
import build_ip

class IPTest(unittest.TestCase):

    def test_build_ip(self):
        res = ['c1p1 + c2p1 <= 1', 'c1p2 + c2p2 <= 1', 'c9p3 + c10p3 <= 1', '150.0 c1p1 + 155.0 c2p1 - 150.0 c1p2 - 155.0 c2p2 <= 10.0', '150.0 c1p2 + 155.0 c2p2 - 190.0 c9p3 - 195.0 c10p3 <= 8.0', '150.0 c1p1 + 155.0 c2p1 - 190.0 c9p3 - 195.0 c10p3 <= 7.0', '65.0 c1p2 + 70.0 c2p2 >= 65.0']
        self.assertEqual(build_ip.build_an_ip(), res)

unittest.main()
