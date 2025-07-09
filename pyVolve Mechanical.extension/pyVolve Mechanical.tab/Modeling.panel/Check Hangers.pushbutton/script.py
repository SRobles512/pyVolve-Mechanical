#  ______   ____     _____  _ __     _______   __  __ _____ ____ _   _    _    _   _ ___ ____    _    _     
# |  _ \ \ / /\ \   / / _ \| |\ \   / / ____| |  \/  | ____/ ___| | | |  / \  | \ | |_ _/ ___|  / \  | |    
# | |_) \ V /  \ \ / / | | | | \ \ / /|  _|   | |\/| |  _|| |   | |_| | / _ \ |  \| || | |     / _ \ | |    
# |  __/ | |    \ V /| |_| | |__\ V / | |___  | |  | | |__| |___|  _  |/ ___ \| |\  || | |___ / ___ \| |___ 
# |_|    |_|     \_/  \___/|_____\_/  |_____| |_|  |_|_____\____|_| |_/_/   \_\_| \_|___\____/_/   \_\_____|
                                                                                                           
# -*- coding: utf-8 -*-
__title__   = "Check Hanger Host"
__doc__     = """Version = 1.0
Date    = 01.28.2025
________________________________________________________________
Description:
Verifies if Hangers are hosted
If Hangers are not hosted "Not Hosted" is added to the Comment Property for filtering purposes
________________________________________________________________
How-To:
Select the hangers that need verification
Click Pushbutton
________________________________________________________________
Author: Sam Robles
"""
__author__ = "Sam Robles"
__helpurl__ = "https://github.com/SRobles512/pyVolve-Mechanical/wiki"
__min_revit_ver__ = 2022
__max_revit_ver = 2024
__context__     = ['MEP Fabrication Hangers']

# ___ __  __ ____   ___  ____ _____ ____  
#|_ _|  \/  |  _ \ / _ \|  _ \_   _/ ___| 
# | || |\/| | |_) | | | | |_) || | \___ \ 
# | || |  | |  __/| |_| |  _ < | |  ___) |
#|___|_|  |_|_|    \___/|_| \_\|_| |____/
#=========================================
# SYSTEM IMPORTS
import clr

# AUTODESK IMPORTS
clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

# PYREVIT IMPORTS
    #None
# .NET IMPORTS
    #None
# CUSTOM IMPORTS
    #None

#   ____ _     ___  ____    _    _      __     ___    ____  ___    _    ____  _     _____ ____  
#  / ___| |   / _ \| __ )  / \  | |     \ \   / / \  |  _ \|_ _|  / \  | __ )| |   | ____/ ___| 
# | |  _| |  | | | |  _ \ / _ \ | |      \ \ / / _ \ | |_) || |  / _ \ |  _ \| |   |  _| \___ \ 
# | |_| | |__| |_| | |_) / ___ \| |___    \ V / ___ \|  _ < | | / ___ \| |_) | |___| |___ ___) |
#  \____|_____\___/|____/_/   \_\_____|    \_/_/   \_\_| \_\___/_/   \_\____/|_____|_____|____/ 
                                                                                              
app = __revit__.Application
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
selection = uidoc.Selection.GetElementIds()

#  _____ _   _ _   _  ____ _____ ___ ___  _   _ ____  
# |  ___| | | | \ | |/ ___|_   _|_ _/ _ \| \ | / ___| 
# | |_  | | | |  \| | |     | |  | | | | |  \| \___ \ 
# |  _| | |_| | |\  | |___  | |  | | |_| | |\  |___) |
# |_|    \___/|_| \_|\____| |_| |___\___/|_| \_|____/                                                     
# ====================================================


#   ____ _        _    ____ ____  _____ ____  
#  / ___| |      / \  / ___/ ___|| ____/ ___| 
# | |   | |     / _ \ \___ \___ \|  _| \___ \ 
# | |___| |___ / ___ \ ___) |__) | |___ ___) |
#  \____|_____/_/   \_\____/____/|_____|____/                                             
# ============================================


#  __  __    _    ___ _   _ 
# |  \/  |  / \  |_ _| \ | |
# | |\/| | / _ \  | ||  \| |
# | |  | |/ ___ \ | || |\  |
# |_|  |_/_/   \_\___|_| \_|
#===========================
# Check if any elements are selected
if not selection:
    print("No elements selected.")
else:
    #print("Number of elements selected: {0}".format(len(selection)))
    fabrication_part_count = 0  # Counter for FabricationPart elements
    host_id_negative_count = 0  # Counter for HostId = -1

    # Start a transaction to modify the document
    with Transaction(doc, "Update Comments for Not Hosted") as t:
        t.Start()

        for element_id in selection:
            element = doc.GetElement(element_id)
            
            # Check if the element is a FabricationPart
            if isinstance(element, FabricationPart):
                fabrication_part_count += 1
                try:
                    # Get Hosted Info
                    hosted_info = element.GetHostedInfo()

                    if hosted_info:
                        host_id = hosted_info.HostId.IntegerValue  # Extract integer value from ElementId
                        #print("Debug: HostId for element {0} is {1}".format(element.Id, host_id))

                        # Check if HostId is -1
                        if host_id == -1:
                            host_id_negative_count += 1
                            
                            # Modify the Comments property
                            param = element.LookupParameter("Comments")
                            if param and param.StorageType == StorageType.String:
                                param.Set("Not Hosted")
                                #print("Updated Comments for element {0} to 'Not Hosted'.".format(element.Id))

                except Exception as e:
                    print("Error accessing properties for element {0}: {1}".format(element.Id, e))
            else:
                print("Element {0} is not a FabricationPart.".format(element.Id))

        # Commit the transaction
        t.Commit()

    message = (
    "Number of Hangers selected: {0}\n"
    "Number of Hangers with HostId = -1: {1}"
).format(fabrication_part_count, host_id_negative_count)

# Create and show a TaskDialog
dialog = TaskDialog("Hanger Information")
dialog.MainInstruction = "Hanger Count Details"
dialog.MainContent = message
dialog.Show()
