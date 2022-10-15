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
for well in db.selectedWellList():
	ds = "COMMON_05"
	zonation = "ZONATION"
	md = db.variableData(well,ds,db.referenceName(well,ds))
	zones = db.variableData(well,zonation,"ZONES")[-1]
	index = db.variableData(well,ds,"Fluid_Index")
	target_zone_md = db.variableData(well,zonation,db.referenceName(well,"ZONATION"))[-1]
	target_td_md = db.variableData(well,"Index",db.referenceName(well,"Index"))[-1]
	print "Общая мощность",zones,"-TD:",round(target_td_md - target_zone_md,0)
	start_ind= db.datasetZoneIndice(well, ds, zonation, zones)[0]
	stop_ind= db.datasetZoneIndice(well, ds, zonation, zones)[1]
	md_sample_rate = md[-1] - md[-2]
	md_netpay = 0
	for j in range(start_ind,stop_ind):
		if index[j] == 1 or index[j] == 2:
			md_netpay += md_sample_rate
	print "Эффект.мощность в",zones,":",round(md_netpay,0)
	print "Коэфф.качества:",round((md_netpay/(target_td_md - target_zone_md)*100),0),"%"

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-10-28"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""