from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QListView, QFileDialog, QMenuBar, QMenu, QStatusBar, QTextBrowser, QTextEdit
from PyQt5 import uic
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal

import sys

class WorkerThread(QThread):
    dialogAdded = pyqtSignal(str)

    def run(self):
        while True:
            text = input("Eklemek istediğiniz yazıyı girin: ")
            self.dialogAdded.emit(text)

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("Niyetli.ui", self)

        self.label = self.findChild(QLabel, "label")
        self.dialogList = self.findChild(QListView, "Dialog")
        self.niyetli_logo = self.findChild(QLabel, "logo")
        self.pixmap = QPixmap("Niyetli_1.png")
        self.setWindowOpacity(0.8)  # İstenilen saydamlık değerini ayarlayabilirsin (0.0 - 1.0)

        self.niyetli_logo.setPixmap(self.pixmap)

        model = QStandardItemModel()
        values = ['one', 'two', 'three']

        for i in values:
            item = QStandardItem(i)
            model.appendRow(item)

        self.dialogList.setModel(model)

        self.show()

        self.workerThread = WorkerThread()
        self.workerThread.dialogAdded.connect(self.addDialog)
        self.workerThread.start()

    def addDialog(self, text):
        model = self.dialogList.model()
        item = QStandardItem(text)
        model.appendRow(item)


app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
