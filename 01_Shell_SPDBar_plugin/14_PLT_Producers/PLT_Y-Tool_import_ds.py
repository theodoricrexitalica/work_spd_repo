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
import time
for well in db.selectedWellList():
	db.currentChange("import")
	for importWell in db.wellList():
		ds = db.datasetList(importWell)[0]
		db.wellRename(importWell,well)
		importWell=well
		for importDs in db.datasetList(importWell):
			date_f = db.wellPropertyValue(importWell, "DATE")
			#date_b = db.wellPropertyValue(importWell, "DATEB")
			#if not date_b:
				#date_b = db.wellPropertyValue(importWell, "DATB")
			date = date_f.replace(".",".").replace("/",".").replace("-",".")
			date = "".join(date.split(".")[1:])
			if date == "" or len(date)>6:
				print "Проверьте дату работы"
				break
			if len(date) == 4:
				date_new = time.strptime(date, "%m%y")
				plt_name = "PLT_Y_" + time.strftime("%b%y",date_new)
			elif len(date) == 6:
				date_new = time.strptime(date, "%m%Y")
				plt_name = "PLT_Y_" + time.strftime("%b%y",date_new)
			else:
				break
				print "Ошибка в определении даты"
				#plt_name = ""
			db.datasetRename(importWell,ds,plt_name)
			print "Датасет", plt_name, "переименован и скопирован"
			db.wellCopy(importWell,"import","project")
			db.currentChange("project")	
			db.importBufferClose()

import TechlogPlot as tp

def check_consistency(well,ds):
	list_mnemomics = ['CCL', 'CWH_15', 'CWH_45', 'CWH_120', 'CWH_b', 'CWH_f1', 
				  'CWH_f2', 'DEPTH', 'DFLOg', 'DFLOoil', 'DFLOw', 'GR', 
				  'IFLOg', 'IFLOoil', 'IFLOw', 'Nh_15', 'Nh_45', 'Nh_120', 
				  'Nh_b', 'Nh_f1', 'Nh_f2', 'P_15', 'P_45', 'P_120', 'P_b', 
				  'P_f1', 'P_f2', 'RWH_15', 'RWH_45', 'RWH_120', 'RWH_b', 
				  'RWH_f1', 'RWH_f2', 'STD_15', 'STD_45', 'STD_120', 'STD_b',
				  'STD_f1', 'STD_f2', 'T_15', 'T_45', 'T_120', 'T_b', 'T_f1', 'T_f2']
	list_plt_y = []
	well_ds_name = well + "_" + ds
	for var in db.variableList(well,ds):
		list_plt_y.append(var)
	result = set(list_mnemomics) - set(list_plt_y)
	print "В датасете",well_ds_name, "отсутствуют переменные:"
	for var in list(result):
		print var


def plt_y(well):
	if db.datasetExists(well,"PLT_Y"):
		db.datasetDelete(well,"PLT_Y",1)
		print "Предыдущий датасует PLT_Y удален"
	else:
		print "Датасет PLT_Y еще не создан"
	db.datasetDuplicate(well,ds,well,"PLT_Y")
	tp.logViewApplyTemplate("User\\PLT_Y_Tool",well, False)
	print "Диаграмма по датасету", "-".join(well.split("-")[:2]),"-",ds," создана"


for well in db.wellList():
	for ds in db.selectedDatasetList(well):
		plt_y(well)
		check_consistency(well,ds)

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2015-12-31"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""