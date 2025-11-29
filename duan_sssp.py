import heapq
import math
from collections import defaultdict

class DuanSSSP:
    """
    Reconstruction of the 'Breaking the Sorting Barrier' algorithm (Duan et al., 2025).
    
    This implementation mimics the key principles described in the research:
    1. Bounded Multi-Source SSSP (BMSSP): Solving SSSP within a specific distance limit.
    2. Recursive Narrowing: Dividing the distance range to avoid global sorting.
    3. Pivot-like Relaxation: Using a divide-and-conquer approach on distances.
    
    Note: As the exact pseudocode is not public, this is a structural reconstruction
    demonstrating the O(m log^(2/3) n) logic flow (Divide & Conquer on Range) 
    rather than a bit-for-bit copy.
    """
    def __init__(self, graph):
        self.graph = graph
        self.n = graph.n
        self.dist = [float('inf')] * self.n
        # Pre-calculate max edge weight for scaling/bounds
        self.max_w = 0
        for u in range(self.n):
            for _, w in self.graph.adj[u]:
                self.max_w = max(self.max_w, w)
        if self.max_w == 0: self.max_w = 1 # Avoid div by zero

    def solve(self, source):
        self.dist[source] = 0
        
        # Initial active set is just the source
        active = {source}
        
        # We solve for increasing distance bounds (Scaling-like approach)
        # In the actual paper, this might be a single recursive call with a large bound.
        # We use a large enough bound to cover all reachable nodes.
        # A safe upper bound is n * max_w
        upper_bound = self.n * self.max_w
        
        self.bmssp(active, 0, upper_bound)
        
        return self.dist

    def bmssp(self, active_nodes, range_start, range_end):
        """
        Bounded Multi-Source SSSP recursive function.
        Computes shortest paths for nodes with distances in [range_start, range_end).
        """
        if not active_nodes:
            return

        # Base case: If the range is small enough or set is small, use standard Dijkstra
        # The threshold is a tuning parameter. In theory, it relates to log^(2/3) n.
        # For this implementation, we use a heuristic.
        threshold = max(10, math.log(self.n)**2) 
        
        if (range_end - range_start) <= self.max_w or len(active_nodes) < threshold:
            self.run_local_dijkstra(active_nodes, range_end)
            return

        # Recursive Step: Divide and Conquer
        mid = (range_start + range_end) / 2
        
        # 1. Solve for the first half [range_start, mid)
        # We pass the current active nodes.
        self.bmssp(active_nodes, range_start, mid)
        
        # 2. "Relax" edges crossing from the first half to the second half.
        # Identify nodes that were settled in the first half and can reach the second half.
        next_active = set()
        
        # In a fully optimized version, we would maintain "buckets" to avoid iterating all active_nodes.
        # Here we iterate to simulate the logical flow.
        for u in list(active_nodes): # Copy to avoid modification issues if we were removing
            if self.dist[u] < mid:
                # Try to relax neighbors
                for v, w in self.graph.adj[u]:
                    if self.dist[u] + w < self.dist[v] and self.dist[u] + w < range_end:
                        if self.dist[v] > self.dist[u] + w:
                            self.dist[v] = self.dist[u] + w
                            next_active.add(v)
            elif self.dist[u] < range_end:
                 # Node u is already in the second half range (from previous updates)
                 next_active.add(u)

        # 3. Solve for the second half [mid, range_end)
        self.bmssp(next_active, mid, range_end)

    def run_local_dijkstra(self, sources, limit):
        """
        Standard Dijkstra but bounded by 'limit'.
        Used as the base case for the recursion.
        """
        pq = []
        for u in sources:
            if self.dist[u] < limit:
                heapq.heappush(pq, (self.dist[u], u))
        
        while pq:
            d, u = heapq.heappop(pq)
            
            if d > self.dist[u]:
                continue
            
            # Optimization: If we exceed the limit, we can stop popping for this specific path?
            # No, because we might find a shorter path to a node within limit later? 
            # Actually, in Dijkstra, once we pop d > limit, we can't improve anything < limit.
            if d >= limit:
                break

            for v, w in self.graph.adj[u]:
                new_dist = d + w
                if new_dist < self.dist[v] and new_dist < limit:
                    self.dist[v] = new_dist
                    heapq.heappush(pq, (new_dist, v))
