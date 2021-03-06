"""Print sheet names to CSV file 
or sheet number and name in one string to
CSV file saved on users desktop. Sheets 
are sorted by sheet number.
"""
__title__ = 'Sheet Names\nto CSV' 
__author__= 'marentette'

from Autodesk.Revit.DB import \
FilteredElementCollector,BuiltInCategory

from Autodesk.Revit.UI import \
TaskDialog,TaskDialogCommandLinkId

import os
import csv 
doc = __revit__.ActiveUIDocument.Document

#User Options
def window():
    dialog = TaskDialog("Sheet Names to CSV")
    dialog.MainInstruction = 'Options'
    dialog.AddCommandLink(TaskDialogCommandLinkId.CommandLink1, 'Sheet Name and Number','')
    dialog.AddCommandLink(TaskDialogCommandLinkId.CommandLink2, 'Sheet Name Only', '')
    return dialog.Show()

"""Collect Sheet Names and Numbers and Sort By Sheet Number"""
collect_sheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets)
#Filter out placeholder sheets
sheets = [i for i in collect_sheets if not any([i.SheetNumber.Contains('Right')])] 
sorted_sheets = sorted(sheets, key=lambda x: x.SheetNumber)
sheet_names = [i.Name for i in sorted_sheets]
sheet_numbers = [i.SheetNumber for i in sorted_sheets]

user_input = str(window())

"""Create Strings"""
name=[]
if user_input == 'CommandLink1':
    for nam, num in zip(sheet_names,sheet_numbers):
        S = '{0}-{1}'.format(num,nam)
        if S: 
            name.append(S)
else:
    for n in sheet_names:
        S = '{}'.format(n)
        if S:
            name.append(S)

"""Wrtie to CSV & Open"""
filepath = os.path.join(os.environ["USERPROFILE"],"Desktop", "Sheet Names For Print.csv") 
with open(filepath, 'w', ) as myfile:
    wr = csv.writer(myfile, lineterminator = '\n',quoting=csv.QUOTE_ALL)
    for word in name:  
        wr.writerow([word])  
    os.startfile(filepath) 
    
