import argparse
import time
import random
from graph_utils import generate_random_graph, verify_results
from dijkstra_baseline import Dijkstra
from duan_sssp import DuanSSSP

def run_correctness(n_trials=10, n_nodes=100, n_edges=500):
    print(f"Running {n_trials} correctness tests (N={n_nodes}, M={n_edges})...")
    passed = 0
    for i in range(n_trials):
        seed = random.randint(0, 10000)
        g = generate_random_graph(n_nodes, n_edges, seed=seed)
        
        # Run Dijkstra
        dijkstra = Dijkstra(g)
        dist_ref = dijkstra.solve(0)
        
        # Run DuanSSSP
        duan = DuanSSSP(g)
        dist_test = duan.solve(0)
        
        match, msg = verify_results(dist_ref, dist_test)
        if match:
            passed += 1
            print(f"Test {i+1}: PASS")
        else:
            print(f"Test {i+1}: FAIL - {msg}")
            print(f"  Seed: {seed}")
            
    print(f"Correctness: {passed}/{n_trials} passed.")

def run_benchmark(sizes=[(1000, 5000), (5000, 25000), (1000000, 5000000)]):
    print(f"{'N':<10} {'M':<10} {'Dijkstra (s)':<15} {'DuanSSSP (s)':<15} {'Speedup':<10}")
    print("-" * 60)
    
    for n, m in sizes:
        g = generate_random_graph(n, m, seed=42)
        
        # Benchmark Dijkstra
        start = time.time()
        dijkstra = Dijkstra(g)
        dijkstra.solve(0)
        time_d = time.time() - start
        
        # Benchmark DuanSSSP
        start = time.time()
        duan = DuanSSSP(g)
        duan.solve(0)
        time_s = time.time() - start
        
        speedup = time_d / time_s if time_s > 0 else 0.0
        print(f"{n:<10} {m:<10} {time_d:<15.4f} {time_s:<15.4f} {speedup:<10.2f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["correctness", "benchmark"], default="correctness")
    args = parser.parse_args()
    
    if args.mode == "correctness":
        run_correctness()
    else:
        run_benchmark()
