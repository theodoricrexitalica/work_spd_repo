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
	cmn = "COMMON_05"
	fl_ind = "Fluid_Index"
	zone = "ZONATION"
	fluid = db.variableData(well, cmn, fl_ind)
	md = db.variableData(well, cmn, db.referenceName(well, cmn))
	perm = db.variableLoad(well, cmn, "Perm")
	kh_tvd = db.variableLoad(well, cmn, "KH_tvd_oil")
	step = md[1] - md[0]
	tvdss = db.variableData(well, cmn, "TVDSS")
	print well
	cc_total = 0
	tvdss_net_pay = 0
	perm_total = 0
	kh_tvd_report_total = 0
	if db.variableExists(well, cmn, fl_ind):
		zones = db.variableData(well, zone, "ZONES")
		if zones[-1] == "AS11.2":
			k = 6
			print "AS11.2 target zone"
		else:
			k = 0
		for i in range(k,len(zones)):
			cc = 0
			tvdss_cc = 0
			perm_cc = 0
			indice = db.datasetZoneIndice(well, cmn, zone, zones[i])
			#print zones[i], indice
			for j in range(indice[0],indice[1]):
				if fluid[j] == 1.0:
					cc +=1
					tvdss_cc += (tvdss[j+1]-tvdss[j])
					perm_cc += (tvdss[j+1]-tvdss[j]) * perm[j]
			if round(cc*step,1) > 0:
				cc_total += cc*step
				tvdss_net_pay += tvdss_cc
				kh_tvd_report = kh_tvd[indice[0]] - kh_tvd[indice[1]]
				kh_tvd_report_total +=  kh_tvd_report
				perm_total += perm_cc
				print zones[i], "\t\t\t", "Net pay: md", round(cc*step,0), " m;  tvdss ", \
					 round(tvdss_cc,0), " m; Kh_tvd_oil = ", round(kh_tvd_report,0), " mD*m"

	print "Total: \t\t\t", "Net pay: md", round(cc_total,0), " m;", "tvdss ", \
			 round(tvdss_net_pay,0), " m", "Kh_tvd_oil = ", round(kh_tvd_report_total,0), " mD*m"

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2017-08-27"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""