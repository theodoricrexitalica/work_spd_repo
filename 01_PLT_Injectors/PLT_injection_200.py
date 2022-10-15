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
import time
import TechlogDialog as td
ids="Index"
ds_com = "COMMON_05"
def REN(well, ds, v, Fam, Uni):
	db.variableFamilyChange(well,ds,v,Fam)
	db.variableUnitChange(well,ds,v,Uni)
#Load dataset from import buffer to selected well
for well in db.selectedWellList():
	db.currentChange("import")
	exitStatus = True
	for well_import in db.wellList():
		ds = db.datasetList(well_import)[0]
		date_f = db.wellPropertyValue(well_import, "DATE")
		date_b = db.wellPropertyValue(well_import, "DATEB")
		if not date_b:
			date_b = db.wellPropertyValue(well_import, "DATB")
		date = date_f.replace(".","").replace("/","")
		try:
			date_new = time.strptime(date, "%d%m%Y")
			plt_name = "PLT_" + time.strftime("%b%y",date_new)
		except:
			plt_name = ""
		db.wellRename(well_import, well)
		if db.wellCopy(well, "import", "project"):
			exitStatus = False
	if exitStatus:
		td.log("error","Load data error. Please check your input data")
		continue
	db.currentChange("project")
	db.importBufferClose()
	db.wellLock(well)
	
	myDialog = tda.dialogAdvanced("Parameters")
	if not plt_name:
		myDialog.addTextInput("plt_name", "PLT DS Name", "PLT_MmmYY")
	myDialog.addDoubleInput("rate", "Injection Rate, m3/d", 0,0,10000,0,1)
	if myDialog.execDialog():
		if not plt_name:
			plt_name=(myDialog.getTextInput("plt_name"))
		rate=(myDialog.getDoubleInput("rate"))
	db.variableCopy(well,ids,"TVD",ds,"TVD")
	DEPT = Variable(well,ds,db.referenceName(well,ds))
	TVD = Variable(well,ds,"TVD")
	Tgeo = Variable(well,ds,"WTEP_G", "Natural Temperature","degC")
	datasetSize=TVD.size()
#-------WTEP_G---------------------------------------------------------------------------------------------------------------------------------------
	for i in xrange(datasetSize):
		tvd=TVD.value(i)
		tgeo=tvd*3.5/100
		Tgeo.setValue(i,tgeo)
	Tgeo.save()
	db.variableDelete(well,ds,"TVD")	
#-------Variables rename------------------------------------------------------------------------------------------------------------------------------
	min_ind = []
	for var in db.variableList(well,ds):
		#rename reference variable
		if var == db.referenceName(well,ds) and var != "DEPT":
			db.variableRename(well, ds, var, "DEPT")
		elif ("DFLO" in var) or ("differencial".lower() in db.variableDescription(well, ds, var).lower()):
			REN(well, ds, var, "Incremental Flow Rate", "%")
			db.variableRename(well, ds, var, "QTZIP")
		elif ("IFLO" in var) or ("integral".lower() in db.variableDescription(well, ds, var).lower()):
			REN(well, ds, var, "Cumulative Flow Rate","%")
			db.variableRename(well, ds, var, "QTZTP")
		elif var.startswith("Nl_"):
			REN(well,ds,var,"Noise","kHz")
			db.variableRename(well, ds, var, var.upper())
		elif var.startswith("P_"):
			REN(well, ds, var, "Borehole Pressure", "atm")
			db.variableRename(well, ds, var, var.replace("P", "WPRE").upper())
		elif var.startswith("T_"):
			REN(well,ds,var,"Borehole Temperature","degC")
			db.variableRename(well, ds, var, var.replace("T", "WTEP").upper())
		elif "GR" in var:
			REN(well,ds,var,"PLT Gamma Ray","uR/h")
			db.variableRename(well, ds, var, "GR_CH")
		elif var.startswith("CCL"): REN(well, ds, var, "Casing Collar Locator","CU")
		elif not var.isupper():
			db.variableRename(well, ds, var, var.upper())
#Алгоритм переименования на базе версии переменной
		#ver = db.variableVersion(var)
		#if ver > 2 and not (ver in min_ind):
			#min_ind.append(ver)
	#min_ind.sort()
	#for var in db.variableList(well, ds):
		#ver = db.variableVersion(var)
		#if ver in min_ind:
			#db.variableRename(well, ds, var, var.replace(str(ver), "S" + str(min_ind.index(ver) + 0)))
#Алгоритм переименования на базе имени переменной
	var_rename = db.variableList(well,ds)
	for i in var_rename:
		if "_WI" in i and "WI_2" not in i:
			db.variableRename(well,ds,i,i + "_1")
		elif "_15" in i:
			db.variableRename(well,ds,i,i.split("_")[0] + "_1")
		elif "_45" in i:
			db.variableRename(well,ds,i,i.split("_")[0] + "_2")
		elif "_120" in i:
			db.variableRename(well,ds,i,i.split("_")[0] + "_3")
#--------Resampling--------------------------------------------------------------------------------------------------------------------------------------------
	DEPT = Variable(well, ds, "DEPT")
	stop = round(max(DEPT.values()))
	start = round(min(DEPT.values()))
	size = int(round((stop - start)/0.05, 0))
	new_ref = []
	for i in xrange(size):
		new_ref.append(start + i*0.05)
	if db.datasetExists(well, plt_name):
		db.datasetDelete(well, plt_name)
	db.datasetCreate(well, plt_name, "DEPT", "Measured Depth", "m", new_ref)
	db.datasetPropertyChange(well, plt_name, "DATEB", date_b)
	db.datasetPropertyChange(well, plt_name, "DATE", date_f)
	vlist = db.variableList(well, ds)
	for var in vlist:
		if var != "DEPT":
			db.variableCopy(well, ds, var, plt_name, var)
	#db.datasetDelete(well, ds)
#--------QTZT---------------------------------------------------------------------------------------------------------------------------------------------------
	iflo = db.variableData(well, plt_name, 'QTZTP')
	qflo = db.variableData(well, plt_name, 'QTZT')
	maxflo = max(iflo)
	for i in xrange(size):
		if iflo[i] != MissingValue:
			qflo[i] = iflo[i] * rate/maxflo
	db.variableSave(well, plt_name,'QTZT', 'Cumulative Flow Rate', 'm3', qflo)
#--------PERF_FINAL-------------------------------------------------
	db.variableCopy(well, ds_com, "PERF_FINAL", plt_name)
	db.variableCopy(well, ds_com, "Flowing", plt_name)
	db.variableTypeChange(well, plt_name, "Flowing","BlockedCurve")
	db.projectBrowserRefresh()
	td.log("information", "Well " + well + " dataset " + plt_name + " has been created")
	db.datasetPropertyChange(well, plt_name, "Q", str(rate), "m3", \
	"Production or Injection rate during PLT job")
#удаление мусорных датасетов PLT, PLT_temp
	if db.datasetExists(well,"PLT"):
		db.datasetDelete(well,"PLT",1)
	else:
		pass
	if db.datasetExists(well,"PLT_temp"):
		db.datasetDelete(well,"PLT_temp",1)
	else:
		pass

__author__ = """Maria PEREZHOGINA (MPerezhogina)"""
__date__ = """2012-03-22"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""