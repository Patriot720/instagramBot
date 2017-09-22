from PyQt5.QtCore import QThread
from PyQt5 import uic
from PyQt5.QtWidgets import (QDialog, QPushButton, QStatusBar, QLabel, QLineEdit,
                             QTextEdit, QApplication, QMainWindow, QMessageBox)
import sys
from instagram_web_api import Client, ClientCompatPatch, ClientError, ClientLoginError
from time import sleep
from APIManager import APIManager
from Follower import Follower
from UI import UI


class Login(QDialog):
    def __init__(self, Client=Client):
        super().__init__()
        uic.loadUi('login.ui', self)
        self.buttonBox.accepted.connect(self.click)
        self.client = Client
        self.show()

    def click(self):
        login = self.login.text() or "empty"
        password = self.password.text() or "empty"
        try:
            api = self.client(auto_patch=True, authenticate=True,
                              username=login, password=password)
        except ClientError:
            self.failed_login = LoginFail(LoginFail.WRONG_CREDENTIALS_MSG)
            return
        except:
            self.failed_login = LoginFail(LoginFail.UNKNOWN_ERROR)

        apiManager = APIManager(api)
        follower = Follower(apiManager)
        self.ui = UI(follower)


class LoginFail(Login):
    WRONG_CREDENTIALS_MSG = "Неверный логин и пароль"
    UNKNOWN_ERROR = "Неизвестная ошибка, пожалуйста свяжитесь с разработчиком"

    def __init__(self, message):
        super().__init__()
        self.error_label.setText(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Login()
    sys.exit(app.exec_())
