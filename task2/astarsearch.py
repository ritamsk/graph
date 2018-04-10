import heapq
#import graphs
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


def heuristic(nodea, nodeb, nodes, lat, lon, delat, delon, adjlf):
    id= adjlf[nodea].get('node')
    node = nodes[b.binsearch_node(nodes, id)]
    y = float(node.attrs["lat"])
    x = float(node.attrs["lon"])
    k = b.binsearch(lat, y)
    l = b.binsearch(lon, x)
    deya = delat[k]
    dexa = delon[l]
    id = adjlf[nodeb].get('node')
    node = nodes[b.binsearch_node(nodes, id)]
    y = float(node.attrs["lat"])
    x = float(node.attrs["lon"])
    k = b.binsearch(lat, y)
    l = b.binsearch(lon, x)
    deyb = delat[k]
    dexb = delon[l]
    return abs(dexa - dexb) + abs(deya - deyb)


def astar(cost, neighbors, start, goal, nodes, lat, lon, delat, delon, adjlf):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in neighbors.get(current):
            new_cost = cost_so_far[current] + cost.get(current.__str__() + ', ' + next.__str__())
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next, nodes, lat, lon, delat, delon, adjlf)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far