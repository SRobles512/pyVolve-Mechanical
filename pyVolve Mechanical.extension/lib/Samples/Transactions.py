# -*- coding: utf-8 -*-
__title__   = "Samples - Transactions"
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


# ╔╦╗╦═╗╔═╗╔╗╔╔═╗╔═╗╔═╗╔╦╗╦╔═╗╔╗╔  ╔═╗╔═╗╔╦╗╔═╗╦  ╔═╗╔═╗
#  ║ ╠╦╝╠═╣║║║╚═╗╠═╣║   ║ ║║ ║║║║  ╚═╗╠═╣║║║╠═╝║  ║╣ ╚═╗
#  ╩ ╩╚═╩ ╩╝╚╝╚═╝╩ ╩╚═╝ ╩ ╩╚═╝╝╚╝  ╚═╝╩ ╩╩ ╩╩  ╩═╝╚═╝╚═╝ TRANSACTION SAMPLES
#====================================================================================================
#🟠 Regular Transaction
t = Transaction(doc, 'Change-Name')
t.Start()

# Changes Here...

t.Commit()


#--------------------------------------------------
#🟠 Regular Transaction + Try/Except
t = Transaction(doc, 'Change-Name')
t.Start()
try:

    # Changes Here...
    t.Commit()
except:
    t.RollBack()

#--------------------------------------------------
#🟠 Regular Transaction as Context-Manager
with Transaction(doc, 'Change-Name') as t:
    t.Start()

    #Changes Here

    t.Commit()




#--------------------------------------------------
#🟠 Sub-Transactions can only exist inside regular Transaction
t = Transaction(doc, 'Change-Name')
t.Start()

# Changes Can be Here...

st1 = SubTransaction(doc)
st1.Start()
# Changes Can be Here...
st1.Commit()

# Changes Can be Here...


st2 = SubTransaction(doc)
st2.Start()
# Changes Can be Here...
st2.Commit()

t.Commit()

#--------------------------------------------------
#🟠 TransactionGroup - Combine Multiple Transactions

tg = TransactionGroup(doc, "Change-Name")
tg.Start()


t1 = Transaction(doc, 'Change A')
t1.Start()
# Changes here
t1.Commit()

t2 = Transaction(doc, 'Change B')
t2.Start()
# Changes here
t2.Commit()

tg.Assimilate() # Combine All Transacitons into one

# ╦ ╦╔═╗╔═╗╔═╗╦ ╦  ╔═╗╔═╗╔╦╗╦╔╗╔╔═╗  ||
# ╠═╣╠═╣╠═╝╠═╝╚╦╝  ║  ║ ║ ║║║║║║║ ╦  ||
# ╩ ╩╩ ╩╩  ╩   ╩   ╚═╝╚═╝═╩╝╩╝╚╝╚═╝  .. ⌨️ HAPPY CODING!

# Find More Snippets Here:              - www.LearnRevitAPI.com/python-snippets
# E-Book: Beginner's Guide to Revit API - www.LearnRevitAPI.com/ebook
# E-Book: Master Getting Elements (FEC) - www.LearnRevitAPI.com/ebook/fec

