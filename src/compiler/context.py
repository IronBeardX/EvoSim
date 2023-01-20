class Context:
    def __init__(self, parent=None, debug=False):
        self.parent = parent
        self.variables = {}
        
        self.debug = debug
        self.children = []
    
    def search(self, name, recursive=True):
        if name in self.variables:
            return self
        if recursive and self.parent:
            return self.parent.search(name, recursive)
        return None
    
    def new_child(self):
        child_context = Context(self, self.debug)
        if self.debug:
            self.children.append(child_context)
        
        return child_context
    
    def get_var(self, name, recursive=True):
        context = self.search(name, recursive)
        if context:
            return context.variables[name]
    
    def set_var(self, name, value, recursive=True):
        context = self.search(name, recursive)

        # if the variable exists:
        if context:
            # asign the new value to it
            context.variables[name] = value
        # if it doesn't:
        else:
            # create it
            self.variables[name] = value
