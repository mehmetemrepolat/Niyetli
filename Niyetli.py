import time


from PyQt5.QtWidgets import QMainWindow, QTableWidget, QApplication, QLabel, QFrame, QToolTip, QHeaderView, QTableWidgetItem, QListView, QLineEdit, QPushButton, QCommandLinkButton, QFileDialog, QMenuBar, QMenu, QStatusBar, QTextBrowser, QTextEdit
from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QResizeEvent, QCursor, QIcon, QTransform
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QFile, QPoint
from PyQt5.QtWidgets import QGroupBox
from database.db_connector import Database
import sys
from PyQt5.QtGui import QKeySequence
import threading
import pygame

#from DailyTasks.secreen_timer import SecreenTimer
from DailyTasks.voiceNotes import VoiceNotes


class WorkerThread(QThread):
    dialogAdded = pyqtSignal(str)

    def run(self):
        pass
        # while True:
            # text = input("Eklemek istediğiniz yazıyı girin: ")
            # self.dialogAdded.emit(text)


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
    #sc = SecreenTimer()
    second_ui_file = "command_communication.ui"

    def __init__(self):
        super(UI, self).__init__()
        self.commandCenter_button = None
        uic.loadUi("Niyetli.ui", self)
        self.label = self.findChild(QLabel, "label")
        # self.dialogList = self.findChild(QListView, "Dialog_2")
        self.niyetli_logo = self.findChild(QLabel, "logo")
        self.hide_show = self.findChild(QPushButton, "niyetli_buton")
        self.container_history = self.findChild(QFrame, "container_history")
        self.container_Content = self.findChild(QFrame, "container_content")
        self.searchTitle = self.findChild(QLineEdit, "search")
        # self.container_history.setStyleSheet("background-color: rgb(0, 18, 25, 0.8); border-radius: 30px;")
        # self.container_history.setWindowOpacity(0.8)
        self.niyetli_status = self.findChild(QFrame, "frame_32")
        self.niyetli_status.setStyleSheet("#frame_32{border-radius:25px; border:5px solid rgb(0, 18, 25); background-color: #eb0000;}")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)  # Etraftaki boşları siler
        # self.command = self.findChild(QLineEdit, "a_input")
        self.comand_comm = self.findChild(QPushButton, "commandCenter_button")


        self.nextCategory = self.findChild(QPushButton, "next_button")
        self.nextCategory.setIcon(QIcon("file_imgs/next.ico"))

        self.next_button.clicked.connect(lambda: self.change_categoryList("next"))


        self.previousCategory = self.findChild(QPushButton, "back_button")
        self.previousCategory.setIcon(QIcon("file_imgs/back.ico"))

        self.back_button.clicked.connect(lambda: self.change_categoryList("back"))


        # self.command.returnPressed.connect(self.addToValues)
        self.niyetli_buton.clicked.connect(self.ContainerState)


        self.command_ui_isOpen = False
        self.commandCenter_button.clicked.connect(self.command_com_state)

        self.command_window = command_com_ui(self)


        self.search_Button = self.findChild(QPushButton, "search_button")
        self.searchBar_status = False

        self.search_Button.setIcon(QIcon("file_imgs/search.ico"))
        self.search_Button.clicked.connect(self.searchText)

        self.setWindowOpacity(1.0)  # İstenilen saydamlık değerini ayarlayabilirsin (0.0 - 1.0)

        self.pixmap = QPixmap("Niyetli_small.png")
        self.niyetli_logo.setPixmap(self.pixmap)
        self.niyetli_logo.setScaledContents(True)
        self.niyetli_logo.setAlignment(Qt.AlignJustify)  # Resmi ortalama

        model = QStandardItemModel()
        self.commands = ["anan", "anan2"]
        self.notlar = ["not1", "not2"]
        self.animsat = ["1 Lorem Ipsum", "2 Lorem Ipsum", "3 Lorem Ipsum", "4 Lorem Ipsum", "5 Lorem Ipsum", "6 Lorem Ipsum"]


        # self.current_category = "commands"  # Başlangıçta gösterilecek kategori
        # self.previous_category = "commands"

        self.category_title = self.findChild(QLabel, "category_title")

        self.QTable = self.findChild(QTableWidget, "tableWidget")
        # self.tableWidget.setColumnCount(3)

        tableWidget = self.findChild(QTableWidget, "tableWidget")
        tableWidget.setRowCount(len(self.commands))
        tableWidget.setColumnCount(len(self.commands[0]))

        # QTableWidget'ın başlık widget'ını al
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)

        header_style = "QHeaderView::section { background-color: <renk>; opacity: <opaklık>; border: none;  padding-left: 5px; }"

        self.hideContainerHistory = self.findChild(QPushButton, "closebtn")

        self.hideContainerHistory.clicked.connect(self.hide_ContainerHistory)


        # Arka plan rengini ve opaklık değerini istediğiniz şekilde değiştirin
        header_style = header_style.replace("<renk>", "rgb(0, 18, 25)")
        header_style = header_style.replace("<opaklık>", "0.5")
        self.tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        # Stil yapısını uygula
        header.setStyleSheet(header_style)

        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.container_content.setVisible(False)

        #for row, rowData in enumerate(self.values):
        #    item = QTableWidgetItem(str(rowData))
        #    tableWidget.setItem(row, item)

        # for i in self.values:
        #     item = QStandardItem(i)
        #     model.appendRow(item)

        # self.dialogList.setModel(model)
        self.tableWidget.cellEntered.connect(self.show_cell_tooltip)
        # self.tableWidget.setToolTip("Anan")
        self.show()

        self.workerThread = WorkerThread()
        self.workerThread.dialogAdded.connect(self.addDialog)
        self.workerThread.start()
        # self.openSecondUI()
        self.tableWidget.cellDoubleClicked.connect(self.cell_clicked)
        self.searchTitle.setVisible(False)

    def searchText(self):
        if self.searchBar_status:
            self.searchTitle.setVisible(False)
            self.searchBar_status = False
        else:
            self.searchTitle.setVisible(True)
            self.searchBar_status = True

    def hide_ContainerHistory(self):
        self.container_content.setVisible(False)

    def show_cell_tooltip(self, row, column):
        item = self.tableWidget.item(row, column)
        if item is not None:
            tooltip_text = item.text()
            self.tableWidget.setToolTip(tooltip_text)
        else:
            self.tableWidget.setToolTip("")



    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            print("Tuşa basıldı!")

            # selected_cell = self.tableWidget.currentCell()
            # if selected_cell.isValid():
            #     self.cell_clicked(selected_cell.row(), selected_cell.column())

    def cell_clicked(self, row, column):
        if self.current_category == "notlar":
            self.container_content.setVisible(True)
            item = self.tableWidget.item(row, column)
            if item is not None:
                value = item.text()
                # print(value, " ", self.current_category)
                self.set_containerNoteContent(value)


        elif self.current_category == "animsaticilar":
            print("Anan")


        elif self.current_category == "Sesli Notlar":
            print("Sesli Notlar:", row)

        else:
            print("Anana")

    def set_containerNoteContent(self, title, content_type=0):
        contents = self.db.get_note_content(str(title))
        # print(contents)
        container_Title = self.findChild(QLabel, "content_title")
        content_Category = self.findChild(QLabel, "content_category")
        content_Note = self.findChild(QTextBrowser, "data_input")
        content_time = self.findChild(QLabel, "time_data")
        content_title2 = contents[0][1]

        content_time2 = f"{contents[0][4]} {contents[0][5]}"
        content_categ2 = contents[0][3]
        content_Note2 = contents[0][2]
        content_Note.setText(content_Note2)
        container_Title.setText(content_title2)
        content_Category.setText(content_categ2)
        content_time.setText(content_time2)

        # content_Category.setText(content_categ2)
        # content_time.setText(content_time2)
        # content_Time = contents

        # container_Title.setText("content_title")
        # content_Category.setText("content_categ")
        # self.content_time.setText(f"{contents[4]} - {contents[5]}")

        # self.container_Title.setText(contents[1])

    category_list = [["commands", "Komut Geçmişi"], ["notlar", "Notlar"], ["animsaticilar", "Anımsatıcılar"], ["Sesli Notlar", "Sesli Notlar"], ["SecreenTimer", "Ekran Süresi"]]
    # Bu kısım daha sonraları veritabanından otomatik olarak çekilecek. Veritabanı güncellendiği zaman burası da güncellenecek
    category_counter = 0
    current_category = category_list[0][0]


    def change_categoryList(self, way):
        data = None

        def category_changer(index):
            if index == len(self.category_list):
                self.category_counter = 0
                index = 0
                current_category = self.category_list[0][0]

            elif index == -1:
                self.category_counter = 0
                index = 0
                value = int(len(self.category_list) - 1)
                current = self.category_list[value][0]

            content_data = None
            try:
                label_name = self.category_list[index][1]
                self.current_category = self.category_list[index][0]
                self.category_title.setText(label_name)
                if self.category_list[index][0] == "commands":
                    content_data = self.commands
                elif self.category_list[index][0] == "notlar":
                    content_data = self.db.show_onlyNotes()
                elif self.category_list[index][0] == "animsaticilar":
                    content_data = self.animsat
                elif self.category_list[index][0] == "Sesli Notlar":
                    voice_notes = self.db.show_voiceNotes()
                    content_data = voice_notes
                #elif self.category_list[index][0] == "SecreenTimer":
                    #secren_time_datas = self.sc.get_statistics()
                else:
                    print("Hata!")
                return content_data

            except Exception as e:
                print(e)

        if way == "next":
            self.category_counter += 1
            data = category_changer(self.category_counter)


        elif way == "back":
            self.category_counter -= 1
            if self.category_counter == -1:
                self.category_counter = len(self.category_list) - 1
            data = category_changer(self.category_counter)


        try:
            tableWidget = self.findChild(QTableWidget, "tableWidget")
            tableWidget.clearContents()  # Tablonun içeriğini temizle
            tableWidget.setRowCount(len(data))  # Satır sayısını güncelle
            tableWidget.setColumnCount(1)  # Sadece bir sütun olduğunu belirt
        except Exception as e:
            print("Hata:", e)
        try:
            for row, value in enumerate(data):

                if self.current_category == "Sesli Notlar":
                    tableWidget.setColumnCount(2)  # Sadece 2 sütun olduğunu belirt
                    button = QPushButton()
                    button.setIcon(QIcon("file_imgs/play.ico"))
                    button.setStyleSheet("text-align: left; padding-left: 0px;")  # ikonu sola hizala
                    button.setObjectName("playButton")  # Düğmenin adını belirle

                    def button_clicked(row):
                        try:
                            button = tableWidget.cellWidget(row, 0)  # Butonun doğru satıra ait olduğundan emin olun
                            print("Deneme1:", button.objectName())
                            if button.objectName() == "playButton":
                                print("Deneme2")
                                try:
                                    voice_name = str(tableWidget.item(row, 1).text())
                                    voice_path = self.db.get_sound_from_db(voice_name)
                                    voice_path2 = f"userDirectory/voiceNotes/{voice_path}"
                                    vn = VoiceNotes()
                                    vn.play_voice_note(voice_path2)
                                    stop_time = vn.get_voice_duration(voice_path2)
                                    timer_changer(stop_time)
                                    # self.play_voice_note(str(tableWidget.item(row, 1).text()))
                                    button.setIcon(QIcon("file_imgs/stop.ico"))
                                    button.setObjectName("stopButton")  # Düğmenin adını güncelle

                                    ############

                                except Exception as e:
                                    print(e)

                            else:
                                # Durdurma işlemini buraya ekleyin
                                button.setIcon(QIcon("file_imgs/play.ico"))
                                button.setObjectName("playButton")  # Düğmenin adını güncelle
                        except Exception as e:
                            print(e)

                    def timer_changer(duration):
                        def change():
                            print("dur:", duration)
                            time.sleep(duration)
                            button.setIcon(QIcon("file_imgs/play.ico"))
                            button.setObjectName("playButton")  # Düğmenin adını güncelle
                            pygame.mixer.music.stop()
                            return
                        thread = threading.Thread(target=change)
                        thread.start()


                    try:
                        button.clicked.connect(lambda _, r=row: button_clicked(
                            r))  # Butona tıklandığında ilgili satırın ikinci sütunundaki değeri yazdır
                    except Exception as e:
                        print(e)

                    tableWidget.setCellWidget(row, 0, button)
                    item = QTableWidgetItem(str(value))  # Değeri doğrudan al
                    tableWidget.setItem(row, 1, item)
                    tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  # İlk sütunu içeriğe göre genişlet
                    tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)  # ikinci sütunu içeriğe göre genişlet
                    tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
#
                else:
                    item = QTableWidgetItem(str(value))  # Değeri doğrudan al
                    tableWidget.setItem(row, 0, item)
        except Exception as e:
            print(e)




    def category_voice_notes(self):
        return None





    def play_voice_note(self, voice_title):
        print("Deneme")
        try:
            path = self.db.get_sound_from_db(voice_title)
            print("yol:", path)

            def play_thread():
                pygame.mixer.init()
                pygame.mixer.music.load(path)
                pygame.mixer.music.play()
                # Burada stop kısmını eklememiz gerekiyor
            thread = threading.Thread(target=play_thread)
            thread.start()
        except Exception as e:
            print(e)


    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = event.globalPos() - self.oldPos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    # def resizeEvent(self, event: QResizeEvent):
    #     super().resizeEvent(event)
    #     self.adjustImageSize()

    # def adjustImageSize(self):
    #     scaledPixmap = self.pixmap.scaled(self.niyetli_logo.size(), Qt.KeepAspectRatio)
    #     self.niyetli_logo.setPixmap(scaledPixmap)

    def addToValues(self, command_text=None):
        text = command_text
        model = self.dialogList.model()
        item = QStandardItem(text)
        self.commands.append(command_text)
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
            print("E çalışıyor")
            self.command_window.hide()

    def command_com_state(self):

        if not self.command_ui_isOpen:
            self.openCommandUI()
            self.command_ui_isOpen = True

        else:
            self.closeCommandUI()
            self.command_ui_isOpen = False
            # self.niyetli_status.setStyleSheet("background-color: red;")


app = QApplication(sys.argv)
ui_window = UI()
command_window = command_com_ui(ui_window)
# command_window.show()
app.exec_()
