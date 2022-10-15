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
	wellName=well.split("-")[0]+"-"+well.split("-")[1]
	for var in db.variableList(well,"ZONATION"):
		if db.variableFamily(well,"ZONATION",var)=="Zone Name" and var!="ZONES" and var!="ZONE":
			ok=db.variableDelete(well,"ZONATION",var)
			if ok: print well+ " Delete " + var
	ZONES=db.variableData(well,"ZONATION","ZONES")
	
	if well.find("PEX")>=0:
		if "AS11.3.2" in ZONES and "AS9.0" not in ZONES:
			id = tp.logViewApplyTemplate("User\\LJ_PEX_AS10_AS1132",well,False)
			
			tp.logViewSetName(id,well)
		elif "AS11.3.2" not in ZONES and "AS9.0" not in ZONES:
			id = tp.logViewApplyTemplate("User\\LJ_PEX_AS10_AS1131",well,False)
			tp.logViewSetName(id,well)
		elif "AS11.3.2" not in ZONES and "AS9.0" in ZONES:
			id = tp.logViewApplyTemplate("User\\LJ_PEX_AS9_AS1131",well,False)
			tp.logViewSetName(id,well)
	else:
		if "AS11.3.2" in ZONES and "AS9.0" not in ZONES:
			id = tp.logViewApplyTemplate("User\\LJ_KNG_AS10_AS1132",well,False)
			tp.logViewSetName(id,well)
		elif "AS11.3.2" not in ZONES and "AS9.0" not in ZONES:
			id = tp.logViewApplyTemplate("User\\LJ_KNG_AS10_AS1131",well,False)
			tp.logViewSetName(id,well)
		elif "AS11.3.2" not in ZONES and "AS9.0" in ZONES:
			id = tp.logViewApplyTemplate("User\\LJ_KNG_AS9_AS1131",well,False)
			tp.logViewSetName(id,well)

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-02-20"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""