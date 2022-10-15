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
#index = db.objectTypeList().index('PythonScript')
#for well in db.wellList():
	#for ds in db.selectedDatasetList(well):
		#object_num = db.objectCreate(index,"Taras_CBL_Bond_Index","user")
		#db.addDataSetForAWI(object_num,well,ds,0)
		#db.objectWorkflowLayoutTemplateChange("User\CBL_Bond_Index",1)
		
index = db.objectTypeList().index('PythonScript')
for well in db.selectedWellList():
	ds = "CBL"
	object_num = db.objectCreate(index,"Taras_CBL_Bond_Index","user")
	db.addDataSetForAWI(object_num,well,ds,0)
	db.objectWorkflowLayoutTemplateChange("User\CBL_Bond_Index",1)


__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-12-03"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""