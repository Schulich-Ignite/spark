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
