def camel_case_name(name: str):
    return ' '.join([ str.upper(x[0]) + str.lower(x[1:]) for x in name.split(' ')])