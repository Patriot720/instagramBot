import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from Login import Login
from MockClasses import mockClient
app = QApplication(sys.argv)
from instagram_web_api import Client


class TestLogin(unittest.TestCase):
    SAMPLE_TEXT = "text"

    def setUp(self):
        self.clear_cache_files()
        self.login = Login(mockClient)

    def tearDown(self):
        self.clear_cache_files()

    def clear_cache_files(self):
        self.path = os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))) + "/"
        if(os.path.exists(self.path + Login.SETTINGS_PATH)):
            os.remove(self.path + Login.SETTINGS_PATH)
        if(os.path.exists(self.path + Login.LOGIN_PATH)):
            os.remove(self.path + Login.LOGIN_PATH)

    def test_failed_login_should_be_undefined(self):
        self.assertFalse(hasattr(self.login, "failed_login"))

    def test_accept_should_create_failed_login_on_empty_input(self):
        self.login.buttonBox.accepted.emit()
        failed_login = hasattr(self.login, "failed_login")
        self.assertTrue(failed_login)

    def test_accept_should_create_UI_on_right_input(self):
        self.login.login.setText(self.SAMPLE_TEXT)
        self.login.password.setText(self.SAMPLE_TEXT)
        self.login.buttonBox.accepted.emit()
        ui = hasattr(self.login, "ui")
        self.assertTrue(ui)

    def test_should_save_settings_on_login(self):
        self.login.login.setText(self.SAMPLE_TEXT)
        self.login.password.setText(self.SAMPLE_TEXT)
        self.login.buttonBox.accepted.emit()
        self.assertTrue(os.path.isfile(self.login.SETTINGS_PATH))

    def test_should_login_if_settings_exists(self):
        f2 = open(Login.SETTINGS_PATH, "w")
        f2.write('"%%"')
        f2.close()
        self.login = Login(mockClient)
        self.assertTrue(hasattr(self.login, "ui"))

    def test_should_login_if_login_exists(self):
        with open(Login.LOGIN_PATH, "w") as f:
            f.write("l\np")
        self.login = Login(mockClient)
        self.assertTrue(hasattr(self.login, "ui"))

    def test_should_not_login_if_no_settings(self):
        self.assertFalse(hasattr(self.login, "ui"))

    def test_should_save_lp(self):
        self.login.login.setText(self.SAMPLE_TEXT)
        self.login.password.setText(self.SAMPLE_TEXT)
        self.login.buttonBox.accepted.emit()
        self.assertTrue(os.path.isfile(self.login.LOGIN_PATH))


if __name__ == '__main__':
    unittest.main()
