class EvoSimError(Exception):
    pass


class EvoSimLexerError(EvoSimError):
    def __init__(self, char, line, column):
        super().__init__(f"invalid char '{char}' at line {line}, column {column}")

class EvoSimSyntaxError(EvoSimError):
    def __init__(self, token, line, column):
        super().__init__(
            f"syntax error at line {line} starting at column {column}: invalid token '{token.value}' with type '{token.type}'"
        )


class EvoSimVariableError(EvoSimError):
    def __init__(self, name):
        super().__init__(f"variable '{name}' doesn't exist")


class EvoSimFunctionError(EvoSimError):
    def __init__(self, message):
        super().__init__(message)

PARAMS_ERROR = lambda name, p, a: EvoSimFunctionError(
    f"function '{name}' expects {p} parameters and received {a} arguments when called"
)

FUNCTION_NOT_FOUND_ERROR = lambda name: EvoSimFunctionError(
    f"function '{name}' doesn't exist"
)

NOT_A_FUNCTION_ERROR = lambda name: EvoSimFunctionError(
    f"'{name}' is not a function"
)
