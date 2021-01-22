"""
GUI 
"""
__author__ = 'marentette'

from rpw.ui.forms import(
FlexForm, 
Label, 
ComboBox, 
TextBox, 
TextBox,
CheckBox,
Separator, 
Button
)
from pyrevit import forms

def flex_form(combo_values = dict, default_text = str):
    """Main Window"""
    components = [Label('Select View Template:'),
                  ComboBox('template', combo_values),
                  Separator(),
                  Label('Enter Suffix:'),
                  TextBox('suffix', Text= default_text),
                  Separator(),
                  CheckBox('select_levels', 'Select Levels'),
                  CheckBox('all_levels', 'All Levels',default= True),
                  Button('Create Views')
                  ]
    form = FlexForm('Create Views', components)
    form.show()
    return form 

def select_levels(doc,levels):
    """Select Levels"""
    level_dict = {level.Name:level for level in levels}  
    selected_levels = forms.SelectFromList.show([i.Name for i in levels], 
                                          title= "Select Levels",
                                          width=300, 
                                          multiselect=True, 
                                          button_name='Create Views From Selected Levels')
    return [level_dict[k] for k in selected_levels if k in selected_levels] 
