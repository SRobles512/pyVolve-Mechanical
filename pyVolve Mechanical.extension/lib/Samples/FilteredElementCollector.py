# -*- coding: utf-8 -*-
__welcome__ = """WELCOME!
You will find various code snippets you could easily copy/paste to use in your own sciprt.

Happy Coding!
- Erik Frits"""
# WELCOME TO SAMPLES FILE:


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================
from Autodesk.Revit.DB import *

#.NET Imports
import clr
clr.AddReference('System')
from System.Collections.Generic import List


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
#==================================================
app    = __revit__.Application
uidoc  = __revit__.ActiveUIDocument
doc    = __revit__.ActiveUIDocument.Document #type:Document



# ╔═╗╔═╗╔═╗  ╔═╗╔═╗╔╦╗╔═╗╦  ╔═╗╔═╗
# ╠╣ ║╣ ║    ╚═╗╠═╣║║║╠═╝║  ║╣ ╚═╗
# ╚  ╚═╝╚═╝  ╚═╝╩ ╩╩ ╩╩  ╩═╝╚═╝╚═╝
#==================================================
#💡 Sometimes, getting the right elements is half the solution.

#🔬 FilteredElementCollector Anatomy (Broken by steps):
# | FilteredElementCollector(doc) | OfCategory                      | OfClass               | WhereElement<Is/IsNot>ElementType | ToElements/ToElementIds
# | Provide doc of the project    | Apply Filter by BuiltInCategory | Apply Filter by Class | Filter Instance/Types             | Convert to a list of Elements or Ids



# Get Instance Elements with OfCategory
all_rooms        = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).ToElements()
all_windows      = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Windows).WhereElementIsNotElementType().ToElements()
all_doors        = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()
all_floors       = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Floors).WhereElementIsNotElementType().ToElements()
all_str_col      = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralColumns).WhereElementIsNotElementType().ToElements()
all_generic      = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GenericModel).WhereElementIsNotElementType().ToElements()
all_roofs        = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Roofs).WhereElementIsNotElementType().ToElements()
#...

# Get Type Elements with OfCategory
all_window_types = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Windows).WhereElementIsElementType().ToElements()
all_door_types   = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsElementType().ToElements()
all_floot_types  = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Floors).WhereElementIsElementType().ToElements()
#...

# Get Instance Elements with OfClass
all_walls        = FilteredElementCollector(doc).OfClass(Wall).ToElements()
all_lines        = FilteredElementCollector(doc).OfClass(CurveElement).ToElements()
materials        = FilteredElementCollector(doc).OfClass(Material).ToElements()
#...

# Get Type Elements with OfClass
all_wall_types  = FilteredElementCollector(doc).OfClass(WallType).ToElements()  #Class of Wall/WallType alread
all_floor_types = FilteredElementCollector(doc).OfClass(Floor).ToElements()  #Class of Wall/WallType alread
all_ceil_types  = FilteredElementCollector(doc).OfClass(CeilingType).ToElements()  #Class of Wall/WallType alread
#...


# ╔╦╗╔═╗╦═╗╔═╗  ╔═╗╔═╗╔╦╗╔═╗╦  ╔═╗╔═╗
# ║║║║ ║╠╦╝║╣   ╚═╗╠═╣║║║╠═╝║  ║╣ ╚═╗
# ╩ ╩╚═╝╩╚═╚═╝  ╚═╝╩ ╩╩ ╩╩  ╩═╝╚═╝╚═╝
all_worksets     = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset)
all_materials    = FilteredElementCollector(doc).OfClass(Material).ToElements()
all_lines        = FilteredElementCollector(doc).OfClass(CurveElement).ToElements()
all_detail_lines = [l for l in all_lines if l.CurveElementType == CurveElementType.DetailCurve]
all_model_lines  = [l for l in all_lines if l.CurveElementType == CurveElementType.ModelCurve]
all_regions      = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_FilledRegion).WhereElementIsNotElementType().ToElements()
all_region_types = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_FilledRegion).WhereElementIsElementType().ToElements()
all_symbols      = FilteredElementCollector(doc).OfClass(FamilySymbol).ToElements()
all_tags_walls   = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_WallTags).WhereElementIsNotElementType().ToElements()
all_tags_windows = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_WindowTags).WhereElementIsNotElementType().ToElements()
all_imgs         = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RasterImages).WhereElementIsElementType().ToElements()
all_levels       = FilteredElementCollector(doc).OfClass(Level).ToElements()
all_grids        = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Grids).WhereElementIsNotElementType().ToElements()
all_text_notes   = FilteredElementCollector(doc).OfClass(TextNote).ToElements()
all_spot_elev    = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_SpotElevations).WhereElementIsNotElementType().ToElements()


# ╔═╗╔═╗╔═╗  ╦  ╦╦╔═╗╦ ╦╔═╗
# ╠╣ ║╣ ║    ╚╗╔╝║║╣ ║║║╚═╗
# ╚  ╚═╝╚═╝   ╚╝ ╩╚═╝╚╩╝╚═╝
#==================================================

# GET VIEWS & SHEETS
all_sheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).WhereElementIsNotElementType().ToElements()
all_views  = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()
all_view_filters = FilteredElementCollector(doc).OfClass(FilterElement).ToElementIds()

# Filter Views by type with List Comprehension
all_drafting    = [view for view in all_views if view.ViewType == ViewType.DraftingView]
all_ceil_views  = [view for view in all_views if view.ViewType == ViewType.CeilingPlan]
all_floor_plans = [view for view in all_views if view.ViewType == ViewType.FloorPlan]
all_elevations  = [view for view in all_views if view.ViewType == ViewType.Elevation]
all_area_views  = [view for view in all_views if view.ViewType == ViewType.AreaPlan]
all_sections    = [view for view in all_views if view.ViewType == ViewType.Section]
all_3D_views    = [view for view in all_views if view.ViewType == ViewType.ThreeD]
all_details     = [view for view in all_views if view.ViewType == ViewType.Detail]
all_legends     = [view for view in all_views if view.ViewType == ViewType.Legend]

# GET VIEW TYPES
view_types          = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()
view_types_sections = [vt for vt in view_types if vt.ViewFamily == ViewFamily.Section]
view_types_legends  = [vt for vt in view_types if vt.ViewFamily == ViewFamily.Legend]



# ╔═╗╦╦ ╔╦╗╔═╗╦═╗╔═╗
# ╠╣ ║║  ║ ║╣ ╠╦╝╚═╗
# ╚  ╩╩═╝╩ ╚═╝╩╚═╚═╝



#==================================================
# ╔═╗═╗ ╦╔═╗╦  ╦ ╦╔╦╗╦╔╗╔╔═╗  ╔═╗╦╦ ╔╦╗╔═╗╦═╗
# ║╣ ╔╩╦╝║  ║  ║ ║ ║║║║║║║ ╦  ╠╣ ║║  ║ ║╣ ╠╦╝
# ╚═╝╩ ╚═╚═╝╩═╝╚═╝═╩╝╩╝╚╝╚═╝  ╚  ╩╩═╝╩ ╚═╝╩╚═ Excluding
# Get Current Selection
selected_element_ids = uidoc.Selection.GetElementIds()

if selected_element_ids:
    # Get Everything in view Excluding selected elements
    excl_collector = FilteredElementCollector(doc, active_view.Id)\
        .Excluding(selected_element_ids)\
        .WhereElementIsNotElementType()\
        .ToElements()

    print('There are {} Elements Excluding current selection in the Active View'.format(len(excl_collector)))

# ╔═╗╦  ╔═╗╔╦╗╔═╗╔╗╔╔╦╗  ╦  ╔═╗╦  ╦╔═╗╦    ╔═╗╦╦ ╔╦╗╔═╗╦═╗
# ║╣ ║  ║╣ ║║║║╣ ║║║ ║   ║  ║╣ ╚╗╔╝║╣ ║    ╠╣ ║║  ║ ║╣ ╠╦╝
# ╚═╝╩═╝╚═╝╩ ╩╚═╝╝╚╝ ╩   ╩═╝╚═╝ ╚╝ ╚═╝╩═╝  ╚  ╩╩═╝╩ ╚═╝╩╚═ ElementLevelFilter
#==================================================
# Get Random Level
random_level = FilteredElementCollector(doc)\
                    .OfClass(Level)\
                    .FirstElement()

# Create LevelFilter
lvl_filter   = ElementLevelFilter(random_level.Id)

# Get Rooms on Level
rooms_on_lvl = FilteredElementCollector(doc)\
                    .OfCategory(BuiltInCategory.OST_Rooms)\
                    .WherePasses(lvl_filter)\
                    .ToElements()
# Get Walls on Level
walls_on_lvl = FilteredElementCollector(doc)\
                    .OfCategory(BuiltInCategory.OST_Walls)\
                    .WherePasses(lvl_filter)\
                    .ToElements()

#👀 Print Results
print('There are {} Rooms on Level: {}'.format(len(rooms_on_lvl),
                                               random_level.Name))

print('There are {} Walls on Level: {}'.format(len(walls_on_lvl),
                                               random_level.Name))


# ╔═╗╦  ╔═╗╔╦╗╔═╗╔╗╔╔╦╗  ╦╔╗╔╔╦╗╔═╗╦═╗╔═╗╔═╗╔═╗╔╦╗╔═╗  ╔═╗╔═╗╦  ╦╔╦╗
# ║╣ ║  ║╣ ║║║║╣ ║║║ ║   ║║║║ ║ ║╣ ╠╦╝╚═╗║╣ ║   ║ ╚═╗  ╚═╗║ ║║  ║ ║║
# ╚═╝╩═╝╚═╝╩ ╩╚═╝╝╚╝ ╩   ╩╝╚╝ ╩ ╚═╝╩╚═╚═╝╚═╝╚═╝ ╩ ╚═╝  ╚═╝╚═╝╩═╝╩═╩╝ ElementIntersectsSolidFilter
#==================================================
from Autodesk.Revit.UI.Selection import ObjectType

# 👉 Choose Element
ref = uidoc.Selection.PickObject(ObjectType.Element)
elem = doc.GetElement(ref)

# ✅ Ensure FilledRegion Selected
if type(elem) != FilledRegion:
    import sys

    sys.exit()

# Create Solid Geometry from Region
region = elem
boundaries = region.GetBoundaries()
solid = GeometryCreationUtilities.CreateExtrusionGeometry(boundaries, XYZ(0, 0, 1), 1000)  # 10 - height

# 🔽 Create a ElementIntersectsElementFilter
filter = ElementIntersectsSolidFilter(solid)

# ✅ Get Intersecting Elements
inter_el_ids = FilteredElementCollector(doc) \
    .WhereElementIsNotElementType() \
    .WherePasses(filter) \
    .ToElementIds()

# 👀 Set Revit UI Selection
uidoc.Selection.SetElementIds(inter_el_ids)

#  ╔═╗╔╦╗╦═╗╦ ╦╔═╗╔╦╗╦ ╦╦═╗╔═╗╦    ╦╔╗╔╔═╗╔╦╗╔═╗╔╗╔╔═╗╔═╗  ╦ ╦╔═╗╔═╗╔═╗╔═╗  ╔═╗╦╦ ╔╦╗╔═╗╦═╗
#  ╚═╗ ║ ╠╦╝║ ║║   ║ ║ ║╠╦╝╠═╣║    ║║║║╚═╗ ║ ╠═╣║║║║  ║╣   ║ ║╚═╗╠═╣║ ╦║╣   ╠╣ ║║  ║ ║╣ ╠╦╝
#  ╚═╝ ╩ ╩╚═╚═╝╚═╝ ╩ ╚═╝╩╚═╩ ╩╩═╝  ╩╝╚╝╚═╝ ╩ ╩ ╩╝╚╝╚═╝╚═╝  ╚═╝╚═╝╩ ╩╚═╝╚═╝  ╚  ╩╩═╝╩ ╚═╝╩╚═ StructuralInstanceUsageFilter
#==================================================
from Autodesk.Revit.DB.Structure import StructuralInstanceUsageFilter, StructuralInstanceUsage

#🔽 Create a StructuralInstanceUsageFilter for beams
filter_str_wall = StructuralInstanceUsageFilter(StructuralInstanceUsage.Wall)
filter_str_col  = StructuralInstanceUsageFilter(StructuralInstanceUsage.Column)
filter_str_gir  = StructuralInstanceUsageFilter(StructuralInstanceUsage.Girder)

#✅ Apply the filter to the elements in the active document
elements = FilteredElementCollector(doc).WherePasses(filter_str_gir).ToElements()

#👀 Show Results
count = len(elements)
print("Number of Elements in the document: {}".format(count))


# ╔╗ ╔═╗╦ ╦╔╗╔╔╦╗╦╔╗╔╔═╗  ╔╗ ╔═╗═╗ ╦  ╔═╗╔═╗╔╗╔╔╦╗╔═╗╦╔╗╔╔═╗  ╔═╗╔═╗╦╔╗╔╔╦╗  ╔═╗╦╦ ╔╦╗╔═╗╦═╗
# ╠╩╗║ ║║ ║║║║ ║║║║║║║ ╦  ╠╩╗║ ║╔╩╦╝  ║  ║ ║║║║ ║ ╠═╣║║║║╚═╗  ╠═╝║ ║║║║║ ║   ╠╣ ║║  ║ ║╣ ╠╦╝
# ╚═╝╚═╝╚═╝╝╚╝═╩╝╩╝╚╝╚═╝  ╚═╝╚═╝╩ ╚═  ╚═╝╚═╝╝╚╝ ╩ ╩ ╩╩╝╚╝╚═╝  ╩  ╚═╝╩╝╚╝ ╩   ╚  ╩╩═╝╩ ╚═╝╩╚═ BoundingBoxContainsPointFilter
#==================================================
# Use BoundingBoxContainsPoint filter to find elements with a bounding box that contains the
# given point in the document.

# Create a BoundingBoxContainsPoint filter for base point of (15, 15, 0)
base_pnt = XYZ(15, 15, 0)
filter   = BoundingBoxContainsPointFilter(base_pnt)

# Apply the filter to the elements in the active document
# This filter will excludes all objects derived from View and objects derived from ElementType
collector         = FilteredElementCollector(doc)
contain_elements  = collector.WherePasses(filter).ToElements()
print('BB Contains Point Found:')
for i in contain_elements  :
    print(i)

# Find walls that do not contain the given point: use an inverted filter to match elements
# Use shortcut command of_class() to find walls only
not_contain_filter = BoundingBoxContainsPointFilter(base_pnt, True)  # inverted filter
collector          = FilteredElementCollector(doc)
not_contain_walls  = collector.OfClass(Wall).WherePasses(not_contain_filter).ToElements()
print('Walls with BB Not Contains Found:')
for i in not_contain_walls:
    print(i)

# ╔╗ ╔═╗╦ ╦╔╗╔╔╦╗╦╔╗╔╔═╗  ╔╗ ╔═╗═╗ ╦  ╦╔╗╔╔╦╗╔═╗╦═╗╔═╗╔═╗╔═╗╔╦╗╔═╗  ╔═╗╦╦ ╔╦╗╔═╗╦═╗
# ╠╩╗║ ║║ ║║║║ ║║║║║║║ ╦  ╠╩╗║ ║╔╩╦╝  ║║║║ ║ ║╣ ╠╦╝╚═╗║╣ ║   ║ ╚═╗  ╠╣ ║║  ║ ║╣ ╠╦╝
# ╚═╝╚═╝╚═╝╝╚╝═╩╝╩╝╚╝╚═╝  ╚═╝╚═╝╩ ╚═  ╩╝╚╝ ╩ ╚═╝╩╚═╚═╝╚═╝╚═╝ ╩ ╚═╝  ╚  ╩╩═╝╩ ╚═╝╩╚═
# Use BoundingBoxIntersects filter to find elements with a bounding box that intersects the
# given Outline in the document.

# Create an Outline, uses a minimum and maximum XYZ point to initialize the outline.
my_out_ln = Outline(XYZ(50, 0, 0), XYZ(80, 30, 10))

# Create a BoundingBoxIntersects filter with this Outline
filter = BoundingBoxIntersectsFilter(my_out_ln)

# Apply the filter to the elements in the active document
# This filter excludes all objects derived from View and objects derived from ElementType
collector = FilteredElementCollector(doc, doc.ActiveView.Id)
elements  = collector.WherePasses(filter).ToElements()

#👀 Print Elements
for i in elements:
    print(i)

# Find all walls which don't intersect with BoundingBox: use an inverted filter to match elements
# Use shortcut command of_class() to find walls only
invert_filter       = BoundingBoxIntersectsFilter(my_out_ln, True)  # inverted filter
collector           = FilteredElementCollector(doc)
not_intersect_walls = collector.OfClass(Wall).WherePasses(invert_filter).ToElements()


# ╔═╗╦  ╔═╗╔╦╗╔═╗╔╗╔╔╦╗  ╔╦╗╦ ╦╦ ╔╦╗╦  ╔═╗╔═╗╔╦╗╔═╗╔═╗╔═╗╦═╗╦ ╦  ╔═╗╦╦ ╔╦╗╔═╗╦═╗
# ║╣ ║  ║╣ ║║║║╣ ║║║ ║   ║║║║ ║║  ║ ║  ║  ╠═╣ ║ ║╣ ║ ╦║ ║╠╦╝╚╦╝  ╠╣ ║║  ║ ║╣ ╠╦╝
# ╚═╝╩═╝╚═╝╩ ╩╚═╝╝╚╝ ╩   ╩ ╩╚═╝╩═╝╩ ╩  ╚═╝╩ ╩ ╩ ╚═╝╚═╝╚═╝╩╚═ ╩   ╚  ╩╩═╝╩ ╚═╝╩╚═
# List of categories we want to filter
cats = [
    BuiltInCategory.OST_Walls,
    BuiltInCategory.OST_Floors,
    BuiltInCategory.OST_Roofs,
    BuiltInCategory.OST_Ceilings
]

# Convert into List[BuiltInCategory]
import clr
clr.AddReference('System')
from System.Collections.Generic import List
List_cats = List[BuiltInCategory](cats)

# Create the multi-category filter
multi_cat_filter = ElementMulticategoryFilter(List_cats)

# Collecting elements from specified categories
elements = FilteredElementCollector(doc).WherePasses(multi_cat_filter).ToElements()

# ╔═╗╦  ╔═╗╔╦╗╔═╗╔╗╔╔╦╗  ╔╦╗╦ ╦╦ ╔╦╗╦  ╔═╗╦  ╔═╗╔═╗╔═╗  ╔═╗╦╦ ╔╦╗╔═╗╦═╗
# ║╣ ║  ║╣ ║║║║╣ ║║║ ║   ║║║║ ║║  ║ ║  ║  ║  ╠═╣╚═╗╚═╗  ╠╣ ║║  ║ ║╣ ╠╦╝
# ╚═╝╩═╝╚═╝╩ ╩╚═╝╝╚╝ ╩   ╩ ╩╚═╝╩═╝╩ ╩  ╚═╝╩═╝╩ ╩╚═╝╚═╝  ╚  ╩╩═╝╩ ╚═╝╩╚═
#⬇️ Import .NET System Classes
import clr
clr.AddReference('System')
from System.Collections.Generic import List
from System import Type

#📦 List of Types we want to Filter
types = [Wall, Floor, RoofBase, Ceiling]

#🔁 Convert into List[Type]
List_types = List[Type]()
for i in types:
    List_types.Add(i)

#🔎 Create Filter
multi_class_filter = ElementMulticlassFilter(List_types)

#👉 Get Elements
elements = FilteredElementCollector(doc, doc.ActiveView.Id).WherePasses(multi_class_filter).ToElements()

#👀 Print Elements
for el in elements:
    print(el)

# ╔═╗╦  ╔═╗╔╦╗╔═╗╔╗╔╔╦╗  ╦ ╦╔═╗╦═╗╦╔═╔═╗╔═╗╔╦╗  ╔═╗╦╦ ╔╦╗╔═╗╦═╗
# ║╣ ║  ║╣ ║║║║╣ ║║║ ║   ║║║║ ║╠╦╝╠╩╗╚═╗║╣  ║   ╠╣ ║║  ║ ║╣ ╠╦╝
# ╚═╝╩═╝╚═╝╩ ╩╚═╝╝╚╝ ╩   ╚╩╝╚═╝╩╚═╩ ╩╚═╝╚═╝ ╩   ╚  ╩╩═╝╩ ╚═╝╩╚═
worksets = FilteredWorksetCollector(doc) \
    .OfKind(WorksetKind.UserWorkset)

for workset in worksets:
    workset_filter = ElementWorksetFilter(workset.Id)

    # Collect elements in the specific workset
    elements_in_workset = FilteredElementCollector(doc) \
        .WherePasses(workset_filter) \
        .ToElements()

    print('Workset: {} has {} Elements'.format(workset.Name,
                                               len(elements_in_workset)))


# ╔═╗╦  ╔═╗╔╦╗╔═╗╔╗╔╔╦╗  ╔═╗╔═╗╦═╗╔═╗╔╦╗╔═╗╔╦╗╔═╗╦═╗  ╔═╗╦╦ ╔╦╗╔═╗╦═╗
# ║╣ ║  ║╣ ║║║║╣ ║║║ ║   ╠═╝╠═╣╠╦╝╠═╣║║║║╣  ║ ║╣ ╠╦╝  ╠╣ ║║  ║ ║╣ ╠╦╝
# ╚═╝╩═╝╚═╝╩ ╩╚═╝╝╚╝ ╩   ╩  ╩ ╩╩╚═╩ ╩╩ ╩╚═╝ ╩ ╚═╝╩╚═  ╚  ╩╩═╝╩ ╚═╝╩╚═
#==================================================
type_name = '2000 x 2250'

#1️⃣ Parameter
p_type_id = ElementId(BuiltInParameter.SYMBOL_NAME_PARAM)
f_param  = ParameterValueProvider(p_type_id)

#2️⃣ Evaluator
evaluator = FilterStringEquals()

#3️⃣ Value
value = type_name

#4️⃣ Rule
rvt_year = int(app.VersionNumber)
if rvt_year >= 2023:
    f_rule = FilterStringRule(f_param, evaluator, value)
else:
    f_rule = FilterStringRule(f_param, evaluator, value, False)


#5️⃣ Filter
filter_fam_name = ElementParameterFilter(f_rule)

#6️⃣ Apply Filter to FEC
elements = FilteredElementCollector(doc)\
                .WherePasses(filter_fam_name)\
                .WhereElementIsNotElementType()\
                .ToElements()

# 🎯 Set Selection in Revit UI
el_ids      = [el.Id for el in elements]
List_el_ids = List[ElementId](el_ids)

uidoc.Selection.SetElementIds(List_el_ids)


# ╦ ╦╔═╗╔═╗╔═╗╦ ╦  ╔═╗╔═╗╔╦╗╦╔╗╔╔═╗  ||
# ╠═╣╠═╣╠═╝╠═╝╚╦╝  ║  ║ ║ ║║║║║║║ ╦  ||
# ╩ ╩╩ ╩╩  ╩   ╩   ╚═╝╚═╝═╩╝╩╝╚╝╚═╝  .. ⌨️ HAPPY CODING!

# Find More Snippets Here:              - www.LearnRevitAPI.com/python-snippets
# E-Book: Beginner's Guide to Revit API - www.LearnRevitAPI.com/ebook
# E-Book: Master Getting Elements (FEC) - www.LearnRevitAPI.com/ebook/fec

