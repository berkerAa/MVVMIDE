import os

class ViewHolder:
    def __init__(self, package, path, logic, screen, recycler, view, app_configuration):
        self.viewholderPath =  os.path.join("..", "templates", "ViewHolder.txt")
        self.template = self.generateTemplates(package, path, logic, screen, recycler, view)
    def generateTemplates(self, package, path, logic, screen, recycler, view):
        with open(self.viewholderPath, 'r') as f:
            template = ''.join(f.readlines())
            return template.format(**{
                "view": view,
                "package": package,
                "path": path,
                "logic": logic,
                "screen": screen,
                "recycler": recycler.lower(),
                "viewlower": view.lower(),
                "screenlower": screen.lower()
            })