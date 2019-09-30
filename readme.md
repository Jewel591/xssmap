# 环境
**请安装 python3.6**，python3.7 字符串转义存在 bug，运行会报错。

# 安装
`
pip3 install -r requirement.txt`

# 介绍

1. 支持 url 编码绕过
2. 支持对 HTML 标签属性的值进行 unicode 编码绕过
3. 支持对 HTML 标签属性的值进行 HTML 编码绕过（未上线）
4. 支持对 ( ) ' " 进行灵活替换进行绕过

### CLOSE
```
1. >
2. <
3. "
4. '
5. /
```

### ACTION
```
1. prompt()
2. confirm()
3. alert()
4. window['ale'+'rt']()
5. eval()
```
### EVENT(后续再增加)
```
1. onwheel
2. onclick
3. onmouseover
4. onfocus
5. onload
6. onerror
7. src
8. href=javascript:
```
### TAG
```
1. <iframe>
2. <a>
3. <script>
4. <input>
5. <body>
6. <img>
```