import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from Login import Login
app = QApplication(sys.argv)
from instagram_web_api import ClientError
from MockClasses import APIMock


def mockClient(**kwargs):
    if(kwargs['username'] and kwargs['password']):
        return APIMock()
    else:
        raise ClientError("Wrong shiet")


class TestLogin(unittest.TestCase):
    SAMPLE_TEXT = "text"

    def setUp(self):
        self.login = Login(mockClient)

    def test_setText(self):
        self.login.login.setText(self.SAMPLE_TEXT)
        text = self.login.login.text()
        self.assertEqual(text, self.SAMPLE_TEXT)

    def test_password_text(self):
        self.login.password.setText(self.SAMPLE_TEXT)
        text = self.login.password.text()
        self.assertEqual(text, self.SAMPLE_TEXT)

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


if __name__ == '__main__':
    unittest.main()
