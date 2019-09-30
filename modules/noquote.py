# 重写 requests send 方法，解决 requests 对发送的请求强行 urlencode 的问题

import urllib.parse

import requests


class NoQuoteSession(requests.Session):
    def send(self, prep, **send_kwargs):
        table = {
            urllib.parse.quote('{'): '{',
            urllib.parse.quote('}'): '}',
            urllib.parse.quote(':'): ':',
            urllib.parse.quote(','): ',',
            urllib.parse.quote('<'): '<',
            urllib.parse.quote('>'): '>',
            urllib.parse.quote('"'): '"',
            urllib.parse.quote('`'): '`',
            urllib.parse.quote('/'): '/',
            urllib.parse.quote('\\'): '\\',
            # urllib.parse.quote(' '): '%20',
            # urllib.parse.quote(' '): ' ',
            # urllib.parse.quote('%3e'): '>'
        }
        for old, new in table.items():
            prep.url = prep.url.replace(old, new)
        return super().send(prep, **send_kwargs)