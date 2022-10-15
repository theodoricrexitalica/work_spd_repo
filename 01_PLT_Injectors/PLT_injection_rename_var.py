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
def rename2015(well,ds):
	db.datasetDuplicate(well,ds,well,ds + "_orig")
	for var in db.variableList(well,ds):
		if var.endswith("_S2"):
			db.variableRename(well,ds,var,var.split("_")[0] + "_1")
		elif var.endswith("_S3"):
			db.variableRename(well,ds,var,var.split("_")[0] + "_2")
		elif var.endswith("_S4"):
			db.variableRename(well,ds,var,var.split("_")[0] + "_3")
		elif var.endswith("WI_S1"):
			db.variableRename(well,ds,var,var.split("_")[0] + "_WI_2")
		elif var.endswith("WI"):
			db.variableRename(well,ds,var,var.split("_")[0] + "_WI_1")

def rename2012(well,ds):
	db.datasetDuplicate(well,ds,well,ds + "_orig")
	for var in db.variableList(well,ds):
		if var.endswith("WTEP"):
			db.variableRename(well,ds,var,var + "_WI")
		if var.endswith("_S1"):
			db.variableRename(well,ds,var,var.split("_")[0] + "_1")
		elif var.endswith("_S2"):
			db.variableRename(well,ds,var,var.split("_")[0] + "_2")
		elif var.endswith("_S3"):
			db.variableRename(well,ds,var,var.split("_")[0] + "_3")
		elif var.endswith("WI"):
			db.variableRename(well,ds,var,var.split("_")[0] + "_WI_1")
		#elif var.endswith("_2"):
			#db.variableRename(well,ds,var,var.split("_")[0] + "_WI_2")


for well in db.wellList():
	for ds in db.selectedDatasetList(well):
		for var in db.variableList(well,ds):
			if var.endswith("WTEP_S4"):
				rename2015(well,ds)
				print "Переменные",var,"в датасете исправлены"
			elif var.endswith("WTEP_S1"):
				rename2012(well,ds)
				print "Переменные", var, "в датасете исправлены"
			elif var.endswith("WTEP_S1") and var.endswith("WTEP_S4"):
				print "Проверьте датасет вручную"

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-12-09"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""