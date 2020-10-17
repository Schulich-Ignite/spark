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
    
        # Copy global methods from Core object
        for field in core.Core.global_fields:
            globals_dict[field] = getattr(self.core_obj, field)

        # Execute the code inside the cell and inject the globals we defined.
        try:
            exec(cell_code, globals_dict, locals_dict)
        except Exception as e:
            print("Error: " + str(e))
        
        # Look at all methods defined by user, and see if they overwrote anything useful
        methods = {}
        for key, val in locals_dict.items():
            if key in core.Core.global_methods:
                methods[key] = val      # Track the global methods and pass to the core_obj.
            else:
                globals_dict[key] = val # Copy locals to global to keep them available.
        
        # Run bootstrap code
        self.core_obj.start(methods)
        
