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
import TechlogPlot as TP
for well in db.selectedWellList():
	db.currentChange("import")
	for importWell in db.wellList():
		db.wellRename(importWell,well)
		importWell=well
		for ds in db.datasetList(importWell):
			for var in db.variableList(importWell,ds,0):
				if var.endswith("r"):
					ds_rep = ds
		db.datasetRename(importWell,ds,"Relog")
	for importWell in db.wellList():
		for ds in db.datasetList(importWell):
			if not ds == "Relog":
				db.datasetRename(importWell,ds,"Log")
	for importWell in db.wellList():
		for importDs in db.datasetList(importWell):
			db.datasetCopy(well,"Relog","import","project")
			db.datasetCopy(well,"Log","import","project")
		db.currentChange("project")
		db.importBufferClose()
	TP.logViewApplyTemplate("User\\Check_Log_Relog",well,0)

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2015-12-31"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""