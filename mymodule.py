# 队列转换为字符串
import payload
import urldata
import re

keyword={'illusion':""}


def list_to_str(list):
    str1 = [str(i) for i in list]
    return ''.join(str1)

# 队列list每个元素头部增加str,注意必须赋值


def list_add_start(list, str):
    return [str + i for i in list]

def list_delete(list, str):
    mylist = []
    for i in list:
        if re.search(str.lower(), i.lower()):
            pass
        else:
            mylist.append(i)
    return mylist

# 队列list每个元素中 old 替换成 new


def list_replace_two(list, old, new):
    return [str(i).replace(old, new) for i in list]

def iilusion_replace():
    keyword['illusion'] = payload.keyword['illusion']
    # 对"进行替换
    # print(str(str(url_data.unsensitive['close'])))
    print("原始 payload：")
    [print(i) for i in keyword['illusion']]
    # print(url_data.unsensitive['close'])

    # 下面校验标签

    while re.search("<iNpUt>",
                    str(urldata.sensitive['tag'])
                    ):
        # print(str(url_data.sensitive['tag']))
        keyword['illusion'] = list_delete(keyword['illusion'], "input")
        break
    while re.search("<BoDy>",
                    str(urldata.sensitive['tag'])
                    ):
        # print(str(url_data.sensitive['tag']))
        keyword['illusion'] = list_delete(keyword['illusion'], "body")
        break
    while re.search("<ImG>",
                    str(urldata.sensitive['tag'])
                    ):
        # print(str(url_data.sensitive['tag']))
        keyword['illusion'] = list_delete(keyword['illusion'], "img")
        break
    while re.search("<IfrAme>591</IfrAme>",
                    str(urldata.sensitive['tag'])
                    ):
        # print(str(url_data.sensitive['tag']))
        keyword['illusion'] = list_delete(keyword['illusion'], "iframe")
        break
    while re.search("<A>591</A>",
                    str(urldata.sensitive['tag'])
                    ):
        # print(str(url_data.sensitive['tag']))
        keyword['illusion'] = list_delete(keyword['illusion'], "/A")
        break
    print("标签校验：", keyword['illusion'])
    # 下面校验闭合字符
    while not re.search("\"",
            str(urldata.unsensitive['close'])
            ):
        if not re.search(
                "\"",
                str(urldata.unsensitive['close'])) and re.search("'",
                                                                 str(urldata.unsensitive['close'])):
            keyword['illusion']=list_replace_two(keyword['illusion'], "\"", "'")
        else:
            if not re.search(
                    "\"",
                    str(urldata.unsensitive['close'])) and re.search(
                    "%22",
                    str(urldata.unsensitive['close'])):
                keyword['illusion']=list_replace_two(keyword['illusion'], "\"", "%22")
            else:
                if not re.search(
                        str(
                        "\"",urldata.unsensitive['close'])) and re.search("%27",
                                                                          str(urldata.unsensitive['close'])
                                                                          ):
                    keyword['illusion']=list_replace_two(keyword['illusion'], "\"", "%27")
                else:  # 如果找不到代替的字符，就将该 payload 删除

                    keyword['illusion']=list_delete(keyword['illusion'],"\"")
        break
    while not re.search("<",
            str(urldata.unsensitive['close'])
            ):
        if not bool(re.search("<",
                str(urldata.unsensitive['close'])
            )) and bool(re.search("%3c",
                str(urldata.unsensitive['close'])
                )):
            keyword['illusion']=list_replace_two(keyword['illusion'], "<", "%3c")
        else:
            keyword['illusion'] = list_delete(keyword['illusion'], "<")
        break

    while not re.search(
            ">",
            str(urldata.unsensitive['close'])):
        if not re.search(
                ">",
                str(urldata.unsensitive['close'])) and re.search("%3e",
                                                                 str(urldata.unsensitive['close'])
                                                                 ):
            keyword['illusion']=list_replace_two(keyword['illusion'], ">", "%3e")
        else:
            keyword['illusion'] = list_delete(keyword['illusion'], ">")
        break

    while not re.search("/",
            str(urldata.unsensitive['close'])
            ):
        if not re.search("/",
                str(urldata.unsensitive['close'])
                ) and re.search("%2f",
                str(urldata.unsensitive['close'])
                ):
            keyword['illusion']=list_replace_two(keyword['illusion'], "/", "%2f")
        else:
            keyword['illusion'] = list_delete(keyword['illusion'], "/")
        break
    print("闭合字符校验：", keyword['illusion'])

    #下面对 pauload 添加闭合字符
    if urldata.unsensitive['close_tag']:
        keyword['illusion'] = list_add_start(
            keyword['illusion'],
            list_to_str(
                urldata.unsensitive['close_tag']).replace("591", ''))
    print("添加闭合字符串：", keyword['illusion'])

    # 下面校验动作函数
    while re.search("prompt(591)",
            str(urldata.sensitive['action'])
            ):

        if urldata.unsensitive['action']:
            keyword['illusion'] = list_replace_two(keyword['illusion'], "prompt(591)", urldata.unsensitive['action'][0])
        else:
            keyword['illusion'] = list_delete(keyword['illusion'], "prompt(591)")
        break

    print("动作校验：",keyword['illusion'])

if __name__ == '__main__':
    payload.keyword_init()
    # print(list_replace(payload.keyword['others'], "<", "%3c"))
    iilusion_replace()
    print("123:",keyword['illusion'])

    pass

