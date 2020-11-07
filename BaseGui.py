# -*- coding: utf-8 -*-
#!/usr/bin/env python

import logging
import os
import sys
import time

from OCC.Core.BRepTools import breptools_Write

from OCC.Display.OCCViewer import OffscreenRenderer
from OCC.Display.backend import load_backend, get_qt_modules
from PyQt5.QtWidgets import QHBoxLayout, QDockWidget, \
    QListWidget, QFileDialog
#from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtWidgets ,Qt

from graphics import GraphicsView, GraphicsPixmapItem
from OCC.Core.AIS import AIS_ColoredShape
from random import random
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Display.OCCViewer import rgb_color
from QSS import *
import threading
import multiprocessing
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from multiprocessing import Process,Queue
import xlsxwriter
from PIL import Image
import openpyxl






#------------------------------------------------------------开始初始化环境
log = logging.getLogger(__name__)
def check_callable(_callable):
    if not callable(_callable):
        raise AssertionError("The function supplied is not callable")
backend_str=None
size=[850, 873]
display_triedron=True
background_gradient_color1=[212, 212, 212]
background_gradient_color2=[128, 128, 128]
if os.getenv("PYTHONOCC_OFFSCREEN_RENDERER") == "1":
    # create the offscreen renderer
    offscreen_renderer = OffscreenRenderer()
    def do_nothing(*kargs, **kwargs):
        """ takes as many parameters as you want,
        ans does nothing
        """
        pass
    def call_function(s, func):
        """ A function that calls another function.
        Helpfull to bypass add_function_to_menu. s should be a string
        """
        check_callable(func)
        log.info("Execute %s :: %s menu fonction" % (s, func.__name__))
        func()
        log.info("done")

    # returns empty classes and functions
used_backend = load_backend(backend_str)
log.info("GUI backend set to: %s", used_backend)
#------------------------------------------------------------初始化结束
from OCC.Display.qtDisplay import qtViewer3d
import MainGui
from PyQt5.QtGui import QPixmap
QtCore, QtGui, QtWidgets, QtOpenGL = get_qt_modules()
from OCC.Extend.DataExchange import read_step_file,write_step_file
from OCC.Core.TopoDS import TopoDS_Shape,TopoDS_Builder,TopoDS_Compound,topods_CompSolid
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism, BRepPrimAPI_MakeRevol
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Ax1, gp_Dir
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCC.Core.BRepGProp import brepgprop_LinearProperties
from OCC.Core.GProp import GProp_GProps
from OCC.Core.TopoDS import topods_Edge,topods_Solid
from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepTools import breptools_Read,breptools_Write
from OCC.Extend.DataExchange import read_iges_file,read_step_file,read_stl_file
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh


class Mywindown(QtWidgets.QMainWindow,MainGui.Ui_MainWindow):
    pass
    def __init__(self, parent=None):
        super(Mywindown,self).__init__(parent)
        self.setupUi(self)
        #3D显示设置
        self.canva = qtViewer3d(self.tab)#链接3D模块
        self.setWindowTitle("【批量导出stp缩略图程序】")
        #self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.setFixedSize(self.width(), self.height());
        self.canva.setGeometry(QtCore.QRect(0, 0, 420, 530))
        self.canva.focusInEvent(self.event)
        self.centerOnScreen()

        #单个产品 信号和槽
        self.pushButton_2.clicked.connect(self.Quit)#退出
        self.pushButton_3.clicked.connect(self.Chose_Document)#选择文件夹
        self.pushButton_4.clicked.connect(self.Bulk_stptoimag)# 批量导出图片


        #Qss定义
        self.pushButton_2.setStyleSheet(butstyle)
        self.pushButton_3.setStyleSheet(butstyle)
        self.pushButton_4.setStyleSheet(butstyle)
        self.pushButton_5.setStyleSheet(butstyle)


    def Chose_Document(self):
        pass
        self.statusbar.showMessage("状态：开始导入......")
        self.chose_document = QFileDialog.getExistingDirectory(self,"选择文件夹","./")#选择转换的问价夹
        print(self.chose_document)
        #self.the_shape = read_step_file(openfile_name[0])
        #self.canva._display.DisplayShape(self.the_shape)
        #self.canva._display.FitAll()
        self.statusbar.showMessage("状态：打开成功")###
        #---------------------------------------------------------------------------------

    def Bulk_stptoimag(self):
        pass
        self.file_list = os.listdir(self.chose_document)
        print(self.file_list)
        for file in self.file_list:
            self.canva._display.EraseAll()
            self.canva._display.hide_triedron()
            self.canva._display.display_triedron()
            if "stp" in file or "step" in file or "iges" in file:
                try:
                    if file=="iseg":
                        continue
                    else:
                        read_path=os.path.join(self.chose_document,file)
                        the_shape = read_step_file(read_path)
                        name = file.split(".")
                        ais_shape=AIS_ColoredShape(the_shape)
                        for e in TopologyExplorer(the_shape).solids():
                            rnd_color = (random(), random(), random())
                            ais_shape.SetCustomColor(e, rgb_color(0.5, 0.5, 0.5))

                        self.canva._display.Context.Display(ais_shape, True)
                        self.canva._display.FitAll()
                        path = self.chose_document+"\\"+name[0] + ".bmp"
                        self.canva._display.ExportToImage(path)

                except:
                    pass

            self.statusbar.showMessage("状态：表格生成成功")




    def Quit(self):
        self.close()

    def centerOnScreen(self):
        '''Centers the window on the screen.'''
        resolution = QtWidgets.QApplication.desktop().screenGeometry()
        x = (resolution.width() - self.frameSize().width()) / 2
        y = (resolution.height() - self.frameSize().height()) / 2
        self.move(x, y)



def line_clicked(shp, *kwargs):
        """ This function is called whenever a line is selected
        """
        try:
            pass
            for shape in shp:  # this should be a TopoDS_Edge
                print("Edge selected: ", shape)
                e = topods_Edge(shape)

                props = GProp_GProps()
                brepgprop_LinearProperties(e, props)

                length = props.Mass()
                print("此边的长度为: %f" % length)
                centerMass = props.CentreOfMass()
                print("此边的中心点为", centerMass.X(), centerMass.Y(), centerMass.Z())
        except:
            pass

# following couple of lines is a tweak to enable ipython --gui='qt'
if __name__ == '__main__':
    app = QtWidgets.QApplication.instance()  # checks if QApplication already exists
    if not app:  # create QApplication if it doesnt exist
        app = QtWidgets.QApplication(sys.argv)
    #启动界面

    #--------------------
    win = Mywindown()
    win.show()
    win.centerOnScreen()
    win.canva.InitDriver()
    win.resize(size[0], size[1])
    win.canva.qApp = app

    display = win.canva._display
    display.display_triedron()
    display.register_select_callback(line_clicked)
    if background_gradient_color1 and background_gradient_color2:
    # background gradient
        display.set_bg_gradient_color(background_gradient_color1, background_gradient_color2)
    win.raise_()  # make the application float to the top
    app.exec_()