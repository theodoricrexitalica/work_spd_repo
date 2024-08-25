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
	well_name_clean ="-".join(well.split("-")[:3])
	for ds in db.datasetList(well):
		if ds == "PLT_temp":
			db.datasetDelete(well,ds,1)
			print "Датасет", ds, "удален"
		if ds == "PLT_FINAL":
			db.datasetDelete(well,ds,1)
			print "Датасет", ds, "удален"
		if "PLT_" in ds and "_orig" in ds:
			db.datasetDelete(well,ds,1)
			print "Датасет", ds, "удален"
		if well_name_clean in ds:
			db.datasetDelete(well,ds,1)
			print "Датасет", ds, "удален"

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-12-09"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""