import re
import url_data

def allclear():
    url_data.sensitive = {
        'close': [],
        'close_tag': [],
        'action': [],
        'onevent': [],
        'tag': [],
        'others': [],
        'illusion':[]}
    url_data.unsensitive = {
        'close': [],
        'close_tag': [],
        'action': [],
        'onevent': [],
        'tag': [],
        'others': [],
    'illusion':[]}
    url_data.signal = {
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


def Dividing_line():
    print("———————————————————————————————————————————————")
