import os


class Component:
    def __init__(self, package, path, logic, modules):
        self.componentPath =  os.path.join("..", "templates", "Component.txt")
        self.importTemplate = "import {package}.core.dm.{module}Module"
        self.template = self.generateTemplates(package, path, logic, modules)
    def generateTemplates(self, package, path, logic, modules):
        with open(self.componentPath, 'r') as f:
            template = ''.join(f.readlines())
        template =  template.format(**{
            "package": package,
            "path": path,
            "modules": ', '.join([item + "Module::class" for item in modules]),
            "logic": logic
        })
        template = template.split('\n')
        for module in modules:
            idx = template.index("//@EndLibraryImport")
            generatedImport = self.importTemplate.format(**{
                "package": package,
                "module": module
            })
            template.insert(idx-1, generatedImport)
        return '\n'.join(template)



