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

def create_picts(well):
	ZONES=db.variableData(well,"ZONATION","ZONES")
	if well.find("PEX")>=0:
		if "AS11.3.2" in ZONES and "AS9.0" not in ZONES:
			id = tp.logViewApplyTemplate("User\UPD_PEX_AS10_AS1132",well,False)
			corr = tp.logViewApplyTemplate("User\CORR_PEX_AS10_AS1132",well,False)
			tp.logViewSetName(id,well)
			tp.logViewSetName(corr,"cor1")
		elif "AS11.3.2" not in ZONES and "AS9.0" not in ZONES:
			id = tp.logViewApplyTemplate("User\UPD_PEX_AS10_AS1131",well,False)
			corr = tp.logViewApplyTemplate("User\CORR_PEX_AS10_AS1131",well,False)
			tp.logViewSetName(id,well)
			tp.logViewSetName(corr,"cor1")
		elif "AS11.3.2" not in ZONES and "AS9.0" in ZONES:
			id = tp.logViewApplyTemplate("User\UPD_PEX_AS9_AS1131",well,False)
			corr = tp.logViewApplyTemplate("User\CORR_PEX_AS9_AS1131",well,False)
			tp.logViewSetName(id,well)
			tp.logViewSetName(corr,"cor1")
	elif well.find("LWD")>=0:
		if "AS11.3.2" in ZONES and "AS9.0" not in ZONES:
			id = tp.logViewApplyTemplate("User\UPD_LWD_AS10_AS1132",well,False)
			corr = tp.logViewApplyTemplate("User\CORR_LWD_AS10_AS1132",well,False)
			tp.logViewSetName(id,well)
			tp.logViewSetName(corr,"cor1")
		elif "AS11.3.2" not in ZONES and "AS9.0" not in ZONES:
			id = tp.logViewApplyTemplate("User\UPD_LWD_AS10_AS1131",well,False)
			corr = tp.logViewApplyTemplate("User\CORR_LWD_AS10_AS1131",well,False)
			tp.logViewSetName(id,well)
			tp.logViewSetName(corr,"cor1")
		elif "AS11.3.2" not in ZONES and "AS9.0" in ZONES:
			id = tp.logViewApplyTemplate("User\UPD_LWD_AS9_AS1131",well,False)
			corr = tp.logViewApplyTemplate("User\CORR_LWD_AS9_AS1131",well,False)
			tp.logViewSetName(id,well)
			tp.logViewSetName(corr,"cor1")
	elif well.find("KNG")>=0:
		if "AS11.3.2" in ZONES and "AS9.0" not in ZONES:
			id = tp.logViewApplyTemplate("User\UPD_KNG_AS10_AS1132",well,False)
			corr = tp.logViewApplyTemplate("User\CORR_KNG_AS10_AS1132",well,False)
			tp.logViewSetName(id,well)
			tp.logViewSetName(corr,"cor1")
		elif "AS11.3.2" not in ZONES and "AS9.0" not in ZONES:
			id = tp.logViewApplyTemplate("User\UPD_KNG_AS10_AS1131",well,False)
			corr = tp.logViewApplyTemplate("User\CORR_KNG_AS10_AS1131",well,False)
			tp.logViewSetName(id,well)
			tp.logViewSetName(corr,"cor1")
		elif "AS11.3.2" not in ZONES and "AS9.0" in ZONES:
			id = tp.logViewApplyTemplate("User\UPD_KNG_AS9_AS1131",well,False)
			corr = tp.logViewApplyTemplate("User\CORR_KNG_AS9_AS1131",well,False)
			tp.logViewSetName(id,well)
			tp.logViewSetName(corr,"cor1")
	else:
		if "AS11.3.2" in ZONES and "AS9.0" not in ZONES:
			id = tp.logViewApplyTemplate("User\UPD_PEX_AS10_AS1132",well,False)
			corr = tp.logViewApplyTemplate("User\CORR_PEX_AS10_AS1132",well,False)
			tp.logViewSetName(id,well)
			tp.logViewSetName(corr,"cor1")
		elif "AS11.3.2" not in ZONES and "AS9.0" not in ZONES:
			id = tp.logViewApplyTemplate("User\UPD_PEX_AS10_AS1131",well,False)
			corr = tp.logViewApplyTemplate("User\CORR_PEX_AS10_AS1131",well,False)
			tp.logViewSetName(id,well)
			tp.logViewSetName(corr,"cor1")
		elif "AS11.3.2" not in ZONES and "AS9.0" in ZONES:
			id = tp.logViewApplyTemplate("User\UPD_PEX_AS9_AS1131",well,False)
			corr = tp.logViewApplyTemplate("User\CORR_PEX_AS9_AS1131",well,False)
			tp.logViewSetName(id,well)
			tp.logViewSetName(corr,"cor1")
def create_hist(well):
	if well.startswith("US"):
		id_dens=tp.histogramMultiWellOpen("US_Bulk Density","User")
		id_neu=tp.histogramMultiWellOpen("US_Neutron Porosity","User")
	if well.startswith("WS"):
		id_dens=tp.histogramMultiWellOpen("WS_Bulk Density","User")
		id_neu=tp.histogramMultiWellOpen("WS_Neutron Porosity","User")
	if well.startswith("SVA"):
		id_dens=tp.histogramMultiWellOpen("SVA_Bulk Density","User")
		id_neu=tp.histogramMultiWellOpen("SVA_Neutron Porosity","User")
	
	tp.histogramMultiWellAddData(id_dens,[well+".COMMON_05"])
	tp.histogramMultiWellSelectVar(id_dens,well,"COMMON_05",0,'RHOZ')
	tp.histogramMultiWellAddData(id_neu,[well+".COMMON_05"])
	tp.histogramMultiWellSelectVar(id_neu,well,"COMMON_05",0,'TNPH')
	
for well in db.selectedWellList():
	create_picts(well)
	create_hist(well)

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-03-03"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""