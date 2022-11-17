

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"<Point>    x = {self.x}; y = {self.y}"


class CartesianPoint(Point):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)

    def __repr__(self):
        return f"<Cartesian Point>    x = {self.x}; y = {self.y}"


class PixelPoint(Point):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)

    def __repr__(self):
        return f"<Pixel Point>    x = {self.x}; y = {self.y}"
