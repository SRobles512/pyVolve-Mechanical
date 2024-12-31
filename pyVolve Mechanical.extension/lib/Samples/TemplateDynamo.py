# -*- coding: utf-8 -*-

# This Template is taken from DynamoPrimer
# Link: https://primer.dynamobim.org/10_Custom-Nodes/10-6_Python-Templates.html

#⬇️ Import CLR + Add References (Don't need all)
import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import *

clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import *

clr.AddReference('System')
from System.Collections.Generic import List

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.GeometryConversion)
clr.ImportExtensions(Revit.Elements)

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

#📦 Get Variables
doc = DocumentManager.Instance.CurrentDBDocument
uidoc=DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

# Unwrap Node Input (Dynamo Element to Revit API Element)
element = UnwrapElement(IN[0])

# 🔓 Start and Commit Transaction to make changes in the project
TransactionManager.Instance.EnsureInTransaction(doc)
#changes here
TransactionManager.Instance.TransactionTaskDone()

# Return values from the Dynamo Python Node.
OUT = element

# This Template is taken from DynamoPrimer
# Link: https://primer.dynamobim.org/10_Custom-Nodes/10-6_Python-Templates.html