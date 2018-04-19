import svgwrite
import csv
import math
import re
import dijkstra
import binsearch as b
import astarsearch as a
import time
import levit
import task2


start=time.time()
print('starting work, please wait')
nodes, adjs, adjlf, weights, nodei, hospitals, nearnode, highways, lat, lon, delat, delon, nodesfortest = task2.task2(False)
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

nodeip = nodei.get(nodep.attrs['id'])



print('doing dijkstra')
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

print('doing astar')
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

print('doing levit')
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

end=time.time()
print('all time:', (end-start)/60, 'min')
