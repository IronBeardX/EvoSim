from src.compiler.context import Context
from src.compiler.util import Signal, BREAK, ValueSignal
from src.compiler.error import (
    PARAMS_ERROR, FUNCTION_NOT_FOUND_ERROR, NOT_A_FUNCTION_ERROR,
    VAR_NOT_FOUND_ERROR, PROP_NOT_IN_VAR_ERROR
)
from src.genetics import (
    Smelling, VisionRadial, Move, Eat, Reproduce,
    Attack, Defend, Pick, Swimming, Health, Hunger, Legs,
    Eye, Arms, Horns, Smell, Fins, Nose, Mouth
)


class Node:
    def evaluate(self, context: Context):
        raise NotImplementedError()


class ValueNode(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, context: Context):
        return self.value


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
                v = v[name]
                current_name = f'{current_name}.{name}'
            except:
                raise PROP_NOT_IN_VAR_ERROR(current_name, name)

        return v


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


class ProgramNode(Node):
    def __init__(self, gene_nodes, dna_nodes, world_node, sim_node):
        self.gene_nodes = gene_nodes
        self.dna_nodes = dna_nodes
        self.world_node = world_node
        self.sim_node = sim_node

    def evaluate(self, context: Context):
        # create gene and dna dicts
        context.set_var("gene", {})
        context.set_var("dna", {})
        
        # store genes
        for node in self.gene_nodes:
            node.evaluate(context)

        # store dna chains
        for node in self.dna_nodes:
            node.evaluate(context)

        # handle world & sim nodes

        # lastly: run simulation
        pass


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
            props looks like: {'episodes': number, 'max_rounds': number, 'stop': Node}
        '''
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


class VariableSettingNode(Node):
    def __init__(self, name, node):
        self.name = name
        self.node = node

    def evaluate(self, context: Context):
        value = self.node.evaluate(context)
        context.set_var(self.name, value)


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
