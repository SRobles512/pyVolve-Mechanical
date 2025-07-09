# -*- coding: utf-8 -*-
#  ______   ____     _____  _ __     _______   __  __ _____ ____ _   _    _    _   _ ___ ____    _    _
# |  _ \ \ / /\ \   / / _ \| |\ \   / / ____| |  \/  | ____/ ___| | | |  / \  | \ | |_ _/ ___|  / \  | |
# | |_) \ V /  \ \ / / | | | | \ \ / /|  _|   | |\/| |  _|| |   | |_| | / _ \ |  \| || | |     / _ \ | |
# |  __/ | |    \ V /| |_| | |__\ V / | |___  | |  | | |__| |___|  _  |/ ___ \| |\  || | |___ / ___ \| |___
# |_|    |_|     \_/  \___/|_____\_/  |_____| |_|  |_|_____\____|_| |_/_/   \_\_| \_|___\____/_/   \_\_____|
#

__title__   = "Align BOI / Spread by Gap"
__doc__     = """Version = 1.0
Date    = 01.24.2025
 --------------------------------------------------------------------------
 Description:
 1) 'Align BOP/BOI': Prompts user to select a reference fabrication part,
    then select additional parts to update their BOP/BOI to match.

 2) 'Spread by Gap': Automatically adjusts the center-to-center measurement
    of pipes to achieve a user-specified gap.

 The script will prompt you to choose which operation you want to run.
 --------------------------------------------------------------------------
 Author: Sam Robles
 """
__author__ = "Sam Robles"
__helpurl__ = "https://github.com/SRobles512/pyVolve-Mechanical/wiki"
__min_revit_ver__ = 2022
__max_revit_ver__ = 2024


# ___ __  __ ____   ___  ____ _____ ____  
#|_ _|  \/  |  _ \ / _ \|  _ \_   _/ ___| 
# | || |\/| | |_) | | | | |_) || | \___ \ 
# | || |  | |  __/| |_| |  _ < | |  ___) |
#|___|_|  |_|_|    \___/|_| \_\|_| |____/
#=========================================
import clr
import math
import System

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Fabrication import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import ObjectType
from System.Collections.Generic import List

# pyRevit imports
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms

# For the gap input UI
clr.AddReference("System.Windows.Forms")
import System.Windows.Forms as WinForms
from System.Windows.Forms import MessageBox

#   ____ _     ___  ____    _    _      __     ___    ____  ___    _    ____  _     _____ ____  
#  / ___| |   / _ \| __ )  / \  | |     \ \   / / \  |  _ \|_ _|  / \  | __ )| |   | ____/ ___| 
# | |  _| |  | | | |  _ \ / _ \ | |      \ \ / / _ \ | |_) || |  / _ \ |  _ \| |   |  _| \___ \ 
# | |_| | |__| |_| | |_) / ___ \| |___    \ V / ___ \|  _ < | | / ___ \| |_) | |___| |___ ___) |
#  \____|_____\___/|____/_/   \_\_____|    \_/_/   \_\_| \_\___/_/   \_\____/|_____|_____|____/ 

doc  = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument


#  _____ _   _ _   _  ____ _____ ___ ___  _   _ ____  
# |  ___| | | | \ | |/ ___|_   _|_ _/ _ \| \ | / ___| 
# | |_  | | | |  \| | |     | |  | | | | |  \| \___ \ 
# |  _| | |_| | |\  | |___  | |  | | |_| | |\  |___) |
# |_|    \___/|_| \_|\____| |_| |___\___/|_| \_|____/                                                     
# ====================================================

def get_fabrication_bop_param_value(element):
    """
    Retrieve the 'FABRICATION_BOTTOM_OF_PART' parameter value in feet (float).
    Returns None if not valid or not found.
    """
    if not element:
        return None
    
    # Named parameter:
    param = element.LookupParameter("FABRICATION_BOTTOM_OF_PART")
    if not (param and not param.IsReadOnly and param.StorageType == StorageType.Double):
        # Built-in
        bip_param = element.get_Parameter(BuiltInParameter.FABRICATION_BOTTOM_OF_PART)
        if bip_param and not bip_param.IsReadOnly and bip_param.StorageType == StorageType.Double:
            param = bip_param
        else:
            param = None
    
    if param:
        return param.AsDouble()
    return None


#  _____ _   _ _   _  ____ _____ ___ ___  _   _ ____  
# |  ___| | | | \ | |/ ___|_   _|_ _/ _ \| \ | / ___| 
# | |_  | | | |  \| | |     | |  | | | | |  \| \___ \ 
# |  _| | |_| | |\  | |___  | |  | | |_| | |\  |___) |
# |_|    \___/|_| \_|\____| |_| |___\___/|_| \_|____/                                                     
# ====================================================

def parse_fractional_inches_to_feet(input_str):
    """
    Converts fractional inch strings like '1 1/2' or '3/4' into feet (float).
    """
    s = input_str.strip().replace('"', '')
    if not s:
        return 0.0
    parts = s.split()
    total_inches = 0.0
    try:
        if len(parts) == 1:
            # e.g. "3/4" or just "2"
            if '/' in parts[0]:
                num, denom = parts[0].split('/')
                total_inches = float(num) / float(denom)
            else:
                total_inches = float(parts[0])
        else:
            # e.g. "1 1/2"
            whole = float(parts[0])
            frac  = parts[1]
            if '/' in frac:
                num, denom = frac.split('/')
                frac_val = float(num) / float(denom)
            else:
                frac_val = float(frac)
            total_inches = whole + frac_val
    except:
        total_inches = 0.0
    # convert inches -> feet
    return total_inches / 12.0


def get_location_curve_data(element):
    """
    Returns (start_x, start_y) and (end_x, end_y) in feet as floats, if it's a LocationCurve.
    """
    loc = element.Location
    if not loc or not hasattr(loc, "Curve"):
        return None
    
    curve = loc.Curve
    if not curve:
        return None
    
    start = curve.GetEndPoint(0)
    end   = curve.GetEndPoint(1)
    return (start.X, start.Y), (end.X, end.Y)


def get_fabrication_half_od(element):
    """
    half_od = (OutsideDiameter/2 + InsulationThickness) in feet.
    """
    if not isinstance(element, FabricationPart):
        return 0.0
    
    # Outside Diameter param
    od_param = element.LookupParameter("Outside Diameter")
    od_val = od_param.AsDouble() if od_param else 0.0
    
    # Insulation Thickness
    ins_thk = element.InsulationThickness  # also in feet
    return (od_val / 2.0) + ins_thk


def calculate_gap_between(pipeA, pipeB):
    """
    For XY:
    - Get center-to-center distance (based on start points).
    - Subtract both half ODs => gap in feet.
    - Also return the 'axis' to help figure out direction for movement.
      axis can be ("x", dist) or ("y", dist) or (dx, dy).
    """
    dataA = get_location_curve_data(pipeA)
    dataB = get_location_curve_data(pipeB)
    if not dataA or not dataB:
        return None, 0.0

    (ax, ay), _ = dataA
    (bx, by), _ = dataB
    dx = bx - ax
    dy = by - ay

    # If both dx & dy are non-negligible, it's diagonal
    if abs(dx) > 1e-6 and abs(dy) > 1e-6:
        c2c = math.sqrt(dx*dx + dy*dy)
        axis = (dx, dy)
    elif abs(dx) > 1e-6:
        c2c = abs(dx)
        axis = ("x", dx)
    else:
        c2c = abs(dy)
        axis = ("y", dy)

    halfA = get_fabrication_half_od(pipeA)
    halfB = get_fabrication_half_od(pipeB)
    gap = c2c - (halfA + halfB)
    return axis, gap


def build_xy_translation(axis, distance_to_move):
    """
    Given 'axis' from calculate_gap_between() and the additional distance_to_move,
    return an XYZ vector for XY plane.
    """
    if axis is None:
        return XYZ(0, 0, 0)

    if isinstance(axis, tuple):
        # axis can be ("x", dist) or ("y", dist) or (dx, dy)
        if isinstance(axis[0], str):
            # e.g. ("x", dx_val) => purely horizontal
            direction_str, axis_val = axis
            if direction_str.lower() == 'x':
                # If axis_val >= 0, move +distance, else -distance
                return XYZ(distance_to_move if axis_val >= 0 else -distance_to_move, 0, 0)
            else:
                return XYZ(0, distance_to_move if axis_val >= 0 else -distance_to_move, 0)
        else:
            # (dx, dy)
            dx, dy = axis
            length_2d = math.sqrt(dx*dx + dy*dy)
            if length_2d > 1e-9:
                scale = distance_to_move / length_2d
                return XYZ(dx * scale, dy * scale, 0)
            else:
                return XYZ(0, 0, 0)
    else:
        # Just in case
        return XYZ(0, 0, 0)


def move_fabrication_part(part, translation_vec):
    """
    Applies the move to the FabricationPart's location curve if valid.
    """
    loc = part.Location
    if isinstance(loc, LocationCurve):
        loc.Move(translation_vec)
        return True
    return False

#  __  __    _    ___ _   _ 
# |  \/  |  / \  |_ _| \ | |
# | |\/| | / _ \  | ||  \| |
# | |  | |/ ___ \ | || |\  |
# |_|  |_/_/   \_\___|_| \_|
#===========================

def spread_and_align_bop():
    """
    1) Prompt user for gap in fractional inches -> convert to feet
    2) Prompt reference pipe (for XY chain & for reference BOP)
    3) Prompt multiple pipes in order
    4) For each pipe:
       - Compute needed XY move to get desired gap from the *previous pipe* (chaining).
       - Compute Z difference from the reference’s BOP so they line up in Z.
       - Move the pipe by that combined XYZ vector.
    """
    # (A) Ask user for gap
    class GapForm(WinForms.Form):
        def __init__(self):
            super(GapForm, self).__init__()
            self.Text = "Enter Desired Gap (fractional inches)"
            self.Width = 300
            self.Height = 150

            self.label = WinForms.Label()
            self.label.Text = 'e.g., "1 1/2" or "3/4"'
            self.label.Left = 10
            self.label.Top = 20
            self.label.Width = 280

            self.txtGap = WinForms.TextBox()
            self.txtGap.Left = 10
            self.txtGap.Top = 50
            self.txtGap.Width = 260

            self.btnOk = WinForms.Button()
            self.btnOk.Text = "OK"
            self.btnOk.Left = 100
            self.btnOk.Top = 80
            self.btnOk.DialogResult = WinForms.DialogResult.OK

            self.Controls.Add(self.label)
            self.Controls.Add(self.txtGap)
            self.Controls.Add(self.btnOk)
            self.AcceptButton = self.btnOk

    form = GapForm()
    if form.ShowDialog() != WinForms.DialogResult.OK:
        MessageBox.Show("Cancelled by user.")
        return

    gap_in_str = form.txtGap.Text
    desired_gap_feet = parse_fractional_inches_to_feet(gap_in_str)
    if desired_gap_feet <= 0:
        MessageBox.Show("Invalid gap. Exiting.")
        return

    # (B) Select REFERENCE pipe (for both XY chain start & Z reference)
    MessageBox.Show("Select the reference pipe. ESC to cancel.", "Reference Pipe")
    try:
        ref_pick = uidoc.Selection.PickObject(ObjectType.Element)
        ref_pipe = doc.GetElement(ref_pick.ElementId)
    except:
        MessageBox.Show("No reference pipe selected. Exiting.")
        return

    ref_bop = get_fabrication_bop_param_value(ref_pipe)
    if ref_bop is None:
        MessageBox.Show("Couldn't read BOP from reference pipe. Exiting.")
        return

    # (C) Prompt user to pick multiple pipes in order
    MessageBox.Show("Select pipes to move in order (nearest to farthest). ESC when done.", "Select Pipes")
    from collections import OrderedDict
    ordered_selection = OrderedDict()
    try:
        i = 0
        while True:
            pick = uidoc.Selection.PickObject(ObjectType.Element)
            ordered_selection[i] = doc.GetElement(pick.ElementId)
            i += 1
    except:
        pass

    pipes_to_move = list(ordered_selection.values())
    if not pipes_to_move:
        MessageBox.Show("No pipes selected to move. Exiting.")
        return

    # (D) Move them in XY to get spacing from the previous pipe,
    #     and also move them in Z to match reference pipe's BOP.
    moved_count = 0
    with revit.Transaction("Spread + Align BOP"):
        # We'll keep the "current_reference_for_XY" as the last pipe we moved,
        # so each subsequent pipe is spaced from the last. Initially it's the ref pipe.
        refXY = ref_pipe
        for p in pipes_to_move:
            # (1) Calculate XY offset
            axis, existing_gap = calculate_gap_between(refXY, p)
            delta_gap = desired_gap_feet - existing_gap
            xy_vec = build_xy_translation(axis, delta_gap)

            # (2) Calculate Z offset to match reference's BOP
            pipe_bop = get_fabrication_bop_param_value(p)
            if pipe_bop is None:
                z_move = 0.0
            else:
                z_move = ref_bop - pipe_bop  # in feet

            # (3) Combine XY + Z
            translation_vec = XYZ(xy_vec.X, xy_vec.Y, z_move)

            # (4) Move the pipe
            if move_fabrication_part(p, translation_vec):
                moved_count += 1
                # Now, for the next pipe, we want to measure XY from the *newly moved* pipe
                refXY = p

    MessageBox.Show("Done.\nSuccessfully moved {} pipe(s).".format(moved_count))



# --------------------------------------------------------------
#   4) Execute
# --------------------------------------------------------------
if __name__ == "__main__":
    spread_and_align_bop()