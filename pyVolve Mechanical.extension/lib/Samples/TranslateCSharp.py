# -*- coding: utf-8 -*-
__title__   = "Samples - C# to Python"
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


# ╔╦╗╦═╗╔═╗╔╗╔╔═╗╦  ╔═╗╔╦╗╔═╗  ╔═╗ ╔═╗╦ ╦╔═╗╦═╗╔═╗  ╔╦╗╔═╗  ╔═╗╦ ╦╔╦╗╦ ╦╔═╗╔╗╔
#  ║ ╠╦╝╠═╣║║║╚═╗║  ╠═╣ ║ ║╣   ║───╚═╗╠═╣╠═╣╠╦╝╠═╝   ║ ║ ║  ╠═╝╚╦╝ ║ ╠═╣║ ║║║║
#  ╩ ╩╚═╩ ╩╝╚╝╚═╝╩═╝╩ ╩ ╩ ╚═╝  ╚═╝ ╚═╝╩ ╩╩ ╩╩╚═╩     ╩ ╚═╝  ╩   ╩  ╩ ╩ ╩╚═╝╝╚╝ TRANSLATE C-SHARP TO PYTHON
#====================================================================================================
#P.S. In C-Sharp double slashed // is used for comments instead of # 😉

#--------------------------------------------------
#🟠 Variables C# vs Python
# Python automatically knows the DataType and can change it.
c_sharp_sample = """
// Defined Data Type
int myNum = 50;

// Non-Defined Data Type
var myNum = 50;
"""

#🐍 Python
my_num = 50

#--------------------------------------------------
#🟠 FEC Sample

c_sharp_sample = """
FilteredElementCollector collector = new FilteredElementCollector(doc);
""" # The first FEC is used for type hinting, it identifies that collector has to have this Type. Also new is used when constructors are used.

collector = FilteredElementCollector(doc)

#--------------------------------------------------
#🟠 If Statements

c_sharp_sample="""
int myNumber = 5;

if (myNumber > 10)
{
    Console.WriteLine("Number is more than 10");
}
else if (myNumber == 5)
{
    Console.WriteLine("Number is 5");
}
else
{
    Console.WriteLine("Number is less than 5");
}"""

#🐍 Python
my_num = 5

if my_num > 10:
    print("Number is more than 5")
elif my_num == 5:
    print("Number is 5")
else:
    print("Number is less than 5")

#--------------------------------------------------
#🟠 Loops
c_sharp_sample = """
// for Loop
for (int i = 0; i < 10; i++)
{
    Console.WriteLine(i);
}

// while Loop
int count = 5;
while (count > 0) {
    Console.WriteLine(count);
    count--;
}"""

#🐍 Python
# for Loop
for i in range(10):
    print(i)

# while Loop
count = 5
while count > 0:
    print(count)
    count -= 1

#--------------------------------------------------
#🟠 Functions without Returned Value

c_sharp_sample = """
void MyFunction()
{
    Console.WriteLine('Simple Function')
}"""

#🐍 Python
def my_function():
    print('Simple Function')

# --------------------------------------------------
# 🟠 Functions With Arguments, without Returned Value

c_sharp_sample = """
def my_function(view, x):
# type: (View, int) -> View
    print("View Name: {}".format(view.Name))
    return view"""

#🐍 Python
def my_function(view, x):
# type: (View, int) -> View
    print("View Name: {}".format(view.Name))
    return view

#💡 Type Hinting is optional in python.



#--------------------------------------------------
#🟠 Translate 1 - Create Wall Using Curve

c_sharp_1 = """
public Wall CreateWallUsingCurve1(Autodesk.Revit.DB.Document document, Level level)
{
    // Build a location line for the wall creation
    XYZ start = new XYZ(0, 0, 0);
    XYZ end = new XYZ(10, 10, 0);
    Line geomLine = Line.CreateBound(start, end);

    // Create a wall using the location line
    return Wall.Create(document, geomLine, level.Id, true);
}"""

#🐍 Python
def CreateWallUsingCurve1(document, level):
    # type: (Document, Level) -> Wall
    """Function to create a sample wall."""
    # Build a location line for the wall creation
    start =  XYZ(0, 0, 0)
    end   =  XYZ(10, 10, 0)
    geomLine = Line.CreateBound(start, end)

    # Create a wall using the location line
    return Wall.Create(document, geomLine, level.Id, False)

# How-To Use?
level = doc.ActiveView.GenLevel # Only works in ViewPlan (Floor, Ceiling, Area, Structural Plans)
with Transaction(doc, 'Create a Wall') as t:
    t.Start()
    new_wall = CreateWallUsingCurve1(doc, level)
    t.Commit()



#--------------------------------------------------
#🟠 Translate 2 - Create Wall Using Curve
c_sharp_2 = """
Ceiling CreateCeilingAtElevation(Document document, Level level, double elevation)
{
   XYZ first = new XYZ(0, 0, 0);
   XYZ second = new XYZ(20, 0, 0);
   XYZ third = new XYZ(20, 15, 0);
   XYZ fourth = new XYZ(0, 15, 0);
   CurveLoop profile = new CurveLoop();
   profile.Append(Line.CreateBound(first, second));
   profile.Append(Line.CreateBound(second, third));
   profile.Append(Line.CreateBound(third, fourth));
   profile.Append(Line.CreateBound(fourth, first));

   var ceiling = Ceiling.Create(document, new List<CurveLoop> { profile }, ElementId.InvalidElementId, level.Id);
   Parameter param = ceiling.get_Parameter(BuiltInParameter.CEILING_HEIGHTABOVELEVEL_PARAM);
   param.Set(elevation);

   return ceiling;
}"""

#🐍 Python
def CreateCeilingAtElevation(doc, level, elevation):
    # type: (Document, Level, float) -> Ceiling
    """Function to create a sample Ceiling"""
    first   = XYZ(0, 0, 0)
    second  = XYZ(20, 0, 0)
    third   = XYZ(20, 15, 0)
    fourth  = XYZ(0, 15, 0)

    profile = CurveLoop()
    profile.Append(Line.CreateBound(first, second))
    profile.Append(Line.CreateBound(second, third))
    profile.Append(Line.CreateBound(third, fourth))
    profile.Append(Line.CreateBound(fourth, first))

    list_curve_loops = List[CurveLoop]()
    list_curve_loops.Add(profile)

    ceil_type_id = doc.GetDefaultElementTypeId(ElementTypeGroup.CeilingType)
    ceiling = Ceiling.Create(doc,
                           list_curve_loops,
                           ceil_type_id,
                           level.Id)

    param = ceiling.get_Parameter(BuiltInParameter.CEILING_HEIGHTABOVELEVEL_PARAM)
    param.Set(elevation)

    return ceiling

# How-To Use?
level = doc.ActiveView.GenLevel # Only works in ViewPlan (Floor, Ceiling, Area, Structural Plans)
with Transaction(doc, 'Create a Ceiling') as t:
    t.Start()
    new_ceil = CreateCeilingAtElevation(doc, level, 10)
    t.Commit()

#--------------------------------------------------
#🟠 Translate 3 - Create Wall Using Curve

c_sharp_3 = """
public void ElementOverride()
{
    Document doc = this.ActiveUIDocument.Document;
    UIDocument uidoc = this.ActiveUIDocument;
    ElementId id = uidoc.Selection.PickObject(ObjectType.Element,"Select an element").ElementId;
    OverrideGraphicSettings ogs = new OverrideGraphicSettings();
    ogs.SetProjectionLineColor(new Color(0,255,0));
    using (Transaction t = new Transaction(doc,"Set Element Override"))
    {
        t.Start();
        doc.ActiveView.SetElementOverrides(id, ogs);
        t.Commit();
    }
}"""



#🐍 Python
from Autodesk.Revit.UI.Selection import ObjectType

def ElementOverride():
    # Select Element
    doc   = __revit__.ActiveUIDocument.Document  # type:Document
    uidoc = __revit__.ActiveUIDocument
    id    = uidoc.Selection.PickObject(ObjectType.Element,"Select an element").ElementId

    # Graphic Settings
    ogs = OverrideGraphicSettings()
    ogs.SetProjectionLineColor( Color(255,0,50))

    # Change Color
    with Transaction(doc,"Set Element Override") as t:
        t.Start()
        doc.ActiveView.SetElementOverrides(id, ogs)
        t.Commit()

ElementOverride()

# ╦ ╦╔═╗╔═╗╔═╗╦ ╦  ╔═╗╔═╗╔╦╗╦╔╗╔╔═╗  ||
# ╠═╣╠═╣╠═╝╠═╝╚╦╝  ║  ║ ║ ║║║║║║║ ╦  ||
# ╩ ╩╩ ╩╩  ╩   ╩   ╚═╝╚═╝═╩╝╩╝╚╝╚═╝  .. ⌨️ HAPPY CODING!

# Find More Snippets Here:              - www.LearnRevitAPI.com/python-snippets
# E-Book: Beginner's Guide to Revit API - www.LearnRevitAPI.com/ebook
# E-Book: Master Getting Elements (FEC) - www.LearnRevitAPI.com/ebook/fec


