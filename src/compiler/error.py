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
