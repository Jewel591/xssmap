# coding=utf-8
import re
import sys
import threading
import time
import urllib.parse
from PyQt5.QtWidgets import QApplication, QMainWindow

import url_data
import human_read
from check_prepare import CheckPrepare
from ui.start import Ui_MainWindow
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
import payload
import mymodule



time_start = time_end = ""


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        # 执行函数
        # 如果不加 self，tt 只是一个局部变量，当初始化完成，该变量的生命周期就结束了，所以会报 QThread: Destroyed
        # while thread is still running
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
        # print(cursor)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.output.setTextCursor(cursor)
        self.output.ensureCursorVisible()


class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))


class Worker(QThread):
    def __init__(self):
        super(Worker, self).__init__()

    def run(self):
        global time_start, time_end
        time_start = time.time()
        # if not len(myWin.input_url.text()):
        #         #     print("请输入目标 URL...")
        #         #     return # 退出逻辑线程
        #         # if not len(myWin.input_arg.text()):
        #         #     print("请输出注入参数...")
        #         #     return
        print("开始分析...".center(160), "\n")
        payload.keyword_init()
        human_read.allclear()  # 输入2
        url_data.word = myWin.input_arg.text().strip()
        url_data.targeturl = myWin.input_url.text()
        if url_data.targeturl=="":
            url_data.targeturl = "http://www.shmsa.gov.cn/searchxxgk.jspx(POST)release=atestu&startDate=2018-11-23&title=atestu&endDate=2018-11-23&contentno=\"%20onclick=zpiqoy`6634`%20var=%20"
        print("Target URL".center(160), "\n", url_data.targeturl)
        human_read.Dividing_line()
        begin = CheckPrepare()
        begin.rebuild()
        begin2 = CheckStart()
        begin2.check_close()
        begin2.check_action()
        begin2.check_onevent()
        begin2.check_tag()
        begin2.check_others()
        begin2.check_illusion()
        human_read.Dividing_line()
        time_end = time.time()
        print("测试耗时：", time_end - time_start)


class CheckStart():

    def check_close(self):
        print("正在进行闭合测试".center(160))
        while url_data.HTTP_METHON == "GET":
            CheckPrepare.isurlok(self, url_data.get_url)
            if url_data.urlok == "no":
                return
            # if re.search(re.escape("\"'>"),Check_Prepare.get_response(re.sub(re.escape("abcdef1234"), "\"'>", url_data.get_url))):
            #     payload.keyword_expand("\"'>")
            # payload.keyword.sort(key=lambda x:len(x))

            def get_start(pd):
                if re.search(
                    re.escape(
                        urllib.parse.unquote(
                            urllib.parse.unquote(pd))),
                        CheckPrepare.get_response(
                            self,
                            re.sub(
                        re.escape("abcdef1234"),
                        pd,
                                url_data.get_url))):  # 使用 re.escape()
                    # print("^^^".center(160))
                    # print(pd.center(160))
                    # print("GET测试：", re.sub(re.escape("abcdef1234"), pd, url_data.get_url))
                    # human_read.Dividing_line()
                    url_data.unsensitive['close'].append(pd)
                else:
                    url_data.sensitive['close'].append(pd)
            for i in payload.keyword['close']:
                mythread = threading.Thread(target=get_start(i))
                mythread.start()

            if re.search(
                r"/|%2f",
                mymodule.list_to_str(
                    url_data.unsensitive['close'])):
                for i in payload.keyword['close_tag']:
                    if re.search(
                            re.escape(
                                urllib.parse.unquote(
                                    urllib.parse.unquote(i))),
                            CheckPrepare.get_response(
                                self,
                                re.sub(
                                    re.escape("abcdef1234"),
                                    i,
                                    url_data.get_url))):

                        url_data.unsensitive['close_tag'].append(i)
                    else:
                        url_data.sensitive['close_tag'].append(i)

            [print("未过滤：", e.replace("591", "")) for e in url_data.unsensitive['close']]
            # 将未过滤的闭合字符整体输出
            str591=""
            for e in url_data.unsensitive['close']:
                str591+=e.replace("591", "")
            print("未过滤闭合字符串：", str591)

            # str1 = mymodule.list_to_str(
            #     url_data.unsensitive['close']).replace(
            #     "591", "")
            # print(str1)
            # human_read.human_read1(url_data.unsensitive)
            [print("过滤：", e.replace("591", ""))
             for e in url_data.sensitive['close']]
            if url_data.unsensitive['close_tag']:
                payload.keyword['others'] = mymodule.list_add_start(
                    payload.keyword['others'],
                    mymodule.list_to_str(
                        url_data.unsensitive['close_tag']).replace("591", ''))
            break


        while url_data.HTTP_METHON == "POST":
            CheckPrepare.isurlok(self, url_data.post_url)
            if url_data.urlok == "no":
                return
            # if re.search(re.escape("\"'>"),self.post_response(re.sub(re.escape("abcdef1234"), "\"'>", url_data.post_data))):
            #     payload.keyword_expand("\"'>")
            # payload.keyword.sort(key=lambda x:len(x))

            def post_start(pd):
                if re.search(
                    re.escape(
                        urllib.parse.unquote(
                            urllib.parse.unquote(pd))),
                        CheckPrepare.post_response(
                            self,
                            re.sub(
                        re.escape("abcdef1234"),
                        i,
                                url_data.post_data))):  # 使用 re.escape()
                    # print(i.center(160))
                    # print("POST测试：", re.sub(re.escape("abcdef1234"),i,url_data.post_data))
                    # human_read.Dividing_line()
                    url_data.unsensitive['close'].append(pd)
                else:
                    url_data.sensitive['close'].append(pd)
            for i in payload.keyword['close']:
                mythread = threading.Thread(target=post_start(i))
                mythread.start()

            if re.search(
                r"/|%2f",
                mymodule.list_to_str(
                    url_data.unsensitive['close'])):
                for i in payload.keyword['close_tag']:
                    if re.search(
                            re.escape(
                                urllib.parse.unquote(
                                    urllib.parse.unquote(i))),
                            CheckPrepare.post_response(
                                self,
                                re.sub(
                                    re.escape("abcdef1234"),
                                    i,
                                    url_data.post_data))):

                        url_data.unsensitive['close_tag'].append(i)
                    else:
                        url_data.sensitive['close_tag'].append(i)

            [print("未过滤：", e.replace("591", ""))
             for e in url_data.unsensitive['close']]  # .replace("591","")优化输出
            # human_read.human_read1(url_data.unsensitive)
            [print("过滤：", e.replace("591", ""))
             for e in url_data.sensitive['close']]
            if url_data.unsensitive['close_tag']:
                payload.keyword['others'] = mymodule.list_add_start(
                    payload.keyword['others'],
                    mymodule.list_to_str(
                        url_data.unsensitive['close_tag']).replace("591", ''))
            break
        if url_data.unsensitive['close']:
            url_data.signal['close'] = 'yes'
        print("url_data.signal.close:", url_data.signal['close'])

    def check_action(self):
        human_read.Dividing_line()
        print("动作测试...".center(160))
        while url_data.HTTP_METHON == "GET":
            def get_start(pd):
                if re.search(
                    re.escape(
                        urllib.parse.unquote(
                            urllib.parse.unquote(pd))),
                        CheckPrepare.get_response(
                            self,
                            re.sub(
                        re.escape("abcdef1234"),
                        pd,
                                url_data.get_url))):  # 使用 re.escape()
                    # print("^^^".center(160))
                    # print(pd.center(160))
                    # print("GET测试：", re.sub(re.escape("abcdef1234"), pd, url_data.get_url))
                    # human_read.Dividing_line()
                    url_data.unsensitive['action'].append(pd)
                else:
                    url_data.sensitive['action'].append(pd)

            for i in payload.keyword['action']:
                mythread = threading.Thread(target=get_start(i))
                mythread.start()

            [print("未过滤：", e.replace("591", ""))
             for e in url_data.unsensitive['action']]
            [print("过滤：", e.replace("591", ""))
             for e in url_data.sensitive['action']]
            break
        while url_data.HTTP_METHON == "POST":
            # if re.search(re.escape("\"'>"),self.post_response(re.sub(re.escape("abcdef1234"), "\"'>", url_data.post_data))):
            #     payload.keyword_expand("\"'>")
            # payload.keyword.sort(key=lambda x:len(x))
            for i in payload.keyword['action']:
                if re.search(
                    re.escape(
                        urllib.parse.unquote(
                            urllib.parse.unquote(i))),
                        CheckPrepare.post_response(
                            self,
                            re.sub(
                        re.escape("abcdef1234"),
                        i,
                                url_data.post_data))):  # 使用 re.escape()
                    # print(i.center(160))
                    # print("POST测试：", re.sub(re.escape("abcdef1234"),i,url_data.post_data))
                    # human_read.Dividing_line()
                    url_data.unsensitive['action'].append(i)
                else:
                    url_data.sensitive['action'].append(i)
            [print("未过滤：", e.replace("591", ""))
             for e in url_data.unsensitive['action']]  # .replace("591","")优化输出
            # human_read.human_read1(url_data.unsensitive)
            [print("过滤：", e.replace("591", ""))
             for e in url_data.sensitive['action']]
            break
        if url_data.unsensitive['action']:
            url_data.signal['action'] = 'yes'
        print("url_data.signal.action:", url_data.signal['action'])

    def check_onevent(self):
        human_read.Dividing_line()
        print("on事件测试...".center(160))
        while url_data.HTTP_METHON == "GET":
            def get_start(pd):
                if re.search(
                    re.escape(
                        urllib.parse.unquote(
                            urllib.parse.unquote(pd))),
                        CheckPrepare.get_response(
                            self,
                            re.sub(
                        re.escape("abcdef1234"),
                        pd,
                                url_data.get_url))):  # 使用 re.escape()
                    # print("^^^".center(160))
                    # print(pd.center(160))
                    # print("GET测试：", re.sub(re.escape("abcdef1234"), pd, url_data.get_url))
                    # human_read.Dividing_line()
                    url_data.unsensitive['onevent'].append(pd)
                else:
                    url_data.sensitive['onevent'].append(pd)

            for i in payload.keyword['onevent']:
                mythread = threading.Thread(target=get_start(i))
                mythread.start()

            [print("未过滤：", e.replace("591", ""))
             for e in url_data.unsensitive['onevent']]
            [print("过滤：", e.replace("591", ""))
             for e in url_data.sensitive['onevent']]
            break
        while url_data.HTTP_METHON == "POST":
            # if re.search(re.escape("\"'>"),self.post_response(re.sub(re.escape("abcdef1234"), "\"'>", url_data.post_data))):
            #     payload.keyword_expand("\"'>")
            # payload.keyword.sort(key=lambda x:len(x))
            for i in payload.keyword['onevent']:
                if re.search(
                    re.escape(
                        urllib.parse.unquote(
                            urllib.parse.unquote(i))),
                        CheckPrepare.post_response(
                            self,
                            re.sub(
                        re.escape("abcdef1234"),
                        i,
                                url_data.post_data))):  # 使用 re.escape()
                    # print(i.center(160))
                    # print("POST测试：", re.sub(re.escape("abcdef1234"),i,url_data.post_data))
                    # human_read.Dividing_line()
                    url_data.unsensitive['onevent'].append(i)
                else:
                    url_data.sensitive['onevent'].append(i)
            [print("未过滤：", e.replace("591", ""))
             for e in url_data.unsensitive['onevent']]  # .replace("591","")优化输出
            # human_read.human_read1(url_data.unsensitive)
            [print("过滤：", e.replace("591", ""))
             for e in url_data.sensitive['onevent']]
            break
        if url_data.unsensitive['onevent']:
            url_data.signal['onevent'] = 'yes'
        print("url_data.signal.onevent:", url_data.signal['onevent'])

    def check_tag(self):
        human_read.Dividing_line()
        print("标签测试...".center(160))
        while url_data.HTTP_METHON == "GET":
            def get_start(pd):
                if re.search(
                    re.escape(
                        urllib.parse.unquote(
                            urllib.parse.unquote(pd))),
                        CheckPrepare.get_response(
                            self,
                            re.sub(
                        re.escape("abcdef1234"),
                        pd,
                                url_data.get_url))):  # 使用 re.escape()
                    # print("^^^".center(160))
                    # print(pd.center(160))
                    # print("GET测试：", re.sub(re.escape("abcdef1234"), pd, url_data.get_url))
                    # human_read.Dividing_line()
                    print(url_data.unsensitive['tag'])
                    url_data.unsensitive['tag'].append(pd)
                else:
                    url_data.sensitive['tag'].append(pd)

            for i in payload.keyword['tag']:
                mythread = threading.Thread(target=get_start(i))
                mythread.start()

            [print("未过滤：", e.replace("591", ""))
             for e in url_data.unsensitive['tag']]
            [print("过滤：", e.replace("591", ""))
             for e in url_data.sensitive['tag']]
            break
        while url_data.HTTP_METHON == "POST":
            # if re.search(re.escape("\"'>"),self.post_response(re.sub(re.escape("abcdef1234"), "\"'>", url_data.post_data))):
            #     payload.keyword_expand("\"'>")
            # payload.keyword.sort(key=lambda x:len(x))
            for i in payload.keyword['tag']:
                if re.search(
                    re.escape(
                        urllib.parse.unquote(
                            urllib.parse.unquote(i))),
                        CheckPrepare.post_response(
                            self,
                            re.sub(
                        re.escape("abcdef1234"),
                        i,
                                url_data.post_data))):  # 使用 re.escape()
                    # print(i.center(160))
                    # print("POST测试：", re.sub(re.escape("abcdef1234"),i,url_data.post_data))
                    # human_read.Dividing_line()
                    url_data.unsensitive['tag'].append(i)
                else:
                    url_data.sensitive['tag'].append(i)
            [print("未过滤：", e.replace("591", ""))
             for e in url_data.unsensitive['tag']]  # .replace("591","")优化输出
            # human_read.human_read1(url_data.unsensitive)
            [print("过滤：", e.replace("591", ""))
             for e in url_data.sensitive['tag']]
            break
        if url_data.unsensitive['tag']:
            url_data.signal['tag'] = 'yes'
        print("url_data.signal.tag:", url_data.signal['tag'])

    def check_others(self):
        human_read.Dividing_line()
        print("综合测试...".center(160))
        if not url_data.signal['action'] == url_data.signal['onevent'] == 'yes':
            print("action和 onevent 均被过滤，不再进行综合测试...".center(160))
            return
        while url_data.HTTP_METHON == "GET":
            def get_start(pd):
                if re.search(
                    re.escape(
                        urllib.parse.unquote(
                            urllib.parse.unquote(pd))),
                        CheckPrepare.get_response(
                            self,
                            re.sub(
                        re.escape("abcdef1234"),
                        pd,
                                url_data.get_url))):  # 使用 re.escape()
                    # print("^^^".center(160))
                    print(pd.center(160))
                    # print("GET测试：", re.sub(re.escape("abcdef1234"), pd, url_data.get_url))
                    human_read.Dividing_line()
                    url_data.unsensitive['others'].append(pd)
                else:
                    url_data.sensitive['others'].append(pd)

            for i in payload.keyword['others']:
                mythread = threading.Thread(target=get_start(i))
                mythread.start()

            [print("未过滤：", e.replace("591", ""))
             for e in url_data.unsensitive['others']]
            [print("过滤：", e.replace("591", ""))
             for e in url_data.sensitive['others']]
            break
        while url_data.HTTP_METHON == "POST":
            # if re.search(re.escape("\"'>"),self.post_response(re.sub(re.escape("abcdef1234"), "\"'>", url_data.post_data))):
            #     payload.keyword_expand("\"'>")
            # payload.keyword.sort(key=lambda x:len(x))
            for i in payload.keyword['others']:
                if re.search(
                    re.escape(
                        urllib.parse.unquote(
                            urllib.parse.unquote(i))),
                        CheckPrepare.post_response(
                            self,
                            re.sub(
                        re.escape("abcdef1234"),
                        i,
                                url_data.post_data))):  # 使用 re.escape()
                    print(i.center(160))
                    print(
                        "注入成功：",
                        re.sub(
                            re.escape("abcdef1234"),
                            i,
                            url_data.post_data))
                    human_read.Dividing_line()
                    url_data.unsensitive['others'].append(i)
                else:
                    url_data.sensitive['others'].append(i)
            if url_data.unsensitive['others']:
                [print("未过滤：", e.replace("591", ""))
                 for e in url_data.unsensitive['others']]  # .replace("591","")优化输出
            else:
                print("无综合 payload...")
            # human_read.human_read1(url_data.unsensitive)
            # [print("过滤：", e.replace("591", "")) for e in url_data.sensitive]
            break
    def check_illusion(self):
        human_read.Dividing_line()
        print("Illusion Testing".center(200))
        mymodule.iilusion_replace() #对 payload 进行校验
        # print(str(mymodule.keyword['illusion']))
        if not mymodule.keyword['illusion']:
            print("No Payload , quit now .".center(160))
            return
        while url_data.HTTP_METHON == "GET":
            def get_start(pd):
                if re.search(
                        re.escape(
                            urllib.parse.unquote(
                                urllib.parse.unquote(pd))),
                        CheckPrepare.get_response(
                            self,
                            re.sub(
                                re.escape("abcdef1234"),
                                pd,
                                url_data.get_url))):  # 使用 re.escape()
                    print(pd.center(160))
                    human_read.Dividing_line()
                    url_data.unsensitive['illusion'].append(pd)
                else:
                    url_data.sensitive['illusion'].append(pd)

            for i in mymodule.keyword['illusion']:
                mythread = threading.Thread(target=get_start(i))
                mythread.start()

            [print("未过滤：", e.replace("591", ""))
             for e in url_data.unsensitive['illusion']]
            [print("过滤：", e.replace("591", ""))
             for e in url_data.sensitive['illusion']]
            break
        while url_data.HTTP_METHON == "POST":
            # if re.search(re.escape("\"'>"),self.post_response(re.sub(re.escape("abcdef1234"), "\"'>", url_data.post_data))):
            #     payload.keyword_expand("\"'>")
            # payload.keyword.sort(key=lambda x:len(x))
            for i in mymodule.keyword['illusion']:
                if re.search(
                        re.escape(
                            urllib.parse.unquote(
                                urllib.parse.unquote(i))),
                        CheckPrepare.post_response(
                            self,
                            re.sub(
                                re.escape("abcdef1234"),
                                i,
                                url_data.post_data))):  # 使用 re.escape()
                    print(i.center(160))
                    print(
                        "注入成功：",
                        re.sub(
                            re.escape("abcdef1234"),
                            i,
                            url_data.post_data))
                    human_read.Dividing_line()
                    url_data.unsensitive['illusion'].append(i)
                else:
                    url_data.sensitive['illusion'].append(i)
            if url_data.unsensitive['illusion']:
                [print("未过滤：", e.replace("591", ""))
                 for e in url_data.unsensitive['illusion']]  # .replace("591","")优化输出
            else:
                print("无综合 payload...")
            # human_read.human_read1(url_data.unsensitive)
            # [print("过滤：", e.replace("591", "")) for e in url_data.sensitive]
            break


        human_read.Dividing_line()

if __name__ == "__main__":
    app = QApplication(sys.argv)  # the standard way to init QT
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())
