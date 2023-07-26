from PyQt5.QtWidgets import QDialog, QPushButton, QApplication, QVBoxLayout, QGroupBox, QRadioButton, QHBoxLayout, \
    QLineEdit, QWidget, QProgressDialog
# from libs.yolov8_detect import *
from PyQt5 import QtWidgets
import os
import glob
from xml.etree import ElementTree as ET
from ultralytics import YOLO  # YOLOV8
from PyQt5.QtCore import Qt, QCoreApplication
from labelImg import *
quan_ju_img_path = ''

class Child(QDialog):
    def __init__(self):
        super().__init__()
        
        self.init_ui()
        self.weight_path = '' # 模型路径
        self.imgdir = ''  # 图片路径
        self.xmldir = ''  # 标注文件保存路径
    def init_ui(self):
        desktop = QApplication.desktop()
        self.w = desktop.width()
        self.h = desktop.height()
        self.resize(self.w * 0.3, self.h * 0.3)
        self.setWindowTitle("Automatic detection window")
        self.container = QVBoxLayout()
        self.gh_box = QGroupBox("select pt")

        self.h_box = QHBoxLayout()
        self.btn4 = QPushButton("select weight file") #选择权重文件的按钮
        self.widget = QWidget()
        self.edit = QLineEdit(self.widget)
        self.edit.setPlaceholderText("select weight file") #显示权重文件的路径

        self.h_box.addWidget(self.btn4)
        self.h_box.addWidget(self.edit)
        self.gh_box.setLayout(self.h_box)

        self.gh_box2 = QGroupBox("select img")
        self.h_box2 = QHBoxLayout()
        self.btn5 = QPushButton("select img path")  #选择读取图片路径的按钮
        self.edit2 = QLineEdit(self.widget)
        self.edit2.setPlaceholderText("select img path")#显示读取图片路径的文本框
        self.h_box2.addWidget(self.btn5)
        self.h_box2.addWidget(self.edit2)
        self.gh_box2.setLayout(self.h_box2)

        self.gh_box3 = QGroupBox("select xml")
        self.h_box3 = QHBoxLayout()
        self.btn6 = QPushButton("select xml path")
        self.edit3 = QLineEdit(self.widget)
        self.edit3.setPlaceholderText("select xml path")
        self.h_box3.addWidget(self.btn6)
        self.h_box3.addWidget(self.edit3)
        self.gh_box3.setLayout(self.h_box3)

        self.container.addWidget(self.gh_box)
        self.container.addWidget(self.gh_box2)
        self.container.addWidget(self.gh_box3)
        self.btn1 = QPushButton("START DETECTION")
        self.edit4 =QLineEdit(self.widget)#显示每个具体被标注的内容
        # self.edit4.setPlaceholderText("hhhh")

        self.container.addWidget(self.edit4)
        self.container.addWidget(self.btn1)

        self.setLayout(self.container)

        self.btn1.clicked.connect(self.btn1_clicked) #开始检测按钮点击事件
        self.btn4.clicked.connect(self.btn4_clicked) #选择权重文件按钮的点击事件
        self.btn5.clicked.connect(self.btn5_clicked) #选择图片路径按钮的点击事件
        self.btn6.clicked.connect(self.btn6_clicked) #选择xml文件的保存路径
    def btn1_clicked(self):
        
        if self.weight_path == '' :
            self.progressDialog1 = QProgressDialog('请选择权重文件路径！', '取消', 0, 0, self)
            self.progressDialog1.setWindowTitle('警告窗口')
            self.progressDialog1.resize(self.w * 0.3, self.h * 0.3 * 0.2)
            self.progressDialog1.canceled.connect(self.on_progressDialog_canceled)
            self.progressDialog1.show()
        elif self.imgdir == '':
            self.progressDialog1 = QProgressDialog('请选择 img 文件打开的路径！', '取消', 0, 0, self)
            self.progressDialog1.setWindowTitle('警告窗口')
            self.progressDialog1.resize(self.w * 0.3, self.h * 0.3 * 0.2)
            self.progressDialog1.canceled.connect(self.on_progressDialog_canceled)
            self.progressDialog1.show()
        elif self.xmldir == '':
            self.progressDialog1 = QProgressDialog('请选择 XML 文件保存的路径！', '取消', 0, 0, self)
            self.progressDialog1.setWindowTitle('警告窗口')
            self.progressDialog1.resize(self.w * 0.3, self.h * 0.3 * 0.2)
            self.progressDialog1.canceled.connect(self.on_progressDialog_canceled)
            self.progressDialog1.show()
        else:
            self.Auto_label(self.weight_path, self.imgdir, self.xmldir)

    def btn4_clicked(self):
        
        filename, filetype = QtWidgets.QFileDialog.getOpenFileName(self, "选取Excel文件", "D:/document/python_project/project1/python_tools/data/"," (*.* *.*)")
        print(filename)
        self.edit.setText(filename)
        self.weight_path = filename

    def btn5_clicked(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹",
                                                               "D:/document/python_project/project1/python_tools/data/")  # 起始路径
        self.edit2.setText(directory)  # 显示读取图片路径的文本框
        self.imgdir = directory
        quan_ju_img_path = directory
        print(self.imgdir)
    def btn6_clicked(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹",
                                                               "D:/document/python_project/project1/python_tools/data/")  # 起始路径
        self.edit3.setText(directory)
        self.xmldir = directory
        print(self.xmldir)

    def create_object(self,root, xyxy, names, cls):  # 参数依次，树根，xmin，ymin，xmax，ymax
        # 创建一级分支object
        _object = ET.SubElement(root, 'object')
        # 创建二级分支
        name = ET.SubElement(_object, 'name')
        # print(obj_name)
        name.text = str(names[int(cls)])
        pose = ET.SubElement(_object, 'pose')
        pose.text = 'Unspecified'
        truncated = ET.SubElement(_object, 'truncated')
        truncated.text = '0'
        difficult = ET.SubElement(_object, 'difficult')
        difficult.text = '0'
        # 创建bndbox
        bndbox = ET.SubElement(_object, 'bndbox')
        xmin = ET.SubElement(bndbox, 'xmin')
        xmin.text = '%s' % int(xyxy[0])
        ymin = ET.SubElement(bndbox, 'ymin')
        ymin.text = '%s' % int(xyxy[1])
        xmax = ET.SubElement(bndbox, 'xmax')
        xmax.text = '%s' % int(xyxy[2])
        ymax = ET.SubElement(bndbox, 'ymax')
        ymax.text = '%s' % int(xyxy[3])

    # 创建xml文件的函数
    def create_tree(self,image_path, h, w):
        # 创建树根annotation
        annotation = ET.Element('annotation')
        # 创建一级分支folder
        folder = ET.SubElement(annotation, 'folder')
        # 添加folder标签内容
        folder.text = os.path.dirname(image_path)

        # 创建一级分支filename
        filename = ET.SubElement(annotation, 'filename')
        filename.text = os.path.basename(image_path)

        # 创建一级分支path
        path = ET.SubElement(annotation, 'path')

        path.text = image_path  # 用于返回当前工作目录getcwd() + '\{}'.format

        # 创建一级分支source
        source = ET.SubElement(annotation, 'source')
        # 创建source下的二级分支database
        database = ET.SubElement(source, 'database')
        database.text = 'Unknown'

        # 创建一级分支size
        size = ET.SubElement(annotation, 'size')
        # 创建size下的二级分支图像的宽、高及depth
        width = ET.SubElement(size, 'width')
        width.text = str(w)
        height = ET.SubElement(size, 'height')
        height.text = str(h)
        depth = ET.SubElement(size, 'depth')
        depth.text = '3'

        # 创建一级分支segmented
        segmented = ET.SubElement(annotation, 'segmented')
        segmented.text = '0'

        return annotation

    def pretty_xml(self,element, indent, newline, level=0):  # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
        if element:  # 判断element是否有子元素
            if (element.text is None) or element.text.isspace():  # 如果element的text没有内容
                element.text = newline + indent * (level + 1)
            else:
                element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
                # else:  # 此处两行如果把注释去掉，Element的text也会另起一行
                # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
        temp = list(element)  # 将element转成list
        for subelement in temp:
            if temp.index(subelement) < (len(temp) - 1):  # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
                subelement.tail = newline + indent * (level + 1)
            else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
                subelement.tail = newline + indent * level
            self.pretty_xml(subelement, indent, newline, level=level + 1)  # 对子元素进行递归操作

    def on_progressDialog_canceled(self):
        """槽函数"""
        print("progressDialog进度对话框被取消啦！")
    def Auto_label(self,weight, imgdir, xmldir):
        # load model
        model = YOLO(weight)
        img_list = glob.glob('%s/*.*' % imgdir)
        num = 0
        elapsed = len(img_list)
        # QProgressDialog组件定义
        self.progressDialog = QProgressDialog('检测进度', '取消', 0, elapsed, self)
        self.progressDialog.setWindowTitle('检测进度窗口')
        self.progressDialog.resize(self.w * 0.3, self.h * 0.3*0.2)
        self.progressDialog.canceled.connect(self.on_progressDialog_canceled)
        self.progressDialog.show()

        for img_path in img_list:

            print(img_path)
            results = model(img_path, show=False, save=False)[0]  # predict on an image
            # 创建xml文件
            annotation = self.create_tree(img_path, results.orig_shape[0], results.orig_shape[1])
            det = results.boxes
            names = results.names

            cls = det.cls
            for i in range(len(det)):
                self.create_object(annotation, det.xyxy[i], names, cls[i])
            # 将树模型写入xml文件
            tree = ET.ElementTree(annotation)
            root = tree.getroot()
            self.pretty_xml(root, '\t', '\n')
            # tree.write('.\{}\{}.xml'.format(outdir, image_name.strip('.jpg')), encoding='utf-8')
            tree.write(img_path.replace(imgdir, xmldir).replace('.jpg', '.xml'), encoding='utf-8')
            num += 1
            self.progressDialog.setValue(num)  # 设置当前的进度值
            QCoreApplication.processEvents()  # 实时刷新页面
            if self.progressDialog.wasCanceled():   # 判断是否点了取消按钮
                self.edit4.setText("取消了检测！")
                break
            if num >= len(img_list):
                print("检测完成！")
                self.edit4.setText("检测完成！")
        self.progressDialog.setValue(elapsed)
