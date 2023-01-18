from math import pow

import src.compiler.ply.yacc as yacc
from src.compiler.lexer import tokens
from src.compiler.util import parse_number, nth_root
from src.compiler.ast import (
    ValueNode, UnaryOpNode, BinaryOpNode, VariableNode,
    WorldNode, SimulationNode,
    PhyGeneNode, PerceptionGeneNode, ActionGeneNode, DNAChainNode,
    IfNode, ElseNode,
    VariableSettingNode,
    LoopNode, ContinueNode, BreakNode,
    FunctionNode, FunctionCallNode, ReturnNode,
    ProgramNode
)



def get_parser(*args, **kwargs):
    # program production
    def p_program(p):
        "program : gene_stmt_list dna_stmt_list world_stmt newline sim_stmt maybe_newline"
        p[0] = ProgramNode(p[1], p[2], p[3], p[5])
    
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

    # generic stmt productions
    def p_stmt_list(p):
        "stmt_list : stmt newline stmt_list"
        p[0] = [p[1], *p[3]]
    
    def p_stmt_list_epsilon(p):
        "stmt_list : epsilon"
        p[0] = []
    
    def p_stmt(p):
        '''stmt : if_stmt
                | var_stmt
                | loop_stmt'''
        p[0] = p[1]
    
    def p_stmt_continue(p):
        "stmt : CONTINUE"
        p[0] = ContinueNode()
    
    def p_stmt_break(p):
        "stmt : BREAK"
        p[0] = BreakNode()
    
    def p_stmt_return(p):
        "stmt : RETURN disjunction"
        p[0] = ReturnNode(p[2])
    
    def p_stmt_return_epsilon(p):
        "stmt : RETURN epsilon"
        p[0] = ReturnNode(None)
    
    # program-related stmt productions
    def p_gene_stmt_list(p):
        "gene_stmt_list : gene_stmt newline gene_stmt_list"
        p[0] = [p[1], *p[3]]
    
    def p_gene_stmt_list_epsilon(p):
        "gene_stmt_list : epsilon"
        p[0] = []
    
    def p_dna_stmt_list(p):
        "dna_stmt_list : dna_stmt newline dna_stmt_list"
        p[0] = [p[1], *p[3]]
    
    def p_dna_stmt_list_epsilon(p):
        "dna_stmt_list : epsilon"
        p[0] = []

    # gene stmt productions
    def p_gene(p):
        '''gene_stmt : GENE phygene_stmt
                     | GENE percpgene
                     | GENE actgene'''
        p[0] = p[2]
    
    def p_percpgene(p):
        '''percpgene : SMELLING
                     | VISION'''
        p[0] = PerceptionGeneNode(p[1])
    
    def p_actgene(p):
        '''actgene : MOVE
                   | EAT
                   | REPRODUCE
                   | ATTACK
                   | DEFEND
                   | PICK
                   | SWIM'''
        p[0] = ActionGeneNode(p[1])

    def p_phygene_stmt(p):
        "phygene_stmt : phygene ID '{' maybe_newline phygeneprop maybe_newline phygeneprop maybe_newline '}'"
        p[0] = PhyGeneNode({**p[1], 'name': p[2] , **p[5], **p[7]})
    
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
    
    # dna chain stmt productions
    def p_dna_stmt(p):
        "dna_stmt : DNA ID '{' maybe_newline dna_elem_list '}'"
        p[0] = DNAChainNode(p[2], p[5])
    
    def p_dna_elem_list(p):
        "dna_elem_list : dna_elem maybe_newline dna_elem_list"
        p[0] = [p[1], *p[3]]
    
    def p_dna_elem_list_epsilon(p):
        "dna_elem_list : epsilon"
        p[0] = []
    
    def p_dna_elem_act(p):
        "dna_elem : actgene"
        p[0] = {"type": "gene", "class": "action", "name": p[1]}
    
    def p_dna_elem_perp(p):
        "dna_elem : percpgene"
        p[0] = {"type": "gene", "class": "perception", "name": p[1]}
    
    def p_dna_elem_phy(p):
        "dna_elem : ID"
        p[0] = {"type": "gene", "class": "physical", "name": p[1]}
    
    def p_dna_elem_dna(p):
        "dna_elem : DNA ID"
        p[0] = {"type": "dna", "name": p[2]}

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
        "sim_stmt : SIMULATION '{' maybe_newline simprop maybe_newline simprop maybe_newline simprop maybe_newline simprop maybe_newline simprop maybe_newline '}'"
        p[0] = SimulationNode({**p[4], **p[6], **p[8], **p[10], **p[12]})
    
    def p_simprop(p):
        '''simprop : EPISODES NUMBER
                   | MAX_ROUNDS NUMBER
                   | ACTIONS_TIME NUMBER'''
        p[0] = {p[1]: parse_number(p[2])}
    
    def p_simprop_stop(p):
        "simprop : STOP IF disjunction"
        p[0] = {'stop': p[3]}
    
    def p_simprop_commands(p):
        "simprop : AVAILABLE_COMMANDS '{' maybe_newline command_list '}'"
        p[0] = {p[1]: p[4]}
    
    def p_command_list(p):
        "command_list : ID maybe_newline command_list"
        p[0] = [p[1], *p[3]]
    
    def p_command_list_epsilon(p):
        "command_list : epsilon"
        p[0] = []
    
    # var setting stmt
    def p_var(p):
        "var_stmt : ID '=' disjunction"
        p[0] = VariableSettingNode(p[1], p[3])
    
    # if-else stmt productions
    def p_if(p):
        "if_stmt : IF disjunction '{' maybe_newline stmt_list '}' else_stmt"
        p[0] = IfNode(p[2], p[5], p[7])

    def p_else_if(p):
        "else_stmt : ELSE if_stmt"
        p[0] = p[2]
    
    def p_else(p):
        "else_stmt : ELSE '{' maybe_newline stmt_list '}'"
        p[0] = ElseNode(p[4])

    def p_else_epsilon(p):
        "else_stmt : epsilon"
        p[0] = None
    
    # loop stmt productions
    def p_loop(p):
        "loop_stmt : LOOP loop_init ',' loop_condition ',' loop_set '{' maybe_newline stmt_list '}'"
        p[0] = LoopNode(p[2], p[4], p[6], p[9])

    def p_loop_init(p):
        "loop_init : var_stmt"
        p[0] = p[1]
    
    def p_loop_init_epsilon(p):
        "loop_init : epsilon"
        p[0] = None
    
    def p_loop_set(p):
        "loop_set : var_stmt"
        p[0] = p[1]
    
    def p_loop_set_epsilon(p):
        "loop_set : epsilon"
        p[0] = None
    
    def p_loop_cond(p):
        "loop_condition : disjunction"
        p[0] = p[1]
    
    def p_loop_cond_epsilon(p):
        "loop_condition : epsilon"
        p[0] = None
    
    # function declaration stmt productions
    def p_func(p):
        "func_stmt : FUNC ID '=' param_list '{' maybe_newline stmt_list '}'"
        p[0] = FunctionNode(p[2], p[4], p[7])
    
    def p_param_list(p):
        "param_list : ID param_list"
        p[0] = [p[1], *p[2]]
    
    def p_param_list_epsilon(p):
        "param_list : epsilon"
        p[0] = []

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
    
    def p_atom_var(p):
        "atom : ID"
        p[0] = VariableNode(p[1])
    
    def p_atom_function(p):
        "atom : ID '(' arg_list ')'"
        p[0] = FunctionCallNode(p[1], p[3])
    
    def p_atom_group(p):
        "atom : '(' expr ')'"
        p[0] = p[2]
    
    def p_arg_list(p):
        "arg_list : disjunction rest_args"
        p[0] = [p[1], *p[2]]
    
    def p_arg_list_epsilon(p):
        "arg_list : epsilon"
        p[0] = []
    
    def p_rest_args(p):
        "rest_args : ',' disjunction rest_args"
        p[0] = [p[2], *p[3]]
    
    def p_rest_args_epsilon(p):
        "rest_args : epsilon"
        p[0] = []

    return yacc.yacc(*args, **kwargs)
