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


def import_ds(well):
	db.currentChange("import")
	for importWell in db.wellList():
		ds = db.datasetList(importWell)[0]
		db.wellRename(importWell,well)
		importWell=well
		for importDs in db.datasetList(importWell):
			date = ds.split("-")[5] + ds.split("-")[6]
			date_new = time.strptime(date, "%m%Y")
			jp_plt_name = "JP_PLT_" + time.strftime("%b%y",date_new)
			db.datasetRename(importWell,ds,jp_plt_name)
			print "Датасет", jp_plt_name, "переименован и скопирован"
			db.wellCopy(importWell,"import","project")
			db.currentChange("project")	
			db.importBufferClose()
	return jp_plt_name
			
			
def check_consistency(well,ds):
	list_mnemomics = ['CCL', 'DEPTH', 'GR', 'GR_b',
					  'CWH_1', 'CWH_2', 'CWH_3', 'CWH_b', 'CWH_f', 
					  'DFLO', 'DFLOoil', 'DFLOw', 'AFLO', 'IFLOoil', 'IFLOw',
					  'P_1', 'P_2', 'P_3', 'P_b', 'P_f',
					  'RWH_1', 'RWH_2', 'RWH_3', 'RWH_b', 'RWH_f', 
					  'STD_1', 'STD_2', 'STD_3', 'STD_b', 'STD_f',
					  'T_1', 'T_2', 'T_3', 'T_b', 'T_f']
	list_jp_plt = []
	well_ds_name = well + "_" + ds
	for var in db.variableList(well,ds):
		list_jp_plt.append(var)
	result = set(list_mnemomics) - set(list_jp_plt)
	print "В датасете",well_ds_name, "отсутствуют переменные:"
	for var in list(result):
		print var


for well in db.selectedWellList():
	jp_plt_name = import_ds(well)
	check_consistency(well,jp_plt_name)

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2015-12-31"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""