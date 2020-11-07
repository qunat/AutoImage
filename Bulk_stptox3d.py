# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 08:29:23 2020

@author: Administrator
"""
from urllib import request

from OCC.Display.WebGl import x3dom_renderer
from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.BRepTools import breptools_Read
from OCC.Extend.DataExchange import read_step_file


from OCC.Display.SimpleGui import init_display
from OCC.Core.TopoDS import topods_Edge
from OCC.Extend.DataExchange import read_step_file
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Display.OCCViewer import rgb_color
from OCC.Core.AIS import AIS_ColoredShape
from random import random
from OCC.Core.AIS import AIS_Shape
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.Quantity import Quantity_Color
from OCC.Core.Quantity import Quantity_Color,Quantity_TOC_RGB
from OCC.Display.SimpleGui import init_display
from OCC.Display.OCCViewer import Viewer3d
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
import os
import socket
import webbrowser
import errno
from flask import Flask, redirect, url_for, request,send_from_directory
from flask import Flask, render_template
import sys

#display, start_display, add_menu, add_function_to_menu = init_display()
#context = display.Context


class Bulk_stptox3d(object):
    def __init__(self,path="."):
        path=os.getcwd()
        self.file_list=os.listdir(path)#返回指定目录下的所有文件和目录名
       
        
    def Exchange_stp_3xd(self):
        try:
            for file in self.file_list:
                if "stp" in file or "step" in file or "iges" in file :
                    try:
                        the_shape = read_step_file(file)
                        my_renderer = x3dom_renderer.X3DomRenderer("./")
                        name=file.split(".")
                        my_renderer.DisplayShape(the_shape,export_edges=True,color=(random(), random(), random()),file_name=name[0])
                        
                        #if file=="iseg":
                            #pass
                        #else:
                            #the_shape = read_step_file(file)
                            #ais_shape=AIS_ColoredShape(the_shape)
                            #for e in TopologyExplorer(the_shape).shells():
                                #rnd_color = (random(), random(), random())
                                #ais_shape.SetCustomColor(e, rgb_color(random(), random(), random()))
                                #display.EraseAll()
                                #context.Display(ais_shape,True)
                                #display.FitAll()
                                #path='./'+name[0]+".bmp"
                                #display.View.Dump(path)
                            
                    except:
                        pass             
        except:
            pass
   
        
        
if __name__ == '__main__':
    pass
    
    new_Bulk_stptox3d=Bulk_stptox3d()
    new_Bulk_stptox3d.Exchange_stp_3xd()
    sys.exit()
    #new_Bulk_stptox3d.Exchange_stp_img()
   