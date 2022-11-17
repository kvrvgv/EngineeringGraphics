

import math
import tkinter as tk
from points import Point


class Settings:
    def __init__(self, title: str, zoom_x: float = 1, zoom_y: float = 1, background_color: str = "white"):
        self.title = title
        self.scale_x = 1 / zoom_x
        self.scale_y = 1 / zoom_y
        self.distance = 20
        self.background_color = background_color


class App(tk.Tk):
    def __init__(self, *, width: int, height: int, settings: Settings):
        self.width = width
        self.height = height
        self.settings = settings
        self.center: Point = Point(width / 2, height / 2)
        super().__init__()
        self.title(self.settings.title)
        self.geometry(f"{width}x{height}")
        canvas_size = min(width, height)
        self.canvas = tk.Canvas(self, width=canvas_size, height=canvas_size, bg=self.settings.background_color)
        self.figure: list[Point] = [Point(3, 4), Point(0, 2), Point(-2, -5), Point(2, 0)]
        self.__create_coordinates()
        self.root_point: Point = Point(5, 5)
        self.draw_root()
        self.rotate_figure()

    def rotate_figure(self, angle=1, color="green"):
        angle = angle * math.pi / 180
        for point in self.figure:
            # cos(theta) * (px-ox) - sin(theta) * (py-oy) + ox
            new_x = (point.x - self.root_point.x) * math.cos(angle) -\
                (point.y - self.root_point.y) * math.sin(angle) + \
                self.root_point.x
            # sin(theta) * (px-ox) + cos(theta) * (py-oy) + oy
            new_y = (point.x - self.root_point.x) * math.sin(angle) + \
                (point.y - self.root_point.y) * math.cos(angle) + \
                self.root_point.y
            point.x, point.y = new_x, new_y

        self.draw_figure(color)
        self.after(20, self.rotate_figure, 1)

    def draw_figure(self, color: str):
        self.canvas.delete("figure")
        args = list()
        for point in self.figure:
            args.append(
                (
                    self.center.x + self.settings.distance * point.x / self.settings.scale_x,
                    self.center.y - self.settings.distance * point.y / self.settings.scale_y
                )
            )
        self.canvas.create_polygon(*args, fill=color, outline="black", tags="figure", activefill="red")
        self.canvas.pack()

    def draw_root(self):
        x = self.center.x + self.settings.distance * self.root_point.x / self.settings.scale_x
        y = self.center.y - self.settings.distance * self.root_point.y / self.settings.scale_y
        self.canvas.create_oval(
            x, y, x + 10, y + 10, fill="black"
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


if __name__ == "__main__":
    app = App(
        width=940,
        height=940,
        settings=Settings(
            title="Lab2",
            zoom_x=2,
            zoom_y=2,
        )
    )
    app.mainloop()
