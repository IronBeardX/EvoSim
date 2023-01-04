import src.compiler.ply.lex as lex


literals = '+-*/%()^@'

tokens = ('INTDIV', 'NUMBER', 'newline')

def get_lexer(*args, **kwargs):
    # token rules
    t_INTDIV = r'//'
    t_NUMBER = r'-?(0|[1-9][0-9]*)(\.[0-9]*)?'

    # match newline chars and record line count
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        return t

    # ignore tabs and spaces
    t_ignore = r' \t'

    return lex.lex(*args, **kwargs)
