import binsearch as b
def levit(start, graph, adjs, w):
    d=[]*graph
    M0=[]
    M11=[]
    M12=[]
    M2=[]
    for u in range(0, graph): #u∈V
        d.append(100000)
    d[start] = 0
    M11.append(start)
    for u in range(0, graph):
        if u!=start:
            M2.append(u)
    while len(M11)!=0 or len(M12)!=0:
        #print(len(M11), len(M12))
        if len(M12)==0:
            u=M11.pop()
        else:
            u=M12.pop()
       # print(len(M11), len(M12))
        #u = (M12=∅ ? M11.pop(): M12.pop())
        for v in adjs.get(u):
            tmp=M2
            tmp.sort()
            M2.sort()
            t=b.binsearch(tmp, v)
            if t!= None:
                    M11.append(v)
                    M2.remove(v)
                    d[v] = min(d[v], d[u] + w.get(u.__str__()+ ', ' +v.__str__()))
            else:
                    tmp=M11
                    #tmp2=M12.copy()
                    #tmp = M11.extend(M12)
                    tmp.sort()
                    t = b.binsearch(tmp, v)
                    if t != None:
                            d[v] = min(d[v], d[u] + w.get(u.__str__()+ ', ' +v.__str__()))
                    else:
                        tmp=M12
                        tmp.sort()
                        t = b.binsearch(tmp, v)
                        if t != None:
                            d[v] = min(d[v], d[u] + w.get(u.__str__() + ', ' + v.__str__()))
                        else:
                            if d[v] > d[u] + w.get(u.__str__()+ ', ' +v.__str__()):
                                M12.append(v)
                                M0.remove(v)
                                d[v] = d[u] + w.get(u.__str__()+ ', ' +v.__str__())
        M0.append(u)
        #print(d)
    return d