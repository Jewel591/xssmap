2020.08.20 update
There are still a lot of bugs, so I'll take the time to fix them soon, so please keep updating.

# XSSMAP

![image.png](https://i.loli.net/2020/08/16/AxjZF1HVKT6RdBD.png)

[![](https://img.shields.io/travis/com/Jewel591/xssmap)](https://travis-ci.com/github/Jewel591/xssmap) [![codecov](https://codecov.io/gh/Jewel591/xssmap/branch/master/graph/badge.svg)](https://codecov.io/gh/Jewel591/xssmap) [![](https://img.shields.io/badge/version-0.1.1-bule.svg)](https://img.shields.io/github/license/Jewel591/xssmap)
[![](https://img.shields.io/badge/python-3.6-bule.svg)](https://www.python.org/) [![](https://img.shields.io/github/license/Jewel591/xssmap)](https://github.com/Jewel591/xssmap/tree/master) ![](https://img.shields.io/github/repo-size/Jewel591/xssmap) 

**Detect XSS vulnerability in  Web Applications**

*Usage mimics sqlmap, and if you know sqlmap, you can easily handle xssmap!*

- [中文介绍](https://github.com/Jewel591/xssmap/blob/master/docs/README_ZH.md)

## Screenshots
![image.png](https://i.loli.net/2020/08/16/dAWR9LIlFK2JS1Z.png)

## Easy Installation
As simple as below, Just one line of code:
```
curl -L https://raw.githubusercontent.com/Jewel591/xssmap/master/docs/install.sh|bash
```

If you get a network error, such as Connection refused, use git clone to install：

```
git clone -b master https://github.com/Jewel591/xssmap.git
cd xssmap
pip3 install -r requirements.txt
```

## Usage Instructions
`python3.6 xssmap.py -h`

![image.png](https://i.loli.net/2020/08/16/ynsxozhfCp2wYLX.png)

Support POST and GET request methods, support parameter injection detection in cookie, referer, useragent fields
For example, test the returnUrl parameter in POST data:

`python3.6 xssmap.py -u "https://example.com/login.do" --data="returnUrl=utest" -p returnUrl` 


## Features
1. Support url encoding bypass
2. Support unicode encoding of HTML tag attribute value to bypass
3. Support HTML encoding to bypass the HTML tag attribute value
4. Support for flexible replacement of () '"to bypass
5. Case bypass

## Contributing

Contributions, issues and feature requests are welcome!

Feel to check [issues page](https://github.com/Jewel591/xssmap/issues)

thanks for [@dwisiswant0](https://github.com/dwisiswant0)

## Maintainers

[@Jewel591](https://github.com/Jewel591)

## Todo

- [ ] DOM XSS Detect
- [ ] Json XSS Detect


## License

MIT © Jewel591, Kyle



