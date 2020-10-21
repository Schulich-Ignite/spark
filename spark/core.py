# from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic)

# Limitations:
# -> Cannot update canvas width / height by updating the global variables width / height.
#    Need to use size() method or canvas object.


import threading
import time
from math import pi

import numpy as np
from IPython.display import Code, display
from ipycanvas import Canvas, hold_canvas
from ipywidgets import Button

from .util import IpyExit


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

    # All methods/fields from this class that will be exposed as global in user"s scope
    global_fields = {
        "canvas", "size", "width", "height",
        "mouse_x", "mouse_y", "mouse_is_pressed",
        "fill_style", "stroke_style",
        "clear", "background",
        "rect", "square", "fill_rect", "stroke_rect", "clear_rect",
        "fill_text", "stroke_text", "text_align",
        "draw_line",
        "circle", "fill_circle", "stroke_circle", "fill_arc", "stroke_arc",
        "print"
    }

    # All methods that user will be able to define and override
    global_methods = {
        "draw", "setup",
        "mouse_down", "mouse_up", "mouse_moved"
    }

    def __init__(self, globals_dict):
        self.status_text = display(Code(""), display_id=True)
        self._globals_dict = globals_dict
        self._methods = {}

        self.stop_button = Button(description="Stop")
        self.stop_button.on_click(self.on_stop_button_clicked)

        self.canvas = Canvas()
        self.output_text = ""
        self.width, self.height = DEFAULT_CANVAS_SIZE
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_is_pressed = False

    ### Properties ###

    @property
    def mouse_x(self):
        return self._globals_dict["mouse_x"]

    @mouse_x.setter
    def mouse_x(self, val):
        self._globals_dict["mouse_x"] = val

    @property
    def mouse_y(self):
        return self._globals_dict["mouse_y"]

    @mouse_y.setter
    def mouse_y(self, val):
        self._globals_dict["mouse_y"] = val

    @property
    def mouse_is_pressed(self):
        return self._globals_dict["mouse_is_pressed"]

    @mouse_is_pressed.setter
    def mouse_is_pressed(self, val):
        self._globals_dict["mouse_is_pressed"] = val

    @property
    def width(self):
        return self._globals_dict["width"]

    @width.setter
    def width(self, val):
        self._globals_dict["width"] = val
        self.canvas.width = val

    @property
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
        else:
            self.print_status("Done drawing")

        display(self.canvas)
        
        self.output_text_code = display(Code(self.output_text), display_id=True)

        self.canvas.on_mouse_down(self.on_mouse_down)
        self.canvas.on_mouse_up(self.on_mouse_up)
        self.canvas.on_mouse_move(self.on_mouse_move)

        thread = threading.Thread(target=self.loop)
        thread.start()

    def stop(self, message="Stopped"):
        global _sparkplug_running

        if not _sparkplug_running:
            return

        _sparkplug_running = False
        self.print_status(message)
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
                self.print_status("Error in setup() function: " + str(e))
                return

        while _sparkplug_running:
            if _sparkplug_active_thread_id != current_thread_id or time.time() - _sparkplug_last_activity > NO_ACTIVITY_THRESHOLD:
                self.stop("Stopped due to inactivity")
                return

            if not draw:
                return

            with hold_canvas(self.canvas):
                try:
                    draw()
                except Exception as e:
                    self.print_status("Error in draw() function: " + str(e))
                    return

            time.sleep(1 / FRAME_RATE)

    # Prints status to embedded error box
    def print_status(self, msg):
        self.status_text.update(Code(msg))
    
    # Prints output to embedded output box
    def print(self, msg):
        global _sparkplug_running
        self.output_text += str(msg) + "\n"

        if _sparkplug_running:
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

    ### Global functions ###

    # Sets canvas size
    def size(self, *args):
        if len(args) == 2:
            self.width = args[0]
            self.height = args[1]

    # Sets fill style
    # 1 arg: HTML string value
    # 3 args: r, g, b are int between 0 and 255
    # 4 args: r, g, b, a, where r, g, b are ints between 0 and 255, and  a (alpha) is a float between 0 and 1.0
    def fill_style(self, *args):
        self.canvas.fill_style = self.parse_color("fill_style", *args)

    def stroke_style(self, *args):
        self.canvas.stroke_style = self.parse_color("stroke_style", *args)

    # Combines fill_rect and stroke_rect into one wrapper function
    def rect(self, *args):
        self.check_coords("rect", *args)
        
        self.canvas.fill_rect(*args)
        self.canvas.stroke_rect(*args)

    # Similar to self.rect wrapper, except only accepts x, y and size
    def square(self, *args):
        self.check_coords("square", *args, width_only=True)
        rect_args = (*args, args[2]) # Copy the width arg into the height
        self.rect(*rect_args)

    # Draws filled rect
    def fill_rect(self, *args):
        self.check_coords("fill_rect", *args)
        self.canvas.fill_rect(*args)
    
    # Strokes a rect
    def stroke_rect(self, *args):
        self.check_coords("stroke_rect", *args)
        self.canvas.stroke_rect(*args)

    #Clears a rect
    def clear_rect(self, *args):
        self.check_coords('clear_rect', *args)
        self.canvas.clear_rect(*args)

    # Draws circle at given coordinates
    def circle(self, *args):
        self.check_coords("circle", *args, width_only=True)
        arc_args = self.arc_args(*args)
        self.canvas.fill_arc(*arc_args)
        self.canvas.stroke_arc(*arc_args)

    # Draws filled circle
    def fill_circle(self, *args):
        self.check_coords("fill_circle", *args, width_only=True)
        arc_args = self.arc_args(*args)
        self.canvas.fill_arc(*arc_args)

    # Draws circle stroke
    def stroke_circle(self, *args):
        self.check_coords("stroke_circle", *args, width_only=True)
        arc_args = self.arc_args(*args)
        self.canvas.stroke_arc(*arc_args)
        
    def fill_arc(self, *args):
        self.canvas.fill_arc(*args)

    def stroke_arc(self, *args):
        self.canvas.stroke_arc(*args)
    
    def fill_text(self, *args):
        self.canvas.font = "{px}px sans-serif".format(px = args[4])
        self.canvas.fill_text(args[0:3])
        self.canvas.font = "12px sans-serif"

    def stroke_text(self, *args):
        self.canvas.font = "{px}px sans-serif".format(px = args[4])
        self.canvas.stroke_text(args[0:3])
        self.canvas.font = "12px sans-serif"

    def text_align(self, *args):
        self.canvas.text_align(*args)

    def draw_line(self, *args):
        if len(args) == 4:
            self.canvas.line_width = args[4]
        else:
            self.canvas.line_width = 1
            
        self.canvas.begin_path()
        self.canvas.move_to(args[0],args[1])
        self.canvas.line_to(args[2],args[4])
        self.canvas.close_path()

    # Clears canvas
    def clear(self, *args):
        self.canvas.clear()

    
    # Draws background on canvas
    def background(self, *args):
        old_fill = self.canvas.fill_style
        argc = len(args)

        if argc == 3:
            if ((not type(args[0]) is int) or (not type(args[1]) is int) or (not type(args[2]) is int)):
                raise TypeError("Enter Values between 0 and 255(integers only) for all 3 values")
            elif (not (args[0] >= 0 and args[0] <= 255) or not (args[1] >= 0 and args[1] <= 255) or not (
                args[2] >= 0 and args[2] <= 255)):
                raise TypeError("Enter Values between 0 and 255(integers only) for all 3 values")
            self.clear()
            self.fill_style(args[0], args[1], args[2])
            self.fill_rect(0, 0, self.width, self.height)
        elif argc == 1:
            if (not type(args[0]) is str):
                raise TypeError("Enter colour value in Hex i.e #000000 for black and so on")
            self.clear()
            self.fill_style(args[0])
            self.fill_rect(0, 0, self.width, self.height)
        elif argc == 4:
            if ((not type(args[0]) is int) or (not type(args[1]) is int) or (not type(args[2]) is int) or (
            not type(args[3]) is float)):
                raise TypeError("Enter Values between 0 and 255(integers only) for all 3 values")
            elif (not (args[0] >= 0 and args[0] <= 255) or not (args[1] >= 0 and args[1] <= 255) or not (
                args[2] >= 0 and args[2] <= 255) or not (args[3] >= 0.0 and args[3] <= 1.0)):
                raise TypeError(
                "Enter Values between 0 and 255(integers only) for all 3 values and a value between 0.0 and 1.0 for opacity(last argument")
            self.clear()
            self.fill_style(args[0], args[1], args[2], args[3])
            self.fill_rect(0, 0, self.width, self.height)
        
        self.canvas.fill_style = old_fill
    
    ### Helper Functions ###

    # Tests if input is numeric
    # Note: No support for complex numbers
    def check_type_is_num(self, n, func_name=None):
        if not isinstance(n, (int, float)):
            msg = "Expected {} to be a number".format(n)
            if func_name:
                msg = "{} expected {} to be a number".format(func_name, self.quote_if_string(n))
            raise TypeError(msg)

    # Tests if input is an int
    def check_type_is_int(self, n, func_name=None):
        if type(n) is not int:
            msg = "Expected {} to be an int".format(n)
            if func_name:
                msg = "{} expected {} to be an int".format(func_name, self.quote_if_string(n))
            raise TypeError(msg)

    # Tests if input is a float
    # allow_int: Set to True to allow ints as a float. Defaults to True.
    def check_type_is_float(self, n, func_name=None, allow_int=True):
        if type(n) is not float:
            if not allow_int or type(n) is not int:
                msg = "Expected {} to be a float".format(n)
                if func_name:
                    msg = "{} expected {} to be a float".format(func_name, self.quote_if_string(n))
                raise TypeError(msg)

    @staticmethod
    def quote_if_string(val):
        if type(val) is str:
            return "\"{}\"".format(val)
        else:
            return val
    
    # Parse a string, rgb or rgba input into an HTML color string
    def parse_color(self, func_name, *args):
        argc = len(args)

        if argc == 1:
            return args[0]
        elif argc == 3 or argc == 4:
            color_args = args[:3]
            for col in color_args:
                self.check_type_is_int(col, func_name)
            color_args = np.clip(color_args, 0, 255)

            if argc == 3:
                return "rgb({}, {}, {})".format(*color_args)
            else:
                # Clip alpha between 0 and 1
                alpha_arg = args[3]
                self.check_type_is_float(alpha_arg, func_name)
                alpha_arg = np.clip(alpha_arg, 0, 1.0)
                return "rgba({}, {}, {}, {})".format(*color_args, alpha_arg)
        else:
            raise TypeError("{} expected {}, {} or {} arguments, got {}".format(func_name, 1, 3, 4, argc))

    # Check a set of 4 args are valid coordinates
    # x, y, w, h
    def check_coords(self, func_name, *args, width_only=False):
        argc = len(args)
        if argc != 4 and not width_only:
            raise TypeError("{} expected {} arguments for x, y, w, h, got {} arguments".format(func_name, 4, argc))
        elif argc != 3 and width_only:
            raise TypeError("{} expected {} arguments for x, y, size, got {} arguments".format(func_name, 3, argc))

        for arg in args:
            self.check_type_is_float(arg, func_name)

    # Convert a tuple of circle args into arc args 
    def arc_args(self, *args):
        return (args[0], args[1], args[2] / 2, 0, 2 * pi)
