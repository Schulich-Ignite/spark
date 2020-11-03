from numbers import Real
from ..decorators import *


@validate_args([Real, Real])
@ignite_global
def helper_size(self, *args):
    self.width = args[0]
    self.height = args[1]


@validate_args([str], [Real], [Real, Real, Real], [Real, Real, Real, Real])
@ignite_global
def helper_fill_style(self, *args):
    self.canvas.fill_style = self.parse_color(func_name="fill_style", *args)


@validate_args([str], [Real], [Real, Real, Real], [Real, Real, Real, Real])
@ignite_global
def helper_stroke_style(self, *args):
    self.canvas.stroke_style = self.parse_color(func_name="stroke_style", *args)


@validate_args([])
@ignite_global
def helper_clear(self, *args):
    self.canvas.clear()


@validate_args([str], [Real], [Real, Real, Real], [Real, Real, Real, Real])
@ignite_global
def helper_background(self, *args):
    fill = self.parse_color(func_name="background", *args)
    old_fill = self.canvas.fill_style
    self.canvas.fill_style = fill
    self.canvas.fill_rect(0, 0, self.width, self.height)
    self.canvas.fill_style = old_fill
