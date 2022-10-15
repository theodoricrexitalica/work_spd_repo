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
#os.startfile("C:\Apps\Routine\OIS\OIS_data.xlsx")
os.startfile("C:\Apps\Routine\PLT\%crossflow.xlsx")
os.startfile("C:\Apps\Routine\PLT\Fish.txt")

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-03-04"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""