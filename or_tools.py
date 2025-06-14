from matplotlib import pyplot as plt, patches
from ortools.sat.python import cp_model

def or_tools_bpp(packages, bins):
    """
    Bin Packing Problem 2D z wykorzystaniem or-tools.
    """

    #model oparty na ograniczeniach
    model = cp_model.CpModel()

    #liczba kontenerów i paczek
    n_b = len(bins)
    n_p = len(packages)

    #szerokość i wysokość każdego kontenera
    W = [b.W for b in bins]
    H = [b.H for b in bins]

    #maksymalna szerokość i wysokość kontenera (potrzebna do zakresu x i y paczek)
    W_max = max(W)
    H_max = max(H)

    #szerokość i wysokość każdej paczki
    w = [p.W for p in packages]
    h = [p.H for p in packages]

    """
    Zmienne
    """

    #koordynaty x i y każdej paczki (zmienne mają zakres od 0 do rozmiar największego kontenera - rozmiar danej paczki)
    x = [model.NewIntVar(0,W_max-w[i],f'x.{i}') for i in range(n_p)]
    y = [model.NewIntVar(0,H_max-h[i],f'y.{i}') for i in range(n_p)]

    #numer kontenera w którym znajduje się paczka i (dodatkowo wymusza, że każda paczka musi się znajdować w kontenerze)
    b = [model.NewIntVar(0, n_b-1,f'b{i}') for i in range(n_p)]

    #czy paczka i jest obrócona
    rotate = [model.NewBoolVar(f'rotate.{i}') for i in range(n_p)]

    #czy paczka i znajduje się w kontenerze k (package in bin)
    pinb = {(i,k):model.NewBoolVar(f'pinb.{i}.{k}') for i in range(n_p) for k in range(n_b)}

    #czy paczka i znajduje się w tym samym kontenerze co paczka j (package with package)
    pwp = {(i,j):model.NewBoolVar(f"pwp.{i}.{j}") for j in range(n_p) for i in range(j)}

    #czy kontener k jest używany (czy znajduje się w nim przynajmniej jedna paczka)
    u = [model.NewBoolVar(f"u{k}") for k in range(n_b)]

    """
    Ograniczenia
    """

    #ograniczenia koordynat paczki i do rozmiaru kontenera k (tylko jeżeli paczka i znajduje się w kontenerze k)
    for k in range(n_b):
        for i in range(n_p):
            model.Add(b[i] != k).OnlyEnforceIf(pinb[(i, k)].Not())
            model.Add(x[i] <= W[k] - w[i]).OnlyEnforceIf(pinb[(i, k)], ~rotate[i])
            model.Add(y[i] <= H[k] - h[i]).OnlyEnforceIf(pinb[(i, k)], ~rotate[i])
            model.Add(x[i] <= W[k] - h[i]).OnlyEnforceIf(pinb[(i, k)], rotate[i])
            model.Add(y[i] <= H[k] - w[i]).OnlyEnforceIf(pinb[(i, k)], rotate[i])

    #ograniczenia nie nakładania się na siebie paczek w tym samym kontenerze
    for j in range(n_p):
        for i in range(j):
            model.Add(b[i] != b[j]).OnlyEnforceIf(pwp[(i, j)].Not())
            no_overlap = [
                model.NewBoolVar(f'left_{i}_{j}'),
                model.NewBoolVar(f'right_{i}_{j}'),
                model.NewBoolVar(f'above_{i}_{j}'),
                model.NewBoolVar(f'below_{i}_{j}')
            ]
            #przynajmniej jedno z ograniczeń musi mieć miejsce żeby paczki na siebie nie nachodziły
            model.AddAtLeastOne(no_overlap).OnlyEnforceIf(pwp[(i,j)])
            model.Add(x[i] + w[i] <= x[j]).OnlyEnforceIf(no_overlap[0], ~rotate[i],pwp[(i,j)])
            model.Add(x[j] + w[j] <= x[i]).OnlyEnforceIf(no_overlap[1], ~rotate[j],pwp[(i,j)])
            model.Add(y[i] + h[i] <= y[j]).OnlyEnforceIf(no_overlap[2], ~rotate[i],pwp[(i,j)])
            model.Add(y[j] + h[j] <= y[i]).OnlyEnforceIf(no_overlap[3], ~rotate[j],pwp[(i,j)])
            model.Add(x[i] + h[i] <= x[j]).OnlyEnforceIf(no_overlap[0], rotate[i],pwp[(i,j)])
            model.Add(x[j] + h[j] <= x[i]).OnlyEnforceIf(no_overlap[1], rotate[j],pwp[(i,j)])
            model.Add(y[i] + w[i] <= y[j]).OnlyEnforceIf(no_overlap[2], rotate[i],pwp[(i,j)])
            model.Add(y[j] + w[j] <= y[i]).OnlyEnforceIf(no_overlap[3], rotate[j],pwp[(i,j)])

    #jeżeli paczka i jest w kontenerze k to kontener k jest używany
    for k in range(n_b):
        for i in range(n_p):
            model.AddImplication(pinb[(i, k)], u[k])

    #minimalizacja użytych kontenerów
    model.Minimize(sum([u[k] for k in range(n_b)]))
    #solver
    solver = cp_model.CpSolver()
    #czas wykonywania solvera, dłuższy czas = potencjalnie lepsze rozwiązanie
    solver.parameters.max_time_in_seconds = 60.0
    rc = solver.Solve(model)

    #status
    print(rc)
    print(solver.StatusName())

    print(f"Liczba użytych kontenerów:{solver.Value(sum([u[k] for k in range(n_b)]))}")

    #rozmiar kontenera w którym znajduje się paczka i
    r_W = []
    r_H = []
    for i in range(n_p):
        r_W.append(W[solver.Value(b[i])])
        r_H.append(H[solver.Value(b[i])])

    #wyniki
    bins_r = []
    for k in range(n_b):
        bins_r.append(k)
        bins_r[k] = []
        for i in range(n_p):
            if solver.Value(b[i]) == k:
                bins_r[k].append(i)
    p_r_id = []
    p_r_x = []
    p_r_y = []
    p_r_w = []
    p_r_h = []
    p_r_rotate = []
    for i in range(n_p):
        p_r_id.append(i)
        p_r_x.append(solver.Value(x[i]))
        p_r_y.append(solver.Value(y[i]))
        p_r_rotate.append(solver.Value(rotate[i]))
        if p_r_rotate[i]:
            p_r_h.append(w[i])
            p_r_w.append(h[i])
        else:
            p_r_w.append(w[i])
            p_r_h.append(h[i])

    for k in range(n_b):
        print(f"Bin ID{k}:")
        for i in bins_r[k]:
            print(f"Package ID{p_r_id[i]} X={p_r_x[i]}, Y={p_r_y[i]}, W={p_r_w[i]}, H={p_r_h[i]}, Rotated={p_r_rotate[i]}")

    #print(bins_r)
    for k in range(n_b):
        fig, ax = plt.subplots()
        ax.set_title(f"Bin {bins[k].ID}")
        ax.set_xlim(0, W[k])
        ax.set_ylim(0, H[k])
        for i in bins_r[k]:
            rect = patches.Rectangle((p_r_x[i], r_H[i]-p_r_y[i]-p_r_h[i]), p_r_w[i], p_r_h[i], linewidth=1, edgecolor='black', facecolor='skyblue')
            ax.add_patch(rect)
            ax.text(p_r_x[i] + p_r_w[i] / 2, (r_H[i]-p_r_y[i]-p_r_h[i]) + p_r_h[i]/ 2, f"{i}", ha='center', va='center', fontsize=8)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.grid(True)
        plt.show()
