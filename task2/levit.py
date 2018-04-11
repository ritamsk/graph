import collections
def levitq(start, graph, adjs, w):
    d = [100000] * graph
    d[start] = 0
    state=[2]*graph
    state[start] = 1
    q = collections.deque()
    q.append(start)
    p=[-1]*graph

    while len(q)!=0:
        node = q.popleft()
        state[node] = 0
        for i in adjs.get(node):
            weight = w.get(node.__str__()+ ', ' +i.__str__())
            if (d[i] > d[node] + weight):
                d[i] = d[node] + weight
                if state[i] == 2:
                    q.append(i)
                elif state[i] == 0:
                    q.appendleft(i)
                p[i] = node
                state[i] = 1

    return d, p
