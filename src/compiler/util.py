def parse_number(number_string, int_fisrt=True):
    first, second = (int, float) if int_fisrt else (float, int)

    try:
        number = first(number_string)
    except ValueError:
        number = second(number_string)
    finally:
        return number
