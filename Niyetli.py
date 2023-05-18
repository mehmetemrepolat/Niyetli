from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QListView, QFileDialog, QMenuBar, QMenu, QStatusBar, QTextBrowser, QTextEdit
from PyQt5 import uic
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtGui import QPixmap

import sys

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("Niyetli.ui", self)

        self.label = self.findChild(QLabel, "label")
        self.dialogList = self.findChild(QListView, "Dialog")

        self.Logo = QLabel()

        self.pixmap = QPixmap("Niyetli_1.png")
        self.Logo.setPixmap(self.pixmap)

        model = QStandardItemModel()
        values = ['one', 'two', 'three']

        for i in values:
            item = QStandardItem(i)
            model.appendRow(item)

        self.dialogList.setModel(model)

        self.show()


app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
