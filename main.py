from package import Package
from bin import Bin
from tabu_search import tabu_search


def check_for_collisions(p1: Package, p2: Package) -> bool:
    if p1.X+p1.W <= p2.X or p1.X >= p2.X+p2.W or p1.Y+p1.H <= p2.Y or p1.Y >= p2.Y+p2.H:
        return False
    else:
        return True

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

#wynik algorytmu i wizualizacja
best_solution = tabu_search(bins, packages)
print("Best solution found:", sum(1 for b in best_solution if b.packages))














