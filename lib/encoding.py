import urllib.parse

def urlencode_list(list):
    list_copy = []
    for str in list:
        list_copy.append(_urlencode_str(str))
    return list_copy

def _urlencode_str(str):
    return urllib.parse.quote(str, 'utf-8')

def urlencode_list_AtoB(list, strA, strB):
    list_copy = []
    for str in list:
        list_copy.append(str.replace(strA, strB))
    return list_copy