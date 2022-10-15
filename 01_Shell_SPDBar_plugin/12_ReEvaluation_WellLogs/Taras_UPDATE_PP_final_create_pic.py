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
			id = tp.logViewApplyTemplate("User\UPD_PEX_AS9-AS1131",well,False)
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
			id = tp.logViewApplyTemplate("User\UPD_KNG_AS9-AS1131",well,False)
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
			id = tp.logViewApplyTemplate("User\UPD_PEX_AS9-AS1131",well,False)
			corr = tp.logViewApplyTemplate("User\CORR_PEX_AS9_AS1131",well,False)
			tp.logViewSetName(id,well)
			tp.logViewSetName(corr,"cor1")
	

def create_hist(well):
	if well.startswith("WS"):
		id_dens=tp.histogramMultiWellOpen("WS_Bulk Density")
		tp.histogramMultiWellAddData(id_dens,[well+".COMMON_05"])
		tp.histogramMultiWellSelectVar(id_dens,well,"COMMON_05",0,'RHOZ')
		tp.histogramMultiWellSelectVar(id_dens,well,"COMMON_05",0,'SBD2')
		if (db.variableExists(well,"COMMON_05","RHOZ_orig") or
			db.variableExists(well,"COMMON_05","SBD2_orig")):
			id_dens_orig=tp.histogramMultiWellOpen("WS_Bulk Density")
			tp.histogramMultiWellAddData(id_dens_orig,[well+".COMMON_05"])
			tp.histogramMultiWellSelectVar(id_dens_orig,well,"COMMON_05",0,'RHOZ_orig')
			tp.histogramMultiWellSelectVar(id_dens_orig,well,"COMMON_05",0,'SBD2_orig')
		else: print " RHOZ_orig not found, no correction was applied to RHOZ"
	
		id_neu=tp.histogramMultiWellOpen("WS_Neutron Porosity")
		tp.histogramMultiWellAddData(id_neu,[well+".COMMON_05"])
		tp.histogramMultiWellSelectVar(id_neu,well,"COMMON_05",0,'TNPH')
		tp.histogramMultiWellSelectVar(id_neu,well,"COMMON_05",0,'TNPL')
		if (db.variableExists(well,"COMMON_05","TNPH_orig") or 
			db.variableExists(well,"COMMON_05","TNPL_orig")):
			id_neu_orig=tp.histogramMultiWellOpen("WS_Neutron Porosity")
			tp.histogramMultiWellAddData(id_neu_orig,[well+".COMMON_05"])
			tp.histogramMultiWellSelectVar(id_neu_orig,well,"COMMON_05",0,'TNPH_orig')
			tp.histogramMultiWellSelectVar(id_neu_orig,well,"COMMON_05",0,'TNPL_orig')
		else: print " TNPH_orig not found, no correction was applied to TNPH"

	if well.startswith("SVA"):
		id_dens=tp.histogramMultiWellOpen("SVA_Bulk Density")
		tp.histogramMultiWellAddData(id_dens,[well+".COMMON_05"])
		tp.histogramMultiWellSelectVar(id_dens,well,"COMMON_05",0,'RHOZ')
		tp.histogramMultiWellSelectVar(id_dens,well,"COMMON_05",0,'SBD2')
		if (db.variableExists(well,"COMMON_05","RHOZ_orig") or
			db.variableExists(well,"COMMON_05","SBD2_orig")):
			id_dens_orig=tp.histogramMultiWellOpen("SVA_Bulk Density")
			tp.histogramMultiWellAddData(id_dens_orig,[well+".COMMON_05"])
			tp.histogramMultiWellSelectVar(id_dens_orig,well,"COMMON_05",0,'RHOZ_orig')
			tp.histogramMultiWellSelectVar(id_dens_orig,well,"COMMON_05",0,'SBD2_orig')
		else: print " RHOZ_orig not found, no correction was applied to RHOZ"
	
		id_neu=tp.histogramMultiWellOpen("SVA_Neutron Porosity")
		tp.histogramMultiWellAddData(id_neu,[well+".COMMON_05"])
		tp.histogramMultiWellSelectVar(id_neu,well,"COMMON_05",0,'TNPH')
		tp.histogramMultiWellSelectVar(id_neu,well,"COMMON_05",0,'TNPL')
		if (db.variableExists(well,"COMMON_05","TNPH_orig") or 
			db.variableExists(well,"COMMON_05","TNPL_orig")):
			id_neu_orig=tp.histogramMultiWellOpen("SVA_Neutron Porosity")
			tp.histogramMultiWellAddData(id_neu_orig,[well+".COMMON_05"])
			tp.histogramMultiWellSelectVar(id_neu_orig,well,"COMMON_05",0,'TNPH_orig')
			tp.histogramMultiWellSelectVar(id_neu_orig,well,"COMMON_05",0,'TNPL_orig')
		else: print " TNPH_orig not found, no correction was applied to TNPH"


def open_data_editor(well):
	list = []
	list.append(well + ".CONTACTS.FWL_bf")
	list.append(well + ".CONTACTS.CONT_TVDSS_PP")
	list.append(well + ".CONTACTS.ZONES")
	db.dataEditorOpen(list)

for well in db.selectedWellList():
	create_picts(well)
	print "Создание диаграмм"
	create_hist(well)
	print "Создание гистограмм"
	open_data_editor(well)
	print "Открытие таблицы"

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-02-28"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""