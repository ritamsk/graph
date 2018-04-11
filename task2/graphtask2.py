'''
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt


class qraphwin(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.text = 'text'
        self.resize(500, 400)
        self.setWindowTitle('Graph')
        btn = QPushButton('start', self)
        btn.resize(btn.sizeHint())
        btn.move(350, 350)
        self.show()

    def paintEvent(self, event):

        qp = QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()

    def drawText(self, event, qp):

        qp.setPen(QColor(168, 34, 3))
        qp.setFont(QFont('Decorative', 10))
        qp.drawText(event.rect(), Qt.AlignCenter, self.text)

app = QApplication(sys.argv)
ex = qraphwin()
sys.exit(app.exec_())
'''
import bs4
import os
import io
import svgwrite
import csv
import math
import re
import dijkstra
import binsearch as b
import astarsearch as a
import time
import levitq
import random

def idsort(node):
    return node.attrs['id']

def adjsort(adjlist):
    return int(adjlist.get('node'))
print('reading file, please wait')
start=time.time()
source_dir = os.getcwd()
map_file= os.path.join(source_dir, 'map.osm') #'map' - файл с данными
mapparsed = bs4.BeautifulSoup(io.open(map_file, encoding='utf-8'), 'xml')
ways = bs4.BeautifulSoup(io.open(map_file, encoding='utf-8'), 'xml', parse_only=bs4.SoupStrainer('way'))
nodes = mapparsed.findAll('node')

highways = []
hospitals = []

for way in ways:
   #     if way.find('tag', k='addr:street')!=None:
        tag = way.findAll('tag')
        for t in tag:
            if t.attrs['k'] == 'amenity' and t.attrs['v'] == 'hospital':
                hospitals.append(way)

v = ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'unclassified', 'residential', 'service', 'road']

for way in ways:
    tag = way.find('tag', k="highway", v=v)
    if tag != None:
        highways.append(way)

nodes.sort(key=idsort)

lat = []
lon = []

for h in hospitals:
        nd = h.findAll('nd')
        for i in nd:
            node = nodes[b.binsearch_node(nodes, i.attrs["ref"])]
            y = float(node.attrs["lat"])
            lat.append(y)
            x = float(node.attrs["lon"])
            lon.append(x)

for way in highways:
        nd = way.findAll('nd')
        for i in nd:
            node = nodes[b.binsearch_node(nodes, i.attrs["ref"])]
            y = float(node.attrs["lat"])
            lat.append(y)
            x = float(node.attrs["lon"])
            lon.append(x)

lat.sort()
lon.sort()
delat = []
delon = []
#перевод в декартовы координаты
for i in lat:
    latr = (i*math.pi)/180.0
    dey = math.log2(math.tan((math.pi/4.0) + (latr/2.0)))
    delat.append(dey*7000)

for i in lon:
    lonr = ((i*math.pi)/180.0)
    delon.append(lonr*7000)

delat.reverse() #иначе город перевернут по оси Y

print('searching hospitals')
nearway=[]
nearnode=[]
for h in hospitals:
    ndh = h.findAll('nd')
    minlat = 40
    minlon = 60
    mind = math.sqrt((math.pow(minlat, 2) + math.pow(minlon, 2)))
    idofnearway=''
    refofnearnode=''
    street = h.find('tag', k='addr:street')
    for way in highways:
        name = way.find('tag', k='name')
        if name!=None:
            #if name.attrs['v'] == street.attrs['v']:
                ndw = way.findAll('nd')
                for i in ndw:
                        nodew = nodes[b.binsearch_node(nodes, i.attrs["ref"])]
                        for j in ndh:
                            nodeh = nodes[b.binsearch_node(nodes, j.attrs["ref"])]
                            tmplat = abs(float(nodeh.attrs['lat']) - float(nodew.attrs['lat']))
                            tmplon = abs(float(nodeh.attrs['lon']) - float(nodew.attrs['lon']))
                            tmpd = math.sqrt((math.pow(tmplat, 2) + math.pow(tmplon, 2)))
                            if tmpd < mind:
                                minlat = tmplat
                                minlon = tmplon
                                mind = math.sqrt((math.pow(minlat, 2) + math.pow(minlon, 2)))
                                idofnearway = way.attrs['id']
                                refofnearnode = nodew.attrs['id']
    if minlat+minlon!=100:
        nearway.append(ways.find(id=idofnearway))
        nearnode.append(refofnearnode)

print('Where are you?')
print("Input longitude")
lonp = input()
lons = re.split('[, .]', lonp)
while not (len(lons)==2 and lons[0].isdigit() and  lons[1].isdigit() and float(lonp) >= lon[0] and float(lonp) <= lon[len(lon)-1] and len(lons[1])>2):
    print("Input longitude")
    lonp = input()
    lons = re.split('[, .]', lonp)

print("Input latitude")
latp = input()
lats = re.split('[, .]', latp)
while not (len(lats)==2 and lats[0].isdigit() and  lats[1].isdigit() and float(latp) >= lat[0] and float(latp) <= lat[len(lat)-1] and len(lats[1])>2):
    print("Input latitude")
    latp = input()
    lats = re.split('[, .]', latp)

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
        if tmpd<mind:
                minlat = tmplat
                minlon = tmplon
                mind = math.sqrt((math.pow(minlat, 2) + math.pow(minlon, 2)))
                nodep = nodew

dwg = svgwrite.Drawing('graph.svg', profile='tiny')
f = open('adjacency_list.csv', 'w', newline='', encoding='utf-8')
adjacency_list = []
awriter = csv.DictWriter(f, fieldnames=['node', 'adj', 'weight'])

for way in highways:
        points = []
        nd = way.findAll('nd')
        xp = 0
        yp = 0
        ip = 0
        for i in nd:
            dex, dey = b.findlatlon(i.attrs["ref"], nodes, lat, lon, delat, delon)
            points.append([dex, dey])
            if xp != 0 and yp != 0:
                if ip == len(nd)-1:
                    weight = math.sqrt((math.pow((dex-points[ip-1][0]), 2) + math.pow((dey-points[ip-1][1]), 2)))
                    adjacency_list.append({'node': i.attrs["ref"], 'adj': [int(nd[ip-1].attrs["ref"])], 'weight': [weight]})
                else:
                    weight1 = math.sqrt((math.pow((dex-points[ip-1][0]), 2) + math.pow((dey-points[ip-1][1]), 2)))
                    tmpdex, tmpdey = b.findlatlon(nd[ip+1].attrs["ref"], nodes, lat, lon, delat, delon)
                    weight2 = math.sqrt((math.pow((dex-tmpdex), 2) + math.pow((dey-tmpdey), 2)))
                    adjacency_list.append({'node': i.attrs["ref"], 'adj': [int(nd[ip-1].attrs["ref"]), int(nd[ip+1].attrs["ref"])], 'weight': [weight1, weight2]})
            else:
                tmpdex, tmpdey = b.findlatlon(nd[ip + 1].attrs["ref"], nodes, lat, lon, delat, delon)
                weight = math.sqrt((math.pow((dex - tmpdex), 2) + math.pow((dey - tmpdey), 2)))
                adjacency_list.append({'node': i.attrs["ref"], 'adj': [int(nd[ip+1].attrs["ref"])], 'weight': [weight]})
            xp = dex
            yp = dey
            ip += 1
            dwg.add(dwg.circle(center=(dex, dey), r=0.02, fill='purple', stroke='none'))
       # print(points)
        dwg.add(dwg.polyline(points, fill='none', stroke='black', stroke_width=0.01))

for h in hospitals:
    points = []
    nd = h.findAll('nd')
    xp = 0
    yp = 0
    ip = 0
    for i in nd:
        dex, dey = b.findlatlon(i.attrs["ref"], nodes, lat, lon, delat, delon)
        points.append([dex, dey])
        dwg.add(dwg.circle(center=(dex, dey), r=0.02, fill='purple', stroke='none'))
    dwg.add(dwg.polyline(points, fill='none', stroke='blue', stroke_width=0.01))




adjacency_list.sort(key=adjsort)
adjlf=[]
adjlf.append(adjacency_list[0])
nodesfortest=[]
nodesfortest.append(adjacency_list[0].get('node'))
for i in range(1, len(adjacency_list)):
    if int(adjacency_list[i].get('node')) != int(adjlf[len(adjlf)-1].get('node')):
        adjlf.append(adjacency_list[i])
        nodesfortest.append(adjacency_list[i].get('node'))
    else:
        adj = adjlf[len(adjlf)-1].get('adj') + adjacency_list[i].get('adj')
        weight = adjlf[len(adjlf)-1].get('weight') + adjacency_list[i].get('weight')
        dnode = adjlf[len(adjlf)-1].get('node')
        adjlf.pop()
       # nodesfortest.pop(adjacency_list[i].get('node'))
       # nodesfortest.append(dnode)
        adjlf.append({'node': dnode, 'adj': adj, 'weight': weight})

weights={}
adjs={}
nodei={}
for i in range(0, len(adjlf)):
    adj = adjlf[i].get('adj')
    weight = adjlf[i].get('weight')
    node = adjlf[i].get('node')
    awriter.writerow({'node': node, 'adj': adj, 'weight': weight})
    nodei.update({node: i})

for i in range(0, len(adjlf)):
    weight = adjlf[i].get('weight')
    adj = adjlf[i].get('adj')
    tmpadjs = []
    for j in range(0, len(adj)):
        tmpadjs.append(nodei.get(adj[j].__str__()))
        ij = i.__str__() + ', ' + nodei.get(adj[j].__str__()).__str__()
        weights.update({ij: weight[j]})
    adjs.update({i: tmpadjs})

nodeip = nodei.get(nodep.attrs['id'])

f.close()
dwg.viewbox(delon[0], delat[len(delat)-1], delon[len(lon)-1]-delon[0], delat[0]-delat[len(delat)-1])
dwg.save()

print('making dijkstra')
dstart=time.time()
dd, p = dijkstra.adjDijkstra(len(adjlf), nodeip, adjs, weights)
dend=time.time()
dtime=dend-dstart
dpaths = []
for i in range(0, len(nearnode)):
    j = nodei.get(nearnode[i])
    path=[]
    while j is not None:
        path.append(j)
        j = p[j]
    path = path[::-1]
    dpaths.append(path)

mind=1560000
minde=0
countd=0
ddofh=[]
for e in nearnode:
    ei = nodei.get(e)
    ddofh.append(dd[ei])
    if dd[ei]<=mind:
        mind=dd[ei]
        minde=countd
    countd+=1

f = open('pathsd.csv', 'w', newline='', encoding='utf-8')
awriter = csv.DictWriter(f, fieldnames=['node', 'path'])
dwg = svgwrite.Drawing('pathsd.svg', profile='tiny')
points=[]
i=0
for path in dpaths:
    pathcsv=[]
    #print(path)
    for v in path:
        id = adjlf[v].get('node')
        pathcsv.append(id)
        dex, dey = b.findlatlon(id, nodes, lat, lon, delat, delon)
        points.append([dex, dey])
        dwg.add(dwg.circle(center=(dex, dey), r=0.02, fill='purple', stroke='none'))
    awriter.writerow({'node': nearnode[i], 'path': pathcsv})
    i+=1
    dwg.add(dwg.polyline(points, fill='none', stroke='blue', stroke_width=0.01))
    points.clear()

points=[]
xp=0
yp=0
for v in dpaths[minde]:
    id = adjlf[v].get('node')
    dex, dey = b.findlatlon(id, nodes, lat, lon, delat, delon)
    points.append([dex, dey])
    dwg.add(dwg.circle(center=(dex, dey), r=0.02, fill='purple', stroke='none'))
dwg.add(dwg.polyline(points, fill='none', stroke='green', stroke_width=0.03))
#print(nodeip)

for h in hospitals:
    points = []
    nd = h.findAll('nd')

    for i in nd:
        dex, dey = b.findlatlon(i.attrs["ref"], nodes, lat, lon, delat, delon)
        points.append([dex, dey])
        dwg.add(dwg.circle(center=(dex, dey), r=0.02, fill='purple', stroke='none'))
    dwg.add(dwg.polyline(points, fill='none', stroke='red', stroke_width=0.01))

dwg.viewbox(delon[0], delat[len(delat)-1], delon[len(lon)-1]-delon[0], delat[0]-delat[len(delat)-1])
dwg.save()
f.close()

print('making astar')
astarpaths=[]
dastars=[]
astarstart = time.time()
for i in nearnode:
    dastar, astarpath = a.astar(weights, adjs, nodeip, nodei.get(i), nodes, lat, lon, delat, delon, adjlf, 1)
    astarpaths.append(astarpath)
    dastars.append(dastar)
astarend=time.time()
astartime = astarend-astarstart

dwg = svgwrite.Drawing('pathsastar.svg', profile='tiny')
f = open('pathsastar.csv', 'w', newline='', encoding='utf-8')
awriter = csv.DictWriter(f, fieldnames=['node', 'path'])

i=0
points=[]
for path in astarpaths:
    key=path[nodei.get(nearnode[i])]
    pathcsv=[]
    while not key == None:
        id = adjlf[key].get('node')
        pathcsv.append(id)
        dex, dey = b.findlatlon(id, nodes, lat, lon, delat, delon)
        points.append([dex, dey])
        dwg.add(dwg.circle(center=(dex, dey), r=0.02, fill='purple', stroke='none'))
        key=path.get(key)
    pathcsv.reverse()
    awriter.writerow({'node': nearnode[i], 'path': pathcsv})
    i+=1
    dwg.add(dwg.polyline(points, fill='none', stroke='blue', stroke_width=0.01))
    points.clear()

mind=1000
minastar=0
for i in range(0, len(dastars)):
        tmpd = dastars[i].get(nodei.get(nearnode[i]))
        if tmpd<mind:
            mind=tmpd
            minastar=i

key=astarpaths[minastar].get(nodei.get(nearnode[minastar]))
i = 0
while not key == None:
        id = adjlf[key].get('node')
        dex, dey = b.findlatlon(id, nodes, lat, lon, delat, delon)
        points.append([dex, dey])
        dwg.add(dwg.circle(center=(dex, dey), r=0.02, fill='purple', stroke='none'))
        key=astarpaths[minastar].get(key)
        i+=1
dwg.add(dwg.polyline(points, fill='none', stroke='green', stroke_width=0.03))
points.clear()

dwg.viewbox(delon[0], delat[len(delat)-1], delon[len(lon)-1]-delon[0], delat[0]-delat[len(delat)-1])
dwg.save()
f.close()

print('making levit')
levitstart=time.time()
dlevit, plevit=levitq.levitq(nodeip, len(adjlf),  adjs, weights)
levitend=time.time()
levittime=levitend-levitstart
ddlevit=[]
levitpaths=[]
for e in nearnode:
    ei = nodei.get(e)
    ddlevit.append(dlevit[ei])
    node =ei
    levitpath=[]
    while node!=-1:
        levitpath.append(node)
        node = plevit[node]
    levitpath.reverse()
    levitpaths.append(levitpath)

f = open('pathslevit.csv', 'w', newline='', encoding='utf-8')
awriter = csv.DictWriter(f, fieldnames=['node', 'path'])
dwg = svgwrite.Drawing('pathslevit.svg', profile='tiny')

mind=1560000
mindl=0
countd=0
for e in nearnode:
    ei = nodei.get(e)
    if dlevit[ei]<=mind:
        mindist=dlevit[ei]
        mindl=countd
    countd+=1

points=[]
i=0
for path in levitpaths:
    pathcsv=[]
    for v in path:
        id = adjlf[v].get('node')
        pathcsv.append(id)
        dex, dey = b.findlatlon(id, nodes, lat, lon, delat, delon)
        points.append([dex, dey])
        dwg.add(dwg.circle(center=(dex, dey), r=0.02, fill='purple', stroke='none'))
    awriter.writerow({'node': nearnode[i], 'path': pathcsv})
    i+=1
    dwg.add(dwg.polyline(points, fill='none', stroke='blue', stroke_width=0.01))
    points.clear()


for v in levitpaths[mindl]:
    id = adjlf[v].get('node')
    dex, dey = b.findlatlon(id, nodes, lat, lon, delat, delon)
    points.append([dex, dey])
    dwg.add(dwg.circle(center=(dex, dey), r=0.02, fill='purple', stroke='none'))
dwg.add(dwg.polyline(points, fill='none', stroke='green', stroke_width=0.03))

for h in hospitals:
    points = []
    nd = h.findAll('nd')
    for i in nd:
        dex, dey = b.findlatlon(i.attrs["ref"], nodes, lat, lon, delat, delon)
        points.append([dex, dey])
        dwg.add(dwg.circle(center=(dex, dey), r=0.02, fill='purple', stroke='none'))
    dwg.add(dwg.polyline(points, fill='none', stroke='red', stroke_width=0.01))

dwg.viewbox(delon[0], delat[len(delat)-1], delon[len(lon)-1]-delon[0], delat[0]-delat[len(delat)-1])
dwg.save()
f.close()

print('TIMES')
print('d:', dtime, 'sec')
print('astar:', astartime, 'sec')
print('levit:', levittime, 'sec')

print('testing:')
test=random.sample(nodesfortest, 100)
print('testing astar with dif f:')

for wm in range(1, 4):
    astartime = 0
    for nodep in test:
        astarstart = time.time()
        for i in nearnode:
            pathastar, cost = a.astar(weights, adjs, nodeip, nodei.get(i), nodes, lat, lon, delat, delon, adjlf, wm)
        astarend = time.time()
        astartime += astarend - astarstart
    print('astar', wm.__str__()+ ':', astartime / 100, 'sec')

#print(test)
dtime=0
astartime=0
levittime=0
for nodep in test:
    nodeip = nodei.get(nodep)
    dstart=time.time()
    dd, p = dijkstra.adjDijkstra(len(adjlf), nodeip, adjs, weights)
    dend=time.time()
    dtime+=dend-dstart

    astarstart = time.time()
    for i in nearnode:
        dastar, astarpath = a.astar(weights, adjs, nodeip, nodei.get(i), nodes, lat, lon, delat, delon, adjlf, 1)
    astarend=time.time()
    astartime += astarend-astarstart

    levitstart=time.time()
    dlevit, plevit=levitq.levitq(nodeip, len(adjlf),  adjs, weights)
    levitend=time.time()
    levittime += levitend - levitstart
    print("new iterations")

print('results')
print('d:', dtime/100, 'sec')
print('astar:', astartime/100, 'sec')
print('levit:', levittime/100, 'sec')

end=time.time()
print('all time:', (end-start)/60, 'min')
