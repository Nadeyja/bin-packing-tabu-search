from box import Box

class Bin(Box):
    bin_start_id = 0
    def __init__(self, w, h):
        super().__init__(w, h)
        self.ID = Bin.bin_start_id
        self.packages = []
        Bin.bin_start_id += 1

    def __str__(self):
        return f"ID = {self.ID}, Height = {self.H}, Width = {self.W}"

    def add_package(self, package):
        if self.can_pack_package(package):
            self.packages.append(package)
            return True
        else:
            print("Cannot add package to bin")
            return False

    def get_number_of_packages(self):
        return len(self.packages)

    def reset_bin(self):
        print("Removed " + str(self.get_number_of_packages()) + " packages!")
        self.packages = []

    def can_pack_package(self, package):
        if package.X+package.W>=self.W or package.X<=0 or package.Y+package.H>=self.H or package.Y<=0:
            return False
        else:
            return True


