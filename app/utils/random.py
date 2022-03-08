import random
import string

def random_string(length, type_string=None):
    if type_string == 'uppercase':
      type_string= string.ascii_uppercase
    elif type_string == 'lowercase':
      type_string= string.ascii_uppercase
    else:
      type_string= string.ascii_letters

    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return result_str

def random_string_number(length, type_string=None):
    if type_string == 'uppercase':
      type_string= string.ascii_uppercase
    elif type_string == 'lowercase':
      type_string= string.ascii_uppercase
    else:
      type_string= string.ascii_letters

    result_str = ''.join(random.choice(string.ascii_letters+ string.digits) for i in range(length))
    return result_str


def random_number(length):
    result_str = ''.join(random.choice(string.digits) for i in range(length))
    return result_str
