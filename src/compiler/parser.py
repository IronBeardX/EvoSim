from math import pow

import src.compiler.ply.yacc as yacc
from src.compiler.lexer import tokens
from src.compiler.util import parse_number, nth_root
from src.compiler.ast import ValueNode, UnaryOpNode, BinaryOpNode



def get_parser(*args, **kwargs):
    # program production
    def p_program(p):
        "program : disjunction"
        p[0] = p[1]
    
    # epsilon production
    def p_epsilon(p):
        "epsilon :"
        pass

    # boolean expr productions
    def p_disjunction(p):
        "disjunction : conjunction OR conjunction"
        p[0] = BinaryOpNode(p[1], p[3], lambda x,y: x or y)
    
    def p_disjunction_conjunction(p):
        "disjunction : conjunction"
        p[0] = p[1]
    
    def p_conjunction(p):
        "conjunction : negation AND negation"
        p[0] = BinaryOpNode(p[1], p[3], lambda x,y: x and y)
    
    def p_conjunction_negation(p):
        "conjunction : negation"
        p[0] = p[1]
    
    def p_negation(p):
        "negation : NOT comparison"
        p[0] = UnaryOpNode(p[2], lambda x: not x)
    
    def p_negation_comparison(p):
        "negation : comparison"
        p[0] = p[1]

    # comparison expr productions
    def p_comparison_eq(p):
        "comparison : expr EQ expr"
        p[0] = BinaryOpNode(p[1], p[3], lambda x,y: x == y)
    
    def p_comparison_neq(p):
        "comparison : expr NEQ expr"
        p[0] = BinaryOpNode(p[1], p[3], lambda x,y: x != y)
    
    def p_comparison_ge(p):
        "comparison : expr GE expr"
        p[0] = BinaryOpNode(p[1], p[3], lambda x,y: x >= y)
    
    def p_comparison_le(p):
        "comparison : expr LE expr"
        p[0] = BinaryOpNode(p[1], p[3], lambda x,y: x <= y)
    
    def p_comparison_gt(p):
        "comparison : expr '>' expr"
        p[0] = BinaryOpNode(p[1], p[3], lambda x,y: x > y)
    
    def p_comparison_lt(p):
        "comparison : expr '<' expr"
        p[0] = BinaryOpNode(p[1], p[3], lambda x,y: x < y)
    
    def p_comparison_expr(p):
        "comparison : expr"
        p[0] = p[1]

    # expr productions
    def p_expr_sum(p):
        "expr : expr '+' term"
        p[0] = BinaryOpNode(p[1], p[3], lambda x,y: x + y)
    
    def p_expr_substr(p):
        "expr : expr '-' term"
        p[0] = BinaryOpNode(p[1], p[3], lambda x,y: x - y)
    
    def p_expr_term(p):
        "expr : term"
        p[0] = p[1]
    
    def p_term_mult(p):
        "term : term '*' factor"
        p[0] = BinaryOpNode(p[1], p[3], lambda x,y: x * y)
    
    def p_term_div(p):
        "term : term '/' factor"
        p[0] = BinaryOpNode(p[1], p[3], lambda x,y: x / y)
    
    def p_term_rem(p):
        "term : term '%' factor"
        p[0] = BinaryOpNode(p[1], p[3], lambda x,y: x % y)
    
    def p_term_intdiv(p):
        "term : term INTDIV factor"
        p[0] = BinaryOpNode(p[1], p[3], lambda x,y: x // y)
    
    def p_term_factor(p):
        "term : factor"
        p[0] = p[1]
    
    def p_factor_negative(p):
        "factor : '-' factor"
        p[0] = UnaryOpNode(p[2], lambda x: -1 * x)
    
    def p_factor_power(p):
        "factor : power"
        p[0] = p[1]
    
    def p_power_power(p):
        "power : atom '^' factor"
        p[0] = BinaryOpNode(p[1], p[3], lambda x,y: pow(x, y))
    
    def p_power_root(p):
        "power : atom '@' factor"
        p[0] = BinaryOpNode(p[1], p[3], lambda x,y: nth_root(x, y))
    
    def p_power_atom(p):
        "power : atom"
        p[0] = p[1]
    
    def p_atom_number(p):
        "atom : NUMBER"
        p[0] = ValueNode(parse_number(p[1]))
    
    def p_atom_false(p):
        "atom : FALSE"
        p[0] = ValueNode(False)
    
    def p_atom_true(p):
        "atom : TRUE"
        p[0] = ValueNode(True)
    
    def p_atom_group(p):
        "atom : '(' expr ')'"
        p[0] = p[2]

    return yacc.yacc(*args, **kwargs)
