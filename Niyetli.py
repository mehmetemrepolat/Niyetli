import time
from PyQt5.QtWidgets import QMainWindow, QGraphicsOpacityEffect, QTableWidget, QApplication, QLabel, QFrame, QHeaderView, QTableWidgetItem, QLineEdit, QPushButton, QTextBrowser, QRadioButton
from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer, QSize
from database.db_connector import Database
import sys
import threading
import pygame
# from DailyTasks.secreen_timer import SecreenTimer
from DailyTasks.voiceNotes import VoiceNotes
from mutagen.mp3 import MP3
import pyaudio
import wave  # Wave modülünü de içe aktardık


class WorkerThread(QThread):
    dialogAdded = pyqtSignal(str)

    def run(self):
        pass
        # while True:
            # text = input("Eklemek istediğiniz yazıyı girin: ")
            # self.dialogAdded.emit(text)


class CommandComUI(QMainWindow):

    def write(self):
        print("Deneme")

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = event.globalPos() - self.oldPos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def __init__(self, ui):
        super(CommandComUI, self).__init__()
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



class VoiceRecorderUI(QMainWindow):
    from DailyTasks.voiceNotes import VoiceNotes
    from DailyTasks.AlarmCalendarReminderOP import DateOperations

    vn = VoiceNotes()
    db = Database()
    do = DateOperations()
    def recorder_toggle(self, toggle):
        if toggle == 1:
            self.toggle_recorder = True
        elif toggle == 0:
            self.toggle_recorder = False
        else:
            return "Error"

    def voice_recording(self, title):
        try:
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 44100
            CHUNK = 1024
            RECORD_SECONDS = 5  # Kaydedilecek süre (saniye)
            OUTPUT_FILENAME = f"{title}.mp3"  # Kaydedilen sesin dosya adı
            audio = pyaudio.PyAudio()
            # Ses kaydetme işlemi
            stream = audio.open(format=FORMAT, channels=CHANNELS,
                                rate=RATE, input=True,
                                frames_per_buffer=CHUNK)
            frames = []
            self.toggle_recorder = True
            recording_thread = threading.Thread(target=self.record_audio, args=(title, CHUNK, frames))
            recording_thread.start()

        except Exception as e:
            print(e)

    def record_audio(self, title, chunk, frames):
        def save_vn_to_db(title, path, categories="Hızlı Sesli Not"):
            query = "INSERT INTO voice_notes(voice_note_title, voice_note_path, voice_note_categories, voice_note_create_date)" \
                    f"VALUES('{title}', '{path}', '{categories}', '{self.do.get_date()}')"
            print(query)
            self.db.insert_to_table_with_query(query)

        # Kayıt ayarları
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNK = 1024
        RECORD_SECONDS = 5  # Kaydedilecek süre (saniye)
        OUTPUT_FILENAME = f"userDirectory/voiceNotes/{title}.mp3"  # Kaydedilen sesin dosya adı
        PATH = f"userDirectory/voiceNotes/{title}.mp3"

        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=chunk)

        print("Kayıt başladı.")

        try:
            while self.toggle_recorder:
                data = stream.read(chunk)
                frames.append(data)
        except KeyboardInterrupt:
            print("Kayıt durduruldu.")
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()

            # Kaydedilen sesi WAV dosyasına kaydet
            with wave.open(OUTPUT_FILENAME, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(audio.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
            save_vn_to_db(title, PATH)
            print(f"Ses {title} dosyasına kaydedildi.")

    def update_timer_label(self):

        start_time = time.time()
        while self.isRecording:
            passed = time.time() - start_time
            mins, secs = divmod(int(passed), 60)
            hours, mins = divmod(mins, 60)
            time_str = f"{hours:02d}:{mins:02d}:{secs:02d}"
            print(time_str)
            self.voice_time_label.setText(time_str)
            time.sleep(1)

    def voice_record_button(self):
        self.isRecording = not self.isRecording
        if self.isRecording:
            self.toggle_recorder = True
            self.timer_thread = threading.Thread(target=self.update_timer_label)
            self.timer_thread.start()
            # Yeni kayıt ismini al
            title = self.vn.name_for_VN()
            self.voice_recording(title)

        else:
            self.toggle_recorder = False


    def __init__(self, ui):

        super(VoiceRecorderUI, self).__init__()
        uic.loadUi("VoiceRecord.ui", self)
        self.setWindowOpacity(0.8)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.ui = ui
        self.voice_time_label = self.findChild(QLabel, "voice_time")
        self.micButton = self.findChild(QPushButton, "micButton")
        self.micButton.setGeometry(100, 50, 64, 64)
        self.micButton.setStyleSheet("background-color: transparent; border: none;")
        icon = QIcon("file_imgs/mic.ico")
        pixmap = icon.pixmap(QSize(64, 64))
        self.micButton.setIcon(QIcon(pixmap))
        self.iconOpacityEffect = QGraphicsOpacityEffect()
        self.iconOpacityEffect.setOpacity(0.5)
        self.micButton.setGraphicsEffect(self.iconOpacityEffect)
        self.micButton.setIconSize(QSize(64, 64))
        self.isRecording = False
        self.toggle_recorder = False
        self.micButton.clicked.connect(self.voice_record_button)

        # closebtn
        self.closebtn = self.findChild(QPushButton, "closebtn")
        self.closebtn.clicked.connect(self.close_button)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()


    def close_button(self):
        self.hide()

    def mouseMoveEvent(self, event):
        delta = event.globalPos() - self.oldPos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()



class UI(QMainWindow):

    db = Database()
    # sc = SecreenTimer()
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
        self.comand_comm = self.findChild(QPushButton, "commandCenter_button")


        self.nextCategory = self.findChild(QPushButton, "next_button")
        self.nextCategory.setIcon(QIcon("file_imgs/next.ico"))

        self.next_button.clicked.connect(lambda: self.change_categoryList("next"))

        self.previousCategory = self.findChild(QPushButton, "back_button")
        self.previousCategory.setIcon(QIcon("file_imgs/back.ico"))

        self.back_button.clicked.connect(lambda: self.change_categoryList("back"))

        self.niyetli_buton.clicked.connect(self.ContainerState)

        self.command_ui_isOpen = False
        self.commandCenter_button.clicked.connect(self.command_com_state)

        self.command_window = CommandComUI(self)

        self.voiceRecord_window = VoiceRecorderUI(self)

        self.search_Button = self.findChild(QPushButton, "search_button")
        self.searchBar_status = False

        self.search_Button.setIcon(QIcon("file_imgs/search.ico"))
        self.search_Button.clicked.connect(self.searchText)

        self.add_content_button = self.findChild(QPushButton, "add_content")
        self.add_content_button.setIcon(QIcon("file_imgs/plus.ico"))


        self.setWindowOpacity(1.0)  # İstenilen saydamlık değerini ayarlayabilirsin (0.0 - 1.0)

        self.pixmap = QPixmap("Niyetli_small.png")
        self.niyetli_logo.setPixmap(self.pixmap)
        self.niyetli_logo.setScaledContents(True)
        self.niyetli_logo.setAlignment(Qt.AlignJustify)  # Resmi ortalama

        model = QStandardItemModel()
        self.commands = ["command"]
        self.notlar = []
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
        self.current_playing_row = -1

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
        global tableWidget
        data = None

        def get_past_data(category):
            self.db.get_past_datas(category)

        def is_music_playing(self):
            try:
                # pygame.mixer.music.get_busy() her zaman 0 dönüyorsa, pygame.mixer.music.get_pos() ile
                # müziğin geçen süresini kontrol edebiliriz.
                return pygame.mixer.music.get_pos() > 0
            except Exception as e:
                print(e)
                return False

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
                    command_list = self.db.showCommands()
                    content_data = command_list

                elif self.category_list[index][0] == "notlar":
                    content_data = self.db.showNotesDatas()
                    note_list = []
                    notes_contents = []
                    # Burada for ile data yüklemesi gerçekleştirmemiz gerekiyor.
                    for x in range(0, len(content_data)):
                        note_list.append(content_data[x][1])
                        notes_contents.append([content_data[x][0], content_data[x][2], content_data[x][3], content_data[x][4]])
                    content_data = note_list
                    # print(notes_contents)

                elif self.category_list[index][0] == "animsaticilar":
                    content_data = self.animsat
                elif self.category_list[index][0] == "Sesli Notlar":
                    voice_notes = self.db.show_voiceNotes()
                    content_data = voice_notes
                elif self.category_list[index][0] == "SecreenTimer":
                    content_data = self.db.show_onlyNotes()

                # elif self.category_list[index][0] == "SecreenTimer":
                    # secren_time_datas = self.sc.get_statistics()

                else:
                    print("Hata!")
                return content_data

            except Exception as e:
                print(e)

        if way == "next":
            self.category_counter += 1
            data = category_changer(self.category_counter)
            print(self.current_category)

            try:
                if is_music_playing(self):
                    pygame.mixer.music.stop()
                else:
                    pass
            except Exception as e:
                print(e)


        elif way == "back":
            print(self.current_category)
            self.category_counter -= 1
            if self.category_counter == -1:
                self.category_counter = len(self.category_list) - 1
            data = category_changer(self.category_counter)
            try:
                if is_music_playing(self):
                    pygame.mixer.music.stop()
                else:
                    pass
            except Exception as e:
                print(e)


        try:
            tableWidget = self.findChild(QTableWidget, "tableWidget")
            tableWidget.clearContents()  # Tablonun içeriğini temizle
            tableWidget.setRowCount(len(data))  # Satır sayısını güncelle
            tableWidget.setColumnCount(1)  # Sadece bir sütun olduğunu belirt
        except Exception as e:
            print("Hata:", e)
        try:
            for row, value in enumerate(data):

                # >------------------------------------------- Sesli Notlar ----------------------------------------------<

                # Parça durduğunda/bittiğinde ikon değişmiyor.
                # Muhtemelen Thread çalışmıyor olabilir. Kontrol edilmesi gerekiyor.

                if self.current_category == "Sesli Notlar":
                    tableWidget.setColumnCount(2)  # Sadece 2 sütun olduğunu belirt
                    tableWidget.horizontalHeader().setVisible(False)

                    self.add_content_button.clicked.connect(self.openVoiceRecorderUI)

                    button = QPushButton()
                    button.setIcon(QIcon("file_imgs/play.ico"))
                    button.setStyleSheet("text-align: left; padding-left: 0px;")  # ikonu sola hizala
                    button.setObjectName("playButton")  # Düğmenin adını belirle

                    def button_clicked(row):
                        try:
                            if self.current_playing_row != -1:
                                stop_playing(self.current_playing_row)  # Önceki çalma işlemi varsa durdurun

                            button = tableWidget.cellWidget(row, 0)  # Butonun doğru satıra ait olduğundan emin ol
                            if button.objectName() == "playButton":
                                try:
                                    voice_name = str(tableWidget.item(row, 1).text())
                                    voice_path = self.db.get_sound_from_db(voice_name)
                                    voice_path2 = f"userDirectory/voiceNotes/{voice_path}"
                                    vn = VoiceNotes()
                                    pygame.mixer.init()
                                    pygame.mixer.music.load(voice_path2)
                                    pygame.mixer.music.play()
                                    stop_time = vn.get_voice_duration(voice_path2)
                                    timer_changer(stop_time)
                                    button.setIcon(QIcon("file_imgs/stop.ico"))
                                    button.setObjectName("stopButton")  # Düğmenin adını güncelle
                                    self.current_playing_row = row  # Mevcut çalan satırı güncelle
                                except Exception as e:
                                    print(e)
                            else:
                                stop_playing(row)  # Durdurma işlemini gerçekleştir
                                button.setIcon(QIcon("file_imgs/play.ico"))
                                button.setObjectName("playButton")  # Düğmenin adını güncelle

                            update_buttons_state()  # Tüm düğmeleri güncelle
                        except Exception as e:
                            print(e)

                    def stop_playing(row):
                        try:
                            pygame.mixer.music.stop()
                        except Exception as e:
                            print(e)

                    def update_buttons_state():
                        for i in range(tableWidget.rowCount()):
                            try:
                                button = tableWidget.cellWidget(i, 0)
                                if isinstance(button, QPushButton):
                                    if button.objectName() == "playButton":
                                        pass
                                    elif button.objectName() == "stopButton" and i != self.current_playing_row:
                                        button.setObjectName("playButton")
                                        button.setIcon(QIcon("file_imgs/play.ico"))
                                    else:
                                        pass
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
                    tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)  # İlk sütunu içeriğe göre genişlet
                    tableWidget.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)  # ikinci sütunu içeriğe göre genişlet
                    tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
                # >--------------------------------------------- Commands ------------------------------------------------<

                elif self.current_category == "commands":
                    stat = self.db.showCommands()
                    column_headers = ["Komut"]
                    sutun1 = column_headers[0]
                    tableWidget.setHorizontalHeaderLabels(column_headers)
                    tableWidget.horizontalHeader().setVisible(True)

                    header_item1 = QTableWidgetItem(sutun1)
                    tableWidget.setHorizontalHeaderItem(0, header_item1)

                    for i, data in enumerate(stat):
                        komut = data[0]
                        tableWidget.setItem(i, 0, QTableWidgetItem(komut))

                    tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)  # İlk sütunu içeriğe göre genişlet
                    tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

                # >------------------------------------------- SecreenTimer ----------------------------------------------<

                elif self.current_category == "SecreenTimer":
                    stat = self.db.get_timer_statics()
                    column_headers = ['Program İsmi', 'Süre(dk)', 'Tekrar']
                    sutun1 = column_headers[0]
                    sutun2 = column_headers[1]
                    sutun3 = column_headers[2]
                    tableWidget.setColumnCount(3)  # Sadece 3 sütun olduğunu belirt
                    # Sütun başlıklarını ekleyin
                    tableWidget.setHorizontalHeaderLabels(column_headers)
                    tableWidget.horizontalHeader().setVisible(True)
                    # İlk sütuna sütun başlığını ekleyin
                    header_item1 = QTableWidgetItem(sutun1)
                    tableWidget.setHorizontalHeaderItem(0, header_item1)
                    # İkinci sütuna sütun başlığını ekleyin
                    header_item2 = QTableWidgetItem(sutun2)
                    tableWidget.setHorizontalHeaderItem(1, header_item2)
                    # Üçüncü sütuna sütun başlığını ekleyin
                    header_item3 = QTableWidgetItem(sutun3)
                    tableWidget.setHorizontalHeaderItem(2, header_item3)

                    for i, data in enumerate(stat):
                        program_ismi = data[0]
                        sure = data[1]  # Saniye cinsinden verilir
                        tekrar = data[3]
                        sure = int(sure) / 60
                        if sure < 1:
                            sure = 1
                        tableWidget.setItem(i, 0, QTableWidgetItem(program_ismi))
                        tableWidget.setItem(i, 1, QTableWidgetItem(str(int(sure))))
                        tableWidget.setItem(i, 2, QTableWidgetItem(tekrar))

                    tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)  # İlk sütunu içeriğe göre genişlet
                    tableWidget.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)  # İkinci sütunu içeriğe göre genişlet
                    tableWidget.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)  # Üçüncü sütunu içeriğe göre genişlet
                    tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
                # animsaticilar

                # Yapılacak işlem basit
                # çekilen listede, son elemanın tarih bilgisine  sahip olması gerekmekte
                # bundan dolayı her bir kategoride kullanılabilecek bir metod(get_string_date) oluşturucaz.
                # Son verinin tarihini o
                # metoda(AlarmCalenderReminderOP.DateOperations.get_string_date) gönderip
                # string tarih verisi çekicez

                elif self.current_category == "animsaticilar":
                    tableWidget.setColumnCount(2)  # Sadece 2 sütun olduğunu belirt
                    tableWidget.horizontalHeader().setVisible(False)
                    radioButton = QRadioButton()
                    radioButton.setObjectName("reminderDone")

                    def radioButton_filled():
                        try:
                            pass
                        except Exception as e:
                            print("Anımsatıcılarda Hata! ", e)
                    if row == 0:
                        tableWidget.setItem(row, 0, QTableWidgetItem('Bugün'))  # Yazı büyütünu büyütmek gerekir
                        tableWidget.setSpan(row, 0, 1, 2)
                        # tableWidget.horizontalHeader().setSectionResizeMode(0, QTableWidget.Fixed)


                    else:
                        tableWidget.setCellWidget(row, 0, radioButton)
                        item = QTableWidgetItem(str(value))
                        tableWidget.setItem(row, 1, item)

                        tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  # İlk sütunu içeriğe göre genişlet
                        tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)  # ikinci sütunu içeriğe göre genişlet
                    tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

                # >---------------------------------------------- Notlar -------------------------------------------------<
                elif self.current_category == "notlar":
                    notes = self.db.showNotesDatas()
                    tableWidget.horizontalHeader().setVisible(False)
                    column_headers = ['Not Başlığı', 'Kategori', 'Tarih']
                    sutun1 = column_headers[0]
                    sutun2 = column_headers[1]
                    sutun3 = column_headers[2]
                    tableWidget.setColumnCount(3)  # Sadece 2 sütun olduğunu belirt
                    tableWidget.setHorizontalHeaderLabels(column_headers)
                    tableWidget.horizontalHeader().setVisible(True)
                    # İlk sütuna sütun başlığını ekleyin
                    header_item1 = QTableWidgetItem(sutun1)
                    tableWidget.setHorizontalHeaderItem(0, header_item1)
                    # İkinci sütuna sütun başlığını ekleyin
                    header_item2 = QTableWidgetItem(sutun2)
                    tableWidget.setHorizontalHeaderItem(1, header_item2)
                    # Üçüncü sütuna sütun başlığını ekleyin
                    header_item3 = QTableWidgetItem(sutun3)
                    tableWidget.setHorizontalHeaderItem(2, header_item3)

                    for i, data in enumerate(notes):
                        note_title = data[1]
                        note_category = data[3]
                        note_date = data[4]

                        tableWidget.setItem(i, 0, QTableWidgetItem(note_title))
                        tableWidget.setItem(i, 1, QTableWidgetItem(note_category))
                        tableWidget.setItem(i, 2, QTableWidgetItem(note_date))

                    tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)  # İlk sütunu içeriğe göre genişlet
                    tableWidget.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)  # İkinci sütunu içeriğe göre genişlet
                    tableWidget.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)  # Üçüncü sütunu içeriğe göre genişlet
                    tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)




                # >----------------------------------------------- Else --------------------------------------------------<

                else:
                    tableWidget.horizontalHeader().setVisible(False)

                    item = QTableWidgetItem(str(value))  # Değeri doğrudan al
                    tableWidget.setItem(row, 0, item)
        except Exception as e:
            print(e)




    def category_voice_notes(self):
        return None




#
#    def play_voice_note(self, voice_title):
#        try:
#            path = self.db.get_sound_from_db(voice_title)
#            # print("yol:", path)
#
#            def play_thread():
#                pygame.mixer.init()
#                pygame.mixer.music.load(path)
#                pygame.mixer.music.play()
#                # Burada stop kısmını eklememiz gerekiyor
#            thread = threading.Thread(target=play_thread)
#            thread.start()
#        except Exception as e:
#            print(e)

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


    def openVoiceRecorderUI(self):
        self.voiceRecord_window = VoiceRecorderUI(self)
        self.voiceRecord_window.show()

    def closeVoiceRecorderUI(self):
        if self.voiceRecord_window is not None and self.voiceRecord_window.isVisible():
            self.voiceRecord_window.hide()

    def openCommandUI(self):
        self.command_window = CommandComUI(self)
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
command_window = CommandComUI(ui_window)
voiceRecord_window = VoiceRecorderUI(ui_window)
# voiceRecord_window.show()
# command_window.show()
app.exec_()
