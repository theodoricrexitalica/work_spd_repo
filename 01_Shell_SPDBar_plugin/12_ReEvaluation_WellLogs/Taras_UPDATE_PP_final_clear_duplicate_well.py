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
ds_min_list = (['COMMON_05',
				'deviation', 
				'DLIS_08ft', 
				'Index', 
				'MAIN', 
				'ZONATION', 
				'ZONATION_PETREL'])
ds_list_del = []
for well in db.selectedWellList():
	if not db.wellExists(well + "_orig"):
		db.wellDuplicate(well,well + "_orig")
		print "Скважина продублирована"
	else:
		print "Скважина уже есть"
		pass
	for ds in db.datasetList(well):
		if ds not in ds_min_list:
			ds_list_del.append(ds)
	print "Список на удаление создан"

for well in db.selectedWellList():
	for ds in ds_list_del:
		db.datasetDelete(well,ds)
	print "Скважина очищена"

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-03-08"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""