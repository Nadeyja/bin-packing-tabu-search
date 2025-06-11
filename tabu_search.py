from copy import deepcopy
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def evaluate_solution(bins):
    """
    Funkcja celu. Zwraca liczbę binów, które zawierają paczki.
    Im mniej binów, tym lepiej.
    """
    return sum(1 for b in bins if b.packages)

def generate_initial_solution(bins, packages):
    """
    Tworzy pierwsze sensowne rozwiązanie.
    Dla każdej paczki próbuje znaleźć pierwszy bin, w którym się mieści (heurystyka: "first-fit")
    """
    bins = deepcopy(bins)
    for p in packages:
        for b in bins:
            if b.place_package(p):
                break
    return bins

def get_neighbors(solution):
    """
    Generuje sąsiednie rozwiązania przez przeniesienie paczki z jednego binu do drugiego,
    rozważając także rotację paczki.
    """
    neighbors = []
    for i, b in enumerate(solution):
        for p in list(b.packages):
            for j, b2 in enumerate(solution):
                if i == j:
                    continue
                for rotated in [False, True]:
                    new_solution = deepcopy(solution)
                    p_copy = deepcopy(p)
                    p_copy.Rotated = rotated
                    if new_solution[i].remove_package_by_id(p.ID):
                        if new_solution[j].place_package(p_copy):
                            neighbors.append(new_solution)
    return neighbors

def visualize_solution(bins):
    """
    Tworzy graficzną reprezentację każdego binu.
    Każdy bin to osobny wykres. Każda paczka to prostokąt z ID wyświetlonym w środku.
    """
    for b in bins:
        fig, ax = plt.subplots()
        ax.set_title(f"Bin {b.ID}")
        ax.set_xlim(0, b.W)
        ax.set_ylim(0, b.H)
        for p in b.packages:
            rect = patches.Rectangle((p.X, p.Y), p.W, p.H, linewidth=1, edgecolor='black', facecolor='skyblue')
            ax.add_patch(rect)
            ax.text(p.X + p.W / 2, p.Y + p.H / 2, f"{p.ID}", ha='center', va='center', fontsize=8)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.grid(True)
        plt.show()

def tabu_search(bins, packages, iterations=100, tabu_size=10, visualize=True):
    """
    Algorytm Tabu Search.

    Tworzy rozwiązanie początkowe (generate_initial_solution).
    Iteracyjnie znajduje lepsze rozwiązania przez przeszukiwanie sąsiedztwa (get_neighbors).
    Unika powtarzania tych samych rozwiązań za pomocą listy tabu.
    Na końcu wypisuje i wizualizuje rozmieszczenie paczek.
    """
    current_solution = generate_initial_solution(bins, packages)
    best_solution = deepcopy(current_solution)
    tabu_list = []
    best_solutions_history = [evaluate_solution(current_solution)]

    for _ in range(iterations):
        neighbors = get_neighbors(current_solution)
        neighbors = [n for n in neighbors if repr(n) not in tabu_list]
        if not neighbors:
            break
        neighbors.sort(key=evaluate_solution)
        current_solution = neighbors[0]
        if evaluate_solution(current_solution) < evaluate_solution(best_solution):
            best_solution = deepcopy(current_solution)
        tabu_list.append(repr(current_solution))
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)
        best_solutions_history.append(evaluate_solution(best_solution))

    #info o rozmieszczeniu paczek
    print("\nRozmieszczenie paczek:")
    for b in best_solution:
        print(f"Bin ID {b.ID}:")
        for p in b.packages:
            print(f"  Package ID {p.ID}: X={p.X}, Y={p.Y}, W={p.W}, H={p.H}, Rotated={p.Rotated}")

    #wizualizacja
    if visualize:
        visualize_solution(best_solution)

    return best_solution, best_solutions_history