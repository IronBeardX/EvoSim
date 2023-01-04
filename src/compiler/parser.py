import src.compiler.ply.yacc as yacc
from src.compiler.lexer import tokens
from src.compiler.util import parse_number
from math import pow, sqrt


def get_parser(*args, **kwargs):
    # program production
    def p_program(p):
        "program : expr"
        p[0] = p[1]
    
    # epsilon production
    def p_epsilon(p):
        "epsilon :"
        pass

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
    
    def p_factor_negative(p):
        "factor : '-' factor"
        p[0] = -1 * p[2]
    
    def p_factor_power(p):
        "factor : power"
        p[0] = p[1]
    
    def p_power_power(p):
        "power : atom '^' factor"
        p[0] = pow(p[1], p[3])
    
    def p_power_root(p):
        "power : atom '@' factor"
        p[0] = sqrt(p[1]) if p[3] == 2 else pow(p[1], 1 / p[3])
    
    def p_power_atom(p):
        "power : atom"
        p[0] = p[1]
    
    def p_atom_number(p):
        "atom : NUMBER"
        p[0] = parse_number(p[1])
    
    def p_atom_group(p):
        "atom : '(' expr ')'"
        p[0] = p[2]

    return yacc.yacc(*args, **kwargs)
