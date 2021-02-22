from ..decorators import *
from ..HTMLColors import HTMLColors
import re
from ..Errors import *
from numbers import Real
from math import pi
from math import sqrt
import random


@validate_args([str, str])
def helper_parse_color_string(self, func_name, s):
    rws = re.compile(r'\s')
    no_ws = rws.sub('', s).lower()
    # Check allowed color strings
    if no_ws in HTMLColors:
        return no_ws
    elif no_ws in self.color_strings:
        return self.color_strings[s]
    # Check other HTML-permissible formats
    else:
        for regex in self.regexes:
            if regex.fullmatch(no_ws) is not None:
                return no_ws
    # Not in any permitted format
    raise ArgumentConditionError(func_name, "", "Valid HTML format or color names", s)


@validate_args([str], [Real], [Real, Real, Real], [Real, Real, Real, Real])
def helper_parse_color(self, *args, func_name="parse_color"):
    def clip(x, lb, ub):
        return min(max(x, lb), ub)
    argc = len(args)

    if argc == 1:
        if isinstance(args[0], Real):
            n = int(clip(args[0], 0, 255))
            return f"rgb({n}, {n}, {n})"
        elif isinstance(args[0], str):
            return self.parse_color_string(func_name, args[0])
        raise ArgumentConditionError(func_name, "", "Valid HTML format or color names", args[0])
    elif argc == 3 or argc == 4:
        color_args = [int(clip(arg, 0, 255)) for arg in args[:3]]

        if argc == 3:
            return "rgb({}, {}, {})".format(*color_args)
        else:
            # Clip alpha between 0 and 1
            alpha_arg = clip(args[3], 0, 1.0)
            return "rgba({}, {}, {}, {})".format(*color_args, alpha_arg)
    else:
        raise ArgumentNumError(func_name, [1, 3, 4], argc)

@validate_args([str], [Real], [Real, Real, Real], [Real, Real, Real, Real])
@ignite_global
def helper_color(self, *args):
    return self.parse_color(*args)

@validate_args([Real, Real, Real, Real],
               [Real, Real, Real, Real, Real],
               [Real, Real, Real, Real, Real, Real],
               [Real, Real, Real, Real, Real, Real, str])
def helper_arc_args(self, *args):
    argc = len(args)
    x, y, w, h = args[:4]
    w, h = abs(w), abs(h)
    defaults = [0, 2*pi, "default"]
    start, stop, mode = [*args[4:argc], *defaults[argc-4:]]
    while start < 0:
        start += 2*pi
    while start > 2*pi:
        start -= 2*pi
    while stop < 0:
        stop += 2*pi
    while stop > 2*pi:
        stop += 2*pi
    
    d = max(w, h)/2
    if d == 0:
        return x, y, d, 0, 0, start, stop, mode
    else:
        w_ratio = w / d
        h_ratio = h / d

    return x, y, d/2, w_ratio, h_ratio, start, stop, mode


@validate_args([])
@ignite_global
def helper_random(self, *args):
    return random.random()


@validate_args([int])
@ignite_global
def helper_randint(self, *args):
    return random.randint(0, args[0])


@validate_args([Real, Real, Real, Real])
@ignite_global
def helper_bounding_box(self, *args):
    x, y, w, h = args
    left = min(x, x + w)
    abs_width = abs(w)
    top = min(y, y + h)
    abs_height = abs(h)

    return (left, top, abs_width, abs_height)

@validate_args([list, list], [list, list, bool], [tuple, tuple], [tuple, tuple, bool])
@ignite_global
def helper_collided(self, *args):
    x1, y1, width1, height1 = args[0]
    x2, y2, width2, height2 = args[1]

    sizes = {'bounding_box1 width': width1, 'bounding_box1 height': height1, 'bounding_box2 width': width2, 'bounding_box2 height': height2}

    for size_name, size_val in sizes.items():
        if size_val < 0:
            raise ArgumentError("collided expected {} to be greater or equal to 0, got {}".format(size_name, size_val)) 

    overlap_on_equal = len(args) == 3 and args[2]
    return self.axis_overlapped(x1, width1, x2, width2, overlap_on_equal) and self.axis_overlapped(y1, height1, y2, height2, overlap_on_equal)

@validate_args([Real, Real, Real, Real], [Real, Real, Real, Real, bool])
@ignite_global
def helper_axis_overlapped(self, *args):
    point1, length1, point2, length2 = args[:4]

    if len(args) == 5 and args[4]:
        return point1 + length1 >= point2 and point2 + length2 >= point1
    else:
        return point1 + length1 > point2 and point2 + length2 > point1

@validate_args([Real, Real, Real, Real])
@ignite_global
def helper_dist(self, *args):
    x1, y1, x2, y2 = args[:4]
    return sqrt((y2 - y1)**2 + (x2 - x1)**2)

