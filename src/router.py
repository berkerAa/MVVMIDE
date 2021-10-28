import os
class Router:
    def __init__(self, package, path, logic, firstScreen, screens, app_configuration):
        self.bridgePath =  os.path.join("..", "templates", "Router.txt")
        self.routerPath = os.path.join(app_configuration["path"],"core", "dm", "RouterModule.kt")
        self.screenNavigationTemplate = "data class {screen}(val {screenUpper}: Class<{screen}Presenter> = {screen}Presenter::class.java): {logic}NavigationStatus()"
        self.screenNavigationCaseTemplate = "\t\tis {screen} -> onFragmentChange(activity, containerViewId, navigationStatus.{screenUpper})"
        self.screenImportsTemplate = "import {package}.src.{path}_logic.{screenlower}.{screen}Presenter"
        self.routerProviderTemplate = "\t@Binds @{logic}Scope\n\tabstract fun provide{logic}Router({path}Provider: {logic}Router): Router<{logic}NavigationStatus>\n"
        self.routerImportTemplate = "import {package}.src.{path}_logic.*"
        self.scopeImport = "import {package}.src.{path}_logic.ds.{logic}Scope"
        self.template = self.generateTemplates(package, path, logic, firstScreen, screens)
    def generateTemplates(self, package, path, logic, firstScreen, screens):
        with open(self.bridgePath, 'r') as f:
            template = ''.join(f.readlines())
        generatedFormat = template.format(**{
            "package": package,
            "path": path,
            "screen": firstScreen,
            "logic": logic
        })
        
        generatedFormat = generatedFormat.split('\n')
        navigationHolderIndex = generatedFormat.index("@{}Scope".format(logic))
        caseHolderIndex = generatedFormat.index("\t//@EndNavigationCaseCheck")
        importHolderIndex = generatedFormat.index("//@EndLibraryImport")
        for screen in screens:
            screen = screen["Name"]
            importGenerated = self.screenImportsTemplate.format(**{
                "path": path,
                "screen": screen,
                "screenlower": screen.lower(),
                "package": package
            })
            generatedFormat.insert(importHolderIndex-1, importGenerated)
            importHolderIndex+=1
            caseHolderIndex +=1
            navigationHolderIndex +=1

            screenGenerated = self.screenNavigationTemplate.format(**{
                "logic": logic,
                "screen": screen,
                "screenUpper": screen.upper()
            })
            generatedFormat.insert(navigationHolderIndex-1, screenGenerated)
            navigationHolderIndex +=1
            caseHolderIndex +=1
            caseGenerated = self.screenNavigationCaseTemplate.format(**{
                "screen": screen,
                "screenUpper": screen.upper()
            })
            generatedFormat.insert(caseHolderIndex, caseGenerated)
            caseHolderIndex+=1
        with open(self.routerPath, 'r') as f:
            routerFile = ''.join(f.readlines())
            routerFile = routerFile.split('\n')
        with open(self.routerPath, 'w+') as f:
            importIndex = routerFile.index("//@EndImportLibraries")
            binderIndex = routerFile.index("//@EndRouterBinder")
            importFormatted = self.routerImportTemplate.format(**{
                "package": package,
                "path": path
            })
            if importFormatted not in routerFile:
                routerFile.insert(importIndex-1, importFormatted)
                importIndex = routerFile.index("//@EndImportLibraries")
                routerFile.insert(importIndex-1, self.scopeImport.format(**{
                    "package": package,
                    "path": path,
                    "logic": logic
                }))
                binderIndex = routerFile.index("//@EndRouterBinder")
                routerFile.insert(binderIndex-1,self.routerProviderTemplate.format(**{
                    "logic": logic,
                    "path": path
                }))
            f.write('\n'.join(routerFile))
        return '\n'.join(generatedFormat)


        