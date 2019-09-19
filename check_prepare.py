import re

import requests

import url_data
import human_read
from noquote import NoQuoteSession


class CheckPrepare():
    def isurlok(self, url):
        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0',
                'Content-Type': 'application/x-www-form-urlencoded'}
            requests.get(url, headers=header, verify=False, timeout=3)
        except BaseException:
            print("站点不可达...".center(160))
            url_data.urlok = "no"

        # 重构 url 和 keyword

    def rebuild(self):
        # payload.keyword_expand("<>")#重构 keyword
        word = url_data.word#去除参数末尾的空格——输入1
        # word="PAGE_ID"
        # word = "serachType2"
        if word=="":
            word = "contentno"
        re_word = word + ".*?&"
        re_word_2 = word + ".*"
        # print(re_word)
        if not re.search("(POST)", url_data.targeturl):
            url_data.HTTP_METHON = "GET"
            # print("Test Get".center(160))
            # Dividing_line()
            # print(re_word)
            if re.search(re_word, url_data.targeturl):
                url_data.get_url = re.sub(
                    re_word, word + "=" + "abcdef1234&", url_data.targeturl)
                print("url replace".center(170), "\n", url_data.get_url)
                human_read.Dividing_line()
            else:
                url_data.get_url = re.sub(
                    re_word_2, word + "=" + "abcdef1234", url_data.targeturl)
                print("url replace".center(170), url_data.get_url)
                human_read.Dividing_line()
        else:
            url_data.HTTP_METHON = "POST"
            # print("Test Post".center(160))
            # Dividing_line()
            url_split_list = re.split(re.escape("(POST)"), url_data.targeturl)
            url_data.post_url = url_split_list[0]
            print("PostURL".center(160), "\n", url_data.post_url)
            human_read.Dividing_line()
            print("PostData".center(160), "\n", url_split_list[1])
            human_read.Dividing_line()

            if re.search(re_word, url_split_list[1]):
                url_data.post_data = re.sub(
                    re_word,
                    word + "=" + "abcdef1234&",
                    url_split_list[1])
                print("Payload Replace".center(160), url_data.post_data)
                human_read.Dividing_line()
            else:
                url_data.post_data = re.sub(
                    re_word_2,
                    word + "=" + "abcdef1234",
                    url_split_list[1])
                print("Payload Replace".center(160), url_data.post_data)
                human_read.Dividing_line()

    def get_response(self, url):
        print("Geting：", url)
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
        # print("Posting:",data)
        r = NoQuoteSession()
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0',
            'Content-Type': 'application/x-www-form-urlencoded'}
        proxy = {"http": "http://127.0.0.1:8080",
                 "https": "http://127.0.0.1:8080"}
        try:
            s2=r.post(
                url_data.post_url,
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
                url_data.post_url,
                data=data,
                headers=header,
                proxies=proxy,
                verify=False,
                timeout=3).text
        except requests.exceptions.ConnectionError:
            return "post no Response"
