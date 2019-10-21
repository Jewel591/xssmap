import re
import sys
import requests
from data import urldata
from urllib import request
from modules import format
from modules.noquote import NoQuoteSession


class PreCheck():
    def checkurlaccessible(self):
        while urldata.HTTP_METHON == "GET":
            try:
                header = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0',
                    'Content-Type': 'application/x-www-form-urlencoded'}
                requests.get(urldata.get_url, headers=header, verify=False, timeout=5)
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
                requests.post(urldata.post_url, data=urldata.post_data, headers=header, verify=False, timeout=5)
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
        revar0 = targetvar + "="
        revar1 = targetvar + "=.*?&"
        revar2 = targetvar + "=.*"
        if len(re.findall(revar0, urldata.targeturl)) > 1:
            print("\033[1;31;8m[警告] "+"匹配到 > 1 个"+urldata.targetvar+"，默认使用第一个，请确认目标参数是否替换正确"+"\033[0m")
        if len(re.findall(revar0, urldata.targeturl)) < 1:
            print("\033[1;31;8m[警告] " + "url 中未匹配到" + urldata.targetvar + "，请确认目标参数是否输入正确" + "\033[0m")
            sys.exit(0)
        if not re.search("(POST)", urldata.targeturl) and not re.search("(REFERER)", urldata.targeturl) and not re.search("(COOKIE)", urldata.targeturl):
            urldata.HTTP_METHON = "GET"
            if re.search(revar1, urldata.targeturl):
                urldata.get_url = re.sub(
                    revar1, targetvar + "=" + "abcdef1234&", urldata.targeturl)
                print(">>> 清除敏感字符: ", urldata.get_url)
            else:
                urldata.get_url = re.sub(
                    revar2, targetvar + "=" + "abcdef1234", urldata.targeturl)
                print(">>> 清除敏感字符: ", urldata.get_url)
        else:
            if re.search("(REFERER)", urldata.targeturl):
                urldata.HTTP_METHON = "REFERER"
                url_split_list = re.split(re.escape("(REFERER)"), urldata.targeturl)
                urldata.referer_url = url_split_list[0]
                print(">>> refererurl ", urldata.referer_url)
                print(">>> referer 自动清空")

            else:
                if re.search("(COOKIE)", urldata.targeturl):
                    print("COOKIE 函数还没写")
                    sys.exit(0)
                else:
                    urldata.HTTP_METHON = "POST"
                    url_split_list = re.split(re.escape("(POST)"), urldata.targeturl)
                    urldata.post_url = url_split_list[0]
                    print(">>> posturl ", urldata.post_url)
                    print(">>> postdata ", url_split_list[1])

                    if re.search(revar1, url_split_list[1]):
                        urldata.post_data = re.sub(
                            revar1,
                            targetvar + "=" + "abcdef1234&",
                            url_split_list[1])
                        print(">>> 清除敏感字符: ", urldata.post_data)
                    else:
                        urldata.post_data = re.sub(
                            revar2,
                            targetvar + "=" + "abcdef1234",
                            url_split_list[1])
                        print(">>> 清除敏感字符: ", urldata.post_data)

    def get_response(self, url, verbose):
        if verbose=="yes":
            print("[+] GET : ", url)
        else:
            print(".",end='')
            sys.stdout.flush()
        r = NoQuoteSession()
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0',
            'Content-Type': 'application/x-www-form-urlencoded'}
        proxy = {"http": "http://127.0.0.1:8080",
                 "https": "http://127.0.0.1:8080"}

        try:
            ### 这三行开启代理
            # proxy_support = request.ProxyHandler({'http': '127.0.0.1:8080'})
            # opener = request.build_opener(proxy_support)
            # request.install_opener(opener)

            # 使用 urllib 才能解决 url 编码的问题
            with request.urlopen(url) as response:
                data = response.read()
                return data.decode('utf-8')
        except BaseException:
            if verbose == "yes":
                print(">>> 连接错误")
            return "get no Response"

    def post_response(self, data, verbose):
        if verbose == "yes":
            print("[+] POST : ",data)
        else:
            print(".", end='')
            sys.stdout.flush()
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
                # proxies = proxy,
                headers=header,
                verify=False,
                timeout=5).text
            return s2
        # except requests.exceptions.ConnectionError:
        except BaseException:
            if verbose == "yes":
                print(">>> 连接错误")
            return "post no Response"

    def referer_response(self, data, verbose):
        if verbose == "yes":
            print("[+] Referer : ",data)
        else:
            print(".", end='')
            sys.stdout.flush()
        # r = NoQuoteSession()
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': data}
        proxy = {"http": "http://127.0.0.1:8080",
                 "https": "http://127.0.0.1:8080"}
        try:
            response2referer=requests.get(
                urldata.referer_url,
                # proxies = proxy,
                headers=header,
                verify=False,
                timeout=5).text
            return response2referer
        # except requests.exceptions.ConnectionError:
        except BaseException:
            if verbose == "yes":
                print(">>> 连接错误")
            return "post no Response"


    def cookie_response(self, data, verbose):
        if verbose == "yes":
            print("[+] Cookie : ",data)
        else:
            print(".", end='')
            sys.stdout.flush()
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
                # proxies = proxy,
                headers=header,
                verify=False,
                timeout=5).text
            return s2
        # except requests.exceptions.ConnectionError:
        except BaseException:
            if verbose == "yes":
                print(">>> 连接错误")
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
