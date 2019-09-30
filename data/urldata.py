# 创建 url 相关变量，并在每次运行之前初始化

urlsuccess = "yes"
post_url = "post请求的url"
get_url = "get请求的url"
post_data = "post请求的data"
targeturl = "目标链接"
targetvar = "目标参数"
HTTP_METHON = "NotKown" # http 请求方法
verbose = "no" #yes 输出请求详情，no 简化输出

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
    global targetvar
    global HTTP_METHON
    global post_data
    global post_url
    global get_url
    global sensitive
    global unsensitive
    global signal
    global verbose
    urlsuccess = "yes"
    targeturl = ""
    targetvar = ""
    HTTP_METHON = "not know"
    post_url = "post 请求的 url"
    post_data = "post 请求的 data"
    get_url = "get 请求的 url"
    verbose = "no"
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

