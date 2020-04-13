import re
import sys
from data import urldata
from urllib import request
from urllib import parse
from modules.argsparse import argsparse
import ssl # disable ssl checking
ssl._create_default_https_context = ssl._create_unverified_context



class PreCheck():
    def responsebyurl(self, payload):
        argss = argsparse().args()

        # init args
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
                    print("\033[1;33m[WARNING]\033[0m"+"Unrecognized response encoding, force bytes-to-string")
                    return str(url_response.read())
        except Exception as e:
            if argss.verbose : print("\033[1;30m[ERROR] \033[0m"+"\033[1;30m"+str(e)+"\033[0m")

            # if argss.verbose : print("\033[1;31m[ERROR]\033[0m unable to connect to the target URL. May be due to a security policy")
            return "NoResponse"

    @staticmethod
    def getallparameter():
        # print("test")
        args2 = argsparse().args()

        argsInUrl = parse.parse_qs(parse.urlparse(args2.url).query)
        argsInPostdata = parse.parse_qs(args2.postdata) if args2.postdata else {}
        argsInCookie = parse.parse_qs(args2.cookie) if args2.cookie else {}
        argsInUsergent = parse.parse_qs(args2.useragent) if args2.useragent else {}
        argsInReferer = parse.parse_qs(args2.referer) if args2.referer else {}
        allargs = {**argsInUrl,**argsInPostdata,**argsInUsergent,**argsInReferer,**argsInCookie}

        return allargs


    def checkurlaccessible(self):
        print("\033[1;32m[INFO]\033[0m testing connection to the target URL")
        if self.responsebyurl("591") =="NoResponse":
            print("\033[1;33m[WARNING] site can't connected\033[0m"+"\033[1;30m (eg.. use -v get information)\033[0m")
            print("exiting...")
            return 0
        else:
            print("\033[1;32m[INFO] site connected success \033[0m ")
            return 1
