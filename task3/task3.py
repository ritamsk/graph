import matplotlib.pyplot as plt
import numpy as np
from numpy import sqrt
import task2
import math
import time
import re
import levitq
import svgwrite
import binsearch as b

print('starting work, please wait')
X = [];
Y = [];
nodes, adjs, adjlf, weights, nodei, hospitals, nearnodes, highways, lat, lon, delat, delon, nodesfortest, dwg = task2.task2(
    False)


print('Where is a warehouse?')
print("Input longitude")
lonp = input()
lons = re.split('[, .]', lonp)
while not (len(lons) == 2 and lons[0].isdigit() and lons[1].isdigit() and float(lonp) >= lon[0] and float(lonp) <= lon[
    len(lon) - 1] and len(lons[1]) > 2):
    print("Input longitude")
    lonp = input()
    lons = re.split('[, .]', lonp)

print("Input latitude")
latp = input()
lats = re.split('[, .]', latp)
while not (len(lats) == 2 and lats[0].isdigit() and lats[1].isdigit() and float(latp) >= lat[0] and float(latp) <= lat[
    len(lat) - 1] and len(lats[1]) > 2):
    print("Input latitude")
    latp = input()
    lats = re.split('[, .]', latp)
print('doing something, wait please')
minlat = 40
minlon = 60
mind = math.sqrt((math.pow(minlat, 2) + math.pow(minlon, 2)))
nodep = ''
for way in highways:
    ndw = way.findAll('nd')
    for i in ndw:
        nodew = nodes[b.binsearch_node(nodes, i.attrs["ref"])]
        tmplat = abs(float(latp) - float(nodew.attrs['lat']))
        tmplon = abs(float(lonp) - float(nodew.attrs['lon']))
        tmpd = math.sqrt((math.pow(tmplat, 2) + math.pow(tmplon, 2)))
        if tmpd < mind:
            minlat = tmplat
            minlon = tmplon
            mind = math.sqrt((math.pow(minlat, 2) + math.pow(minlon, 2)))
            nodep = nodew

nodeip = nodei.get(nodep.attrs['id'])
# n=50; m=100; way=[]; a=0
points = []
points.append(nodep.attrs['id'])
points.extend(nearnodes)
n = len(points);
m = len(points);

X = [];
Y = [];

for nearnode in points:
    for node in nodes:
        if nearnode == node.attrs["id"]:
            node = nodes[b.binsearch_node(nodes, nearnode)]
            x, y = b.findlatlon(nearnode, nodes, lat, lon, delat, delon)
            Y.append(y)
            X.append(x)

way = [];
a = 0

# n=len(X)
RS = [];
RW = [];
RIB = []
s = []

print('doing levit')
dds = []
lps=[]
for nearnode in points:
    d, plevit = levitq.levitq(nodei.get(nearnode), len(adjlf), adjs, weights)
    dd = []
    levitpaths=[]
    for e in points:
        ei = nodei.get(e)
        dd.append(d[ei])
        node = ei
        levitpath = []
        while node != -1:
            levitpath.append(node)
            node = plevit[node]
        levitpath.reverse()
        levitpaths.append(levitpath)
    lps.append(levitpaths)
    dds.append(dd)
print('done')
for ib in range(n):
    M = np.zeros([n, n])
    for i in range(n):
        for j in range(n):
            if i != j:
                # M[i,j]=sqrt((X[i]-X[j])**2+(Y[i]-Y[j])**2)
                M[i, j] = dds[i][j]
            else:
                M[i, j] = float('inf')
    way = []
    way.append(ib)
    for i in range(1, n):
                    s = []
                    for j in range(n):
                        s.append(M[way[i - 1], j])
                    way.append(s.index(min(s)))
                    for j in range(i):
                        M[way[i], way[j]] = float('inf')
                        M[way[i], way[j]] = float('inf')
                # S=sum([sqrt((X[way[i]]-X[way[i+1]])**2+(Y[way[i]]-Y[way[i+1]])**2) for i in np.arange(0,n-1,1)])+ sqrt((X[way[n-1]]-X[way[0]])**2+(Y[way[n-1]]-Y[way[0]])**2)
    S = sum([dds[way[i]][way[i + 1]] for i in range(n - 1)]) + dds[way[n - 1]][way[0]]
    RS.append(S)
    RW.append(way)
    RIB.append(ib)

S = min(RS)
way = RW[RS.index(min(RS))]
ib = RIB[RS.index(min(RS))]
X1 = [X[way[i]] for i in range(n)]
Y1 = [Y[way[i]] for i in range(n)]
plt.title('Общий путь-%s.Номер города-%i.Всего городов -%i.n Координаты X,Y заданы' % (round(S, 3), ib, n), size=14)
plt.plot(X1, Y1, color='r', linestyle=' ', marker='o')
plt.plot(X1, Y1, color='b', linewidth=1)
X2 = [X[way[n - 1]], X[way[0]]]
Y2 = [Y[way[n - 1]], Y[way[0]]]
plt.plot(X2, Y2, color='g', linewidth=2, linestyle='-', label='Путь от  последнего n к первому городу')
plt.legend(loc='best')
plt.grid(True)
plt.show()
Z = sqrt((X[way[n - 1]] - X[way[0]]) ** 2 + (Y[way[n - 1]] - Y[way[0]]) ** 2)
Y3 = [sqrt((X[way[i + 1]] - X[way[i]]) ** 2 + (Y[way[i + 1]] - Y[way[i]]) ** 2) for i in range(n - 1)]
X3 = [i for i in range(n - 1)]
plt.title('Пути от города к городу')
plt.plot(X3, Y3, color='b', linestyle=' ', marker='o')
plt.plot(X3, Y3, color='r', linewidth=1, linestyle='-', label='Без учёта замыкающего пути - %s' % str(round(Z, 3)))
plt.legend(loc='best')
plt.grid(True)
plt.show()

print('doing prima')
M = np.zeros([n, n])
for i in range(n):
        for j in range(n):
            if i != j:
                # M[i,j]=sqrt((X[i]-X[j])**2+(Y[i]-Y[j])**2)
                M[i, j] = dds[i][j]
            else:
                M[i, j] = float('inf')
ost = []
used = [False] * n
used[0] = True
tree = []
tree.append(0)
count = 0;
while len(tree) != n:
    min_dist = float('inf')
    for i in tree:
        for j in range(n):
            if not used[j] and M[i][j] < min_dist:
                min_dist = M[i][j]
                u = j
                v = i
    count += min_dist
    used[u] = True
    ost.append(v)
    tree.append(u)

tree.pop(0)
osttreef = {}
osttreeb = {}
for i in range(len(ost)):
    osttreef.setdefault(ost[i], []).append(tree[i])

for i in range(len(tree)):
    osttreeb.setdefault(tree[i], []).append(ost[i])


primapoints = []
primapoints.append(ost[0]);
key = ost[0]
while osttreef.get(key) != None:
    while osttreef.get(key) != None:
        j = osttreef.get(key)[0]
        primapoints.append(j)
        osttreef.get(key).remove(j)
        if (osttreef.get(key) == []):
            osttreef.pop(key, None)
        key = j

    while osttreef.get(key) == None and osttreeb.get(key) != None:
        j = osttreeb.get(key)[0]
        # points.append(j)
        osttreeb.get(key).remove(j)
        if (osttreeb.get(key) == []):
            osttreeb.pop(key, None)
        key = j




primapointsid=[]
for point in primapoints:
    primapointsid.append(points[point])


dwg = svgwrite.Drawing('prima.svg', profile='tiny')

for nearnode in points:
    for node in nodes:
        if nearnode == node.attrs["id"]:
            node = nodes[b.binsearch_node(nodes, nearnode)]
            x, y = b.findlatlon(nearnode, nodes, lat, lon, delat, delon)
            dwg.add(dwg.circle(center=(x, y), r=0.05, fill='purple'))

primapoints.append(ost[0])

for i in range(len(primapoints)-1):
        j = primapoints[i+1]
        p = []
        for v in lps[primapoints[i]][j]:
            id = adjlf[v].get('node')
            dex, dey = b.findlatlon(id, nodes, lat, lon, delat, delon)
            p.append([dex, dey])
            dwg.add(dwg.circle(center=(dex, dey), r=0.02, fill='red', stroke='none'))
        if j==0:
            dwg.add(dwg.polyline(p, fill='none', stroke='black', stroke_width=0.01))
            p.clear()
        else:
            dwg.add(dwg.polyline(p, fill='none', stroke='blue', stroke_width=0.01))
            p.clear()
dwg.viewbox(delon[0], delat[len(delat) - 1], delon[len(lon) - 1] - delon[0], delat[0] - delat[len(delat) - 1])
dwg.save()


dwg = svgwrite.Drawing('task3.svg', profile='tiny')
for nearnode in points:
    for node in nodes:
        if nearnode == node.attrs["id"]:
            node = nodes[b.binsearch_node(nodes, nearnode)]
            x, y = b.findlatlon(nearnode, nodes, lat, lon, delat, delon)
            dwg.add(dwg.circle(center=(x, y), r=0.05, fill='purple'))

way.append(way[0])

for i in range(len(way)-1):
        j = way[i+1]
        p = []
        for v in lps[way[i]][j]:
            id = adjlf[v].get('node')
            dex, dey = b.findlatlon(id, nodes, lat, lon, delat, delon)
            p.append([dex, dey])
            dwg.add(dwg.circle(center=(dex, dey), r=0.02, fill='red', stroke='none'))
        if j == 0:
            dwg.add(dwg.polyline(p, fill='none', stroke='black', stroke_width=0.01))
            p.clear()
        else:
            dwg.add(dwg.polyline(p, fill='none', stroke='blue', stroke_width=0.01))
            p.clear()



dwg.viewbox(delon[0], delat[len(delat) - 1], delon[len(lon) - 1] - delon[0], delat[0] - delat[len(delat) - 1])
dwg.save()
