"""Create Walls
Note: 
Creates walls
from detail lines in active view

author @ marentette
 """
__title__ = 'Create\nWalls'

from Autodesk.Revit.DB import \
FilteredElementCollector,Wall,\
BuiltInCategory,Line,Transaction 

#Import UI 
import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')
from pyrevit import script
xamlfile = script.get_bundle_file('ui.xaml')
import wpf
from System import Windows
################Definitions##############################        
doc = __revit__.ActiveUIDocument.Document
def combo_data(): 
    D =  FilteredElementCollector(doc).OfClass(Wall)
    family = [i for i in D]
    names = [i.Name for i in D]
    mydict = dict(zip(names,family))
    unique = list(set(names))
    elements = [mydict[k] for k in unique if k in mydict]
    return elements
    
########Class Window
class MyWindow(Windows.Window):
    def __init__(self):
        wpf.LoadComponent(self, xamlfile)
        #Define Drop Down UI Values
        self.text = combo_data()
        self.combobox_wall.DataContext = self.text
               
    def Set_tag(self, sender, e):
        self.Close()
        wall = self.combobox_wall.SelectedItem
        height = self.start.Value
        view = doc.ActiveView
        lines = FilteredElementCollector(doc,view.Id).OfCategory(BuiltInCategory.OST_Lines).WhereElementIsNotElementType().ToElements()
        level = view.LookupParameter('Associated Level')
        actlevelid = level.AsString()
        #Collect All Levels
        levels= FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
        ##Determine Active Level id 
        for i in levels:
            if i.Name == actlevelid:
                levelid = i.Id
        start = []
        end = []
        for i in lines:
            try:
                S= i.Location.Curve.GetEndPoint(0) 
                E= i.Location.Curve.GetEndPoint(1)
                if S and E:
                    start.append(S)
                    end.append(E)
            except:
                pass
        curves = []
        for s,e in zip(start,end):
            L = Line.CreateBound(s,e)
            if L: 
                curves.append(L)
        t1 = Transaction(doc, "Create Lines")
        t1.Start()
        for i in curves:
            wall = Wall.Create(doc, i, wall.WallType.Id, levelid, height, 0, False, False)
        t1.Commit()
MyWindow().ShowDialog()
