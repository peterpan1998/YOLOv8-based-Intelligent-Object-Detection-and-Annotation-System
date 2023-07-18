from PyQt5 import QtWidgets
import  os
from libs.jindu import *
from PyQt5.QtCore import QThread, QCoreApplication
from PyQt5.QtWidgets import QDialog, QPushButton, QApplication, QVBoxLayout, QGroupBox, QRadioButton, QHBoxLayout, \
    QLineEdit, QWidget, QProgressDialog, QMessageBox
import time
import subprocess
from xml.etree import ElementTree as ET
from os import getcwd
class Xml2TXT(QDialog):

    def __init__(self,sourcepath,flag,last_open_dir):
        super().__init__()
        print("我是弹出条件窗口")
        self.flag = flag
        self.last_open_dir = last_open_dir
        self.default_save_dir = sourcepath
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
        self.resize(self.w * 0.4, self.h * 0.2)
        self.setWindowTitle("XML TO TXT")
        self.container = QVBoxLayout()


        self.gh_box1 = QGroupBox("set names")
        self.h_box1= QHBoxLayout()
        self.btn1 = QPushButton("names")
        self.widget = QWidget()
        self.edit1 = QLineEdit(self.widget)
        self.edit1.setPlaceholderText("such as: name1,name2,name3,...")
        self.h_box1.addWidget(self.btn1)
        self.h_box1.addWidget(self.edit1)
        self.gh_box1.setLayout(self.h_box1)


        self.btn10 = QPushButton("start xml to txt")

        self.btn10.clicked.connect(self.btn10_clicked)#开始模型的训练
        self.edit10 = QLineEdit(self.widget)


        self.container.addWidget(self.gh_box1)
        self.container.addWidget(self.edit10)
        self.container.addWidget(self.btn10)
        self.setLayout(self.container)

        # year ='2012', 对应图片的id（文件名）
        # xml文件转换成txt文件的开始
        # 进行归一化操作
    def convert(self, size, box):  # size:(原图w,原图h) , box:(xmin,xmax,ymin,ymax)
            if size[0] == 0.:
                dw = 1.0 / 1.0  # 1/w
            else:

                dw = 1.0 / size[0]  # 1/w
            if size[1] == 0.:
                dh = 1.0 / 1.  # 1/h
            else:

                dh = 1.0 / size[1]  # 1/h
            x = (box[0] + box[1]) / 2.0  # 物体在图中的中心点x坐标
            y = (box[2] + box[3]) / 2.0  # 物体在图中的中心点y坐标
            w = box[1] - box[0]  # 物体实际像素宽度
            h = box[3] - box[2]  # 物体实际像素高度
            x = x * dw  # 物体中心点x的坐标比(相当于 x/原图w)
            w = w * dw  # 物体宽度的宽度比(相当于 w/原图w)
            y = y * dh  # 物体中心点y的坐标比(相当于 y/原图h)
            h = h * dh  # 物体宽度的宽度比(相当于 h/原图h)
            return (x, y, w, h)
    def convert_annotation(self, image_id):
        # classes = ['1', '2', '3', '4']
        str1 = self.edit1.text()
        classes = []
        if ',' in str1:
            classes = str1.split(',')
        if '，' in str1:
            classes = str1.split('，')
        else:
            classes.append(str1)
        # classes.append()
        # 对应的通过year 找到相应的文件夹，并且打开相应image_id的xml文件，其对应bund文件
        in_file = open(self.default_save_dir + '/%s.xml' % (image_id), encoding='utf-8')
        # 准备在对应的image_id 中写入对应的label，分别为
        # <object-class> <x> <y> <width> <height>
        xmlfilepath1 = self.default_save_dir
        labelpath = xmlfilepath1.replace('/Annotations', '/labels')
        if not os.path.exists(labelpath):
            os.makedirs(labelpath)
        out_file = open(labelpath + '/%s.txt' % (image_id), 'w', encoding='utf-8')
        # 解析xml文件
        tree = ET.parse(in_file)
        # 获得对应的键值对
        root = tree.getroot()
        # 获得图片的尺寸大小
        size = root.find('size')
        # 如果xml内的标记为空，增加判断条件
        if size != None:
            # 获得宽
            w = int(size.find('width').text)
            # 获得高
            h = int(size.find('height').text)
            # 遍历目标obj
            for obj in root.iter('object'):
                # 获得difficult ？？
                difficult = obj.find('difficult').text
                # 获得类别 =string 类型
                cls = obj.find('name').text
                # 如果类别不是对应在我们预定好的class文件中，或difficult==1则跳过
                if cls not in classes or int(difficult) == 1:
                    continue
                # 通过类别名称找到id
                cls_id = classes.index(cls)
                # 找到bndbox 对象
                xmlbox = obj.find('bndbox')
                # 获取对应的bndbox的数组 = ['xmin','xmax','ymin','ymax']
                b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                     float(xmlbox.find('ymax').text))
                print(image_id, cls, b)
                # 带入进行归一化操作
                # w = 宽, h = 高， b= bndbox的数组 = ['xmin','xmax','ymin','ymax']
                bb = self.convert((w, h), b)
                # bb 对应的是归一化后的(x,y,w,h)
                # 生成 calss x y w h 在label文件中
                out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    def on_progressDialog_canceled(self):
        """槽函数"""
        print("progressDialog进度对话框被取消啦！")
    def btn10_clicked(self):
        # print(self.edit1.text())
        print(self.sourcepath,'==========')

        print(self.edit1.text())

        if self.flag == 1:
            if len(self.edit1.text()) == 0:
                title = 'Alert  Text         '
                info = "       please write names  !             "
                alertText = QMessageBox()
                alertText.warning(self, title, info)
            else:
                print("xmltotxt")
                sets = ['train', 'test', 'val']
                for image_set in sets:
                    '''
                    对所有的文件数据集进行遍历
                    做了两个工作：
                　　　　１．将所有图片文件都遍历一遍，并且将其所有的全路径都写在对应的txt文件中去，方便定位
                　　　　２．同时对所有的图片文件进行解析和转化，将其对应的bundingbox 以及类别的信息全部解析写到label 文件中去
                    　　　　　最后再通过直接读取文件，就能找到对应的label 信息
                    '''
                    # 先找labels文件夹如果不存在则创建
                    xmlfilepath1 = self.default_save_dir
                    labelpath = xmlfilepath1.replace('/Annotations', '/labels/')
                    if not os.path.exists(labelpath):
                        os.makedirs(labelpath)
                    # 读取在ImageSets/Main 中的train、test..等文件的内容
                    # 包含对应的文件名称
                    imagesetspath = xmlfilepath1.replace('/Annotations', '/ImageSets')
                    image_ids = open(imagesetspath + '/%s.txt' % (image_set)).read().strip().split()
                    # 打开对应的2012_train.txt 文件对其进行写入准备
                    listdatafilepath = xmlfilepath1.replace('/Annotations', '/')
                    list_file = open(listdatafilepath + '%s.txt' % (image_set), 'w')




                    elapsed = len(image_ids)
                    # QProgressDialog组件定义
                    self.progressDialog = QProgressDialog(image_set+' 转换进度', '取消', 0, elapsed, self)
                    self.progressDialog.setWindowTitle(image_set+' 转换进度窗口')
                    self.progressDialog.resize(self.w * 0.3, self.h * 0.3 * 0.2)
                    self.progressDialog.canceled.connect(self.on_progressDialog_canceled)
                    self.progressDialog.show()

                    # 将对应的文件_id以及全路径写进去并换行
                    for process, image_id in enumerate(image_ids):
                        list_file.write(self.last_open_dir + '/%s.jpg\n' % (image_id))
                        # 调用  year = 年份  image_id = 对应的文件名_id
                        self.convert_annotation(image_id)



                        self.progressDialog.setValue(process)  # 设置当前的进度值
                        QCoreApplication.processEvents()  # 实时刷新页面
                        if self.progressDialog.wasCanceled():  # 判断是否点了取消按钮
                            self.edit10.setText(image_set+" 取消了检测！")
                            break
                        if process >= len(image_ids):
                            print("检测完成！")
                            self.edit10.setText(image_set+" 检测完成！")



                    # 关闭文件
                    self.progressDialog.setValue(elapsed)
                    list_file.close()



                # title = 'Alert  Text         '
                # info = "       xml to txt  complete !             "
                # alertText = QMessageBox()
                # alertText.information(self, title, info)
                self.edit1.setText('')
                self.edit1.setPlaceholderText("such as: name1,name2,name3,...")
                self.edit10.setPlaceholderText("xml to txt  complete !")
        else:
            title = 'Alert  Text         '
            info = "       please split dataset  !             "
            alertText = QMessageBox()
            alertText.warning(self, title, info)
