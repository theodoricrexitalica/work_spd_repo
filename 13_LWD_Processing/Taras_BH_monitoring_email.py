# -*- coding: utf-8 -*-
from __future__ import division
#Declarations
#The dictionary of parameters
#name,bname,type,family,unit,value,mode,description,group,min,max,list,enable,iscombocheckbox,isused
parameterDict = {}
try:
	if Parameter:
		pass
except NameError:
	class Parameter:
		def __init__(self, **d):
			pass
#DeclarationsEnd
# -*- coding: utf-8 -*-
import TechlogDialogAdvanced as TDA
import win32com.client as win32
import pythoncom
pythoncom.CoInitialize()
name_list = (["Тарас Долгушин",
		 "Александр Головатый"])
myDialog = TDA.dialogAdvanced("Horizontal wells")
myDialog.addButtonsGroup("Name", "Operator", name_list,1)
if myDialog.execDialog():
	name = myDialog.getButtonsGroup("Name")[0]

text1 = "Добрый день,<br>С 21:00 до 9:00 на дежурство со стороны SPD SSFT заступает " 
name1     = u"<p>Regards," + \
			"<br>Taras Dolgushin" + \
		 	"<br>Field Petrophysicist" + \
		 	"<br>Sub Surface Field Team" + \
			"<br>Salym Petroleum Development N.V." + \
			"<br>Phone:  +7 3463 297 300 ext.3486" + \
			"<br>Mobile: +7 932 440 29 29" + \
			"<br>E-mail work: SPD-SALYM-SSFT-GE-C@salympetroleum.ru" + \
			"<br>E-mail personal: Taras.Dolgushin@salympetroleum.ru"
name2     = u"<p>Regards," + \
			"<br>Alexander Golovatiy" + \
		 	"<br>Field Petrophysicist" + \
		 	"<br>Sub Surface Field Team" + \
			"<br>Salym Petroleum Development N.V." + \
			"<br>Phone:  +7 3463 297 300, ext. 3486" + \
			"<br>Mobile: +7 922 247 40 15" + \
			"<br>E-mail work: SPD-SALYM-SSFT-GE-C@salympetroleum.ru" + \
			"<br>E-mail personal: Alexander.Golovatiy@salympetroleum.ru"

if name == name_list[0].decode("utf-8"):
	text2 = name1
else:
	text2 = name2
for well in db.selectedWellList():
	well_name = "-".join(well.split("-")[:3])
email = win32.Dispatch("Outlook.Application")
Msg = email.CreateItem(0)
Msg.Subject = "Дежурство ".decode("utf-8") + well_name
Msg.HTMLBody = text1.decode("utf-8") + name + "." + text2
Msg.Display()

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-03-02"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""