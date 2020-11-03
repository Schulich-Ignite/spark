from ..decorators import *
from numbers import Real


@validate_args([Real, Real, Real])
@global_immut
def helper_circle(self, *args):
    self.ellipse(*args, args[2])


@validate_args([Real, Real, Real])
@global_immut
def helper_stroke_circle(self, *args):
    self.stroke_ellipse(*args, args[2])


@validate_args([Real, Real, Real])
@global_immut
def helper_fill_circle(self, *args):
    self.fill_ellipse(*args, args[2])
