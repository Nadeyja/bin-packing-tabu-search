from box import Box

class Package(Box):
    def __init__(self, package_id, w, h, x = 0, y = 0):
        super().__init__(w, h)
        self.ID = package_id
        self.X = x
        self.Y = y
        self.Rotated = False


    def __str__(self):
        return f"ID = {self.ID}, X coordinate = {self.X}, Y coordinate = {self.Y}, Height = {self.H}, Width = {self.W}, Rotated? = {self.Rotated}"

    def move_package(self, x, y):
        self.X = x
        self.Y = y

    def change_orientation(self):
        self.Rotated = True
        h = self.H
        self.H = self.W
        self.W = h




