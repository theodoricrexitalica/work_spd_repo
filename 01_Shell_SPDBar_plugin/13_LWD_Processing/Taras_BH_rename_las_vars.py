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
	well_prop_list = db.wellPropertyList(well)
	las_list = db.variableList(well,"LAS")
	for i in range(len(well_prop_list)):
		for j in range(len(las_list)):
			if well_prop_list[i] == las_list[j]:
				if db.wellPropertyValue(well,well_prop_list[i]) != "Zero":
					db.variableRename(well,"LAS",las_list[j], db.wellPropertyValue(well,well_prop_list[i]))
					print las_list[j],"--->",db.wellPropertyValue(well,well_prop_list[i])

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-08-25"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""