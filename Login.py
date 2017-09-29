from PyQt5.QtCore import QThread
from PyQt5 import uic
from PyQt5.QtWidgets import (QDialog, QPushButton, QStatusBar, QLabel, QLineEdit,
                             QTextEdit, QApplication, QMainWindow, QMessageBox)
import sys
from instagram_web_api import Client, ClientCompatPatch, ClientError, ClientLoginError, ClientCookieExpiredError
from time import sleep
from APIManager import APIManager
from Follower import Follower
from UI import UI
import json
import os
import codecs


def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object


class Login(QDialog):
    SETTINGS_PATH = "settings"
    LOGIN_PATH = "lp"

    def __init__(self, Client=Client):
        super().__init__()
        uic.loadUi('login.ui', self)
        self.buttonBox.accepted.connect(self.try_to_log_in)
        self.client = Client
        if(os.path.exists(self.SETTINGS_PATH)):
            self.try_to_log_in()
            return
        if(os.path.exists(self.LOGIN_PATH)):
            self.use_cached_lp()
            self.try_to_log_in()
            return

        self.show()

    def try_to_log_in(self):
        login = self.login.text() or "empty"
        password = self.password.text() or "empty"
        self.log_in(
            login, password, on_login=lambda x: self.onlogin_callback(x),
            settings=self.getSettings())

    def log_in(self, login, password, on_login=None, settings=None):
        on_login = on_login if not settings else None
        settings = settings
        try:
            api = self.client(auto_patch=True, authenticate=True,
                              username=login, password=password,
                              on_login=on_login, settings=settings)
        except ClientError:
            self.failed_login = LoginFail(LoginFail.WRONG_CREDENTIALS)
            return
        except ClientCookieExpiredError:
            os.remove(self.SETTINGS_PATH)
            self.log_in(login, password,
                        on_login=lambda x: self.onlogin_callback(x))
            return
        if not settings:
            self.save_lp(login, password)
        self.create_main_window(api)
        return api

    def create_main_window(self, api):
        apiManager = APIManager(api)
        follower = Follower(apiManager)
        self.ui = UI(follower)

    def getSettings(self):
        if(not os.path.exists(self.SETTINGS_PATH)):
            return
        with open(self.SETTINGS_PATH) as data:
            cached_settings = json.load(data, object_hook=from_json)
        return cached_settings

    def save_lp(self, login, password):
        with open(self.LOGIN_PATH, "w") as lp:
            string = login + "\n" + password
            lp.write(string)

    def use_cached_lp(self):
        with open(self.LOGIN_PATH, "r") as lp:
            vm = lp.read().splitlines()
        self.login.setText(vm[0])
        self.password.setText(vm[1])

    def onlogin_callback(self, api):
        cache_settings = api.settings
        with open(self.SETTINGS_PATH, 'w') as outfile:
            json.dump(cache_settings, outfile, default=to_json)


class LoginFail(Login):
    WRONG_CREDENTIALS = "Неверный логин и пароль"
    UNKNOWN_ERROR = "Неизвестная ошибка, пожалуйста свяжитесь с разработчиком"
    COOKIE_EXPIRED = "Сессия закончилась"

    def __init__(self, message):
        super().__init__()
        self.error_label.setText(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Login()
    sys.exit(app.exec_())
