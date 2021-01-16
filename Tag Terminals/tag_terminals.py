"""This script tags any selected elements or groups and tags
all the air terminals
"""
__title__ = 'Tag\nTerminals'
__author__= 'marentette'

from Autodesk.Revit.DB import \
FilteredElementCollector,BuiltInCategory,\
Reference,TagOrientation

from Autodesk.Revit.DB.IndependentTag import Create

from june import revit_transaction

uidoc = __revit__.ActiveUIDocument 
doc = uidoc.Document

def exit_(reason): 
    """Exit Function"""
    import sys
    from pyrevit import forms
    forms.alert(reason)
    return sys.exit() 

def selected_terminals():
    """Grab User Selections and Exit if No Air Terminals were Selected"""
    selected_elements = uidoc.Selection.GetElementIds()    
    if len(selected_elements) > 0: pass
    else: 
        exit_('No Elements were Selected') 
    air_terminals = [] 
    for e in selected_elements: 
        el = doc.GetElement(e)
        if el.ToString() == 'Autodesk.Revit.DB.Group': #Check if user selected a group 
            group_members = el.GetMemberIds()
            for g in group_members:
                element = doc.GetElement(g)
                if element.Category.Name== 'Air Terminals':
                    air_terminals.append(element) 
        elif el.Category.Name == 'Air Terminals':
            air_terminals.append(el)
        else: pass 
    return air_terminals if air_terminals else exit_('No Air Terminals were Selected')

@revit_transaction('Tag Terminals')
def tag_terminals(air_terminals):
    terminal_tags = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_DuctTerminalTags).WhereElementIsNotElementType().ToElements()
    for a in air_terminals:
        Create(doc,
               terminal_tags[0].GetTypeId(),
               doc.ActiveView.Id,
               Reference(a),
               True,
               TagOrientation.Horizontal,
               a.Location.Point)
                   
if __name__ == '__main__':
    tag_terminals(selected_terminals()) 
