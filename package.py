class Package:
    def __init__(self, package_id, w, h, x=0, y=0):
        self.ID = int(package_id)
        self.W = w
        self.H = h
        self.X = x
        self.Y = y
        self.Rotated = False

    def move_package(self, x, y):
        self.X = x
        self.Y = y

    def change_orientation(self):
        self.W, self.H = self.H, self.W
        self.Rotated = not self.Rotated

    def __repr__(self):
        return f"Pkg(ID={self.ID}, X={self.X}, Y={self.Y}, W={self.W}, H={self.H})"