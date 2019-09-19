
import requests
import re
import sys
import threading
import time
import subprocess

adminversion1 = adminversion2 = targeturl = ""


class IsUrlOk():
    def refactorurl(self, url):
        global targeturl
        if re.findall("http", url):
            return
        else:
            if re.findall(r":\d?443", url):
                targeturl = "https://" + sys.argv[1]
                print("x443 port find ,try https")
                return
            else:
                targeturl = "http://" + sys.argv[1]
                return

    def isconnected(self, url):
        global connected
        try:
            requests.get(url, verify=False, timeout=3)
            print("url access is normal ...")
        except IOError:
            print("url Unable to access ...")
            sys.exit(0)

    def isurlok(self, url):
        global targeturl
        try:
            targeturl = sys.argv[1]
        except IndexError:
            print("please input url ...")
            sys.exit(0)
        self.refactorurl(targeturl)
        print("Test if the url is  accessible :", targeturl)
        self.isconnected(targeturl)


class GetResponse:
    global targeturl

    def request(self, dsturl):
        try:
            return requests.get(dsturl, verify=False, timeout=5)
        except BaseException:
            return ""

    def getphpmyadmin(self, url):
        return self.request(url).text


class GetVersion:

    def research(self, keyword, dststr):
        try:
            return re.search(keyword, str(dststr)).group()
        except BaseException:
            return ""

    def request(self, dsturl):
        try:
            return requests.get(dsturl, verify=False, timeout=5)
        except IOError:
            return ""

    def getphpversion(self):

        for url in [
                targeturl + "/phpmyadmin/Documentation.html#glossary",
                targeturl + "/Documentation.html#glossary",
                targeturl + "/phpmyadmin/Documentation.html",
                targeturl + "/phpmyadmin/doc/html/index.html"]:
            adminversion = self.research(
                r'phpMyAdmin\s(\d|\.)*( - Documentation)',
                GetResponse.getphpmyadmin(
                    self,
                    url))
            if adminversion:
                print("phpMyAdmin:", adminversion)
                print("getbyurl: ", url)
                adminversion = 0

        for url2 in [
                targeturl,
                targeturl + "/phpmyadmin/index.php",
                targeturl + "/phpMyAdmin/index.php",
                targeturl + "/phpmyadmin/doc/html/index.html",
                targeturl + "/phpmyadmin/Documentation.html#glossary",
                targeturl + "/Documentation.html#glossary",
                targeturl + "/phpmyadmin/Documentation.html"
        ]:
            adminversion2 = self.research(
                r'phpMyAdmin\s(\d|\.)+',
                GetResponse.getphpmyadmin(
                    self,
                    url2))
            if adminversion2:
                print("phpMyAdmin:", adminversion2)
                print("getbyurl: ", url2)
                adminversion2 = 0


if __name__ == '__main__':
    timestart = time.time()
    checkurl = IsUrlOk()
    checkurl.isurlok(targeturl)
    timemiddle = time.time()
    Jewel = GetVersion()
    t = threading.Thread(target=Jewel.getphpversion())
    t.start()
    timeend = time.time()
    print("")
    print("scanned in " + str(timeend - timestart) + " seconds")
