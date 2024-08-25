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
import TechlogDialog as td
import time

ds_com="COMMON_05"
ds_zone="ZONATION"
#top_zone = "AS9.0"
#top_zone = "AS10.0"
#bottom_zone = "AS11.3.1"

for well in db.selectedWellList():
	
	ds_report = "REPORT_SPLIT"
	count = 1
	while db.datasetExists(well, ds_report + "_" + str(count)):
		count += 1
	ds_report_prev= ds_report + "_" + str(count-1)
	#db.variableCopy(well,ds_report_prev,"Flowing",ds_com,"Flowing","linear")
	
	TVDSS = Variable(well, ds_com, "TVDSS")
	Kmerge = Variable(well, ds_com, "K_merge")
	Flowing = Variable(well, ds_com, "Flowing")
	ZONE = db.variableData(well, ds_zone, "ZONES")
	top_zone=ZONE[0]
	bottom_zone=ZONE[-2]

#--- New dataset-------------------------------------------------------------------------------------------------------
	#dlist=db.variableData(well,CDS,"DEPT")
	ds_report = "REPORT_SPLIT"
	count = 1
	while db.datasetExists(well, ds_report + "_" + str(count)):
		count += 1
	ds_report = ds_report + "_" + str(count)
	print ds_report
	myDialog = tda.dialogAdvanced("Parameters")
	plt_list = []
	for ds in db.datasetList(well):
		if ds.startswith("PLT_"):
			plt_list.append(ds)
	myDialog.addListInput("plt_name", "PLT data", plt_list)
	myDialog.addTextInput("plt_type", "PLT type", "1")
	myDialog.addTextInput("log_company", "Logging Company", "TPG")
	myDialog.addTextInput("tool", "Logging tool", "PLT-92")
	if myDialog.execDialog():
		plt_name = myDialog.getListInput("plt_name")
		plt_type = myDialog.getTextInput("plt_type")
		log_company = myDialog.getTextInput("log_company")
		tool = myDialog.getTextInput("tool")
	db.variableCopy(well,plt_name,"Flowing",ds_com,"Flowing")
	
	#check data stop and data start
	#start_date = db.datasetPropertyValue(well, plt_name, "DATEB")
	#if not start_date:
		#start_date = db.datasetPropertyValue(well, plt_name, "PLT Start Date")
	stop_date = db.datasetPropertyValue(well, plt_name, "DATE")
	if not stop_date:
		stop_date = db.datasetPropertyValue(well, plt_name, "PLT Stop Date")
	
	#if not start_date or not stop_date:
	if not stop_date:
		myDialog = tda.dialogAdvanced("PLT date")
		#myDialog.addTextInput("start_date", "PLT Start Date(dd.mm.yy)", start_date)
		myDialog.addTextInput("stop_date", "PLT Stop Date(dd.mm.yy)", stop_date)
	
		if myDialog.execDialog():
			#start_date = myDialog.getTextInput("start_date")
			stop_date = myDialog.getTextInput("stop_date")

#---- %_water creation  --------------------------------------------------------------------------------------
	try:
		start_ind = db.datasetZoneIndice(well, ds_com, ds_zone, top_zone)[0]
		stop_ind = db.datasetZoneIndice(well, ds_com, ds_zone, bottom_zone)[1]
	except:
		td.log("error", "Can't find index for " + str(top_zone) + " or " + str(bottom_zone) + ". Please check your data")
		continue
	kmerge_c = [0]*TVDSS.size()
	kmerge_pr = 0
	for i in xrange(stop_ind - 1, start_ind - 1, -1):
		tvdss = TVDSS.value(i)
		kmerge = Kmerge.value(i)
		flow = Flowing.value(i)
		if kmerge > 0 and flow > 0:
			kmerge_c[i] = kmerge_pr + kmerge*(tvdss - TVDSS.value(i-1))
			kmerge_pr = kmerge_c[i]
		else:
			kmerge_c[i] = kmerge_pr
	kmerge_sum = max(kmerge_c)
	
	water = [MissingValue]*TVDSS.size()
	for i in xrange(start_ind, stop_ind):
		water[i] = kmerge_c[i]*100/kmerge_sum
	db.variableSave(well, ds_com, "%_water", "Integrated Water Flow", "%", water)
	db.variableSave(well, ds_com, "%_oil", "Integrated Oil Flow", "%", [0]*TVDSS.size())

#-----Properties delete----------------------------------------------------------------------------------------------
	for p in db.datasetPropertyList(well, plt_name):
		db.datasetPropertyDelete(well,plt_name, p)
	td.log("information", plt_name + " properties have been deleted")

#-----QTZT------------------------------------------------------------------------------------------------------------
	qtzt_values = db.variableData(well, plt_name, 'QTZT')
	maxq = max(qtzt_values)
	td.log("information", 'max(QTZT) = ' + str(maxq))

#----New dataset and new properties for PLT dataset-------------------------------------------------------------
	db.datasetCreate(well, ds_report, "DEPT", "Measured Depth", "m", db.variableData(well, ds_com, db.referenceName(well, ds_com)))
	db.datasetPropertyChange(well, plt_name, "Well type", "Injector", "", "Well type @ interpretation date")
	db.datasetPropertyChange(well, ds_report, "Well type", "Injector", "", "Well type @ PLT date")
	current_date = time.strftime("%d.%m.%y", time.localtime(time.time()))
	db.datasetPropertyChange(well, ds_report, "Date", current_date, "", "Interpretation date")
	#db.datasetPropertyChange(well, plt_name, "PLT Start Date", start_date, "", "PLT Start Date")
	db.datasetPropertyChange(well, plt_name, "PLT Stop Date", stop_date, "", "PLT Stop Date")
	db.datasetPropertyChange(well, ds_report, "Trigger", "PLT", "", "PLT; BSW; New perforations; Analysis")
	db.datasetPropertyChange(well, plt_name, "PLT type", plt_type, "", "PLT type")
	db.datasetPropertyChange(well, ds_report, "Q", str(maxq), "m3", "Production or Injection rate during PLT job")
	db.datasetPropertyChange(well, plt_name, "Q", str(maxq), "m3", "Production or Injection rate during PLT job")
	db.datasetPropertyChange(well, ds_report, "WC", "", "%", "BSW during PLT job")
	db.datasetPropertyChange(well, plt_name, "WC", "", "%", "BSW during PLT job")
	db.datasetPropertyChange(well, ds_report, "Logging Company", log_company, "", "Contractor Name")
	db.datasetPropertyChange(well, plt_name, "Logging Company", log_company, "", "Contractor Name")
	db.datasetPropertyChange(well, ds_report, "Tool", tool, "", "Logging tool")
	db.datasetPropertyChange(well, ds_report, "Comments", plt_name, "", "Any operational comments. Print No if there is no any")
	db.variableCopy(well, ds_com, "PERF_FINAL", ds_report, "PERF_FINAL")
	db.variableCopy(well, ds_com, "Flowing", ds_report, "Flowing")
	db.variableCopy(well, ds_com, "%_water", ds_report, "%_water")
	db.variableCopy(well, ds_com, "%_oil", ds_report, "%_oil")
	db.variableCopy(well, ds_com, "PERF_FINAL", plt_name, "PERF_FINAL")
	db.variableCopy(well, ds_com, "Flowing", plt_name, "Flowing")
	db.variableCopy(well, ds_com, "%_water", plt_name, "%_water")
	db.variableDelete(well, ds_com, "%_water")
	db.variableDelete(well, ds_com, "%_oil")

__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""