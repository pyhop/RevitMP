from functools import wraps
from Autodesk.Revit.Exceptions import InvalidOperationException
import Autodesk
import System
from Autodesk.Revit.DB import *
doc = __revit__.ActiveUIDocument.Document

"""Decorator Curtosity of Gui Talarico"""

def revit_transaction(transaction_name):
    def wrap(f):
        @wraps(f)
        def wrapped_f(*args):
            try:
                t = Transaction(doc, transaction_name)
                t.Start()
            except InvalidOperationException as errmsg:
                print('Transaciton Error: {}'.format(errmsg))
                return_value = f(*args)
            else:
                return_value = f(*args)
                t.Commit()
            return return_value
        return wrapped_f
    return wrap

