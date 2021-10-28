import os

class Recycler:
    def __init__(self, package, path, logic, screen, recycler, views, app_configuration):
        self.recyclerPath =  os.path.join("..", "templates", "Adapter.txt")
        self.viewTypeTemplate = "object {view}Type: {recycler}TypeCase()"
        self.view2layoutTemplate = "\t\t\t is {view}Type -> {view}ViewHolder(LayoutInflater.from(context).inflate(R.layout.item_{recycler}_{logic}_{screen}_{viewlower}, parent, false), listeners[{view}Type]!!)"
        self.importTemplate = "import {package}.src.{path}_logic.{screenlower}.adapter.".format(**{"package": package,"path": path, "screenlower": screen.lower()})
        self.scopeImport = "import {package}.src.{path}_logic.ds.{logic}Scope".format(**{
            "package": package,
            "path": path,
            "logic": logic
        })
        self.moduleImportTemplate = "import {package}.src.{path}_logic.{screenlower}.adapter.".format(**{
            "package": package,
            "path": path,
            "screenlower": screen.lower(),
            "logic": logic
        })
        self.moduleProvideTemplate = "\t\t@Provides @{}Scope\n\t\tfun ".format(logic) + "{recyclerlower}AdapterProvider(): {recycler}Adapter = {recycler}Adapter(arrayListOf())"
        self.layoutPath = os.path.join("D:", "AutonomTest", "app","src",  "main", "res", "layout")
        self.viewPath = os.path.join(app_configuration["path"], "src", "{}_logic".format(path), screen.lower(), "{}View.kt".format(screen))
        self.modulePath = os.path.join(app_configuration["path"], "core", "dm","RecyclerModule.kt")
        self.template = self.generateTemplates(package, path, logic, screen, recycler, views)
    def generateTemplates(self, package, path, logic, screen, recycler, views):
        with open(self.recyclerPath, 'r') as f:
            template = ''.join(f.readlines())
            template = template.format(**{
                "package": package,
                "path": path,
                "screen": screen,
                "recycler": recycler["Name"],
                "screenlower": screen.lower()
            })
            template = template.split('\n')
    
        for view in views:
            typeIndex = template.index("//@EndViewHolderTypes")
            template.insert(typeIndex-1, self.viewTypeTemplate.format(**{
                "view": view,
                "recycler": recycler["Name"]
            }))
            type2layoutIndex = template.index("\t//@EndViewCreator")
            template.insert(type2layoutIndex-1, self.view2layoutTemplate.format(**{
                "view": view,
                "viewlower": view.lower(),
                "recycler": recycler["Name"].lower(),
                "logic": logic.lower(),
                "screen": screen.lower()
            }))
            open(os.path.join(self.layoutPath, "item_{recycler}_{logic}_{screen}_{viewlower}.xml".format(**{
                "viewlower": view.lower(),
                "recycler": recycler["Name"].lower(),
                "logic": logic.lower(),
                "screen": screen.lower()
            })), "w").close()
        return '\n'.join(template)
    def updateView(self, recycler):
        with open(self.viewPath, "r") as f:
            viewFile = "".join(f.readlines())
            viewFile = viewFile.split("\n")
        with open(self.viewPath, "w+") as f:
            InjectionIndex = viewFile.index("//@EndDependencyInjection")
            ImportIndex = viewFile.index("//@EndImportLibraries")
            InjectionTemplate = "val {recyclerlower}Adapter: {recycler}Adapter".format(**{
                "recycler": recycler,
                "recyclerlower": recycler.lower()
            })
            if "@Inject" in viewFile[InjectionIndex-2]:
                viewFile.insert(InjectionIndex-1, InjectionTemplate)
                viewFile.insert(ImportIndex-1, self.importTemplate + "{}Adapter".format(recycler))
            else:
                viewFile[InjectionIndex-2] = viewFile[InjectionIndex-2] + ','
                viewFile.insert(InjectionIndex-1, InjectionTemplate)
                viewFile.insert(ImportIndex-1, self.importTemplate + "{}Adapter".format(recycler))
            f.write('\n'.join(viewFile))
        with open(self.modulePath, "r") as f:
            providerFile = "".join(f.readlines())
            providerFile = providerFile.split('\n')
        with open(self.modulePath, "w+") as f:
            moduleIndex = providerFile.index("//@EndImportLibraries")
            providerIndex = providerFile.index("//@EndAdapterProvider")
            providerFile.insert(providerIndex-1, self.moduleProvideTemplate.format(**{"recycler": recycler, "recyclerlower": recycler.lower()}))
            if self.scopeImport not in providerFile:
                providerFile.insert(moduleIndex-1, self.scopeImport)
                moduleIndex = providerFile.index("//@EndImportLibraries")
            providerFile.insert(moduleIndex-1, self.moduleImportTemplate + "{}Adapter".format(recycler))
            f.write('\n'.join(providerFile))