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
path = r"C:\Apps\Routine\PP_eval\HRZ_plots"
for well in db.selectedWellList():
	well_name = "-".join(well.split("-")[:3])
	id = tp.logViewGetIdByName(well_name)
	tp.printToFile(id,"Custom",".png",path + "\\" + well_name,0,0,0,-1,0,-1,-1,False,600)

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-10-28"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""