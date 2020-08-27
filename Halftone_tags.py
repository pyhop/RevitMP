"""Halftone Tags
Halftone tags referencing exsiting phased elements

"""
__title__ = 'Halftone\nTags' 
__author__= 'marentette'

import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

from june import revit_transaction 
#Active document 
doc = __revit__.ActiveUIDocument.Document

#Result Window
def window(numberoftags):
    dialog = TaskDialog("Header")
    dialog.MainInstruction = "Results"
    dialog.MainContent = "{0} tags were switched to {1}".format(numberoftags,'halftone')
    dialog.CommonButtons = TaskDialogCommonButtons.Close;
    return dialog.Show()

#Halftone function 
@revit_transaction('Halftone Existing Tags')
def halftone(tags): 
    graphic_halftone = OverrideGraphicSettings().SetHalftone(True)
    count = 0
    for t in tags:
        try: 
            t.tag_view.SetElementOverrides(t.ID,graphic_halftone)
            count +=1 
        except:
             pass 
    return count 

"""Create Tag Class"""
class Tag:
    def __init__(self,tag):
        self.tag= tag
    
    @property
    def tag_view(self):
        Owner_id = self.tag.OwnerViewId
        view = doc.GetElement(Owner_id)
        return view  
    
    @property
    def el_phase(self):
        try:
            element = doc.GetElement(self.tag.TaggedLocalElementId)
            phase = element.get_Parameter(BuiltInParameter.PHASE_CREATED).AsValueString()
            existing = True if phase == 'Existing' else False 
        except:
            existing = False 
        return existing  
    
    @property    
    def ID(self):
        return self.tag.Id 


"""Collect Duct, Pipe, and Equipment Tags"""
duct_tag = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_DuctTags).WhereElementIsNotElementType().ToElements()
pipe_tag = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_PipeTags).WhereElementIsNotElementType().ToElements()
equipment_tag = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_MechanicalEquipmentTags).WhereElementIsNotElementType().ToElements()
#Join tags into one list
all_tags = [Tag(i) for i in duct_tag] + [Tag(i) for i in pipe_tag] + [Tag(i) for i in equipment_tag]

# Filter to tags referencing existing elements
ex_tags = [i for i in all_tags if i.el_phase]

#Result Window
Result_window = window(halftone(ex_tags))
