# [CheckXSS](https://github.com/Jewel591/CheckXSS.git)



![image.png](https://i.loli.net/2020/04/12/zv9iC3UXGfTutkK.png)

**Detect XSS vulnerability in  Web Applications**

![](https://img.shields.io/badge/version-0.1.1-bule.svg)  ![](https://img.shields.io/badge/python-3.6-bule.svg)  ![](https://img.shields.io/github/license/Jewel591/CheckXSS)



# Installation

```
git clone https://github.com/Jewel591/CheckXSS.git && cd CheckXSS
pip3 install -r requirement.txt -i https://pypi.douban.com/simple
```

# Usage Instructions
`python3.6 checkxss.py -h`

![help information](https://i.loli.net/2019/12/20/orA92adSUWv7Ofm.png)

支持 POST 和 GET 请求方法，支持 cookie、referer、useragent 字段中的参数注入检测

# Contributing
Contributions, issues and feature requests are welcome!
Feel to check [issues page](https://github.com/Jewel591/CheckXSS/issues)

# Author

1. 支持 url 编码绕过
2. 支持对 HTML 标签属性的值进行 unicode 编码绕过
3. 支持对 HTML 标签属性的值进行 HTML 编码绕过（未上线）
4. 支持对 ( ) ' " 进行灵活替换进行绕过
5. 大小写绕过
# License
1. 测试 POST 数据中的 returnUrl 参数：

`python3.6 checkxss.py -u "https://example.com/login.do" --data="returnUrl=utest" -p returnUrl` 

![](https://i.loli.net/2019/12/20/8Nct5Zay3f1RDHz.png)

也可以不使用`-p` 指定参数，checkxss 会自动列出所有参数让你选择，输入*遍历所有参数：

![](https://i.loli.net/2019/12/20/8fNpzW5Z4VuJPmi.png)

