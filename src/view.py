import os

class View:
    def __init__(self, package, path, logic, screen, app_configuration):
        self.viewPath =  os.path.join("..", "templates", "View.txt")
        self.viewBindingPath = os.path.join(app_configuration["path"],"core", "dm", "ViewBindingModule.kt")
        self.bindTemplate = "\t@Binds @{logic}Scope\n \tabstract fun provide{screen}View({screenlower}View: {screen}View): ViewBinding<{screen}Model>"
        self.viewImport = "import {package}.src.{path}_logic.{screenlower}.*"
        self.scopeImport = "import {package}.src.{path}_logic.ds.{logic}Scope"
        self.modelImport = "import {package}.src.{path}_logic.model.*"
        self.template = self.generateTemplates(package, path, logic, screen)
    def generateTemplates(self, package, path, logic, screen):
        with open(self.viewPath, 'r') as f:
            template = ''.join(f.readlines())
        template = template.format(**{
            "package": package,
            "path": path,
            "screen": screen,
            "logic": logic,
            "screenlower": screen.lower()
        })
        with open(self.viewBindingPath, 'r') as f:
            viewBindingFile = ''.join(f.readlines())
            viewBindingFile = viewBindingFile.split("\n")
        with open(self.viewBindingPath, 'w+') as f:
            bindIndex = viewBindingFile.index("//@EndViewBinding")
            bindFormatted = self.bindTemplate.format(**{
                "screen": screen,
                "screenlower": screen.lower(),
                "logic": logic
            })
            if bindFormatted.split('\n')[1] not in viewBindingFile:
                print(bindFormatted)
                print(viewBindingFile)
                viewBindingFile.insert(bindIndex-1, bindFormatted)

            scopeFormatted = self.scopeImport.format(**{
                "package": package,
                "path": path, 
                "logic": logic
            })
            if scopeFormatted not in viewBindingFile:
                importIndex = viewBindingFile.index("//@EndImportLibraries")
                viewBindingFile.insert(importIndex-1, scopeFormatted)
            
            modelFormatted = self.modelImport.format(**{
                "package": package,
                "path": path            
                })
            if modelFormatted not in viewBindingFile:
                importIndex = viewBindingFile.index("//@EndImportLibraries")
                viewBindingFile.insert(importIndex-1, modelFormatted)


            viewFormatted = self.viewImport.format(**{
                "package": package,
                "screenlower": screen.lower(),
                "path": path
            })
            if viewFormatted not in viewBindingFile:
                importIndex = viewBindingFile.index("//@EndImportLibraries")
                viewBindingFile.insert(importIndex-1, viewFormatted)


            f.write('\n'.join(viewBindingFile))
        return template