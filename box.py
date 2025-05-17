class Box:

    def __init__(self, w, h):
        super().__init__()
        self.H = h
        self.W = w

    def can_fit(self, package):
        #sprawdzenie czy paczka zmiesci sie w binie i nie koliduje z innymi
        if package.W > self.width or package.H > self.height:
            return False
        for p in self.packages:
            if not (package.X + package.W <= p.X or package.X >= p.X + p.W or
                    package.Y + package.H <= p.Y or package.Y >= p.Y + p.H):
                return False
        return True

    def add_package(self, package):
        self.packages.append(package)

    def remove_package(self, package):
        if package in self.packages:
            self.packages.remove(package)



