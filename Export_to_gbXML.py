"""
Creates a gbXML file from spaces in Revit model
"""
from Autodesk.Revit.DB import(
FilteredElementCollector,
BuiltInCategory
)
from rpw import revit
from pyrevit import forms
import xml.etree.ElementTree as ET
import os
#current revit document
doc = revit.doc
# Collect Spaces in model
spaces = FilteredElementCollector(doc)\
        .OfCategory(BuiltInCategory.OST_MEPSpaces)\
        .WhereElementIsNotElementType().ToElements()

gbXML = ET.Element("gbXML", lengthUnit="Feet", areaUnit="SquareFeet", useSIUnitsForResults="false", version="1.0")
Campus = ET.SubElement(gbXML, "Campus", id="cmps-1")
Building = ET.SubElement(Campus, "Building", id="bldg-1")


#counter
spaces_created =0
for space in spaces:
    area = space.Area
    #skip space if area is undefined
    if area > 0:
        try:
        	area_string = str(round(area, 0))
        	#split string at "." to truncate the period and the zeros following the period
        	area_print = area_string.split(".")[0]
        	#add space to element tree
        	Space = ET.SubElement(Building, "Space")
        	ET.SubElement(Space, "Name").text = space.LookupParameter("Name").AsString()
        	ET.SubElement(Space, "Area").text = area_print
        	spaces_created +=1
        except:
        	pass
#create xml tree
tree = ET.ElementTree(gbXML)
save_path = os.path.join(forms.pick_folder(title= "Choose folder to Save gbXML file"),"revit_export.xml")
#write to file
tree.write(save_path, encoding="utf-8", xml_declaration=True)

print(str(spaces_created) + " spaces created")
