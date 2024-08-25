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
import TechlogDialogAdvanced as TDA
import os
import TechlogPlot as tp
ZDS = "ZONATION"
DS="COMMON_05"
for WELL in db.selectedWellList():
	ZONE = Variable(WELL, ZDS, "ZONES")
	DEPT = Variable(WELL,DS,db.referenceName(WELL,DS))
	PERF = Variable(WELL,DS,"PERF_FINAL")
	ZonesSize = ZONE.size()
	datasetSize = DEPT.size()
#Perforation intervals creation
	perf_tops=[]
	perf_bots=[]
	indx=[]
	for i in range(1,datasetSize):
		dept=DEPT.value(i)
		perf=PERF.value(i)
		if perf>0 and perf<>PERF.value(i-1):
			perf_top=dept
			ind=perf
			perf_tops.append(perf_top)
			indx.append(ind)
		if perf>0 and perf==PERF.value(i-1) and perf<>PERF.value(i+1):
			perf_bot=DEPT.value(i+1)
			perf_bots.append(perf_bot)
	for x in range(len(perf_tops),10):
		perf_tops.append(-9999)
		perf_bots.append(-9999)
		indx.append(-9999)
	db.variableDelete(WELL,DS,"PERF_FINAL")
	PERF.familyNameChange("Perforation")
	PERF.unitNameChange("unitless")
	myDialog = TDA.dialogAdvanced("Pre-perforated Liner" +
								  "\n Isolated Index    = 1" +
								  "\n Perforated Index  = 2" +
								  "\n Swell Paker Index = 3")
	myDialog.addLabel("Pre-perforated Liner", "Pre-perforated Liner depth" + 
											   "\n" + WELL +
											   "\n Isolated Index      = 1" +
											   "\n Perforated Index  = 2" +
											   "\n Swell Paker Index = 3")
	myDialog.addDoubleInput("TOP_1", "Top depth", perf_tops[0],-100000,10000,2,0.01)
	myDialog.addDoubleInput("BOT_1", "Bot depth", perf_bots[0],-100000,10000,2,0.01)
	myDialog.addDoubleInput("IND_1", "Index", indx[0])
	myDialog.addDoubleInput("TOP_2", "Top depth", perf_tops[1],-100000,10000,2,0.01)
	myDialog.addDoubleInput("BOT_2", "Bot depth", perf_bots[1],-100000,10000,2,0.01)
	myDialog.addDoubleInput("IND_2", "Index", indx[1])
	myDialog.addDoubleInput("TOP_3", "Top depth", perf_tops[2],-100000,10000,2,0.01)
	myDialog.addDoubleInput("BOT_3", "Bot depth",perf_bots[2],-100000,10000,2,0.01)
	myDialog.addDoubleInput("IND_3", "Index", indx[2])
	myDialog.addDoubleInput("TOP_4", "Top depth", perf_tops[3],-100000,10000,2,0.01)
	myDialog.addDoubleInput("BOT_4", "Bot depth", perf_bots[3],-100000,10000,2,0.01)
	myDialog.addDoubleInput("IND_4", "Index", indx[3])
	myDialog.addDoubleInput("TOP_5", "Top depth", perf_tops[4],-100000,10000,2,0.01)
	myDialog.addDoubleInput("BOT_5", "Bot depth", perf_bots[4],-100000,10000,2,0.01)
	myDialog.addDoubleInput("IND_5", "Index", indx[4])
	myDialog.addDoubleInput("TOP_6", "Top depth", perf_tops[5],-100000,10000,2,0.01)
	myDialog.addDoubleInput("BOT_6", "Bot depth",perf_bots[5],-100000,10000,2,0.01)
	myDialog.addDoubleInput("IND_6", "Index", indx[5])
	if myDialog.execDialog():
		top_perf_1=(myDialog.getDoubleInput("TOP_1"))
		bot_perf_1=(myDialog.getDoubleInput("BOT_1"))
		ind_1=(myDialog.getDoubleInput("IND_1"))
		top_perf_2=(myDialog.getDoubleInput("TOP_2"))
		bot_perf_2=(myDialog.getDoubleInput("BOT_2"))
		ind_2=(myDialog.getDoubleInput("IND_2"))
		top_perf_3=(myDialog.getDoubleInput("TOP_3"))
		bot_perf_3=(myDialog.getDoubleInput("BOT_3"))
		ind_3=(myDialog.getDoubleInput("IND_3"))
		top_perf_4=(myDialog.getDoubleInput("TOP_4"))
		bot_perf_4=(myDialog.getDoubleInput("BOT_4"))
		ind_4=(myDialog.getDoubleInput("IND_4"))
		top_perf_5=(myDialog.getDoubleInput("TOP_5"))
		bot_perf_5=(myDialog.getDoubleInput("BOT_5"))
		ind_5=(myDialog.getDoubleInput("IND_5"))
		top_perf_6=(myDialog.getDoubleInput("TOP_6"))
		bot_perf_6=(myDialog.getDoubleInput("BOT_6"))
		ind_6=(myDialog.getDoubleInput("IND_6"))
	for i in range(0,datasetSize):
		perf=PERF.value(i)
		dept=DEPT.value(i)
		perf=-9999
		if top_perf_1<=dept and bot_perf_1>dept:
			perf=ind_1
		if top_perf_2<=dept and bot_perf_2>dept:
			perf=ind_2
		if top_perf_3<=dept and bot_perf_3>dept:
			perf=ind_3
		if top_perf_4<=dept and bot_perf_4>dept:
			perf=ind_4
		if top_perf_5<=dept and bot_perf_5>dept:
			perf=ind_5
		if top_perf_6<=dept and bot_perf_6>dept:
			perf=ind_6
		PERF.setValue(i,perf)
	PERF.save()
#Perfo report creation
file_path = os.path.join(db.dirProject(), "Data", "report.txt")
file_txt = file(file_path, "wb")
ind = "Index"
ds = "COMMON_05"
ds_zone = "ZONATION"
brk = ","
template = "User\HORIZ_ST_WELLS"
for well in db.selectedWellList():
	dialog = TDA.dialogAdvanced("Выбор пласта")
	ref_var_td = db.referenceName(well,ind)
	td =  round(db.variableData(well, ind,ref_var_td)[-1],2)
	td_value = "TD : " + str(td)
	ref_var_zone = db.referenceName(well,ds_zone)
	zone = db.variableData(well,ds_zone,"ZONES")
	md_zone = db.variableData(well,ds_zone,ref_var_zone)
	list = []
	for i in range(len(zone)):
		list.append(zone[i] + " : " + str(md_zone[i]))
	list.append(td_value)
	dialog.addButtonsGroup("Выбор пласта","HorizWell zone ",list,1)
	dialog.execDialog()
	zone_selected = dialog.getButtonsGroup("Выбор пласта")[0].split(" : ")[0]
	top_layer = dialog.getButtonsGroup("Выбор пласта")[0].split(" : ")[1]
	bot_layer = td
#----Print perfs----------------------------------------------------------------------------------------------------------
	file_txt.write(WELL+"\r\n")
	file_txt.write("\r\n" + well.split("-")[1]+"\r\n"+"Perforation intervals"+"\r\n")
	cmn = "COMMON_05"
	perf_n = "PERF_FINAL"
	zone_n = "ZONES"
	t=" "
	md = Variable(WELL,cmn,db.referenceName(WELL,cmn))
	perf = Variable(WELL,cmn,perf_n)
	zone = Variable(WELL,cmn,zone_n)
	if db.variableExists(WELL,cmn,perf_n):
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
		indx_rus = []
		for i in indx:
			if i == 3.0:
				i = "swell paker"
				indx_rus.append(i)
			elif i == 2.0:
				i = "perforation"
				indx_rus.append(i)
			elif i == 1.0:
				i = "isolation"
				indx_rus.append(i)
		for j in range(0,len(perf_tops)):
			file_txt.write(znx[j] + " " + str(perf_tops[j]) + 
			"-" + str(perf_bots[j]) + " " + str(indx_rus[j]) + "\r\n")
	file_txt.write("\r\n" + well.split("-")[1] + brk + "доб" + brk + "освоен" + brk + "добыча" + 
	brk + zone_selected + brk + str(top_layer) + "-" + str(bot_layer) +  brk +
	brk + "100" + brk + "100" + brk + "100" + brk  + brk + "освоение ГС")

file_txt.close()
os.startfile(file_path)
os.startfile("C:\Apps\Routine\OIS\OIS_data.xlsx")
id_plot = tp.logViewApplyTemplate(template,well,False)
tp.logViewSetName(id_plot,well)

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-03-05"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""