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
import TechlogPlot as tp
cbl = "CBL"
for well in db.selectedWellList():
	if db.datasetExists(well,cbl):
		if db.variableExists(well,cbl,"BI"):
			id = tp.logViewApplyTemplate("User\PPeval_CBL_BI",well,0)
			print "User\PPeval_CBL_BI"
		elif db.variableExists(well,cbl,"ALFK"):
			id = tp.logViewApplyTemplate("User\PPeval_CBL_ALFK",well,0)
			print "User\PPeval_CBL_ALFK"
		elif db.variableExists(well,cbl,"CMT"):
			id = tp.logViewApplyTemplate("User\PPeval_CBL_CMT",well,0)
			print "User\PPeval_CBL_CMT"
	tp.logViewSetName(id,well)

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2017-07-07"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""