# from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic)

# Limitations:
# -> Cannot update canvas width / height by updating the global variables width / height.
#    Need to use size() method or canvas object.


import threading
import time

from math import pi
import re

from IPython.display import Code, display
from ipycanvas import Canvas, hold_canvas
from ipywidgets import Button
from ipyevents import Event

from .util import IpyExit
from .util.decorators import extern, _ignite_globals, ignite_global

DEFAULT_CANVAS_SIZE = (100, 100)
FRAME_RATE = 30
NO_ACTIVITY_THRESHOLD = 5 * 60  # 5 minutes

_sparkplug_active_thread_id = None
_sparkplug_last_activity = 0
_sparkplug_running = False


class Core:
    # All constants that will be injected into global scope in the user"s cell
    global_constants = {
        "pi": pi
    }

    ignite_globals = _ignite_globals

    def __init__(self, globals_dict):
        self.status_text = display(Code(""), display_id=True)
        self._globals_dict = globals_dict
        self._methods = {}

        self.stop_button = Button(description="Stop")
        self.stop_button.on_click(self.on_stop_button_clicked)
        self._globals_dict["canvas"] = Canvas()
        self.kb_mon = Event(source=self.canvas, watched_events=['keydown', 'keyup'], wait=1000 // FRAME_RATE,
                            prevent_default_actions=True)
        self.output_text = ""
        self.color_strings = {
            "default": "#888888"
        }
        match_255 = r"(?:(?:2(?:(?:5[0-5])|(?:[0-4][0-9])))|(?:[01]?[0-9]{1,2}))"
        match_alpha = r"(?:(?:1(?:\.0*)?)|(?:0(?:\.[0-9]*)?))"
        match_360 = r"(?:(?:3[0-5][0-9])|(?:[0-2]?[0-9]{1,2}))"
        match_100 = r"(?:100|[0-9]{1,2})"
        self.regexes = [
            re.compile(r"#[0-9A-Fa-f]{6}"),
            re.compile(r"rgb\({},{},{}\)".format(match_255, match_255, match_255)),
            re.compile(r"rgba\({},{},{},{}\)".format(match_255, match_255, match_255, match_alpha)),
            re.compile(r"hsl\({},{}%,{}%\)".format(match_360, match_100, match_100)),
            re.compile(r"hsla\({},{}%,{}%,{}\)".format(match_360, match_100, match_100, match_alpha))
        ]
        self.width, self.height = DEFAULT_CANVAS_SIZE
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_is_pressed = False
        self.key = ""
        self._keys_held = {}

        # Settings for drawing text (https://ipycanvas.readthedocs.io/en/latest/drawing_text.html).
        self.font_settings = {
            'size': 12.0,
            'font': 'sans-serif',
            'baseline': 'top',
            'align': 'left'
        }

    ### Properties ###

    @property
    @ignite_global
    def canvas(self) -> Canvas:
        return self._globals_dict["canvas"]

    @property
    @ignite_global
    def mouse_x(self):
        return self._globals_dict["mouse_x"]

    @mouse_x.setter
    def mouse_x(self, val):
        self._globals_dict["mouse_x"] = val

    @property
    @ignite_global
    def mouse_y(self):
        return self._globals_dict["mouse_y"]

    @mouse_y.setter
    def mouse_y(self, val):
        self._globals_dict["mouse_y"] = val

    @property
    @ignite_global
    def mouse_is_pressed(self):
        return self._globals_dict["mouse_is_pressed"]

    @mouse_is_pressed.setter
    def mouse_is_pressed(self, val):
        self._globals_dict["mouse_is_pressed"] = val

    @property
    @ignite_global
    def key(self):
        return self._globals_dict["key"]

    @key.setter
    def key(self, val):
        self._globals_dict["key"] = val

    @property
    @ignite_global
    def width(self):
        return self._globals_dict["width"]

    @width.setter
    def width(self, val):
        self._globals_dict["width"] = val
        self.canvas.width = val

    @property
    @ignite_global
    def height(self):
        return self._globals_dict["height"]

    @height.setter
    def height(self, val):
        self._globals_dict["height"] = val
        self.canvas.height = val

    ### Library init ###

    # Updates last activity time
    @staticmethod
    def refresh_last_activity():
        global _sparkplug_last_activity
        _sparkplug_last_activity = time.time()

    # Creates canvas and starts thread
    def start(self, methods):
        self._methods = methods
        draw = self._methods.get("draw", None)

        if draw:
            self.print_status("Running...")
            display(self.stop_button)

        display(self.canvas)

        self.output_text_code = display(Code(self.output_text), display_id=True)

        self.canvas.on_mouse_down(self.on_mouse_down)
        self.canvas.on_mouse_up(self.on_mouse_up)
        self.canvas.on_mouse_move(self.on_mouse_move)

        self.kb_mon.on_dom_event(self.handle_kb_event)

        # Initialize text drawing settings for the canvas. ()
        self.canvas.font = f"{self.font_settings['size']}px {self.font_settings['font']}"
        self.canvas.text_baseline = 'top'
        self.canvas.text_align = 'left'

        thread = threading.Thread(target=self.loop)
        thread.start()

    def stop(self, message="Stopped"):
        global _sparkplug_running

        if not _sparkplug_running:
            return

        _sparkplug_running = False
        self.print_status(message)
        self.kb_mon.reset_callbacks()
        self.kb_mon.close()

        # Assuming we're using IPython to draw the canvas through the display() function.
        # Commenting this out for now, it throws exception since it does not derive BaseException
        # raise IpyExit

    # Loop method that handles drawing and setup
    def loop(self):
        global _sparkplug_active_thread_id, _sparkplug_running

        # Set active thread to this thread. This will stop any other active thread.
        current_thread_id = threading.current_thread().native_id
        _sparkplug_active_thread_id = current_thread_id
        _sparkplug_running = True
        self.refresh_last_activity()

        draw = self._methods.get("draw", None)
        setup = self._methods.get("setup", None)

        if setup:
            try:
                setup()
            except Exception as e:
                self.stop("Error in setup() function: " + str(e))
                return

        while _sparkplug_running:
            if _sparkplug_active_thread_id != current_thread_id \
                    or time.time() - _sparkplug_last_activity > NO_ACTIVITY_THRESHOLD:
                self.stop("Stopped due to inactivity")
                return

            if not draw:
                self.stop("Done drawing.")
                return

            with hold_canvas(self.canvas):
                try:
                    draw()
                except Exception as e:
                    self.stop("Error in draw() function: " + str(e))
                    return

            time.sleep(1 / FRAME_RATE)

    # Prints status to embedded error box
    def print_status(self, msg):
        self.status_text.update(Code(msg))

    # Prints output to embedded output box
    # Can't use @validate_args decorator for functions actually accepting variable arguments
    @ignite_global
    def print(self, *args, sep=' ', end='\n', flush=True):
        global _sparkplug_running
        self.output_text += sep.join([str(arg) for arg in args]) + end

        if _sparkplug_running and flush:
            self.output_text_code.update(Code(self.output_text))

    # Update mouse_x, mouse_y, and call mouse_down handler
    def on_mouse_down(self, x, y):
        self.refresh_last_activity()
        self.mouse_x, self.mouse_y = int(x), int(y)
        self.mouse_is_pressed = True

        mouse_down = self._methods.get("mouse_down", None)
        if mouse_down:
            mouse_down()

    # Update mouse_x, mouse_y, and call mouse_up handler
    def on_mouse_up(self, x, y):
        self.refresh_last_activity()
        self.mouse_x, self.mouse_y = int(x), int(y)
        self.mouse_is_pressed = False

        mouse_up = self._methods.get("mouse_up", None)
        if mouse_up:
            mouse_up()

    # Update mouse_x, mouse_y, and call mouse_moved handler
    def on_mouse_move(self, x, y):
        self.refresh_last_activity()
        self.mouse_x, self.mouse_y = int(x), int(y)

        mouse_moved = self._methods.get("mouse_moved", None)
        if mouse_moved:
            mouse_moved()

    def on_stop_button_clicked(self, button):
        self.stop()

    @extern
    def handle_kb_event(self, event): pass

    ### User overrideable functions ###

    # The function bodies here do not matter, they are discarded
    @ignite_global(mutable=True)
    def setup(self): pass

    @ignite_global(mutable=True)
    def draw(self): pass

    @ignite_global(mutable=True)
    def mouse_up(self): pass

    @ignite_global(mutable=True)
    def mouse_down(self): pass

    @ignite_global(mutable=True)
    def mouse_moved(self): pass

    @ignite_global(mutable=True)
    def key_pressed(self): pass

    @ignite_global(mutable=True)
    def key_released(self): pass

    @ignite_global(mutable=True)
    def key_repeated(self): pass

    ### Global functions ###

    # From .util.helper_functions.keyboard_functions

    @extern
    def keys_held(self, *args):
        pass

    # From .util.helper_functions.canvas_functions

    @extern
    def size(self, *args): pass

    @extern
    def fill_style(self): pass

    @extern
    def stroke_style(self, *args): pass

    @extern
    def clear(self, *args): pass

    @extern
    def background(self, *args): pass

    # From util.helper_functions.rect_functions

    @extern
    def rect(self, *args): pass

    @extern
    def fill_rect(self, *args): pass

    @extern
    def stroke_rect(self, *args): pass

    @extern
    def clear_rect(self, *args): pass

    # From util.helper_functions.square_functions

    @extern
    def square(self, *args): pass

    @extern
    def stroke_square(self, *args): pass

    @extern
    def fill_square(self, *args): pass

    # From util.helper_functions.circle_functions

    @extern
    def circle(self, *args): pass

    @extern
    def fill_circle(self, *args): pass

    @extern
    def stroke_circle(self, *args): pass

    # From util.helper_functions.ellipse_functions

    @extern
    def ellipse(self, *args): pass

    @extern
    def fill_ellipse(self, *args): pass

    @extern
    def stroke_ellipse(self, *args): pass

    # From util.helper_functions.arc_functions

    @extern
    def arc(self, *args): pass

    @extern
    def fill_arc(self, *args): pass

    @extern
    def stroke_arc(self, *args): pass

    # From util.helper_functions.triangle_functions

    @extern
    def triangle(self, *args): pass

    @extern
    def fill_triangle(self, *args): pass

    @extern
    def stroke_triangle(self, *args): pass

    # From util.helper_functions.text_functions

    @extern
    def text_size(self, *args): pass

    @extern
    def text_align(self, *args): pass

    @extern
    def text(self, *args): pass

    # From util.helper_functions.line_functions

    @extern
    def draw_line(self, *args): pass

    @extern
    def line(self, *args): pass

    @extern
    def line_width(self, *args): pass

    # An alias to line_width
    @extern
    def stroke_width(self, *args): pass

    ### Helper Functions ###

    # From util.helper_functions.misc_functions

    @extern
    def parse_color(self, *args, func_name="parse_color"): pass

    @extern
    def parse_color_string(self, func_name, s): pass

    @extern
    def arc_args(self, *args): pass

    @extern
    def random(self, *args): pass

    @extern
    def randint(self, *args): pass
