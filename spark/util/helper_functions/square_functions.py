from ..decorators import *
from numbers import Real


@validate_args([Real, Real, Real])
@global_immut
def helper_square(self, *args):
    self.rect(*args, args[2])


@validate_args([Real, Real, Real])
@global_immut
def helper_stroke_square(self, *args):
    self.stroke_rect(*args, args[2])


@validate_args([Real, Real, Real])
@global_immut
def helper_fill_square(self, *args):
    self.fill_rect(*args, args[2])
