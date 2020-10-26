global_immut_names = set()
global_mut_names = set()

def global_immut(func):
    global global_immut_names
    if func.__name__ in global_mut_names:
        raise RuntimeError("Attempted to define {} as both mutable and immutable.".format(func.__name__))
    global_immut_names.add(func.__name__)
    return func

def global_mut(func):
    global global_mut_names
    if func.__name__ in global_immut_names:
        raise RuntimeError("Attempted to define {} as both mutable and immutable.".format(func.__name__))
    global_mut_names.add(func.__name__)
    return None
