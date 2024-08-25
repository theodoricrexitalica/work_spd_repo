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
	index = db.objectTypeList().index("PythonScriptAWI")
	script = db.objectOpen(index, '..\PythonScripts\\PPEVAL_MAIN_AWI_psv1.py', "User", 0, well)

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-08-28"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""