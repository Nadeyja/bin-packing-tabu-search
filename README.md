# 🧠 2D Bin Packing with Tabu Search

This project implements a heuristic-based solution for the **2D Bin Packing Problem** using the **Tabu Search** metaheuristic. It includes support for:

* Non-overlapping rectangular package placement
* Package rotation (90 degrees)
* Bin usage minimization
* Solution visualization with `matplotlib`

---

## 📂 Project Structure

```bash
project/
├── tabu_search.py      # Core algorithm (Tabu Search)
├── bin.py              # Bin logic (container)
├── package.py          # Package logic (rectangles to place)
├── box.py              # [optional base class, if used separately]
├── main.py             # Example use with file input (e.g., M1a.txt)
├── README.md           # This file
└──BinPackingData/      # Example data
    ├── M1a.txt
    ├── M1b.txt
    ├── M1c.txt
    ├── M1d.txt
    └── M1e.txt
```

---

## 📌 Problem Statement

Place a given list of rectangular packages into a limited set of rectangular bins:

* Each bin has width and height
* Each package has width and height (and can be rotated)
* No packages can overlap
* The goal is to use **as few bins as possible**

---

## 🚀 How It Works

### ✴️ `tabu_search()`

A classic Tabu Search that:

* Starts with a greedy "first-fit" placement
* Iteratively explores neighbors (moving packages between bins)
* Avoids cycles using a Tabu list
* Keeps track of the best solution found

### 🧱 `Bin` and `Package`

* `Bin` stores a list of packages and handles placement/collision detection
* `Package` knows its dimensions, position, and rotation

### 📊 Visualization

Using `matplotlib`, each bin and its packages are visualized after optimization. Each package is shown as a rectangle with its ID.

---

## 🧪 Example Usage

```python
from package import Package
from bin import Bin
from tabu_search import tabu_search

bins = [Bin(10, 10) for _ in range(5)]
packages = [Package(i, w, h) for i, (w, h) in enumerate([(3,4), (5,5), (2,2), (4,3)])]

best = tabu_search(bins, packages)
```

---

## 📈 Output Example

After running, the algorithm will:

* Print out where each package was placed
* Show a plot for each used bin with package positions

---

## 📦 Requirements

* Python 3.7+
* matplotlib

Install dependencies:

```bash
pip install matplotlib
```

---

## 📜 License

MIT or educational use — feel free to adapt, cite, or reuse.

---

## 👨‍💻 Author

Created by a students solving 2D bin packing for an project. Contributions welcome!
