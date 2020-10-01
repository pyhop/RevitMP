"""Reloads user selected CAD and Revit links
"""
__title__ = 'Reload Multiple\n Links'
__author__= 'marentette'

from Autodesk.Revit.DB import FilteredElementCollector,RevitLinkInstance,ImportInstance
from june import revit_transaction  
from pyrevit import forms

doc = __revit__.ActiveUIDocument.Document

def reload_Revit(revit_links):
    """Reload Revit Link"""
    name = [] 
    for link in revit_links:
    	linkType  = doc.GetElement(link.GetTypeId());
    	filepath = linkType.GetExternalFileReference().GetAbsolutePath();
    	try:
    		linkType.LoadFrom(filepath,None);
    		name.append(link.Name.split(" : ")[0]+" ");
    	except:
    		name.append(link.Name.split(" : ")[0]+" ")
    		pass
    return name 

@revit_transaction('Reload Links') 
def reload_CAD(CAD_Links): 
    """Reload CAD links"""
    name =  []
    for i in CAD_Links:
    	if i.IsLinked:
            try:
        		CADLink = doc.GetElement(i.GetTypeId())
        		CADLink.Reload()
        		name.append(i.Category.Name)
            except:
                pass     
    return name

"""Collect Links"""
linkInstances = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()
ALLCADTypesInDocument = FilteredElementCollector(doc).OfClass(ImportInstance).ToElements()

"""Format For Dictionaries"""
revit_name = [i.Name.split(" : ")[0]+" " for i in linkInstances]
CAD_name = [i.Category.Name for i in ALLCADTypesInDocument]
link_Revit = [i for i in linkInstances] 
link_CAD = [i for i in ALLCADTypesInDocument]  

"""Create Dictionaries"""
Revit_dict = dict(zip(revit_name,link_Revit))
CAD_dict = dict(zip(CAD_name,link_CAD))

"""User Input Window"""
ops = revit_name + CAD_name 
User_Options = forms.SelectFromList.show(ops,
                                    title='Select Links to be Reloaded', 
                                    multiselect=True,
                                    button_name = 'Reload Links') 

"""Get users Options"""                                  
CAD_links_Reload = [CAD_dict[k] for k in User_Options if k in CAD_dict]
Revit_links_Reload = [Revit_dict[k] for k in User_Options if k in Revit_dict]

"""Reload"""
Revit = reload_Revit(Revit_links_Reload) 
CAD = reload_CAD(CAD_links_Reload) 
reloaded = Revit + CAD
"""Result Window"""
forms.alert(str(reloaded).replace('[','').replace(']',''), 'Reloaded the Following Links')
