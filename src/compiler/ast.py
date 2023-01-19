from src.compiler.context import Context
from src.compiler.util import Signal, BREAK, ValueSignal
from src.evo_entity import *
from src.compiler.error import (
    PARAMS_ERROR, FUNCTION_NOT_FOUND_ERROR, NOT_A_FUNCTION_ERROR,
    VAR_NOT_FOUND_ERROR, PROP_NOT_IN_VAR_ERROR,
    NOT_A_LIST_ERROR, BAD_LIST_INDEXER_ERROR,
    KEY_NOT_IN_DICT_ERROR, NOT_A_DICT_ERROR, BAD_INDEXER_ERROR
)
from src.genetics import (
    Smelling, VisionRadial, Move, Eat, Reproduce,
    Attack, Defend, Pick, Swimming, Health, Hunger, Legs,
    Eye, Arms, Horns, Smell, Fins, Nose, Mouth
)


class Node:
    def evaluate(self, context: Context):
        raise NotImplementedError()


class ProgramNode(Node):
    def __init__(self, gene_nodes, dna_nodes, behavior_nodes, entity_org_nodes, world_node, sim_node):
        self.gene_nodes = gene_nodes
        self.dna_nodes = dna_nodes
        self.behavior_nodes = behavior_nodes
        self.entity_org_nodes = entity_org_nodes
        self.world_node = world_node
        self.sim_node = sim_node

    def evaluate(self, context: Context):
        # create gene, dna and behavior dicts, and entity factory list
        context.set_var("gene", {})
        context.set_var("dna", {})
        context.set_var("behaviors", {})
        context.set_var("ent_facts", [])

        # store genes
        for node in self.gene_nodes:
            node.evaluate(context)

        # store dna chains
        for node in self.dna_nodes:
            node.evaluate(context)
        
        # store behavior classes
        for node in self.behavior_nodes:
            node.evaluate(context)
        
        # store entity factories
        for node in self.entity_org_nodes:
            node.evaluate(context)

        # handle world & sim nodes

        # lastly: run simulation
        pass


class PerceptionGeneNode(Node):
    TYPES = {
        'smelling': Smelling,
        'vision': VisionRadial
    }

    def __init__(self, classname):
        self.gene_instance = self.TYPES[classname]()
        self.classname = classname

    def evaluate(self, context: Context):
        gene_dict = context.get_var('gene')
        gene_dict[self.classname] = self.gene_instance


class ActionGeneNode(Node):
    TYPES = {
        'move': Move,
        'eat': Eat,
        'reproduce': Reproduce,
        'attack': Attack,
        'defend': Defend,
        'pick': Pick,
        'swim': Swimming
    }

    def __init__(self, props):
        DELETE_THIS_VAR = '''
            props looks like: {
                'name': string,
                'cost': number,
                'class': string (for example: 'health' or 'legs')
            }
            }
        '''
        self.name = props['name']
        cost = props['cost']
        gene_class = props['class']
        self.gene_instance = self.TYPES[gene_class](cost)

    def evaluate(self, context: Context):
        gene_dict = context.get_var('gene')
        gene_dict[self.name] = self.gene_instance


class PhyGeneNode(Node):
    TYPES = {
        'health': Health,
        'hunger': Hunger,
        'legs': Legs,
        'eye': Eye,
        'arms': Arms,
        'horns': Horns,
        'smell': Smell,
        'fins': Fins,
        'nose': Nose,
        'mouth': Mouth
    }

    def __init__(self, props):
        DELETE_THIS_VAR = '''
            props looks like: {
                'name': string,
                'value': (number, {'min': number, 'max': number}),
                'mutation': {'step': number, 'chance': number},
                'class': string (for example: 'health' or 'legs')
            }
        '''
        props_names = {'name', 'value', 'mutation', 'class'}

        if props['value'][0] < props['value'][1]['min'] or props['value'][0] > props['value'][1]['max']:
            raise ValueError('Invalid value for gene')
        if props['mutation']['step'] <= 0:
            raise ValueError('Gene step should be grater than 0')
        if props['mutation']['chance'] < 0 or props['mutation']['chance'] > 1:
            raise ValueError('Mutation chance should be between 0 and 1')

        value = props['value'][0]
        value_extras = props['value'][1]
        mutation = props['mutation']
        self.name = props['name']
        self.gene_instance = self.TYPES[props['class']](
            mutation_chance=mutation['chance'],
            mutation_step=mutation['step'],
            value=value,
            min_val=value_extras['min'],
            max_val=value_extras['max']
        )

    def evaluate(self, context: Context):
        gene_dict = context.get_var('gene')
        gene_dict[self.name] = self.gene_instance


class DNAChainNode(Node):
    def __init__(self, name, props):
        DELETE_THIS_VAR = '''
            props looks like: list of dna_element
            
            dna_element looks like:
            {   
                TODO: Remove class from props
                {"type": "gene", "name": string} |
                {"type": "dna", "name": string}
        '''
        self.name = name
        self.props = props

    def evaluate(self, context: Context):
        gene_dict = context.get_var("gene")
        dna_dict = context.get_var("dna")
        new_chain = []
        for dna_element in self.props:
            if dna_element['type'] == 'gene':
                new_chain.append(gene_dict[dna_element['name']])
            elif dna_element['type'] == 'dna':
                new_chain.extend(dna_dict[dna_element['name']])
            else:
                raise ValueError('Invalid dna element')
        dna_dict[self.name] = new_chain


class BehaviorNode(Node):
    def __init__(self, name, func_nodes, decide_node):
        self.name = name
        self.func_nodes = func_nodes
        self.decide_node = decide_node
    
    def evaluate(self, context: Context):
        child_context = context.create_child()
        behavior_dict = context.get_var('behaviors')
        for node in self.func_nodes:
            node.evaluate(child_context)

        class NewBehavior(Behavior):
            def decide_action(self, time = 1):
                return self.decide_node.call(child_context, [self, time])
        
        behavior_dict[self.name] = NewBehavior


class EntityNode(Node):
    def __init__(self, props):
        DELETE_THIS = '''
        'representation':str
        'coexistence':bool
        '''

        #checking if all props are in props
        if not ('representation' in props and 'coexistence' in props):
            raise ValueError('Entity must have representation and coexistence')

        self.factory = lambda: Entity(props['representation'], props['coexistence'])
        

    def evaluate(self, context: Context):
        fac_list = context.get_var('ent_facts')
        fac_list.append(self.factory)


class OrganismNode(Node):
    def __init__(self, props):
        DELETE_THIS = '''
        'representation':str
        'dna':str
        'behavior':str
        '''
        if not('representation' in props or 'dna' in props or 'behavior' in props):
            raise ValueError('Organism must have representation and dna_chain')
        
        self.representation = props['representation']
        self.dna_chain = props['dna']
        self.behavior = props['behavior']


    def evaluate(self, context: Context):
        fac_list = context.get_var('ent_facts')
        dna_chain = context.get_var('dna')[self.dna_chain]
        behavior_class = context.get_var('behaviors')[self.behavior]
        representation = self.representation

        #create a new class that inherits from Organism and the behavior class
        class NewOrganism(Organism, behavior_class):
            def __init__(self):
                super().__init__(dna_chain, representation)
            
        fac_list.append(lambda: NewOrganism())


class WorldNode(Node):
    def __init__(self, props):
        DELETE_THIS_VAR = '''
            props looks like: {'size': Tuple, 'terrain': List}

            'size' is (True, {'width': -1, 'height': -1}) if infinite
            else is (False, {'width': number, 'height': number})

            'terrain' is a list of Tuple (string, boolean, list)
            the string is the name of the terrain
            the boolean represents if it's default or not
            the list of numbers are the positions (empty if terrain is default)
        '''

        #TODO: averiguar q pasa y arreglar
        #Traceback (most recent call last):
        #    File "/home/yeyon/Uni/EvoSim/compiler_play.py", line 17, in <module>
        #      expr = parser.parse(text, lexer=lexer)
        #             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        #    File "/home/yeyon/Uni/EvoSim/src/compiler/ply/yacc.py", line 409, in parse
        #      p.callable(pslice)
        #    File "/home/yeyon/Uni/EvoSim/src/compiler/parser.py", line 194, in p_world
        #      p[0] = WorldNode({**p[3], **p[4]})
        #             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
        #    File "/home/yeyon/Uni/EvoSim/src/compiler/ast.py", line 270, in __init__
        #      raise PARAMS_ERROR('World', 'size', 'width or height')
        #src.compiler.error.EvoSimFunctionError: function 'World' expects size parameters and received width or height arguments when called

        # Checking if all properties are in the dictionary:
        if not 'size' in props or not 'terrain' in props:
            raise PARAMS_ERROR('world', 'size or terrain')
        
        if not isinstance(props['size'][0], bool):
            raise PARAMS_ERROR('world', 'finite must be a boolean')

        if not 'width' in props['size'] or not 'height' in props['size']:
            raise PARAMS_ERROR('World', 'size', 'width or height')

        if not (isinstance(props['size'][1]['width'], int) and isinstance(props['size'][1]['height'], int)):
            raise ValueError('World size must be integers')

        if props['size'][1]['width'] <= 0 or props['size'][1]['height'] <= 0:
            raise ValueError('Invalid size for world')

        self.world_props = props

    def evaluate(self, context: Context):
        return self.world_props


class SimulationNode(Node):
    def __init__(self, props):
        DELETE_THIS_VAR = '''
            props looks like: {'episodes': number, 'max_rounds': number, 'stop': FunctionNode, 'actions_time': number, 'available_commands': dict{string, callable}}
        '''

        #en 'stop' hay un FunctionNode q recibe a la propia simulacion, so:
        #TODO: hacer cambios pertinentes

        if not isinstance(props['episodes'], int):
            raise ValueError('Number of episodes must be an integer')
        if not isinstance(props['max_rounds'], int):
            raise ValueError('The number of rounds must be an integer')
        if props['episodes'] <= 0:
            raise ValueError('Invalid number of episodes')
        if props['max_rounds'] <= 0:
            raise ValueError('Invalid number of rounds')

        self.evo_props = props

    def evaluate(self, context: Context):
        return self.evo_props


class FunctionNode(Node):
    def __init__(self, name, params, body_nodes):
        self.name = name
        self.params = params
        self.body = body_nodes

    def evaluate(self, context: Context):
        context.set_var(self.name, self)

    def call(self, context: Context, args):
        # create child context because function
        # represents a new block
        child_context = context.new_child()

        if len(self.params) != len(args):
            raise PARAMS_ERROR(self.name, len(self.params), len(args))

        # set param values NOT RECURSIVELY
        for param, arg in zip(self.params, args):
            child_context.set_var(param, arg, recursive=False)

        # catch ValueSignal in case the function
        # returns a value
        try:
            for node in self.body:
                node.evaluate(child_context)
        except ValueSignal as s:
            return s.value


class FunctionCallNode(Node):
    def __init__(self, name, arg_nodes):
        self.name = name
        self.args = arg_nodes

    def evaluate(self, context: Context):
        # search context where 'name' func was declared
        func_context = context.search(self.name)

        # check if it exists and is an actual func
        if func_context:
            f = func_context.get_var(self.name)
            if isinstance(f, FunctionNode):
                args = [arg.evaluate(context) for arg in self.args]
                return f.call(func_context, args)

            raise NOT_A_FUNCTION_ERROR(self.name)

        raise FUNCTION_NOT_FOUND_ERROR(self.name)


class ReturnNode(Node):
    def __init__(self, node):
        self.node = node

    def evaluate(self, context: Context):
        value = self.node and self.node.evaluate(context)
        raise ValueSignal(value)


class IfNode(Node):
    def __init__(self, condition_node, body_nodes, else_node):
        self.condition = condition_node
        self.body = body_nodes
        self.else_node = else_node

    def evaluate(self, context: Context):
        child_context = context.new_child()

        if (self.condition.evaluate(child_context)):
            for node in self.body:
                node.evaluate(child_context)
        elif self.else_node:
            self.else_node.evaluate(context)


class ElseNode(Node):
    def __init__(self, body_nodes):
        self.body = body_nodes or []

    def evaluate(self, context: Context):
        child_context = context.new_child()

        for node in self.body:
            node.evaluate(child_context)


class LoopNode(Node):
    def __init__(self, init_node, condition_node, final_node, body_nodes):
        self.init = init_node
        self.condition = condition_node or ValueNode(True)
        self.final = final_node
        self.body = body_nodes or []

    def evaluate(self, context: Context):
        child_context = context.new_child()

        if self.init:
            self.init.evaluate(child_context)

        while self.condition.evaluate(child_context):
            try:
                for node in self.body:
                    node.evaluate(child_context)
            # catches a CONTINUE or BREAK signal
            # from any level of child scope
            except Signal as s:
                if s == BREAK:
                    break

            if self.final:
                self.final.evaluate(child_context)


class BreakNode(Node):
    def evaluate(self, context: Context):
        raise BREAK


class ContinueNode(Node):
    def evaluate(self, context: Context):
        raise Signal()


class VariableNode(Node):
    def __init__(self, names):
        name, *rest = names
        self.name = name
        self.rest = rest

    def evaluate(self, context: Context):
        v = context.get_var(self.name)
        if v is None:
            raise VAR_NOT_FOUND_ERROR(self.name)

        current_name = self.name
        for name in self.rest:
            try:
                v = getattr(v, name)
                current_name = f'{current_name}.{name}'
            except:
                raise PROP_NOT_IN_VAR_ERROR(current_name, name)

        return v

class VariableSettingNode(Node):
    def __init__(self, names, node):
        name, *rest = names
        self.name = name
        self.rest = rest
        self.node = node

    def evaluate(self, context: Context):
        value = self.node.evaluate(context)

        if len(self.rest) == 0:
            context.set_var(self.name, value)
        else:
            *middle, last = self.rest
            names = [self.name, *middle]

            vnode = VariableNode(names)
            v = vnode.evaluate(context)

            try:
                setattr(v, last, value)
            except:
                raise PROP_NOT_IN_VAR_ERROR('.'.join(names), last)


class ListNode(Node):
    def __init__(self, element_nodes):
        self.elements = element_nodes
    
    def evaluate(self, context: Context):
        return [element.evaluate(context) for element in self.elements]


class ListAccessNode(Node):
    def __init__(self, listlike_node, index_node, set_node=None):
        self.list_node = listlike_node
        self.index_node = index_node
        self.set_node = set_node
    
    def evaluate(self, context: Context):
        l = self.list_node.evaluate(context)
        if not isinstance(l, (list, str)):
            raise NOT_A_LIST_ERROR()
        
        i = self.index_node.evaluate(context)
        try:
            i = int(i)
        except ValueError:
            raise BAD_LIST_INDEXER_ERROR(i)
        
        if self.set_node:
            l[i % len(l)] = self.set_node.evaluate(context)
        else:
            return l[i % len(l)]


class DictNode(Node):
    def __init__(self, keyarg_nodes):
        self.pairs = keyarg_nodes
    
    def evaluate(self, context: Context):
        d = {}
        for p in self.pairs:
            k, v = p
            key = k.evaluate(context)
            try:
                d[key] = v.evaluate(context)
            except TypeError:
                raise BAD_INDEXER_ERROR(key)
        
        return d


class DictAccessNode(Node):
    def __init__(self, dictlike_node, index_node, set_node=None):
        self.dict_node = dictlike_node
        self.index_node = index_node
        self.set_node = set_node
    
    def evaluate(self, context: Context):
        d = self.dict_node.evaluate(context)
        if not isinstance(d, dict):
            raise NOT_A_DICT_ERROR()
        
        i = self.index_node.evaluate(context)

        if self.set_node:
            try:
                d[i] = self.set_node.evaluate(context)
            except TypeError:
                raise BAD_INDEXER_ERROR(i)
        else:
            try:
                return d[i]
            except KeyError:
                raise KEY_NOT_IN_DICT_ERROR(i)


class UnaryOpNode(Node):
    def __init__(self, node, apply):
        self.node = node
        self.apply = apply

    def evaluate(self, context):
        value = self.node.evaluate(context)
        return self.apply(value)


class BinaryOpNode(Node):
    def __init__(self, leftnode, rightnode, apply):
        self.leftnode = leftnode
        self.rightnode = rightnode
        self.apply = apply

    def evaluate(self, context):
        left = self.leftnode.evaluate(context)
        right = self.rightnode.evaluate(context)
        return self.apply(left, right)


class ValueNode(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, context: Context):
        return self.value
