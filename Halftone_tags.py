"""Halftone Tags.

Note:
Halftone tags referencing 
existing phased elements 
"""
__title__ = 'Halftone\nTags' 
__author__= 'marentette'
##Import Libraries 
import clr
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Transactions import TransactionManager
from Autodesk.Revit.UI import *
doc = __revit__.ActiveUIDocument.Document

"""Define Result Window"""
def window(numberoftags):
    dialog = TaskDialog("Header")
    dialog.MainInstruction = "Results"
    dialog.MainContent = "{0} tags were switched to {1}".format(numberoftags,'halftone')
    dialog.CommonButtons = TaskDialogCommonButtons.Close;
    return dialog.Show()

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
    def phase(self):
        element = doc.GetElement(self.tag.TaggedLocalElementId)
        phase = element.get_Parameter(BuiltInParameter.PHASE_CREATED).AsValueString()
        return True if phase == 'Existing' else False   
    
    @property    
    def ID(self):
        return self.tag.Id 

"""Collect Duct, Pipe, and Mechanical Equipment Tags"""
duct_tag = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_DuctTags).WhereElementIsNotElementType().ToElements()
pipe_tag = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_PipeTags).WhereElementIsNotElementType().ToElements()
equipment_tag = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_MechanicalEquipmentTags).WhereElementIsNotElementType().ToElements()

#Join tags into one list
all_tags = [Tag(i) for i in duct_tag] + [Tag(i) for i in pipe_tag] + [Tag(i) for i in equipment_tag]

# Filter tags to ones referencing existing elements
ex_tags = [i for i in all_tags if i.phase]

#Create Graphic Settings for Halftone Tags
graphic_halftone = OverrideGraphicSettings().SetHalftone(True)

#Start Transaction 
t1 = Transaction(doc, 'Halftone Tags')
t1.Start()
count = 0
for t in ex_tags:
    try: 
        t.tag_view.SetElementOverrides(t.ID,graphic_halftone)
        count +=1 
    except:
         pass 
t1.Commit()
Result_window = window(count)
