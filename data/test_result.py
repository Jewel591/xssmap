urlsuccess = "yes"
urlxssalbe = "yes"
post_url = "url"
get_url = "url"
referer_url="url"
cookie_url="cookie"
post_data = "data"
targeturl = "url"
target_parameter = "var"
targetvarlist = []
HTTP_METHON = "nk"
verbose = "no" # 如果要更详细的输出，可将此处设为 yes

whitelist = {
    'close': [],
    'close_tag': [],
    'action': [],
    'onevent': [],
    'tag': [],
    'others': [],
    'illusion': [],
    'combination_close_no': [],
    'combination_close_yes': []}
blacklist = {
    'close': [],
    'close_tag': [],
    'action': [],
    'onevent': [],
    'tag': [],
    'others': [],
    'illusion': [],
    'combination_close_no': [],
    'combination_close_yes': []}
signal = {
    'close': 'no',
    'close_tag': 'no',
    'action': 'no',
    'onevent': 'no',
    'tag': 'no',
    'others': 'no'}

def urldata_init():
    global urlsuccess
    global HTTP_METHON
    global urlxssalbe
    global post_data
    global post_url
    global get_url
    global whitelist
    global blacklist
    global signal
    global verbose
    urlxssalbe = "yes"
    urlsuccess = "yes"
    targeturl = ""
    HTTP_METHON = "nk"
    post_url = "url"
    post_data = "data"
    get_url = "url"
    whitelist = {
        'close': [],
        'close_tag': [],
        'action': [],
        'onevent': [],
        'tag': [],
        'others': [],
        'illusion': [],
        'combination_close_no': [],
        'combination_close_yes': []}
    blacklist = {
        'close': [],
        'close_tag': [],
        'action': [],
        'onevent': [],
        'tag': [],
        'others': [],
        'illusion': [],
        'combination_close_no': [],
        'combination_close_yes': []}
    signal = {
        'close': 'no',
        'close_tag': 'no',
        'action': 'no',
        'onevent': 'no',
        'tag': 'no',
        'others': 'no'}

