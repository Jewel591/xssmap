import argparse

class argsparse:
    def args(self):
        parser = argparse.ArgumentParser()
        parser.description="Detect XSS vulnerability in Web Applications "
        parser.add_argument("-u",dest="url",type=str,help="target URL (e.g. \"http://www.site.com/vuln.php?id=1\")",required=True)
        parser.add_argument("-p", dest="parameter", metavar="PARAMETER",help="testable parameter(s)")
        parser.add_argument("--version",action="version", version="checkxss version 0.1.1 ")
        parser.add_argument("--cookie", dest="cookie", help="HTTP cookie header value (e.g. \"PHPSESSID=a8d127e..\")")
        parser.add_argument("--referer", dest="referer", help="HTTP referer header value")
        parser.add_argument("--ua", dest="useragent", help="HTTP useragent header value")
        parser.add_argument("--data", dest="postdata", help=" Data string to be sent through POST ")
        parser.add_argument("--timeout", default=5, help="Connection timeout（default.. 5s）")
        parser.add_argument("--proxy", help="Use a http proxy to connect to the target URL（e.g. \"127.0.0.1:8080\"）")
        parser.add_argument("--random-agent", metavar="", help="Use randomly selected HTTP User-Agent header value")
        parser.add_argument("-v", dest="verbose", action="store_true", help="verbose mode")
        return parser.parse_args()
