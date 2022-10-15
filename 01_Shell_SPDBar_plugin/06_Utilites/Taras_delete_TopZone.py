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
for well in db.selectedWellList():
	
	if db.variableData(well,"ZONATION","ZONES")[0]=="TOP_ZONE":
		print "TOP_ZONE найден"
		#db.datasetDuplicate(well,"ZONATION",well,"ZONATION_old")
		db.variableLoad(well,"ZONATION","DEPTH")[1:]
		db.variableLoad(well,"ZONATION","TVDSS")[1:]
		db.variableLoad(well,"ZONATION","ZONES")[1:]
		db.datasetCreate(well,"ZONATION_temp","DEPTH","Measured Depth","m",db.variableLoad(well,"ZONATION","DEPTH")[1:])
		db.variableSave(well,"ZONATION_temp","TVDSS","Reference","m",db.variableLoad(well,"ZONATION","TVDSS")[1:])
		db.variableSave(well,"ZONATION_temp","ZONES","Zone Name","unitless",db.variableLoad(well,"ZONATION","ZONES")[1:])
		db.datasetDelete(well,"ZONATION",1)
		db.datasetTypeChange(well,"ZONATION_temp","interval")
		db.datasetRename(well,"ZONATION_temp","ZONATION")
		db.variableDuplicate(well,"ZONATION","ZONES","ZONES_spr")
		print "TOP_ZONE удален"
	else:
		continue
#for well in db.selectedWellList():
	#db.variableDuplicate(well,"ZONATION","ZONES","ZONES_spr")
	
	
	
	

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2015-03-31"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""