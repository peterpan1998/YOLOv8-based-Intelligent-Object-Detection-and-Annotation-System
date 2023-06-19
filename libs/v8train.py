from PyQt5 import QtWidgets
import  os

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QDialog, QPushButton, QApplication, QVBoxLayout, QGroupBox, QRadioButton, QHBoxLayout, \
    QLineEdit, QWidget, QProgressDialog, QMessageBox

import subprocess
class Mythread(QThread):
    def __init__(self,cmd1,cmd2):

        super(Mythread, self).__init__()
        self.cmd1 = cmd1
        self.cmd2 = cmd2
    def run(self):
        # subprocess.call('start cmd', shell=True)
        os.chdir(self.cmd1)
        subprocess.call(self.cmd2, shell=True)
class YOLOv8(QDialog):

    def __init__(self,sourcepath):
        super().__init__()
        print("我是弹出条件窗口")
        if sourcepath == None:
            self.sourcepath = r'D:/'

        else:
            self.sourcepath = sourcepath.replace('/Annotations','/')
        print(self.sourcepath)
        self.init_ui()
    def init_ui(self):
        desktop = QApplication.desktop()
        self.w = desktop.width()
        self.h = desktop.height()
        self.resize(self.w * 0.4, self.h * 0.4)
        self.setWindowTitle("alertText")
        self.container = QVBoxLayout()


        self.gh_box1 = QGroupBox("set task")
        self.h_box1= QHBoxLayout()
        self.btn1 = QPushButton("task")
        self.widget = QWidget()
        self.edit1 = QLineEdit(self.widget)
        self.edit1.setText("detect")
        self.h_box1.addWidget(self.btn1)
        self.h_box1.addWidget(self.edit1)
        self.gh_box1.setLayout(self.h_box1)

        self.gh_box2 = QGroupBox("set mode")
        self.h_box2 = QHBoxLayout()
        self.btn2 = QPushButton("mode")
        self.widget = QWidget()
        self.edit2 = QLineEdit(self.widget)
        self.edit2.setText("train")
        self.h_box2.addWidget(self.btn2)
        self.h_box2.addWidget(self.edit2)
        self.gh_box2.setLayout(self.h_box2)

        self.gh_box3 = QGroupBox("select model.pt")
        self.h_box3 = QHBoxLayout()
        self.btn3 = QPushButton("model")
        self.edit3 = QLineEdit(self.widget)
        self.edit3.setPlaceholderText("select model.pt path")
        self.h_box3.addWidget(self.btn3)
        self.h_box3.addWidget(self.edit3)
        self.gh_box3.setLayout(self.h_box3)

        self.gh_box4 = QGroupBox("select data.yaml path")
        self.h_box4 = QHBoxLayout()
        self.btn4 = QPushButton("data")
        self.edit4 = QLineEdit(self.widget)
        self.edit4.setPlaceholderText("such as : select garbage.yaml path")
        self.h_box4.addWidget(self.btn4)
        self.h_box4.addWidget(self.edit4)
        self.gh_box4.setLayout(self.h_box4)

        self.gh_box5 = QGroupBox("set batch size")
        self.h_box5 = QHBoxLayout()
        self.btn5 = QPushButton("batch")
        self.edit5 = QLineEdit(self.widget)
        self.edit5.setText("32")
        self.h_box5.addWidget(self.btn5)
        self.h_box5.addWidget(self.edit5)
        self.gh_box5.setLayout(self.h_box5)

        self.gh_box6 = QGroupBox("set epochs")
        self.h_box6 = QHBoxLayout()
        self.btn6 = QPushButton("epochs")
        self.edit6 = QLineEdit(self.widget)
        self.edit6.setText("10")
        self.h_box6.addWidget(self.btn6)
        self.h_box6.addWidget(self.edit6)
        self.gh_box6.setLayout(self.h_box6)

        self.gh_box7 = QGroupBox("set imgsz")
        self.h_box7 = QHBoxLayout()
        self.btn7 = QPushButton("imgsz")
        self.edit7 = QLineEdit(self.widget)
        self.edit7.setText("640")
        self.h_box7.addWidget(self.btn7)
        self.h_box7.addWidget(self.edit7)
        self.gh_box7.setLayout(self.h_box7)

        self.gh_box8 = QGroupBox("set workers")
        self.h_box8 = QHBoxLayout()
        self.btn8 = QPushButton("workers")
        self.edit8 = QLineEdit(self.widget)
        self.edit8.setText("16")
        self.h_box8.addWidget(self.btn8)
        self.h_box8.addWidget(self.edit8)
        self.gh_box8.setLayout(self.h_box8)

        self.gh_box9 = QGroupBox("set device")
        self.h_box9 = QHBoxLayout()
        self.btn9 = QPushButton("device")
        self.edit9 = QLineEdit(self.widget)
        self.edit9.setText("0")
        self.h_box9.addWidget(self.btn9)
        self.h_box9.addWidget(self.edit9)
        self.gh_box9.setLayout(self.h_box9)

        self.btn10 = QPushButton("start train")

        self.btn3.clicked.connect(self.btn3_clicked) #选取基础的权重文件
        self.btn4.clicked.connect(self.btn4_clicked) #选取garbage.yaml文件
        self.btn10.clicked.connect(self.btn10_clicked)#开始模型的训练
        self.edit10 = QLineEdit(self.widget)


        self.container.addWidget(self.gh_box1)
        self.container.addWidget(self.gh_box2)
        self.container.addWidget(self.gh_box3)
        self.container.addWidget(self.gh_box4)
        self.container.addWidget(self.gh_box5)
        self.container.addWidget(self.gh_box6)
        self.container.addWidget(self.gh_box7)
        self.container.addWidget(self.gh_box8)
        self.container.addWidget(self.gh_box9)
        self.container.addWidget(self.edit10)
        self.container.addWidget(self.btn10)
        self.setLayout(self.container)

    def btn3_clicked(self):
        filename, filetype = QtWidgets.QFileDialog.getOpenFileName(self, "选取pt文件", self.sourcepath, " (*.* *.*)")
        print(filename)
        self.edit3.setText(filename)
        self.model_path = filename
    def btn4_clicked(self):
        filename, filetype = QtWidgets.QFileDialog.getOpenFileName(self, "选取yaml文件", self.sourcepath, " (*.* *.*)")
        print(filename)
        self.edit4.setText(filename)
        self.garbage_yaml_path = filename
    def btn10_clicked(self):
        if(self.edit1.text()=='' or self.edit2.text()=='' or self.edit3.text()=='' or self.edit4.text()=='' or  self.edit5.text()=='' or self.edit6.text()=='' or self.edit7.text()=='' or self.edit8.text()=='' or self.edit9.text()==''):
            title = 'Alert  Text         '
            info = "       所有内容不能为空 !             "
            alertText = QMessageBox()
            alertText.warning(self, title, info)
        else:
            command = "yolo "
            command = command + 'task=' +self.edit1.text() + ' mode='+self.edit2.text()+' model='+self.edit3.text()+' data='+self.edit4.text()+' batch='+self.edit5.text()+' epochs='+self.edit6.text()+' imgsz='+self.edit7.text()+' workers='+self.edit8.text()+' device='+self.edit9.text()+' show=True'

            dir_list = self.garbage_yaml_path.split("/")
            dir_list.pop()
            dir_list.pop()
            dir_path = "/".join(dir_list)
            print(dir_path)
            print(command)
            self.mythread = Mythread(dir_path,command)
            self.mythread.start()
            title = 'Alert  Text         '
            info = "       请在刚刚打开的cmd命令窗口中查看训练的中间过程  !             "
            alertText = QMessageBox()
            alertText.warning(self, title, info)

            self.edit3.setText('')
            self.edit4.setText('')
            self.edit3.setPlaceholderText("select model.pt path")
            self.edit4.setPlaceholderText("such as : select garbage.yaml path")