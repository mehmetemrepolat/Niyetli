from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTableWidget, \
    QTableWidgetItem
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import Qt, QSize
import sys
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QFont
from cryptography.fernet import Fernet
from Niyetli.database.localdb_sqlite import LocalDatabase


class passwordManagerAdd(QMainWindow):
    def mouseMoveEvent(self, event):
        delta = event.globalPos() - self.oldPos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def close_button(self):
        self.hide()

    def __init__(self, ui):

        super(passwordManagerAdd, self).__init__()
        uic.loadUi("passwordManager.ui", self)
        self.setWindowOpacity(0.8)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.ui = ui

        #self.closebtn = self.findChild(QPushButton, "closebtn")
        # self.closebtn.clicked.connect(self.close_button)




class passwordManagerUI(QMainWindow):

    # Bu fonksiyonda ikon değiştirmeden çok daha fazlası olacak aslında.
    # *- Parolaların görüntülenip görüntülenmemesi
    # *- Anahtarın girilmesi
    # Bu gibi olaylar bu butona basılması sonrasında gerçekleşecek olaylar.
    def lockIcon_change(self):
        if self.isLocked is True:
            buttonIcon = QIcon("../file_imgs/lock_red.ico")
            self.isLocked = False
        else:
            buttonIcon = QIcon("../file_imgs/lock_green.ico")
            self.isLocked = True
        pixmap = buttonIcon.pixmap(QSize(32, 32))

        if not pixmap.isNull():
            self.lockButton.setIcon(QIcon(pixmap))
            self.lockButton.setIconSize(pixmap.size())  # Set the icon size to match pixmap size
            self.lockButton.setFixedSize(pixmap.size())  # Set button size to match icon size
        else:
            print("Pixmap is null, icon not loaded.")


    def encryptPassword(self, password, key):  # Key dışarıdan girilecek şekilde ayarlanacak.
        cipher_suite = Fernet(key)
        encrypted_password = cipher_suite.encrypt(password.encode())
        return encrypted_password

    def Save_LoginInformations(self, encrypted_password, MailorUserName, url="", description=""):
        self.ld.insert_information_Password_Manager(url, MailorUserName, encrypted_password, description)

    def passwordManager(self, userName, password, url, description, key):
        # encrypt password
        encrypted_pass = self.encryptPassword(password, key)
        self.Save_LoginInformations(encrypted_pass, userName, url, description)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = event.globalPos() - self.oldPos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def open_passwordManagerWindow(self):
        self.open_passwordManagerWindow = passwordManagerAdd(self)
        self.open_passwordManagerWindow.show()

    def __init__(self):
        super(passwordManagerUI, self).__init__()
        self.ld = LocalDatabase()
        uic.loadUi("passwordManager_menu.ui", self)
        self.setWindowOpacity(1)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.isLocked = False
        self.lockButton = self.findChild(QPushButton, "lockButton")
        self.addPasswordButton = self.findChild(QPushButton, "addPasswordButton")

        self.addPasswordButton.clicked.connect(self.open_passwordManagerWindow)
        buttonIcon = QIcon("../file_imgs/lock_red.ico")
        pixmap = buttonIcon.pixmap(QSize(32, 32))
        self.addPasswordButton.clicked.connect(self.open_passwordManagerWindow)
        if not pixmap.isNull():
            self.lockButton.setIcon(QIcon(pixmap))
            self.lockButton.setIconSize(pixmap.size())  # Set the icon size to match pixmap size
            self.lockButton.setFixedSize(pixmap.size())  # Set button size to match icon size
        else:
            print("Pixmap is null, icon not loaded.")
        self.lockButton.clicked.connect(self.lockIcon_change)

        # key getirilmesi gerekiyor ama şimdilik boşta kalacak
        key = ""

        passwordData = self.ld.get_PasswordData()

        passwordTable = self.findChild(QTableWidget, "passwordTable")
        passwordTable.setColumnCount(4)
        passwordTable.setRowCount(len(passwordData))
        column_names = ["Uygulama Adı/URL", "Kullanıcı Adı/Mail", "Şifre", "Açıklama"]
        passwordTable.setHorizontalHeaderLabels(column_names)
        passwordTable.horizontalHeader().setVisible(True)
        passwordTable.horizontalHeader().setSectionResizeMode(0,
                                                                 QtWidgets.QHeaderView.ResizeToContents)  # İlk sütunu içeriğe göre genişlet
        passwordTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        passwordTable.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        passwordTable.verticalHeader().setVisible(False)

        passwordTable_header = passwordTable.horizontalHeader()
        header_style = "QHeaderView::section { background-color: rgb(0, 18, 25); color: white; opacity: 0.5; border: none; padding-left: 5px; }"
        header_font = QFont()
        header_font.setBold(True)
        header_font.setPointSize(10)
        header_palette = QPalette()
        header_palette.setColor(QPalette.WindowText, Qt.white)  # Yazı rengi: Beyaz
        passwordTable.horizontalHeader().setFont(header_font)
        passwordTable.horizontalHeader().setPalette(header_palette)
        passwordTable_header.setStyleSheet(header_style)
        passwordTable_Vertical_scrollbar_style = """
        QScrollBar:vertical {
            border: none;
            background: transparent;
            width: 10px;
            margin: 0px;
        }

        QScrollBar::handle:vertical {
            background: #48C9B0; /* Slider rengi */
            border: 1px solid #16A085; 
            min-height: 20px;
            border-radius: 5px;
        }
        """
        scrollbar_horizontal_style = """
        QScrollBar:horizontal {
            border: none;
            background: transparent; /* Arka planı şeffaf yapar */
            height: 10px; /* Yükseklik */
            margin: 0px;
        }

        QScrollBar::handle:horizontal {
            background: #48C9B0; /* Slider rengi */
            border: 1px solid #16A085; /* Kenarlık rengi */
            min-width: 20px; /* Min. genişlik */
            border-radius: 5px; /* Kenar yumuşatma */
        }
        """

        passwordTable.verticalScrollBar().setStyleSheet(passwordTable_Vertical_scrollbar_style)
        passwordTable.horizontalScrollBar().setStyleSheet(scrollbar_horizontal_style)

        passwordTable.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)  # Hücre seçimini kapatma
        passwordTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        print(len(passwordData))
        for i in range(0, len(passwordData)):
            passwordTable.setItem(i, 0, QTableWidgetItem(passwordData[i][0]))
            passwordTable.setItem(i, 1, QTableWidgetItem(passwordData[i][1]))
            passwordTable.setItem(i, 2, QTableWidgetItem(passwordData[i][2]))
            passwordTable.setItem(i, 3, QTableWidgetItem(passwordData[i][3]))


app = QApplication(sys.argv)

ui_window = passwordManagerUI()
passwordManagerAdd_window = passwordManagerAdd(ui_window)


pm = passwordManagerUI()

pm.show()
app.exec_()
