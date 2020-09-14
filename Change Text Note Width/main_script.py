"""Adjust all textnotes width in document by a multiplier
"""
__title__ = 'Adjust Text Note Width'
__author__= 'marentette'

from Autodesk.Revit.DB import \
FilteredElementCollector,TextNote

from june import revit_transaction 

#Import UI 
import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')
from pyrevit import script
xamlfile = script.get_bundle_file('ui.xaml')
import wpf
from System import Windows

#Collect all textnotes in active document
doc = __revit__.ActiveUIDocument.Document
text_notes= FilteredElementCollector(doc).OfClass(TextNote).WhereElementIsNotElementType().ToElements() 

@revit_transaction('Set Width')
def set_text_width(elements,Multiplier):
    for e in elements:
        new_width = e.Width*Multiplier  
        if e.GetMaximumAllowedWidth() > new_width:
            e.Width = new_width 
        else: 
            e.Width = e.GetMaximumAllowedWidth()
    
class MyWindow(Windows.Window):
    def __init__(self):
        wpf.LoadComponent(self, xamlfile)

    def Set_text(self,sender,args):
        self.Close()
        set_text_width(text_notes,self.Multiplier.Value)
MyWindow().ShowDialog()
