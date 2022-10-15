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
my_dialog = tda.dialogAdvanced("Splits")
for well in db.wellList():
	for ds in db.selectedDatasetList(well):
		ds = "PLT_Y_ZONE"
		zones = db.variableData(well,"ZONATION","ZONES")
		md = db.variableData(well,ds, db.referenceName(well,ds))
		split_g = db.variableData(well,ds,"Split_g")
		split_o = db.variableData(well,ds,"Split_o")
		split_w = db.variableData(well,ds,"Split_w")
		for i in range(len(md)):
			my_dialog.addTextInput("oil" + str(i),"Oil " + str(zones[i]),split_o[i],0)
		for i in range(len(md)):
			my_dialog.addTextInput("water" + str(i),"Water " + str(zones[i]),split_w[i],0)
		for i in range(len(md)):
			my_dialog.addTextInput("gas" + str(i),"Gas " + str(zones[i]),split_g[i],0)
		my_dialog.execDialog()
		split_o_new = []
		split_w_new = []
		split_g_new = []
		for i in range(len(md)):
			split_o_new.append(my_dialog.getTextInput("oil" + str(i)))
			split_w_new.append(my_dialog.getTextInput("water" + str(i)))
			split_g_new.append(my_dialog.getTextInput("gas" + str(i)))
		db.variableSave(well,ds,"Split_o","Other","%",split_o_new)
		db.variableSave(well,ds,"Split_w","Other","%",split_w_new)
		db.variableSave(well,ds,"Split_g","Other","%",split_g_new)

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-12-05"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""