from src.compiler.context import Context


class Node:
    def evaluate(self, context: Context):
        raise NotImplementedError()

class ValueNode(Node):
    def __init__(self, value):
        self.value = value
    
    def evaluate(self, context: Context):
        return self.value

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
