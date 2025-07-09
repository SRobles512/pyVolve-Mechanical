# -*- coding: utf-8 -*-
#  ______   ____     _____  _ __     _______   __  __ _____ ____ _   _    _    _   _ ___ ____    _    _     
# |  _ \ \ / /\ \   / / _ \| |\ \   / / ____| |  \/  | ____/ ___| | | |  / \  | \ | |_ _/ ___|  / \  | |    
# | |_) \ V /  \ \ / / | | | | \ \ / /|  _|   | |\/| |  _|| |   | |_| | / _ \ |  \| || | |     / _ \ | |    
# |  __/ | |    \ V /| |_| | |__\ V / | |___  | |  | | |__| |___|  _  |/ ___ \| |\  || | |___ / ___ \| |___ 
# |_|    |_|     \_/  \___/|_____\_/  |_____| |_|  |_|_____\____|_| |_/_/   \_\_| \_|___\____/_/   \_\_____|

__title__   = "Spread by Gap"
__doc__     = """Version = 1.0
Date    = 01.24.2025
________________________________________________________________
Description:

Automatically adjusts the Center - Center measurement of pipes to get the desired gap between pipes.
________________________________________________________________
How-To:
1. Enter desired gap distance.
2. Select reference pipe.
3. Select pipes that will move.
NOTE: IF THE TOOL IS NOT WORKING AS INTENDED, MAKE SURE YOU ARE NOT USING A SCOPE BOX AND ENSURE THE PIPES ARE PARALLEL TO THE X OR Y AXIS.
________________________________________________________________
Author: Sam Robles
"""
__author__ = "Sam Robles"
__helpurl__ = "https://github.com/SRobles512/pyVolve-Mechanical/wiki"
__min_revit_ver__ = 2022
__max_revit_ver = 2024

# ___ __  __ ____   ___  ____ _____ ____  
#|_ _|  \/  |  _ \ / _ \|  _ \_   _/ ___| 
# | || |\/| | |_) | | | | |_) || | \___ \ 
# | || |  | |  __/| |_| |  _ < | |  ___) |
#|___|_|  |_|_|    \___/|_| \_\|_| |____/
#=========================================

import clr
import math
from collections import OrderedDict

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Fabrication import *

clr.AddReference("RevitAPIUI")
from Autodesk.Revit.UI import *

clr.AddReference("System.Windows.Forms")
import System.Windows.Forms as WinForms
from System.Windows.Forms import MessageBox

# __     ___    ____  ___    _    ____  _     _____ ____  
# \ \   / / \  |  _ \|_ _|  / \  | __ )| |   | ____/ ___| 
#  \ \ / / _ \ | |_) || |  / _ \ |  _ \| |   |  _| \___ \ 
#   \ V / ___ \|  _ < | | / ___ \| |_) | |___| |___ ___) |
#    \_/_/   \_\_| \_\___/_/   \_\____/|_____|_____|____/
#=========================================================

app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

#  _____ _   _ _   _  ____ _____ ___ ___  _   _ ____  
# |  ___| | | | \ | |/ ___|_   _|_ _/ _ \| \ | / ___| 
# | |_  | | | |  \| | |     | |  | | | | |  \| \___ \ 
# |  _| | |_| | |\  | |___  | |  | | |_| | |\  |___) |
# |_|    \___/|_| \_|\____| |_| |___\___/|_| \_|____/                                                     
# ====================================================

def get_user_selected_elements():
    try:
        MessageBox.Show("Please select the fabrication parts in order.\nPress ESC when done.","Select Elements")
        ordered_elements = OrderedDict()
        try:
            index = 0
            while True:
                reference = uidoc.Selection.PickObject(Selection.ObjectType.Element)
                element = doc.GetElement(reference)
                ordered_elements[index] = element
                index += 1
        except:
            pass
        if not ordered_elements:
            MessageBox.Show("No elements were selected. The script will now exit.","No Selection")
            return None
        elements = list(ordered_elements.values())
        return elements
    except Exception as e:
        if 'Operation cancelled by user' not in str(e):
            MessageBox.Show("Error during element selection: {}".format(str(e)), "Error")
        return None

def format_number(value):
    return "{:.5f}".format(value)

def get_location_curve_data(element):
    try:
        location = element.Location
        if not location:
            return None
        location_curve = location.Curve
        if not location_curve:
            return None
        start_point = location_curve.GetEndPoint(0)
        end_point = location_curve.GetEndPoint(1)
        return {
            'curve_type': location_curve.GetType().Name,
            'start': (format_number(start_point.X), format_number(start_point.Y)),
            'end': (format_number(end_point.X), format_number(end_point.Y))
        }
    except Exception:
        pass
    return None

def get_fabrication_parameters(element):
    try:
        if isinstance(element, FabricationPart):
            insulation_thickness = format_number(element.InsulationThickness)
            outside_diameter = element.LookupParameter("Outside Diameter")
            outside_diameter_value = format_number(outside_diameter.AsDouble()) if outside_diameter else "0.00000"
            service_name = element.LookupParameter("Fabrication Service Name")
            service_name_value = service_name.AsString() if service_name else "N/A"
            half_od_value = (float(outside_diameter_value)/2) + float(insulation_thickness)
            half_od = format_number(half_od_value)
            return {
                'insulation_thickness': insulation_thickness,
                'outside_diameter': outside_diameter_value,
                'service_name': service_name_value,
                'half_od': half_od
            }
    except Exception:
        pass
    return None

def calculate_point_difference(point1, point2):
    return (
        format_number(float(point2[0]) - float(point1[0])),
        format_number(float(point2[1]) - float(point1[1]))
    )

def format_difference_output(start_diff, end_diff, next_element_service, current_half_od, next_half_od):
    start_x, start_y = float(start_diff[0]), float(start_diff[1])
    end_x, end_y = float(end_diff[0]), float(end_diff[1])
    output_lines = []
    output_lines.append("\n   Difference to {}:".format(next_element_service))
    def format_point_diff(x_val, y_val, point_type):
        components = []
        if abs(x_val) > 1e-6:
            components.append("X: {}".format(format_number(x_val)))
        if abs(y_val) > 1e-6:
            components.append("Y: {}".format(format_number(y_val)))
        if components:
            return "   {} Point Difference: {}".format(point_type, ", ".join(components))
        return None
    start_diff_line = format_point_diff(start_x, start_y, "Start")
    if start_diff_line:
        output_lines.append(start_diff_line)
    end_diff_line = format_point_diff(end_x, end_y, "End")
    if end_diff_line:
        output_lines.append(end_diff_line)
    x_equal = abs(start_x - end_x) < 1e-6
    y_equal = abs(start_y - end_y) < 1e-6
    if (x_equal and y_equal) or (not x_equal and not y_equal):
        x_value = abs(start_x)
        y_value = abs(start_y)
        center_to_center = format_number(math.sqrt(x_value**2 + y_value**2))
    elif y_equal:
        center_to_center = format_number(abs(start_y))
    elif x_equal:
        center_to_center = format_number(abs(start_x))
    gap = float(center_to_center) - (float(current_half_od) + float(next_half_od))
    gap_str = format_number(gap)
    output_lines.append("   Center to Center: {}".format(center_to_center))
    output_lines.append("   Gap: {}".format(gap_str))
    return "\n".join(output_lines)

def process_elements(elements):
    for i, current_element in enumerate(elements):
        fab_params = get_fabrication_parameters(current_element)
        curve_data = get_location_curve_data(current_element)
        if not fab_params or not curve_data:
            continue
        if i < len(elements) - 1:
            next_element = elements[i + 1]
            next_fab_params = get_fabrication_parameters(next_element)
            next_curve_data = get_location_curve_data(next_element)
            if next_fab_params and next_curve_data:
                start_diff = calculate_point_difference(curve_data['start'], next_curve_data['start'])
                end_diff = calculate_point_difference(curve_data['end'], next_curve_data['end'])
                format_difference_output(
                    start_diff, 
                    end_diff, 
                    next_fab_params['service_name'],
                    fab_params['half_od'],
                    next_half_od=next_fab_params['half_od']
                )

class SpacingForm(WinForms.Form):
    def __init__(self):
        super(SpacingForm, self).__init__()
        self.Text = "Enter Desired Gap"
        self.Width = 300
        self.Height = 150
        self.label = WinForms.Label()
        self.label.Text = 'Enter gap in fractional inches (e.g., 1 1/2"):'
        self.label.Left = 10
        self.label.Top = 20
        self.label.Width = 280
        self.textbox = WinForms.TextBox()
        self.textbox.Left = 10
        self.textbox.Top = 50
        self.textbox.Width = 260
        self.button = WinForms.Button()
        self.button.Text = "OK"
        self.button.Left = 100
        self.button.Top = 80
        self.button.DialogResult = WinForms.DialogResult.OK
        self.Controls.Add(self.label)
        self.Controls.Add(self.textbox)
        self.Controls.Add(self.button)
        self.AcceptButton = self.button

def parse_fractional_inches_to_feet(input_str):
    s = input_str.strip().replace('"', '')
    if not s:
        return 0.0
    parts = s.split()
    total_inches = 0.0
    try:
        if len(parts) == 1:
            if '/' in parts[0]:
                num, denom = parts[0].split('/')
                total_inches = float(num) / float(denom)
            else:
                total_inches = float(parts[0])
        else:
            whole = float(parts[0])
            frac = parts[1]
            if '/' in frac:
                num, denom = frac.split('/')
                frac_val = float(num) / float(denom)
            else:
                frac_val = float(frac)
            total_inches = whole + frac_val
    except:
        total_inches = 0.0
    return total_inches / 12.0

def get_user_selected_reference_pipe():
    MessageBox.Show("Please select the reference pipe.\nPress ESC if you wish to cancel.", "Select Reference Pipe")
    try:
        ref = uidoc.Selection.PickObject(Selection.ObjectType.Element)
        if ref:
            return doc.GetElement(ref)
    except:
        pass
    return None

def get_user_selected_pipes_to_move():
    MessageBox.Show("Please select the pipes to move in order from nearest to farthest.\nPress ESC when done.", "Select Pipes to Move")
    ordered_elements = OrderedDict()
    try:
        index = 0
        while True:
            reference = uidoc.Selection.PickObject(Selection.ObjectType.Element)
            element = doc.GetElement(reference)
            ordered_elements[index] = element
            index += 1
    except:
        pass
    if not ordered_elements:
        MessageBox.Show("No pipes were selected to move.", "No Selection")
        return None
    return list(ordered_elements.values())

def move_fabrication_part(part, translation_vector):
    location = part.Location
    if isinstance(location, LocationCurve):
        location.Move(translation_vector)
        return True
    return False

def calculate_gap_between(pipeA, pipeB):
    paramsA = get_fabrication_parameters(pipeA)
    curveA = get_location_curve_data(pipeA)
    paramsB = get_fabrication_parameters(pipeB)
    curveB = get_location_curve_data(pipeB)
    if not (paramsA and curveA and paramsB and curveB):
        return None, 0.0
    start_diff = calculate_point_difference(curveA['start'], curveB['start'])
    start_x = float(start_diff[0])
    start_y = float(start_diff[1])
    if abs(start_x) > 1e-6 and abs(start_y) > 1e-6:
        c2c = math.sqrt((start_x**2) + (start_y**2))
        axis = (start_x, start_y)
    elif abs(start_x) > 1e-6:
        c2c = abs(start_x)
        axis = ("x", start_x)
    else:
        c2c = abs(start_y)
        axis = ("y", start_y)
    half_od_A = float(paramsA['half_od'])
    half_od_B = float(paramsB['half_od'])
    gap = c2c - (half_od_A + half_od_B)
    return axis, gap

def move_selected_pipes(reference_pipe, pipes_to_move, desired_gap_feet):
    moved_info = []
    t = Transaction(doc, "Move Pipes")
    t.Start()
    current_reference = reference_pipe
    for p in pipes_to_move:
        axis, actual_gap = calculate_gap_between(current_reference, p)
        if axis is None:
            continue
        distance_to_move = desired_gap_feet - actual_gap
        if isinstance(axis, tuple):
            if isinstance(axis[0], str):
                direction_str, axis_val = axis
                if direction_str.lower() == 'x':
                    translation_vec = XYZ(distance_to_move if axis_val >= 0 else -distance_to_move, 0, 0)
                else:
                    translation_vec = XYZ(0, distance_to_move if axis_val >= 0 else -distance_to_move, 0)
            else:
                start_x, start_y = axis
                length_2d = math.sqrt(start_x**2 + start_y**2)
                if length_2d > 1e-9:
                    scale = distance_to_move / length_2d
                    dx = start_x * scale
                    dy = start_y * scale
                    translation_vec = XYZ(dx, dy, 0)
                else:
                    translation_vec = XYZ(0, 0, 0)
        else:
            translation_vec = XYZ(0, 0, 0)
        success = move_fabrication_part(p, translation_vec)
        if success:
            _, new_gap = calculate_gap_between(current_reference, p)
            moved_info.append((p.Id, new_gap))
        current_reference = p
    t.Commit()
    return moved_info

#  __  __    _    ___ _   _ 
# |  \/  |  / \  |_ _| \ | |
# | |\/| | / _ \  | ||  \| |
# | |  | |/ ___ \ | || |\  |
# |_|  |_/_/   \_\___|_| \_|
#===========================

def main():
    form = SpacingForm()
    dialog_result = form.ShowDialog()
    if dialog_result != WinForms.DialogResult.OK:
        MessageBox.Show("Operation cancelled by user. Exiting.", "Cancelled")
        return
    desired_gap_str = form.textbox.Text
    desired_gap_feet = parse_fractional_inches_to_feet(desired_gap_str)
    if desired_gap_feet <= 0.0:
        MessageBox.Show("Invalid gap entered. Exiting.", "Error")
        return
    reference_pipe = get_user_selected_reference_pipe()
    if not reference_pipe:
        MessageBox.Show("No reference pipe selected. Exiting.", "No Selection")
        return
    pipes_to_move = get_user_selected_pipes_to_move()
    if not pipes_to_move:
        MessageBox.Show("No pipes selected. Exiting.", "No Selection")
        return
    moved_info = move_selected_pipes(reference_pipe, pipes_to_move, desired_gap_feet)
    moved_count = len(moved_info)
    msg = "Successfully moved {} pipes.".format(moved_count)
    MessageBox.Show(msg, "Operation Complete")

if __name__ == '__main__':
    main()