import os
import pandas as pd
class ViewModel:
    def __init__(self, package, path, logic, screen):
        self.viewmodelPath =  os.path.join("..", "templates", "ViewModel.txt")
        self.statusMapTemplate = "\t\t\t  {statusCode} -> {status}(status.data)" 
        self.template = self.generateTemplates(package, path, logic, screen)
        

    def generateTemplates(self, package, path, logic, screen):
        with open(self.viewmodelPath, 'r') as f:
            template = ''.join(f.readlines())
        template =  template.format(**{
            "package": package,
            "path": path,
            "screen": screen,
            "logic": logic,
            "screenlower": screen.lower()
        })
        template = template.split('\n')
        Status = pd.read_excel(os.path.join("..", "status", "{}Status.xlsx".format(logic)), screen)
        Status['Mobile Description'] = Status['Mobile Description'].apply(lambda x: screen + x.replace(' ', ''))
        templateIdx = template.index("\t//@StartRepositoryConnection")
        with open("..\\templates\\ViewModelRepositoryConnection.txt", 'r') as f:
            statusMapper = ''.join(f.readlines())
            statusMapper = statusMapper.format(**{
                "screen": screen,
                "screenlower": screen.lower(),
                "path": path
            })
            statusMapper = statusMapper.split('\n')
            for count, status in enumerate(Status.iloc()):
                statusMapperIdx = statusMapper.index("\t\t//@EndStatusMapping")
                statusMapper.insert(statusMapperIdx-1, self.statusMapTemplate.format(**{
                    "statusCode": status["Status Code"],
                    "status": status["Mobile Description"]
                }))
            statusMapperIdx = statusMapper.index("\t\t//@EndStatusMapping")
            statusMapper.insert(statusMapperIdx-1, "\t\t\t  else -> {}ObservableErrorStatus(status.data)".format(screen))
            template.insert(templateIdx-1, '\n'.join(statusMapper))
        return '\n'.join(template)
