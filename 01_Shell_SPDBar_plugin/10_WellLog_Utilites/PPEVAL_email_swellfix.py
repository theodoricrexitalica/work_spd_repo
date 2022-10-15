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
import win32com.client
from os import *
import pythoncom
pythoncom.CoInitialize()


### Calculate quick net pay
for well in db.selectedWellList():
	as_top = round(db.variableData(well,"ZONATION","DEPTH")[0],2)
	zone = db.variableData(well,"ZONATION","ZONES")[0]
	print zone,"=",as_top
	cmn = "COMMON_05"
	fl_ind = "Fluid_Index"
	zone = "ZONATION"
	fluid = db.variableData(well, cmn, fl_ind)
	md = db.variableData(well, cmn, db.referenceName(well, cmn))
	step = md[1] - md[0]
	tvdss = db.variableData(well, cmn, "TVDSS")
	print well
	tvdss_net_pay = 0
	if db.variableExists(well, cmn, fl_ind):
		zones = db.variableData(well, zone, "ZONES")
		for i in range(len(zones)):
			cc = 0
			tvdss_cc = 0
			indice = db.datasetZoneIndice(well, cmn, zone, zones[i])
			#print zones[i], indice
			for j in range(indice[0],indice[1]):
				if fluid[j] == 1.0:
					cc +=1
					tvdss_cc += (tvdss[j+1]-tvdss[j])
			if round(cc*step,1) > 0:
				tvdss_net_pay += tvdss_cc
				print zones[i], "\t\t\t", "Net pay: md", round(cc*step,0), " m;  tvdss ", \
					 round(tvdss_cc,0), " m"
### Creating emails for distribution list
	email = win32com.client.Dispatch("Outlook.Application")
#### Creating SwellFix & AS
	zone = db.variableData(well,"ZONATION","ZONES")[0]
	Msg = email.CreateItem(0)
	Msg.To = "Swell fix"
	if well.startswith("US"):
		Msg.Subject = "SwellFix & AS9_" + well
		Msg.Body ="Please RIH casing." + \
		"\nBased on logging data" + \
		"\nTop of " + zone + " = " + str(as_top) +" m MD." + \
		"\nSwellable packer will NOT be installed." + \
		"\n\rPreliminary net pay  ~" + str(round(tvdss_net_pay,1)) + "m , expected ~ m" + \
		"\n\rRegards," + \
		"\nTaras Dolgushin" +\
	 	"\nField Petrophysicist" + \
	 	"\nSub Surface Field Team" + \
		"\nSalym Petroleum Development N.V." + \
		"\nPhone:  +7 495 411 7074 ext.3486" + \
		"\nMobile: +7 932 440 29 29" + \
		"\nE-mail work: SPD-SALYM-SSFT-GE-C@salympetroleum.ru" + \
		"\nE-mail personal: Taras.Dolgushin@salympetroleum.ru"
		Msg.Display()
	else:
		Msg.Subject = "SwellFix & AS10_" + well
		Msg.Body ="Please RIH casing." + \
		"\nBased on logging data" + \
		"\nTop of " + zone + " = " + str(as_top) +" m MD." + \
		"\nSwellable packer will NOT be installed." + \
		"\n\rPreliminary net pay  ~" + str(round(tvdss_net_pay,1)) +  "m , expected ~ m" +\
		"\n\rRegards," + \
		"\nTaras Dolgushin" +\
	 	"\nField Petrophysicist" + \
	 	"\nSub Surface Field Team" + \
		"\nSalym Petroleum Development N.V." + \
		"\nPhone:  +7 495 411 7074 ext.3486" + \
		"\nMobile: +7 932 440 29 29" + \
		"\nE-mail work: SPD-SALYM-SSFT-GE-C@salympetroleum.ru" + \
		"\nE-mail personal: Taras.Dolgushin@salympetroleum.ru"
		Msg.Display()

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-01-03"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""