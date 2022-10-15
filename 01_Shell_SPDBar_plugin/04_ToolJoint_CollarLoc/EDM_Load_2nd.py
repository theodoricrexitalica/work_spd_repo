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
sys.path.append("C:\Apps\Routine\PP_eval\pypyodbc-1.3.1")
import pypyodbc
import datetime
from EDM_lib import *
myconnection = pypyodbc.connect("DSN=EDM_UI_PRODUCTION;UID=SPDIQM;PWD=SPDIQM") 
mycursor = myconnection.cursor()
for well in db.selectedWellList():
	#проверка наличия датасета со сдвинутыми муфтами,изменение типа данных и 
	#копирование в CBL
	if db.datasetExists(well,"CBL_sft"):
		print well
		db.variableTypeChange(well,"CBL_sft","CC","point data")
		db.variableCopy(well,"CBL_sft","CC","CBL","CC","")
		db.variableCopy(well,"CBL_sft","CC","CCL","CC","")
	#основной скрипт
	well_name=GET_WELL_NAME(well)
	well_id=GET_WELL_ID(well_name)
	wellbore_id=GET_WELLBORE_ID(well_name)
	isRemove=REMOVE_CASING_COLLAR_FROM_EDM(well_id)
	event_id=GET_EVENT_ID(well_name)
	date_report= GET_DATE_REPORT(well_name)
	date_report_str=(str(date_report.day) + "/" + str(date_report.month) + 
					 "/" + str(date_report.year))
	event_id=GET_EVENT_ID(well_name)
	SQL_ins="INSERT INTO EDM.DM_REPORT_JOURNAL (REPORT_JOURNAL_ID, WELL_ID, WELLBORE_ID, EVENT_ID, DATE_REPORT, REPORT_NO, DESCRIPTION, ENTITY_TYPE, EVENT_CODE, CREATE_DATE, REPORT_ALIAS, CREATE_USER_ID, CREATE_APP_ID, IS_VALIDATED, SECTION_STATUS) VALUES (generate_key(10), '"+str(well_id)+"', '"+str(wellbore_id)+"', '"+str(event_id)+"',  TO_DATE('"+str(date_report_str)+"', 'dd/mm/yyyy')+3, 5, 'CCL interp', 'Pipe Tally', 'DRO', SYSDATE, 'GEN_PIPE','Techlog upload', 'Techlog upload', 'N', 'GEN=C TALLY=C')"
	mycursor.execute(SQL_ins)
	mycursor.execute("commit")
	report_journal_id=GET_REPORT_JOURNAL_ID(well_id, date_report_str )
	SQL_ins="INSERT INTO EDM.DM_PIPE_RUN (WELL_ID, EVENT_ID, PIPE_RUN_ID, WELLBORE_ID, PIPE_NOTE, REPORT_JOURNAL_ID, REPORT_NO, DATE_REPORT, RUN_TALLY_TYPE, IS_TOP_DOWN, IS_JOINT_NO_TOP_DOWN) VALUES ('"+str(well_id)+"', '"+str(event_id)+"',generate_key(5),  '"+str(wellbore_id)+"', 'INTERPRETED CASING COLLARS', '"+ str(report_journal_id)+"', 5, TO_DATE('"+str(date_report_str)+"', 'dd/mm/yyyy')+3, 'RUN', 'N', 'N')"
	mycursor.execute(SQL_ins)
	mycursor.execute("commit")
	pipe_run_id=GET_PIPE_RUN_ID(well_id, date_report_str, report_journal_id)
	DLIST=db.datasetList(well)
	for d in DLIST:
		if d=="CBL":
			CC=Variable(well,d,"CC")
			DEPT=Variable(well,d,"DEPTH")
			CBL_Size=DEPT.size()
			sequence_no=0
			length=0
			for f in range(0, CBL_Size):
				if CC.value(CBL_Size-f-1)==1:
					sequence_no=sequence_no+1
					length=0
					if sequence_no>1:
						length=Prev_DEPTH-DEPT.value(CBL_Size-f-1)
					cum_length=DEPT.value(CBL_Size-f-1)
					print str(sequence_no)+", "+str(length) +", " +str(DEPT.value(CBL_Size-f-1))
					Prev_DEPTH=cum_length
					SQL_ins="INSERT INTO EDM.DM_PIPE_TALLY (WELL_ID, EVENT_ID, PIPE_RUN_ID, PIPE_TALLY_ID, SEQUENCE_NO, LENGTH, cum_length, RUN_NUMBER) VALUES ('"+str(well_id)+"','"+str(event_id)+"', '"+str(pipe_run_id)+"', generate_key(5), "+str(sequence_no)+", "+str(length)+", "+str(cum_length)+", 5)"
					mycursor.execute(SQL_ins)
					mycursor.execute("commit")
	db.datasetDelete(well,"CBL_sft",1)
	#mycursor.execute(SQL)
	#for well, sequence_no, cum_length, length  in mycursor.fetchall():
		#print well, ' ', sequence_no,' ', cum_length,' ', length

__author__ = """Danila KARNAUKH (D.Karnaukh)"""
__date__ = """2011-11-02"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""