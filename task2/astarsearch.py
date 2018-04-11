import heapq
import math
import binsearch as b
class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        return heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]



def heuristic(nodea, nodeb, nodes, lat, lon, delat, delon, adjlf, whatmetric):
    id= adjlf[nodea].get('node')
    dexa, deya = b.findlatlon(id, nodes, lat, lon, delat, delon)
    id = adjlf[nodeb].get('node')
    dexb, deyb = b.findlatlon(id, nodes, lat, lon, delat, delon)
    tmplat = abs(dexa - dexb)
    tmplon = abs(deya - deyb)
    if whatmetric == 1:
        tmpd = math.sqrt((math.pow(tmplat, 2) + math.pow(tmplon, 2)))
        return tmpd
    if whatmetric == 2:
        tmpd = max(tmplon, tmplat)
        return tmpd
    if whatmetric == 3:
        tmpd = tmplat+tmplon
        return tmpd



def astar(weight, adjs, start, goal, nodes, lat, lon, delat, delon, adjlf, whatmetric):
    q = PriorityQueue()
    q.put(start, 0)
    p = {}
    d = {}
    p[start] = None
    d[start] = 0

    while not q.empty():
        u = q.get()

        if u == goal:
            break

        for v in adjs.get(u):
            new_d = d[u] + weight.get(u.__str__() + ', ' + v.__str__())
            if v not in d or new_d < d[v]:
                d[v] = new_d
                priority = new_d + heuristic(goal, v, nodes, lat, lon, delat, delon, adjlf, whatmetric)
                q.put(v, priority)
                p[v] = u

    return d, p
