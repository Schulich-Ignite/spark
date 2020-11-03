from .Errors import *


class FunctionSignature:
    def __init__(self, func_name=None, valid_inputs=None, has_self=True):
        if func_name is not None:
            self.func_name = func_name
        else:
            self.func_name = ""
        if valid_inputs is not None:
            self.valid_inputs = valid_inputs
            self.valid_lens = [len(x) for x in valid_inputs]
        else:
            self.valid_inputs = []
            self.valid_lens = []
        self.has_self = has_self

    def add_valid_inputs(self, *args):
        self.valid_inputs += args
        self.valid_lens += [len(x) for x in args]

    def check_inputs(self, *args):
        check = args
        if self.has_self:
            check = args[1:]
        if len(check) in self.valid_lens:
            against = [self.valid_inputs[i] for i, vl in enumerate(self.valid_lens) if vl == len(check)]
            found_valid = False
            for fmt in against:
                found_valid = True
                for arg, arg_type in zip(check, fmt):
                    if not isinstance(arg, arg_type):
                        found_valid = False
                        break
                if found_valid:
                    break

            if not found_valid:
                raise ArgumentTypeListError(self.func_name, against, [type(a) for a in check], check)
        else:
            raise ArgumentNumError(self.func_name, list(dict.fromkeys(self.valid_lens)), len(check))
