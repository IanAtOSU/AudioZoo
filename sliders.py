class slider():
    minX = 200
    x = 400
    maxX = 600
    y = 700

    def __init__(self, y, minX, maxX):
        if minX > maxX or minX < 0 or maxX > 900:
            RuntimeError
        self.y = y
        self.minX = minX
        self.maxX = maxX
        self.x = minX + (maxX - minX) / 2

    def set_x(self, x):
        self.x = x
    def set_y(self, y):
        self.y = y

    def get_level(self):
        return self.x - ((self.maxX - self.minX) / 2)