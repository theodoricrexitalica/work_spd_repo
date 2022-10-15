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
for well in db.wellList():
	for ds in db.selectedDatasetList(well):
		if db.datasetPropertyValue(well,ds,"RECAL") != "1":
#Дублирование IFLO
			db.variableDuplicate(well,ds,"IFLOg","IFLOg_orig")
			db.variableDelete(well,ds,"IFLOg")
			db.variableDuplicate(well,ds,"IFLOw","IFLOw_orig")
			db.variableDelete(well,ds,"IFLOw")
			db.variableDuplicate(well,ds,"IFLOoil","IFLOoil_orig")
			db.variableDelete(well,ds,"IFLOoil")
#Дублирование DFLO
			db.variableDuplicate(well,ds,"DFLOg","DFLOg_orig")
			db.variableDelete(well,ds,"DFLOg")
			db.variableDuplicate(well,ds,"DFLOoil","DFLOoil_orig")
			db.variableDelete(well,ds,"DFLOoil")
			db.variableDuplicate(well,ds,"DFLOw","DFLOw_orig")
			db.variableDelete(well,ds,"DFLOw")
#Переименование DFLO/IFLO
			db.variableRename(well,ds,"IFLOg_orig","DFLOg")
			db.variableRename(well,ds,"DFLOg_orig","IFLOg")
			db.variableRename(well,ds,"IFLOw_orig","DFLOw")
			db.variableRename(well,ds,"DFLOw_orig","IFLOw")
			db.variableRename(well,ds,"IFLOoil_orig","DFLOoil")
			db.variableRename(well,ds,"DFLOoil_orig","IFLOoil")

			db.datasetPropertyChange(well,ds,"RECAL","1","unitless")
			print "Dif/Integ Flow изменено"
		else:
			print "Dif/Integ Flow уже обновлено"
			pass

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-09-02"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""