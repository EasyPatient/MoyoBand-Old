from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5 import QtCore, QtWidgets, QtGui
import database


'''     # input Id Patient who we want to search in database.
        self.BazaData.PatientData(1)
        #print data of patient who we searched.
        print(self.BazaData.sPatientData)
        #This function search only name of patients
        self.BazaData.PatientAllInfo()
        print(self.BazaData.sName) '''


class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_secondwindow()

    #sets up the look of second window
    def setup_secondwindow(self):
        self.setObjectName("SecondWindow")

        self.background = QtWidgets.QLabel(self)
        self.background.setGeometry(QtCore.QRect(0, 0, 1080, 620))
        self.background.setText("")
        self.background.setPixmap(QtGui.QPixmap("data\\front_page.png"))
        self.background.setObjectName("background")

        self.logout_button = QtWidgets.QPushButton(self)
        self.logout_button.setGeometry(QtCore.QRect(740, 260, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei Light")
        font.setPointSize(12)
        self.logout_button.setFont(font)
        self.logout_button.setObjectName("Logout")



        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    #sets the text and titles of widgets
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("SecondWindow", "SecondWindow"))
        self.logout_button.setText(_translate("SecondWindow", "Logout"))


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_loginwindow()

    #sets up the look of login window
    def setup_loginwindow(self):
        self.setObjectName("LoginWindow")
        self.setAutoFillBackground(True)

        self.login_window = QtWidgets.QWidget(self)
        self.login_window.setObjectName("login_window")


        self.front_pix = QtWidgets.QLabel(self.login_window)
        self.front_pix.setGeometry(QtCore.QRect(-1, 0, 1100, 620))
        self.front_pix.setText("")
        self.front_pix.setTextFormat(QtCore.Qt.PlainText)
        self.front_pix.setPixmap(QtGui.QPixmap("data\\front_page_moyo_1.png"))
        self.front_pix.setObjectName("front_pix")


        self.username_label = QtWidgets.QLabel(self.login_window)
        self.username_label.setGeometry(QtCore.QRect(897, 190, 110, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI Light")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.username_label.setFont(font)
        self.username_label.setObjectName("username_label")
        self.username_label.setStyleSheet('QLabel#username_label {color: white}')


        self.password_label = QtWidgets.QLabel(self.login_window)
        self.password_label.setGeometry(QtCore.QRect(900, 290, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI Light")
        font.setPointSize(14)
        self.password_label.setFont(font)
        self.password_label.setObjectName("password_label")
        self.password_label.setStyleSheet('QLabel#password_label {color: white}')


        self.login_button = QtWidgets.QPushButton(self.login_window)
        self.login_button.setGeometry(QtCore.QRect(850, 400, 201, 41))
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI Light")
        font.setPointSize(14)
        self.login_button.setFont(font)
        self.login_button.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.login_button.setAccessibleDescription("")
        self.login_button.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.login_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("data\\button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.login_button.setIcon(icon)
        self.login_button.setIconSize(QtCore.QSize(220, 41))
        self.login_button.setCheckable(False)
        self.login_button.setObjectName("login_button")


        self.loginlineEdit = QtWidgets.QLineEdit(self.login_window)
        self.loginlineEdit.setGeometry(QtCore.QRect(850, 230, 201, 41))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI Light")
        font.setPointSize(12)
        self.loginlineEdit.setFont(font)
        self.loginlineEdit.setObjectName("loginlineEdit")


        self.passwordlineEdit = QtWidgets.QLineEdit(self.login_window)
        self.passwordlineEdit.setGeometry(QtCore.QRect(850, 330, 201, 41))
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI Light")
        font.setPointSize(12)
        self.passwordlineEdit.setFont(font)
        self.passwordlineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordlineEdit.setObjectName("passwordlineEdit")

        self.login_error_label = QtWidgets.QLabel(self)
        self.login_error_label.setGeometry(QtCore.QRect(850, 440, 201, 41))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI Light")
        font.setPointSize(9)
        self.login_error_label.setFont(font)
        self.login_error_label.setObjectName("login_error_label")
        self.login_error_label.setStyleSheet('QLabel#login_error_label {color: white}')


        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    #sets the text and titles of the widgets
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("LoginWindow", "Moyo Band Panel"))
        self.username_label.setText(_translate("LoginWindow", "Username"))
        self.password_label.setText(_translate("LoginWindow", "Password"))
        self.login_button.setShortcut(_translate("LoginWindow", "Return"))
        self.login_error_label.setText(_translate("MainWindow", ""))




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.BazaData = database.Data()
        self.resize(1080, 620)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.start_login_window()

    def start_login_window(self):
        def login_button_clicked():
            self.start_second_window()

        def check_user():
            login = self.login_window.loginlineEdit.text()
            password = self.login_window.passwordlineEdit.text()

            self.BazaData.UserData(login, password)

            if self.BazaData.sd:
                    login_button_clicked()
            self.login_window.login_error_label.setText("Wrong username or password")


        self.login_window = LoginWindow()
        self.setCentralWidget(self.login_window)
        self.login_window.login_button.clicked.connect(check_user)
        self.show()

    def start_second_window(self):

        self.x =0
        self.second_window = SecondWindow()
        self.data_Name = []
        self.rect_data = []
        self.BazaData.PatientAllInfo()
        self.setCentralWidget(self.second_window)
        self.second_window.logout_button.clicked.connect(self.start_login_window)
        self.BazaData.PatientData_Counter()
        for i in range(1,self.BazaData.SumPatient+1):
            self.BazaData.PatientData(i)
            self.y=0
            self.add_Rect()
            for self.k in range(6):
                self.add_Label(str(self.BazaData.sPatientData[self.k]))
            self.x += 200

        self.show()
    def add_Label(self,name):

        data = QtWidgets.QLabel(self)
        data.setGeometry(QtCore.QRect(90+self.x, 100+self.y, 201, 41))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI Light")
        font.setPointSize(12)
        data.setFont(font)
        data.setObjectName("data_test")
        data.setStyleSheet('QLabel#data_test {color: white}')
        data.setText(name)
        self.data_Name.append(data)
        self.y+=25


        data.show()
    def add_Rect(self):
        rect = QtWidgets.QLabel(self)
        rect.setGeometry(QtCore.QRect(75 + self.x, 85, 150, 250))
        rect.setStyleSheet('QLabel#rect {background-color: black}')
        rect.setObjectName("rect")
        self.rect_data.append(rect)
        rect.show()

#executed when program ran from this file
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
