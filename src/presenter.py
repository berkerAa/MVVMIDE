import os
import pandas as pd
class Presenter:
    def __init__(self, package, path, logic, screen):
        self.presenterPath =  os.path.join("..", "templates", "Presenter.txt")
        self.statusCheckTemplate = "\t\t\tis {status} -> {{}}{description}"
        self.layout = "activity_{logic}_{screen}_layout".format(**{"logic": logic.lower(), "screen": screen.lower() })
        self.template = self.generateTemplates(package, path, logic, screen)
    def generateTemplates(self, package, path, logic, screen):
        with open(self.presenterPath, 'r') as f:
            template = ''.join(f.readlines())
        template = template.format(**{
            "package": package,
            "path": path,
            "screen": screen,
            "logic": logic,
            "layout_name" : self.layout,
            "screenlower": screen.lower()
        })
        template = template.split('\n')
        Status = pd.read_excel(os.path.join("..", "status", "{}Status.xlsx".format(logic)), screen)
        Status['Mobile Description'] = Status['Mobile Description'].apply(lambda x: screen + x.replace(' ', ''))
        
        for status in Status.iloc():
            templateIdx = template.index("\t\t//@EndStatusCheck")
            template.insert(templateIdx-1, self.statusCheckTemplate.format(**{
                "status": status["Mobile Description"],
                "description": "//Perform action on " + status["Detailed Description"]
            }))
        return '\n'.join(template)


