# setup()
# draw()

global canvas
def fill_rect (x, y, width, height=None):
    if (height == None):
        canvas.fill_rect(x, y, width, width)
    else:
        canvas.fill_rect(x, y, width, height)

def stroke_rect (x, y, width, height=None):
    if (height == None):
        canvas.stroke_rect(x, y, width, width)
    else:
        canvas.stroke_rect(x, y, width, height)

def clear_rect(x, y, width, height=None):
    if (height == None):
        canvas.clear_rect(x, y, width, width)
    else:
        canvas.clear_rect(x, y, width, height)