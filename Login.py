import pymysql
from PyQt5.Qt import QWidget
from PyQt5 import QtGui,QtWidgets
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import (QFrame, QApplication, QDialog, QDialogButtonBox,
        QMessageBox, QVBoxLayout, QLineEdit, QTableWidgetItem, QTableWidget, QHBoxLayout, QPushButton)
from functools import partial
import sys
from MainPage import MainPage

class Login(QDialog):
    connection = pymysql.connect(host='localhost', port=3306, user='root',
                                 password='000000', db='database_lab1', charset='utf8')
    cursor = connection.cursor()

    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.resize(210, 160)
        self.setWindowTitle('登录')

        # self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        ###### 设置界面控件
        self.frame = QFrame(self)
        self.verticalLayout = QVBoxLayout(self.frame)

        self.lineEdit_account = QLineEdit()
        self.lineEdit_account.setPlaceholderText("请输入账号")
        self.verticalLayout.addWidget(self.lineEdit_account)

        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setPlaceholderText("请输入密码")
        self.verticalLayout.addWidget(self.lineEdit_password)

        self.pushButton_enter = QPushButton()
        self.pushButton_enter.setText("确定")
        self.verticalLayout.addWidget(self.pushButton_enter)

        self.pushButton_quit = QPushButton()
        self.pushButton_quit.setText("取消")
        self.verticalLayout.addWidget(self.pushButton_quit)

        self.pushButton_enter.clicked.connect(self.on_pushbutton_enter_clicked)
        self.pushButton_quit.clicked.connect(QCoreApplication.instance().quit)

        if Login.exec_(self) == QDialog.Accepted:
            mainpage = MainPage()
            mainpage.show()
            sys.exit(app.exec_())

    def on_pushbutton_enter_clicked(self):
        # 账号判断
        if self.lineEdit_account.text() == "":
            return

        # 密码判断
        if self.lineEdit_password.text() == "":
            return

        account = self.lineEdit_account.text()
        password = self.lineEdit_password.text()

        self.cursor.execute("select password from users where username = '" + account + "'")
        row_1 = self.cursor.fetchone()
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

        # 通过验证，关闭对话框并返回1
        if password == row_1[0]:
            self.accept()
        else:
            QMessageBox.warning(self, "Error", u'您输入的密码有误',
                                      buttons=QMessageBox.Ok, defaultButton=QMessageBox.Ok)


app = QApplication(sys.argv)
c = Login()
c.show()
sys.exit(app.exec_())
