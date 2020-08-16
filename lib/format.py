from data import payloads
def breakline():
    print("------------------------------------------------------------")

def payloadReplace(llist,lvar,rvar):
    rlist = []
    for i in llist:
        rlist.append(i.replace(lvar, rvar))
    return rlist