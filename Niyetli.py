from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFrame, QListView, QLineEdit, QPushButton, QFileDialog, QMenuBar, QMenu, QStatusBar, QTextBrowser, QTextEdit
from PyQt5 import uic
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QResizeEvent
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QFile
from PyQt5.QtWidgets import QGroupBox

import sys

class WorkerThread(QThread):
    dialogAdded = pyqtSignal(str)

    def run(self):
        while True:
            text = input("Eklemek istediğiniz yazıyı girin: ")
            self.dialogAdded.emit(text)
class command_com_ui(QMainWindow):

    def write(self):
        print("Deneme")


    def addToValues(self):
        text = self.command.text()
        first_ui = UI()
        model = first_ui.dialogList.model()
        item = QStandardItem(text)
        model.appendRow(item)
        self.command.clear()

    def __init__(self):
        super(command_com_ui, self).__init__()
        uic.loadUi("command_communication.ui", self)
        self.setWindowOpacity(0.8)  # İstenilen saydamlık değerini ayarlayabilirsin (0.0 - 1.0)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.command = self.findChild(QLineEdit, "a_input")
        self.command.returnPressed.connect(self.addToValues)

class UI(QMainWindow):
    second_ui_file = "command_communication.ui"

    def command_com_state(self):
        if self.secondUI.isVisible():
            self.secondUI.setVisible(False)
        else:
            self.secondUI.setVisible(True)

    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("Niyetli.ui", self)
        self.label = self.findChild(QLabel, "label")
        self.dialogList = self.findChild(QListView, "Dialog_2")
        self.niyetli_logo = self.findChild(QLabel, "logo")
        self.hide_show = self.findChild(QPushButton, "niyetli_buton")
        self.container_history = self.findChild(QFrame, "container_history")
        self.comand_comm = self.findChild(QPushButton, "commandCenter_button")
        self.command = self.findChild(QLineEdit, "a_input")

        self.command.returnPressed.connect(self.addToValues)

        self.niyetli_buton.clicked.connect(self.ContainerState)
        self.commandCenter_button.clicked.connect(self.command_com_state)

        self.setWindowOpacity(0.8)  # İstenilen saydamlık değerini ayarlayabilirsin (0.0 - 1.0)

        self.pixmap = QPixmap("Niyetli_1.png")
        self.niyetli_logo.setPixmap(self.pixmap)
        self.niyetli_logo.setScaledContents(True)
        self.niyetli_logo.setAlignment(Qt.AlignJustify)  # Resmi ortalama

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
        self.openSecondUI()

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.adjustImageSize()

    def adjustImageSize(self):
        scaledPixmap = self.pixmap.scaled(self.niyetli_logo.size(), Qt.KeepAspectRatio)
        self.niyetli_logo.setPixmap(scaledPixmap)

    def addToValues(self):
        text = self.command.text()
        model = self.dialogList.model()
        item = QStandardItem(text)
        model.appendRow(item)
        self.command.clear()

    def addDialog(self, text):
        model = self.dialogList.model()
        item = QStandardItem(text)
        model.appendRow(item)

    def ContainerState(self):
        if self.container_history.isVisible():
            self.container_history.setVisible(False)
        else:
            self.container_history.setVisible(True)

    def openSecondUI(self):
        self.secondUI = command_com_ui()
        self.secondUI.show()


app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
