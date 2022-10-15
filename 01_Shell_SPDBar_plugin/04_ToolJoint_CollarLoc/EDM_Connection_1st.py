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
import os
import sys
sys.path.append("C:\Apps\Routine\PP_eval\pypyodbc-1.3.1\\")
import pypyodbc
import TechlogPlot as plot
myconnection = pypyodbc.connect("DSN=EDM_UI_PRODUCTION;UID=SPDIQM;PWD=SPDIQM") 
mycursor = myconnection.cursor()
template = "User\EDM"
def GET_WELL_NAME(well):
	well=well.replace("_", "-")
	wellname_arr=well.split('-')
	wellnum=wellname_arr[1]
	if wellnum[0]=="0":
		wellnum=wellnum[1:]
	wellname=wellname_arr[0]+'-'+wellnum
	return wellname
for well in db.selectedWellList():
	WELL=well
	well_name=GET_WELL_NAME(well)
	print well_name
	#SQL="select w.well_common_name as well, p.sequence_no as sequence_no, \
	#round(cum_length*0.3048,2) as cum_length,round(length*0.3048,2) as length from dm_pipe_run r, \
	#dm_pipe_tally p, cd_well w, cd_site s where w.site_id = s.site_id and w.well_id = p.well_id \
	#and r.well_id= p.well_id and p.PIPE_RUN_ID = r.PIPE_RUN_ID and s.project_id in \
	#('uepgCCUr88','zubFM70aiT','iZGXXF4Sq8') and run_tally_type = 'RUN' and \
	#round(total_length*0.3048,0)>2000 and round(cum_length*0.3048,2)>2100 and \
	#w.well_common_name like '"+ well_name +"%' order by sequence_no"
	SQL="select w.well_common_name as well, p.sequence_no, round(cum_length*0.3048,2),\
		round(length*0.3048,2) from dm_pipe_run r, dm_pipe_tally p, cd_well w, \
		cd_site s where w.site_id = s.site_id and w.well_id = p.well_id \
		and r.well_id= p.well_id and p.PIPE_RUN_ID = r.PIPE_RUN_ID and \
		s.project_id in ('uepgCCUr88','zubFM70aiT','iZGXXF4Sq8') and \
		run_tally_type = 'RUN' and round(total_length*0.3048,0)>2000 and \
		w.well_common_name like '"+ well_name +"%' order by sequence_no"
	mycursor.execute(SQL)
	NUMBER=[]
	DEPTH=[]
	for well, sequence_no, cum_length, length  in mycursor.fetchall():
		print well, ' ', sequence_no,' ', cum_length,' ', length
		DEPTH.append(cum_length)
		NUMBER.append(1)
	if DEPTH==[]:
		print well_name
	else:
		DEPTH=DEPTH[::-1]
#Генерация плота для посадки муфт
		db.datasetCreate(WELL,"CCL","DEPT","Measured Depth","M",DEPTH)
		db.variableSave(WELL,"CCL","CC","","",NUMBER)	
		db.datasetTypeChange(WELL,"CCL","point data")
		db.variableTypeChange(WELL,"CCL","CC","point data")
		db.variableCopy(WELL,"CCL","CC","CBL","CC","")
		id_plot=plot.logViewApplyTemplate(template,WELL,0)
		plot.logViewInsertTrackByWell(id_plot,WELL,0,1)
		list_gr=db.variableListByFamily(WELL,"CBL","Gamma Ray")+db.variableListByFamily(WELL,"COMMON_05","Gamma Ray")
		plot.logViewInsertVariable(id_plot,[WELL+".CBL."+list_gr[0],WELL+".COMMON_05."+list_gr[1]],1)
		plot.logViewSetVariableColour(id_plot,WELL+".CBL."+list_gr[0],0,0,0)
		plot.logViewSetVariableColour(id_plot,WELL+".COMMON_05."+list_gr[1],255,0,0)
		plot.logViewSetAxeLimitTypeByVariable(id_plot,WELL+".CBL."+list_gr[0],1)
		plot.logViewSetMinMaxUserByVariable(id_plot,WELL+".CBL."+list_gr[0],150,0,0)
		#db.datasetDelete(WELL,"CCL",1)

__author__ = """Danila KARNAUKH (D.Karnaukh)"""
__date__ = """2011-11-02"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""