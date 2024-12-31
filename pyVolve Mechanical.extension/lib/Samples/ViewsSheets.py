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

#🟠 Get All View Types
# ALL VIEW TYPES
view_types = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()

# FILTER CERTAIN VIEW TYPES
view_types_plans    = [vt for vt in view_types if vt.ViewFamily == ViewFamily.FloorPlan]
view_types_sections = [vt for vt in view_types if vt.ViewFamily == ViewFamily.Section]
view_types_3D       = [vt for vt in view_types if vt.ViewFamily == ViewFamily.ThreeDimensional]
view_types_legends  = [vt for vt in view_types if vt.ViewFamily == ViewFamily.Legend]
view_types_drafting = [vt for vt in view_types if vt.ViewFamily == ViewFamily.Drafting]
view_types_elev     = [vt for vt in view_types if vt.ViewFamily == ViewFamily.Elevation]
view_types_ceil     = [vt for vt in view_types if vt.ViewFamily == ViewFamily.CeilingPlan]
view_types_stru     = [vt for vt in view_types if vt.ViewFamily == ViewFamily.StructuralPlan]
view_types_area     = [vt for vt in view_types if vt.ViewFamily == ViewFamily.AreaPlan]


# ╔═╗╦═╗╔═╗╔═╗╔╦╗╔═╗  ╦  ╦╦╔═╗╦ ╦╔═╗
# ║  ╠╦╝║╣ ╠═╣ ║ ║╣   ╚╗╔╝║║╣ ║║║╚═╗
# ╚═╝╩╚═╚═╝╩ ╩ ╩ ╚═╝   ╚╝ ╩╚═╝╚╩╝╚═╝ CREATE VIEWS
#----------------------------------------------------------------------------------------------------
#🟠 Create FloorPlan (Same principle for Ceiling, Structural, Area plans. Apply the right ViewType)
view_type_plan_id = doc.GetDefaultElementTypeId(ElementTypeGroup.ViewTypeFloorPlan)
view_floor        = ViewPlan.Create(doc, view_type_plan_id, active_level.Id)

#----------------------------------------------------------------------------------------------------
#🟠 Create 3D View
view_type_3D_id = doc.GetDefaultElementTypeId(ElementTypeGroup.ViewType3D)
view_3d_iso     = View3D.CreateIsometric(doc, view_type_3D_id)
view_3d_per     = View3D.CreatePerspective(doc, view_type_3D_id)

# Set SectionBox to random Room BB.
my_room = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).FirstElement()
room_bb = my_room.get_BoundingBox(view_floor)
view_3d_iso.SetSectionBox(room_bb)

#----------------------------------------------------------------------------------------------------
#🟠 Create Drafting
view_type_draft_id = doc.GetDefaultElementTypeId(ElementTypeGroup.ViewTypeDrafting)
view_draft         = ViewDrafting.Create(doc, view_type_draft_id)

#----------------------------------------------------------------------------------------------------
#🟠 Create Legend

#Get All Legends
all_views   = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).ToElements()
all_views   = [view for view in all_views if not view.IsTemplate]
all_legends = [view for view in all_views if view.ViewType == ViewType.Legend]

#Check Legend in the Project
if not all_legends:
    from pyrevit.forms import alert
    alert('There has to be at least 1 legend view in the project! '
          'Please Create a legend and try again', exitscript=True)

#GET RANDOM LEGEND
random_legend      = all_legends[0]

#CREATE NEW LEGEND VIEW
new_legend_view_id = random_legend.Duplicate(ViewDuplicateOption.Duplicate)
new_legend         = doc.GetElement(new_legend_view_id)

#Change Scale
new_legend.Scale   = 100

#----------------------------------------------------------------------------------------------------
#🟠 Create Section

# Pick a Wall
from Autodesk.Revit.UI.Selection import ObjectType
el_ref = uidoc.Selection.PickObject(ObjectType.Element)
wall   = doc.GetElement(el_ref)

if type(wall) == Wall:

    # Get Curve
    curve = wall.Location.Curve

    # Get Origin Point
    pt_start = curve.GetEndPoint(0)
    pt_end   = curve.GetEndPoint(1)
    pt_mid   = (pt_start + pt_end) /2 # Origin

    # Get Direction Vector
    vector   = pt_end - pt_start # XYZ (10,20,0)
    curvedir = vector.Normalize() *-1# To Flip vector -> Multiply by -1

    # Get Dimensions
    W = curve.Length
    H = wall.get_Parameter(BuiltInParameter.WALL_USER_HEIGHT_PARAM).AsDouble() # In Feet
    D = 10
    D_= 5
    O = 1

    # Create Transform
    trans        = Transform.Identity
    trans.Origin = pt_mid

    trans.BasisX = curvedir
    trans.BasisY = XYZ.BasisZ
    trans.BasisZ = curvedir.CrossProduct(XYZ.BasisZ)

    # Create SectionBox
    sectionBox           = BoundingBoxXYZ()
    sectionBox.Transform = trans

    sectionBox.Min = XYZ(-W/2-O  , 0 -O     , -D_)
    sectionBox.Max = XYZ(W/2 +O  , H +O     , D)
                    # Left/Right  Up/Down   Forward/Backwards


    # Create Section
    view_type_section_id = doc.GetDefaultElementTypeId(ElementTypeGroup.ViewTypeSection)
    view_section = ViewSection.CreateSection(doc, view_type_section_id, sectionBox)


#----------------------------------------------------------------------------------------------------
#🟠 Create Elevations

# Get a Room
my_room = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).FirstElement()

# Create Elevation Marker
view_type_el_id = doc.GetDefaultElementTypeId(ElementTypeGroup.ViewTypeElevation)
room_pt         = my_room.Location.Point
scale           = 50

marker = ElevationMarker.CreateElevationMarker(doc, view_type_el_id, room_pt, scale)

elev_view_0 = marker.CreateElevation(doc, active_view.Id, 0)
elev_view_1 = marker.CreateElevation(doc, active_view.Id, 1)
elev_view_2 = marker.CreateElevation(doc, active_view.Id, 2)
elev_view_3 = marker.CreateElevation(doc, active_view.Id, 3)

# ╔═╗╦  ╦╔═╗╦═╗╦═╗╦╔╦╗╔═╗  ╔═╗╦═╗╔═╗╔═╗╦ ╦╦╔═╗╔═╗
# ║ ║╚╗╔╝║╣ ╠╦╝╠╦╝║ ║║║╣   ║ ╦╠╦╝╠═╣╠═╝╠═╣║║  ╚═╗
# ╚═╝ ╚╝ ╚═╝╩╚═╩╚═╩═╩╝╚═╝  ╚═╝╩╚═╩ ╩╩  ╩ ╩╩╚═╝╚═╝ OVERRIDE GRAPHICS
#----------------------------------------------------------------------------------------------------
#🟠 Override Graphic Overrides of selected element

from Autodesk.Revit.UI.Selection import ObjectType

# PICK AN ELEMENT
ref_object = uidoc.Selection.PickObject(ObjectType.Element)
elem       = doc.GetElement(ref_object)

#️ Create Override Settings
override_settings = OverrideGraphicSettings()

# Define Color
color = Color(255,200,0)

# GET FILL PATTERN
all_patterns  = FilteredElementCollector(doc).OfClass(FillPatternElement).ToElements()
solid_pattern = [i for i in all_patterns if i.GetFillPattern().IsSolidFill][0]

# GET LINE PATTERNS AND WEIGHT
line_patterns       = FilteredElementCollector(doc).OfClass(LinePatternElement).ToElements()
random_line_pattern = line_patterns[0]
lineweight          = 5


#️ Modify Override Settings (COLOR, COLOR PATTERN, LINE PATTERN, LINEWEIGHT)
override_settings.SetSurfaceForegroundPatternId(solid_pattern.Id)
override_settings.SetSurfaceForegroundPatternColor(color)
override_settings.SetProjectionLinePatternId(random_line_pattern.Id)
override_settings.SetProjectionLineColor(color)
override_settings.SetProjectionLineWeight(lineweight)

# More Settings
override_settings.SetSurfaceTransparency(45)
override_settings.SetHalftone(True)

# Transaction 🔓
t = Transaction(doc, 'Override Graphics')
t.Start()

active_view = doc.ActiveView
active_view.SetElementOverrides(elem.Id, override_settings)

t.Commit()


# ╦═╗╔═╗╔╗╔╔═╗╔╦╗╔═╗
# ╠╦╝║╣ ║║║╠═╣║║║║╣
# ╩╚═╚═╝╝╚╝╩ ╩╩ ╩╚═╝
#----------------------------------------------------------------------------------------------------

view = doc.ActiveView

# RENAME VIEW UNIQUE by adding * symbol.
new_name =  'EF New View'
for i in range(20):
    try:
        view.Name = new_name
        break
    except:
        new_name += '*'







# ╔═╗╦═╗╔═╗╔═╗╔╦╗╔═╗  ╦  ╦╦╔═╗╦ ╦  ╔═╗╦╦ ╔╦╗╔═╗╦═╗╔═╗
# ║  ╠╦╝║╣ ╠═╣ ║ ║╣   ╚╗╔╝║║╣ ║║║  ╠╣ ║║  ║ ║╣ ╠╦╝╚═╗
# ╚═╝╩╚═╚═╝╩ ╩ ╩ ╚═╝   ╚╝ ╩╚═╝╚╩╝  ╚  ╩╩═╝╩ ╚═╝╩╚═╚═╝
#----------------------------------------------------------------------------------------------------
all_par_filters      = FilteredElementCollector(doc).OfClass(ParameterFilterElement).ToElements()
all_par_filter_names = [f.Name for f in all_par_filters]

wall_types      = FilteredElementCollector(doc).OfClass(WallType).ToElements()
wall_type_names = [Element.Name.GetValue(typ) for typ in wall_types]


with Transaction(doc, 'Create VewFilter') as t:
    t.Start()

    for wall_type_name in wall_type_names:
            filter_name = 'WallType_{}'.format(wall_type_name)

            if not filter_name in all_par_filter_names:

                #🐈 Select ViewFilter Category
                cats = List[ElementId]()
                cats.Add(ElementId(BuiltInCategory.OST_Walls))

                #1️⃣ Rule 1 - Wall Function
                pvp    = ParameterValueProvider(ElementId(BuiltInParameter.SYMBOL_NAME_PARAM))
                rule_1 = FilterStringRule(pvp, FilterStringEquals(), wall_type_name) # 4 arguments in Revit 2021!

                #💪 Create an Element Parameter Filter
                wall_filter = ElementParameterFilter(rule_1)

                #🎯 Create View Filter
                view_filter = ParameterFilterElement.Create(doc, filter_name, cats, wall_filter)


                #🎨 Get Color and Solid Pattern
                import random
                color = Color(random.randint(200, 255),random.randint(200, 255),random.randint(200, 255))
                all_patterns = FilteredElementCollector(doc).OfClass(FillPatternElement).ToElements()
                solid_pattern = [i for i in all_patterns if i.GetFillPattern().IsSolidFill][0]

                #🖌️ Create Override Settings
                override_settings = OverrideGraphicSettings()
                override_settings.SetSurfaceForegroundPatternId(solid_pattern.Id)
                override_settings.SetSurfaceForegroundPatternColor(color)

                #✅ Apply the override to a view (e.g., active view)
                active_view = doc.ActiveView
                active_view.AddFilter(view_filter.Id)
                active_view.SetFilterOverrides(view_filter.Id, override_settings)
    t.Commit()

# ╦ ╦╔═╗╔═╗╔═╗╦ ╦  ╔═╗╔═╗╔╦╗╦╔╗╔╔═╗  ||
# ╠═╣╠═╣╠═╝╠═╝╚╦╝  ║  ║ ║ ║║║║║║║ ╦  ||
# ╩ ╩╩ ╩╩  ╩   ╩   ╚═╝╚═╝═╩╝╩╝╚╝╚═╝  .. ⌨️ HAPPY CODING!

# Find More Snippets Here:              - www.LearnRevitAPI.com/python-snippets
# E-Book: Beginner's Guide to Revit API - www.LearnRevitAPI.com/ebook
# E-Book: Master Getting Elements (FEC) - www.LearnRevitAPI.com/ebook/fec

