import time
import csv
import tracemalloc
from package import Package
from bin import Bin
from tabu_search import tabu_search

#inicjalizacja binow i paczek
bins = []
packages = []

#odczyt danych z pliku
f = open("BinPackingData\M1a.txt")
n = int(f.readline().strip())
print(n)
for i in range(n):
    a = f.readline().strip().split(" ")
    for j in range(int(a[2])):
        b = Bin(int(a[0]),int(a[1]))
        print(b)
        bins.append(b)
f.readline()
m = int(f.readline().strip())
print(m)
for i in range(m):
    a = f.readline().strip().split(" ")
    p = Package(a[0], int(a[1]), int(a[2]))
    print(p)
    packages.append(p)
f.close()

results = []
for iterations in [10,20,30,40,50]:
    for tabu_size in [4,8,12,16,20]:
        times = []
        solutions = []
        for run in range(1): #stabilność wyników
            bins_copy = [Bin(b.W, b.H) for b in bins]
            start = time.time()
            best_solution, _ = tabu_search(bins_copy, packages, iterations=iterations, tabu_size=tabu_size, visualize=False)
            elapsed = time.time() - start
            times.append(elapsed)
            solutions.append(sum(1 for b in best_solution if b.packages))
        results.append({
            'iterations': iterations,
            'tabu_size': tabu_size,
            'avg_time': sum(times)/len(times),
            'avg_bins': sum(solutions)/len(solutions),
        })

#zapisywanie do CSV
with open('tabu_search_results_n.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)