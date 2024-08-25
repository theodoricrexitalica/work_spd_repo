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

def target_md(well):
	target_zone_md = db.variableData(well,"ZONATION",db.referenceName(well,"ZONATION"))[-1]
	target_td_md = db.variableData(well,"Index",db.referenceName(well,"Index"))[-1]
	result = target_td_md - target_zone_md
	return result


def netpay_tvdss(start_ind,stop_ind,ind1,ind2):
	top_np_tvd = []
	bot_np_tvd = []
	for j in range(start_ind,stop_ind):
		if index[j] != ind1 and index[j+1] == ind1:
			top_np_tvd.append(tvdss[j+1])
		if index[j] == ind1 and index[j+1] != ind1:
			bot_np_tvd.append(tvdss[j])
	for j in range(start_ind,stop_ind):
		if index[j] != ind2 and index[j+1] == ind2:
			top_np_tvd.append(tvdss[j+1])
		if index[j] == ind2 and index[j+1] != ind2:
			bot_np_tvd.append(tvdss[j])
	list_np_tvdss = []
	for i in range(len(top_np_tvd)):
		list_np_tvdss.append(bot_np_tvd[i] - top_np_tvd[i])
	return round(ts.sum(list_np_tvdss),2)


def index_stat(start_ind,stop_ind,ind1,ind2):
	phi_zones = []
	swws_zones = []
	md_netpay = 0
	for j in range(start_ind,stop_ind):
		if index[j] == ind1 or index[j] == ind2:
			phi_zones.append(phi[j])
			swws_zones.append(swws[j])
			md_netpay += md_sample_rate
	if ts.average(phi_zones) == MissingValue: print zones[i],",", \
											  netpay_tvdss(start_ind,stop_ind,ind1,ind2), ",", \
											  round(md_netpay,1), ":", 0, ":", 0
	else: print zones[i],",", \
		  netpay_tvdss(start_ind,stop_ind,ind1,ind2), ",",\
		  round(md_netpay,0), ",", \
		  round(ts.average(phi_zones),2),",", \
		  round(1 - ts.average(swws_zones),2), "\r"
	return round(md_netpay,0)


def zone_ind(zones):
	try:
		START_ind= db.datasetZoneIndice(well, ds, zonation, zones)[0]
		STOP_ind= db.datasetZoneIndice(well, ds, zonation, zones)[1]
	except TypeError:
		print zones,": Нет данных"
		pass
	return START_ind,STOP_ind


for well in db.selectedWellList():
	print well
	ds = "COMMON_05"
	zonation = "ZONATION"
	md = db.variableData(well,ds,db.referenceName(well,ds))
	if db.variableExists(well,ds,"TVDSS"):
		#print "TVDSS присутствует в COMMON_05"
		tvdss = db.variableData(well,ds,"TVDSS")
	else:
		db.variableCopy(well,"Index","TVDSS",ds,"TVDSS","anti-aliasing")
		#print "TVDSS скопировано в COMMON_05"
		tvdss = db.variableData(well,ds,"TVDSS")
	zones = db.variableData(well,zonation,"ZONES")
	index = db.variableData(well,ds,"Fluid_Index")
	phi = db.variableData(well,ds,"Porden")
	swws = db.variableData(well,ds,"SWWS")
	md_sample_rate = md[-1] - md[-2]
	#print "Sample rate:", round(md_sample_rate,2)

	print "Продуктивная часть"
	print "Zone, np_tvd, np_md, Phi, SH"
	for i in range(len(zones)):
		try:
			START_ind = zone_ind(zones[i])[0]
			STOP_ind = zone_ind(zones[i])[1]
		except NameError:
			pass
		try:
			index_stat(START_ind,STOP_ind,1,2)
		except NameError:
			pass
	hrz_quality = index_stat(START_ind,STOP_ind,1,2)/target_md(well)
	#print "HRZ quality:", round(hrz_quality*100,0),"%"
	print ""
	print "Непродуктивная часть"
	print "Zone, np_tvd, np_md, Phi, SH"
	for i in range(len(zones)):
		try:
			START_ind = zone_ind(zones[i])[0]
			STOP_ind = zone_ind(zones[i])[1]
		except NameError:
			pass
		try:
			index_stat(START_ind,STOP_ind,3,4)
		except NameError:
			pass

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-10-20"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""