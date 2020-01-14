

# convert javascript style variable names to python style.
# the suggested solution uses re which fails to work on the javascript python compiler:
# **************************************************************
# import re
# def camel_case_to_snake_case(name):
#     s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
#     return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
# **************************************************************
# hence I cooked up this magnificent pythonic alternative:
def camel_case_to_snake_case(name):
    return "".join(["_" + letter.lower() if letter.isupper() else letter for letter in name]).lstrip('_')
