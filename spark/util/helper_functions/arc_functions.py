from math import sin, cos
from ..decorators import validate_args, ignite_global
from numbers import Real


@validate_args([Real, Real, Real, Real],
               [Real, Real, Real, Real, Real],
               [Real, Real, Real, Real, Real, Real],
               [Real, Real, Real, Real, Real, Real, str])
@ignite_global
def helper_fill_arc(self, *args):
    x, y, r, scale_x, scale_y, start, stop, mode = self.arc_args(*args)

    if scale_x == 0 or scale_y == 0:
        return

    self.canvas.translate(x, y)
    self.canvas.scale(scale_x, scale_y)

    if mode == "open" or mode == "chord":
        self.canvas.fill_arc(0, 0, r, start, stop)
    elif mode == "default" or mode == "pie":
        self.canvas.begin_path()
        start_x = r*cos(start)
        start_y = r*sin(start)
        self.canvas.move_to(start_x, start_y)
        self.canvas.arc(0, 0, r, start, stop)
        self.canvas.line_to(0, 0)
        self.canvas.close_path()
        self.canvas.fill()

    self.canvas.scale(1/scale_x, 1/scale_y)
    self.canvas.translate(-x, -y)


@validate_args([Real, Real, Real, Real],
               [Real, Real, Real, Real, Real],
               [Real, Real, Real, Real, Real, Real],
               [Real, Real, Real, Real, Real, Real, str])
@ignite_global
def helper_stroke_arc(self, *args):
    x, y, r, scale_x, scale_y, start, stop, mode = self.arc_args(*args)

    if scale_x == 0 or scale_y == 0:
        return

    start_x = r*cos(start)
    start_y = r*sin(start)

    self.canvas.translate(x, y)
    self.canvas.scale(scale_x, scale_y)

    self.canvas.begin_path()
    self.canvas.move_to(start_x, start_y)
    self.canvas.arc(0, 0, r, start, stop)
    if mode == "open" or mode == "default":
        self.canvas.move_to(start_x, start_y)
    elif mode == "pie":
        self.canvas.line_to(0, 0)
    elif mode == "chord":
        pass
    self.canvas.close_path()
    self.canvas.stroke()

    self.canvas.scale(1/scale_x, 1/scale_y)
    self.canvas.translate(-x, -y)


@validate_args([Real, Real, Real, Real],
               [Real, Real, Real, Real, Real],
               [Real, Real, Real, Real, Real, Real],
               [Real, Real, Real, Real, Real, Real, str])
@ignite_global
def helper_arc(self, *args):
    self.fill_arc(*args)
    self.stroke_arc(*args)
