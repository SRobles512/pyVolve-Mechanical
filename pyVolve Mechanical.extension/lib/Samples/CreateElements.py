# -*- coding: utf-8 -*-
__title__   = "Samples - Create Elements"
__doc__     = """Version = 1.0
Date    = 15.06.2024
________________________________________________________________
Description:

Link to a reusable FEC Samples library for 
FilteredElementCollector Class.

________________________________________________________________
How-To:

1. Click on the button to open the FEC Samples file 
in your default IDE (code editor)

2. Master Getting Your Elements!

________________________________________________________________
Author: Erik Frits"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#====================================================================================================
from Autodesk.Revit.DB import *

#.NET Imports
import clr
clr.AddReference('System')
from System.Collections.Generic import List


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
#====================================================================================================
app    = __revit__.Application
uidoc  = __revit__.ActiveUIDocument
doc    = __revit__.ActiveUIDocument.Document #type:Document
active_view  = doc.ActiveView
active_level = doc.ActiveView.GenLevel

# ╔═╗╦═╗╔═╗╔═╗╔╦╗╔═╗  ╦ ╦╔═╗╦  ╦
# ║  ╠╦╝║╣ ╠═╣ ║ ║╣   ║║║╠═╣║  ║
# ╚═╝╩╚═╚═╝╩ ╩ ╩ ╚═╝  ╚╩╝╩ ╩╩═╝╩═╝
#====================================================================================================

# ARGUMENTS
pt_start = XYZ(30,0,0)
pt_end   = XYZ(30,5,0)
curve    = Line.CreateBound(pt_start, pt_end)

# CREATE A WALL
wall = Wall.Create(doc, curve, active_level.Id, False)


# ╔═╗╦═╗╔═╗╔═╗╔╦╗╔═╗  ╦  ╦╔╗╔╔═╗
# ║  ╠╦╝║╣ ╠═╣ ║ ║╣   ║  ║║║║║╣
# ╚═╝╩╚═╚═╝╩ ╩ ╩ ╚═╝  ╩═╝╩╝╚╝╚═╝
#====================================================================================================
#ARGUMENTS
pt_start = XYZ(20,0,0)
pt_end   = XYZ(20,5,0)
curve    = Line.CreateBound(pt_start, pt_end)

#CREATE DETAIL LINE
detail_line = doc.Create.NewDetailCurve(active_view, curve)


# ╔═╗╦═╗╔═╗╔═╗╔╦╗╔═╗  ╦═╗╔═╗╔═╗╔╦╗
# ║  ╠╦╝║╣ ╠═╣ ║ ║╣   ╠╦╝║ ║║ ║║║║
# ╚═╝╩╚═╚═╝╩ ╩ ╩ ╚═╝  ╩╚═╚═╝╚═╝╩ ╩
#====================================================================================================
# ARGUMENTS
pt = UV(10,0)

# CREATE ROOM
room = doc.Create.NewRoom(active_level, pt)

# CREATE ROOM TAG
room_link = LinkElementId(room.Id)
doc.Create.NewRoomTag(room_link, pt, active_view.Id )

# ╔═╗╦═╗╔═╗╔═╗╔╦╗╔═╗  ╔╦╗╔═╗═╗ ╦╔╦╗
# ║  ╠╦╝║╣ ╠═╣ ║ ║╣    ║ ║╣ ╔╩╦╝ ║
# ╚═╝╩╚═╚═╝╩ ╩ ╩ ╚═╝   ╩ ╚═╝╩ ╚═ ╩
#====================================================================================================
# ARGUMENTS
text_type_id = FilteredElementCollector(doc).OfClass(TextNoteType).FirstElementId()
pt           = XYZ(0,0,0)
text         = 'Hello BIM World!'

# CREATE TEXT NOTE
TextNote.Create(doc, active_view.Id, pt, text, text_type_id)

# ╔═╗╦═╗╔═╗╔═╗╔╦╗╔═╗  ╔╗ ╔═╗╔═╗╔╦╗
# ║  ╠╦╝║╣ ╠═╣ ║ ║╣   ╠╩╗║╣ ╠═╣║║║
# ╚═╝╩╚═╚═╝╩ ╩ ╩ ╚═╝  ╚═╝╚═╝╩ ╩╩ ╩
#====================================================================================================
# Create Line
pt_start = XYZ(0,0,0)
pt_end   = XYZ(20,0,0)
line = Line.CreateBound(pt_start, pt_end)

# Get Default Beam Type
beam_type_id   = doc.GetDefaultFamilyTypeId(ElementId(BuiltInCategory.OST_StructuralFraming))
beam_type      = doc.GetElement(beam_type_id)


# Create Beam
t = Transaction(doc,'Create Beam')
t.Start()

beam = doc.Create.NewFamilyInstance(line, beam_type, active_level, StructuralType.Beam)


t.Commit()

print('Created Beam: {}'.format(beam.Id))

# ╔═╗╦═╗╔═╗╔═╗╔╦╗╔═╗  ╔═╗╦╦  ╦  ╔═╗╔╦╗  ╦═╗╔═╗╔═╗╦╔═╗╔╗╔
# ║  ╠╦╝║╣ ╠═╣ ║ ║╣   ╠╣ ║║  ║  ║╣  ║║  ╠╦╝║╣ ║ ╦║║ ║║║║
# ╚═╝╩╚═╚═╝╩ ╩ ╩ ╚═╝  ╚  ╩╩═╝╩═╝╚═╝═╩╝  ╩╚═╚═╝╚═╝╩╚═╝╝╚╝
#====================================================================================================
# ARGUMENTS
region_type_id = doc.GetDefaultElementTypeId(ElementTypeGroup.FilledRegionType)

# POINTS
pt_0 = XYZ(50, 0, 0)
pt_1 = XYZ(55, 0, 0)
pt_2 = XYZ(55, 5, 0)
pt_3 = XYZ(50, 5, 0)

# LINES
l_0 = Line.CreateBound(pt_0, pt_1)
l_1 = Line.CreateBound(pt_1, pt_2)
l_2 = Line.CreateBound(pt_2, pt_3)
l_3 = Line.CreateBound(pt_3, pt_0)

# BOUNDARY
boundary = CurveLoop()
boundary.Append(l_0)
boundary.Append(l_1)
boundary.Append(l_2)
boundary.Append(l_3)

# LIST OF BOUNDARIES
list_boundaries = List[CurveLoop]()
list_boundaries.Add(boundary)

# CREATE FILLED REGION
region = FilledRegion.Create(doc, region_type_id, active_view.Id, list_boundaries)

# ╔═╗╔═╗╔═╗╦ ╦  ╦ ╦╦╔╦╗╦ ╦  ╦  ╦╔═╗╔═╗╔╦╗╔═╗╦═╗
# ║  ║ ║╠═╝╚╦╝  ║║║║ ║ ╠═╣  ╚╗╔╝║╣ ║   ║ ║ ║╠╦╝
# ╚═╝╚═╝╩   ╩   ╚╩╝╩ ╩ ╩ ╩   ╚╝ ╚═╝╚═╝ ╩ ╚═╝╩╚═ COPY WITH VECTOR
#====================================================================================================
# 👉 Get Walls
wallsToCopy = FilteredElementCollector(doc)\
    .OfCategory(BuiltInCategory.OST_Walls)\
    .WhereElementIsNotElementType()\
    .ToElementIds()

#📐 Vector
vector = XYZ(50, 50, 0)

#🔓 Start Transaction
t = Transaction(doc, __title__)
t.Start()

#✅ Copy Elements
ElementTransformUtils.CopyElements(doc, wallsToCopy, vector)

#🔒 End Transaction
t.Commit()


# ╔═╗╔═╗╔═╗╦ ╦  ╔╗ ╔═╗╔╦╗╦ ╦╔═╗╔═╗╔╗╔  ╦  ╦╦╔═╗╦ ╦╔═╗
# ║  ║ ║╠═╝╚╦╝  ╠╩╗║╣  ║ ║║║║╣ ║╣ ║║║  ╚╗╔╝║║╣ ║║║╚═╗
# ╚═╝╚═╝╩   ╩   ╚═╝╚═╝ ╩ ╚╩╝╚═╝╚═╝╝╚╝   ╚╝ ╩╚═╝╚╩╝╚═╝ COPY BETWEEN VIEWS
#=======================================================================================

#👉 Get TextNotes
textToCopy = FilteredElementCollector(doc, doc.ActiveView.Id)\
    .OfCategory(BuiltInCategory.OST_TextNotes)\
    .WhereElementIsNotElementType()\
    .ToElementIds()

#👁️ ️Get Views
src_view = doc.ActiveView
dest_view = select_views(__title__,multiple=False)

#⚙ Transform & Options
transform = Transform.Identity
opts      = CopyPasteOptions()

#🔓 Start Transaction
t = Transaction(doc, __title__)
t.Start()

#✅ Copy Elements
ElementTransformUtils.CopyElements(src_view, textToCopy, dest_view, transform, opts)

#🔒 End Transaction
t.Commit()


# ╔═╗╔═╗╔═╗╦ ╦  ╔╗ ╔═╗╔╦╗╦ ╦╔═╗╔═╗╔╗╔  ╔═╗╦═╗╔═╗ ╦╔═╗╔═╗╔╦╗╔═╗
# ║  ║ ║╠═╝╚╦╝  ╠╩╗║╣  ║ ║║║║╣ ║╣ ║║║  ╠═╝╠╦╝║ ║ ║║╣ ║   ║ ╚═╗
# ╚═╝╚═╝╩   ╩   ╚═╝╚═╝ ╩ ╚╩╝╚═╝╚═╝╝╚╝  ╩  ╩╚═╚═╝╚╝╚═╝╚═╝ ╩ ╚═╝ COPY BETWEEN PROJECTS
#=======================================================================================
# 👉 Get Walls
wallsToCopy = FilteredElementCollector(doc)\
    .OfCategory(BuiltInCategory.OST_Walls)\
    .WhereElementIsNotElementType()\
    .ToElementIds()


#🏠 Get all Docs
all_docs = list(app.Documents)
doc_A = all_docs[0]
doc_B = all_docs[1]


#⚙ Transform & Options
transform = Transform.Identity
opts      = CopyPasteOptions()

#🔓 Start Transaction
t = Transaction(doc_B, __title__)
t.Start()

#✅ Copy Elements
ElementTransformUtils.CopyElements(doc_A, wallsToCopy, doc_B, transform, opts)

#🔒 End Transaction
t.Commit()

#====================================================================================================
# ╦ ╦╔═╗╔═╗╔═╗╦ ╦  ╔═╗╔═╗╔╦╗╦╔╗╔╔═╗  ||
# ╠═╣╠═╣╠═╝╠═╝╚╦╝  ║  ║ ║ ║║║║║║║ ╦  ||
# ╩ ╩╩ ╩╩  ╩   ╩   ╚═╝╚═╝═╩╝╩╝╚╝╚═╝  .. ⌨️ HAPPY CODING!

# Find More Snippets Here:              - www.LearnRevitAPI.com/python-snippets
# E-Book: Beginner's Guide to Revit API - www.LearnRevitAPI.com/ebook
# E-Book: Master Getting Elements (FEC) - www.LearnRevitAPI.com/ebook/fec
