import datetime
import urllib.request,urllib,re
import time
from tkinter import *
import os
import copy

import MainUi
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread,pyqtSignal
import threading
from PyQt5.QtWidgets import QMessageBox
import os
import autotrade
from multiprocessing import Process,Queue
import parameter
import autotrade
import multiprocessing
import nest_asyncio



'''
 1  0: 未知
 2  1: 股票名字
 3  2: 股票代码
 4  3: 当前价格
 5  4: 昨收
 6  5: 今开
 7  6: 成交量（手）
 8  7: 外盘
 9  8: 内盘
10  9: 买一
11 10: 买一量（手）
12 11-18: 买二 买五
13 19: 卖一
14 20: 卖一量
15 21-28: 卖二 卖五
16 29: 最近逐笔成交
17 30: 时间
18 31: 涨跌
19 32: 涨跌%
20 33: 最高
21 34: 最低
22 35: 价格/成交量（手）/成交额
23 36: 成交量（手）
24 37: 成交额（万）
25 38: 换手率
26 39: 市盈率
27 40: 
28 41: 最高
29 42: 最低
30 43: 振幅
31 44: 流通市值
32 45: 总市值
33 46: 市净率
34 47: 涨停价
35 48: 跌停价
'''

global_para=[]
global_singnal=0
global_max_down_65_stock_code_list = []
global_button_signal=0
global_button_lock=0
global_button_voice=-1
global_start_down_signal=0
global_parameter=[7.0,3.5,4.5]




class Mywindown(QtWidgets.QMainWindow,MainUi.Ui_MainWindow):
    update_date = pyqtSignal(str)  # 自定义信号
    def __init__(self, parent=None):
        super(Mywindown, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.Show_data)
        self.pushButton.clicked.connect(self.voice_alarm)
        self.pushButton_4.clicked.connect(self.Autodeal)
        self.pushButton_5.clicked.connect(self.buy_stock)
        self.pushButton_6.clicked.connect(self.sell_stock)
        self.statusBar().showMessage('状态：软件运行正常')
        self.start_update.triggered.connect(self.down_load)
        self.set_parameter.triggered.connect(self.Setting_para)
        self.Is_buy_stock=None
        self.Is_buy_succeed=None
        self.able_to_buy_stock_coe=""


    def centerOnScreen(self):
        '''Centers the window on the screen.'''
        resolution = QtWidgets.QApplication.desktop().screenGeometry()
        x = (resolution.width() - self.frameSize().width()) / 2
        y = (resolution.height() - self.frameSize().height()) / 2
        self.move(x, y)

    def run(self,stock_code):
        r = r"^,\d*\.\d*"
        url = "http://qt.gtimg.cn/q="
        result=[]
        if (stock_code[0] == "6" or stock_code == "000001"):
            pass
            url = url + "sh" + stock_code
            web = urllib.request.urlopen(url).read()
            cc = web.decode("gbk")
            dd = re.findall(r, cc)
            day_list = []
            aa = []
            aa = cc.split('~')
            #         代码               现价         买一量         涨幅       最高价      最低价     昨收     今开盘价
            result = stock_code + "," + aa[3] + "," + aa[10] + "," + aa[32]+","+aa[33]+","+aa[34]+","+aa[4]+","+aa[5]
        elif (stock_code[0] == "0" or stock_code[0] == "3"):
            pass
            url = url + "sz" + stock_code
            web = urllib.request.urlopen(url).read()
            cc = web.decode("gbk")
            dd = re.findall(r, cc)
            day_list = []
            aa = []
            aa = cc.split('~')
            result = stock_code + "," + aa[3] + "," + aa[10] + "," + aa[32]+","+aa[33]+","+aa[34]+","+aa[4]+","+aa[5]

        return result


    def Create(self,para=3.5):
        pass
        global global_singnal
        global global_para
        global global_max_down_65_stock_code_list
        global global_button_signal
        global global_button_voice
        succeed_stock_code_list=[]
        global_button_signal=1
        order_num=0

        if global_singnal == 1:
            for i in range(len(global_para)):
                pass
                try:
                    pass
                    if float(global_para[i][3]) <3.5 :
                        i=i-1
                        continue
                    newItem = QtWidgets.QTableWidgetItem(global_para[i][0])
                    self.tableWidget.setItem(order_num, 0, newItem)  # 代码
                    newItem = QtWidgets.QTableWidgetItem(global_para[i][1])
                    self.tableWidget.setItem(order_num, 1, newItem)  # 现价
                    #print(self.tableWidget.item(0,1).text())

                    newItem = QtWidgets.QTableWidgetItem(global_para[i][2])
                    self.tableWidget.setItem(order_num, 2, newItem)  # 涨幅

                    if float(global_para[i][2]) >= 0:
                        self.tableWidget.item(order_num, 2).setBackground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
                    else:
                        self.tableWidget.item(order_num, 2).setBackground(QtGui.QBrush(QtGui.QColor(0, 255, 0)))

                    newItem = QtWidgets.QTableWidgetItem(global_para[i][3])
                    self.tableWidget.setItem(order_num, 3, newItem)  # 最大涨幅

                    newItem = QtWidgets.QTableWidgetItem(global_para[i][4])
                    self.tableWidget.setItem(order_num, 4, newItem)  # 最大跌幅

                    if float(global_para[i][3])>=3.5 and global_max_down_65_stock_code_list.count(global_para[i][0]) == 0:
                        global_max_down_65_stock_code_list.append(global_para[i][0])#去掉重复股票

                    if float(global_para[i][3]) >=3.5 :
                        self.newItem = QtWidgets.QTableWidgetItem(str("能"))
                        try:
                            self.new_autotrade.detect_time()
                            if self.new_autotrade.hourse >= 9 and self.new_autotrade.munite >= 25 or self.new_autotrade.hourse>=10 :  # 交易时间设定
                                buy_price = float(global_para[i][1]) + 0.05  # 溢价买入
                                buy_num = int(float(self.new_autotrade.able_captial) / buy_price/100)*100# 计算买入数量
                                while True:
                                    if not self.Is_buy_succeed:
                                        pass
                                        Is_buy_succeed=self.new_autotrade.buy_stock(global_para[i][0], str(buy_price), str(buy_num))
                                        time.sleep(5)
                                        self.new_autotrade.browser.close()
                                        Is_buy_succeed=True
                                        break
                                    
                        except:
                            pass
                        



                    else:
                        self.newItem = QtWidgets.QTableWidgetItem(str("否"))
                    self.tableWidget.setItem(order_num, 5, self.newItem)  # 能否买入

                    newItem = QtWidgets.QTableWidgetItem(global_para[i][5])
                    self.tableWidget.setItem(order_num, 6, newItem)  # 策略成功率
                    order_num+=1

                except:
                    pass
                    self.statusBar().showMessage('状态：软件运行错误')

            # 设置窗口弹出

            if len(global_max_down_65_stock_code_list)!=0 and global_button_voice==1:
                pass
                print("\a")
                #for i in global_max_down_65_stock_code_list:
                    #QMessageBox.information(self, '可买入提示', i, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        global_para=[]
        self.statusBar().showMessage('状态：软件运行正常')


    def Show_data(self):
        global global_button_lock#线程保护 自锁
        if global_button_lock==0:
            self.Create()
        global_button_lock=1

    def buy_stock(self):
        try:
            pass
            p2=threading.Thread(target=self.buy_stock_start,args=())
            p2.start()

        except:
            pass
    def buy_stock_start(self):
        while True:
            self.new_autotrade.detect_time()
            if self.new_autotrade.hourse==9 and   self.new_autotrade.munite>=25 :
                pass
                break
            if self.new_autotrade.hourse==10 :
                pass
                break
            if self.new_autotrade.hourse==11 and self.new_autotrade.munite<=30:
                pass
                break
            if self.new_autotrade.hourse==13 or self.new_autotrade.hourse==14:
                pass
                break
            self.statusBar().showMessage('状态：未到交易时间')
        while True:
            try:
                buy_price=float(lines[1])+0.05#溢价买入
                buy_num=int(float(self.new_autotrade.able_captial)/buy_price/100)*100#计算买入数量
                result=self.new_autotrade.buy_stock(self.able_to_buy_stock_coe,str(buy_price),str(buy_num))
                if result==1:
                    break
                else:
                    continue
            except:
                pass


    def sell_stock(self):
        pass
        try:
            pass
            p2=threading.Thread(target=self.sell_stock_start,args=())
            p2.start()
        except:
            pass
    def sell_stock_start(self,para1=1.0,para2=3.0):
        global global_parameter
        para1=global_parameter[1]
        para2=global_parameter[2]
        while True:
            self.new_autotrade.detect_time()
            if self.new_autotrade.hourse==9 and  self.new_autotrade.munite>=25 :
                pass
                break
            if self.new_autotrade.hourse==10 :
                pass
                break
            if self.new_autotrade.hourse==11 and self.new_autotrade.munite<=30:
                pass
                break
            if self.new_autotrade.hourse==13 or self.new_autotrade.hourse==14:
                pass
                break
            self.statusBar().showMessage('状态：未到交易时间')

        while True:
            try:
                self.new_autotrade.get_counter_detail()
                time.sleep(0.5)
                if self.new_autotrade.hold_stock_code==None:
                    break
                if float(self.new_autotrade.hold_stock_profit_percent)>=para1 or float(self.new_autotrade.hold_stock_profit_percent)<para2:
                    result=self.new_autotrade.sell_stock(str(self.new_autotrade.hold_stock_code),str(self.new_autotrade.hold_stock_now_price),\
                                                      str(self.new_autotrade.hold_stock_num))
                    if result:
                        break

            except:
                pass


    def open_jpg(self):
        os.system("succeed.text")
    def voice_alarm(self):
        global global_button_voice
        global_button_voice=-global_button_voice
        if global_button_voice==-1:
            pass
            self.pushButton.setText("声音预警开启")
        else:
            self.pushButton.setText("声音预警关闭")
    def down_load(self):
        self.statusBar().showMessage('状态：开始下载')
        self.update_date.emit(str(1))
    def Setting_para(self):
        self.new_pareGUI=ParaGui()
        self.new_pareGUI.Show()
    def Autodeal(self):
        p1=threading.Thread(target=self.start_,args=())
        p1.start()

    def start_(self):

        self.new_autotrade = autotrade.autotrade(0)
        yzm = str(input("请输入验证码："))
        self.new_autotrade.auto_login(yzm)
        self.new_autotrade.get_counter_detail()












class Update_data(QThread):
    update_date = pyqtSignal(str)  # 自定义信号
    def compute(self,stock_code):
        r = r"^,\d*\.\d*"
        url = "http://qt.gtimg.cn/q="
        result=[]
        if (stock_code[0] == "6" or stock_code == "000001"):
            pass
            url = url + "sh" + stock_code
            web = urllib.request.urlopen(url).read()
            cc = web.decode("gbk")
            dd = re.findall(r, cc)
            day_list = []
            aa = []
            aa = cc.split('~')
            #         代码               现价         买一量         涨幅       最高价      最低价     昨收       今开
            result = stock_code + "," + aa[3] + "," + aa[10] + "," + aa[32]+","+aa[33]+","+aa[34]+","+aa[4]+","+aa[5]
        elif (stock_code[0] == "0" or stock_code[0] == "3"):
            pass
            url = url + "sz" + stock_code
            web = urllib.request.urlopen(url).read()
            cc = web.decode("gbk")
            dd = re.findall(r, cc)
            day_list = []
            aa = []
            aa = cc.split('~')
            result = stock_code + "," + aa[3] + "," + aa[10] + "," + aa[32]+","+aa[33]+","+aa[34]+","+aa[4]+","+aa[5]

        return result
    def run(self,para=3.5):
        pwd = os.getcwd()  # 获取工作文件的当前目录
        pwd = pwd + '\\' + 'rsult' + '\\' + 'boll.dat'
        f1 = open(pwd, "r")
        lines = f1.read()  # 获取所有的股票代码
        f1.close()
        self.ls_stock_code = []
        self.ls_stock_code = lines.split(",")

        percent=0
        global global_button_signal
        while True:
            pass
            global global_para#数据
            global global_singnal
            global global_parameter#参数
            para=global_parameter[0]
            if global_button_signal==1:
                pass
                n = 0  # 实际可以获取股票的个数
                for stock_code in self.ls_stock_code:
                    pass
                    ls_list = []
                    try:
                        pass
                        ls_1 = self.compute(stock_code[0:6])
                        ls_2 = copy.deepcopy(ls_1)
                        ls_2 = ls_2.split(",")
                        ls_3 = stock_code.split("!")#result中的数据读取
                        percent = copy.deepcopy(float(ls_2[3]))
                        compute_2 = (float(ls_2[5]) - float(ls_2[6])) / float(ls_2[6]) * 100
                        compute_2 = round(compute_2, 2)  # 最大跌幅
                        compute_4=(float(ls_2[7]) - float(ls_2[6])) / float(ls_3[2]) * 100
                        compute_4 = round(compute_4, 2)  # 楼氏开盘涨幅

                        if (1):
                            pass
                            compute_1 = (float(ls_2[4]) - float(ls_2[6])) / float(ls_2[6]) * 100
                            compute_1 = round(compute_1, 2)  # 最大涨幅
                            compute_2 = (float(ls_2[5]) - float(ls_2[6])) / float(ls_2[6]) * 100
                            compute_2 = round(compute_2, 2)  # 最大跌幅
                            compute_3=(float(ls_2[7]) - float(ls_2[6])) / float(ls_2[6]) * 100
                            compute_3=round(compute_3,2)#开盘涨幅
                            #数据列表
                            ls_list.append(stock_code[0:6])  # 0 代码
                            ls_list.append(ls_2[1])  # 1 #现价
                            ls_list.append(ls_2[3])  # 2#涨幅
                            ls_list.append(str(compute_1))  # 3#最大涨幅
                            ls_list.append(str(compute_2))  # 4#最大跌幅
                            ls_list.append(ls_3[1][0:4])  # 5 成功率
                            ls_list.append(str(compute_3))#6 开盘涨幅
                            ls_list.append(str(compute_4))  # 7 楼氏开盘涨幅

                        n += 1

                    except:
                        pass

                    if len(ls_list) != 0:
                        pass
                        global_para.append(ls_list)

                if len(global_para) == n :
                    global_singnal = 1
                    self.update_date.emit(str(1))
                else:
                    global_singnal = 0



class Update_data_multp_cpu(object):
    def __init__(self):
        pass
        # 判断是否需要刷新数据
        ls_pwd = os.getcwd()  # 获取工作文件的当前目录
        ls_pwd = ls_pwd + "\\" + "rsult"  # 获取工作文件的当前目录
        ls_pwd = ls_pwd + '\\' + 'boll_new_data' + ".dat"  # 完整的路径
        try:
            os.remove(ls_pwd)
        except:
            pass
    def detect_time(self):
        try:
            pass
            today_time = time.localtime()
            self.hourse=today_time[3]
            self.munite=today_time[4]
            self.second=today_time[5]
            self.week=today_time[6]
        except:
            pass


    def Auto_deal(self):
        pass
    def compute(self,stock_code):
        r = r"^,\d*\.\d*"
        url = "http://qt.gtimg.cn/q="
        result=[]
        if (stock_code[0] == "6" or stock_code == "000001"):
            pass
            url = url + "sh" + stock_code
            web = urllib.request.urlopen(url).read()
            cc = web.decode("gbk")
            dd = re.findall(r, cc)
            day_list = []
            aa = []
            aa = cc.split('~')
            #         代码               现价         买一量         涨幅       最高价      最低价     昨收      今开
            result = stock_code + "," + aa[3] + "," + aa[10] + "," + aa[32]+","+aa[33]+","+aa[34]+","+aa[4]+","+aa[5]
        elif (stock_code[0] == "0" or stock_code[0] == "3"):
            pass
            url = url + "sz" + stock_code
            web = urllib.request.urlopen(url).read()
            cc = web.decode("gbk")
            dd = re.findall(r, cc)
            day_list = []
            aa = []
            aa = cc.split('~')
            result = stock_code + "," + aa[3] + "," + aa[10] + "," + aa[32]+","+aa[33]+","+aa[34]+","+aa[4]+","+aa[5]

        return result
    def start(self,para=-6.5):
        pwd = os.getcwd()  # 获取工作文件的当前目录
        pwd = pwd + '\\' + 'rsult' + '\\' + 'boll.dat'
        f1 = open(pwd, "r")
        lines = f1.read()  # 获取所有的股票代码
        f1.close()
        self.ls_stock_code = []
        self.ls_stock_code = lines.split(",")
        percent=0
        stock_code_list = []
        divid_num=len(self.ls_stock_code)/os.cpu_count()
        divid_num = int(len(self.ls_stock_code) / 4)
        stock_code_list_1=self.ls_stock_code[0:divid_num]
        stock_code_list_2=self.ls_stock_code[divid_num:2*divid_num]
        stock_code_list_3 = self.ls_stock_code[2*divid_num:3 * divid_num]
        stock_code_list_4 = self.ls_stock_code[3 * divid_num:len(self.ls_stock_code)]
        stock_code_list.append(stock_code_list_1)
        stock_code_list.append(stock_code_list_2)
        stock_code_list.append(stock_code_list_3)
        stock_code_list.append(stock_code_list_4)
        con1 = Queue()
        con1_sinal_l=Queue()
        con2 = Queue()
        con1_sinal_2 = Queue()
        con3 = Queue()
        con1_sinal_3 = Queue()
        con4 = Queue()
        con1_sinal_4 = Queue()
        con=[]
        con.append(con1)
        con.append(con2)
        con.append(con3)
        con.append(con4)
        con_sinal=[]
        con_sinal.append(con1_sinal_l)
        con_sinal.append(con1_sinal_2)
        con_sinal.append(con1_sinal_3)
        con_sinal.append(con1_sinal_4)
        #判断是否需要刷新数据
        ls_pwd = os.getcwd()  # 获取工作文件的当前目录
        ls_pwd = ls_pwd + "\\" + "rsult"  # 获取工作文件的当前目录
        ls_pwd = ls_pwd + '\\' + 'boll_new_data' + ".dat"  # 完整的路径
        ls_start_signal=1
        try:
            with open(ls_pwd, "r") as f:
                pass
                ls_start_signal=0
        except:
            pass
            ls_start_signal=1
        p_list=[]
        while True:
            self.detect_time()
            if self.hourse==9 and   self.munite>=25 :
                pass
                break
            if self.hourse==10:
                pass
                break
            if self.hourse==11 and self.munite<=30:
                pass
                break
            if self.hourse==13 or self.hourse==14:
                pass
                break
            if 1:
                break
        while ls_start_signal:
            pass
            p_list = []

            for x in range(4):
                p = Process(target=self.run, args=(con[x], con_sinal[x], stock_code_list[x], -6.5,))
                p.start()
                p_list.append(p)
            while True:
                value1 = con[0].get()
                value2 = con[1].get()
                value3 = con[2].get()
                value4 = con[3].get()
                value1_sinal = con_sinal[0].get()
                value2_sina2 = con_sinal[1].get()
                value3_sina3 = con_sinal[2].get()
                value4_sina4 = con_sinal[3].get()

                if value1_sinal == "ok" and value4_sina4 == "ok" and value2_sina2 == "ok" and value3_sina3 == "ok":
                    #print(value1)
                    break
            if value1_sinal == "ok" and value4_sina4 == "ok" and value2_sina2 == "ok" and value3_sina3 == "ok":
                try:
                    ls_pwd = os.getcwd()  # 获取工作文件的当前目录
                    ls_pwd = ls_pwd + "\\" + "rsult"  # 获取工作文件的当前目录
                    ls_pwd = ls_pwd + '\\' + 'boll_new_data' + ".dat"  # 完整的路径
                    file = open(ls_pwd, "w+")
                    all_write_list=[]
                    ls_str=""
                    try:
                        pass
                        for i in value1:
                            pass
                            ls_str = ""
                            for k in i:
                                ls_str=ls_str+str(k)+","
                            file.write(ls_str)
                            file.write(str("\n"))
                        for i in value2:
                            pass
                            ls_str = ""
                            for k in i:
                                ls_str=ls_str+str(k)+","
                            file.write(ls_str)
                            file.write(str("\n"))
                        for i in value3:
                            pass
                            ls_str = ""
                            for k in i:
                                ls_str=ls_str+str(k)+","
                            file.write(ls_str)
                            file.write(str("\n"))
                        for i in value4:
                            pass
                            ls_str = ""
                            for k in i:
                                ls_str=ls_str+str(k)+","
                            file.write(ls_str)
                            file.write(str("\n"))

                    except:
                        pass

                    file.close()
                    size = os.path.getsize(ls_pwd)
                    if size == 0:
                        continue
                    else:
                        break

                    break

                except:
                    pass
            for p in p_list:

                p.close()
    def run(self,con,con_sinal,stock_code_list=[],para=2.5):
        global global_button_signal
        global global_multpro_parameter
        ls_list=[]
        for i in stock_code_list:
            try:
                ls_1 = self.compute(i[0:6])
                ls_2 = copy.deepcopy(ls_1)
                ls_2 = ls_2.split(",")
                ls_3 = i.split("!")  # result中的数据读取,并分解
                result=self.compute(i[0:6])
                result=result.split(",")
                compute_1 = (float(ls_2[4]) - float(ls_2[6])) / float(ls_2[6]) * 100
                compute_1 = round(compute_1, 2)  # 最大涨幅
                compute_2 = (float(ls_2[5]) - float(ls_2[6])) / float(ls_2[6]) * 100
                compute_2 = round(compute_2, 2)  # 最大跌幅
                compute_3 = (float(result[7]) - float(result[6])) / float(result[6]) * 100
                compute_3 = round(compute_3, 2)  # 开盘涨幅
                compute_4 = (float(result[7]) - float(result[6])) / float(ls_3[2]) * 100
                compute_4 = round(compute_4, 2)  # 楼氏开盘涨幅
                if compute_4>=1.25 and  float(result[3])>=3.5 and compute_1<=9.86:
                    ls_list.append(result)
            except:
                pass
        con.put(ls_list)
        con_sinal.put("ok")





class ParaGui(QtWidgets.QMainWindow,parameter.Ui_Dialog):
    def __init__(self):
        super(ParaGui, self).__init__()
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.setpara_1)
        self.pushButton_4.clicked.connect(self.setpara_2)
        self.pushButton_5.clicked.connect(self.setpara_3)
        self.pushButton.clicked.connect(self.Quit)
        self.pushButton_2.clicked.connect(self.Quit)

    def Show(self):
        self.show()
    def setpara_1(self):#涨跌幅设置
        global global_parameter
        try:
            global_parameter[0]=float(self.lineEdit.text())
            self.statusBar().showMessage('状态：设置成功')
        except:
            pass
    def setpara_2(self):#止盈
        global global_parameter
        try:
            global_parameter[1]=float(self.lineEdit_2.text())
            self.statusBar().showMessage('状态：设置成功')
        except:
            pass
    def setpara_3(self):#止损
        global global_parameter
        try:
            global_parameter[2]=float(self.lineEdit_3.text())
            self.statusBar().showMessage('状态：设置成功')
        except:
            pass
    def Quit(self):
        self.close()


def Auto_deal():
    new_autotrade = autotrade.autotrade(0)
    yzm = str(input("请输入验证码："))
    new_autotrade.auto_login(yzm)
    new_autotrade.get_counter_detail()












if __name__ == '__main__':
    app = QtWidgets.QApplication.instance()  # checks if QApplication already exists
    if not app:  # create QApplication if it doesnt exist
        app = QtWidgets.QApplication(sys.argv)
    #启动界面
    #--------------------
    win = Mywindown()#主窗口
    new_123=Update_data()#多线程数据更新
    new_123.update_date.connect(win.Create)
    new_123.start()

    #multiprocessing.freeze_support()#
    #new_456 = Update_data_multp_cpu()  # 多进程数据更新
    #p1 = Process(target=new_456.start, args=(1.25,))
    #p1.start()



    win.centerOnScreen()
    win.show()
    app.exec_()



