import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from Login import Login


class TestLogin(unittest.TestCase):
    def test_should_(self):
        self.assertTrue(1)


if __name__ == '__main__':
    unittest.main()
