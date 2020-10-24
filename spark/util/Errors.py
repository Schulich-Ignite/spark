
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
            if len(allowed_types) == 1:
                type_str += str(allowed_types[0])
            elif len(allowed_types) == 2:
                type_str += "{} or {}".format(*allowed_types)
            else:
                type_str = (", ".join(["{}"]*(len(allowed_types)-1))).format(*allowed_types[:-1])
                # When merging, get rid of this one!
                type_str += ", or {}".format(allowed_types[-1])
        else:
            type_str = str(allowed_types)

        self.message = "{} expected {} {}, got {} of type {}".format(
            func_name, argname, type_str, arg, actual_type)
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
                num_str = (", ".join(["{}"]*(len(allowed_nums)-1))).format(*allowed_nums[:-1])
                # when merging, get rid of this one!
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

