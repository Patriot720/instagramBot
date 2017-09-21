from PyQt5.QtCore import QThread
from PyQt5 import uic
from PyQt5.QtWidgets import (QDialog, QPushButton, QStatusBar, QLabel, QLineEdit,
                             QTextEdit, QApplication, QMainWindow, QMessageBox)
import sys
from time import sleep


class Login(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui', self)
        self.buttonBox.accepted.connect(self.click)
        print('l')
        self.show()

    def click(self):
        sleep(2)
        self.log_dialog = LoginWrong()


class LoginWrong(Login):
    WRONG_CREDENTIALS_MSG = "Неверный логин и пароль"

    def __init__(self):
        super().__init__()
        self.error_label.setText(self.WRONG_CREDENTIALS_MSG)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Login()
    sys.exit(app.exec_())
