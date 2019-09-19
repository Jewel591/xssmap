# 每行增加双引号和逗号

import os

with open('input.txt', 'r') as lines:
     with open('output.txt', 'w') as outfile:
        for line in lines:
            str1 = '"' + line + '",'
            print(str1)
            outfile.write(str1)
