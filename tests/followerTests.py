# -*- coding: utf8 -*-
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import ../db.py
from Follower import Follower
import unittest


class followerSpec(unittest.TestCase):
    def test_test(self):
        self.assertEqual(2, 2)
    
if __name__ == '__main__':
    unittest.main()