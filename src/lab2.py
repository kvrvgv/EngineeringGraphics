

import math
import tkinter as tk
from points import CartesianPoint, PixelPoint


class Settings:
    def __init__(self, title: str, zoom_x: float = 1, zoom_y: float = 1, background_color: str = "white"):
        self.title = title
        self.scale_x = 1 / zoom_x
        self.scale_y = 1 / zoom_y
        self.distance = 20
        self.background_color = background_color


class Figure:
    def __init__(self, *args: CartesianPoint):
        self.points = list()
        for arg in args:
            self.points.append(arg)
        self.points = tuple(self.points)


class App(tk.Tk):
    def __init__(
            self, *, width: int, height: int, settings: Settings,
            figure: Figure, root_point: CartesianPoint, rotate_angle: int
    ):
        self.width = width
        self.height = height
        self.settings = settings
        self.rotate_angle = rotate_angle
        self.center_pixel: PixelPoint = PixelPoint(width / 2, height / 2)
        super().__init__()
        self.title(self.settings.title)
        self.geometry(f"{width}x{height}")
        canvas_size = min(width, height)
        self.canvas = tk.Canvas(self, width=canvas_size, height=canvas_size, bg=self.settings.background_color)
        self.figure: Figure = figure
        self.__create_coordinates()
        self.root_point: CartesianPoint = root_point
        self.draw_root()
        self.rotate_figure()

    def rotate_figure(self, angle: int = None, color="green"):
        if angle is None:
            angle = self.rotate_angle
        angle = angle * math.pi / 180
        for point in self.figure.points:
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
        for point in self.figure.points:
            pixel_point = self.__convert_cartesian_to_pixels(point)
            args.append((pixel_point.x, pixel_point.y))
        self.canvas.create_polygon(*args, fill=color, outline="black", tags="figure", activefill="red")
        self.canvas.pack()

    def draw_root(self):
        root_point = self.__convert_cartesian_to_pixels(self.root_point)
        self.canvas.create_oval(
            root_point.x - 5, root_point.y - 5, root_point.x + 5, root_point.y + 5, fill="black"
        )

    def __convert_cartesian_to_pixels(self, point: CartesianPoint) -> PixelPoint:
        return PixelPoint(
            self.center_pixel.x + self.settings.distance * point.x / self.settings.scale_x,
            self.center_pixel.y - self.settings.distance * point.y / self.settings.scale_y
        )

    def __create_coordinates(self) -> None:
        """
        A private method for constructing a Cartesian coordinate system on the canvas
        :return: None
        """
        # region lined
        lineage = 7
        for i in range(-25, 25):
            x = self.center_pixel.x + i * self.settings.distance
            self.canvas.create_line(x, 0, x, self.height, fill="#F0F0F0")
            self.canvas.create_line(x, self.center_pixel.y + lineage, x, self.center_pixel.y - lineage)
            if i != 0:
                self.canvas.create_text(
                    x, self.center_pixel.y + lineage + 6,
                    text=str(i * self.settings.scale_x),
                    font=('Arial', 7, 'italic')
                )
        for i in range(-25, 25):
            y = self.center_pixel.y + i * self.settings.distance
            self.canvas.create_line(0, y, self.width, y, fill="#F0F0F0")
            self.canvas.create_line(self.center_pixel.x + lineage, y, self.center_pixel.x - lineage, y)
            if i != 0:
                self.canvas.create_text(
                    self.center_pixel.x - lineage - 6, y,
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
            zoom_x=1,
            zoom_y=1,
        ),
        root_point=CartesianPoint(5, 5),
        figure=Figure(
            CartesianPoint(3, 4),
            CartesianPoint(0, 2),
            CartesianPoint(-2, -2),
            CartesianPoint(2, 0)
        ),
        rotate_angle=1
    )
    app.mainloop()
