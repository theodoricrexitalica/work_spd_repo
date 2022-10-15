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
import time
import TechlogDialogAdvanced as tda
from FUNLIB import *

for well in db.selectedWellList():
	db.currentChange("import")
	#exitStatus = True
	for importWell in db.wellList():
		ds = db.datasetList(importWell)[0]
		print ds
		db.wellRename(importWell,well)
		importWell=well
		print well

		for importDs in db.datasetList(importWell):
			db.datasetRename(importWell,importDs,"CBL")
			db.datasetCopy(well,"CBL","import","project")
		db.currentChange("project")
		db.importBufferClose()

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2013-06-08"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""