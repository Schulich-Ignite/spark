from ..decorators import *
from numbers import Real


@validate_args([Real, Real, Real, Real])
@ignite_global
def helper_rect(self, *args):
    self.canvas.fill_rect(*args)
    self.canvas.stroke_rect(*args)


@validate_args([Real, Real, Real, Real])
@ignite_global
def helper_fill_rect(self, *args):
    self.canvas.fill_rect(*args)


@validate_args([Real, Real, Real, Real])
@ignite_global
def helper_stroke_rect(self, *args):
    self.canvas.stroke_rect(*args)


@validate_args([Real, Real, Real, Real])
@ignite_global
def helper_clear_rect(self, *args):
    self.canvas.clear_rect(*args)
