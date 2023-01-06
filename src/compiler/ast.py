from src.compiler.context import Context


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
        pass

class SimulationNode(Node):
    def __init__(self, props):
        pass

class PhyGeneNode(Node):
    def __init__(self, props):
        pass

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
