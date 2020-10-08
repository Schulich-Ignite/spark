# Commands to run on JupyterLab
# !pip install ipycanvas
# !conda install -c conda-forge nodejs
# !jupyter labextension install @jupyter-widgets/jupyterlab-manager ipycanvas

global canvas


def size(w, h):
    global canvas
    canvas = Canvas(width=w, height=h)


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


def rect(x, y, width, height=None):
    global canvas
    canvas.fill_rect(x, y, width, height)


def stroke_rect(x, y, width, height=None):
    global canvas
    canvas.stroke_rect(x, y, width, height)
