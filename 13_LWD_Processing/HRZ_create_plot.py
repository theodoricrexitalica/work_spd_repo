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
for well in db.selectedWellList():
	id = tp.logViewApplyTemplate("User\HRZ",well,False)
	tp.logViewSetName(id,"-".join(well.split("-")[:3]))
	tvdss_var = [well + ".Index.TVDSS"]
	tvdss_max = int(db.variableData(well, "Index","TVDSS")[-1])
	tp.logViewInsertVariable(id, tvdss_var, 6)
	delta = 10
	tvdss_min = tvdss_max - delta
	tvdss_max =  tvdss_max + 3
	tp.logViewSetAxeLimitTypeByVariable(id, tvdss_var[0],1)
	tp.logViewSetMinMaxUserByVariable(id,tvdss_var[0], tvdss_min, tvdss_max, 1)
	tp.logViewSetLineProperties(id, tvdss_var[0], 2, 1, 2)
	tp.logViewSetVariableColour(id, tvdss_var[0], 0, 190, 0)

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-10-28"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""