# -*- coding: utf-8 -*-
__title__   = "List Insulation Types"
__doc__     = """Version = 1.0
Date    = 12.6.2024
________________________________________________________________
Description:
Lists all loaded Insulation Specifications in model, 
displaying the index number before each spec name.
________________________________________________________________
How-To:
1. Click the button to get a list of all loaded Insulation Types.
________________________________________________________________
________________________________________________________________
Last Updates:
- [12.30.2024] - RELEASE
________________________________________________________________
Author: Sam Robles"""

#IMPORTS
# =============================================================

#Revit Imports
from Autodesk.Revit.DB import FabricationConfiguration

# .NET Imports
import clr
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import MessageBox

app = __revit__.Application
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

# Get the Fabrication Configuration object
fab_config = FabricationConfiguration.GetFabricationConfiguration(doc)

# Check if the Fabrication Configuration is valid
if fab_config:
    # Get all insulation specification IDs
    insulation_spec_ids = fab_config.GetAllInsulationSpecifications(None)
    
    # Build the message string
    message = "Insulation Types:\n\n"
    for spec_id in insulation_spec_ids:
        spec_name = fab_config.GetInsulationSpecificationName(spec_id)
        message += "{0}: {1}\n".format(spec_id, spec_name)
    
    # Show the alert dialog
    MessageBox.Show(message, "Insulation Types")
else:
    MessageBox.Show("No Fabrication Configuration found.", "Error")