import re
import os
import requests
import subprocess
import urldata
import format
from noquote import NoQuoteSession


class CheckPrepare():
    def isurlok(self):
        while urldata.HTTP_METHON == "GET":
            try:
                header = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0',
                    'Content-Type': 'application/x-www-form-urlencoded'}
                requests.get(urldata.get_url, headers=header, verify=False, timeout=3)
            except BaseException:
                print("站点不可达...".center(170))
                urldata.urlok = "no"
                return

        while urldata.HTTP_METHON == "POST":
            try:
                header = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0',
                    'Content-Type': 'application/x-www-form-urlencoded'}
                requests.post(urldata.post_url,data=urldata.post_data, headers=header, verify=False, timeout=3)
            except BaseException:
                print("站点不可达...".center(170))
                urldata.urlok = "no"
                return 


        # 重构 url 和 keyword

    def rebuild(self):
        # payload.keyword_expand("<>")#重构 keyword
        word = urldata.word#去除参数末尾的空格——输入1
        if word=="":
            word = "style"
        re_word = word + ".*?&"
        re_word_2 = word + ".*"
        # print(re_word)
        if not re.search("(POST)", urldata.targeturl):
            urldata.HTTP_METHON = "GET"
            if re.search(re_word, urldata.targeturl):
                urldata.get_url = re.sub(
                    re_word, word + "=" + "abcdef1234&", urldata.targeturl)
                print("清除敏感字符".center(170), "\n","\n", urldata.get_url)
                format.breakline()
            else:
                urldata.get_url = re.sub(
                    re_word_2, word + "=" + "abcdef1234", urldata.targeturl)
                print("清除敏感字符".center(170),"\n","\n", urldata.get_url)
                format.breakline()
        else:
            urldata.HTTP_METHON = "POST"
            # print("Test Post".center(170))
            # Dividing_line()
            url_split_list = re.split(re.escape("(POST)"), urldata.targeturl)
            urldata.post_url = url_split_list[0]
            print("PostURL".center(170), "\n", urldata.post_url)
            format.breakline()
            print("PostData".center(170), "\n", url_split_list[1])
            format.breakline()

            if re.search(re_word, url_split_list[1]):
                urldata.post_data = re.sub(
                    re_word,
                    word + "=" + "abcdef1234&",
                    url_split_list[1])
                print("Payload Replace".center(170),"\n", urldata.post_data)
                format.breakline()
            else:
                urldata.post_data = re.sub(
                    re_word_2,
                    word + "=" + "abcdef1234",
                    url_split_list[1])
                print("Payload Replace".center(170), urldata.post_data)
                format.breakline()

    def get_response(self, url):
        print("[测试中]-Get:", url)
        # Dividing_line()
        r = NoQuoteSession()
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0',
            'Content-Type': 'application/x-www-form-urlencoded'}
        proxy = {"http": "http://127.0.0.1:8080",
                 "https": "http://127.0.0.1:8080"}
        try:
            return r.get(url, headers=header, verify=False, timeout=3).text
        # except requests.exceptions.ConnectionError:
        except BaseException:
            # print("请确认 BurpSuite 是否开启~")
            return "get no Response"

    def post_response(self, data):
        print("[测试中]-Post:",data)
        r = NoQuoteSession()
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0',
            'Content-Type': 'application/x-www-form-urlencoded'}
        proxy = {"http": "http://127.0.0.1:8080",
                 "https": "http://127.0.0.1:8080"}
        try:
            s2=r.post(
                urldata.post_url,
                data=data,
                headers=header,
                verify=False,
                timeout=3).text
            return s2
            print("1212")
        # except requests.exceptions.ConnectionError:
        except BaseException:
            print("连接超时...timeout:3")
            return "post no Response"

    def get_response_burp(self, url):
        # print("GET测试：",url)
        # Dividing_line()
        r = NoQuoteSession()
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0',
            'Content-Type': 'application/x-www-form-urlencoded'}
        proxy = {"http": "http://127.0.0.1:8080",
                 "https": "http://127.0.0.1:8080"}
        try:
            return r.get(
                url,
                headers=header,
                proxies=proxy,
                verify=False,
                timeout=3).text
        except requests.exceptions.ConnectionError:
            return "get no Response"

    def post_response_burp(self, data):
        # print("url_data.post_data:",data)
        r = NoQuoteSession()
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0',
            'Content-Type': 'application/x-www-form-urlencoded'}
        proxy = {"http": "http://127.0.0.1:8080",
                 "https": "http://127.0f.0.1:8080"}
        try:
            return r.post(
                urldata.post_url,
                data=data,
                headers=header,
                proxies=proxy,
                verify=False,
                timeout=3).text
        except requests.exceptions.ConnectionError:
            return "post no Response"
