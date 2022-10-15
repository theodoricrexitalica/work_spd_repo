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
import os
import webbrowser

def folder_path(well):
	path = r"C:\Apps\Routine\PLT" + "\\" + "-".join(well.split("-")[:2])
	if os.path.exists(path) == True:
		print "Well folder is exist"
		pass
	else:
		os.mkdir(path)
		print "Well folder is done"
	return(path)
	
for well in db.selectedWellList():
	path = folder_path(well)
	webbrowser.open(path)
#удаление мусорных датасетов PLT, PLT_temp
	if db.datasetExists(well,"PLT"):
		db.datasetDelete(well,"PLT",1)
	else:
		pass
	if db.datasetExists(well,"PLT_temp"):
		db.datasetDelete(well,"PLT_temp",1)
	else:
		pass

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-03-02"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""