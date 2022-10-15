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
import TechlogStat as ts
ds = "MAIN"

def TNPH(well):
	neu_list = []
	for i in db.variableList(well,ds):
		if db.variableFamily(well,ds,i) == "Neutron Porosity":
			neu_list.append(i)
	
	neu_avg = ts.average(db.variableData(well,ds,neu_list[0]))
	
	if neu_avg > 1:
		neu_new = []
		neu = db.variableData(well,ds,neu_list[0])
		neu_old = db.variableDuplicate(well,ds,neu_list[0],neu_list[0] + "_old")
		for i in neu:
			neu_new.append(i/100)
	
		db.variableSave(well,ds,neu_list[0],"Neutron Porosity","v/v",neu_new)
		print "TNPH - пересчитана" 
	else: print "TNPH - пересчет не требуется"

def RHOZ(well):
	dens_list = []
	for i in db.variableList(well,ds):
		if db.variableFamily(well,ds,i) == "Bulk Density":
			dens_list.append(i)

	dens_avg = ts.average(db.variableData(well,ds,dens_list[0]))
	
	if dens_avg > 10:
		dens_new = []
		dens = db.variableData(well,ds,dens_list[0])
		dens_old = db.variableDuplicate(well,ds,dens_list[0],dens_list[0] + "_old")
		for i in dens:
			dens_new.append(i/1000)

		db.variableSave(well,ds,dens_list[0],"Bulk Density","g/cm3",dens_new)
		print "RHOZ - пересчитана"
	else: print "RHOZ - пересчет не требуется"

def DLIS(well):
	dlis = "DLIS_08ft"
	if db.datasetExists(well,dlis):
		if not db.variableExists(well,dlis,"SSW") or db.variableExists(well,dlis,"SSW_column4"):
			db.datasetDelete(well,dlis,1)
			print "DLIS удален за ненадобностью"
	else: print "DLIS отсутствует"

for well in db.selectedWellList():
	TNPH(well)
	RHOZ(well)
	DLIS(well)

	

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-03-17"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""