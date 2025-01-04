# pyVolve Mechanical

pyVolve Mechanical is an extension for the [pyRevit](https://github.com/pyrevitlabs/pyRevit) add-in, tailored specifically for piping detailers working with Fabrication Parts. This extension is designed to save time, reduce repetitive tasks, and make your modeling process smoother and more efficient.

see [Wiki](https://github.com/SRobles512/pyVolve-Mechanical/wiki) for more details.

---

## Installation
To install pyVolve Mechanical, follow these steps:
1. Ensure you have [**pyRevit**](https://github.com/pyrevitlabs/pyRevit/releases) and [**Revit (versions 2022–2024)**](https://www.autodesk.com/products/revit/overview?term=1-YEAR&tab=subscription) installed on your machine.

2. **If you have Git installed**, Clone the repository using:
   ```
   gh repo clone SRobles512/pyVolve-Mechanical
   ```
   **If you do not have Git installed**, click on the green <> Code Button and click downlaod ZIP
   
   ![image](https://github.com/user-attachments/assets/aa114efd-a7aa-4c04-99d2-61849a64c0d6)

4. Move the `pyVolve Mechanical.extension` folder to the following directory by copy and pasting into the address bar of the File Explorer:
   ```
   %AppData%\pyRevit\Extensions\
   ```
5. Discard the rest of the cloned content.
6. Reload pyRevit to activate the extension.

*Note: The extension must be located in the specified directory to ensure proper pathing.*

---

## Features

- **Adjust Rod Length**: Allows the user to adjust the Rod Length of hangers that are attached to structure.
- **Automate Insulation**: Save time by automating insulation tasks for piping.
- **Elevation Alignment**: Allows the user to align pipes by any of the following - Align by Bottom of Insulation, Align by Bottom of Pipe, Align by Centerline, Align by Top of Pipe, Align by Top of Insulation

---

## License

This project is licensed under the **GNU General Public License v3.0**.  
For more details, see the [full license text](https://www.gnu.org/licenses/gpl-3.0.html).

---

## Acknowledgments

Special thanks to:

- [pyRevit Labs](https://github.com/pyrevitlabs) for developing pyRevit.
- [Erik Frits](https://github.com/ErikFrits) for his YouTube tutorials and the template used to create this extension.

---

Thank you for using pyVolve Mechanical! Feel free to contribute, report issues, or share your feedback.

---

## Disclaimer

Let me be perfectly clear: I am not a developer, nor a programmer. At best I am decent at debugging the scripts that AI writes. This extension was crafted with the assistance of ChatGPT and Claude AI. Blame them if it misbehaves. 
