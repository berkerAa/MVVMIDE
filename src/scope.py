import os

class Scope:
    def __init__(self, logic, package, path):
        self.scopePath = os.path.join("..", "templates", "Scope.txt")
        self.template = self.generateScope(logic, package, path)
    def generateScope(self, logic, package, path):
        with open(self.scopePath, 'r') as f:
            template = ''.join(f.readlines())
        return template.format(**{
            "path": path,
            "package": package,
            "logic": logic
        })