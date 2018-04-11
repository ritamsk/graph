def binsearch_node(nodes, id):
    left = 0
    right = len(nodes)
    while left != right:
        i = (left + right) // 2
        if id == nodes[i].attrs['id']:
            return i
        elif id < nodes[i].attrs['id']:
            right = i
        else:   
            left = i + 1
    return None


def binsearch(lst, x):
    left = 0
    right = len(lst)
    while left != right:
        i = (left + right) // 2
        if x == lst[i]:
            return i
        elif x < lst[i]:
            right = i
        else:
            left = i + 1
    return None

def findlatlon(i, nodes, lat, lon, delat, delon):
    node = nodes[binsearch_node(nodes, i)]
    y = float(node.attrs["lat"])
    x = float(node.attrs["lon"])
    k = binsearch(lat, y)
    l = binsearch(lon, x)
    dey = delat[k]
    dex = delon[l]
    return dex, dey
