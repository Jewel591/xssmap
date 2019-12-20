import re
import sys
import time
import requests
from data import urldata
from urllib import request
from modules.noquote import NoQuoteSession
from urllib import parse
from modules.argsparse import argsparse
import ssl # 关闭 ssl 证书验证
ssl._create_default_https_context = ssl._create_unverified_context



class PreCheck():
    def responsebyurl(self, payload):
        argss = argsparse().args()

        # 初始化部分变量
        urlafter=argss.url
        dataafter=argss.postdata
        cookieafter=argss.cookie
        refererafter=argss.referer
        useragentafter=argss.useragent

        param_replace = {urldata.targetvar: payload}


        #  distinguish POST / GET

        argsInUrl=parse.parse_qs(parse.urlparse(argss.url).query)
        argsInPostdata=parse.parse_qs(argss.postdata) if argss.postdata else {}
        argsInCookie=parse.parse_qs(argss.cookie) if argss.cookie else {}
        argsInUsergent=parse.parse_qs(argss.useragent) if argss.useragent else {}
        argsInReferer=parse.parse_qs(argss.referer) if argss.referer else {}

        def encoder(mydict):
            return ("&".join("{}={}".format(*i) for i in mydict.items()))

        if urldata.targetvar in argsInUrl:
            url_parts=list(parse.urlparse(argss.url))
            query_url=dict(parse.parse_qsl(url_parts[4]))
            query_url.update(param_replace)
            url_parts[4]=encoder(query_url)
            urlafter = parse.urlunparse(url_parts)


        if urldata.targetvar in argsInPostdata:
            query_postdata=dict(parse.parse_qsl(argss.postdata))
            query_postdata.update(param_replace)
            dataafter=encoder(query_postdata)

        if urldata.targetvar in argsInCookie:
            query_cookie = dict(parse.parse_qsl(argss.cookie))
            query_cookie.update(param_replace)
            cookieafter = encoder(query_cookie)

        if urldata.targetvar in argsInReferer:
            query_referer = dict(parse.parse_qsl(argss.referer))
            query_referer.update(param_replace)
            refererafter = encoder(query_referer)

        if urldata.targetvar in argsInUsergent:
            query_useragent = dict(parse.parse_qsl(argss.useragent))
            query_useragent.update(param_replace)
            useragentafter = encoder(query_useragent)



        # set proxy http/https
        if argss.proxy and "https" in urlafter:
            proxy_support_https = request.ProxyHandler({'https': argss.proxy})
            opener = request.build_opener(proxy_support_https)
            request.install_opener(opener)
        elif argss.proxy and "http" in urlafter:
            proxy_support_http = request.ProxyHandler({'http': argss.proxy})
            opener = request.build_opener(proxy_support_http)
            request.install_opener(opener)

        # set header
        header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            }
        if argss.cookie : header['Cookie'] = cookieafter
        if argss.referer: header['Referer'] = refererafter
        header['User-Agent'] = useragentafter if argss.useragent else "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
        url_request = request.Request(url=urlafter.replace(" ","%20"), data=dataafter.encode('utf-8'),headers=header) if argss.postdata else request.Request(url=urlafter.replace(" ","%20"),headers=header)

        try:
            url_response = request.urlopen(url_request, timeout=int(argss.timeout), capath=None)  # capath 不解析 https 证书
            try:
                return url_response.read().decode('utf-8')
            except:
                try:
                    return url_response.read().decode('gb2312')
                except:
                    print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"\033[1;33m[WARNING]\033[0m"+"Unrecognized response encoding, force bytes-to-string")
                    return str(url_response.read())
        except Exception as e:
            if argss.verbose : print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"\033[1;30m[ERROR] \033[0m"+"\033[1;30m"+str(e)+"\033[0m")

            # if argss.verbose : print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"\033[1;31m[ERROR]\033[0m unable to connect to the target URL. May be due to a security policy")
            return "NoResponse"

    @staticmethod
    def getallparameter():
        # print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"test")
        args2 = argsparse().args()

        argsInUrl = parse.parse_qs(parse.urlparse(args2.url).query)
        argsInPostdata = parse.parse_qs(args2.postdata) if args2.postdata else {}
        argsInCookie = parse.parse_qs(args2.cookie) if args2.cookie else {}
        argsInUsergent = parse.parse_qs(args2.useragent) if args2.useragent else {}
        argsInReferer = parse.parse_qs(args2.referer) if args2.referer else {}
        allargs = {**argsInUrl,**argsInPostdata,**argsInUsergent,**argsInReferer,**argsInCookie}

        return allargs


    def checkurlaccessible(self):
        print("\033[1;34m[" + str(time.strftime("%H:%M:%S",
                                                time.localtime())) + "]\033[0m " + "\033[1;32m[INFO]\033[0m testing connection to the target URL")
        if self.responsebyurl("591") =="NoResponse":
            print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"\033[1;33m[WARNING] site can't connected\033[0m"+"\033[1;30m (eg.. use -v get information)\033[0m")
            print("\033[1;34m[" + str(time.strftime("%H:%M:%S", time.localtime())) + "]\033[0m " + "exiting...")
            return 0
        else:
            print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"\033[1;32m[INFO] site connected success \033[0m ")
            return 1

    def rebuildurl(self):
        targetvar = urldata.targetvar #去除参数末尾的空格——输入1
        if len(targetvar)==0:
            targetvar = "不存在的参数"
        revar0 = targetvar + "="
        revar1 = targetvar + "=.*?&"
        revar2 = targetvar + "=.*"
        if len(re.findall(revar0, urldata.targeturl)) > 1:
            print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"\033[1;32;8m[警告] "+"匹配到 > 1 个"+urldata.targetvar+"，默认使用第一个，请确认目标参数是否替换正确"+"\033[0m")
        if len(re.findall(revar0, urldata.targeturl)) < 1 and "REFERER" not in urldata.targeturl and "COOKIE" not in urldata.targeturl:
            print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"\033[1;32;8m[警告] " + "url 中未匹配到" + urldata.targetvar + "，请确认目标参数是否输入正确" + "\033[0m")
            sys.exit(0)
        if not re.search("(POST)", urldata.targeturl) and not re.search("(REFERER)", urldata.targeturl) and not re.search("(COOKIE)", urldata.targeturl):
            urldata.HTTP_METHON = "GET"
            if re.search(revar1, urldata.targeturl):
                urldata.get_url = re.sub(
                    revar1, targetvar + "=" + "abcdef1234&", urldata.targeturl)
                # print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"[!] 清除敏感字符: ", urldata.get_url)
            else:
                urldata.get_url = re.sub(
                    revar2, targetvar + "=" + "abcdef1234", urldata.targeturl)
                # print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"[!] 清除敏感字符: ", urldata.get_url)
        else:
            if re.search("(REFERER)", urldata.targeturl):
                if re.search("(POST)", urldata.targeturl):
                    print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+'\033[1;32;8m[警告] 同时检测到 POST 和 REFERER，请手动删除 POST 数据，仅保留 REFERER 数据再尝试! \033[0m')
                    print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+'\033[1;32;8m[举个栗子] www.abc.com(POST)data1(REFERER)data2 => www.abc.com(REFERER)data2 \033[0m')
                    sys.exit(0)
                else:
                    print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+'\033[1;32;8m[+] REFERER FIND ! 尝试进行 Referer 注入 \033[0m')
                    urldata.HTTP_METHON = "REFERER"
                    url_split_list = re.split(re.escape("(REFERER)"), urldata.targeturl)
                    urldata.referer_url = url_split_list[0]

            else:
                if re.search("(COOKIE)", urldata.targeturl):
                    print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+'\033[1;32;8m[+] COOKIE FIND ! 尝试进行 Cookie 注入 \033[0m'+"\n")
                    print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+"COOKIE 检测代码还没写，莫慌 ~")
                    urldata.HTTP_METHON = "COOKIE"
                    url_split_list = re.split(re.escape("(COOKIE)"), urldata.targeturl)
                    urldata.referer_url = url_split_list[0]
                    sys.exit(0)
                else:
                    urldata.HTTP_METHON = "POST"
                    print("\033[1;34m["+str(time.strftime("%H:%M:%S", time.localtime()))+"]\033[0m "+'\033[1;32;8m[+] POST FIND ! 尝试进行 POST 参数注入 \033[0m'+"\n")
                    url_split_list = re.split(re.escape("(POST)"), urldata.targeturl)
                    urldata.post_url = url_split_list[0]

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