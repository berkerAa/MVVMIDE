import os

class Provider:
    def __init__(self, package, path, logic):
        self.providerPath =  os.path.join("..", "templates", "Provider.txt")
        self.template = self.generateTemplates(package, path, logic)
    def generateTemplates(self, package, path, logic):
        with open(self.providerPath, 'r') as f:
            template = ''.join(f.readlines())
        return template.format(**{
            "package": package,
            "path": path,
            "logic": logic,
        })