import math

def adjDijkstra(n, start, adjs, weight):
    INF=math.inf
    d = [INF] * n
    d[start] = 0
    p = [None] * n
    seen = [False] * n
    min_d = 0
    min_node = start
    while min_d < INF:
        i = min_node
        seen[i] = True
        for j in adjs.get(i):
            if d[i] + weight.get(i.__str__() + ', ' + j.__str__()) < d[j]:
                d[j] = d[i] + weight.get(i.__str__() + ', ' + j.__str__())
                p[j] = i
        min_dist = INF
        for i in range(n):
            if not seen[i] and d[i] < min_d:
                min_d = d[i]
                min_node = i

    return d, p
