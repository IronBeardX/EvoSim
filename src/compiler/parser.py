from math import pow

import src.compiler.ply.yacc as yacc
from src.compiler.lexer import tokens
from src.compiler.util import parse_number, nth_root
from src.compiler.ast import (
    ValueNode,
    UnaryOpNode,
    BinaryOpNode,
    WorldNode,
    SimulationNode,
    PhyGeneNode
)



def get_parser(*args, **kwargs):
    # program production
    def p_program(p):
        "program : gene_stmt"
        p[0] = p[1]
    
    # handy productions
    def p_epsilon(p):
        "epsilon :"
        pass

    def p_maybe_newline(p):
        "maybe_newline : newline"
        p[0] = p[1]
    
    def p_maybe_epsilon(p):
        "maybe_newline : epsilon"
        pass

    # gene stmt productions
    def p_gene(p):
        "gene_stmt : GENE phygene_stmt"
        p[0] = p[2]

    def p_phygene_stmt(p):
        "phygene_stmt : phygene '{' maybe_newline phygeneprop maybe_newline phygeneprop maybe_newline '}'"
        p[0] = PhyGeneNode({**p[1], **p[4], **p[6]})
    
    def p_phygene(p):
        '''phygene : HEALTH
                   | HUNGER
                   | LEGS
                   | EYES
                   | ARMS
                   | HORNS
                   | SMELL
                   | FINS
                   | NOSE
                   | MOUTH'''
        p[0] = {"class": p[1]}

    def p_phygeneprop_value(p):
        "phygeneprop : VALUE NUMBER IN '{' NUMBER NUMBER '}'"
        m, mx = parse_number(p[5]), parse_number(p[6])
        p[0] = {"value": (parse_number(2), {"min": m, "max": mx})}
    
    def p_phygeneprop_mutation(p):
        "phygeneprop : MUTATION '{' maybe_newline mutationprop maybe_newline mutationprop maybe_newline '}'"
        p[0] = {"mutation": {**p[4], **p[6]}}
    
    def p_mutationprop(p):
        '''mutationprop : CHANCE NUMBER
                        | STEP NUMBER'''
        p[0] = {p[1]: parse_number(p[2])}

    # world stmt productions
    def p_world(p):
        "world_stmt : WORLD '{' maybe_newline worldprop maybe_newline worldprop maybe_newline '}'"
        p[0] = WorldNode({**p[4], **p[6]})
    
    def p_worldprop(p):
        '''worldprop : SIZE worldsize
                     | TERRAIN worldterrain'''
        p[0] = p[2]
    
    def p_worldsize_infinite(p):
        "worldsize : INFINITE"
        p[0] = {"size": (True, {"width": -1, "height": -1})}
    
    def p_worldsize(p):
        "worldsize : '{' maybe_newline worldsizeprop maybe_newline worldsizeprop maybe_newline '}'"
        p[0] = {"size": (False, {**p[3], **p[5]})}
    
    def p_worldsizeprop(p):
        '''worldsizeprop : WIDTH NUMBER
                         | HEIGHT NUMBER'''
        p[0] = {p[1]: parse_number(p[2])}
    
    def p_worldterrain(p):
        "worldterrain : '{' maybe_newline terrainprop_list '}'"
        p[0] = {"terrain": p[3]}

    def p_terrainprop_list(p):
        "terrainprop_list : terrainprop maybe_newline terrainprop_list"
        p[0] = [p[1], *p[3]]
    
    def p_terrainprop_list_epsilon(p):
        "terrainprop_list : epsilon"
        p[0] = []
    
    def p_terrainprop(p):
        "terrainprop : ID"
        p[0] = (p[1], False, [])
    
    def p_terrainprop_default(p):
        "terrainprop : DEFAULT ID"
        p[0] = (p[2], True, [])
    
    def p_terrainprop_at(p):
        "terrainprop : ID AT '{' maybe_newline NUMBER maybe_newline terrainposn_list '}'"
        p[0] = (p[1], False, [parse_number(p[5]), *p[7]])
    
    def p_terrainposn_list(p):
        "terrainposn_list : NUMBER maybe_newline terrainposn_list"
        p[0] = [parse_number(p[1]), *p[3]]
    
    def p_terrainposn_list_epsilon(p):
        "terrainposn_list : epsilon"
        p[0] = []
    
    # simulation stmt productions
    def p_sim(p):
        "sim_stmt : SIMULATION '{' maybe_newline simprop maybe_newline simprop maybe_newline simprop maybe_newline '}'"
        p[0] = SimulationNode({**p[4], **p[6], **p[8]})
    
    def p_simprop(p):
        '''simprop : EPISODES NUMBER
                   | MAX_ROUNDS NUMBER'''
        p[0] = {p[1]: parse_number(p[2])}
    
    def p_simprop_stop(p):
        "simprop : STOP IF disjunction"
        p[0] = {'stop': p[3]}

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
