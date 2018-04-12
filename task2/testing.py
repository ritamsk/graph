import dijkstra
import astarsearch as a
import time
import levitq
import random
import task2

print('starting work, please wait')
start=time.time()
nodes, adjs, adjlf, weights, nodei, hospitals, nearnode, highways, lat, lon, delat, delon, nodesfortest = task2.task2(True)
print('testing:')
test=random.sample(nodesfortest, 100)
print('testing astar with dif f:')

for wm in range(1, 4):
    astartime = 0
    for nodep in test:
        astarstart = time.time()
        for i in nearnode:
            dastar, astarpath = a.astar(weights, adjs, nodei.get(nodep), nodei.get(i), nodes, lat, lon, delat, delon, adjlf, wm)
        astarend = time.time()
        astartime += astarend - astarstart
    print('astar', wm.__str__()+ ':', astartime / 100, 'sec')

print('main testing')
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