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
    def __init__(self, message):
        super().__init__(message)

VAR_NOT_FOUND_ERROR = lambda name: EvoSimVariableError(
    f"'{name}' variable doesn't exist"
)

PROP_NOT_IN_VAR_ERROR = lambda var_name, name: EvoSimVariableError(
    f"'{name}' property not found in '{var_name}' variable"
)

NOT_A_LIST_ERROR = lambda: EvoSimVariableError(
    f"the variable is not a list or a string"
)

BAD_LIST_INDEXER_ERROR = lambda value: EvoSimVariableError(
    f"'{value}' key is not an integer"
)

KEY_NOT_IN_DICT_ERROR = lambda value: EvoSimVariableError(
    f"'{value}' key not found in dictionary"
)

NOT_A_DICT_ERROR = lambda: EvoSimVariableError(
    f"the variable is not a dictionary"
)

BAD_INDEXER_ERROR = lambda value: EvoSimVariableError(
    f"dictionary not indexable by '{value}'"
)


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
