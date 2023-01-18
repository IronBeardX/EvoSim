from math import sqrt, pow


class Signal(Exception):
    pass

BREAK = Signal()

class ValueSignal(Exception):
    def __init__(self, value):
        super().__init__()
        self.value = value


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

def token_column(input_data, token):
    line_start = input_data.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1
