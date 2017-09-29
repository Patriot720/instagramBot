# -*- coding: utf8 -*-
from PyQt5.QtCore import QThread
from PyQt5 import uic
from PyQt5.QtWidgets import (QDialog, QPushButton, QStatusBar, QLabel, QLineEdit,
                             QTextEdit, QApplication, QMainWindow, QMessageBox)
import os.path
import time
import sys
from Follower import Follower
from io import StringIO


class UI(QMainWindow):
    label_types = [
        "Ник",
        "Хештег без #",
        "Хештег без #",
        "Ничего"
    ]

    def __init__(self, follower):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.follower = follower
        self.thread = QThread()
        self.follower.moveToThread(self.thread)
        self.thread.started.connect(self.follower.start)
        self.follower.end.connect(self.on_end)
        self.follower.mid.connect(self.on_mid)
        self.type_chooser.currentIndexChanged.connect(self.on_index_change)
        self.start_btn.clicked.connect(self.on_start)
        self.show()

    def on_index_change(self, index):
        self.type_label.setText(self.label_types[index])

    def launch(self):
        self.follower.set_index(self.type_chooser.currentIndex())
        self.follower.set_name(self.choose_box.text())
        self.thread.start()

    def on_end(self, msg):
        self.progress_box.append(msg)
        self.start_btn.setText("Старт")
        self.start_btn.setChecked(False)
        self.stop_thread()

    def on_mid(self, msg):
        self.progress_box.append(msg)

    def stop_thread(self):
        self.follower.stop()
        self.thread.quit()
        self.thread.wait()

    def on_start(self, checked):
        if(checked):
            self.start_btn.setText("Стоп")
            self.launch()
        else:
            self.start_btn.setText("Старт")
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

    tbinfofile = StringIO()
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
