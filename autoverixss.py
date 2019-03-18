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
import payload
# from payload import PAYPOAD
# # 这两行是为了去除"请求 https 站点取消 ssl 认证时控制台的警告信息"
# # from requests.packages.urllib3.exceptions import InsecureRequestWarning
# # requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
time_start = time_end=""
urlok="yes"
targeturl = ""
word = ""
HTTP_METHON="not know"
post_url="post 请求的 url"
post_data="post 请求的 data"
get_url="get 请求的 url"
sensitive = []
unsensitive = []
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


#用于整理、输出一些更人性化的提醒
class HumanRead():
    def check_1(list):#此方法用于提醒<>都被过滤
        newstr=""
        for i in list:
            newstr+=i
        if not re.search("<|>|%3c|%3e",newstr):
            print("<>都被过滤...")

    def Dividing_line():
        print("———————————————————————————————————————————————")

class Check_XSS():
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
        payload.keyword_expand("<>")#重构 keyword
        word = myWin.input_arg.text().strip()#去除参数末尾的空格
        # word="PAGE_ID"
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
                HumanRead.Dividing_line()
            else:
                get_url = re.sub(re_word_2,word+"="+"abcdef(1234)",targeturl)
                print("url replace".center(170),get_url)
                HumanRead.Dividing_line()
        else:
            HTTP_METHON = "POST"
            # print("Test Post".center(160))
            # Dividing_line()
            url_split_list=re.split(re.escape("(POST)"),targeturl)
            post_url = url_split_list[0]
            print("PostURL".center(160),"\n",post_url)
            HumanRead.Dividing_line()
            print("PostData".center(160),"\n",url_split_list[1])
            HumanRead.Dividing_line()

            if re.search(re_word,url_split_list[1]):
                post_data = re.sub(re_word, word + "=" + "abcdef(1234)&", url_split_list[1])
                print("Payload Replace".center(160),post_data)
                HumanRead.Dividing_line()
            else:
                post_data = re.sub(re_word_2, word + "=" + "abcdef(1234)", url_split_list[1])
                print("Payload Replace".center(160), post_data)

    def start_check(self):
        global targeturl,sensitive,unsensitive,HTTP_METHON
        print("正在测试...".center(160),"\n")
        sensitive.clear()
        unsensitive.clear()
        while HTTP_METHON=="GET":
            self.isurlok(get_url)
            if urlok == "no":
                return
            if re.search(re.escape("\"'>"),self.get_response(re.sub(re.escape("abcdef(1234)"), "\"'>", get_url))):
                payload.keyword_expand("\"'>")
            payload.keyword.sort(key=lambda x:len(x))
            def get_start(pd):
                if re.search(re.escape(urllib.parse.unquote(urllib.parse.unquote(pd))),
                             self.get_response(re.sub(re.escape("abcdef(1234)"), pd, get_url))):  # 使用 re.escape()
                    # print("^^^".center(160))
                    print(pd.center(160))
                    print("GET测试：", re.sub(re.escape("abcdef(1234)"), pd, get_url))
                    HumanRead.Dividing_line()
                    unsensitive.append(pd)
                else:
                    sensitive.append(pd)
            for i in payload.keyword:
                mythread=threading.Thread(target=get_start(i))
                mythread.start()
                # get_start(i)

            print("测试结果".center(160))
            [print("未过滤：", e.replace("591", "")) for e in unsensitive]
            HumanRead.check_1(unsensitive)
            [print("过滤：",e.replace("591", "")) for e in sensitive]
            break
        while HTTP_METHON=="POST":
            self.isurlok(post_url)
            if urlok == "no":
                return
            if re.search(re.escape("\"'>"),self.post_response(re.sub(re.escape("abcdef(1234)"), "\"'>", post_data))):
                payload.keyword_expand("\"'>")
            payload.keyword.sort(key=lambda x:len(x))
            # print(payload.keyword)
            for i in payload.keyword:
                if re.search(re.escape(urllib.parse.unquote(urllib.parse.unquote(i))), self.post_response(re.sub(re.escape("abcdef(1234)"),i,post_data))):  # 使用 re.escape()
                    # print("^^^".center(160))
                    print(i.center(160))
                    print("POST测试：", re.sub(re.escape("abcdef(1234)"),i,post_data))
                    HumanRead.Dividing_line()
                    unsensitive.append(i)
                else:
                    sensitive.append(i)
            print("测试结果".center(160))
            [print("未过滤：", e.replace("591","")) for e in unsensitive]#.replace("591","")优化输出
            HumanRead.check_1(unsensitive)
            [print("过滤：", e.replace("591", "")) for e in sensitive]
            break



class Worker(QThread):
    def __init__(self):
        super(Worker, self).__init__()

    def run(self):
        global time_start, time_end, targeturl
        time_start = time.time()
        # if not len(myWin.input_url.text()):
        #         #     print("请输入目标 URL...")
        #         #     return # 退出逻辑线程
        #         # if not len(myWin.input_arg.text()):
        #         #     print("请输出注入参数...")
        #         #     return
        print("开始分析...".center(160), "\n")
        payload.keyword_init()
        targeturl = myWin.input_url.text()
        # targeturl = "http://www.hebeizy.com.cn/ycplatform/hcomp/exWebSite/cms/cmsApp(POST)_TIMESTAMP=1500552979927&pageSize=&pageNo=&jspUrl=&classIds=ICd7a83f151139ed5f91f1c,111&WEB_PART_ID=A9B48317461F6882755A62F3DB1B97EB&COMPONENT_METHOD=queryAccessCmsPageContentWwmh&PAGE_ID=\"'\"></a><object+data=jav\x61scr\x69pt:wryvwb(6590)>&WEB_PART_INST_ID=1448419998869"
        # targeturl ="https://jfdh.qlbchina.com/jfymall-client/goods/searchgoods.do(POST)serachType2=aaaa';window[`conf`+`irm`]`1`//&searchvalue=%E5%85%B3%E9%94%AE%E5%AD%97 "
        print("Target URL".center(160), "\n", targeturl)
        HumanRead.Dividing_line()
        begin = Check_XSS()
        begin.rebuild()
        begin.start_check()
        HumanRead.Dividing_line()
        time_end = time.time()
        print("测试耗时：", time_end - time_start)



class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))


if __name__=="__main__":
    app = QApplication(sys.argv) #the standard way to init QT
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())