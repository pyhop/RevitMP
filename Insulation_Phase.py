
"""This script looks at all the insulation in the project, grabs the duct that the insulation is on, 
and matches the created phase. Works for insulation inside groups as well. 
"""
__title__ = 'Match Insulation to Duct Phase'
__author__= 'marentette'

from Autodesk.Revit.DB import FilteredElementCollector,BuiltInCategory,Transaction 

from june import revit_transaction 

@revit_transaction("Match Insulation Phase to Duct")
def set_insulation (ducts,insulation):
    for d,i in zip(ducts,insulation):
        i.CreatedPhaseId  = d.CreatedPhaseId
    
doc = __revit__.ActiveUIDocument.Document

insulation = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_DuctInsulations).WhereElementIsNotElementType().ToElements() 

ducts = [doc.GetElement(x.HostElementId) for x in insulation]
  
if __name__ == '__main__':
    set_insulation(ducts,insulation) 

