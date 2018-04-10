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
import levit
start=time.time()
dwg = svgwrite.Drawing('graph.svg', profile='tiny')
source_dir = os.getcwd()
map_file= os.path.join(source_dir, 'map.osm') #'map' - файл с данными
mapparsed = bs4.BeautifulSoup(io.open(map_file, encoding='utf-8'), 'xml')
ways = bs4.BeautifulSoup(io.open(map_file, encoding='utf-8'), 'xml', parse_only=bs4.SoupStrainer('way'))
nodes = mapparsed.findAll('node')
relations =bs4.BeautifulSoup(io.open(map_file, encoding='utf-8'), 'xml',  parse_only=bs4.SoupStrainer('relation'))
highways = []
hospitals = []
count = 0
for way in ways:
   #     if way.find('tag', k='addr:street')!=None:
        tag = way.findAll('tag')
        for t in tag:
            if t.attrs['k'] == 'amenity' and t.attrs['v'] == 'hospital': #and count<10:
                hospitals.append(way)
                count += 1

v = ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'unclassified', 'residential', 'service', 'road']

for way in ways:
    tag = way.find('tag', k="highway", v=v)
    if tag != None:
        highways.append(way)



def idsort(node):
    return node.attrs['id']


def adjsort(adjlist):
    return int(adjlist.get('node'))






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




nearway=[]
nearnode=[]
for h in hospitals:
    ndh = h.findAll('nd')
    minlat = 40
    minlon = 60
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
                            mind = math.sqrt((math.pow(minlat, 2) + math.pow(minlon, 2)))
                            if tmpd < mind:
                                minlat = tmplat
                                minlon = tmplon
                                idofnearway = way.attrs['id']
                                refofnearnode = nodew.attrs['id']
    if minlat+minlon!=100:
        nearway.append(ways.find(id=idofnearway))
        nearnode.append(refofnearnode)
    #print(minlat, minlon)
    #print(nearway[len(nearway)-1])

#print(len(nearway), len(hospitals))
#for way in nearway:
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
#print(lat[0], lat[len(lat)-1])
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

#print(latp, lonp)


minlat = 40
minlon = 60
nodep = ''
for way in highways:
    ndw = way.findAll('nd')
    for i in ndw:
        nodew = nodes[b.binsearch_node(nodes, i.attrs["ref"])]
        for j in ndh:
            nodeh = nodes[b.binsearch_node(nodes, j.attrs["ref"])]
            tmplat = abs(float(latp) - float(nodew.attrs['lat']))
            tmplon = abs(float(lonp) - float(nodew.attrs['lon']))
            tmpd = math.sqrt((math.pow(tmplat, 2) + math.pow(tmplon, 2)))
            mind = math.sqrt((math.pow(minlat, 2) + math.pow(minlon, 2)))
            if tmpd<mind:
                minlat = tmplat
                minlon = tmplon
                nodep = nodew

#print(nodep)
f = open('adjacency_list.csv', 'w', newline='', encoding='utf-8')
adjacency_list = []
awriter = csv.DictWriter(f, fieldnames=['node', 'adj', 'weight'])

for way in highways:
#nearwaycount=0;
#for way in nearway:
        points = []
        nd = way.findAll('nd')
        xp = 0
        yp = 0
        ip = 0
        for i in nd:
            node = nodes[b.binsearch_node(nodes, i.attrs["ref"])]
            y = float(node.attrs["lat"])
            x = float(node.attrs["lon"])
            k = b.binsearch(lat, y)
            l = b.binsearch(lon, x)
            dey = delat[k]
            dex = delon[l]
            points.append([dex, dey])
            if xp != 0 and yp != 0:

                if ip == len(nd)-1:
                    weight = math.sqrt((math.pow((dex-points[ip-1][0]), 2) + math.pow((dey-points[ip-1][1]), 2)))
                    adjacency_list.append({'node': i.attrs["ref"], 'adj': [int(nd[ip-1].attrs["ref"])], 'weight': [weight]})
                else:
                    weight1 = math.sqrt((math.pow((dex-points[ip-1][0]), 2) + math.pow((dey-points[ip-1][1]), 2)))
                    tmpnode = nodes[b.binsearch_node(nodes, nd[ip+1].attrs["ref"])]
                    tmpy = float(tmpnode.attrs["lat"])
                    tmpx = float(tmpnode.attrs["lon"])
                    tmpk = b.binsearch(lat, tmpy)
                    tmpl = b.binsearch(lon, tmpx)
                    tmpdey = delat[tmpk]
                    tmpdex = delon[tmpl]
                    weight2 = math.sqrt((math.pow((dex-tmpdex), 2) + math.pow((dey-tmpdey), 2)))
                    adjacency_list.append({'node': i.attrs["ref"], 'adj': [int(nd[ip-1].attrs["ref"]), int(nd[ip+1].attrs["ref"])], 'weight': [weight1, weight2]})

                xp = x
                yp = y
            else:
                tmpnode = nodes[b.binsearch_node(nodes, nd[ip + 1].attrs["ref"])]
                tmpy = float(tmpnode.attrs["lat"])
                tmpx = float(tmpnode.attrs["lon"])
                tmpk = b.binsearch(lat, tmpy)
                tmpl = b.binsearch(lon, tmpx)
                tmpdey = delat[tmpk]
                tmpdex = delon[tmpl]
                weight = math.sqrt((math.pow((dex - tmpdex), 2) + math.pow((dey - tmpdey), 2)))
                adjacency_list.append({'node': i.attrs["ref"], 'adj': [int(nd[ip+1].attrs["ref"])], 'weight': [weight]})

            xp = dex
            yp = dey
            ip += 1
            dwg.add(dwg.circle(center=(dex, dey), r=0.02, fill='purple', stroke='none'))
       # print(points)
        dwg.add(dwg.polyline(points, fill='none', stroke='black', stroke_width=0.01))



#hospitals.pop(9)
#print(len(hospitals))
for h in hospitals:
    points = []
    nd = h.findAll('nd')
    xp = 0
    yp = 0
    ip = 0
    for i in nd:
        node = nodes[b.binsearch_node(nodes, i.attrs["ref"])]
        y = float(node.attrs["lat"])
        x = float(node.attrs["lon"])
        k = b.binsearch(lat, y)
        l = b.binsearch(lon, x)
        dey = delat[k]
        dex = delon[l]
        points.append([dex, dey])
        dwg.add(dwg.circle(center=(dex, dey), r=0.02, fill='purple', stroke='none'))
    dwg.add(dwg.polyline(points, fill='none', stroke='blue', stroke_width=0.01))


adjacency_list.sort(key=adjsort)
adjlf=[]
adjlf.append(adjacency_list[0])

for i in range(1, len(adjacency_list)):
    if int(adjacency_list[i].get('node')) != int(adjlf[len(adjlf)-1].get('node')):
        adjlf.append(adjacency_list[i])
    else:
        adj = adjlf[len(adjlf)-1].get('adj') + adjacency_list[i].get('adj')
        weight = adjlf[len(adjlf)-1].get('weight') + adjacency_list[i].get('weight')
        dnode = adjlf[len(adjlf)-1].get('node')
        adjlf.pop()
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

#print(nodei)
for i in range(0, len(adjlf)):
    weight = adjlf[i].get('weight')
    adj = adjlf[i].get('adj')
    tmpadjs = []
    for j in range(0, len(adj)):
        tmpadjs.append(nodei.get(adj[j].__str__()))
        ij = i.__str__() + ', ' + nodei.get(adj[j].__str__()).__str__()
        weights.update({ij: weight[j]})
    adjs.update({i: tmpadjs})

f.close()
dwg.viewbox(delon[0], delat[len(delat)-1], delon[len(lon)-1]-delon[0], delat[0]-delat[len(delat)-1])
dwg.save()

nodeip = nodei.get(nodep.attrs['id'])

dstart=time.time()
dist, prev = dijkstra.adjDijkstra(len(adjlf), nodeip, adjs, weights)
paths = []
f = open('pathsd.csv', 'w', newline='', encoding='utf-8')
awriter = csv.DictWriter(f, fieldnames=['node', 'path'])
for i in range(0, len(nearnode)):
    j = nodei.get(nearnode[i])
    path=[]
    while j is not None:
        path.append(j)
        j = prev[j]
    path = path[::-1]
    paths.append(path)

    #print(path)
dend=time.time()
dtime=dend-dstart
mindist=1560000
mindiste=0
countdist=0
ddist=[]
for e in nearnode:
    ei = nodei.get(e)
    ddist.append(dist[ei])
    #print(dist[ei])
    if dist[ei]<=mindist:
        mindist=dist[ei]
        mindiste=countdist
    countdist+=1

#print(mindist, mindiste, len(paths))

points=[]
dwg = svgwrite.Drawing('pathsd.svg', profile='tiny')
i=0
for path in paths:
    pathcsv=[]
    #print(path)
    for v in path:
        id = adjlf[v].get('node')
        pathcsv.append(id)
        node = nodes[b.binsearch_node(nodes, id)]
        y = float(node.attrs["lat"])
        x = float(node.attrs["lon"])
        k = b.binsearch(lat, y)
        l = b.binsearch(lon, x)
        dey = delat[k]
        dex = delon[l]
        points.append([dex, dey])
        dwg.add(dwg.circle(center=(dex, dey), r=0.02, fill='purple', stroke='none'))
    awriter.writerow({'node': nearnode[i], 'path': pathcsv})
    i+=1
    dwg.add(dwg.polyline(points, fill='none', stroke='blue', stroke_width=0.01))
    points.clear()
f.close()
points=[]
xp=0
yp=0
for v in paths[mindiste]:
    id = adjlf[v].get('node')
    node = nodes[b.binsearch_node(nodes, id)]
    y = float(node.attrs["lat"])
    x = float(node.attrs["lon"])
    k = b.binsearch(lat, y)
    l = b.binsearch(lon, x)
    dey = delat[k]
    dex = delon[l]
    points.append([dex, dey])
    dwg.add(dwg.circle(center=(dex, dey), r=0.02, fill='purple', stroke='none'))
dwg.add(dwg.polyline(points, fill='none', stroke='green', stroke_width=0.03))
#print(nodeip)

for h in hospitals:
    points = []
    nd = h.findAll('nd')

    for i in nd:
        node = nodes[b.binsearch_node(nodes, i.attrs["ref"])]
        y = float(node.attrs["lat"])
        x = float(node.attrs["lon"])
        k = b.binsearch(lat, y)
        l = b.binsearch(lon, x)
        dey = delat[k]
        dex = delon[l]
        points.append([dex, dey])
        dwg.add(dwg.circle(center=(dex, dey), r=0.02, fill='purple', stroke='none'))
    dwg.add(dwg.polyline(points, fill='none', stroke='red', stroke_width=0.01))

dwg.viewbox(delon[0], delat[len(delat)-1], delon[len(lon)-1]-delon[0], delat[0]-delat[len(delat)-1])
dwg.save()
pathastars=[]
costs=[]
astarstart = time.time()
for i in nearnode:
    pathastar, cost = a.astar(weights, adjs, nodeip, nodei.get(i), nodes, lat, lon, delat, delon, adjlf)
    pathastars.append(pathastar)
    costs.append(cost)
astarend=time.time()
astartime = astarend-astarstart
points=[]
dwg = svgwrite.Drawing('pathsastar.svg', profile='tiny')
i=0
f = open('pathsastar.csv', 'w', newline='', encoding='utf-8')
awriter = csv.DictWriter(f, fieldnames=['node', 'path'])
for path in pathastars:
    #pathkeys.reverse()
    key=path[nodei.get(nearnode[i])]
    pathcsv=[]
    while not key == None:
    #for v in keys:
        id = adjlf[key].get('node')
        pathcsv.append(id)
        node = nodes[b.binsearch_node(nodes, id)]
        y = float(node.attrs["lat"])
        x = float(node.attrs["lon"])
        k = b.binsearch(lat, y)
        l = b.binsearch(lon, x)
        dey = delat[k]
        dex = delon[l]
        points.append([dex, dey])
        dwg.add(dwg.circle(center=(dex, dey), r=0.02, fill='purple', stroke='none'))
        key=path.get(key)
    pathcsv.reverse()
    awriter.writerow({'node': nearnode[i], 'path': pathcsv})
    i+=1
    dwg.add(dwg.polyline(points, fill='none', stroke='blue', stroke_width=0.01))
    points.clear()
f.close()
mincost=1000
minastar=0
for i in range(0, len(costs)):
        tmpcost = costs[i].get(nodei.get(nearnode[i]))
        if tmpcost<mincost:
            mincost=tmpcost
            minastar=i

key=pathastars[minastar].get(nodei.get(nearnode[minastar]))
i = 0
while not key == None:
        id = adjlf[key].get('node')
        node = nodes[b.binsearch_node(nodes, id)]
        y = float(node.attrs["lat"])
        x = float(node.attrs["lon"])
        k = b.binsearch(lat, y)
        l = b.binsearch(lon, x)
        dey = delat[k]
        dex = delon[l]
        points.append([dex, dey])
        dwg.add(dwg.circle(center=(dex, dey), r=0.02, fill='purple', stroke='none'))
        key=pathastars[minastar].get(key)
        i+=1
dwg.add(dwg.polyline(points, fill='none', stroke='green', stroke_width=0.03))
points.clear()

dwg.viewbox(delon[0], delat[len(delat)-1], delon[len(lon)-1]-delon[0], delat[0]-delat[len(delat)-1])
dwg.save()
nearnodei=[]
for e in nearnode:
    ei = nodei.get(e)
    nearnodei.append(ei)

startlevit=time.time()
dlevit=levit.levit(nodeip, len(adjlf),  adjs, weights)
endlevit=time.time()
levittime=endlevit-startlevit
ddlevit=[]
for e in nearnode:
    ei = nodei.get(e)
    ddlevit.append(dlevit[ei])
print(ddist)
print(ddlevit)
print('astar:', astartime)
print('d:', dtime)
print('levit:', levittime)
end=time.time()
print('all:', (end-start)/60)