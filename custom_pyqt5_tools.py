from PyQt5.QtWidgets import QDialog, QLabel, QWidget, QMessageBox
from PyQt5 import QtCore
   
class MessageBox(QWidget):#继承自父类QtWidgets.QWidget
    def __init__(self, parent = None, title: str = "", message: str = ""):#parent = None代表此QWidget属于最上层的窗口,也就是MainWindows.
        QWidget.__init__(self)
        self.setGeometry(300, 300, 1000,1000)  # setGeometry()方法完成两个功能--设置窗口在屏幕上的位置和设置窗口本身的大小。它的前两个参数是窗口在屏幕上的x和y坐标。后两个参数是窗口本身的宽和高
        # self.setWindowTitle(u'窗口')  # 设置窗体标题，本行可有可无。
        # self.button = QtWidgets.QPushButton(u'测试', self)  # 创建一个按钮显示‘测试’两字
        # self.button.move(300,300)
        # self.button.clicked.connect(self.show_message)  # 信号槽
        self.title = title
        self.message = message

    def show_message(self):
        QMessageBox.critical(self, self.title, self.message)