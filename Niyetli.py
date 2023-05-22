from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFrame, QListView, QLineEdit, QPushButton, QCommandLinkButton, QFileDialog, QMenuBar, QMenu, QStatusBar, QTextBrowser, QTextEdit
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QResizeEvent
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QFile, QPoint
from PyQt5.QtWidgets import QGroupBox

from database.db_connector import Database
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

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = event.globalPos() - self.oldPos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def __init__(self, ui):
        super(command_com_ui, self).__init__()
        uic.loadUi("command_communication.ui", self)
        self.setWindowOpacity(0.8)  # İstenilen saydamlık değerini ayarlayabilirsin (0.0 - 1.0)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)  # Etraftaki boşları siler

        self.command = self.findChild(QLineEdit, "a_input")
        self.hideCommandUI = self.findChild(QPushButton, "closebtn")

        self.hideCommandUI.clicked.connect(self.hide_command_ui)
        self.ui = ui
        self.command.returnPressed.connect(self.add_to_values)
        # self.ui = UI()

    def hide_command_ui(self):
        self.hide()

    def add_to_values(self):
        command_text = self.command.text()
        self.ui.addToValues(command_text)
        self.command.clear()

    def print_command(self):
        command_text = self.command.text()
        self.command.clear()
        print(command_text)

    def add_CommandList(self):
        command_text = self.command.text()
        self.ui.addToValues(command_text)




class UI(QMainWindow):

    db = Database()
    second_ui_file = "command_communication.ui"

    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("Niyetli.ui", self)
        self.label = self.findChild(QLabel, "label")
        self.dialogList = self.findChild(QListView, "Dialog_2")
        self.niyetli_logo = self.findChild(QLabel, "logo")
        self.hide_show = self.findChild(QPushButton, "niyetli_buton")
        self.container_history = self.findChild(QFrame, "container_history")
        # self.container_history.setStyleSheet("background-color: rgb(0, 18, 25, 0.8); border-radius: 30px;")
        # self.container_history.setWindowOpacity(0.8)
        self.niyetli_status = self.findChild(QFrame, "frame_32")

        self.niyetli_status.setStyleSheet("#frame_32{border-radius:25px; border:5px solid rgb(0, 18, 25); background-color: #eb0000;}")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)  # Etraftaki boşları siler
        # self.command = self.findChild(QLineEdit, "a_input")

        self.comand_comm = self.findChild(QPushButton, "commandCenter_button")
        self.change_categoryListFunc = self.findChild(QCommandLinkButton, "change_category")

        # self.command.returnPressed.connect(self.addToValues)
        self.change_category.clicked.connect(self.change_categoryList)
        self.niyetli_buton.clicked.connect(self.ContainerState)
        self.commandCenter_button.clicked.connect(self.command_com_state)

        self.setWindowOpacity(1.0)  # İstenilen saydamlık değerini ayarlayabilirsin (0.0 - 1.0)

        self.pixmap = QPixmap("Niyetli_small.png")
        self.niyetli_logo.setPixmap(self.pixmap)
        self.niyetli_logo.setScaledContents(True)
        self.niyetli_logo.setAlignment(Qt.AlignJustify)  # Resmi ortalama

        model = QStandardItemModel()
        self.values = ["anan", "anan2"]
        self.notlar = ["not1", "not2"]
        self.animsat = ["2"]
        self.current_category = "values"  # Başlangıçta gösterilecek kategori

        for i in self.values:
            item = QStandardItem(i)
            model.appendRow(item)

        self.dialogList.setModel(model)

        self.show()

        self.workerThread = WorkerThread()
        self.workerThread.dialogAdded.connect(self.addDialog)
        self.workerThread.start()
        # self.openSecondUI()

    def change_categoryList(self):
        model = self.dialogList.model()
        label = self.findChild(QLabel, "category_title")

        if self.current_category == "values":
            label.setText("Notlar")
            notes = self.db.show_onlyNotes()
            data = notes
            self.current_category = "notlar"

        elif self.current_category == "notlar":
            label.setText("Anımsatıcılar")
            data = self.animsat
            self.current_category = "animsaticilar"

        else:
            label.setText("Komut Geçmişi")
            data = self.values
            self.current_category = "values"
        model.clear()

        for i in data:
            item = QStandardItem(i)
            model.appendRow(item)


    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = event.globalPos() - self.oldPos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    #def resizeEvent(self, event: QResizeEvent):
    #    super().resizeEvent(event)
    #    self.adjustImageSize()

    #def adjustImageSize(self):
    #    scaledPixmap = self.pixmap.scaled(self.niyetli_logo.size(), Qt.KeepAspectRatio)
    #    self.niyetli_logo.setPixmap(scaledPixmap)

    def addToValues(self, command_text=None):
        text = command_text
        model = self.dialogList.model()
        item = QStandardItem(text)
        self.values.append(command_text)
        model.insertRow(0, item)
        # self.command.clear()

    def addDialog(self, text):
        model = self.dialogList.model()
        item = QStandardItem(text)
        model.appendRow(item)

    def ContainerState(self):
        if self.container_history.isVisible():
            self.container_history.setVisible(False)
        else:
            self.container_history.setVisible(True)

    def openCommandUI(self):
        self.command_window = command_com_ui(self)
        self.command_window.show()

    def closeCommandUI(self):
        if self.command_window is not None and self.command_window.isVisible():
            self.command_window.hide()

    def command_com_state(self):

        self.command_window = command_com_ui(self)
        if command_window.isHidden():
            self.openCommandUI()
            #self.niyetli_status.setStyleSheet("")

        else:
            self.closeCommandUI()
            # self.niyetli_status.setStyleSheet("background-color: red;")


app = QApplication(sys.argv)
ui_window = UI()
command_window = command_com_ui(ui_window)
# command_window.show()
app.exec_()
