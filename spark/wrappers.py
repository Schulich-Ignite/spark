# Commands to run on JupyterLab
# !pip install ipycanvas
# !conda install -c conda-forge nodejs
# !jupyter labextension install @jupyter-widgets/jupyterlab-manager ipycanvas

global canvas


def size(w, h):
    global canvas
    canvas = canvas(width=w, height=h)


def display():
    global canvas
    return canvas


def width(w):
    global canvas
    canvas.width = w


def height(h):
    global canvas
    canvas.height = h


def clear():
    global canvas
    canvas.clear()


# Shadows name 'width' and 'height' from outer scope. Changed to 'w' and 'h'.
def rect(x, y, w, h=None):
    global canvas
    canvas.fill_rect(x, y, w, h)


# Shadows name 'width' and 'height' from outer scope. Changed to 'w' and 'h'.
def stroke_rect(x, y, w, h=None):
    global canvas
    canvas.stroke_rect(x, y, w, h)
