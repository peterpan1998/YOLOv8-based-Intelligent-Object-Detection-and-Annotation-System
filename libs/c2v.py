import os, cv2, shutil
from PyQt5.QtCore import  QCoreApplication
from lxml import etree, objectify
from tqdm import tqdm
from PIL import Image
from pycocotools.coco import \
    COCO
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QPushButton, QApplication, QVBoxLayout, QGroupBox, QRadioButton, QHBoxLayout, \
    QLineEdit, QWidget, QProgressDialog, QMessageBox
class Co2voc(QDialog):
    def __init__(self):
        super(Co2voc, self).__init__()
        self.init_ui()
        self.voc_path = ''
        self.coco_img_path = ''
        self.coco_json_path = ''
    def init_ui(self):
        desktop = QApplication.desktop()
        self.w = desktop.width()
        self.h = desktop.height()
        self.resize(self.w * 0.3, self.h * 0.3)
        self.setWindowTitle("coco to voc")

        self.container = QVBoxLayout()
        #
        self.gh_box1 = QGroupBox("select voc folder")
        self.h_box1 = QHBoxLayout()
        self.btn1 = QPushButton("voc")
        self.widget = QWidget()
        self.edit1 = QLineEdit(self.widget)
        self.edit1.setPlaceholderText("voc path")
        self.h_box1.addWidget(self.btn1)
        self.h_box1.addWidget(self.edit1)
        self.gh_box1.setLayout(self.h_box1)

        self.gh_box2 = QGroupBox("select coco images folder")
        self.h_box2 = QHBoxLayout()
        self.btn2 = QPushButton("coco images")
        self.widget = QWidget()
        self.edit2 = QLineEdit(self.widget)
        self.edit2.setPlaceholderText("coco images path")
        self.h_box2.addWidget(self.btn2)
        self.h_box2.addWidget(self.edit2)
        self.gh_box2.setLayout(self.h_box2)

        self.gh_box3 = QGroupBox("select coco images json ")
        self.h_box3 = QHBoxLayout()
        self.btn3 = QPushButton("name.json")
        self.widget = QWidget()
        self.edit3 = QLineEdit(self.widget)
        self.edit3.setPlaceholderText("coco name.json path")
        self.h_box3.addWidget(self.btn3)
        self.h_box3.addWidget(self.edit3)
        self.gh_box3.setLayout(self.h_box3)

        self.btn4 = QPushButton("start coco to voc")
        #
        self.container.addWidget(self.gh_box1)
        self.container.addWidget(self.gh_box2)
        self.container.addWidget(self.gh_box3)
        self.container.addWidget(self.btn4)

        self.setLayout(self.container)

        self.btn1.clicked.connect(self.btn1_clicked)  # 开始检测按钮点击事件

        self.btn2.clicked.connect(self.btn2_clicked)  # 开始检测按钮点击事件

        self.btn3.clicked.connect(self.btn3_clicked)  # 开始检测按钮点击事件

        self.btn4.clicked.connect(self.btn4_clicked)  # 开始检测按钮点击事件
    def btn1_clicked(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹",
                                                               "D:/document/v8test/coco2voc/2017valvoc/")  # 起始路径
        self.edit1.setText(directory)  # 显示读取图片路径的文本框
        self.voc_path = directory
        print(self.voc_path)
    def mkr(self,path):
        if os.path.exists(path):
            shutil.rmtree(path)
            os.mkdir(path)
        else:
            os.mkdir(path)

    def catid2name(self, coco):  # 将名字和id号建立一个字典
        classes = dict()
        for cat in coco.dataset['categories']:
            classes[cat['id']] = cat['name']
        return classes
    def save_annotations(self, filename, objs, filepath, CKimg_dir, CKanno_dir):

        annopath = CKanno_dir + "/" + filename[:-3] + "xml"  # 生成的xml文件保存路径
        dst_path = CKimg_dir + "/" + filename
        img_path = filepath
        img = cv2.imread(img_path)
        im = Image.open(img_path)
        if im.mode != "RGB":
            print(filename + " not a RGB image")
            im.close()
            return
        im.close()
        shutil.copy(img_path, dst_path)  # 把原始图像复制到目标文件夹
        E = objectify.ElementMaker(annotate=False)
        anno_tree = E.annotation(
            E.folder('1'),
            E.filename(filename),
            E.source(
                E.database('CKdemo'),
                E.annotation('VOC'),
                E.image('CK')
            ),
            E.size(
                E.width(img.shape[1]),
                E.height(img.shape[0]),
                E.depth(img.shape[2])
            ),
            E.segmented(0)
        )
        for obj in objs:
            E2 = objectify.ElementMaker(annotate=False)
            anno_tree2 = E2.object(
                E.name(obj[0]),
                E.pose(),
                E.truncated("0"),
                E.difficult(0),
                E.bndbox(
                    E.xmin(obj[2]),
                    E.ymin(obj[3]),
                    E.xmax(obj[4]),
                    E.ymax(obj[5])
                )
            )
            anno_tree.append(anno_tree2)

        etree.ElementTree(anno_tree).write(annopath, pretty_print=True)
    def showbycv(self, coco, img, classes, origin_image_dir, CKimg_dir, CKanno_dir, verbose=False):
        filename = img['file_name']
        filepath = os.path.join(origin_image_dir, filename)
        I = cv2.imread(filepath)
        annIds = coco.getAnnIds(imgIds=img['id'], iscrowd=None)
        anns = coco.loadAnns(annIds)
        objs = []
        for ann in anns:
            name = classes[ann['category_id']]
            if 'bbox' in ann:
                bbox = ann['bbox']
                xmin = (int)(bbox[0])
                ymin = (int)(bbox[1])
                xmax = (int)(bbox[2] + bbox[0])
                ymax = (int)(bbox[3] + bbox[1])
                obj = [name, 1.0, xmin, ymin, xmax, ymax]
                objs.append(obj)
                if verbose:
                    cv2.rectangle(I, (xmin, ymin), (xmax, ymax), (255, 0, 0))
                    cv2.putText(I, name, (xmin, ymin), 3, 1, (0, 0, 255))
        self.save_annotations(filename, objs, filepath, CKimg_dir, CKanno_dir)
        if verbose:
            cv2.imshow("img", I)
            cv2.waitKey(0)
    def on_progressDialog_canceled(self):
        """槽函数"""
        print("progressDialog进度对话框被取消啦！")
    def get_CK5(self, origin_anno_dir, origin_image_dir, CKimg_dir, CKanno_dir, verbose=False):
        annpath = origin_anno_dir
        print(annpath, "==========")
        coco = COCO(annpath)
        classes = self.catid2name(coco)
        imgIds = coco.getImgIds()
        # imgIds=imgIds[0:1000]#测试用，抽取10张图片，看下存储效果

        # QProgressDialog组件定义
        num = 0
        elapsed = len(tqdm(imgIds))
        print(elapsed, '========')
        self.progressDialog = QProgressDialog('转换进度', '取消', 0, elapsed, self)
        self.progressDialog.setWindowTitle('转换进度窗口')
        self.progressDialog.resize(self.w * 0.3, self.h * 0.3 * 0.2)
        self.progressDialog.canceled.connect(self.on_progressDialog_canceled)
        self.progressDialog.show()
        for imgId in tqdm(imgIds):
            img = coco.loadImgs(imgId)[0]
            self.showbycv(coco, img, classes, origin_image_dir, CKimg_dir, CKanno_dir, verbose=False)
            num += 1
            self.progressDialog.setValue(num)  # 设置当前的进度值
            if self.progressDialog.wasCanceled():  # 判断是否点了取消按钮
                # self.edit4.setText("取消了检测！")
                break
            if num >= len(tqdm(imgIds)):
                print("检测完成！")
                # self.edit4.setText("检测完成！")
            QCoreApplication.processEvents()  # 实时刷新页面
        self.progressDialog.setValue(elapsed)
    def btn2_clicked(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹",
                                                               "D:/document/v8test/coco2voc/2017valvoc/")  # 起始路径
        self.edit2.setText(directory)  # 显示读取图片路径的文本框
        self.coco_img_path = directory
        print(self.coco_img_path)
    def btn3_clicked(self):
        filename, filetype = QtWidgets.QFileDialog.getOpenFileName(self, "选取json文件", "D:/document/v8test/coco2voc/2017valvoc/"," (*.* *.*)")
        self.edit3.setText(filename)
        self.coco_json_path = filename
        print(filename)
    def btn4_clicked(self):
        if self.edit1.text() == '' or self.edit2.text() == '' or self.edit3.text() == '':
            title = 'Alert  Text         '
            info = "       所有内容不能为空 !             "
            alertText = QMessageBox()
            alertText.warning(self, title, info)
        else:
            base_dir = self.voc_path
            image_dir = base_dir +'/'+'images'
            print(image_dir)
            anno_dir = base_dir + '/' + 'annotations'
            print(anno_dir)
            self.mkr(image_dir)
            self.mkr(anno_dir)
            origin_image_dir = self.coco_img_path + '/'
            origin_anno_dir = self.coco_json_path
            verbose = True  # 是否需要看下标记是否正确的开关标记，若是true,就会把标记展示到图片上
            self.get_CK5(origin_anno_dir, origin_image_dir, image_dir, anno_dir, verbose)

            title = 'Alert  Text         '
            info = "       转换完成 !             "
            alertText = QMessageBox()
            alertText.warning(self, title, info)
            self.reset()

    def reset(self):
        self.voc_path = ''
        self.coco_img_path = ''
        self.coco_json_path = ''
        self.edit1.setText('')
        self.edit2.setText('')
        self.edit3.setText('')
        self.edit1.setPlaceholderText("voc path")
        self.edit2.setPlaceholderText("coco images path")
        self.edit3.setPlaceholderText("coco name.json path")