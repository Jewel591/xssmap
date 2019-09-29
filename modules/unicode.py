for s in 'prompt':
    print(hex(ord(s)).replace("0x","\\u00"), end='')

print("\n")

f = u"prompt"
print(f.encode('raw_unicode_escape'))

a ="'"
print(a.isalnum())