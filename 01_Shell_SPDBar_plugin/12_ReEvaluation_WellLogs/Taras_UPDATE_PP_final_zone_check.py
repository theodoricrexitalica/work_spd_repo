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
	
for well in db.selectedWellList():
	
	com_ds = 'COMMON_05'
	md = db.variableData(well, com_ds, 'DEPT')
	tvdss = db.variableData(well, com_ds, 'TVDSS')
	porden = db.variableData(well, com_ds, 'Porden')
	perm = db.variableData(well, com_ds, 'K_merge')
	permo = db.variableData(well, com_ds, 'Ko')
	permw = db.variableData(well, com_ds, 'Kw')
	swws = db.variableData(well, com_ds, 'SWWS')
	sw_shf_bf = db.variableData(well, com_ds, 'SW_SHF_bf')
	fi = db.variableData(well, com_ds, 'Fluid_Index')
	z_ds = 'ZONATION'
	zones = db.variableData(well, z_ds, 'ZONES')
	pp_ds = 'CONTACTS_PP'
	gg_ds = 'CONTACTS_GG'
	if db.datasetExists(well, gg_ds):
		zone_c = db.variableData(well, gg_ds, 'ZONE')
		tvdss_c = db.variableData(well, gg_ds, 'CONT_TVDSS')
		cont_type = gg_ds
	else:
		zone_c = db.variableData(well, pp_ds, 'ZONE')
		tvdss_c = db.variableData(well, pp_ds, 'CONT_TVDSS')
		cont_type = pp_ds
	print
	print well
	for zone in zones:
		# Zone border definitions
		if zone == "AS9.0" or zone == "AS9.0_SH" or zone == "AS10.0" or zone == "AS11.1" or zone == "AS11.2" or zone == "AS11.3" or zone == "AS11.3_1" or zone == "AS11.3_2"  or zone == "AS11.3.1" or zone == "AS11.3.2":  
			zone_top_ind=db.datasetZoneIndice(well, com_ds, z_ds, zone)[0]
			zone_bot_ind=db.datasetZoneIndice(well, com_ds, z_ds, zone)[1]
			zone_top_tvdss = tvdss[zone_top_ind]
			zone_bot_tvdss = tvdss[zone_bot_ind]
			zone_top_md = md[zone_top_ind]
			zone_bot_md = md[zone_bot_ind]
			
			print zone,"\t\t", zone_top_ind, "-", zone_bot_ind
		

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-03-02"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""