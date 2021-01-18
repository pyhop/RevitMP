"""Adds detail lines around selected pipes or ducts in view.
"""
__title__ = 'Trace Pipes or Ducts' 
__author__= 'marentette'

from Autodesk.Revit.DB import(
Element,
GraphicsStyleType,
BuiltInParameter,
XYZ, 
Line, 
BuiltInCategory  
)
from Autodesk.Revit.DB.Plumbing import Pipe  
from Autodesk.Revit.DB.Mechanical import Duct 

from june import revit_transaction 

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

def exit_(reason): 
    """Exit Function"""
    import sys
    from pyrevit import forms
    forms.alert(reason)
    return sys.exit() 
    
@revit_transaction('Trace')
def trace_elements(elements,factor,view):
    """Trace Selected Elements"""
    for e in elements: 
        BB_Box(e,view).Trace(factor,line_style('Dashed'))

def selected():
    """Get Selected Elements"""
    selection_ids = uidoc.Selection.GetElementIds()
    get_elements = [doc.GetElement(e) for e in selection_ids]
    elements = [e for e in get_elements if isinstance(e, Pipe) or isinstance(e, Duct)]
    return elements if elements else exit_('Select elements before running') 

def line_style(style = str):
    """Line Style"""
    line= doc.Settings.Categories.get_Item(BuiltInCategory.OST_Lines)
    return line.SubCategories.get_Item(style).GetGraphicsStyle(GraphicsStyleType.Projection)


class BB_Box:
    def __init__(self,element,view):
        self.element = element 
        self.view = view 

    def Trace(self,factor,line_style):
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
        if (abs(BB.Max[0]) - abs(BB.Min[0])) > (abs(BB.Max[1]) - abs(BB.Min[1])): 
            start = [pt1,pt2]
            end = [pt4,pt3]
        else: 
            start = [pt1,pt3]
            end = [pt2,pt4]
        """Create Line"""
        lines = [] 
        for i,j in zip(start,end):
            L = Line.CreateBound(i,j)
            doc.Create.NewDetailCurve(self.view, L).LineStyle= line_style

if __name__ == '__main__':
    trace_elements(selected(),0.5,doc.ActiveView)
