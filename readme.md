2019.12.16
新版本正在开发中~~~

--------------------------------------------

介绍：https://zhuanlan.zhihu.com/p/88534569

# 更新
2019/12/20:

大版本更新(v1.2.1)

本次更新完全重构了代码，更新了使用方式（使用大家熟悉的指定args 的方式，不再是交互式获取数据），删除了图形化运行模式，以后都用命令行交互，添加了众多功能：
1. 自定义 Cookie
2. 自定义 Timeout
3. 自定义 UserAgent
4. 指定 http/https 代理
5. 增加了 verbose 模式

2019/10/24:

大版本更新(v1.1.1):
1. 添加功能：若不输出参数，自动对所有参数进行检测
2. 添加功能：增加对 ctrl c 信号捕获，增加暂停机制
3. 优化展示：大幅度调整输出展示信息，更美观、更简洁

# 环境
**请安装 python3.6**，python3.7 字符串转义存在 bug，运行会报错。

# 安装
`
pip3 install -r requirement.txt -i https://pypi.douban.com/simple`

# 使用方法
`python3.6 checkxss.py -h`

![help information](https://i.loli.net/2019/12/20/orA92adSUWv7Ofm.png)

支持 POST 和 GET 请求方法，支持 cookie、referer、useragent 字段中的参数注入检测



# 介绍

1. 支持 url 编码绕过
2. 支持对 HTML 标签属性的值进行 unicode 编码绕过
3. 支持对 HTML 标签属性的值进行 HTML 编码绕过（未上线）
4. 支持对 ( ) ' " 进行灵活替换进行绕过
5. 大小写绕过
### 举个栗子
1. 测试 POST 数据中的 returnUrl 参数：

`python3.6 checkxss.py -u "https://example.com/login.do" --data="returnUrl=utest" -p returnUrl` 

![](https://i.loli.net/2019/12/20/8Nct5Zay3f1RDHz.png)

也可以不使用`-p` 指定参数，checkxss 会自动列出所有参数让你选择，输入*遍历所有参数：

![](https://i.loli.net/2019/12/20/8fNpzW5Z4VuJPmi.png)


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
