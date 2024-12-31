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

# ╔═╗╔═╗╦  ╔═╗╔═╗╔╦╗╦╔═╗╔╗╔  ╔═╗╔═╗╔╦╗╔═╗╦  ╔═╗╔═╗
# ╚═╗║╣ ║  ║╣ ║   ║ ║║ ║║║║  ╚═╗╠═╣║║║╠═╝║  ║╣ ╚═╗
# ╚═╝╚═╝╩═╝╚═╝╚═╝ ╩ ╩╚═╝╝╚╝  ╚═╝╩ ╩╩ ╩╩  ╩═╝╚═╝╚═╝ SELECTION SAMPLES
#====================================================================================================
#🟠 1. Get Selected Elements
selected_element_ids = selection.GetElementIds()
selected_elements    = [doc.GetElement(e_id) for e_id in selected_element_ids]

# Filter Selection (Optionally)
filtered_elements = [el for el in selected_elements if type(el) == Wall]

#--------------------------------------------------
#🟠 2. Pick Elements by Rectangle
selected_elements = selection.PickElementsByRectangle('Select some Elements.')
print(selected_elements)

#--------------------------------------------------
#🟠 3. Pick Object
ref_picked_object = selection.PickObject(ObjectType.Element)
picked_object = doc.GetElement(ref_picked_object)
print(picked_object)

#--------------------------------------------------
#🟠 4. Pick Objects (Multiple)
ref_picked_objects = selection.PickObjects(ObjectType.Element)
picked_objects     = [doc.GetElement(ref) for ref in ref_picked_objects]

for el in picked_objects:
    print(el)
#--------------------------------------------------

#🟠 5. Pick Point
selected_pt = selection.PickPoint()
print(selected_pt, type(selected_pt))

#--------------------------------------------------
#🟠 6. PickBox
picked_box = selection.PickBox(PickBoxStyle.Directional)
print(picked_box)
print(picked_box.Min)
print(picked_box.Max)

#--------------------------------------------------
#🟠 7. Set Selection in Revit UI
new_selection = FilteredElementCollector(doc).OfClass(Wall).ToElementIds()
selection.SetElementIds(new_selection)

# #💡 P.S. If You have a python list you need to turn it into List[ElementId] ;)
List_el_ids = List[ElementId]()
for el_id in list_element_ids:
    List_el_ids.Add(el_id)




# ╦  ╦╔╦╗╦╔╦╗  ╔═╗╔═╗╦  ╔═╗╔═╗╔╦╗╦╔═╗╔╗╔
# ║  ║║║║║ ║   ╚═╗║╣ ║  ║╣ ║   ║ ║║ ║║║║
# ╩═╝╩╩ ╩╩ ╩   ╚═╝╚═╝╩═╝╚═╝╚═╝ ╩ ╩╚═╝╝╚╝ LIMIT SELECTION
#====================================================================================================
#🟠 ISelectionFilter
class ISF_wall_filter(ISelectionFilter):
    def AllowElement(self, element):
        """Define Rules for elements that can be selected.
        Use element variable for checking parameters, type or anything you would check on the element.
        Errors here will be suppressed and element selection will not be allowed. """
        if type(element) == Wall:
            return True

# Apply ISelectionFilter to PickElementsByRectangle
custom_filter     = ISF_wall_filter()
selected_elements = selection.PickElementsByRectangle(custom_filter, "Select rooms ")
print(selected_elements)


# ╦ ╦╔═╗╔═╗╔═╗╦ ╦  ╔═╗╔═╗╔╦╗╦╔╗╔╔═╗  ||
# ╠═╣╠═╣╠═╝╠═╝╚╦╝  ║  ║ ║ ║║║║║║║ ╦  ||
# ╩ ╩╩ ╩╩  ╩   ╩   ╚═╝╚═╝═╩╝╩╝╚╝╚═╝  .. ⌨️ HAPPY CODING!

# Find More Snippets Here:              - www.LearnRevitAPI.com/python-snippets
# E-Book: Beginner's Guide to Revit API - www.LearnRevitAPI.com/ebook
# E-Book: Master Getting Elements (FEC) - www.LearnRevitAPI.com/ebook/fec

