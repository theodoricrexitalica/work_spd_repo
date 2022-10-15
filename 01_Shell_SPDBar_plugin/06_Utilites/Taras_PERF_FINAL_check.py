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
#Скрипт для проверка интервалов перфораций
import TechlogDialog as td
from os import *
import TechlogDialogAdvanced as tda
import TechlogDialog as td

file_path = os.path.join(db.dirProject(), "Data", "report.txt")
file_txt = file(file_path, "wb")


cmn = "COMMON_05"
perf_n = "PERF_FINAL"
zone_n = "ZONES"
path = "C:\\Apps\Routine\OIS\\perfstatus.xls"
t = "\t"

for well in db.selectedWellList():
#Проверка наличия хотя бы одного датасета REPORT_SPLIT_1
	if not db.datasetExists(well,"REPORT_SPLIT_1"):
		td.information("Внимание","Перфорации отсутствуют")
		break
	else:
		ds_report = "REPORT_SPLIT"
		count = 1
		while db.datasetExists(well, ds_report + "_" + str(count)):
			count += 1
		ds_report = ds_report + "_" + str(count-1)
		wt = []
		well_type = db.datasetPropertyValue(well,ds_report,"Well type")
		
		md = Variable(well,cmn,db.referenceName(well,cmn))
		perf = Variable(well,cmn,perf_n)
		zone = Variable(well,cmn,zone_n)
		
		if db.variableExists(well,cmn,perf_n):
			perf_tops=[]
			perf_bots=[]
			indx=[]
			znx=[]
			for i in range(1,md.size()):
				perf_w = perf.value(i)
				zone_w = zone.value(i)
				if perf_w>0 and perf_w<>perf.value(i-1):
					perf_top = round(md.value(i),2)
					znx_top = zone.value(i)
					ind=perf_w
					perf_tops.append(perf_top)
					indx.append(ind)
					znx.append(znx_top)
			
				if perf_w > 0 and perf_w == perf.value(i-1) and perf_w <> perf.value(i+1):
					perf_bot = round(md.value(i+1),2)
					perf_bots.append(perf_bot)
					
			text_full = []
			for j in range(0,len(perf_tops)):
				text = (str(znx[j]) + "  " + str(perf_tops[j]) + '-' + str(perf_bots[j]) + "  " + str(indx[j]))
				text_full.append(text)

#Вывод на экран панели с интервалами перфораций			
		myDialog = tda.dialogAdvanced(well)
		taras = myDialog.addListBox(well,well_type,text_full)
		myDialog.getListBox(taras)
		myDialog.execDialog()
		file_txt.close()

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2015-10-25"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""