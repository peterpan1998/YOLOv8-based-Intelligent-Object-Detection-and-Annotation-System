import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
    QFileDialog, QDialog


class YOLOv8Trainer(QDialog):

    def __init__(self):
        super().__init__()

        # 创建布局管理器
        self.v_layout = QVBoxLayout()
        self.h_layouts = {}

        # 添加任务选项
        self.add_option("Task")

        # 添加模式选项
        self.add_option("Mode")

        # 添加模型选项
        self.add_file_option("Model")

        # 添加数据选项
        self.add_file_option("Data")

        # 添加批量大小选项
        self.add_int_option("Batch", default_value=64)

        # 添加 epochs 选项
        self.add_int_option("Epochs", default_value=10)

        # 添加图片大小选项
        self.add_int_option("Imgsz", default_value=640)

        # 添加 workers 选项
        self.add_int_option("Workers", default_value=4)

        # 添加 device 选项
        self.add_int_option("Device", default_value=0)

        # 添加开始按钮
        self.add_button("Start", self.start_training)

        # 设置窗口布局
        self.setLayout(self.v_layout)
        self.setWindowTitle("YOLOv8 Trainer GUI")
        desktop = QApplication.desktop()
        self.w = desktop.width()
        self.h = desktop.height()
        self.resize(self.w * 0.3, self.h * 0.3)

    def add_option(self, name):
        # 创建水平布局
        h_layout = QHBoxLayout()
        self.h_layouts[name] = h_layout

        # 添加标签和文本框
        label = QLabel(name)
        h_layout.addWidget(label)
        line_edit = QLineEdit()
        h_layout.addWidget(line_edit)

        # 将布局添加到垂直布局中
        self.v_layout.addLayout(h_layout)

    def add_file_option(self, name):
        # 创建水平布局
        h_layout = QHBoxLayout()
        self.h_layouts[name] = h_layout

        # 添加标签和文本框
        label = QLabel(name)
        h_layout.addWidget(label)
        line_edit = QLineEdit()
        h_layout.addWidget(line_edit)

        # 添加文件选择器按钮
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(lambda: self.select_file(line_edit))
        h_layout.addWidget(browse_button)

        # 将布局添加到垂直布局中
        self.v_layout.addLayout(h_layout)

    def add_int_option(self, name, default_value):
        # 创建水平布局
        h_layout = QHBoxLayout()
        self.h_layouts[name] = h_layout

        # 添加标签和文本框
        label = QLabel(name)
        h_layout.addWidget(label)
        line_edit = QLineEdit(str(default_value))
        h_layout.addWidget(line_edit)

        # 将布局添加到垂直布局中
        self.v_layout.addLayout(h_layout)

    def add_button(self, name, callback):
        button = QPushButton(name)
        button.clicked.connect(callback)
        self.v_layout.addWidget(button)

    def select_file(self, line_edit):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a file")
        line_edit.setText(file_path)

    def start_training(self):
        # 获取所有选项的值
        options = {}
        for name, h_layout in self.h_layouts.items():
            line_edit = h_layout.itemAt(1).widget()
            options[name] = line_edit.text()

        # 构造命令字符串
        command = "python train.py"
        for name, value in options.items():
            if name in ["model", "data"]:
                command += f" {name.lower()}='{value}'"
            else:
                command += f" {name.lower()}={value}"

        # 调用 YOLOv8 训练命令
        print(command)
        # process = subprocess.Popen(command, shell=True)
        # process.communicate()