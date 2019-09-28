import re
import urldata

def allclear():
    urldata.sensitive = {
        'close': [],
        'close_tag': [],
        'action': [],
        'onevent': [],
        'tag': [],
        'others': [],
        'illusion':[],
        'combination_close_no': []}
    urldata.unsensitive = {
        'close': [],
        'close_tag': [],
        'action': [],
        'onevent': [],
        'tag': [],
        'others': [],
        'illusion':[],
        'combination_close_no': []}
    urldata.signal = {
        'close': 'no',
        'close_tag': 'no',
        'action': 'no',
        'onevent': 'no',
        'tag': [],
        'others': 'no'}


def human_read1(list):  # 此方法用于提醒<>都被过滤
    newstr = ""
    for i in list:
        newstr += i
    if not re.search("<|>|%3c|%3e", newstr):
        print("<>都被过滤...")


def breakline():
    print("———————————————————————————————————————————————")
