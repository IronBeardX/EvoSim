class Context:
    def __init__(self, parent=None):
        self.parent = parent
        self.variables = {}
    
    def search(self, name, recursive):
        if name in self.variables:
            return self
        if recursive and self.parent:
            return self.parent.search(name, recursive)
        return None
    
    def new_child(self):
        return Context(self)
    
    def get_var(self, name, recursive=True):
        context = self.search(name, recursive)
        if context:
            return context.variables[name]
        
        raise Exception(f"context error: variable '{name}' not found")
    
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
