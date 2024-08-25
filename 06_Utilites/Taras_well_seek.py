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
import TechlogDialogAdvanced as tda
import TechlogDialog as td
import os
file_path = os.path.join(db.dirProject(), "Data", "report.txt")
file_txt = file(file_path, "wb")
list = ["Print report"]
myDialog = tda.dialogAdvanced("Well Name")
myDialog.addTextInput("Name","Type well name","",0)
myDialog.addButtonsGroup("Well Name","",list,0)
myDialog.execDialog()
well_name = myDialog.getTextInput("Name")
trigger = myDialog.getButtonsGroup("Well Name")
for well in db.wellList():
	if well_name in well:
		print well
		if len(trigger) != 0:
			file_txt.write(well+"\r\n")
		else:
			pass
if len(trigger) != 0:
	os.startfile(file_path)
	file_txt.close()

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-05-03"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""