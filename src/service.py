import numpy as np
import os, random, json, subprocess
from component import *
from scope import *
from bridge import *
from repository import *
from router import *
from presenter import *
from viewmodel import *
from provider import *
from view import *
from recycler import *
from ViewHolder import *
from pathlib import Path

class Service:
    def __init__(self, description):
        self.packages = {
            "AutonomTest": os.path.join("D:", "AutonomTest", "app","src",  "main") #D:\AutonomTest header
        }
        self.subPaths = {
            "Structure": os.path.join("java", "com", "example", "autonomtest"),
            "Resource": "res"
        }

        self.app_config = {
            "path": "D:" + "\\" + os.path.join( "AutonomTest", "app","src",  "main", "java", "com", "example", "autonomtest")
        }

        self.description = description

        self.FOLDER = lambda folder: Path(folder).mkdir(parents=True, exist_ok=True)
        self.FOLDER(os.path.join(self.app_config["path"],"src", self.description["path"] + "_logic", "model"))

        #Per Logic Code Generation System
        self.getComponent = lambda : Component(self.description["package"], self.description["path"], self.description["logic"], self.description["modules"])
        self.getProvider = lambda : Provider(self.description["package"], self.description["path"], self.description["logic"])
        self.getScope = lambda : Scope(self.description["logic"], self.description["package"], self.description["path"])
        self.getBridge = lambda : Bridge(self.description["package"], self.description["path"], self.description["logic"], self.description["firstScreen"], self.description["logic"].lower())
        self.getRepository = lambda : Repository(self.description["package"], self.description["path"], self.description["logic"],  self.description["screens"], self.app_config)
        self.getRouter = lambda : Router(self.description["package"], self.description["path"], self.description["logic"], self.description["firstScreen"], self.description["screens"], self.app_config)

        #Per Screen Code Generation System
        self.getPresenter = lambda screen: Presenter(self.description["package"], self.description["path"], self.description["logic"], screen)
        self.getView = lambda screen: View(self.description["package"], self.description["path"], self.description["logic"], screen, self.app_config)
        self.getViewModel = lambda screen: ViewModel(self.description["package"], self.description["path"], self.description["logic"], screen)
        
        #Per Screen Per Recycler Generation System
        self.getRecycler = lambda recycler, screen: Recycler(self.description["package"], self.description["path"], self.description["logic"], screen, recycler, recycler["ViewHolder"], self.app_config) 
        self.recyclerLoop = lambda recycler, screen: [{"Name": recyclerItem["Name"], "Template": self.getRecycler(recyclerItem, screen).template, "ViewHolders": recyclerItem["ViewHolder"], "Object": self.getRecycler(recyclerItem, screen)} for recyclerItem in recycler]
        self.getViewHolder = lambda recyclerName, viewHolderName, screenName: ViewHolder(self.description["package"], self.description["path"], self.description["logic"], screenName, recyclerName, viewHolderName, self.app_config)

        self.constructPath = lambda head, end: "{}{}".format(head , end)
        self.buildTemplates = lambda : {
            "Component": self.getComponent().template,
            "Provider": self.getProvider().template,
            "Bridge": self.getBridge().template,
            "Repository": self.getRepository().template,
            "Router": self.getRouter().template,
            "Scope": self.getScope().template,
            "Screens": [
                {"Presenter": self.getPresenter(screen["Name"]).template,
                "View": self.getView(screen["Name"]).template,
                "ViewModel": self.getViewModel(screen["Name"]).template,
                "Name": screen["Name"],
                "Recycler": self.recyclerLoop(screen["Recycler"], screen["Name"]) if "Recycler" in screen.keys() else None}
                for screen in self.description["screens"]
            ]
        }
            
    def buildArchitecture(self):
        templates = self.buildTemplates()

            #Generate Component File
        tmpPath = os.path.join(self.packages["AutonomTest"], self.subPaths["Structure"], "src", "{}_logic".format(self.description["path"]), "di")
        self.FOLDER(tmpPath)
        with open(os.path.join(tmpPath, self.constructPath(self.description["logic"], "Component.kt")), "w") as component:
            component.write(templates["Component"])
            
            #Generate Provider File
        tmpPath = os.path.join(self.packages["AutonomTest"], self.subPaths["Structure"], "src", "{}_logic".format(self.description["path"]), "di")
        self.FOLDER(tmpPath)
        with open(os.path.join(tmpPath, self.constructPath(self.description["logic"], "Provider.kt")), "w") as component:
            component.write(templates["Provider"])
            
        #Generate Scope File
        tmpPath = os.path.join(self.packages["AutonomTest"], self.subPaths["Structure"], "src", "{}_logic".format(self.description["path"]), "ds")
        self.FOLDER(tmpPath)
        with open(os.path.join(tmpPath, self.constructPath(self.description["logic"], "Scope.kt")), "w") as component:
            component.write(templates["Scope"])


            #Generate Bridge File
        tmpPath = os.path.join(self.packages["AutonomTest"], self.subPaths["Structure"], "src", "{}_logic".format(self.description["path"]))
        self.FOLDER(tmpPath)
        with open(os.path.join(tmpPath, self.constructPath(self.description["logic"], "Bridge.kt")), "w") as component:
            component.write(templates["Bridge"])

            #Generate Repository File
        tmpPath = os.path.join(self.packages["AutonomTest"], self.subPaths["Structure"], "src", "{}_logic".format(self.description["path"]))
        self.FOLDER(tmpPath)
        with open(os.path.join(tmpPath, self.constructPath(self.description["logic"], "Repository.kt")), "w") as component:
            component.write(templates["Repository"])

            #Generate Router File
        tmpPath = os.path.join(self.packages["AutonomTest"], self.subPaths["Structure"], "src", "{}_logic".format(self.description["path"]))
        self.FOLDER(tmpPath)
        with open(os.path.join(tmpPath, self.constructPath(self.description["logic"], "Router.kt")), "w") as component:
            component.write(templates["Router"])

        for screen in templates["Screens"]:
            tmpPath = os.path.join(self.packages["AutonomTest"], self.subPaths["Structure"], "src", "{}_logic".format(self.description["path"]), screen["Name"].lower())
            self.FOLDER(tmpPath)
                
            with open(os.path.join(tmpPath, self.constructPath(screen["Name"], "Presenter.kt")), "w") as presenter:
                presenter.write(screen["Presenter"])

            with open(os.path.join(tmpPath, self.constructPath(screen["Name"], "View.kt")), "w") as view:
                view.write(screen["View"])

            with open(os.path.join(tmpPath, self.constructPath(screen["Name"], "ViewModel.kt")), "w") as viewmodel:
                viewmodel.write(screen["ViewModel"])

            with open(os.path.join(self.packages["AutonomTest"], self.subPaths["Resource"],"layout" ,  "activity_{logic}_{screen}_layout.xml".format(**{"logic": self.description["path"], "screen": screen["Name"].lower() })), 'w') as f:
                    f.write('<?xml version="1.0" encoding="utf-8"?>\n<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"\nxmlns:app="http://schemas.android.com/apk/res-auto"\nxmlns:tools="http://schemas.android.com/tools"\nandroid:layout_width="match_parent"\nandroid:layout_height="match_parent"></androidx.constraintlayout.widget.ConstraintLayout>')


            if screen["Recycler"]:
                tmpPath = os.path.join(self.packages["AutonomTest"], self.subPaths["Structure"], "src", "{}_logic".format(self.description["path"]), screen["Name"].lower(), "adapter")
                viewHoldertmpPath = os.path.join(self.packages["AutonomTest"], self.subPaths["Structure"], "src", "{}_logic".format(self.description["path"]), screen["Name"].lower(), "viewholder")
                self.FOLDER(tmpPath)
                self.FOLDER(viewHoldertmpPath)
                for template in screen["Recycler"]:
                    with open(os.path.join(tmpPath, "{}Adapter.kt".format(template["Name"])), "w") as recycler:
                        recycler.write(template["Template"])
                    template["Object"].updateView(template["Name"])
                    for viewHolder in template["ViewHolders"]:
                           viewPath = os.path.join(viewHoldertmpPath, "{}ViewHolder.kt".format(viewHolder))
                           with open(viewPath, "w") as viewHolderFile:
                               viewHolderFile.write(self.getViewHolder(template["Name"], viewHolder, screen["Name"]).template)
            

            

           
if __name__ == "__main__":
    with open("../example.json", "r") as js:
        description = json.load(js)
    for desc in description:
        service = Service(desc)
        service.buildArchitecture()
    