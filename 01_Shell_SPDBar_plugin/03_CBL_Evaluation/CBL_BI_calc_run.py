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
index = db.objectTypeList().index('PythonScript')
db.objectOpen(index,"CBL_BI_calc","user")

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2017-07-05"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""