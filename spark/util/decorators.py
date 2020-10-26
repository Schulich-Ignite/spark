global_field_names = set()
def global_field(func):
    global global_field_names
    global_field_names.add(func.__name__)
    return func
