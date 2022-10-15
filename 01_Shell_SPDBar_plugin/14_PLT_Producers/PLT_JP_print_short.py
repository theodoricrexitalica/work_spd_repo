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
import TechlogPlot as tp

for well in db.wellList():
	for ds in db.selectedDatasetList(well):
		if db.datasetExists(well,"JP_PLT"):
			db.datasetDelete(well,"JP_PLT",1)
			print "Предыдущий датасует JP_PLT удален"
		else:
			print "Датасет JP_PLT еще не создан"
		db.datasetDuplicate(well,ds,well,"JP_PLT")
		tp.logViewApplyTemplate("User\\PLT_JP",well, False)
		print "Диаграмма по датасету", "-".join(well.split("-")[:2]),"-",ds," создана"

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-09-06"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""