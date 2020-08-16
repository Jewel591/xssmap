# 队列转换为字符串
from data import payloads, test_result
import re

payloads={'illusion': ""}


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
    payloads['illusion'] = payloads.payload['illusion']
    # 对"进行替换
    # print(str(str(url_data.unsensitive['close'])))
    print("原始 payload：")
    [print(i) for i in payloads['illusion']]
    # print(url_data.unsensitive['close'])

    # 下面校验标签

    while re.search("<iNpUt>",
                    str(test_result.whitelist['tag'])
                    ):
        # print(str(url_data.sensitive['tag']))
        payloads['illusion'] = list_delete(payloads['illusion'], "input")
        break
    while re.search("<BoDy>",
                    str(test_result.whitelist['tag'])
                    ):
        # print(str(url_data.sensitive['tag']))
        payloads['illusion'] = list_delete(payloads['illusion'], "body")
        break
    while re.search("<ImG>",
                    str(test_result.whitelist['tag'])
                    ):
        # print(str(url_data.sensitive['tag']))
        payloads['illusion'] = list_delete(payloads['illusion'], "img")
        break
    while re.search("<IfrAme>591</IfrAme>",
                    str(test_result.whitelist['tag'])
                    ):
        # print(str(url_data.sensitive['tag']))
        payloads['illusion'] = list_delete(payloads['illusion'], "iframe")
        break
    while re.search("<A>591</A>",
                    str(test_result.whitelist['tag'])
                    ):
        # print(str(url_data.sensitive['tag']))
        payloads['illusion'] = list_delete(payloads['illusion'], "/A")
        break
    print("标签校验：", payloads['illusion'])
    # 下面校验闭合字符
    while not re.search("\"",
            str(test_result.blacklist['close'])
            ):
        if not re.search(
                "\"",
                str(test_result.blacklist['close'])) and re.search("'",
                                                                   str(test_result.blacklist['close'])):
            payloads['illusion']=list_replace_two(payloads['illusion'], "\"", "'")
        else:
            if not re.search(
                    "\"",
                    str(test_result.blacklist['close'])) and re.search(
                    "%22",
                    str(test_result.blacklist['close'])):
                payloads['illusion']=list_replace_two(payloads['illusion'], "\"", "%22")
            else:
                if not re.search(
                        str(
                        "\"", test_result.blacklist['close'])) and re.search("%27",
                                                                             str(test_result.blacklist['close'])
                                                                             ):
                    payloads['illusion']=list_replace_two(payloads['illusion'], "\"", "%27")
                else:  # 如果找不到代替的字符，就将该 payload 删除

                    payloads['illusion']=list_delete(payloads['illusion'], "\"")
        break
    while not re.search("<",
            str(test_result.blacklist['close'])
            ):
        if not bool(re.search("<",
                str(test_result.blacklist['close'])
            )) and bool(re.search("%3c",
                str(test_result.blacklist['close'])
                )):
            payloads['illusion']=list_replace_two(payloads['illusion'], "<", "%3c")
        else:
            payloads['illusion'] = list_delete(payloads['illusion'], "<")
        break

    while not re.search(
            ">",
            str(test_result.blacklist['close'])):
        if not re.search(
                ">",
                str(test_result.blacklist['close'])) and re.search("%3e",
                                                                   str(test_result.blacklist['close'])
                                                                   ):
            payloads['illusion']=list_replace_two(payloads['illusion'], ">", "%3e")
        else:
            payloads['illusion'] = list_delete(payloads['illusion'], ">")
        break

    while not re.search("/",
            str(test_result.blacklist['close'])
            ):
        if not re.search("/",
                str(test_result.blacklist['close'])
                ) and re.search("%2f",
                str(test_result.blacklist['close'])
                ):
            payloads['illusion']=list_replace_two(payloads['illusion'], "/", "%2f")
        else:
            payloads['illusion'] = list_delete(payloads['illusion'], "/")
        break
    print("闭合字符校验：", payloads['illusion'])

    #下面对 pauload 添加闭合字符
    if test_result.blacklist['close_tag']:
        payloads['illusion'] = list_add_start(
            payloads['illusion'],
            list_to_str(
                test_result.blacklist['close_tag']).replace("591", ''))
    print("添加闭合字符串：", payloads['illusion'])

    # 下面校验动作函数
    while re.search("prompt(591)",
            str(test_result.whitelist['action'])
            ):

        if test_result.blacklist['action']:
            payloads['illusion'] = list_replace_two(payloads['illusion'], "prompt(591)", test_result.blacklist['action'][0])
        else:
            payloads['illusion'] = list_delete(payloads['illusion'], "prompt(591)")
        break

    print("动作校验：", payloads['illusion'])

if __name__ == '__main__':
    payloads.keyword_init()
    # print(list_replace(payload.keyword['others'], "<", "%3c"))
    iilusion_replace()
    print("123:", payloads['illusion'])

    pass

