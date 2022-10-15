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
import time
template = "User\PLT_500"

##Load dataset from import buffer to selected well
for well in db.selectedWellList():
	db.currentChange("import")
	exitStatus = True
	for well_import in db.wellList():
		ds = db.datasetList(well_import)[0]
		date_f = db.wellPropertyValue(well_import, "DATE")
		date = date_f.replace(".","").replace("/","")
		date_new = time.strptime(date, "%d%m%Y")
		db.datasetRename(well_import,ds,"PLT500_"+time.strftime("%b%y",date_new))
		db.wellRename(well_import, well)
		if db.wellCopy(well, "import", "project"):
			exitStatus = False
	if exitStatus:
		td.log("error","Load data error. Please check your input data")
		continue
	db.currentChange("project")
	db.importBufferClose()
	db.wellLock(well)

##Counter to find last dataset
	plt_data = []
	for ds in db.datasetList(well):
		if ds.startswith("PLT500_"):
			#print ds
			try:
				date = time.strptime(ds.split("_")[-1], "%b%y")
				plt_data.append(date)
			except:
				continue
	plt_data.sort()
	
	ds_name_list = []
	for pdata in plt_data:
		
		date_str = time.strftime("%b%y",pdata)
		ds_name = "PLT500_" + date_str
		ds_name_list.append(ds_name)
	ds=ds_name_list[-1]

__author__ = """Maria PEREZHOGINA (MPerezhogina)"""
__date__ = """2012-03-22"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""