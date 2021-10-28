import os
import pandas as pd

class Repository:
    def __init__(self,package, path, logic, screens, app_configuration):
        self.app_configuration = app_configuration
        self.repositoryPath = os.path.join("..", "templates", "Repository.txt")
        self.importModel = """import {package}.src.{path}_logic.model.{screen}Model"""
        self.apiTemplate = """\t@Headers("Content-Type:application/json")\n\t@POST("/{backendregister}")\n\tfun {screenlower}(@Body {screenlower}Model: {screen}Model): Observable<BaseResponse>"""
        self.modelTemplateSerialize = """\t@SerializedName("{backendserialize}") val {backendserialize}: {type} //{descriptions}"""
        self.caseTemplate = """data class {case}(var data: Any?): {screen}Status()"""
        

        self.template = self.generateTemplates(package, path.lower(), logic, screens)
    def generateTemplates(self, package, path, logic, screens):
        with open(self.repositoryPath, 'r') as f:
            template = ''.join(f.readlines())
        template =  template.format(**{
            "package": package,
            "path": path,
            "logic": logic,
        })
        template = template.split('\n')
        for screen in screens:
            screen = screen["Name"]
            Models = pd.read_excel(os.path.join("..", "models", "{}Models.xlsx".format(logic)), screen)
            #Models["Description"] = Models["Description"].apply(lambda x: "//" + x)
            Status = pd.read_excel(os.path.join("..", "status", "{}Status.xlsx".format(logic)), screen)
            Status['Mobile Description'] = Status['Mobile Description'].apply(lambda x: screen + x.replace(' ', ''))
            modelFile = os.path.join(self.app_configuration["path"],"src", path + "_logic", "model", "{}Model.kt".format(screen))
            webApiFile = os.path.join(self.app_configuration["path"], "app_modules", "web_api", "WebApi.kt")
            with open(os.path.join("..", "templates", "Model.txt"), 'r') as f:
                modelTemplate = ''.join(f.readlines())
                modelTemplate = modelTemplate.format(**{
                    "package": package,
                    "path": path, 
                    "logic": logic,
                    "screen": screen
                })
            modelTemplate = modelTemplate.split("\n")
            index = modelTemplate.index("//@EndDataClassDecleration")
            SeriliazeTemplate = []
            for count, variable in enumerate(Models.iloc()):
                if variable["Backend"] != "expose":
                    SeriliazeTemplate.append(self.modelTemplateSerialize.format(**{
                        "backendserialize": variable["Name"], 
                        "type": variable["Type"] + ', '  if (count != Models.shape[0] -1 )  else variable["Type"],
                        "descriptions":variable["Description"]
                    }))
            modelTemplate.insert(index -1, ('\n'.join(SeriliazeTemplate)))
            for status in Status.iloc():
                index = modelTemplate.index("//@EndStatusCheckDecleration")
                modelTemplate.insert(index -1, self.caseTemplate.format(**{
                        "case": status["Mobile Description"], 
                        "screen": screen
                    }))
            index = modelTemplate.index("//@EndStatusCheckDecleration")
            modelTemplate.insert(index -1, self.caseTemplate.format(**{
                        "case": screen + "ObservableErrorStatus", 
                        "screen": screen
                    }))

            with open(modelFile, 'w') as f:
                f.write('\n'.join(modelTemplate))
            with open(webApiFile, 'r') as f:
                temp = ''.join(f.readlines())
                temp = temp.split('\n')
            with open(webApiFile, 'w+') as f:
                    tempIdx = temp.index("//@EndNetworkRegisterEnds")
                    apiTemplate = self.apiTemplate.format(**{
                        "backendregister": Models["Backend"][0],
                        "screenlower": screen.lower(),
                        "screen": screen
                    })
                    importTemplate = self.importModel.format(**{
                            "package": package, 
                            "path": path,
                            "screen": screen
                        })
                    if not (importTemplate in temp):
                        temp.insert(tempIdx-1, apiTemplate)
                        importIdx = temp.index("//@EndImportLibraries")
                        temp.insert(importIdx-1, importTemplate)
                    f.write('\n'.join(temp))
            templateIdx = template.index("\t//@EndRepositoryConnections")
            with open("..\\templates\\RepositoryConnection.txt", 'r') as f:
                connectionTemplate = ''.join(f.readlines())
                template.insert(templateIdx -1, connectionTemplate.format(**{
                    "screen": screen,
                    "screenlower": screen.lower()
                }))
        return '\n'.join(template)
            
            

            

        