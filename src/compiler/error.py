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


class EvoSimTypeError(EvoSimError):
    def __init__(self, variable_name, expected_type):
        super().__init__(f'variable {variable_name} must have type {expected_type}')
    

class EvoSimVariableError(EvoSimError):
    def __init__(self, message):
        super().__init__(message)

VAR_NOT_FOUND_ERROR = lambda name: EvoSimVariableError(
    f"'{name}' variable doesn't exist"
)

INVALID_GENE_VALUE_ERROR = lambda value: EvoSimVariableError(
    f"'{value}' is an valid value for gene"
)

INVALID_GENE_STEP_ERROR = lambda value: EvoSimVariableError(
    f"'{value}' is an valid step for gene."
)

MUTATION_CHANCE_ERROR = lambda value: EvoSimVariableError(
    f'Mutation chance must be a number between 0 and 1, not "{value}"'
)

PROP_NOT_IN_VAR_ERROR = lambda var_name, name: EvoSimVariableError(
    f"'{name}' property not found in '{var_name}' variable"
)

BAD_LIST_INDEXER_ERROR = lambda value: EvoSimVariableError(
    f"'{value}' key is not an integer"
)

KEY_NOT_IN_DICT_ERROR = lambda value: EvoSimVariableError(
    f"'{value}' key not found in dictionary"
)

BAD_INDEXER_ERROR = lambda value: EvoSimVariableError(
    f"dictionary not indexable by '{value}'"
)

NOT_INDEXABLE_ERROR = lambda store: EvoSimVariableError(
    f"'{store}' variable not a dictionary, list or string"
)

INDEX_ASSIGNMENT_ERROR = lambda store: EvoSimVariableError(
    f"'{store}' do not support index assignment"
)

NOT_A_DICT_ERROR = lambda store: EvoSimVariableError(
    f"'{store}' is not a dictionary"
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
