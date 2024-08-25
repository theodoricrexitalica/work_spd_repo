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
def check_var(well,ds,var):
	if db.variableExists(well,ds,var):
		result = 1
	else:
		print "Переменная",var,"отсутствует"
		result = 0
	return result

for well in db.selectedWellList():
	if db.datasetExists(well, "COMMON_05"):
		print "COMMON_05 сущесвует"
		pass
	else:
		if db.datasetExists(well,"MAIN"):
			ds = "MAIN"
			if check_var(well,ds,"RHOZ") == False:
				db.variableRename(well,ds,"RHOB","RHOZ")
				db.variableFamilyChange(well,ds,"RHOZ","Bulk Density")
				db.variableUnitChange(well,ds,"RHOZ","g/cm3")
				print "Переменная RHOZ создана"
			if check_var(well,ds,"TNPH") == False:
				db.variableRename(well,ds,"TRNP","TNPH")
				db.variableFamilyChange(well,ds,"TNPH","Neutron Porosity")
				db.variableUnitChange(well,ds,"TNPH","v/v")
				print "Переменная TNPH создана"
			for var in db.variableList(well,ds):
				if var.startswith("Z"):
					db.variableFamilyChange(well,ds,var,"Array Resistivity")
					db.variableUnitChange(well,ds,var,"ohm.m")
					print "Переменные группы Z оформлены"
			if db.variableExists(well,ds,"Z60") and db.variableExists(well,ds,"Z90"):
				z60 = db.variableData(well,ds,"Z60")
				z90 = db.variableData(well,ds,"Z90")
				func = lambda x,y: ( x + y ) / 2
				rt = map(func,z60,z90)
				db.variableSave(well,ds,"RT","Formation Resistivity","ohm.m",rt,1,"float")
				print "Переменная RT создана"
			db.datasetDuplicate(well,"MAIN",well,"COMMON_05")
			print "Датасет COMMON_05 создан"
			db.variableCopy(well,"Index","TVDSS","COMMON_05","TVDSS","anti-aliasing","project","project",-1,0)
			print "Переменная TVDSS скопирована в COMMON_05"	
		else:
			print "Датасет MAIN отсутствует"


#Запуск основного рассчетного скрипта в AWI-оболочке
for well in db.selectedWellList():
	index = db.objectTypeList().index('PythonScript')
	object_num = db.objectCreate(index,"PPEVAL_Pad13","user")

	

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-10-10"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""