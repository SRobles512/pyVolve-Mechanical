# -*- coding: utf-8 -*-
__title__   = "Align by BOI"
__doc__     = """Version = 1.0
Date    = 01.03.2025
________________________________________________________________
Description:
This script aligns selected fabrication parts to a reference part's 
Bottom of Insulation elevation. It supports single or multiple element selection
for alignment.
________________________________________________________________
How-To:
1. Run the script
2. Select the reference pipe (this sets the target elevation)
3. Select one or more pipes to align
4. The selected pipes will be aligned to match the reference elevation
________________________________________________________________
TODO:
________________________________________________________________
Last Updates:
- [01.03.2025] RELEASE
________________________________________________________________
Author: Sam Robles"""

#IMPORTS
#==================================================
# Autodesk Imports
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Fabrication import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import ObjectType, ISelectionFilter

#pyRevit Imports
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms

#.NET Imports
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
import System

#VARIABLES
#==================================================
app = __revit__.Application
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

# Debug mode flag
DEBUG_MODE = False  # Set to True to enable debug prints

# Parameter name we're working with
PARAM_NAME = "Lower End Bottom of Insulation Elevation"

#CLASSES
#==================================================
# Custom Filter Class
class FabricationPartFilter(ISelectionFilter):
    def AllowElement(self, element):
        if isinstance(element, FabricationPart):
            return True
        return False
    
    def AllowReference(self, reference, point):
        return True

#FUNCTIONS
#==================================================
def debug_print(message):
    """Print debug messages if DEBUG_MODE is True"""
    if DEBUG_MODE:
        print("DEBUG: %s" % str(message))

def get_parameter_value(element, param_name):
    """Gets the value of a parameter from an element"""
    param = element.LookupParameter(param_name)
    if param and param.StorageType == StorageType.Double:
        try:
            value = param.AsDouble()
            debug_print("Parameter value: {0}".format(value))
            return value
        except Exception as ex:
            debug_print("Error getting elevation: %s" % str(ex))
            return None
    else:
        debug_print("Parameter {0} not found or invalid type".format(param_name))
        return None

def set_parameter_value(element, param_name, value):
    """Sets the value of a parameter for an element"""
    param = element.LookupParameter(param_name)
    if param and param.StorageType == StorageType.Double and not param.IsReadOnly:
        try:
            param.Set(value)
            debug_print("Set parameter {0} to {1}".format(param_name, value))
            return True
        except Exception as ex:
            debug_print("Error setting parameter: %s" % str(ex))
            return False
    return False

#MAIN SCRIPT
#==================================================
def main():
    # Create selection filter
    fab_filter = FabricationPartFilter()
    
    try:
        # Get reference part
        forms.alert("Please select the reference pipe.", title="Select Reference Pipe")
        ref_element = uidoc.Selection.PickObject(
            ObjectType.Element,
            fab_filter,
            "Select reference pipe"
        )
        ref_part = doc.GetElement(ref_element.ElementId)
        
        # Get reference elevation
        ref_elevation = get_parameter_value(ref_part, PARAM_NAME)
        if ref_elevation is None:
            forms.alert("Failed to get reference elevation.", title="Error")
            return
            
        # Get parts to modify
        forms.alert("Please select the pipes you wish to align.", title="Select Pipes")
        parts_to_move = uidoc.Selection.PickObjects(
            ObjectType.Element,
            fab_filter,
            "select the pipes you wish to align"
        )
        
        # Process selected parts
        with revit.Transaction("Align Parts by BOI"):
            success_count = 0
            for part_ref in parts_to_move:
                part = doc.GetElement(part_ref.ElementId)
                if set_parameter_value(part, PARAM_NAME, ref_elevation):
                    success_count += 1
        
        # Report results
        forms.alert(
            "Successfully aligned {0} of {1} pipes.".format(success_count, len(parts_to_move)),
            title="Operation Complete"
        )
            
    except Exception as e:
        debug_print("Error in main: %s" % str(e))
        forms.alert("Operation cancelled or failed.", title="Error")

# Run main script
if __name__ == '__main__':
    main()
#==================================================

