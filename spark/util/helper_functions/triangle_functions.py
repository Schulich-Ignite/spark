from ..decorators import *
from numbers import Real


@validate_args([Real, Real, Real, Real, Real, Real])
@ignite_global
def helper_triangle(self, *args):
    self.fill_triangle(*args)
    self.stroke_triangle(*args)


@validate_args([Real, Real, Real, Real, Real, Real])
@ignite_global
def helper_stroke_triangle(self, *args):
    self.canvas.begin_path()
    self.canvas.move_to(args[0], args[1])
    self.canvas.line_to(args[2], args[3])
    self.canvas.line_to(args[4], args[5])
    self.canvas.close_path()
    self.canvas.stroke()


@validate_args([Real, Real, Real, Real, Real, Real])
@ignite_global
def helper_fill_triangle(self, *args):
    self.canvas.begin_path()
    self.canvas.move_to(args[0], args[1])
    self.canvas.line_to(args[2], args[3])
    self.canvas.line_to(args[4], args[5])
    self.canvas.close_path()
    self.canvas.fill()
