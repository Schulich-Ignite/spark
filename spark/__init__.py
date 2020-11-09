# from .sparkplug import SparkplugMagic
from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic)
import importlib
from . import core

importlib.reload(core)


def load_ipython_extension(ipython):
    ipython.register_magics(IgniteMagic)


# Defines the "magic" that will be used inside the cells
@magics_class
class IgniteMagic(Magics):
    @cell_magic
    def ignite(self, line, cell_code):
        if hasattr(self, "core_obj"):
            self.core_obj.stop()

        globals_dict = {}
        locals_dict = {}

        self.core_obj = core.Core(globals_dict)

        # Copy global constants from Core object
        for key, val in core.Core.global_constants.items():
            globals_dict[key] = val

        for field, mutable in core.Core.ignite_globals.items():
            if not mutable:
                globals_dict[field] = getattr(self.core_obj, field)

        # Execute the code inside the cell and inject the globals we defined.
        try:
            exec(cell_code, globals_dict, locals_dict)
        except Exception as e:
            print("Error: " + str(e))

        # Look at all methods defined by user, and see if they overwrote anything useful
        methods = {}
        for key, val in locals_dict.items():
            mutable = core.Core.ignite_globals.get(key)
            if mutable is None:
                globals_dict[key] = val
            elif mutable:
                methods[key] = val
            else:
                print(f'Error in cell: Attempted redefinition of immutable Spark global "{key}".')
                return

        # Run bootstrap code
        self.core_obj.start(methods)
