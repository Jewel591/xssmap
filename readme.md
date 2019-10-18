# 环境
**请安装 python3.6**，python3.7 字符串转义存在 bug，运行会报错。

# 安装
`
pip3 install -r requirement.txt`

# 使用方法
CheckXSS 提供图形化和命令行两种启动方式（图形界面基于 PyQt5）
- 图形化界面启动：`python3.6 checkxss.py -x`
- 命令行模式：`python3.6 checkxss.py`
1. 默认进行请求为 GET ，如果目标参数在 POST 请求中，请使用如下格式输入: url(POST)postdata, 例如：www.example.com/example.do(POST)targatvar=xss
2. 默认不输出测试细节，如果想查看更详细的输出，可在 /data/urldata.py 中修改verbose = "yes"

# 请求方法支持
支持 POST 和 GET 请求的检测，默认请求为 GET ，后续增加 Cookie 和 Referer 检测

# 注意点
1. 使用 Burp Suite 配合进行 url解码
2. 工具不解析执行 JS 代码，不会检测 payload 是否能弹窗，所以仍然存在误报，请手工测试。
3. 如果  ---------组合测试（闭合标签）--------- 有结果，可优先测试该 payload，准确性最高。
# 介绍

1. 支持 url 编码绕过
2. 支持对 HTML 标签属性的值进行 unicode 编码绕过
3. 支持对 HTML 标签属性的值进行 HTML 编码绕过（未上线）
4. 支持对 ( ) ' " 进行灵活替换进行绕过
5. 大小写绕过
### 命令行
![CheckXSSTerminal](https://i.loli.net/2019/10/18/IUTh9cFOPoRNtWe.png)
### 图形化
![CheckXSSGUI.png](https://i.loli.net/2019/09/30/P5g2NWklJ4mEoqF.png)

### 闭合字符
```
1. >
2. <
3. "
4. '
5. /
```

### 动作
```
1. prompt()
2. confirm()
3. alert()
4. window[action]()
5. eval(action)
```
### 事件
```
1. onwheel
2. onclick
3. onmouseover
4. onfocus
5. onload
6. onerror
7. src
8. href=javascript:
9. ontoggle
```
### HTML 标签
```
1. <a>
2. <script>
3. <iframe>
4. <input>
5. <body>
6. <img>
7. <details>
8. <svg>
9. <select>
10. <video>
11. <audio>
12. <textarea> 
```
