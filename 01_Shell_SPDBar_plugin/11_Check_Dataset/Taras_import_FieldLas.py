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
		ds = db.datasetList(importWell)[0]
		db.wellRename(importWell,well)
		importWell=well
		for importDs in db.datasetList(importWell):
			db.datasetRename(importWell,importDs,"MAIN_3hr")
			db.datasetCopy(well,"MAIN_3hr","import","project")
		db.currentChange("project")
		db.importBufferClose()
	if "KNG" in well:
		TP.logViewApplyTemplate("User\\Check_MAIN_3hr_KNG",well,0)
	elif "PEX" in well:
		TP.logViewApplyTemplate("User\\Check_MAIN_3hr_SLB",well,0)
		

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2015-12-31"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""