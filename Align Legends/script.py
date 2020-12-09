"""Align Legends on Sheets.

Note:
Aligns legends on multiple sheets
from user selected aligned legend
"""

__author__= 'marentette'
__title__ = "Align\nLegends"

from collections import namedtuple

import sys

from Autodesk.Revit.DB import \
FilteredElementCollector,BuiltInCategory

import Autodesk

from pyrevit import forms

from june import revit_transaction   

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

    
def selected_legend():
    """Get Box Outline Point of User Selected Legend"""
    with forms.WarningBar(title='Select Legend on Sheet'):
        selected_element = doc.GetElement(uidoc.Selection.PickObject(Autodesk.Revit.UI.Selection.ObjectType.Element))
    select_legend = -1
    try:
        if doc.GetElement(selected_element.ViewId).ViewType.ToString() == 'Legend':
            select_legend = selected_element
    except: pass        

    return select_legend 
    

def legend_views(viewports): 
    """Create namedtuple with Legends in Model"""
    Legends = []
    Legend = namedtuple('Legend','viewport legend_name sheet sheet_name')
    for v in viewports:
        if doc.GetElement(v.ViewId).ViewType.ToString() == 'Legend': 
            create_namedtuple = Legend(v,doc.GetElement(v.ViewId).Name,doc.GetElement(v.SheetId),doc.GetElement(v.SheetId).Name)
            if create_namedtuple:
                Legends.append(create_namedtuple)
        else: pass
    return Legends

@revit_transaction('Align Legends')
def move_legend(selected_point,legends_to_move):
    """Align Legend on Sheet"""
    for L in legends_to_move:
        vector = selected_point.Subtract(L.GetBoxOutline().MaximumPoint)
        new_center = L.GetBoxCenter().Add(vector)
        new_location = L.SetBoxCenter(new_center)
                
if __name__ == '__main__':
     
    #namedtuples
    viewports = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Viewports).WhereElementIsNotElementType().ToElements()   
    legends = legend_views(viewports) 
    
    #User Selected Legend
    selected_legend = selected_legend()
    if selected_legend == -1:
        forms.alert('You did not select a legend on the sheet, please try again', title='Error')
        sys.exit() 
    else:
        selected_name = doc.GetElement(selected_legend.ViewId).Name
        selected_point = selected_legend.GetBoxOutline().MaximumPoint
        
        #Ask User to Select Sheets to Move Legend On
        same_legends = [L for L in legends if L.legend_name == selected_name]
        viewports =[L.viewport for L in same_legends]
        sheet_names = [L.sheet_name for L in same_legends]
        option_dict = dict(zip(sheet_names,viewports)) 
        selected_sheets = forms.SelectFromList.show(sheet_names,
                                                    multiselect=True, 
                                                    title= 'Select Sheets To Move Legend Ons', 
                                                    button_name='Align Legends') 
        
        legends_to_align = [option_dict[s] for s in selected_sheets if s in option_dict] 
        
        #Align Legends
        move = move_legend(selected_point,legends_to_align)
