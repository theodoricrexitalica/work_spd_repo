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
def rev_zonation():
	n = 10
	dialog = tda.dialogAdvanced("Revisions")
	list = [i for i in range(1,n)]
	for i in list:
		dialog.addDoubleInput(str(i),"Depth",-9999,0,10000,1,0.1)
		dialog.addTextInput(str(i)+"text","Revision","Rev_",0)
	dialog.execDialog()
	list_depth = []
	list_rev = []
	for i in list:
		if dialog.getDoubleInput(str(i)) != 0 and dialog.getTextInput(str(i)+"text") != "Rev_":
			list_depth.append(dialog.getDoubleInput(str(i)))
			list_rev.append(dialog.getTextInput(str(i)+"text"))
	return list_depth,list_rev


for well in db.selectedWellList():
	depth, zones = rev_zonation()
	db.datasetCreate(well,"REV_ZONE","MD","Measured Depth","m",depth)
	db.variableSave(well,"REV_ZONE","REV_ZONES","Zone Name","unitless",zones)
	db.datasetTypeChange(well,"REV_ZONE","interval")

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-10-29"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""