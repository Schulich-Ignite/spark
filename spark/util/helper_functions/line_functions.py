from ..decorators import *
from numbers import Real


@validate_args([Real, Real, Real, Real])
@ignite_global
def helper_draw_line(self, *args):
    self.canvas.begin_path()
    self.canvas.move_to(args[0], args[1])
    self.canvas.line_to(args[2], args[3])
    self.canvas.close_path()
    self.canvas.stroke()


@validate_args([Real, Real, Real, Real])
@ignite_global
def helper_line(self, *args):
    self.draw_line(*args)


@validate_args([Real])
@ignite_global
def helper_line_width(self, *args):
    self.canvas.line_width = args[0]


@validate_args([Real])
@ignite_global
def helper_stroke_width(self, *args):
    self.line_width(*args)
