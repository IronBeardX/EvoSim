from math import sqrt, pow


class Signal(Exception):
    pass

BREAK = Signal()

def parse_number(number_string, int_fisrt=True):
    first, second = (int, float) if int_fisrt else (float, int)

    try:
        number = first(number_string)
    except ValueError:
        number = second(number_string)
    finally:
        return number

def nth_root(n, root):
    return sqrt(n) if root == 2 else pow(n, 1 / root)
