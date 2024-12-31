# -*- coding: utf-8 -*-
__title__ = "Adjust Rod Length"  
__doc__ = """Version = 1.0
Date    = 12.30.2024
_____________________________________________________________________
Description:
This tool modifies the rod length on MEP Fabrication Hangers that are attached to structure.
_____________________________________________________________________
Instructions:
-> Select the hanger you want to modify.
-> Input desired distance from structure you want the top of the rod. 
-> Click enter. 
_____________________________________________________________________
Last update:
- [12.30.2024] - 1.0 - Release
_____________________________________________________________________
To-Do:
- Allow selection of multiple hangers
_____________________________________________________________________
Author: Sam Robles"""                                           

#pyRevit Metadata                                         
#__context__  = ['MEP Fabrication Hangers'] # Button isn't available unless a hanger is already selected. 

#IMPORTS
# ==================================================

# .NET Imports
import clr

clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from System.Windows.Forms import (
    Form, Label, TextBox, Button, DialogResult, 
    FormStartPosition, MessageBox
)
from System.Drawing import Point, Size, Font
import re
import traceback

#Revit & pyRevit Imports
from pyrevit import DB, revit

# VARIABLES
# ==================================================

doc       = __revit__.ActiveUIDocument.Document   #type: UIDocument     # Document   class from RevitAPI that represents project. Used to Create, Delete, Modify and Query elements from the project.
uidoc     = __revit__.ActiveUIDocument            #type: Document       # UIDocument class from RevitAPI that represents Revit project opened in the Revit UI.
selection = uidoc.Selection                       #type: Selection
app       = __revit__.Application                 #type: UIApplication  # Represents the Autodesk Revit Application, providing access to documents, options and other application wide data and settings.
rvt_year  = int(app.VersionNumber)                # e.g. 2023

# MAIN
# ==================================================

class DistanceInputForm(Form):
    def __init__(self):

        # Explicitly call the base class constructor
        Form.__init__(self)   # This avoids potential issues with super()

        # Initialize the form
        self.Text = "Adjust Rod Lengths"
        self.Size = Size(800, 400)
        self.StartPosition = FormStartPosition.CenterScreen

        # Instruction label
        self.label = Label()
        self.label.Text = (
            "Enter desired distance below structure using one of the following formats:\n\n"
            "1. Feet: 1'\n"
            "2. Feet and Inches: 1' 1\"\n"
            "3. Feet and Fractional Inches: 0' 0-1/2\"\n"
            "4. Inches: 1\"\n"
            "5. Inches with Fraction: 1-1/2\"\n"
            "6. Fraction only: 1/2\"\n"
        )
        self.label.Location = Point(10, 10)
        self.label.Size = Size(800, 220)
        self.label.Font = Font("Arial", 10)
        self.label.AutoSize = False
        self.Controls.Add(self.label)

        # Text box for user input
        self.textbox = TextBox()
        self.textbox.Location = Point(125, 230)
        self.textbox.Size = Size(500, 20)
        self.Controls.Add(self.textbox)

        # Enter button
        self.button = Button()
        self.button.Text = "Enter"
        self.button.Location = Point(325, 270)
        self.button.Size = Size(100, 50)
        self.button.Click += self.on_enter
        self.Controls.Add(self.button)

        # Store the user input
        self.user_input = None
        self.decimal_feet = None

    def on_enter(self, sender, event):
        # Capture the user input
        self.user_input = self.textbox.Text

        # Validate the input using regex
        if not self.validate_input(self.user_input):
            # Show error message if validation fails
            MessageBox.Show(
                "Invalid input format. Please use one of the formats described in the instructions.",
                "Input Error"
            )
        else:
            # Convert the input to decimal feet
            decimal_feet_value = self.convert_to_decimal_feet(self.user_input)
            # Show conversion in a message box (informative, optional)
            #MessageBox.Show(
            #   "Input in Decimal Feet: {:.5f}".format(float(decimal_feet_value)),
            #   "Conversion Successful"
            #)
            # Close the form with OK result if input is valid
            self.DialogResult = DialogResult.OK
            # Store conversion result
            self.decimal_feet = decimal_feet_value
            self.Close()

    def validate_input(self, input_text):
        # Regex for valid formats
        pattern = (
            r"^(\d+' \d+-\d+/\d+\")|"  # e.g. 0' 0-1/2"
            r"(\d+-\d+/\d+\")|"        # e.g. 1-1/2"
            r"(\d+/\d+\")|"            # e.g. 1/2"
            r"(\d+' \d+\")|"           # e.g. 1' 1"
            r"(\d+\")|"                # e.g. 1"
            r"(\d+')$"                 # e.g. 1'
        )
        return bool(re.match(pattern, input_text))

    def convert_to_decimal_feet(self, input_text):
        # Handle conversion based on input format

        # 1) Feet + Inches + Fraction, e.g. "0' 0-1/2"
        if "'" in input_text and "-" in input_text:  
            feet, rest = input_text.split("'")
            feet = int(feet.strip())
            inches, fraction = rest.split("-")
            inches = int(inches.strip())
            num, denom = map(int, fraction[:-1].split("/"))  # remove the trailing "
            fraction_val = float(num) / float(denom)
            return float(feet) + float(inches + fraction_val) / 12.0

        # 2) Inches + Fraction only, e.g. "1-1/2"
        elif "-" in input_text:  
            inches, fraction = input_text.split("-")
            inches = int(inches.strip())
            num, denom = map(int, fraction[:-1].split("/"))  # remove "
            fraction_val = float(num) / float(denom)
            return float(inches + fraction_val) / 12.0

        # 3) Fraction only, e.g. "1/2"
        elif "/" in input_text:  
            num, denom = map(int, input_text[:-1].split("/"))  # remove "
            fraction_val = float(num) / float(denom)
            return float(fraction_val) / 12.0

        # 4) Feet + Inches, e.g. "1' 6""
        elif "'" in input_text and '"' in input_text:  
            feet, inches = input_text.split("'")
            feet = int(feet.strip())
            inches = int(inches[:-1].strip())  # remove "
            return float(feet) + float(inches) / 12.0

        # 5) Inches only, e.g. "6""
        elif '"' in input_text:  
            inches = int(input_text[:-1].strip())  # remove "
            return float(inches) / 12.0

        # 6) Feet only, e.g. "1'"
        elif "'" in input_text:  
            feet = int(input_text[:-1].strip())  # remove '
            return float(feet)

        # Fallback
        return 0.0


# ---------------------------------------------------------
# MAIN SCRIPT 
# ---------------------------------------------------------
def main():
    
    try:
        # Get the currently selected element(s)
        selection = revit.get_selection()
        if not selection:
            MessageBox.Show("No elements selected. Please select an element and run the script again.",
                            "Selection Error")
            return  # Exit script

        # Work with the first selected element (single-element workflow)
        selected_element = selection.first

        # Check if the selected element has FabricationRodInfo
        if not hasattr(selected_element, "GetRodInfo"):
            MessageBox.Show("The selected element does not have FabricationRodInfo.",
                            "Invalid Element")
            return  # Exit script

        fabrication_rod_info = selected_element.GetRodInfo()
        if fabrication_rod_info is None:
            MessageBox.Show("The selected element's FabricationRodInfo is unavailable.",
                            "Invalid Element")
            return  # Exit script

        # Show the user input form to get distance in decimal feet
        form = DistanceInputForm()
        result = form.ShowDialog()
        if result != DialogResult.OK:
            # If the user cancels or closes form, exit without changes
            return

        decimal_feet_value = float(form.decimal_feet)  # Make sure it's float
       
        # Convert to negative (distance below structure)
        negative_decimal_feet = -decimal_feet_value
        
        # Loop through rods, set extension in a single transaction per rod
        for rod_index in range(fabrication_rod_info.RodCount):

            # Start a new transaction for each rod
            with revit.Transaction("Set Rod Extension for Rod {}".format(rod_index)):
                initial_length = fabrication_rod_info.GetRodLength(rod_index)

                # Set the rod extension to negative_decimal_feet
                result_extension = fabrication_rod_info.SetRodStructureExtension(rod_index, negative_decimal_feet)
                
                updated_length = fabrication_rod_info.GetRodLength(rod_index)

        # Final success message
        MessageBox.Show("Script completed successfully.", "Success")

    except Exception as e:
        # Catch and display any exceptions
        error_msg = "An error occurred:\n{}\n\nTraceback:\n{}".format(str(e), traceback.format_exc())
        MessageBox.Show(error_msg, "Error")



# ---------------------------------------------------------
# RUN MAIN
# ---------------------------------------------------------
if __name__ == "__main__":
    main()