from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Tuple
if TYPE_CHECKING:
    from ...core import Core

from ..decorators import *
from numbers import Real
from ipywidgets import Image
from ipycanvas import Canvas


_loaded_images: Dict[Tuple[str, int, int], Canvas] = {}


@validate_args([str, Real, Real, Real, Real])
@ignite_global
def helper_image(self: Core, *args):
    filename: str = args[0]
    x: int = int(args[1])
    y: int = int(args[2])
    w: int = int(args[3])
    h: int = int(args[4])

    key = (filename, abs(w), abs(h))

    if key not in _loaded_images:
        _loaded_images[key] = Canvas(width=abs(w), height=abs(h))
        _loaded_images[key].draw_image(Image.from_file(filename, width=abs(w), height=abs(h)), 0, 0, abs(w), abs(h))
    self.canvas.translate(x, y)
    if w < 0:
        self.canvas.scale(-1, 1)
    if h < 0:
        self.canvas.scale(1, -1)
    self.canvas.draw_image(_loaded_images[key], 0, 0)
    if h < 0:
        self.canvas.scale(1, -1)
    if w < 0:
        self.canvas.scale(-1, 1)
    self.canvas.translate(-x, -y)
