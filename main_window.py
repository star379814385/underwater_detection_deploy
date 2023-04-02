import sys
import cv2
from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QDialog, QMessageBox

from Ui_detection import Ui_MainWindow
from utils import read_image
import numpy as np
from detector_onnx import URPC_Detector
import copy


def rgb2label(img: np.ndarray, win_label: QtWidgets.QLabel):
        # 后面这几行代码几乎都一样，可以尝试封装成一个函数
        rows, cols, channels = img.shape
        bytesPerLine = channels * cols
        # Qt显示图片时，需要先转换成QImgage类型
        QImg = QImage(img.data, cols, rows, bytesPerLine, QImage.Format_RGB888)
        # self.labelCapture.setPixmap(QPixmap.fromImage(QImg).scaled(
        #     self.labelCapture.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        win_label.setPixmap(QPixmap.fromImage(QImg).scaled(win_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

class EmittingStr(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str) #定义一个发送str的信号
    def write(self, text):
      self.textWritten.emit(str(text))

class URPC_Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.img = None
        self.detector = None
        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        sys.stderr = EmittingStr(textWritten=self.outputWritten)
        # self.set_detector()
        
    def load_model_clicked(self):
        default_dir = str(Path(__file__).parent / "model_zoo")
                # 打开文件选取对话框
        filename,  _ = QFileDialog.getOpenFileName(
            self, 
            caption='选择模型',
            directory=default_dir,
            filter="onnx模型文件(*.onnx)",
        )
        if filename:
            try:
                self.detector = URPC_Detector(filename)
            except:
                self.after_loading_bad_model()
                return 
        print("读取模型成功！")
    
    def after_loading_bad_image(self):
        QMessageBox.critical(self, "错误", "读取图片失败")
        
    
    def after_loading_bad_model(self):
        QMessageBox.critical(self, "错误", "读取模型失败")
    
    def not_init_model(self):
        QMessageBox.critical(self, "错误", "未初始化模型") 

    def load_image_clicked(self):
        '''
        从本地读取图片
        '''
        # 打开文件选取对话框
        filename,  _ = QFileDialog.getOpenFileName(
            self, 
            caption='选择图像',
            # directory=default_dir,
            filter="图像文件(*.jpg *.png *.bmp);;全部文件()",
        )
        if filename:
            try:
                self.img = read_image(str(filename))
                assert self.img is not None
            except:
                self.after_loading_bad_image()
                return 
            # OpenCV图像以BGR通道存储，显示时需要从BGR转到RGB
            img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            rgb2label(img, self.ori_win)

    def detect_clicked(self):
        if self.detector is None:
            self.not_init_model()
            return 
        detections, img_vis = self.detector.predict(copy.deepcopy(self.img))
        img_vis = cv2.cvtColor(img_vis, cv2.COLOR_BGR2RGB)
        rgb2label(img_vis, self.vis_win)
        print("检测成功！")
        for detection in detections:
            print("{}: {}".format(detection["class_name"], [round(x) for x in detection["box"]]))
        

    def exit_clicked(self):
        exit()
        
    def outputWritten(self, text):
        cursor = self.output_text.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.output_text.setTextCursor(cursor)
        self.output_text.ensureCursorVisible()


    

if __name__ == "__main__":
    pass
    # app = QtWidgets.QApplication(sys.argv)
    # window = PyqtDemo()
    # window.show()
    # sys.exit(app.exec_())
