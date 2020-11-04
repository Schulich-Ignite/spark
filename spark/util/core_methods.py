from .helper_functions.arc_functions import *
from .helper_functions.canvas_functions import *
from .helper_functions.circle_functions import *
from .helper_functions.ellipse_functions import *
from .helper_functions.line_functions import *
from .helper_functions.misc_functions import *
from .helper_functions.rect_functions import *
from .helper_functions.square_functions import *
from .helper_functions.text_functions import *
from .helper_functions.triangle_functions import *

from .helper_functions.keyboard_functions import *


def extern(func):
    return globals()[f"helper_{func.__name__}"]
