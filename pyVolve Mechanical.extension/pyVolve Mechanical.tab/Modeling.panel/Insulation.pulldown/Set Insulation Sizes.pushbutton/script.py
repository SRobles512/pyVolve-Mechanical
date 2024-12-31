# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
__title__   = "Set Insulation Specification"
__doc__     = """Version = 1.0
Date    = 12.30.2024
________________________________________________________________
Description:
Opens CSV file where you are able to modify the insulation sizes placed on the pipe.
________________________________________________________________
Last Updates:
- [12.30.2024] - RELEASE
________________________________________________________________
Author: Sam Robles"""

#IMPORTS
#===============================================================

# .NET Imports
import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
import os
import csv

from System.Windows.Forms import (
    Form, DataGridView, DataGridViewTextBoxColumn, 
    Button, AnchorStyles, DialogResult,
    DockStyle, ScrollBars, DataGridViewAutoSizeColumnsMode,
    DataGridViewTriState, DataGridViewColumnHeadersHeightSizeMode,
    MessageBox, MessageBoxButtons, MessageBoxIcon,
    Keys, Clipboard
)
from System.Drawing import Point, Size, Color

class CSVEditorForm(Form):
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.InitializeComponent()
        self.LoadCSVData()

    def InitializeComponent(self):
        # Form settings
        self.Text = "Insulation Specification Editor"
        self.Size = Size(1500, 950)
        
        # Create DataGridView
        self.grid = DataGridView()
        self.grid.Location = Point(100, 100)
        self.grid.Size = Size(1300, 700)
        self.grid.ScrollBars = ScrollBars.Vertical
        self.grid.AllowUserToAddRows = True
        self.grid.AllowUserToDeleteRows = True
        self.grid.BackgroundColor = Color.White
        self.grid.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill
        self.grid.RowHeadersWidth = 50
        self.grid.ColumnHeadersHeight = 100
        
        # Add key event handler for copy/paste and delete
        self.grid.KeyDown += self.HandleKeyDown
        
        # Create Save button
        self.save_button = Button()
        self.save_button.Size = Size(100, 50)
        self.save_button.Text = "Save"
        self.save_button.Location = Point(1350, 825)
        self.save_button.Click += self.SaveCSV
        
        # Create Cancel button
        self.cancel_button = Button()
        self.cancel_button.Size = Size(100, 50)
        self.cancel_button.Text = "Cancel"
        self.cancel_button.Location = Point(1200, 825)
        self.cancel_button.Click += self.CancelEdit
        
        # Add controls to form
        self.Controls.Add(self.grid)
        self.Controls.Add(self.save_button)
        self.Controls.Add(self.cancel_button)

    def HandleKeyDown(self, sender, event):
        # Handle copy (Ctrl+C)
        if event.Control and event.KeyCode == Keys.C:
            self.CopyToClipboard()
            event.Handled = True
            
        # Handle paste (Ctrl+V)
        elif event.Control and event.KeyCode == Keys.V:
            self.PasteFromClipboard()
            event.Handled = True
            
        # Handle delete key
        elif event.KeyCode == Keys.Delete:
            self.DeleteSelectedRows()
            event.Handled = True

    def CopyToClipboard(self):
        try:
            if self.grid.SelectedCells.Count > 0:
                rows = set()
                cols = set()
                
                # Get the range of selected cells
                for cell in self.grid.SelectedCells:
                    rows.add(cell.RowIndex)
                    cols.add(cell.ColumnIndex)
                
                # Sort rows and columns
                rows = sorted(list(rows))
                cols = sorted(list(cols))
                
                # Build the clipboard text
                clipboard_text = []
                for row in rows:
                    row_data = []
                    for col in cols:
                        value = self.grid[col, row].Value
                        row_data.append(str(value) if value is not None else '')
                    clipboard_text.append('\t'.join(row_data))
                
                # Set clipboard content
                Clipboard.SetText('\n'.join(clipboard_text))
        except Exception as e:
            MessageBox.Show(str(e), "Copy Error", MessageBoxButtons.OK, MessageBoxIcon.Error)

    def PasteFromClipboard(self):
        try:
            clipboard_text = Clipboard.GetText()
            if not clipboard_text:
                return

            rows = clipboard_text.split('\n')
            if not rows:
                return

            current_row = self.grid.CurrentCell.RowIndex
            current_col = self.grid.CurrentCell.ColumnIndex

            for i, row_text in enumerate(rows):
                if not row_text.strip():  # Skip empty rows
                    continue
                    
                if current_row + i >= self.grid.RowCount - 1:  # -1 to account for new row
                    self.grid.Rows.Add()

                cells = row_text.split('\t')
                for j, cell_text in enumerate(cells):
                    if current_col + j < self.grid.ColumnCount:
                        self.grid[current_col + j, current_row + i].Value = cell_text.strip()

        except Exception as e:
            MessageBox.Show(str(e), "Paste Error", MessageBoxButtons.OK, MessageBoxIcon.Error)

    def DeleteSelectedRows(self):
        try:
            if self.grid.SelectedRows.Count > 0:
                # Convert to list because we'll be modifying the collection
                rows_to_delete = sorted([row.Index for row in self.grid.SelectedRows 
                                      if not row.IsNewRow], reverse=True)
                for row_index in rows_to_delete:
                    self.grid.Rows.RemoveAt(row_index)
        except Exception as e:
            MessageBox.Show(str(e), "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Error)

    def LoadCSVData(self):
        try:
            # Read CSV data
            with open(self.csv_path, 'r') as file:
                reader = csv.reader(file)
                headers = next(reader)
                data = []
                for row in reader:
                    # Convert empty strings to None for numeric columns
                    processed_row = []
                    for i, value in enumerate(row):
                        if i == 0:  # Service column (string)
                            processed_row.append(value)
                        elif i in (1, 2):  # Min OD and Max OD (float)
                            processed_row.append(float(value) if value else None)
                        elif i == 3:  # Insulation Specification (integer)
                            processed_row.append(int(value) if value else None)
                    data.append(processed_row)
            
            # Add columns to grid with proper formatting
            # Service Column
            service_col = DataGridViewTextBoxColumn()
            service_col.HeaderText = "Service"
            service_col.Name = "Service"
            service_col.Width = 250
            self.grid.Columns.Add(service_col)
            
            # Min OD Column
            min_od_col = DataGridViewTextBoxColumn()
            min_od_col.HeaderText = "Min\nOD"
            min_od_col.Name = "Min OD"
            min_od_col.Width = 100
            self.grid.Columns.Add(min_od_col)
            
            # Max OD Column
            max_od_col = DataGridViewTextBoxColumn()
            max_od_col.HeaderText = "Max\nOD"
            max_od_col.Name = "Max OD"
            max_od_col.Width = 100
            self.grid.Columns.Add(max_od_col)
            
            # Insulation Specification Column
            insulation_col = DataGridViewTextBoxColumn()
            insulation_col.HeaderText = "Insulation Specification"
            insulation_col.Name = "Insulation Specification"
            insulation_col.Width = 300
            self.grid.Columns.Add(insulation_col)
            
            # Add data to grid
            for row in data:
                self.grid.Rows.Add(*row)
                
        except Exception as e:
            MessageBox.Show(
                'Error loading CSV file:\n{}'.format(str(e)),
                'Error',
                MessageBoxButtons.OK,
                MessageBoxIcon.Error)
            self.Close()

    def SaveCSV(self, sender, event):
        try:
            # Get headers
            headers = [col.Name for col in self.grid.Columns]  # Use Name instead of HeaderText
            
            # Get data
            data = []
            for row in range(self.grid.RowCount - 1):  # -1 to skip empty row
                row_data = []
                for col in range(self.grid.ColumnCount):
                    value = self.grid.Rows[row].Cells[col].Value
                    row_data.append(value if value is not None else '')
                data.append(row_data)
            
            # Write to CSV
            with open(self.csv_path, 'wb') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerows(data)
            
            MessageBox.Show(
                'CSV file saved successfully!',
                'Success',
                MessageBoxButtons.OK,
                MessageBoxIcon.Information)
            self.DialogResult = DialogResult.OK
            self.Close()
            
        except Exception as e:
            MessageBox.Show(
                'Error saving CSV file:\n{}'.format(str(e)),
                'Error',
                MessageBoxButtons.OK,
                MessageBoxIcon.Error)

    def CancelEdit(self, sender, event):
        self.DialogResult = DialogResult.Cancel
        self.Close()

def main():
    # CSV file path
    csv_path = os.path.join(
        os.getenv("APPDATA"),
        r"pyRevit\Extensions\pyVolve Mechanical.extension\pyVolve Mechanical.tab\Modeling.panel\Insulation.pulldown\Verify Correct Insulation.pushbutton\InsulationSpecs.csv"
    )

    # Check if file exists
    if not os.path.exists(csv_path):
        MessageBox.Show(
            'CSV file not found at specified location.',
            'Error',
            MessageBoxButtons.OK,
            MessageBoxIcon.Error
        )
        # Exit the script
        return()
    
    # Create and show form
    form = CSVEditorForm(csv_path)
    form.ShowDialog()

if __name__ == '__main__':
    main()
