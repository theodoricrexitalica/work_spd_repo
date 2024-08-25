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
	ds = "LAS"
	thres_dens = float(db.wellPropertyValue(well,"High dens flag, Ohm.m"))
	thres_oilwater = float(db.wellPropertyValue(well,"Oil+water flag, Ohm.m"))
	thres_non_res = float(db.wellPropertyValue(well,"Non res flag, gAPI"))
	res = db.variableData(well,"LAS","RES_PH2")
	gr = db.variableData(well,"LAS","GR")
	md = db.variableData(well,"LAS",db.referenceName(well,"LAS"))
	md_zone = db.variableData(well,"ZONATION",db.referenceName(well,"ZONATION"))
	if db.variableExists(well,ds,"cut"):
		print "Cut существует"
	else:
		cut = []
		for i in range(len(md)):
			cut.append(MissingValue)
		db.variableSave(well,ds,"cut","General Flag","unitless",cut)
		print "Cut создан"
	cut = db.variableData(well,ds,"cut")
	index_flag = []
	res_count = 0
	oil_water_count = 0
	non_res_count = 0
	ind1 = md.index(md_zone[0])
	ind2 = res.index(-9999.0,ind1)
	for i in range(len(md)):
		index_flag.append(MissingValue)
	for i in range(ind1,ind2):
		if  res[i] <= thres_dens and \
			res[i] >= thres_oilwater and \
			gr[i] <= thres_non_res:
			index_flag.pop(i)
			index_flag.insert(i,1)
			res_count += md[1] - md[0]
		elif res[i] <= thres_oilwater and \
			 gr[i] <= thres_non_res:
			 index_flag.pop(i)
			 index_flag.insert(i,2)
		elif res[i] <= (thres_oilwater-1) and \
			 gr[i] <= thres_non_res:
			 index_flag.pop(i)
			 index_flag.insert(i,2)
		if  cut[i] == 1:
			index_flag.pop(i)
			index_flag.insert(i,MissingValue)
	db.variableSave(well,ds,"Index_flag","Saturation_Index","unitless",index_flag)
	print "Index_flag посчитан"

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-12-12"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""