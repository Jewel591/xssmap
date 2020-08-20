2020.08.20 update
小 bug 还比较多，最近会抽时间来修改，请保持 update
# XSSMAP

![image.png](https://i.loli.net/2020/08/16/AxjZF1HVKT6RdBD.png)

[![](https://img.shields.io/travis/com/Jewel591/xssmap)](https://travis-ci.com/github/Jewel591/xssmap) [![codecov](https://codecov.io/gh/Jewel591/xssmap/branch/master/graph/badge.svg)](https://codecov.io/gh/Jewel591/xssmap) [![](https://img.shields.io/badge/version-0.1.1-bule.svg)](https://img.shields.io/github/license/Jewel591/xssmap)
[![](https://img.shields.io/badge/python-3.6-bule.svg)](https://www.python.org/) [![](https://img.shields.io/github/license/Jewel591/xssmap)](https://github.com/Jewel591/xssmap/tree/master) ![](https://img.shields.io/github/repo-size/Jewel591/xssmap) 

**检测Web应用程序中的XSS漏洞**

*交互模块参考自 sqlmap，如果你熟悉 sqlmap，那么一定可以轻松上手 xssmap！*

- [英文介绍](https://github.com/Jewel591/xssmap/blob/master/README.md)

## 截图
![image.png](https://i.loli.net/2020/08/16/dAWR9LIlFK2JS1Z.png)

## 快速安装
只需一行代码，就是如此简单:
```
curl -L -s https://raw.githubusercontent.com/Jewel591/xssmap/master/docs/install.sh|bash
```

如果提示网络错误，例如 Connection refused，使用 git clone 安装：

```
git clone -b master https://github.com/Jewel591/xssmap.git
cd xssmap
pip3 install -r requirements.txt
```

## 用法介绍
`python3.6 xssmap.py -h`

![image.png](https://i.loli.net/2020/08/16/ynsxozhfCp2wYLX.png)

支持 POST 和 GET 请求方式，支持 `Cookie`、`Referer`、`UserAgent` 字段的参数注入检测。

例如，测试 POST 数据中的 returnUrl 参数。:

`python3.6 xssmap.py -u "https://example.com/login.do" --data="returnUrl=utest" -p returnUrl` 

不指定参数，默认对所有参数进行测试。

## 功能
1. 支持自动 urlencode 编码
2. 支持自动 unicode 编码
3. 支持自动 HTML 编码
4. 自动灵活替换 `()'"`
5. 智能 Payload 组合

## 贡献

欢迎通过[issues 页面](https://github.com/Jewel591/xssmap/issues) 提交 Contributions、issues 和功能需求！

## 维护者

[@Jewel591](https://github.com/Jewel591)



## License

MIT © Jewel591, Kyle



