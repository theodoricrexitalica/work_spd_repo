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
#проверка существует ли датасет АКЦ и переменной CBL
for well in db.selectedWellList():
	if db.datasetExists(well,"CBL"):
		if db.variableExists(well,"CBL","CBL"):
			continue
		else:
			db.variableCopy(well,"CBL","AP2","CBL","CBL")
			if db.variableCopy(well,"CBL","AP2","CBL","CBL")==True:
				print "Copy AP2 -> CBL;",well, "\r"
			if db.variableCopy(well,"CBL","AP1","CBL","CBL")==True:
				print "Copy AP1 -> CBL;",well, "\r"
			db.variableCopy(well,"CBL","AK","CBL","CBL")
			if db.variableCopy(well,"CBL","AK","CBL","CBL")==True:
				print "Copy AK -> CBL;",well, "\r"
			if db.variableCopy(well,"CBL","AK1","CBL","CBL1")==True:
				print "Copy AK1 -> CBL1;",well, "\r"
			if db.variableCopy(well,"CBL","AK2","CBL","CBL2")==True:
				print "Copy AK2 -> CBL2;",well, "\r"
			db.variableCopy(well,"CBL","AK","CBL","CBL")
			if db.variableCopy(well,"CBL","A1","CBL","CBL1")==True: 
				print "Copy A1 -> CBL1;", "\r"
			if db.variableCopy(well,"CBL","A2","CBL","CBL2")==True:
				print "Copy A2 -> CBL2;", "\r"
	else:
		print "Создайте датасет CBL",well


for well in db.selectedWellList():
##Блок замены семейств и единиц измерения
	db.variableFamilyChange(well,"CBL","PR","Cement Bond Amplitude")
	db.variableFamilyChange(well,"CBL","TP1","Travel Time")
	db.variableFamilyChange(well,"CBL","TP2","Travel Time")
	db.variableFamilyChange(well,"CBL","T1","Travel Time")
	db.variableFamilyChange(well,"CBL","T2","Travel Time")
	db.variableFamilyChange(well,"CBL","CBL","Cement Bond Amplitude")
	db.variableFamilyChange(well,"CBL","CBL1","Cement Bond Amplitude")
	db.variableFamilyChange(well,"CBL","CBL2","Cement Bond Amplitude")
	db.variableUnitChange(well,"CBL","CBL","mV")
	db.variableUnitChange(well,"CBL","CBL1","mV")
	db.variableUnitChange(well,"CBL","CBL2","mV")
	print "Семейства обновлены"

print "Датасет CBL проверен"
##Блок проверки семейств и единиц измерения
	#print "PR family:", db.variableFamily(well,"CBL","PR")
	#print "TP2 family:", db.variableFamily(well,"CBL","TP2")
	#print "CBL unit:",  db.variableUnit(well,"CBL","CBL"),  \
						#db.variableUnit(well,"CBL","CBL1"), \
						#db.variableUnit(well,"CBL","CBL2")

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2014-12-26"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""