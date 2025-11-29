import random
import heapq
import time

class Graph:
    def __init__(self, n, directed=True):
        self.n = n
        self.directed = directed
        self.adj = [[] for _ in range(n)]
        self.edges = []

    def add_edge(self, u, v, w):
        self.adj[u].append((v, w))
        self.edges.append((u, v, w))
        if not self.directed:
            self.adj[v].append((u, w))

def generate_random_graph(n, m, min_w=1, max_w=100, seed=None):
    if seed is not None:
        random.seed(seed)
    
    g = Graph(n, directed=True)
    # Ensure connectivity (simple path 0->1->...->n-1)
    for i in range(n - 1):
        w = random.uniform(min_w, max_w)
        g.add_edge(i, i + 1, w)
    
    # Add remaining edges
    remaining_edges = m - (n - 1)
    for _ in range(remaining_edges):
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v:
            w = random.uniform(min_w, max_w)
            g.add_edge(u, v, w)
            
    return g

def verify_results(dist_ref, dist_test, tolerance=1e-9):
    if len(dist_ref) != len(dist_test):
        return False, "Length mismatch"
    
    for i in range(len(dist_ref)):
        # Handle infinity
        if dist_ref[i] == float('inf'):
            if dist_test[i] != float('inf'):
                return False, f"Mismatch at node {i}: Ref=inf, Test={dist_test[i]}"
        elif dist_test[i] == float('inf'):
             return False, f"Mismatch at node {i}: Ref={dist_ref[i]}, Test=inf"
        elif abs(dist_ref[i] - dist_test[i]) > tolerance:
            return False, f"Mismatch at node {i}: Ref={dist_ref[i]}, Test={dist_test[i]}"
            
    return True, "Match"
