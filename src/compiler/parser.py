import src.compiler.ply.yacc as yacc
from src.compiler.lexer import tokens
from src.compiler.util import parse_number, nth_root
from math import pow


def get_parser(*args, **kwargs):
    # program production
    def p_program(p):
        "program : comparison"
        p[0] = p[1]
    
    # epsilon production
    def p_epsilon(p):
        "epsilon :"
        pass

    # comparison expr productions
    def p_comparison_eq(p):
        "comparison : expr EQ expr"
        p[0] = p[1] == p[3]
    
    def p_comparison_neq(p):
        "comparison : expr NEQ expr"
        p[0] = p[1] != p[3]
    
    def p_comparison_ge(p):
        "comparison : expr GE expr"
        p[0] = p[1] >= p[3]
    
    def p_comparison_le(p):
        "comparison : expr LE expr"
        p[0] = p[1] <= p[3]
    
    def p_comparison_gt(p):
        "comparison : expr '>' expr"
        p[0] = p[1] > p[3]
    
    def p_comparison_lt(p):
        "comparison : expr '<' expr"
        p[0] = p[1] < p[3]

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
        p[0] = nth_root(p[1], p[3])
    
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
