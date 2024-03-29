import src.compiler.ply.lex as lex
from src.compiler.util import token_column
from src.compiler.error import EvoSimLexerError


literals = '+-*/%()^@<{>}=,.[];'

reserved = {
    'or'                : 'OR',
    'and'               : 'AND',
    'not'               : 'NOT',
    'world'             : 'WORLD',
    'width'             : 'WIDTH',
    'height'            : 'HEIGHT',
    'infinite'          : 'INFINITE',
    'default'           : 'DEFAULT',
    'at'                : 'AT',
    'size'              : 'SIZE',
    'terrain'           : 'TERRAIN',
    'simulation'        : 'SIMULATION',
    'episodes'          : 'EPISODES',
    'max_rounds'        : 'MAX_ROUNDS',
    'stop'              : 'STOP',
    'if'                : 'IF',
    'else'              : 'ELSE',
    'loop'              : 'LOOP',
    'continue'          : 'CONTINUE',
    'break'             : 'BREAK',
    'func'              : 'FUNC',
    'return'            : 'RETURN',
    'true'              : 'TRUE',
    'false'             : 'FALSE',
    'gene'              : 'GENE',
    'health'            : 'HEALTH',
    'hunger'            : 'HUNGER',
    'legs'              : 'LEGS',
    'eyes'              : 'EYES',
    'arms'              : 'ARMS',
    'horns'             : 'HORNS',
    'smell'             : 'SMELL',
    'fins'              : 'FINS',
    'nose'              : 'NOSE',
    'mouth'             : 'MOUTH',
    'smelling'          : 'SMELLING',
    'vision'            : 'VISION',
    'move'              : 'MOVE',
    'eat'               : 'EAT',
    'reproduce'         : 'REPRODUCE',
    'attack'            : 'ATTACK',
    'defend'            : 'DEFEND',
    'pick'              : 'PICK',
    'swim'              : 'SWIM',
    'value'             : 'VALUE',
    'in'                : 'IN',
    'mutation'          : 'MUTATION',
    'chance'            : 'CHANCE',
    'step'              : 'STEP',
    'actions_time'      : 'ACTIONS_TIME',
    'available_commands': 'AVAILABLE_COMMANDS',
    'dna'               : 'DNA',
    'cost'              : 'COST',
    'repr'              : 'REPR',
    'coexistence'       : 'COEXISTENCE',
    'entity'            : 'ENTITY',
    'behavior'          : 'BEHAVIOR',
    'decide'            : 'DECIDE',
    'time'              : 'TIME',
    'organism'          : 'ORGANISM',
    'keys'              : 'KEYS'
}

tokens = (
    'INTDIV',
    'EQ',
    'NEQ',
    'GE',
    'LE',
    'NUMBER',
    'STRING',
    'ID',
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
    t_STRING = r"'[^']*'"

    # match reserved words then IDs
    # valid IDs start with letter, followed by letters, digits and underscore chars
    def t_ID(t):
        r'[a-zA-Z][a-zA-Z0-9_]*'
        
        # fix lexer ignoring 't' as first letter
        if t.value in ['errain', 'rue', 'ime']:
            t.value = f't{t.value}'
        
        t.type = reserved.get(t.value, 'ID')
        return t

    # match newline chars and record line count
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        pass

    # ignore tabs and spaces
    t_ignore = r' \t'

    # handle errors
    def t_error(t):
        column = token_column(t.lexer.lexdata, t)
        raise EvoSimLexerError(t.value[0], t.lexer.lineno, column)

    return lex.lex(*args, **kwargs)
