urlsuccess = "yes"
targeturl = ""
word = ""
HTTP_METHON = "not know"
posturl = "post 请求的 url"
post_data = "post 请求的 data"
get_url = "get 请求的 url"
sensitive = {
    'close': [],
    'close_tag': [],
    'action': [],
    'onevent': [],
    'tag': [],
    'others': [],
    'illusion': [],
    'combination_close_no': [],
    'combination_close_yes': []}
unsensitive = {
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
    global targeturl
    global word
    global HTTP_METHON
    global post_data
    global post_url
    global get_url
    global sensitive
    global unsensitive
    global signal
    urlsuccess = "yes"
    targeturl = ""
    word = ""
    HTTP_METHON = "not know"
    post_url = "post 请求的 url"
    post_data = "post 请求的 data"
    get_url = "get 请求的 url"
    sensitive = {
        'close': [],
        'close_tag': [],
        'action': [],
        'onevent': [],
        'tag': [],
        'others': [],
        'illusion': [],
        'combination_close_no': [],
        'combination_close_yes': []}
    unsensitive = {
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

