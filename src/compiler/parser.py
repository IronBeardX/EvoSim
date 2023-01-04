import src.compiler.ply.yacc as yacc
from src.compiler.lexer import tokens
from src.compiler.util import parse_number


def get_parser(*args, **kwargs):
    # program production
    def p_program(p):
        "program : expr"
        p[0] = p[1]

    # expr productions
    def p_expr_sum(p):
        "expr : expr '+' term"
        p[0] = p[1] + p[3]
    
    def p_expr_substr(p):
        "expr : expr '-' term"
        p[0] = p[1] - p[3]
    
    def p_expr_term(p):
        "expr : term"
        p[0] = p[1]
    
    def p_term_mult(p):
        "term : term '*' factor"
        p[0] = p[1] * p[3]
    
    def p_term_div(p):
        "term : term '/' factor"
        p[0] = p[1] / p[3]
    
    def p_term_rem(p):
        "term : term '%' factor"
        p[0] = p[1] % p[3]
    
    def p_term_intdiv(p):
        "term : term INTDIV factor"
        p[0] = p[1] // p[3]
    
    def p_term_factor(p):
        "term : factor"
        p[0] = p[1]
    
    def p_factor_number(p):
        "factor : NUMBER"
        p[0] = parse_number(p[1])
    
    def p_factor_group(p):
        "factor : '(' expr ')'"
        p[0] = p[2]

    return yacc.yacc(*args, **kwargs)
