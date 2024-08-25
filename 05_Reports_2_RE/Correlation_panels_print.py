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
import time
import webbrowser
import TechlogPlot as tp

Path="\\\europe.shell.com\\europe\\E & P\\SPD Moscow\\Dept_05\\OFM\\Correlation Panel\\PPevals_for_panel\\"

for well in db.selectedWellList():
	wellName=well.split("-")[0]+"-"+well.split("-")[1]
	for var in db.variableList(well,"ZONATION"):
		if db.variableFamily(well,"ZONATION",var)=="Zone Name" and var!="ZONES" and var!="ZONE":
			ok=db.variableDelete(well,"ZONATION",var)
			if ok: print well+ " Delete " + var
	ZONES=db.variableData(well,"ZONATION","ZONES")
	
	if "PLT_FINAL" in db.datasetList(well):
		if "AS11.3.2" in ZONES and "AS9.0" not in ZONES:
			id=tp.logViewGetIdByName('WITH_PLT_AS10-AS1132')
			tp.printToFile(id,'Custom','.png',Path+wellName,21,29.7,0,-1,0,-1,-1,False,150)
			#tp.close(id)
		elif "AS11.3.2" not in ZONES and "AS9.0" not in ZONES:
			id=tp.logViewGetIdByName('WITH_PLT_AS10-AS1131')
			tp.printToFile(id,'Custom','.png',Path+wellName,21,29.7,0,-1,0,-1,-1,False,150)
			#tp.close(id)
		elif "AS11.3.2" not in ZONES and "AS9.0" in ZONES:
			id=tp.logViewGetIdByName('WITH_PLT_AS9-AS1131')
			tp.printToFile(id,'Custom','.png',Path+wellName,21,29.7,0,-1,0,-1,-1,False,150)
			#tp.close(id)
		elif "AS11.3.2" in ZONES and "AS9.0" in ZONES:
			id=tp.logViewGetIdByName('WITH_PLT_AS9-AS1132')
			tp.printToFile(id,'Custom','.png',Path+wellName,21,29.7,0,-1,0,-1,-1,False,150)
			#tp.close(id)
	else:
		if "AS11.3.2" in ZONES and "AS9.0" not in ZONES:
			id=tp.logViewGetIdByName('NO_PLT_AS10-AS1132')
			tp.printToFile(id,'Custom','.png',Path+wellName,21,29.7,0,-1,0,-1,-1,False,150)
			#tp.close(id)
		elif "AS11.3.2" not in ZONES and "AS9.0" not in ZONES:
			id=tp.logViewGetIdByName('NO_PLT_AS10-AS1131')
			tp.printToFile(id,'Custom','.png',Path+wellName,21,29.7,0,-1,0,-1,-1,False,150)
			#tp.close(id)
		elif "AS11.3.2" not in ZONES and "AS9.0" in ZONES:
			id=tp.logViewGetIdByName('NO_PLT_AS9-AS1131')
			tp.printToFile(id,'Custom','.png',Path+wellName,21,29.7,0,-1,0,-1,-1,False,150)
			#tp.close(id)
		#elif "AS11.3.2" in ZONES and "AS9.0" in ZONES:
			#id=tp.logViewGetIdByName('NO_PLT_AS9-AS1132')
			#tp.printToFile(id,'Custom','.png',Path+wellName,21,29.7,0,-1,0,-1,-1,False,150)
			#tp.close(id)

webbrowser.open(Path)

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2015-11-12"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""