import os

from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QDialog, QPushButton, QApplication, QVBoxLayout, QGroupBox, QRadioButton, QHBoxLayout, \
    QLineEdit, QWidget, QProgressDialog, QMessageBox


class AlertText(QDialog):
    def __init__(self,sourcepath):
        super().__init__()
        print("我是弹出条件窗口")
        if sourcepath == None:
            self.sourcepath = r'D:\document\python_project\project1\python_tools\data/'

        else:
            self.sourcepath = sourcepath.replace('/Annotations','/')
        print(self.sourcepath)
        self.init_ui()
        self.train_path = ''
        self.val_path = ''
        self.test_path = ''
    def init_ui(self):
        desktop = QApplication.desktop()
        self.w = desktop.width()
        self.h = desktop.height()
        self.resize(self.w * 0.3, self.h * 0.3)
        self.setWindowTitle("create yaml")

        self.container = QVBoxLayout()

        self.gh_box = QGroupBox("select train.txt")
        self.h_box = QHBoxLayout()
        self.btn4 = QPushButton("train.txt") #选择train.txt的按钮
        self.widget = QWidget()
        self.edit = QLineEdit(self.widget)
        self.edit.setPlaceholderText("select train.txt path") #显示train.txt文件的路径
        self.h_box.addWidget(self.btn4)
        self.h_box.addWidget(self.edit)
        self.gh_box.setLayout(self.h_box)

        self.gh_box2 = QGroupBox("select val.txt")
        self.h_box2 = QHBoxLayout()
        self.btn5 = QPushButton("val.txt")  #选择读取图片路径的按钮
        self.edit2 = QLineEdit(self.widget)
        self.edit2.setPlaceholderText("select val.txt path")#显示val.txt路径的文本框
        self.h_box2.addWidget(self.btn5)
        self.h_box2.addWidget(self.edit2)
        self.gh_box2.setLayout(self.h_box2)

        self.gh_box3 = QGroupBox("select test.txt")
        self.h_box3 = QHBoxLayout()
        self.btn6 = QPushButton("test.txt")
        self.edit3 = QLineEdit(self.widget)
        self.edit3.setPlaceholderText("select test.txt path")
        self.h_box3.addWidget(self.btn6)
        self.h_box3.addWidget(self.edit3)
        self.gh_box3.setLayout(self.h_box3)

        self.gh_box4 = QGroupBox("set number of classes")
        self.h_box4 = QHBoxLayout()
        self.btn7 = QPushButton("nc")
        self.edit5 = QLineEdit(self.widget)
        self.edit5.setPlaceholderText("such as: 4")
        self.h_box4.addWidget(self.btn7)
        self.h_box4.addWidget(self.edit5)
        self.gh_box4.setLayout(self.h_box4)

        self.gh_box5 = QGroupBox("set class names")
        self.h_box5 = QHBoxLayout()
        self.btn8 = QPushButton("names")
        self.edit6 = QLineEdit(self.widget)
        self.edit6.setPlaceholderText("name1,name2,name3,name4,......")
        self.h_box5.addWidget(self.btn8)
        self.h_box5.addWidget(self.edit6)
        self.gh_box5.setLayout(self.h_box5)

        self.gh_box6 = QGroupBox("yaml name")
        self.h_box6 = QHBoxLayout()
        self.btn9 = QPushButton("name.yaml")
        self.edit7 = QLineEdit(self.widget)
        self.edit7.setPlaceholderText("such as : garbage.yaml")
        self.h_box6.addWidget(self.btn9)
        self.h_box6.addWidget(self.edit7)
        self.gh_box6.setLayout(self.h_box6)

        self.container.addWidget(self.gh_box)
        self.container.addWidget(self.gh_box2)
        self.container.addWidget(self.gh_box3)
        self.container.addWidget(self.gh_box4)
        self.container.addWidget(self.gh_box5)
        self.container.addWidget(self.gh_box6)

        self.btn1 = QPushButton("create yaml")
        self.edit4 =QLineEdit(self.widget)#显示创建结果
        self.edit4.setPlaceholderText("还没创建yaml文件")

        self.container.addWidget(self.edit4)
        self.container.addWidget(self.btn1)

        self.setLayout(self.container)

        self.btn1.clicked.connect(self.btn1_clicked)  # 创建yaml按钮点击事件
        self.btn4.clicked.connect(self.btn4_clicked)  # 选择train.txt文件按钮的点击事件
        self.btn5.clicked.connect(self.btn5_clicked)  # 选择val.txt文件按钮的点击事件
        self.btn6.clicked.connect(self.btn6_clicked)  # 选择test.txt文件按钮的点击事件
    def btn1_clicked(self):
        if self.train_path == '' or self.test_path == '' or self.val_path == '' or self.edit6.text() == '' or self.edit5.text() == '':

            title = 'Alert  Text         '
            info = "       所有内容不能为空 !             "
            alertText = QMessageBox()
            alertText.warning(self, title, info)
        else:
            print(type(self.edit5.text()), '++++')
            namesstr = self.edit6.text()
            new_namestr = ''
            namelist = []
            if '，' in namesstr:
                namelist = namesstr.split('，')
                print(namelist)
            if ',' in namesstr:
                namelist = namesstr.split(',')
            else:
                namelist = "['"+namesstr+"']"
            print(namelist,'********')
            yamlname = self.sourcepath+self.edit7.text()
            if '.yaml' in yamlname:
                with open(yamlname,'w',encoding='utf-8') as f:
                    print(str(namelist),'-------------------')
                    f.write('train: '+self.train_path+'\n'+'val: '+self.val_path+'\n'+'test: '+self.test_path+'\n'+'nc: '+self.edit5.text()+'\n'+'names: '+str(namelist))
                title = 'Alert  Text         '
                info = "       创建成功 !             "
                alertText = QMessageBox()
                alertText.warning(self, title, info)
                self.edit4.setText("创建成功！")
                self.reset()
            else:
                title = 'Alert  Text         '
                info = "       请填写正确的文件名 !             "
                alertText = QMessageBox()
                alertText.warning(self, title, info)

    def btn4_clicked(self):
        # directory = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹","D:/document/python_project/project1/python_tools/data/")  # 起始路径
        filename, filetype = QtWidgets.QFileDialog.getOpenFileName(self, "选取Excel文件", self.sourcepath," (*.* *.*)")
        print(filename)
        self.edit.setText(filename)
        self.train_path = filename
    def btn5_clicked(self):
        # directory = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹","D:/document/python_project/project1/python_tools/data/")  # 起始路径
        filename, filetype = QtWidgets.QFileDialog.getOpenFileName(self, "选取Excel文件", self.sourcepath," (*.* *.*)")
        print(filename)
        self.edit2.setText(filename)
        self.val_path = filename
    def btn6_clicked(self):
        filename, filetype = QtWidgets.QFileDialog.getOpenFileName(self, "选取Excel文件", self.sourcepath, " (*.* *.*)")
        print(filename)
        self.edit3.setText(filename)
        self.test_path = filename
    def reset(self):
        self.train_path = ''
        self.val_path = ''
        self.test_path = ''
        self.edit5.setText('')
        self.edit.setText('')
        self.edit2.setText('')
        self.edit3.setText('')
        self.edit6.setText('')
        self.edit7.setText('')
        self.edit7.setPlaceholderText("such as: garbage.yaml")
        self.edit.setPlaceholderText("select train.txt path")  # 显示train.txt文件的路径
        self.edit2.setPlaceholderText("select val.txt path")  # 显示val.txt路径的文本框
        self.edit3.setPlaceholderText("select test.txt path")
        self.edit5.setPlaceholderText("such as: 4")
        self.edit6.setPlaceholderText("name1,name2,name3,name4,......")
        self.edit7.text()
