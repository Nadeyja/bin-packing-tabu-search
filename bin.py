class Bin:
    """
    Klasa reprezentująca kontener (bin), który może pomieścić paczki.

    Atrybuty:
        W (int): Szerokość kontenera.
        H (int): Wysokość kontenera.
        ID (int): Unikalny identyfikator kontenera.
        packages (list): Lista paczek znajdujących się w kontenerze.
    """
    bin_start_id = 0

    def __init__(self, w, h):
        self.W = w
        self.H = h
        self.ID = Bin.bin_start_id
        Bin.bin_start_id += 1
        self.packages = []

    def can_fit(self, package):
        """
        Sprawdza, czy paczka może zmieścić się w kontenerze.
        """
        if package.W > self.W or package.H > self.H:
            return False
        for p in self.packages:
            if not (package.X + package.W <= p.X or package.X >= p.X + p.W or
                    package.Y + package.H <= p.Y or package.Y >= p.Y + p.H):
                return False
        return True

    def place_package(self, package):
        """
        Umieszcza paczkę na pierwszym możliwym wolnym miejscu, z rotacją.
        Zwraca True, jeśli udało się umieścić paczkę, w przeciwnym razie False.
        """
        for rotate in [False, True]:
            if rotate:
                package.change_orientation()
            for x in range(self.W - package.W + 1):
                for y in range(self.H - package.H + 1):
                    package.move_package(x, y)
                    if self.can_fit(package):
                        self.add_package(package)
                        return True
            if rotate:
                package.change_orientation()  #cofniecie rotacji
        return False

    def add_package(self, package):
        self.packages.append(package)

    def remove_package_by_id(self, package_id):
        for p in self.packages:
            if p.ID == package_id:
                self.packages.remove(p)
                return True
        return False

    def __repr__(self):
        return f"Bin({self.ID}, {[p.ID for p in self.packages]})"