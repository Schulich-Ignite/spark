import functools
from .TypeSignature import FunctionSignature


def validate_args(*fmts, has_self=True):
    def decorator_validate_args(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            fname = func.__name__
            if fname.startswith("helper_"):
                fname = fname[7:]
            sig = FunctionSignature(fname, fmts, has_self)
            sig.check_inputs(*args)
            return func(*args, **kwargs)

        return wrapper

    return decorator_validate_args


_ignite_globals = {}


def ignite_global(_func=None, *, mutable=False):
    def decorator(func):
        global _ignite_globals
        # If this was a helper function, the global will be accessed without the "helper_" prefix
        if func.__name__.startswith("helper_"):
            fname = func.__name__[7:]
        else:
            fname = func.__name__

        # This is the first declaration of this global
        if fname not in _ignite_globals or mutable == _ignite_globals[fname]:
            _ignite_globals[fname] = mutable
            if mutable:
                return None
            return func
        # This is a redefinition of this global, and the definitions have different mutabilities
        else:
            raise RuntimeError(f"Attempted to define global {fname} as both mutable and immutable.")
    if _func is None:
        return decorator
    else:
        return decorator(_func)


from .core_methods import extern
