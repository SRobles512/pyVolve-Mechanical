# -*- coding: utf-8 -*-

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
#====================================================================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import ISelectionFilter, Selection, ObjectType

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
#==================================================
app       = __revit__.Application
uidoc     = __revit__.ActiveUIDocument
doc       = __revit__.ActiveUIDocument.Document #type:Document
selection = uidoc.Selection                     #type: Selection

# ╔═╗╔═╗╦═╗╔═╗╔╦╗╔═╗╔╦╗╔═╗╦═╗╔═╗  ╔═╗╔═╗╔╦╗╔═╗╦  ╔═╗╔═╗
# ╠═╝╠═╣╠╦╝╠═╣║║║║╣  ║ ║╣ ╠╦╝╚═╗  ╚═╗╠═╣║║║╠═╝║  ║╣ ╚═╗
# ╩  ╩ ╩╩╚═╩ ╩╩ ╩╚═╝ ╩ ╚═╝╩╚═╚═╝  ╚═╝╩ ╩╩ ╩╩  ╩═╝╚═╝╚═╝ PARAMETERS SAMPLES
#====================================================================================================
#🟧 Pick Object to work with parameters
ref_picked_object = selection.PickObject(ObjectType.Element)
picked_object     = doc.GetElement(ref_picked_object)

#--------------------------------------------------
#🟠 Get All Instance/Type Parameters
# Keep in mind that you can't get Type parameters from an Instance.
#     You can get Instance Parameters from an Instance
# And You can get Type     Parameters from a  Type
# You can always get a type with .GetTypeId()

instance_params = picked_object.Parameters

# Get Type Parameters from Type!
picked_object_type = doc.GetElement(picked_object.GetTypeId())
type_params        = picked_object_type.Parameters

#--------------------------------------------------
#🟠 Read Parameter Properties
def get_param_value(param):
    """Get a value from a Parameter based on its StorageType."""
    value = None
    if param.StorageType == StorageType.Double:      value = param.AsDouble()
    elif param.StorageType == StorageType.ElementId: value = param.AsElementId()
    elif param.StorageType == StorageType.Integer:   value = param.AsInteger()
    elif param.StorageType == StorageType.String:    value = param.AsString()
    return value

# Read All Instance Parameters of an Element
for p in picked_object.Parameters:
    print("Name: {}".format(p.Definition.Name))
    print("ParameterGroup: {}".format(p.Definition.ParameterGroup))
    print("BuiltInParameter: {}".format(p.Definition.BuiltInParameter))
    print("IsReadOnly: {}".format(p.IsReadOnly))
    print("HasValue: {}".format(p.HasValue))
    print("IsShared: {}".format(p.IsShared))
    print("StorageType: {}".format(p.StorageType))
    print("Value: {}".format(get_param_value(p)))
    print("AsValueString(): {}".format(p.AsValueString()))
    print('-'*100)

#--------------------------------------------------
#🟠 Get Built-In Parameter
# You can check BuilltInParameter wit RevitLookup under Parameters -> Definition -> BuiltInParameter (p.Definition.BuiltInParameter)
comments = picked_object.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)
mark     = picked_object.get_Parameter(BuiltInParameter.ALL_MODEL_MARK)
el_type  = picked_object.get_Parameter(BuiltInParameter.ELEM_TYPE_PARAM)

#--------------------------------------------------
#🟠 Get Project/Shared Parameters
custom_p1 = picked_object.LookupParameter("P_NAME_1")
custom_p2 = picked_object.LookupParameter("P_NAME_1")

# It's good to check if you got the parameter when you use LookupParameter 😉
if custom_p1:
    print(custom_p1.AsValueString())

#--------------------------------------------------
#🟠 Set Parameter Values
# Parameter should not be IsReadOnly!
# Make sure you use Transaction to allow changes in the project
# Provide values in the correct StorageType. You can check p.StorageType Property. (String/Integer/Double/ElementId)

with Transaction(doc, __title__) as t:
    t.Start()

    comments.Set('EF-Comment')  #StorageType.String
    mark.Set('EF-Mark')         #StorageType.String
    custom_p1.Set(69)           #StorageType.Integer

    t.Commit()

#--------------------------------------------------
#🟠 Check Loaded Parameters / Ensure SharedParameter Loaded

def check_loaded_params(list_p_names):
    """Check if any parameters from provided list are missing in the project
    :param list_p_names: List of Parameter Names
    :return:             List of Missing Parameter Names"""
    # 📃 Get Parameter Bindings Map.
    bm = doc.ParameterBindings

    # 💡 Create a forward iterator
    itor = bm.ForwardIterator()
    itor.Reset()

    #ITerate over the map
    loaded_parameters = []
    while itor.MoveNext():
        try:
            d = itor.Key
            loaded_parameters.append(d.Name)
        except:
            pass

    # ✅ Check if Parameters are loaded:
    missing_params = [p_name for p_name in list_p_names if p_name not in loaded_parameters]

    # 👆 This is same as this 👇 just one-liner vs multi-line.

    # missing_params = []
    # for p_name in req_params:
    #     if p_name not in loaded_parameters:
    #         missing_params.append(p_name)

    return missing_params



# ╦ ╦╔═╗╔═╗╔═╗╦ ╦  ╔═╗╔═╗╔╦╗╦╔╗╔╔═╗  ||
# ╠═╣╠═╣╠═╝╠═╝╚╦╝  ║  ║ ║ ║║║║║║║ ╦  ||
# ╩ ╩╩ ╩╩  ╩   ╩   ╚═╝╚═╝═╩╝╩╝╚╝╚═╝  .. ⌨️ HAPPY CODING!

# Find More Snippets Here:              - www.LearnRevitAPI.com/python-snippets
# E-Book: Beginner's Guide to Revit API - www.LearnRevitAPI.com/ebook
# E-Book: Master Getting Elements (FEC) - www.LearnRevitAPI.com/ebook/fec

