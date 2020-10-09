# setup()
# draw()
from math import pi
from ipycanvas import *

canvas = Canvas(width = 400, height = 400)

def fill_arc (x, y, radius, start_angle, end_angle, anticlockwise = False):
    canvas.fill_arc(x, y, radius, start_angle, end_angle, anticlockwise)

def stroke_arc (x, y, radius, start_angle, end_angle, anticlockwise = False):
    canvas.stroke_arc(x, y, radius, start_angle, end_angle, anticlockwise)

def fill_circle (x, y, radius):
    fill_arc(x, y, radius, 0, 2 * pi)

def stroke_circle (x, y, radius):
    stroke_arc(x, y, radius, 0, 2 * pi)

def draw_line (x1, y1, x2, y2, thickness = 1):
    canvas.begin_path()
    canvas.line_width(thickness)
    canvas.move_to(x1, y1)
    canvas.line_to(x2, y2)
    canvas.line_width(1)
    canvas.close_path()

def fill_text (text, x, y, size = 32):
    canvas.font = "{px}px serif".format(px = size)
    canvas.fill_text(text, x, y)

def stroke_text (text, x, y, size = 32):
    canvas.font = "{px}px serif".format(px = size)
    canvas.stroke_text(text, x, y)

def text_align (alignment):
    canvas.text_align(alignment)