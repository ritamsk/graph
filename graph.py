import bs4
import os
import io
import svgwrite
import csv
import math

dwg = svgwrite.Drawing('graph.svg', profile='tiny')
source_dir = "path/to/sourse"

map= os.path.join(source_dir, 'map') #'map' - файл с данными
mapparsed = bs4.BeautifulSoup(io.open(map, encoding='utf-8'), 'xml')
ways = bs4.BeautifulSoup(io.open(map, encoding='utf-8'), 'xml', parse_only=bs4.SoupStrainer('way'))
nodes = mapparsed.findAll('node')

highways = []

v = ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'unclassified', 'residential', 'service', 'road']

for way in ways:
    tag = way.find('tag', k="highway", v=v)
    if tag != None:
        highways.append(way)


def idsort(node):
    return node.attrs['id']


def adjsort(adjlist):
    return int(adjlist.get('node'))


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



nodes.sort(key=idsort)

lat = []
lon = []

for way in highways:
        nd = way.findAll('nd')
        for i in nd:
            node = nodes[binsearch_node(nodes, i.attrs["ref"])]
            y = float(node.attrs["lat"])
            lat.append(y)
            x = float(node.attrs["lon"])
            lon.append(x)


lat.sort()
lon.sort()
delat = []
delon = []

#перевод в декартовы коорлинаты
for i in lat:
    latr = (i*math.pi)/180.0
    dey = math.log2(math.tan((math.pi/4.0) + (latr/2.0)))
    delat.append(dey*7000)


for i in lon:
    lonr = ((i*math.pi)/180.0)
    delon.append(lonr*7000)


delat.reverse() #иначе город перевернут по оси Y
f = open('adjacency_list.csv', 'w', newline='', encoding='utf-8')
adjacency_list = []
awriter = csv.DictWriter(f, fieldnames=['node', 'adj'])

for way in highways:
        points = []
        nd = way.findAll('nd')
        xp = 0
        yp = 0
        ip = 0
        for i in nd:
            node = nodes[binsearch_node(nodes, i.attrs["ref"])]
            y = float(node.attrs["lat"])
            x = float(node.attrs["lon"])
            k = binsearch(lat, y)
            l = binsearch(lon, x)
            dey = delat[k]
            dex = delon[l]
            points.append([dex, dey])
            if xp != 0 and yp != 0:

                if ip == len(nd)-1:
                    adjacency_list.append({'node': i.attrs["ref"], 'adj': [int(nd[ip-1].attrs["ref"])]})
                else:
                    adjacency_list.append({'node': i.attrs["ref"], 'adj': [int(nd[ip - 1].attrs["ref"]), int(nd[ip + 1].attrs["ref"])]})

                xp = x
                yp = y
            else:
                adjacency_list.append({'node': i.attrs["ref"], 'adj': [int(nd[ip + 1].attrs["ref"])]})

            xp = dex
            yp = dey
            ip += 1
            dwg.add(dwg.circle(center=(dex, dey), r=0.02, fill='red', stroke='none'))
        dwg.add(dwg.polyline(points, fill='none', stroke='black', stroke_width=0.01))



adjacency_list.sort(key=adjsort)
adjlf=[]
adjlf.append(adjacency_list[0])

for i in range(1, len(adjacency_list)):
    if int(adjacency_list[i].get('node')) != int(adjlf[len(adjlf)-1].get('node')):
        adjlf.append(adjacency_list[i])
    else:
        adj = adjlf[len(adjlf)-1].get('adj') + adjacency_list[i].get('adj')
        dnode = adjlf[len(adjlf)-1].get('node')
        adjlf.pop()
        adjlf.append({'node': dnode, 'adj': adj})


for node in adjlf:
    awriter.writerow({'node': node.get('node'), 'adj': node.get('adj')})

f.close()
dwg.viewbox(delon[0], delat[len(delat)-1], delon[len(lon)-1]-delon[0], delat[0]-delat[len(delat)-1])
dwg.save()

