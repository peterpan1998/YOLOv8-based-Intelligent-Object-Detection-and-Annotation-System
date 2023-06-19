import os
import glob
from xml.etree import ElementTree as ET
from ultralytics import YOLO  # YOLOV8
# from libs.SonWindow import *
# 定义一个创建一级分支object的函数
def create_object(root, xyxy, names,cls):  # 参数依次，树根，xmin，ymin，xmax，ymax
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
def create_tree(image_path, h, w):
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


def pretty_xml(element, indent, newline, level=0):  # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
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
        pretty_xml(subelement, indent, newline, level=level + 1)  # 对子元素进行递归操作

# child = Child()
def Auto_label(weight,imgdir,xmldir):
    # load model
    model = YOLO(weight)
    img_list = glob.glob('%s/*.*' % imgdir)
    num = 0
    # child = Child()
    # con_text = child.edit4

    for img_path in img_list:
            print(img_path)
            results = model(img_path,show=False,save=False)[0]  # predict on an image
            # 创建xml文件
            annotation = create_tree(img_path, results.orig_shape[0], results.orig_shape[1])
            det = results.boxes
            names = results.names

            cls = det.cls
            for i in range(len(det)):
                create_object(annotation,det.xyxy[i],names,cls[i])
            # 将树模型写入xml文件
            tree = ET.ElementTree(annotation)
            root = tree.getroot()
            pretty_xml(root, '\t', '\n')
            # tree.write('.\{}\{}.xml'.format(outdir, image_name.strip('.jpg')), encoding='utf-8')
            tree.write(img_path.replace(imgdir,xmldir).replace('.jpg','.xml'), encoding='utf-8')
            num += 1
            # con_text.setText(img_path," : 检测完成！")
            if num>=len(img_list):
                print("检测完成！")
                # con_text.setText(child.imgdir," : 下所有图片已检测完成！")
