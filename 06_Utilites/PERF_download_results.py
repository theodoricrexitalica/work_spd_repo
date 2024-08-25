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
from Techlog import*
import os

filepath="C:\\Apps\\"
#filepath="I:\\Common\\2UlyanovEgor\\WS\\"
perf_result=open(filepath+'Perf_final.txt', 'w+')

well=''
for well in db.selectedWellList():
	dataset='COMMON_05'
	DEPT='DEPT'
	TVDSS='TVDSS'
	ZONES='ZONES'
	PERF_FINAL='PERF_FINAL'
	if db.datasetExists(well, dataset):
		if db.variableExists(well, dataset, PERF_FINAL):
			DEPT=db.variableData(well, dataset, DEPT)
			TVDSS=db.variableData(well, dataset, TVDSS)
			PERF_FINAL=db.variableData(well, dataset, PERF_FINAL)
			ZONES=db.variableData(well, dataset, ZONES)
			i=0
			perf_top=0;
			perf_bottom=0;
			perf=0;
			zones='';
			for val in DEPT:
				#try:
				if PERF_FINAL[i]>=0:
					if perf_top==0:
						perf_top=val
						perf=PERF_FINAL[i]
						zones=ZONES[i]
				else:
					if perf_top>0:
						perf_bottom=val
				if perf_bottom>0:
					perf_result.writelines(str(well)+';'+ str(perf_top)+';'+str(perf_bottom)+';'+str(ZONES[i])+';'+str(perf)+'\n')
					perf_top=0;
					perf_bottom=0;
					perf=0;
					zones='';
				i=i+1
				#except:
					#print well
perf_result.close()

__author__ = """rugza0 RUGZA0 (Gulshat.Zakirova)"""
__date__ = """2012-09-21"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""