"""Opens model without Revit interface
"""
__title__ = 'Ope'
__author__= 'marentette'

from Autodesk.Revit.DB import OpenOptions,\
DetachFromCentralOption,FilteredElementCollector,Level

from Autodesk.Revit.DB.Macros.ApplicationEntryPoint import OpenDocumentFile
from Autodesk.Revit.DB.ModelPathUtils import ConvertUserVisiblePathToModelPath

from pyrevit import forms 

def background_open(audit= bool,detachFromCentral = bool,preserveWorksets = bool):
    """Opens a model in the background without Revit Interface"""
    filePath = forms.pick_file() 
    app = __revit__.Application
    openOpts =  OpenOptions()
    openOpts.Audit = audit   
    if detachFromCentral == False:
    	openOpts.DetachFromCentralOption = DetachFromCentralOption.DoNotDetach       
    else:
    	if preserveWorksets:
    		openOpts.DetachFromCentralOption = DetachFromCentralOption.DetachAndPreserveWorksets
    	else:
    		openOpts.DetachFromCentralOption = DetachFromCentralOption.DetachAndDiscardWorksets  
    modelPath = ConvertUserVisiblePathToModelPath(filePath)
    background_doc = 	app.OpenDocumentFile(modelPath, openOpts)
    return background_doc

if __name__=='__main__':
    doc_background = background_open(True,False,True)
