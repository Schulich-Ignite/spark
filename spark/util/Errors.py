class ArgumentError(Exception):

    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)


class ArgumentTypeError(ArgumentError):
    def __init__(self, func_name, argument_name, allowed_types, actual_type, arg):
        if type(argument_name) == str and len(argument_name) > 0:
            argname = "{} to be of type".format(argument_name)
        else:
            argname = "type"
        type_str = ""
        if type(allowed_types) == list:
            allowed_type_names = [t.__name__ for t in allowed_types]
            if len(allowed_type_names) == 1:
                type_str += allowed_type_names[0]
            elif len(allowed_type_names) == 2:
                type_str += "{} or {}".format(*allowed_type_names)
            else:
                type_str = ", ".join([str(t) for t in allowed_type_names[:-1]])
                type_str += ", or {}".format(allowed_type_names[-1])
        elif type(allowed_types) == type:
            type_str = allowed_types.__name__
        else:
            type_str = str(allowed_types)

        self.message = "{} expected {} {}, got {} of type {}".format(
            func_name, argname, type_str, arg, actual_type.__name__)
        super().__init__(self.message)


class ArgumentTypeListError(ArgumentError):
    def __init__(self, func_name, valid_fmts, actual_fmt, actual_vals=None):
        arg_plural = "argument"
        if len(actual_fmt) > 1:
            arg_plural += "s"
        s = "Invalid types for {} with {} {}, expected".format(func_name, len(actual_fmt), arg_plural)
        if len(valid_fmts) >= 1:
            if len(valid_fmts) > 1:
                s += " one of"
            s += " \n"
            s += "".join(["\t{}({})\n".format(func_name, ", ".join([t.__name__ for t in fmt])) for fmt in valid_fmts])
        else:
            s += "{}()\n".format(func_name)
        s += "received {}(".format(func_name)
        if actual_vals is not None and len(actual_vals) == len(actual_fmt):
            s += ", ".join(["{}: {}".format(arg, t.__name__) for arg, t in zip(actual_vals, actual_fmt)])
        else:
            s += ", ".join([t.__name__ for t in actual_fmt])
        s += ")"
        self.message = s
        super().__init__(self.message)


class ArgumentNumError(ArgumentError):
    def __init__(self, func_name, allowed_nums, actual_num):
        num_str = ""
        if type(allowed_nums) == list:
            if len(allowed_nums) == 1:
                num_str += str(allowed_nums[0])
            elif len(allowed_nums) == 2:
                num_str += "{} or {}".format(*allowed_nums)
            else:
                num_str = ", ".join([str(n) for n in allowed_nums[:-1]])
                num_str += ", or {}".format(allowed_nums[-1])
        else:
            num_str = str(allowed_nums)
        self.message = "{} expected {} arguments, got {}".format(
            func_name,
            num_str,
            actual_num
        )
        super().__init__(self.message)


class ArgumentConditionError(ArgumentError):
    def __init__(self, func_name, arg_name, expected_condition, actual_value):
        if type(arg_name) == str and len(arg_name) > 0:
            argname = "{}".format(arg_name)
        else:
            argname = "argument"
        self.message = "{} expected {} to match \"{}\", got {}".format(
            func_name,
            argname,
            expected_condition,
            actual_value
        )
        super().__init__(self.message)

    pass
