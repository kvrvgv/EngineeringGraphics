

import math
import tkinter as tk
from dataclasses import dataclass
from tkinter import TclError
from typing import Generator, Callable
from points import PixelPoint, CartesianPoint


exceptions = dict()


@dataclass
class Settings:
    def __init__(self, title: str, detailing: int = 100, min_x: float = None, max_x: float = None, zoom_x: float = 1,
                 zoom_y: float = 1, background_color: str = "white"):
        """
        Class of application settings
        :param title: Window name
        :param detailing: If we increase this parameter, we decrease the iterator step and plot more accurately.
                          But this greatly slows down the construction
        :param min_x: start x-value (Default: 0)
        :param max_x: finish x-value (Default: canvas width)
        :param zoom_x: x-axis approximation
        :param zoom_y: y-axis approximation
        :param background_color: hex value for background color
        """
        self.title = title
        self.min_x = min_x
        self.max_x = max_x
        if 0 in (zoom_x, zoom_y):
            raise ValueError("Zoom can't be zero")
        self.scale_x = 1 / zoom_x
        self.scale_y = 1 / zoom_y
        self.distance = 20
        self.detailing = detailing
        self.background_color = background_color


class App(tk.Tk):
    def __init__(self, *, width: int, height: int, settings: Settings):
        self.width = width
        self.height = height
        self.settings = settings
        self.center: PixelPoint = PixelPoint(width / 2, height / 2)
        super().__init__()
        self.title(self.settings.title)
        self.geometry(f"{width}x{height}")
        canvas_size = min(width, height)
        self.canvas = tk.Canvas(self, width=canvas_size, height=canvas_size, bg=self.settings.background_color)
        self.__create_coordinates()
        self.generator = self.__create_generator(function)
        self.build_function_graphic()

    @property
    def corner_point(self) -> CartesianPoint:
        """
        Shows top-left corner point
        :return: CartesianPoint object
        """
        return CartesianPoint(
            -self.settings.scale_x * self.center.x / self.settings.distance,
            self.settings.scale_y * self.center.y / self.settings.distance
        )

    def build_function_graphic(self, prev_point: CartesianPoint = None) -> None:
        try:
            point = next(self.generator)
        except StopIteration:
            print(f"Done.\nRaised exceptions: {exceptions or 'No exceptions'}")
            exceptions.clear()
            return
        if self.__validate_point(prev_point) and self.__validate_point(point):
            self.draw_line(prev_point, point)

        self.after(1, self.build_function_graphic, point)

    def draw_line(self, prev_point: CartesianPoint, point: CartesianPoint, color: str = "red"):
        new_prev_point = self.__convert_cartesian_to_pixels(prev_point)
        new_point = self.__convert_cartesian_to_pixels(point)
        try:
            self.canvas.create_line(new_prev_point.x, new_prev_point.y, new_point.x, new_point.y, fill=color)
        except TclError as e:
            e = e.args[0].split("\"")[0][:-1]
            exceptions.update({e: exceptions.get(e, 0) + 1})

    def __create_generator(self, func: Callable) -> Generator[CartesianPoint, None, None]:
        """
        The function that returns the point generator for the function
        :return: Generator object
        """
        left = round((self.settings.min_x or self.corner_point.x) * self.settings.detailing)
        right = round((self.settings.max_x or -self.corner_point.x) * self.settings.detailing)
        for x_pix in range(left, right):
            x = x_pix / self.settings.detailing
            try:
                yield CartesianPoint(x, func(x))
            except Exception as e:
                exceptions.update({e.args[0]: exceptions.get(e.args[0], 0) + 1})
                yield None

    def __validate_point(self, point: CartesianPoint) -> bool:
        """
        A private method that checks if a point can be drawn on the coordinate plane
        :param point: Point object
        :return: True if point can be drawn
        """
        if point is None or abs(point.x) > abs(self.corner_point.x) or abs(point.y) > abs(self.corner_point.y):
            return False
        return True

    def __convert_cartesian_to_pixels(self, point: CartesianPoint) -> PixelPoint:
        return PixelPoint(
            self.center.x + self.settings.distance * point.x / self.settings.scale_x,
            self.center.y - self.settings.distance * point.y / self.settings.scale_y
        )

    def __create_coordinates(self) -> None:
        """
        A private method for constructing a Cartesian coordinate system on the canvas
        :return: None
        """
        # region lined
        lineage = 7
        for i in range(-25, 25):
            x = self.center.x + i * self.settings.distance
            self.canvas.create_line(x, 0, x, self.height, fill="#F0F0F0")
            self.canvas.create_line(x, self.center.y + lineage, x, self.center.y - lineage)
            if i != 0:
                self.canvas.create_text(
                    x, self.center.y + lineage + 6,
                    text=str(i * self.settings.scale_x),
                    font=('Arial', 7, 'italic')
                )
        for i in range(-25, 25):
            y = self.center.y + i * self.settings.distance
            self.canvas.create_line(0, y, self.width, y, fill="#F0F0F0")
            self.canvas.create_line(self.center.x + lineage, y, self.center.x - lineage, y)
            if i != 0:
                self.canvas.create_text(
                    self.center.x - lineage - 6, y,
                    text=str(- i * self.settings.scale_y),
                    font=('Arial', 7, 'italic')
                )
        # endregion
        # region cross
        x_line_height = self.height / 2
        self.canvas.create_line(0, x_line_height, self.width, x_line_height)  # Ox
        y_line_width = self.width / 2
        self.canvas.create_line(y_line_width, 0, y_line_width, self.height)
        # endregion
        self.canvas.pack()


def function(x: float):
    return (math.tan(x) ** 0.5) / math.sqrt(x) + 9


if __name__ == "__main__":
    app = App(
        width=940,
        height=940,
        settings=Settings(
            title="Lab1",
            zoom_x=1,
            zoom_y=1,
            detailing=100
        )
    )
    app.mainloop()
