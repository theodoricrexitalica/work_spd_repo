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
def input_threshold(well):
	import TechlogDialogAdvanced as tda
	list_thresholds = (["High dens flag, Ohm.m","Oil+water flag, Ohm.m", \
						"Non res flag, gAPI","T1, m","T2, m", "GausianSmooth, pnt"])
	list_values_thresholds = [25,8,75,0,0,20]
	list_values_unit = ["Ohm.m","Ohm.m","api","m","m", ""]
	dialog = tda.dialogAdvanced("")
	for i in range(len(list_thresholds)):
		dialog.addDoubleInput(list_thresholds[i],list_thresholds[i],list_values_thresholds[i],0,10000,1,0.1)
	dialog.execDialog()
	final_list_thresholds = []
	for j in range(len(list_thresholds)):
		final_list_thresholds.append(dialog.getDoubleInput(list_thresholds[j]))
	for k in range(len(list_thresholds)):
		db.wellPropertyDelete(well,list_thresholds[k])
		db.wellPropertyChange(well,list_thresholds[k],str(final_list_thresholds[k]),list_values_unit[k])
	db.projectBrowserRefresh()
	print "Граничные значения добавлены"


for well in db.selectedWellList():
	input_threshold(well)

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-10-19"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""