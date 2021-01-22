"""Script creates floor plan views based on user 
specified levels,view template, and suffix 
"""
__title__ = 'Create Views'
__author__= 'marentette'

from Autodesk.Revit.DB import( 
FilteredElementCollector,
View,
Level,
ViewPlan,
ViewType,
ElementTypeGroup 
)
from rpw import revit,db 
from gui import flex_form,select_levels 

doc = revit.doc

#Collect View Templates
views = list(FilteredElementCollector(doc).OfClass(View).ToElements()) 
view_templates = [v for v in views if v.ViewType==ViewType.FloorPlan and v.IsTemplate]
template_dict =dict(zip([i.Name for i in view_templates],view_templates)) 

#Collect Levels
levels = FilteredElementCollector(doc).OfClass(Level).ToElements() 

#Create Floor Plan View Type 
view_type = doc.GetDefaultElementTypeId(ElementTypeGroup.ViewTypeFloorPlan)

#Launch main window 
user_input = flex_form(template_dict,'Enter Suffix Here').values 

if user_input['select_levels']:
    levels = select_levels(doc,levels)
else: 
    pass 

with db.Transaction(doc=doc, name="Create Views"):
    print('The Following Views were Created' + '\n' + '-'*50)
    for level in levels:
        new_view = ViewPlan.Create(doc,
                                   view_type,
                                   level.Id) 
        new_view.Name = level.Name.upper() + '-' + user_input['suffix']
        new_view.ViewTemplateId = user_input['template'].Id
        print(new_view.Name)
    print('Template --> {}'.format(user_input['template'].Name))
