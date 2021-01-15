"""
Compares ducts area to connect the selected ducts all 
to the largest duct selected. Matches the elevation of the
largest duct to the smaller ducts before connecting
"""
__title__ = 'Duct Selection to Connection' 
__author__= 'marentette'

from Autodesk.Revit.DB import \
BuiltInParameter,XYZ,ElementTransformUtils

from june import revit_transaction

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

def exit_(reason): 
    """Exit Function"""
    from pyrevit import forms
    import sys
    forms.alert(reason)
    return sys.exit() 	


def selected_ducts():
    """Grab User Selections and Exit if No Air Terminals were Selected"""
    selected_elements = uidoc.Selection.GetElementIds()
    if len(selected_elements) > 0: pass
    
    else: exit_('No Elements were Selected')
    
    ducts = [] 
    for e in selected_elements: 
        el = doc.GetElement(e)
        if el.Category.Name == 'Ducts':
            ducts.append(el)
        else: pass 
    return ducts if ducts else exit_('No Ducts Were Selected')


def sort_ducts(ducts):
    """Compare ducts area to find main branch"""
    areas = [d.get_Parameter(BuiltInParameter.RBS_CURVE_SURFACE_AREA).AsDouble() for d in ducts]
    max_index = areas.index(max(areas))# Index of the duct with the max area
    main_duct = ducts[max_index]
    ducts.pop(max_index)
    return main_duct,ducts


def match_elevation(e1,e2):
    """Match Elevation of Elements"""
    if e1.Location.ToString() == 'Autodesk.Revit.DB.LocationCurve' :
        element1location = e1.Location.Curve.GetEndPoint(1)
    else:
        element1location = e1.Location.Point
        
    if e2.Location.ToString() == 'Autodesk.Revit.DB.LocationCurve':
        element2location = e2.Location.Curve.GetEndPoint(1)
    else:
        element2location = e2.Location.Point
    
    vector_z = element1location[2] - element2location[2] 
    vector = XYZ(0,0,vector_z) 
    
    return ElementTransformUtils.MoveElement(doc, e2.Id, vector)

@revit_transaction('Selection to Connection')
def main(ducts):
    """Connect Ducts"""
    main_curve = ducts[0].Location.Curve
    connectors = []
    for d in ducts[1]:
        match_elevation(ducts[0],d)
        connectors = d.ConnectorManager.Connectors
        con,dis = [],[]
        for c in connectors:
            con.append(c)
            dis.append(main_curve.Project(c.Origin).Distance)
        closes_connector = con[dis.index(min(dis))]
        doc.Create.NewTakeoffFitting(closes_connector,ducts[0])    
         
if __name__ =='__main__':
    main(sort_ducts(selected_ducts()))   

	
