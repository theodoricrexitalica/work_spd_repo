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
zone_temp = "ZONATION_temp"
ind = "Index"
ds_zone = "ZONATION"
tvdss = "TVDSS"
for well in db.selectedWellList():
#Объявление переменных
	ref_var_td = db.referenceName(well,ind)
	td = db.variableData(well, ind,ref_var_td)[-1]
	print "Забой скважины:",round(td,0),"м"
	ref_var_zone = db.referenceName(well,ds_zone)
	zone = db.variableData(well,ds_zone,"ZONES")
#Поиск переменной TD в ZONES
	for i in range(len(zone)):
		if zone[i] == "TD":
			td_index = i
		else:
			td_index = -1
#Запуск процедуры добавления TD
	if zone[td_index] != "TD":
		print "Строка TD добавлена"
		md_zone = db.variableData(well,ds_zone,ref_var_zone)
		md_zone.append(td)
		zone.append("TD")
		db.datasetCreate(well,zone_temp,ref_var_zone,"Measured Depth","m",md_zone)
		db.variableSave(well,zone_temp,"ZONES","Zone Name","unitless",zone)
		db.variableResampling(well,ind,tvdss,zone_temp,tvdss,"linear anti-aliasing",0.1524)
		db.datasetDelete(well,"ZONATION",1)
		db.datasetTypeChange(well,"ZONATION_temp","interval")
		db.datasetRename(well,"ZONATION_temp","ZONATION")
	else:
		print "Строка TD уже существует"
		pass
	
	

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-03-05"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""