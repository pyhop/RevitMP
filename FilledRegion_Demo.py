"""Adds a filled region over demolished elements in view.
"""
__title__ = 'Demo\nFilled Region' 
__author__= 'marentette'

from Autodesk.Revit.DB import \
FilledRegionType, Element,\
FilteredElementCollector, BuiltInParameter,\
XYZ, Line, CurveLoop,FilledRegion

from june import revit_transaction 

doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView

@revit_transaction('Demo Filled Region')
def create_filledRegion(elements,factor,fill):
    for e in elements: 
        Box = BB_Box(e,view)
        if Box.phase:
            Box.filled_Region(factor,fill)
        else:
            pass

class BB_Box:
    def __init__(self,element,view):
        self.element = element 
        self.view = view 
   
    @property
    def phase(self):
        try:
            phase = self.element.get_Parameter(BuiltInParameter.PHASE_DEMOLISHED).AsValueString()
            demo = False if phase == 'None' else True 
        except:
            demo = False 
        return demo  
    
    def filled_Region(self,factor,fill):
        BB= self.element.get_BoundingBox(self.view)
        """Expand Boundry Box by Factor"""
        pt1X = (BB.Min[0] - factor) if BB.Min[1] > 0 else (BB.Min[0] - factor)
        pt1Y= (BB.Min[1] - factor) if BB.Min[1] > 0 else (BB.Min[1] - factor)
        pt3X = (BB.Max[0] + factor) if BB.Max[0] > 0 else (BB.Max[0] + factor)
        pt3Y= (BB.Max[1] + factor) if BB.Max[1] > 0 else (BB.Max[1] + factor)
        """Points"""
        pt1 = XYZ(pt1X,pt1Y,0)
        pt2 = XYZ(pt1X,pt3Y,0)
        pt3 = XYZ(pt3X,pt3Y,0)
        pt4 = XYZ(pt3X,pt1Y,0)
        start = [pt1,pt2,pt3,pt4]
        end = [pt2,pt3,pt4,pt1]
        """Create Curveloop"""
        lines = [] 
        for i,j in zip(start,end):
            L = Line.CreateBound(i,j)
            if L:
                lines.append(L)
        curveloop = CurveLoop.Create(lines)
        """Create Filled Region"""
        outRegion  = FilledRegion.Create(doc, fill.Id, self.view.Id, [curveloop])

elements = FilteredElementCollector(doc,view.Id).ToElements() 

"""Enter Desired Filled Region Name"""
Filled_Region_Name = 'Diagonal Down - Transparent'

filled_region_types = FilteredElementCollector(doc).OfClass(FilledRegionType)
for f in filled_region_types:
    if Element.Name.GetValue(f) == Filled_Region_Name:
        fill = f 
    else: 
        pass
"""Enter Size Factor to Extend Around Element"""
factor = 0.5    

create_filledRegion(elements,factor,fill)
