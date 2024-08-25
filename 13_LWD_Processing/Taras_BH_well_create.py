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
dialog = tda.dialogAdvanced("New well")
dialog.addTextInput("Well","New well","")
dialog.execDialog()
well_name = dialog.getTextInput("Well")
db.datasetCreate(well_name,"Index","MD","Measured Depth","m",[i for i in xrange(1000)])

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-10-24"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""