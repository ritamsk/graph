import math

def adjDijkstra(n, start, w, weight):
    INF=math.inf
    dist = [INF] * n
    dist[start] = 0
    prev = [None] * n
    used = [False] * n
    min_dist = 0
    min_vertex = start
    while min_dist < INF:
        i = min_vertex
        used[i] = True
        for j in w.get(i):
            if dist[i] + weight.get(i.__str__() + ', ' + j.__str__()) < dist[j]:
                dist[j] = dist[i] + weight.get(i.__str__() + ', ' + j.__str__())
                prev[j] = i
        min_dist = INF
        for i in range(n):
            if not used[i] and dist[i] < min_dist:
                min_dist = dist[i]
                min_vertex = i

    return dist, prev