import heapq

class Dijkstra:
    def __init__(self, graph):
        self.graph = graph
        self.n = graph.n

    def solve(self, source):
        dist = [float('inf')] * self.n
        dist[source] = 0
        pq = [(0, source)]

        while pq:
            d, u = heapq.heappop(pq)

            if d > dist[u]:
                continue

            for v, w in self.graph.adj[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    heapq.heappush(pq, (dist[v], v))
        
        return dist
