import time

localtime = time.asctime( time.localtime(time.time()) )
# print ("本地时间为 :", localtime)

def get_time():
    return (time.strftime("[%H:%M:%S]", time.localtime()))

# print(get_time())

def colour_highlight(input_str):
    return "\033[1m" + str(input_str) + "\033[0m"
def colour_green(input_str):
    return "\033[32m" + str(input_str) + "\033[0m"
def colour_yellow(input_str):
    return "\033[33m" + str(input_str) + "\033[0m"
def colour_blue(input_str):
    return "\033[36m" + str(input_str) + "\033[0m"
def colour_red(input_str):
    return "\033[31m" + str(input_str) + "\033[0m"
def colour_green_highlight(input_str):
    return "\033[1;32m" + str(input_str) + "\033[0m"
