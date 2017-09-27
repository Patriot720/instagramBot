import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from UI import UI
from MockClasses import *
app = QApplication(sys.argv)
from instagram_web_api import Client
from time import sleep


class TestUI(unittest.TestCase):
    SAMPLE_TEXT = "text"

    def setUp(self):
        self.mock = mockFollower()
        self.ui = UI(self.mock)

    def test_should_start_on_button(self):
        QTest.mouseClick(self.ui.start_btn, Qt.LeftButton)
        QTest.qWait(100)
        self.assertTrue(hasattr(self.mock, "started"))

    def test_should_stop_on_button(self):
        QTest.mouseClick(self.ui.start_btn, Qt.LeftButton)
        QTest.mouseClick(self.ui.start_btn, Qt.LeftButton)
        self.assertTrue(hasattr(self.mock, "started"))

    def test_start_should_send_2_parameters(self):
        self.ui.choose_box.setText(self.SAMPLE_TEXT)
        QTest.mouseClick(self.ui.start_btn, Qt.LeftButton)
        QTest.qWait(100)
        self.assertEqual(self.mock.index, 0)
        self.assertEqual(self.mock.name, self.SAMPLE_TEXT)

    def test_should_launch_funcs_depending_on_index(self):
        self.ui.type_chooser.setCurrentIndex(1)
        QTest.mouseClick(self.ui.start_btn, Qt.LeftButton)
        QTest.qWait(100)
        self.assertTrue(hasattr(self.mock, "func2_launched"))
        self.assertFalse(hasattr(self.mock, "func1_launched"))

    def test_should_append_to_when_mid_emited(self):
        self.mock.mid.emit(self.SAMPLE_TEXT)
        self.assertTrue(self.ui.progress_box.document().characterCount() > 1)


if __name__ == '__main__':
    unittest.main()
