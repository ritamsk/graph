import bs4
import os
import io
import svgwrite
import csv
import math
import binsearch as b

def idsort(node):
    return node.attrs['id']

def adjsort(adjlist):
    return int(adjlist.get('node'))

def task2(iftest):
    print('reading file')
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


    if not iftest:
        dwg = svgwrite.Drawing('graph.svg', profile='tiny')
        f = open('adjacency_list.csv', 'w', newline='', encoding='utf-8')
        awriter = csv.DictWriter(f, fieldnames=['node', 'adj', 'weight'])

    adjacency_list = []
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
                if not iftest:
                    dwg.add(dwg.circle(center=(dex, dey), r=0.02, fill='purple', stroke='none'))
           # print(points)
            if not iftest:
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
            if not iftest:
                dwg.add(dwg.circle(center=(dex, dey), r=0.02, fill='purple', stroke='none'))
        if not iftest:
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
        if not iftest:
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
    if not iftest:
        f.close()
        dwg.viewbox(delon[0], delat[len(delat) - 1], delon[len(lon) - 1] - delon[0], delat[0] - delat[len(delat) - 1])
        dwg.save()
    return nodes, adjs, adjlf, weights, nodei, hospitals, nearnode, highways, lat, lon, delat, delon, nodesfortest