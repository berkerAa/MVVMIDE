import os

class Bridge:
    def __init__(self, package, path, logic, firstScreen, component):
        self.bridgePath =  os.path.join("..", "templates", "Bridge.txt")
        self.template = self.generateTemplates(package, path, logic, firstScreen, component)
    def generateTemplates(self, package, path, logic, firstScreen, component):
        with open(self.bridgePath, 'r') as f:
            template = ''.join(f.readlines())
        return template.format(**{
            "package": package,
            "path": path,
            "screen": firstScreen,
            "logic": logic,
            "component" : component,
            "screenlower": firstScreen.lower()
        })