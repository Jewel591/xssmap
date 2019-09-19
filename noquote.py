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
            # urllib.parse.quote(' '): ' ',
            # urllib.parse.quote('%3e'): '>'
        }
        for old, new in table.items():
            prep.url = prep.url.replace(old, new)
        # print("+++正在测试：", prep.url)
        return super().send(prep, **send_kwargs)