from math import pow

import src.compiler.ply.yacc as yacc
from src.compiler.lexer import tokens
from src.compiler.util import parse_number, nth_root, token_column
from src.compiler.error import EvoSimSyntaxError
from src.compiler.ast import (
    ValueNode, UnaryOpNode, BinaryOpNode, VariableNode,
    ListNode, DictNode, IndexNode, KeysNode,
    WorldNode, SimulationNode, EntityNode, OrganismNode, BehaviorNode,
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
        "program : gene_stmt_list dna_stmt_list behavior_stmt_list entity_org_stmt_list world_stmt sim_stmt"
        p[0] = ProgramNode(p[1], p[2], p[3], p[4], p[5], p[6])
    
    # handy productions
    def p_epsilon(p):
        "epsilon :"
        pass

    def p_test(p):
        "test : program"
        p[0] = p[1]

    # handle errors
    def p_error(t):
        if t:
            column = token_column(t.lexer.lexdata, t)
            raise EvoSimSyntaxError(t, t.lexer.lineno, column)
    
    # gene stmt productions
    def p_gene_stmt_list(p):
        "gene_stmt_list : gene_stmt gene_stmt_list"
        p[0] = [p[1], *p[2]]
    
    def p_gene_stmt_list_epsilon(p):
        "gene_stmt_list : epsilon"
        p[0] = []

    def p_gene(p):
        '''gene_stmt : GENE phygene_stmt
                     | GENE percpgene
                     | GENE actgene_stmt'''
        p[0] = p[2]
    
    def p_percpgene(p):
        '''percpgene : SMELLING
                     | VISION'''
        p[0] = PerceptionGeneNode(p[1])
    
    def p_actgene_stmt(p):
        "actgene_stmt : actgene ID '{' COST NUMBER '}'"
        p[0] = ActionGeneNode({**p[1], "name": p[2], p[4]: p[5]})
    
    def p_actgene(p):
        '''actgene : MOVE
                   | EAT
                   | REPRODUCE
                   | ATTACK
                   | DEFEND
                   | PICK
                   | SWIM'''
        p[0] = {"class": p[1]}

    def p_phygene_stmt(p):
        "phygene_stmt : phygene ID '{' phygeneprop phygeneprop '}'"
        p[0] = PhyGeneNode({**p[1], 'name': p[2] , **p[4], **p[5]})
    
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
        "phygeneprop : MUTATION '{' mutationprop mutationprop '}'"
        p[0] = {"mutation": {**p[3], **p[4]}}
    
    def p_mutationprop(p):
        '''mutationprop : CHANCE NUMBER
                        | STEP NUMBER'''
        p[0] = {p[1]: parse_number(p[2])}
    
    # dna chain stmt productions
    def p_dna_stmt_list(p):
        "dna_stmt_list : dna_stmt dna_stmt_list"
        p[0] = [p[1], *p[2]]
    
    def p_dna_stmt_list_epsilon(p):
        "dna_stmt_list : epsilon"
        p[0] = []
    
    def p_dna_stmt(p):
        "dna_stmt : DNA ID '{' dna_elem_list '}'"
        p[0] = DNAChainNode(p[2], p[4])
    
    def p_dna_elem_list(p):
        "dna_elem_list : dna_elem dna_elem_list"
        p[0] = [p[1], *p[2]]
    
    def p_dna_elem_list_epsilon(p):
        "dna_elem_list : epsilon"
        p[0] = []
    
    def p_dna_elem_gene(p):
        '''dna_elem : ID
                    | SMELLING
                    | VISION'''
        p[0] = {"type": "gene", "name": p[1]}
    
    def p_dna_elem_dna(p):
        "dna_elem : DNA ID"
        p[0] = {"type": "dna", "name": p[2]}
    
    # behavior stmt productions
    def p_behavior_stmt_list(p):
        "behavior_stmt_list : behavior_stmt behavior_stmt_list"
        p[0] = [p[1], *p[2]]
    
    def p_behavior_stmt_list_epsilon(p):
        "behavior_stmt_list : epsilon"
        p[0] = []

    def p_behavior_stmt(p):
        "behavior_stmt : BEHAVIOR ID '{' func_stmt_list decide_stmt '}'"
        p[0] = BehaviorNode(p[2], p[4], p[5])
    
    def p_behavior_stmt_epsilon(p):
        "behavior_stmt : BEHAVIOR ID"
        p[0] = BehaviorNode(p[2], [], None)

    def p_decide_stmt(p):
        "decide_stmt : DECIDE ORGANISM TIME '{' stmt_list '}'"
        p[0] = FunctionNode(p[1], [p[2], p[3]], p[5])
    
    # entity and organism stmt productions
    def p_entity_org_stmt_list(p):
        '''entity_org_stmt_list : entity_stmt entity_org_stmt_list
                                | organism_stmt entity_org_stmt_list'''
        p[0] = [p[1], *p[2]]
    
    def p_entity_org_stmt_list_epsilon(p):
        "entity_org_stmt_list : epsilon"
        p[0] = []

    def p_entity_stmt(p):
        "entity_stmt : ENTITY '{' entityprop entityprop entityprop '}'"
        p[0] = EntityNode({**p[3], **p[4], **p[5]})

    def p_entityprop_coex(p):
        "entityprop : COEXISTENCE bool"
        p[0] = {p[1]: p[2] == 'true'}
    
    def p_entityprop_repr(p):
        "entityprop : REPR ID"
        p[0] = {'representation': p[2]}
    
    def p_entityprop_position(p):
        "entityprop : AT '{' position position_list '}'"
        p[0] = {'positions': [p[3], *p[4]]}
    
    def p_organism_stmt(p):
        "organism_stmt : ORGANISM '{' orgprop orgprop orgprop orgprop '}'"
        p[0] = OrganismNode({**p[3], **p[4], **p[5], **p[6]})

    def p_orgprop_dna(p):
        '''orgprop : DNA ID
                   | BEHAVIOR ID'''
        p[0] = {p[1]: p[2]}
    
    def p_orgprop_repr(p):
        "orgprop : REPR ID"
        p[0] = {'representation': p[2]}
    
    def p_orgprop_position(p):
        "orgprop : AT '{' position position_list '}'"
        p[0] = {'positions': [p[3], *p[4]]}

    def p_position_list(p):
        "position_list : position position_list"
        p[0] = [p[1], *p[2]]
    
    def p_position_list_epsilon(p):
        "position_list : epsilon"
        p[0] = []
    
    def p_position(p):
        "position : '(' NUMBER NUMBER ')'"
        p[0] = (parse_number(p[2]), parse_number(p[3]))
    
    # world stmt productions
    def p_world(p):
        "world_stmt : WORLD '{' worldprop worldprop '}'"
        p[0] = WorldNode({**p[3], **p[4]})
    
    def p_worldprop(p):
        '''worldprop : SIZE worldsize
                     | TERRAIN worldterrain'''
        p[0] = p[2]
    
    def p_worldsize_infinite(p):
        "worldsize : INFINITE '{' worldsizeprop worldsizeprop '}'"
        p[0] = {"size": (True, {**p[3], **p[4]})}
    
    def p_worldsize(p):
        "worldsize : '{' worldsizeprop worldsizeprop '}'"
        p[0] = {"size": (False, {**p[2], **p[3]})}
    
    def p_worldsizeprop(p):
        '''worldsizeprop : WIDTH NUMBER
                         | HEIGHT NUMBER'''
        p[0] = {p[1]: parse_number(p[2])}
    
    def p_worldterrain(p):
        "worldterrain : '{' terrainprop_list '}'"
        p[0] = {"terrain": p[2]}

    def p_terrainprop_list(p):
        "terrainprop_list : terrainprop terrainprop_list"
        p[0] = [p[1], *p[2]]
    
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
        "terrainprop : ID AT '{' NUMBER terrainposn_list '}'"
        p[0] = (p[1], False, [parse_number(p[4]), *p[5]])
    
    def p_terrainposn_list(p):
        "terrainposn_list : NUMBER terrainposn_list"
        p[0] = [parse_number(p[1]), *p[2]]
    
    def p_terrainposn_list_epsilon(p):
        "terrainposn_list : epsilon"
        p[0] = []
    
    # simulation stmt productions
    def p_sim(p):
        "sim_stmt : SIMULATION '{' simprop simprop simprop simprop simprop '}'"
        p[0] = SimulationNode({**p[3], **p[4], **p[5], **p[6], **p[7]})
    
    def p_simprop(p):
        '''simprop : EPISODES NUMBER
                   | MAX_ROUNDS NUMBER
                   | ACTIONS_TIME NUMBER'''
        p[0] = {p[1]: parse_number(p[2])}
    
    def p_simprop_stop(p):
        "simprop : STOP SIMULATION '{' stmt_list '}'"
        p[0] = {p[1]: FunctionNode(p[1], [p[2]], p[4])}
    
    def p_simprop_commands(p):
        "simprop : AVAILABLE_COMMANDS '{' command_list '}'"
        p[0] = {p[1]: p[3]}
    
    def p_command_list(p):
        "command_list : ID command_list"
        p[0] = [p[1], *p[2]]
    
    def p_command_list_epsilon(p):
        "command_list : epsilon"
        p[0] = []
    
    # function declaration stmt productions
    def p_func_list(p):
        "func_stmt_list : func_stmt func_stmt_list"
        p[0] = [p[1], *p[2]]
    
    def p_func_list_epsilon(p):
        "func_stmt_list : epsilon"
        p[0] = []

    def p_func(p):
        "func_stmt : FUNC ID '=' param_list '{' stmt_list '}'"
        p[0] = FunctionNode(p[2], p[4], p[6])
    
    def p_param_list(p):
        "param_list : ID param_list"
        p[0] = [p[1], *p[2]]
    
    def p_param_list_epsilon(p):
        "param_list : epsilon"
        p[0] = []

    # generic stmt productions
    def p_stmt_list(p):
        "stmt_list : stmt stmt_list"
        p[0] = [p[1], *p[2]]
    
    def p_stmt_list_epsilon(p):
        "stmt_list : epsilon"
        p[0] = []
    
    def p_stmt(p):
        '''stmt : if_stmt
                | var_stmt ';'
                | index_stmt ';'
                | disjunction ';'
                | loop_stmt'''
        p[0] = p[1]
    
    def p_stmt_continue(p):
        "stmt : CONTINUE ';'"
        p[0] = ContinueNode()
    
    def p_stmt_break(p):
        "stmt : BREAK ';'"
        p[0] = BreakNode()
    
    def p_stmt_return(p):
        "stmt : RETURN disjunction ';'"
        p[0] = ReturnNode(p[2])
    
    def p_stmt_return_epsilon(p):
        "stmt : RETURN ';'"
        p[0] = ReturnNode(None)
    
    # var setting stmt production
    def p_var_stmt(p):
        "var_stmt : accessing '=' disjunction"
        p[0] = VariableSettingNode(p[1], p[3])
    
    # index stmt production
    def p_index_stmt(p):
        "index_stmt : naming '[' disjunction ']' '=' disjunction"
        p[0] = IndexNode(p[1], p[3], p[6])
    
    # if-else stmt productions
    def p_if(p):
        "if_stmt : IF disjunction '{' stmt_list '}' else_stmt"
        p[0] = IfNode(p[2], p[4], p[6])

    def p_else_if(p):
        "else_stmt : ELSE if_stmt"
        p[0] = p[2]
    
    def p_else(p):
        "else_stmt : ELSE '{' stmt_list '}'"
        p[0] = ElseNode(p[3])

    def p_else_epsilon(p):
        "else_stmt : epsilon"
        p[0] = None
    
    # loop stmt productions
    def p_loop(p):
        "loop_stmt : LOOP loop_init ',' loop_condition ',' loop_set '{' stmt_list '}'"
        p[0] = LoopNode(p[2], p[4], p[6], p[8])

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
        "power : naming"
        p[0] = p[1]
    
    def p_naming_index(p):
        "naming : naming '[' disjunction ']'"
        p[0] = IndexNode(p[1], p[3])

    def p_naming_accessing(p):
        "naming : accessing"
        p[0] = VariableNode(p[1])
    
    def p_naming_keys(p):
        "naming : KEYS '(' naming ')'"
        p[0] = KeysNode(p[3])

    def p_naming_func(p):
        "naming : ID '(' arg_list ')'"
        p[0] = FunctionCallNode(p[1], p[3])
    
    def p_naming_atom(p):
        "naming : atom"
        p[0] = p[1]
    
    def p_atom_number(p):
        "atom : NUMBER"
        p[0] = ValueNode(parse_number(p[1]))
    
    def p_atom_string(p):
        "atom : STRING"
        p[0] = ValueNode(p[1][1:-1])
    
    def p_atom_false(p):
        "atom : bool"
        p[0] = ValueNode(p[1] == 'true')
    
    def p_atom_group(p):
        "atom : '(' expr ')'"
        p[0] = p[2]
    
    def p_atom_list(p):
        "atom : '[' arg_list ']'"
        p[0] = ListNode(p[2])
    
    def p_atom_dict(p):
        "atom : '{' keyarg_list '}'"
        p[0] = DictNode(p[2])
    
    def p_accessing(p):
        "accessing : word"
        p[0] = [p[1]]
    
    def p_accessing_dot(p):
        "accessing : word '.' accessing"
        p[0] = [p[1], *p[3]]
    
    def p_word(p):
        '''word : ID
                | ORGANISM
                | SIMULATION
                | WORLD'''
        p[0] = p[1]
    
    def p_bool(p):
        '''bool : TRUE
                | FALSE'''
        p[0] = p[1]
    
    def p_arg_list(p):
        "arg_list : disjunction"
        p[0] = [p[1]]
    
    def p_arg_list_comma(p):
        "arg_list : disjunction ',' arg_list"
        p[0] = [p[1], *p[3]]
    
    def p_arg_list_epsilon(p):
        "arg_list : epsilon"
        p[0] = []
    
    def p_keyarg_list(p):
        "keyarg_list : keyarg"
        p[0] = [p[1]]
    
    def p_keyarg_list_comma(p):
        "keyarg_list : keyarg ',' keyarg_list"
        p[0] = [p[1], *p[3]]
    
    def p_keyarg_list_epsilon(p):
        "keyarg_list : epsilon"
        p[0] = []
    
    def p_keyarg(p):
        "keyarg : disjunction '=' disjunction"
        p[0] = (p[1], p[3])


    # TEST PRODUCTIONS FOR PARSING
    def p_test_world_stmt(p):
        "test_world : world_stmt"
        p[0] = p[1]

    return yacc.yacc(*args, **kwargs)
