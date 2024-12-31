# -*- coding: utf-8 -*-
from pyrevit import script
output = script.get_output()

def kit_button_clicked(btn_name):
    # 👀 Print Message
    output.print_md('## ✅️ {btn_name} was Clicked ✨'.format(btn_name=btn_name))  # <- Print MarkDown Heading 2
    output.print_md('---')
    output.print_md('⌨️ Hold **ALT + CLICK** to open the source code of this button. ')  # <- Print MarkDown Heading 2
    output.print_md('*You can Duplicate, or use this placeholder for your own script.*')
