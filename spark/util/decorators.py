import functools
from .TypeSignature import FunctionSignature


def validate_args(*fmts, has_self=True):
    def decorator_validate_args(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            sig = FunctionSignature(func.__name__, fmts, has_self)
            sig.check_inputs(*args)
            return func(*args, **kwargs)
        return wrapper
    return decorator_validate_args


global_immut_names = set()


def global_immut(func):
    global global_immut_names
    if func.__name__ in global_mut_names:
        raise RuntimeError("Attempted to define {} as both mutable and immutable.".format(func.__name__))
    global_immut_names.add(func.__name__)
    return func


global_mut_names = set()


def global_mut(func):
    global global_mut_names
    if func.__name__ in global_immut_names:
        raise RuntimeError("Attempted to define {} as both mutable and immutable.".format(func.__name__))
    global_mut_names.add(func.__name__)
    return None
