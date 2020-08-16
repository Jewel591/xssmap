# XSSMAP

![image.png](https://i.loli.net/2020/08/16/AxjZF1HVKT6RdBD.png)

[![](https://img.shields.io/travis/com/Jewel591/CheckXSS)](https://travis-ci.com/github/Jewel591/CheckXSS) [![codecov](https://codecov.io/gh/Jewel591/CheckXSS/branch/master/graph/badge.svg)](https://codecov.io/gh/Jewel591/CheckXSS) [![](https://img.shields.io/badge/version-0.1.1-bule.svg)](https://img.shields.io/github/license/Jewel591/CheckXSS)
[![](https://img.shields.io/badge/python-3.6-bule.svg)](https://www.python.org/) [![](https://img.shields.io/github/license/Jewel591/CheckXSS)](https://github.com/Jewel591/CheckXSS/tree/master) ![](https://img.shields.io/github/repo-size/Jewel591/CheckXSS) 

**Detect XSS vulnerability in  Web Applications**

## Screenshots
![image.png](https://i.loli.net/2020/08/16/dAWR9LIlFK2JS1Z.png)

## Easy Installation
As simple as below, Just one line of code:
```
curl -L -s https://raw.githubusercontent.com/Jewel591/CheckXSS/master/docs/install.sh|bash
```

## Usage Instructions
`python3.6 checkxss.py -h`

![image.png](https://i.loli.net/2020/08/16/ynsxozhfCp2wYLX.png)

Support POST and GET request methods, support parameter injection detection in cookie, referer, useragent fields
For example, test the returnUrl parameter in POST data:

`python3.6 checkxss.py -u "https://example.com/login.do" --data="returnUrl=utest" -p returnUrl` 


## Features
1. Support url encoding bypass
2. Support unicode encoding of HTML tag attribute value to bypass
3. Support HTML encoding to bypass the HTML tag attribute value
4. Support for flexible replacement of () '"to bypass
5. Case bypass

## Contributing

Contributions, issues and feature requests are welcome!

Feel to check [issues page](https://github.com/Jewel591/CheckXSS/issues)

## Maintainers

[@Jewel591](https://github.com/Jewel591)



## License

MIT © Jewel591, Kyle



