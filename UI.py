# -*- coding: utf8 -*-
from PyQt5.QtCore import QThread
from PyQt5 import uic
from PyQt5.QtWidgets import (QDialog, QPushButton, QStatusBar, QLabel, QLineEdit,
                             QTextEdit, QApplication, QMainWindow, QMessageBox)
import os.path
import time
import sys
from Follower import Follower


class UI(QMainWindow):
    label_types = [
        "Ник",
        "Хештег без #",
        "Хештег без #",
        "Ничего"
    ]
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.follower = Follower()
        self.thread = QThread()
        self.follower.moveToThread(self.thread)
        self.thread.started.connect(self.follower.start)
        self.follower.api_end.connect(self.on_api_end)
        self.follower.end.connect(self.on_end)
        self.follower.mid.connect(self.on_mid)
        self.type_chooser.currentIndexChanged.connect(self.on_index_change)
        self.start_btn.clicked.connect(self.on_start)
        lp = self.getLPFromCache()
        if(lp):
            self.login.setText(lp[0])
            self.password.setText(lp[1])
        self.show()

    def getLPFromCache(self):
        vm = []
        if(os.path.isfile("login.txt")):
            f = open("login.txt", "r")
            vm = f.read().splitlines()
            f.close()
            if(len(vm) != 2):
                vm = []
        return vm

    def on_index_change(self, index):
        self.type_label.setText(self.label_types[index])

    def on_api_end(self, msg):
        self.progress_box.append(msg)

    def launch(self):
        self.follower.login = self.login.text()
        self.follower.password = self.password.text()
        self.follower.index = self.type_chooser.currentIndex()
        self.follower.text = self.choose_box.text()
        self.thread.start()

    def on_end(self, msg):
        self.progress_box.append(msg)
        self.enableBtn()
        self.start_btn.setChecked(False)
        self.stop_thread()

    def enableBtn(self):
        self.start_btn.setText("Старт")

    def disableBtn(self):
        self.start_btn.setText("Стоп")

    def on_mid(self, msg):
        self.progress_box.append(msg)

    def saveLP(self):
        login = self.login.text()
        password = self.password.text()
        f = open("login.txt", 'w')
        f.write(login + "\n" + password)
        f.close()

    def stop_thread(self):
        self.follower.stop()
        self.thread.quit()
        self.thread.wait()

    def on_start(self, checked):
        if(checked):
            self.saveLP()
            self.launch()
            self.disableBtn()
        else:
            self.enableBtn()
            self.stop_thread()


def excepthook(excType, excValue, tracebackobj):
    """
    Global function to catch unhandled exceptions.

    @param excType exception type
    @param excValue exception value
    @param tracebackobj traceback object
    """
    separator = '-' * 80
    logFile = "simple.log"
    notice = \
        """An unhandled exception occurred. Please report the problem\n"""\
        """using the error reporting dialog or via email to <%s>.\n"""\
        """A log has been written to "%s".\n\nError information:\n""" % \
        ("yourmail at server.com", "")
    versionInfo = "0.0.1"
    timeString = time.strftime("%Y-%m-%d, %H:%M:%S")

    tbinfofile = cStringIO.StringIO()
    traceback.print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()
    errmsg = '%s: \n%s' % (str(excType), str(excValue))
    sections = [separator, timeString, separator, errmsg, separator, tbinfo]
    msg = '\n'.join(sections)
    try:
        f = open(logFile, "w")
        f.write(msg)
        f.write(versionInfo)
        f.close()
    except IOError:
        pass
    errorbox = QMessageBox()
    errorbox.setText(str(notice) + str(msg) + str(versionInfo))
    errorbox.exec_()


sys.excepthook = excepthook

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UI()
    sys.exit(app.exec_())
