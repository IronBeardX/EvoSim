from pydoc import classname
from src.compiler.context import Context
from src.compiler.util import Signal, BREAK, ValueSignal
from src.evo_sim import EvoSim
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
    def __init__(self, name):
        self.name = name

    def evaluate(self, context: Context):
        return context.get_var(self.name)


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
        # TODO: Make validations on the entries
        self.world_props = props

    def evaluate(self, context: Context):
        return self.world_props


class SimulationNode(Node):
    def __init__(self, props):
        DELETE_THIS_VAR = '''
            props looks like: {'episodes': number, 'max_rounds': number, 'stop': Node}
        '''
        # TODO Check values
        # raise Exception("TODO: Implement Exceptions")
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

        if not props_names.issubset(props):
            # TODO: throw Except
            pass
        
        value = props['value'][0]
        value_extras = props['value'][1]
        mutation = props['mutation']

        self.TYPES['name'](
            mutation_chance = mutation['chance'], 
            min_val = value_extras['min'],
            max_val = value_extras['max'],
            mutation_step = mutation['step'],
            value = value
            )
        
        #TODO: finish this
        

    def evaluate(self, context: Context):
        return super().evaluate(context)


class PerceptionGeneNode(Node):
    TYPES = {
        'smelling': Smelling,
        'vision': VisionRadial
    }

    def __init__(self, classname):
        self.classname = classname

    def evaluate(self, context: Context):
        return super().evaluate(context)


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

    def __init__(self, classname):
        self.classname = classname

    def evaluate(self, context: Context):
        return super().evaluate(context)


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
            raise Exception()

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

        raise Exception()


class ReturnNode(Node):
    def __init__(self, node):
        self.node = node

    def evaluate(self, context: Context):
        value = self.node and self.node.evaluate(context)
        raise ValueSignal(value)
