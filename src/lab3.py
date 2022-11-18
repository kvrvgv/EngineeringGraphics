

import math
import tkinter as tk
from random import choice

from points import PixelPoint


class PixelFigure:
    def __init__(self, *args: PixelPoint):
        self.points = list()
        for arg in args:
            self.points.append(arg)
        self.points: tuple[PixelPoint] = tuple(self.points[::-1])


variant_figure = {
    1: PixelFigure(
        PixelPoint(270, 300),
        PixelPoint(270, 200),
        PixelPoint(400, 160),
        PixelPoint(500, 230),
        PixelPoint(380, 370),
        PixelPoint(420, 260),
        PixelPoint(360, 280),
        PixelPoint(360, 210),
    ),
    2: PixelFigure(
        PixelPoint(280, 340),
        PixelPoint(200, 270),
        PixelPoint(270, 80),
        PixelPoint(480, 70),
        PixelPoint(550, 210),
        PixelPoint(490, 310),
    ),
    3: PixelFigure(
        PixelPoint(210, 360),
        PixelPoint(160, 220),
        PixelPoint(320, 90),
        PixelPoint(270, 210),
        PixelPoint(480, 180),
        PixelPoint(480, 400),
    ),
    4: PixelFigure(
        PixelPoint(140, 320),
        PixelPoint(130, 100),
        PixelPoint(360, 50),
        PixelPoint(210, 210),
        PixelPoint(420, 280),
        PixelPoint(480, 410),
        PixelPoint(400, 300),
        PixelPoint(390, 380),
    ),
    5: PixelFigure(
        PixelPoint(210, 380),
        PixelPoint(160, 100),
        PixelPoint(290, 200),
        PixelPoint(600, 170),
        PixelPoint(470, 390),
        PixelPoint(350, 270),
    ),
    6: PixelFigure(
        PixelPoint(190, 400),
        PixelPoint(120, 160),
        PixelPoint(200, 210),
        PixelPoint(310, 90),
        PixelPoint(460, 90),
        PixelPoint(290, 310),
        PixelPoint(590, 120),
        PixelPoint(550, 400),
    ),
    7: PixelFigure(
        PixelPoint(220, 410),
        PixelPoint(120, 110),
        PixelPoint(480, 60),
        PixelPoint(320, 200),
        PixelPoint(560, 190),
        PixelPoint(390, 360),
        PixelPoint(600, 440),
    ),
    8: PixelFigure(
        PixelPoint(270, 430),
        PixelPoint(170, 340),
        PixelPoint(400, 60),
        PixelPoint(290, 240),
        PixelPoint(490, 200),
        PixelPoint(580, 390),
        PixelPoint(400, 420),
    ),
}


class App(tk.Tk):
    def __init__(self, *, title: str, width: int, height: int, variant: int):
        self.width = width
        self.height = height
        self.center_pixel: PixelPoint = PixelPoint(width / 2, height / 2)
        super().__init__()
        self.title(title)
        self.geometry(f"{width}x{height}")
        canvas_size = min(width, height)
        self.canvas = tk.Canvas(self, width=canvas_size, height=canvas_size, bg="white")
        self.figure: PixelFigure = variant_figure.get(variant)
        self.__draw_figure(color="green")
        self.cut_triangles(color="black")
        self.__draw_figure_enum_points()

    def cut_triangles(self, color: str):
        figure_points = list(self.figure.points).copy()
        triangles = list()
        i = 0
        while len(self.figure.points) - 3 != len(triangles):
            p1 = figure_points[i - 1]
            p2 = figure_points[i]
            p3 = figure_points[i + 1]
            temp = figure_points.copy()
            temp.remove(figure_points[i - 1])
            temp.remove(figure_points[i])
            temp.remove(figure_points[i + 1])
            points_in_triangle = False
            for point in temp:
                if points_in_triangle:
                    continue
                if self.check_point_in_triangle(p1, p2, p3, point):
                    points_in_triangle = True
            if points_in_triangle == 0 and determinant([[p1.x, p1.y, 1], [p2.x, p2.y, 1], [p3.x, p3.y, 1]]) <= 0:
                self.canvas.create_polygon(p1.x, p1.y, p2.x, p2.y, p3.x, p3.y, fill=get_random_color(), outline=color)
                # self.canvas.create_line(p1.x, p1.y, p3.x, p3.y, fill=color)
                figure_points.pop(i)
                triangles.append((p1, p2, p3))
                i = 0
            i += 1

    def __draw_figure(self, color: str):
        self.canvas.delete("figure")
        args = list()
        for point in self.figure.points:
            args.append((point.x, point.y))
        self.canvas.create_polygon(*args, fill=color, outline="black", tags="figure", activefill="red")
        self.canvas.pack()

    def __draw_figure_enum_points(self, point_color: str = "red", text_color: str = "black"):
        for i, point in enumerate(self.figure.points):
            self.canvas.create_oval(
                point.x - 5, point.y - 5, point.x + 5, point.y + 5, fill=point_color, outline="black"
            )
            self.canvas.create_text(point.x, point.y - 15, text=f"P{i}", fill=text_color)
        self.canvas.pack()

    @staticmethod
    def check_point_in_triangle(p1: PixelPoint, p2: PixelPoint, p3: PixelPoint, point_in: PixelPoint) -> bool:
        """
        Function returns True if point_in in triangle p1p2p3
        :param p1: first triangle point
        :param p2: second triangle point
        :param p3: third triangle point
        :param point_in: point in triangle or not (point for check)
        :return: True if point in triangle
        """
        check_1 = (p1.x - point_in.x) * (p2.y - p1.y) - (p2.x - p1.x) * (p1.y - point_in.y)
        check_2 = (p2.x - point_in.x) * (p3.y - p2.y) - (p3.x - p2.x) * (p2.y - point_in.y)
        check_3 = (p3.x - point_in.x) * (p1.y - p3.y) - (p1.x - p3.x) * (p3.y - point_in.y)
        if check_3 <= 0 and check_2 <= 0 and check_1 <= 0:
            return True
        if check_3 >= 0 and check_2 >= 0 and check_1 >= 0:
            return True
        return False


def get_random_color() -> str:
    response = '#'
    for _ in range(0, 6):
        response += choice("456789ABCDEF")
    return response


def determinant(matrix: list[list[int]]) -> int:
    """
    Function that returns determinant of 3x3 matrix
    :param matrix: list[list[int]]
    :return: determinant
    """
    return (
            matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[2][1] * matrix[1][2]) -
            matrix[1][0] * (matrix[0][1] * matrix[2][2] - matrix[2][1] * matrix[0][2]) +
            matrix[2][0] * (matrix[0][1] * matrix[1][2] - matrix[1][1] * matrix[0][2])
    )


if __name__ == "__main__":
    app = App(
        width=650,
        height=650,
        title="Lab3",
        variant=4
    )
    app.mainloop()
