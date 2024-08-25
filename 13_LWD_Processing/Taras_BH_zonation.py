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
import TechlogDialogAdvanced as tda
#Функция выбора отбивки и названия целевой зоны
def zonation_choice():
	zone_list = ["Cherkashin","AS9.0","AS10","AS11.1","AS11.2","AS11.3.1"]
	zn_list = []
	dialog = tda.dialogAdvanced("Zonation")
	dialog.addDoubleInput("Zone1","Target Zone Depth",0,-10000,10000,1,0.1)
	dialog.addListInput("Zone2","Taget Zone Name",zone_list,0,1)
	dialog.execDialog()
	zn_list.append(round(dialog.getDoubleInput("Zone1"),1))
	zn_name = dialog.getListInput("Zone2")
	zn_names = [zn_name,"TD"]
	return zn_names, zn_list
#Создание датасета ZONATION с копированием данных из Index
def zonation_creation(well,zn_names,zn_list):
	zn = "ZONATION"
	ind = "Index"
	ref_name = db.referenceName(well,ind)
	ref_md = db.variableLoad(well,ind,ref_name)
	zn_list.append(ref_md[-1])
	db.datasetCreate(well,zn,"DEPTH","Measured Depth","m",zn_list)
	db.datasetTypeChange(well,zn,"interval")
	db.variableCopy(well,ind,"TVDSS",zn,"TVDSS","linear")
	db.variableCreate(well,zn,"ZONES",1)
	db.variableSave(well,zn,"ZONES","Zone Name","unitless",zn_names)
	print "Датасет ZONATION создан"
	print "Глубина TD",round(zn_list[-1],0),"м"
#Обновление глубины TD, если ZONATION уже создан
def add_TD_depth(well):
	zn = "ZONATION"
	ind = "Index"
	zn_list = []
	ind_ref_name = db.referenceName(well,ind)
	ind_td = db.variableLoad(well,ind,ind_ref_name)[-1]
	zn_ref_name = db.referenceName(well,zn)
	top_zone_depth = db.variableData(well,zn,zn_ref_name)[0]
	zn_list.append(top_zone_depth)
	zn_list.append(ind_td)
	db.variableSave(well,zn,zn_ref_name,"Measured Depth","m",zn_list)
	db.variableCopy(well,ind,"TVDSS",zn,"TVDSS","linear")
	db.wellPropertyChange(well,"Total_depth",str(round(ind_td,0)),"m")
	db.projectBrowserRefresh()
	print "Глубина TD",round(ind_td,0),"м обновлена"
#Запуск функция для текущей скважины
for well in db.selectedWellList():
	if db.datasetExists(well,"ZONATION"):
		add_TD_depth(well)
	else:
		zn_names, zn_list = zonation_choice()
		zonation_creation(well,zn_names,zn_list)

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-08-24"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""