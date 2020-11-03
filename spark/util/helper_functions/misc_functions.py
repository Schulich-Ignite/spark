from ..decorators import *
from ..HTMLColors import HTMLColors
import re
from ..Errors import *
from numbers import Real
from math import pi
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


@validate_args([Real, Real, Real, Real],
               [Real, Real, Real, Real, Real],
               [Real, Real, Real, Real, Real, Real],
               [Real, Real, Real, Real, Real, Real, str])
def helper_arc_args(self, *args):
    argc = len(args)
    x, y, w, h = args[:4]
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

    return x, y, d/2, w/d, h/d, start, stop, mode


@validate_args([])
@ignite_global
def helper_random(self, *args):
    return random.random()


@validate_args([int])
@ignite_global
def helper_randint(self, *args):
    return random.randint(0, args[0])
