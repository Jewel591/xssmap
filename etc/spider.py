# 本脚本用于获取公司所有人员的邮箱
import requests
import re
import sys
import threading
import time
import subprocess
targeturl="http://10.5.5.23/pages/myspace/myAddressBookList.jsf"
f = open("result.txt","w+")

def request():
    header={'Host': '10.5.5.23',
            'Content-Length': '5670',
            'Origin': 'http://10.5.5.23',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'Referer': 'http://10.5.5.23/pages/myspace/myAddressBookList.jsf',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cookie': 'username=liaolin; remember=; userpassword=; JSESSIONID=B0CD3E933D3D2D87B7783C2136A009FA',
            'Connection': 'close'}

    str1="AJAXREQUEST=j_id_jsp_859067921_0&operate=operate&orderBy=&orderType=&operate%3Aname=&operate%3Anumber=&operate%3Adept=&operate%3Atel=&operate%3Amobile=&operate%3Amail=&operate%3AdTel=&operate%3AdFax=&operate%3Apage="
    str2="&operate%3Aconfig=&javax.faces.ViewState=H4sIAAAAAAAAAN2cX2wcRxnA5y7%2F0zTNv0a0NOWSpnbSXta3e%2F%2FtpImd1MmlZzuyHTdNaJ25u7G9zt3uZnfOPqd%2FSCtBBRW0FS0U0YoKkACRvpQX4IE%2FAqlSpSJRiRceUIWQEBLlAVUq8ADM7N7s7Z139ta9DV1qqZO9vW%2B%2BnfnN930z881eb7wPNtR1sPtScREuQaEKlXlhorSIynjohd9c%2BNYO43A1CkBDAwBkDB0ky2pNMOqKMAfLyBCgplXlMsSyqghTGGI0BhU4j%2FRCTasenNYRGlcr6IO5n%2F7sjcTpn2%2BjepZPAfp3SNXnBbgIG6lFY06Y02ENLav6FfOWMEyKGRktT6oqBnsWZ%2BXK7KKhzebS%2BUQmm5fE2UTDuAqeAtFlyVR2D216o9kk0kBNVZCChQVcqwpnSDGq6jWwSdWQTlrIqmZIxQi4r0vVgqLV8Rm5UkEKWK%2BQVrLquTVX36jUayWk9%2FD8CtIwq55ec%2FV1GFV7aH1NLcnVXujVoFztpfPTqKfqo7DRQ3WNWHUP8MqqMifPdyhocwHT8O3K1ANOqrUaVCpFWbkCNhoI6uWFdrPfbyrQYHkBCbWVZkPqBiYeWpGXhFPyEtiCYamKRtTKCqs6QireCu7t8uxJpCGIwe0uviemmKpRomo7ONyFw0QdExDTqMFRlw5WXcbZ0e09dTTrbNnOri07BxVUPa2rdc1dXc6pblfPHc0H2jop4VS3p9fWSSJTVzDtbQ3qPmWrEyUxlZBSmUxuNqGVpWA1ioFrlALXmAxcYypwjenANWYC15gNXGMucI15h8aza9V4h6uFO51mdC1h312d2NHC%2Fb23UApeZTJ4langhyYdvMpM8CqzwavMBa8y32HmoOfJK2B1yWDVpYJVlw5WXSZYddlg1eWCVZcPVF0yEaw6MVh1wXpFMtmoU3X0L%2Bpytdm%2B2mLoYKeZnKhjmeiGxsIY1DZs%2Bv0vf7X38m%2FXgego2FpVIdnglbGqF8ieZ0FHxoJarTS04ydMFRuXN1OV9AEYHHQ2fBmVoKYJJ89PTj44Pj07U3jw4dnJiYlp%2BvDjGMTcZCfGzk2MU%2BnCqSnStt2ttg3rOlwpygZuPP3uvm%2B8BV9bByIFsN6QryEzg3LX8npS9mGwkRJJpbCdlWC3MtixZ2vezKZ5cYoJZHiRhwlkebGECeR40YEJ5Hn%2B3hTIJXgezAREnk8yAYnnZUwgyfMbJpDieQIT4JBMMpI5DklirQ2Nk4uipjJr26iZQBtR1SqCyjsx%2FfrvXv3X36IgchFsWILVOjGDiOlFl4GmEYVbz0yPFWdHhqcKJ4lhDtAsgzFQWzHIph6Rf4crFWLKBlF3hVqVQJ5MHrSjZXBFtQyr6Kl%2F7Lz8auKff42C9QWweYE4SFmtoCLYVFbrCtaJHe0ys3sDtHEDU1iXlfmhIthMP9bJI2mD5oj4EtRlqGDzY0P7D%2FnDIHpynBTXFjAA7X0sKBjNI33XH1%2F%2F7odPP5uLUktv9pE10ZQbN7NeX7jx8r5bXnrvOZZLvEC6b3v4BnpRMgutdWl%2Fvd0lPOx1hAd6dWyVp0fo7RPml8Pk4zbT9XYwPyOGYKbzMEvLYSu9hs00GWbpLmylrbCVfsJWGglb6SDM0jrYTs80zOafsgtodgRbOFgYodlIzW7XOrNdG0kkQEoZr2hE7QYDr1TNQTnR0Dr%2FMNhekQ2tClcGYwoJuUNOkLe4kIq0SNlX61r3NEeVjjRw01DeeHfmz3%2FZ9%2FhpNnQR3Bzn1iOIZfS5TwdmUvgMicVIn4JLSH%2Fk7R8d%2B%2Bqr74xFQbQItpSr0DDGyTA0LXCrQWQqZh0M9lo2K6sDU4jYZVW%2BRuPiEEFCHtfvyH0tQoMEUQFVhbOGNkNb9mBDo34jqwp85P0%2FJPb8%2BCjNPetk52U2kkh2iC1vvX7pvV%2F8%2B8WoKbbbFmtJfOfzX5r6%2B8V3j5oUyNL1jB9nPSRl4tLhWP89j9dgycqqj5C4IKCatqQK1P6e7CedcSbyVreN5tL3i2df%2BLb8TJR2g7J6eXkAfNpDq9MBLQlNaxDD3dacbgaVJvQlp5nuco6hlbpsGWrEMlT68XkyBpa3atYFdNgg6M0G6dWXmfs%2B7zAxevWi1ZyXlh8CBX%2F8sx78F9VSoUIGgKp8ZTkB7vIS4xHdbhM1wwjVtdxiSotv%2BmZI%2F3ntf4GvAE77w5fzwFfRsA1PAHfyhboaIw28VE%2FjkwMu7wGOTDDdwVEhHrhbGDgiRNWshJ5bEZz1xS2Z8OBmTck2OhHs85Tr6rGWHFV2LfQA%2FU44SdELIFnK2Pi4E4gp1dVnqRRV9Hjo0fm2Pck72Dndlmt7TbnuIW%2Fact0nPjn4kt745mDDFz4q1x0fWYZTVU%2BGHp9vx0254sNQJzuNc0SBl%2BM6pLqi05obvqdCj24MPOQPnfsiG1qiJ809mk1PAnd7C3adNqxNH9X2uaARCq0tsQOc5ni4tdGk311vPRyDgbaDHXv7ZQgdLxJMIoXsxJBOmmKxxmDQfeM2hvCCWmntQqzPI7JSIXvC4QrUMNJbPSCbmAPtm5jO%2BnQX8%2Bzrx3%2Fy2Pc%2BmLA2Y3fYu6xO2TcH3n7uTx%2BmvhJt7na%2BthxbvTgnBn%2ByrutjsGQ82dx0UJMCZLQweID%2FmlJbRzqf3OyYNUKjGsN05TpRbKJuJm%2FsAXV%2BxmC%2FmbobgzJ1SXJ1qF9HczQZ2R%2BPYb2ODg9Zm%2FhOLa2%2Fjm86ns6zmw1uDsfJi0Tp7VZe5EB7SpKTKBRZojCd8TihZzJZjzN3JpPzOEVnMnmPc3GPA%2B5m9UzC48ja4%2BzZ4xCZaRY9joWZDE9P3iGT9Dq6ZUIprwNZJpT3OmlkOdyE19khExK9TgOZkOR1vseEuL1zIMim6Nw0p%2BplVKgUSHCyDhkuR6xU2qhdsEh3wOWlJ3rcMA3nHcGNxszNJbWycqQiLzmSE7vc5i0SvBKrD8Z18yxcOF84BTE044KqH6TXZnrKrLh%2B5ddRsKEINtMKD6EVA4PbrKQVTc4OTCE8VAS32THVrNghMwY1IrNFV5dJ%2FRlo5g%2FmiEaDyrY%2BbzXqZAJoJsacydzmq5qNZqhg7r7NdPcd9JLwXbcEqy0Gm9aaOt1khoitLERwjgpEdlSQ4hwViOyoIM05KhDZUUE63eg8HOKvFjDIuc9gHWk08yN3%2FrIWBy45IPKJTjN0seG%2BNMDgKH%2BycT60oz1sqiFPjgw4LbyPN5dbb2d0TuFXaJ6eP%2FrEEdbLypzqMkNEXUyipwXbIMj5WrCl8nExZa7YaMsuJR61V2d3g62tm7yV2P2uE9Sgq01SumUn3bZUPD2d5C7arD%2FelBsQMhnM%2B0KWTsbFhInsUIzKO5b8sSMxMXY4dl%2Bs%2BQ0tpuRriNy7P0Y8n5RizCY8BvIfWUcAA5KhA4La1s2Rpz%2FiEJgoIw972H4PQS%2FKzmXc3%2BXkHFUm1hC4aONrq0JQywNEjgfQeiaUyHw7x6sWq4jeJRpgVHOh2bpav1ZW9hmWFb05B70iO8dNS%2B6UyJStW8GtwnOXU2DEn7tk42krwJDOklgS238s1o9ozqrf9oQYuN31e7CpZB3fWsY97N%2B4s653c3RMvu6MQTudMch8J1frtDta54ZJueE84It8%2FME7nYunHWylzuDdvMmLFT3jzFM03w8mgvRq6ZwXEiT2vkE6xY0HkRu92nhG7LDxY11s%2FNhNs3GJvgQReaV9UN4MgVEPgbw%2FllJcbM6vH4tVSyJl81YwVh0QOxEMNNmRNWhNVcwPVsItnhNNVm1rBZvYQbCj8yt3brSTIivC0%2FFWJOzseCaeNPuNybrxUr95uwpLqCpgWRP7H20%2F1eMJ8VkkWREeFmUAuSyy2ZYRmG8a0QiTiB0n%2Fw3GDrmsMOkCs315SZaVNrQZMNK7Mj7cNCvCA%2FeH4AdcuGI24UG3veMPkHt9favW9J18jsYcyo53FR90iNuD9Br4YmjaxB%2FrLCvCM9ZHwSA%2FqCRFbljJ%2BgkrWc%2BwkmNFeGjwQ2zOI8Qm%2FbBIerIYZEV4WAggzmWRTnYEAbv%2F%2B8Gtbff5XR5iRXi63FqWre5yPnEzfeEoK8ID4yK4wIEhinEp1TIAR1wkYVeMPfGEM3g2I3H%2FglxB%2FSRQ9rd2AUWQ%2B6gq%2BCQfYMX%2FBUkpnsqHleQJVoSHZBak%2BSTFdNYN5ZHWUu4Q2OP2NR%2FBCCvCnhZsPwvJpL1%2B2ciEMl6%2FVWRCWa9fHzKhnGs6wTzRff5qW04h6pVj7Ae7HRs06wV9wyPZ6KXrXrDTocsg6z7OOF%2B105an2sfZX9pynVKvudh24JZ%2FCPTxLD9NFmqm4ZOm2KZ%2BJ9ho3eClBpLcs9tBruUQ1dHLoQoIEMzyseRFXmglYGgYLKtVVR8sVWH5ytCcquAjy0ieX8CDJbVa6YiwU%2BB4j5qCGohkcyBKoRqIw6CfPxBiLnHzDTTV5FIJFRd%2BokLMecz9jsjlexFwHgz3rIs%2FFY6yIjxs8yDLZytmMq5wnamd%2B8BedwE%2BhjOsCA8GDxPLeyzUw2diZ1kRHrYJIPDZiqmOdLPhsg227vM7XWRFeDqdAhKn01IynpHcDMrueB%2FYtfpLfu%2FHWRGe3vt9sTybjaccKQG9oiF9TtVrUCkjQdWQ4sgKmC%2BWe8hxAYEzduEXEAa31pBSL9RIH8wXSW4yrwkw5otXLhmX2vKJuko7Khjmryit1b4DWRJ8poskH9pZuwiNVU2Cc%2F4opeKSM9PYlBbqpPPNZBL9jaQDVAYc6C7MZ1W0i9CwOg%2Bm%2FLFKx6W0g5WxYji7Ti%2Fp%2F7yRLDIduPLgXl%2FyfGLjdhEaYr6tK9OVGP3Ro7t18YX5rM7ZRWhY%2Bf35Ri4blyQ%2BK4yq7gHeVY5PaNIuQkPoHBj3RyjnaU3W7xgdkFIg1k2Uz2naLkLDyffMZy%2FDXTtvvfviOvNxJPmUZuwiNJQeBZd8Ucon3Gc%2BEmOgjmv01Wnbo5C2oCpO0xoGR9ZUj0%2Fwgl2EhuDD4Lw%2FgmJ7xOKSmIMNB7sh4LcGn9pFuwgNNb9zYl6KSxm%2Bd9IVAf0lnq850SHMZ%2FVZuwgNqxkw7Y9VMp7snBOrFagJEGNd0FRDpj8vKKKltslxEPT5q8Bn9phdrJHZfwHAT6h1SFwAAA%3D%3D&operate%3Asearch=operate%3Asearch&"
    for i in range(1,25):
        postdata = str1+str(i)+str2
        response = requests.post(targeturl,data=postdata, verify=False, headers=header).text
        worker = re.findall("\w*@nsfocus.com|\w*@intra.nsfocus.com",response)
        [print(i,file=f) for i in worker]
    f.close()

if __name__ == '__main__':
    timestart = time.time()
    request()
    timeend = time.time()
    print("")
    print("crash in " + str(timeend - timestart) + " seconds")
