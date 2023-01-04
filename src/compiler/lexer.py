import src.compiler.ply.lex as lex


literals = '+-*/%()^@<>'

reserved = {
    'or'   : 'OR',
    'and'  : 'AND',
    'not'  : 'NOT',
    'TRUE' : 'TRUE',
    'FALSE': 'FALSE'
}

tokens = (
    'INTDIV',
    'EQ',
    'NEQ',
    'GE',
    'LE',
    'NUMBER',
    *reserved.values(),
    'newline'
)

def get_lexer(*args, **kwargs):
    # token rules
    t_INTDIV = r'//'
    t_EQ     = r'=='
    t_NEQ    = r'!='
    t_GE     = r'>='
    t_LE     = r'<='
    t_NUMBER = r'-?(0|[1-9][0-9]*)(\.[0-9]*)?'

    # match reserved words then IDs
    # valid IDs start with letter, followed by letters, digits and underscore chars
    def t_ID(t):
        r'[a-zA-Z][a-zA-Z0-9_]*'
        t.type = reserved.get(t.value, 'ID')
        return t

    # match newline chars and record line count
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        return t

    # ignore tabs and spaces
    t_ignore = r' \t'

    return lex.lex(*args, **kwargs)
