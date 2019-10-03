import re
import requests
from data import urldata
from modules import format
from modules.noquote import NoQuoteSession


class PreCheck():
    def checkurlaccessible(self):
        while urldata.HTTP_METHON == "GET":
            try:
                header = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0',
                    'Content-Type': 'application/x-www-form-urlencoded'}
                requests.get(urldata.get_url, headers=header, verify=False, timeout=3)
                print(">>> 站点可访")
                break
            except BaseException:
                print(">>> 站点不可访")
                urldata.urlsuccess = "no"
                return

        while urldata.HTTP_METHON == "POST":
            try:
                header = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0',
                    'Content-Type': 'application/x-www-form-urlencoded'}
                requests.post(urldata.post_url, data=urldata.post_data, headers=header, verify=False, timeout=3)
                print(">>> 站点可访")
                break
            except BaseException:
                print(">>> 站点不可访")
                urldata.urlsuccess = "no"
                return 


### 去除 url 中目标参数自带的敏感字符
    def rebuildurl(self):
        targetvar = urldata.targetvar #去除参数末尾的空格——输入1
        if targetvar=="":
            targetvar = "height"
        revar1 = targetvar + ".*?&"
        revar2 = targetvar + ".*"
        if not re.search("(POST)", urldata.targeturl):
            urldata.HTTP_METHON = "GET"
            if re.search(revar1, urldata.targeturl):
                urldata.get_url = re.sub(
                    revar1, targetvar + "=" + "abcdef1234&", urldata.targeturl)
                print(">>> 清除敏感字符: ", urldata.get_url)
                # format.breakline()
            else:
                urldata.get_url = re.sub(
                    revar2, targetvar + "=" + "abcdef1234", urldata.targeturl)
                print(">>> 清除敏感字符: ", urldata.get_url)
                # format.breakline()
        else:
            urldata.HTTP_METHON = "POST"
            url_split_list = re.split(re.escape("(POST)"), urldata.targeturl)
            urldata.post_url = url_split_list[0]
            print(">>> posturl ", urldata.post_url)
            # format.breakline()
            print(">>> postdata ", url_split_list[1])

            if re.search(revar1, url_split_list[1]):
                urldata.post_data = re.sub(
                    revar1,
                    targetvar + "=" + "abcdef1234&",
                    url_split_list[1])
            else:
                urldata.post_data = re.sub(
                    revar2,
                    targetvar + "=" + "abcdef1234",
                    url_split_list[1])

    def get_response(self, url, verbose):
        if verbose=="yes":
            print("[+] GET : ", url)
        else:
            print(".",end='')
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

    def post_response(self, data, verbose):
        if verbose == "yes":
            print("[+] POST : ",data)
        else:
            print(".", end='')
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
            print(">>> 连接超时...timeout:3")
            return "post no Response"

    def get_response_burp(self, url):
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
