from ..decorators import *
from numbers import Real


@validate_args([Real, Real, Real, Real])
@ignite_global
def helper_ellipse(self, *args):
    self.fill_ellipse(*args)
    self.stroke_ellipse(*args)


@validate_args([Real, Real, Real, Real])
@ignite_global
def helper_stroke_ellipse(self, *args):
    self.stroke_arc(*args)


@validate_args([Real, Real, Real, Real])
@ignite_global
def helper_fill_ellipse(self, *args):
    self.fill_arc(*args)