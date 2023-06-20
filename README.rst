
YOLOv8-based-Intelligent-Object-Detection-and-Annotation-System
========

.. image:: https://img.shields.io/pypi/v/labelimg.svg
        :target: https://pypi.python.org/pypi/labelimg

.. image:: https://img.shields.io/travis/tzutalin/labelImg.svg
        :target: https://travis-ci.org/tzutalin/labelImg


The project is based on YOLOv8 and features automatic annotation, dataset splitting, and conversion functions. Users can easily convert COCO datasets to VOC or YOLO format with just one click, as well as perform model inference and training. Additionally, the system provides annotation and modification capabilities for both VOC and YOLO formatted datasets.
by `ImageNet <http://www.image-net.org/>`__.  Besides, it also supports YOLO and CreateML formats.

.. image:: https://github.com/peterpan1998/YOLOv8-based-Intelligent-Object-Detection-and-Annotation-System/blob/master/demo/demo3.jpg
     :alt: Demo Image

.. image:: https://github.com/peterpan1998/YOLOv8-based-Intelligent-Object-Detection-and-Annotation-System/blob/master/demo/demo4.jpg
     :alt: Demo Image

`Watch a demo video <https://youtu.be/p0nR2YsCY_U>`__

Installation
------------------

Get from PyPI but only python3.0 or above
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Before using this software, please ensure that you have installed the Python SDK. Whether you have directly installed the Python SDK or are using tools like Anaconda, please activate the corresponding environment before proceeding with the following steps.

.. code:: shell

    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
    pip3 install ultralytics
    pip3 install lxml -i https://pypi.tuna.tsinghua.edu.cn/simple
    pip3 install PyQt5 -i https://pypi.tuna.tsinghua.edu.cn/simple
    pip3 install PyQt5_tools -i https://pypi.tuna.tsinghua.edu.cn/simple
    pip3 install pycocotools
    pip3 install labelImg
    


Build from source
~~~~~~~~~~~~~~~~~
Please make sure that all the above-mentioned packages are installed before proceeding. Next, you can start the software. As the required environment includes dependencies such as PyTorch, packaging the software would result in a large file size. Therefore, we have decided to open-source the code and provide instructions for running the software directly.

Note: The code provided is written for the Windows environment, and theoretically should work as described in the above process. If you are running it on Linux, it should also work, but there might be some bugs that you may need to modify yourself.

Usage
-----


Steps (Auto label)
~~~~~~~~~~~~~~~~~

1. Click 'v8-detect' 
2. Click 'v8 auto label'




.. image:: https://github.com/peterpan1998/YOLOv8-based-Intelligent-Object-Detection-and-Annotation-System/blob/master/demo/v8-annotations.png


Note: 
        "select weight file"  is the option to choose the corresponding inference weight file.
        "select img    path"  is the folder where you store the images to be automatically annotated, 
        "select xml    path"  is the folder where the automatically generated XML files will be saved.
        
After selecting all the mentioned files, you can click the "START DETECTION" button to initiate the automatic annotation process.

After the automatic annotation is completed, you can return to the main interface to perform the following two operations and review the results of the automatic annotation:
By reviewing and modifying the annotations, you can ensure that they meet your specific requirements and achieve the desired level of accuracy.

1. Click 'Open Dir'
2. Click 'Change save dir'

"Open Dir" is the option to select the folder containing the images you want to annotate.
"Change Save Dir" is the folder where XML files are saved.



Steps (Auto Train)
~~~~~~~~~~~~~~~~~
It is recommended to organize the folder structure as follows:

.. code:: shell

        |--./data
        |  |--./data/Annotations
        |  |   |--./data/Annotations/001.xml
        |  |   |--./data/Annotations/002.xml
        |  |   |--...
        |  |--./data/images
        |  |   |--./data/images/001.jpg
        |  |   |--./data/images/002.jpg
        |  |   |--...


Please ensure that your dataset is prepared before proceeding with the training. Here are the two basic steps to prepare the dataset:

1. Click 'Open Dir'
2. Click 'Change save dir'






todo。。。。。。。。。。。。。。。。。。。

Steps (PascalVOC)
~~~~~~~~~~~~~~~~~

1. Build and launch using the instructions above.
2. Click 'Change default saved annotation folder' in Menu/File
3. Click 'Open Dir'
4. Click 'Create RectBox'
5. Click and release left mouse to select a region to annotate the rect
   box
6. You can use right mouse to drag the rect box to copy or move it

The annotation will be saved to the folder you specify.

You can refer to the below hotkeys to speed up your workflow.

Steps (YOLO)
~~~~~~~~~~~~

1. In ``data/predefined_classes.txt`` define the list of classes that will be used for your training.

2. Build and launch using the instructions above.

3. Right below "Save" button in the toolbar, click "PascalVOC" button to switch to YOLO format.

4. You may use Open/OpenDIR to process single or multiple images. When finished with a single image, click save.

A txt file of YOLO format will be saved in the same folder as your image with same name. A file named "classes.txt" is saved to that folder too. "classes.txt" defines the list of class names that your YOLO label refers to.

Note:

- Your label list shall not change in the middle of processing a list of images. When you save an image, classes.txt will also get updated, while previous annotations will not be updated.

- You shouldn't use "default class" function when saving to YOLO format, it will not be referred.

- When saving as YOLO format, "difficult" flag is discarded.

Create pre-defined classes
~~~~~~~~~~~~~~~~~~~~~~~~~~

You can edit the
`data/predefined\_classes.txt <https://github.com/tzutalin/labelImg/blob/master/data/predefined_classes.txt>`__
to load pre-defined classes

Annotation visualization
~~~~~~~~~~~~~~~~~~~~~~~~

1. Copy the existing lables file to same folder with the images. The labels file name must be same with image file name.

2. Click File and choose 'Open Dir' then Open the image folder.

3. Select image in File List, it will appear the bounding box and label for all objects in that image.

(Choose Display Labels mode in View to show/hide lablels)


Hotkeys
~~~~~~~

+--------------------+--------------------------------------------+
| Ctrl + u           | Load all of the images from a directory    |
+--------------------+--------------------------------------------+
| Ctrl + r           | Change the default annotation target dir   |
+--------------------+--------------------------------------------+
| Ctrl + s           | Save                                       |
+--------------------+--------------------------------------------+
| Ctrl + d           | Copy the current label and rect box        |
+--------------------+--------------------------------------------+
| Ctrl + Shift + d   | Delete the current image                   |
+--------------------+--------------------------------------------+
| Space              | Flag the current image as verified         |
+--------------------+--------------------------------------------+
| w                  | Create a rect box                          |
+--------------------+--------------------------------------------+
| d                  | Next image                                 |
+--------------------+--------------------------------------------+
| a                  | Previous image                             |
+--------------------+--------------------------------------------+
| del                | Delete the selected rect box               |
+--------------------+--------------------------------------------+
| Ctrl++             | Zoom in                                    |
+--------------------+--------------------------------------------+
| Ctrl--             | Zoom out                                   |
+--------------------+--------------------------------------------+
| ↑→↓←               | Keyboard arrows to move selected rect box  |
+--------------------+--------------------------------------------+

**Verify Image:**

When pressing space, the user can flag the image as verified, a green background will appear.
This is used when creating a dataset automatically, the user can then through all the pictures and flag them instead of annotate them.

**Difficult:**

The difficult field is set to 1 indicates that the object has been annotated as "difficult", for example, an object which is clearly visible but difficult to recognize without substantial use of context.
According to your deep neural network implementation, you can include or exclude difficult objects during training.

How to reset the settings
~~~~~~~~~~~~~~~~~~~~~~~~~

In case there are issues with loading the classes, you can either:

1. From the top menu of the labelimg click on Menu/File/Reset All
2. Remove the `.labelImgSettings.pkl` from your home directory. In Linux and Mac you can do:
    `rm ~/.labelImgSettings.pkl`


How to contribute
~~~~~~~~~~~~~~~~~

Send a pull request

License
~~~~~~~
`Free software: MIT license <https://github.com/tzutalin/labelImg/blob/master/LICENSE>`_

Citation: Tzutalin. LabelImg. Git code (2015). https://github.com/tzutalin/labelImg

Related and additional tools
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. `ImageNet Utils <https://github.com/tzutalin/ImageNet_Utils>`__ to
   download image, create a label text for machine learning, etc
2. `Use Docker to run labelImg <https://hub.docker.com/r/tzutalin/py2qt4>`__
3. `Generating the PASCAL VOC TFRecord files <https://github.com/tensorflow/models/blob/4f32535fe7040bb1e429ad0e3c948a492a89482d/research/object_detection/g3doc/preparing_inputs.md#generating-the-pascal-voc-tfrecord-files>`__
4. `App Icon based on Icon by Nick Roach (GPL) <https://www.elegantthemes.com/>`__
5. `Setup python development in vscode <https://tzutalin.blogspot.com/2019/04/set-up-visual-studio-code-for-python-in.html>`__
6. `The link of this project on iHub platform <https://code.ihub.org.cn/projects/260/repository/labelImg>`__
7. `Convert annotation files to CSV format or format for Google Cloud AutoML <https://github.com/tzutalin/labelImg/tree/master/tools>`__



Stargazers over time
~~~~~~~~~~~~~~~~~~~~

.. image:: https://starchart.cc/tzutalin/labelImg.svg

