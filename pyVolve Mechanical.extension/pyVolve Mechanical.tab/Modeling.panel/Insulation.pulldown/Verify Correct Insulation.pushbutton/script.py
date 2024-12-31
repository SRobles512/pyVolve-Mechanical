
# -*- coding: utf-8 -*-
__title__   = "Place Insulation"
__doc__     = """Version = 1.0
Date    = 12.28.2024
________________________________________________________________
Description:
Places Insulation based on user-defined specification.

________________________________________________________________
How-To:

1. Choose service name from drop down box

________________________________________________________________
________________________________________________________________
Last Updates:
- [12.28.2024] - RELEASE
________________________________________________________________
Author: Sam Robles"""

import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
import csv
import os

from System.Windows.Forms import Form, ComboBox, Button, Label, DialogResult, ComboBoxStyle
from System.Drawing import Point, Size as DrawingSize

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction, ElementId, FabricationPart
from Autodesk.Revit.UI import UIDocument

def load_insulation_specs():
    """Load insulation specifications from CSV file."""
    specs = []
    script_dir = os.path.dirname(__file__)
    csv_path = os.path.join(script_dir, "InsulationSpecs.csv")
    
    try:
        with open(csv_path, 'rb') as f:  # Use 'rb' for IronPython
            reader = csv.DictReader(f)
            for row in reader:
                # Handle empty values for Min OD and Max OD
                min_od = float(row['Min OD']) if row['Min OD'].strip() else 0.0
                max_od = float(row['Max OD']) if row['Max OD'].strip() else float('inf')
                
                specs.append({
                    'Service': row['Service'].strip(),
                    'Min_OD': min_od,
                    'Max_OD': max_od,
                    'Insulation_Specification': int(row['Insulation Specification'])
                })
        return specs
    except Exception as e:
        print("Error loading CSV: {}".format(e))
        return []

def parse_size_to_inches(size_str):
    """
    Parse size string to inches.
    
    Args:
        size_str (str): Size string to parse
        
    Returns:
        float: Size in inches
    """
    # Remove double quotes and strip whitespace
    size_str = size_str.replace('"', '').strip()

    if not size_str:
        return 0.0

    # Check if there's a dash in the size_str
    if '-' in size_str:
        # If there's a dash, only parse the first token
        parts = size_str.split()
        if not parts:
            return 0.0
        first_token = parts[0]

        # If the first token contains a dash, split and take the first part
        if '-' in first_token:
            first_token = first_token.split('-')[0]

        # Parse the cleaned first_token
        if '/' in first_token:
            num, den = first_token.split('/')
            return float(num) / float(den)
        else:
            return float(first_token)
    else:
        # No dash: parse the entire size_str
        # Combine all tokens to get a total in inches
        parts = size_str.split()
        total = 0.0
        for p in parts:
            if '/' in p:
                num, den = p.split('/')
                total += float(num) / float(den)
            else:
                total += float(p)
        return total

def get_new_insulation_spec(service, size_inches):
    """
    Determine insulation specification based on service and size.
    
    Args:
        service (str): Service type
        size_inches (float): Size in inches
        
    Returns:
        float: Insulation specification number
    """
    specs = load_insulation_specs()
    
    # Find matching specifications for the service
    service_specs = [spec for spec in specs if spec['Service'] == service]
    
    if not service_specs:
        return 0  # Default to no insulation if service not found
        
    # Find the appropriate specification based on size
    for spec in service_specs:
        if spec['Min_OD'] <= size_inches <= spec['Max_OD']:
            return spec['Insulation_Specification']
    
    return 0  # Default to no insulation if no size range matches

class ServiceSelectionForm(Form):
    """Form for selecting service type."""
    def __init__(self):
        self.Text = "Select Service"
        self.Size = DrawingSize(400, 200)

        self.label = Label()
        self.label.Text = "Please select a service:"
        self.label.Location = Point(80, 10)
        self.label.AutoSize = True
        self.Controls.Add(self.label)

        self.combo = ComboBox()
        self.combo.Location = Point(40, 40)
        self.combo.Width = 300
        self.combo.DropDownStyle = ComboBoxStyle.DropDownList
        
        # Load services from CSV
        specs = load_insulation_specs()
        if specs:
            # Get unique services using a set comprehension and add to combo box
            unique_services = {spec['Service'] for spec in specs}
            for service in sorted(unique_services):
                self.combo.Items.Add(service)
        
        self.Controls.Add(self.combo)

        self.ok_button = Button()
        self.ok_button.Text = "OK"
        self.ok_button.Size = DrawingSize(100, 50)
        self.ok_button.Location = Point(150, 80)
        self.ok_button.Click += self.ok_clicked
        self.Controls.Add(self.ok_button)

    def ok_clicked(self, sender, args):
        if self.combo.SelectedItem:
            self.DialogResult = DialogResult.OK
            self.Close()
        else:
            # If no selection, do nothing.
            pass

# Main execution
if __name__ == '__main__':
    # Display the form
    form = ServiceSelectionForm()
    dialog_result = form.ShowDialog()
    if dialog_result != DialogResult.OK:
        # If user closed without selecting, end the script
        raise SystemExit("No service selected.")

    selected_service = form.combo.SelectedItem

    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document

    fabricationPipeworkCatId = ElementId(BuiltInCategory.OST_FabricationPipework)

    # Get the currently selected element IDs
    selected_ids = uidoc.Selection.GetElementIds()

    selected_fabrication_parts = []
    failed_elements = []  # Track elements that couldn't be modified

    for elem_id in selected_ids:
        elem = doc.GetElement(elem_id)
        if elem is not None and elem.Category is not None:
            if elem.Category.Id == fabricationPipeworkCatId:
                fab_part = elem if isinstance(elem, FabricationPart) else None
                if fab_part:
                    selected_fabrication_parts.append(fab_part)

    # Start a transaction to modify the model
    t = Transaction(doc, "Change Insulation Specification")
    t.Start()

    for part in selected_fabrication_parts:
        try:
            # Get current properties
            current_insulation = part.InsulationSpecification
            size_str = part.Size
            size_inches = parse_size_to_inches(size_str)

            # Determine new_insulation_spec based on selected service and size_inches
            new_insulation_spec = get_new_insulation_spec(selected_service, size_inches)

            # Set the insulation spec accordingly
            part.InsulationSpecification = new_insulation_spec
            
        except Exception as e:
            # Add failed element to the list
            failed_elements.append(part.Id)

    t.Commit()

    # Report failed elements if any
    if failed_elements:
        print("Could not place insulation on elements: {}".format(", ".join(str(id.IntegerValue) for id in failed_elements)))