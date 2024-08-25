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
import win32com.client
from os import *
import pythoncom
pythoncom.CoInitialize()
from win32com import client
import TechlogDialogAdvanced as TDA
import datetime
import TechlogPlot as tp
today=datetime.date.today()
date=str(today.strftime("%d.%m.%y"))

file_path = os.path.join(db.dirProject(), "Data", "report.txt")
file_txt = file(file_path, "wb")

#Блок выбора какой датасет с отбивками будем использовать
#Для кустов SVA_K151, SVA_K52, US_K07, US_К11 неоходим датасет ZON_6GR
zonation = ["ZONATION","ZON_JAN16","ZON_6GR"]
Pad_dialog = TDA.dialogAdvanced("Выбор отбивок")
Pad_dialog.addLabel("Выбор отбивок", "Выбираем:"
					+"\n- SVA-K151 и SVA-K52"
					+"\nнадо брать ZON_6GR"
					+"\n- для ВС надо брать"
					+ "\nZON_JAN16" )
Pad_dialog.addListInput("Pad list","Pad_list", zonation)
Pad_dialog.execDialog()
ZDS = Pad_dialog.getListInput("Pad list")
#-----------------------------------------------------------------------------------
LIST=db.selectedWellList()
DS="COMMON_05"
template = "User\PPeval_CBL"
template_us = "User\US_ZON_JAN16"
p=";"
t=" "
for j in db.selectedWellList():
	WELL=j
	ZONE = Variable(WELL, ZDS, "ZONES")
	DeptZone = Variable(WELL, ZDS, "DEPTH")
	DEPT = Variable(WELL,DS,"DEPT")
	PERF = Variable(WELL,DS,"PERF_FINAL")
	KH_tvd_oil = Variable(WELL,DS,"KH_tvd_oil_perf")
	KH_tvd_water = Variable(WELL,DS,"KH_tvd_water_perf")
	KH_brine = Variable(WELL,DS,"KH_brine_perf")
	Oil = Variable(WELL,DS,"%_oil")
	Water = Variable(WELL,DS,"%_water")
	Brine = Variable(WELL,DS,"%_brine")
	TVDSS = Variable(WELL,DS,"TVDSS")
	TVDSS_ZONE = Variable(WELL,ZDS,"TVDSS")
	Ko = Variable(WELL, DS, "Ko")
	Kw = Variable(WELL, DS, "Kw")
	Kmerge = Variable(WELL, DS, "K_merge")
	ZonesSize = ZONE.size()
	datasetSize = DEPT.size()
	PHI_cutoff = 0.13
#----- Family for Split curves--------------------------------------------------------------------------------
	Oil.familyNameChange("Integrated Oil Flow")
	Water.familyNameChange("Integrated Water Flow")
	Brine.familyNameChange("Integrated Water Flow")
#----- Perforation intervals-----------------------------------------------------------------------------------
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
	myDialog = TDA.dialogAdvanced("Perforation")
	myDialog.addDoubleInput("PERF_TOP_1", "Perforation 1	TOP", perf_tops[0])
	myDialog.addDoubleInput("PERF_BOT_1", "	BOTTOM", perf_bots[0])
	myDialog.addDoubleInput("IND_1", "	Index", indx[0])
	myDialog.addDoubleInput("PERF_TOP_2", "Perforation 2	TOP", perf_tops[1])
	myDialog.addDoubleInput("PERF_BOT_2", "	BOTTOM", perf_bots[1])
	myDialog.addDoubleInput("IND_2", "	Index", indx[1])
	myDialog.addDoubleInput("PERF_TOP_3", "Perforation 3	TOP", perf_tops[2])
	myDialog.addDoubleInput("PERF_BOT_3", "	BOTTOM",perf_bots[2])
	myDialog.addDoubleInput("IND_3", "	Index", indx[2])
	myDialog.addDoubleInput("PERF_TOP_4", "Perforation 4	TOP", perf_tops[3])
	myDialog.addDoubleInput("PERF_BOT_4", "	BOTTOM", perf_bots[3])
	myDialog.addDoubleInput("IND_4", "	Index", indx[3])
	myDialog.addDoubleInput("PERF_TOP_5", "Perforation 5	TOP", perf_tops[4])
	myDialog.addDoubleInput("PERF_BOT_5", "	BOTTOM", perf_bots[4])
	myDialog.addDoubleInput("IND_5", "	Index", indx[4])
	myDialog.addDoubleInput("PERF_TOP_6", "Perforation 6	TOP", perf_tops[5])
	myDialog.addDoubleInput("PERF_BOT_6", "	BOTTOM", perf_bots[5])
	myDialog.addDoubleInput("IND_6", "	Index", indx[5])
	myDialog.addDoubleInput("PERF_TOP_7", "Perforation 7	TOP", perf_tops[6])
	myDialog.addDoubleInput("PERF_BOT_7", "	BOTTOM", perf_bots[6])
	myDialog.addDoubleInput("IND_7", "	Index", indx[6])
	myDialog.addDoubleInput("PERF_TOP_8", "Perforation 8	TOP", perf_tops[7])
	myDialog.addDoubleInput("PERF_BOT_8", "	BOTTOM", perf_bots[7])
	myDialog.addDoubleInput("IND_8", "	Index", indx[7])
	myDialog.addDoubleInput("PERF_TOP_9", "Perforation 9	TOP", perf_tops[8])
	myDialog.addDoubleInput("PERF_BOT_9", "	BOTTOM", perf_bots[8])
	myDialog.addDoubleInput("IND_9", "	Index", indx[8])
	myDialog.addDoubleInput("PERF_TOP_10", "Perforation 10	TOP", perf_tops[9])
	myDialog.addDoubleInput("PERF_BOT_10", "	BOTTOM", perf_bots[9])
	myDialog.addDoubleInput("IND_10", "	Index", indx[9])
	if myDialog.execDialog():
		top_perf_1=(myDialog.getDoubleInput("PERF_TOP_1"))
		bot_perf_1=(myDialog.getDoubleInput("PERF_BOT_1"))
		ind_1=(myDialog.getDoubleInput("IND_1"))
		top_perf_2=(myDialog.getDoubleInput("PERF_TOP_2"))
		bot_perf_2=(myDialog.getDoubleInput("PERF_BOT_2"))
		ind_2=(myDialog.getDoubleInput("IND_2"))
		top_perf_3=(myDialog.getDoubleInput("PERF_TOP_3"))
		bot_perf_3=(myDialog.getDoubleInput("PERF_BOT_3"))
		ind_3=(myDialog.getDoubleInput("IND_3"))
		top_perf_4=(myDialog.getDoubleInput("PERF_TOP_4"))
		bot_perf_4=(myDialog.getDoubleInput("PERF_BOT_4"))
		ind_4=(myDialog.getDoubleInput("IND_4"))
		top_perf_5=(myDialog.getDoubleInput("PERF_TOP_5"))
		bot_perf_5=(myDialog.getDoubleInput("PERF_BOT_5"))
		ind_5=(myDialog.getDoubleInput("IND_5"))
		top_perf_6=(myDialog.getDoubleInput("PERF_TOP_6"))
		bot_perf_6=(myDialog.getDoubleInput("PERF_BOT_6"))
		ind_6=(myDialog.getDoubleInput("IND_6"))
		top_perf_7=(myDialog.getDoubleInput("PERF_TOP_7"))
		bot_perf_7=(myDialog.getDoubleInput("PERF_BOT_7"))
		ind_7=(myDialog.getDoubleInput("IND_7"))
		top_perf_8=(myDialog.getDoubleInput("PERF_TOP_8"))
		bot_perf_8=(myDialog.getDoubleInput("PERF_BOT_8"))
		ind_8=(myDialog.getDoubleInput("IND_8"))
		top_perf_9=(myDialog.getDoubleInput("PERF_TOP_9"))
		bot_perf_9=(myDialog.getDoubleInput("PERF_BOT_9"))
		ind_9=(myDialog.getDoubleInput("IND_9"))
		top_perf_10=(myDialog.getDoubleInput("PERF_TOP_10"))
		bot_perf_10=(myDialog.getDoubleInput("PERF_BOT_10"))
		ind_10=(myDialog.getDoubleInput("IND_10"))
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
		if top_perf_7<=dept and bot_perf_7>dept:
			perf=ind_7
		if top_perf_8<=dept and bot_perf_8>dept:
			perf=ind_8
		if top_perf_9<=dept and bot_perf_9>dept:
			perf=ind_9
		if top_perf_10<=dept and bot_perf_10>dept:
			perf=ind_10	
		PERF.setValue(i,perf)
	PERF.save()
#----- Flowing curve-----------------------------------------------------------------------------------------
	db.variableDelete(WELL,DS,"Flowing")
	Flowing=Variable(WELL,DS,"Flowing")
	Flowing.familyNameChange("Flowing Interval")
	for f in range(0,datasetSize):
		perf=PERF.value(f)
		flow=Flowing.value(f)
		if perf==2: flow=5
		Flowing.setValue(f,flow)
	Flowing.save()
	print "Flowing created"
#----Print perfs----------------------------------------------------------------------------------------------------------
	file_txt.write(WELL+"\r\n")
	file_txt.write("\r\n" + j.split("-")[1]+"\r\n"+"Perforation intervals"+"\r\n")
	cmn = "COMMON_05"
	perf_n = "PERF_FINAL"
	zone_n = "ZONES"
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
			if i == 2.0:
				i = "perforation"
				indx_rus.append(i)
			else:
				i = "isolation"
				indx_rus.append(i)
		print ""
		for j in range(0,len(perf_tops)):
			print znx[j], t , perf_tops[j],"-", perf_bots[j], t, indx_rus[j]
			file_txt.write(znx[j] + " " + str(perf_tops[j]) + 
			"-" + str(perf_bots[j]) + " " + str(indx_rus[j]) + "\r\n")
	#----Старая версия вывода интервалов перфорации без индексов перфорация открыта/закрыта------------------------------------------
	#file_txt.write(j.split("-")[1]+"\r\n"+"Perforation intervals"+"\r\n")
	#file_txt.write(j.split("-")[1]+"\r\n"+"Perforation intervals"+"\r\n")
	#for i in range (0, ZonesSize-1):
		#zone = ZONE.value(i)
		#deptzone=DeptZone.value(i)
		#perf_int=""
		#written="no"
		#p_list=[[top_perf_1, bot_perf_1],[top_perf_2, bot_perf_2],[top_perf_3, bot_perf_3],[top_perf_4, bot_perf_4],[top_perf_5, bot_perf_5],[top_perf_6, bot_perf_6],[top_perf_7, bot_perf_7],[top_perf_8, bot_perf_8],[top_perf_9, bot_perf_9],[top_perf_10, bot_perf_10]]
		#for perf in p_list:
			#if (perf[0])>=deptzone and (perf[0])<DeptZone.value(i+1):
				#perf_int=perf_int+str(perf)
				#if perf_int<>-9999:
					#print zone,p, str(round(perf[0],1))+"-"+str(round(perf[1],1))
					#file_txt.write(zone+" "+str(perf[0])+"-"+str(perf[1])+str(perf_int)+"\r\n")
				#written="yes"
#---- KH_perf creation  --------------------------------------------------------------------------------------
	"ZONES", db.variableData(WELL, ZDS, "ZONES")
	top_zone=db.variableData(WELL, ZDS, "ZONES")[0]
	print ""
	print "Top zone=", top_zone
	bot_zone=db.variableData(WELL, ZDS, "ZONES")[-1]
	print "Bottom zone=", bot_zone
	try:
		for z in range (0,ZONE.size()):
			START_ind= db.datasetZoneIndice(WELL, DS, ZDS, top_zone)[0]
			STOP_ind= db.datasetZoneIndice(WELL, DS, ZDS, bot_zone)[1]
	except TypeError,NameError: 
		print "Проблема с зонейшенами"
	ko_h=0
	kw_h=0
	kmerge_h=0
	for j in range (STOP_ind, START_ind, -1):
		tvdss=TVDSS.value(j)
		ko=Ko.value(j)
		kw=Kw.value(j)
		kmerge=Kmerge.value(j)
		perf_final=PERF.value(j)
		if ko>0 and perf_final==2 :
			ko_h=ko_h+ko*(tvdss-TVDSS.value(j-1))
		KH_tvd_oil. setValue(j,ko_h)
		if kw>0 and perf_final==2 :
			kw_h=kw_h+kw*(tvdss-TVDSS.value(j-1))
		KH_tvd_water. setValue(j,kw_h)
		if kmerge>0 and perf_final==2 :
			kmerge_h=kmerge_h+kmerge*(tvdss-TVDSS.value(j-1))
		KH_brine. setValue(j,kmerge_h)
	KH_tvd_oil.save()
	KH_tvd_water.save()
	KH_brine.save()
#----Max kh---------------------------------------------------------------------------------------------------------
	kh_oil_max=max(KH_tvd_oil.values())
	print ""
	print "kh_oil_max=", round(kh_oil_max,1)
	kh_water_max=max(KH_tvd_water.values())
	print "kh_water_max", round(kh_water_max,1)
	kh_brine_max=max(KH_brine.values())
	print "kh_brine_max", round(kh_brine_max,1)
#-----Splits-------------------------------------------------------------------------------------------------------
	print ""
	print"zone top_bot oil water brine_WI"
	for m in range(0,datasetSize):
		oil=Oil.value(m)
		water=Water.value(m)
		brine=Brine.value(m)
		kh_oil=KH_tvd_oil.value(m)
		kh_water=KH_tvd_water.value(m)
		kh_brine=KH_brine.value(m)
		if kh_oil<>-9999:
			oil=kh_oil*100/kh_oil_max
		Oil.setValue(m,oil)
		if kh_water<>-9999:
			water=kh_water*100/kh_water_max
		Water.setValue(m,water)
		if kh_brine<>-9999:
			brine=kh_brine*100/kh_brine_max
		Brine.setValue(m,brine)
	Oil.save()
	Water.save()
	Brine.save()
	
#----Split based on KH_perf -------------------------------------------------------------------------------------
	file_txt.write("\r\n"+"zone top_bot oil water brine_WI"+"\r\n")
	for j in range(0,ZonesSize-1):
		zone=ZONE.value(j)
		tvdss_zone=TVDSS_ZONE.value(j)
		deptzone=DeptZone.value(j)
		kh_o=KH_tvd_oil.value(j)
		kh_w=KH_tvd_water.value(j)
		kh_b=KH_brine.value(j)
		kh_o_top=-9999
		kh_w_top=-9999
		kh_b_top=-9999
		rzone=" "
		if zone=="AS9.0": rzone="АС9"
		if zone=="AS10.0": rzone="АС10"
		elif zone=="AS11.1": rzone="АС11(1)"
		elif zone=="AS11.2": rzone="АС11(2)"
		elif zone=="AS11.3.1": rzone="АС11(3-1)"
		elif zone=="AS11.3.2": rzone="АС11(3-2)"
		elif zone=="AS11.3": rzone="АС11(3)"
		elif zone=="Prodelta": rzone="Продельта"
		elif zone=="АС9".decode("utf-8"):  rzone="AC9"
		elif zone=="АС9-2".decode("utf-8"): rzone="AC9(2)"
		elif zone=="АС10-1".decode("utf-8"):  rzone="AC10(1)"
		elif zone=="АС10-2".decode("utf-8"):  rzone="AC10(2)"
		elif zone=="АС11-1".decode("utf-8"):  rzone="AC11(1)"
		elif zone=="АС11-2".decode("utf-8"): rzone="AC11(2)"
		elif zone=="АС11-2б".decode("utf-8"): rzone="AC11(2б)"
		elif zone=="АС11-3".decode("utf-8"): rzone="AC11(3)"
		elif zone=="AS9":  rzone="AC9"
		elif zone=="AS9-2": rzone="AC9(2)"
		elif zone=="AS10-1":  rzone="AC10(1)"
		elif zone=="AS10-2":  rzone="AC10(2)"
		elif zone=="AS11-1":  rzone="AC11(1)"
		elif zone=="AS11-2": rzone="AC11(2)"
		elif zone=="AS11-2b": rzone="AC11(2б)"
		elif zone=="AS11-3": rzone="AC11(3)"
		elif zone=="BS8":  rzone="BS(8)"
		elif zone=="BS8_SH": rzone="BS(8SH)"
		elif zone=="ACH1":  rzone="ACH1"
		elif zone=="ACH2":  rzone="ACH2"
		elif zone=="ACH3":  rzone="ACH3"
		elif zone=="ACH4": rzone="ACH4"
		elif zone=="ACH5": rzone="ACH5"
		
		for k in range(0,datasetSize):
			tvdss=TVDSS.value(k)
			kh_o=KH_tvd_oil.value(k)
			kh_w=KH_tvd_water.value(k)
			kh_b=KH_brine.value(k)
			if tvdss>=tvdss_zone and tvdss<=TVDSS_ZONE.value(j+1):
				if kh_o_top==-9999:
					 kh_o_top=kh_o
				kh_o_bot=kh_o
				if kh_w_top==-9999:
					kh_w_top=kh_w
				kh_w_bot=kh_w
				if kh_b_top==-9999:
					kh_b_top=kh_b
				kh_b_bot=kh_b
		if round((kh_b_top-kh_b_bot)*100/kh_brine_max,1)>0 and kh_b_bot<>-9999:
			print (rzone + p + str(round(deptzone,1))+
					"-"+str(round(DeptZone.value(j+1),1))+p
					+ str(round((kh_o_top-kh_o_bot)*100/kh_oil_max,1))+p
					+ str(round((kh_w_top-kh_w_bot)*100/kh_water_max,1))+p
					+ str(round((kh_b_top-kh_b_bot)*100/kh_brine_max,1)))
			file_txt.write(rzone+" "+str(round(deptzone,1))+"-"+
						   str(round(DeptZone.value(j+1),1))+" "+
						   str(round((kh_o_top-kh_o_bot)*100/kh_oil_max,1))+" "+
						   str(round((kh_w_top-kh_w_bot)*100/kh_water_max,1))+" "+
						   str(round((kh_b_top-kh_b_bot)*100/kh_brine_max,1))+"\r\n")
	file_txt.write("\r\n"+"Well Zones"+"\r\n")
	print ""
	for j in range(0,ZonesSize-1):
		zone=ZONE.value(j)
		if zone=="AS9.0": rzone="АС9"
		if zone=="AS10.0": rzone="АС10"
		elif zone=="AS11.1": rzone="АС11(1)"
		elif zone=="AS11.2": rzone="АС11(2)"
		elif zone=="AS11.3.1": rzone="АС11(3-1)"
		elif zone=="AS11.3.2": rzone="АС11(3-2)"
		elif zone=="AS11.3": rzone="АС11(3)"
		elif zone=="Prodelta": rzone="Продельта"
		elif zone=="АС9".decode("utf-8"):  rzone="AC9"
		elif zone=="АС9-2".decode("utf-8"): rzone="AC9(2)"
		elif zone=="АС10-1".decode("utf-8"):  rzone="AC10(1)"
		elif zone=="АС10-2".decode("utf-8"):  rzone="AC10(2)"
		elif zone=="АС11-1".decode("utf-8"):  rzone="AC11(1)"
		elif zone=="АС11-2".decode("utf-8"): rzone="AC11(2)"
		elif zone=="АС11-2б".decode("utf-8"): rzone="AC11(2б)"
		elif zone=="АС11-3".decode("utf-8"): rzone="AC11(3)"
		elif zone=="AS9":  rzone="AC9"
		elif zone=="AS9-2": rzone="AC9(2)"
		elif zone=="AS10-1":  rzone="AC10(1)"
		elif zone=="AS10-2":  rzone="AC10(2)"
		elif zone=="AS11-1":  rzone="AC11(1)"
		elif zone=="AS11-2": rzone="AC11(2)"
		elif zone=="AS11-2b": rzone="AC11(2б)"
		elif zone=="AS11-3": rzone="AC11(3)"
		elif zone=="BS8":  rzone="BS(8)"
		elif zone=="BS8_SH": rzone="BS(8SH)"
		elif zone=="ACH1":  rzone="ACH1"
		elif zone=="ACH2":  rzone="ACH2"
		elif zone=="ACH3":  rzone="ACH3"
		elif zone=="ACH4": rzone="ACH4"
		elif zone=="ACH5": rzone="ACH5"
		
		print rzone, str(round(deptzone,1))+"-"+str(round(DeptZone.value(j+1),1))
		file_txt.write(rzone+" "+str(round(DeptZone.value(j),1))+"-"+str(round(DeptZone.value(j+1),1))+"\r\n")
#---------Create Split dataset-----------------------------------------------------------------------------------------------
#Блок автоматического заполнения свойст датасета REPORT_SPLIT 
	ds_report = "REPORT_SPLIT"
	count = 1
	while db.datasetExists(WELL, ds_report + "_" + str(count)):
		count += 1
	ds_report_prev = ds_report + "_" + str(count-1)
	print ds_report_prev
	wt_list = ["p","i"]
	if ds_report_prev == "REPORT_SPLIT_0":
		pass
	else: 
		well_type = db.datasetPropertyValue(WELL,ds_report_prev,"Well type")
		if well_type=="Producer":
			wt="p"
			wt_list = ["p","i"]
		if well_type=="Injector":
			wt="i"
			wt_list = ["i","p"]
		myDialog.addListInput("Well type", "Well type", wt_list)
	dlist=db.variableData(WELL,"COMMON_05","DEPT")
	myDialog = TDA.dialogAdvanced("Dataset Header Properties")
	myDialog.addTextInput("DS", "SPLIT DATASET #", str(count))
	myDialog.addListInput("Well type", "Well type", wt_list)
	myDialog.addTextInput("Date", "Interpretation Date(dd.mm.yy)", date)
	list_comments = (["Completion","Add perf",
					   "Conv to inj","Isolation", 
					   "Correction","I've my own comment..."])
	myDialog.addListInput("Comments", "Comments", list_comments)
	myDialog.addTextInput("Text", "Comments", "Add your comment...")
	if myDialog.execDialog():
		SDS=(myDialog.getTextInput("DS"))
		NSDS="REPORT_SPLIT_"+SDS
		date=(myDialog.getTextInput("Date"))
		type=(myDialog.getListInput("Well type"))
		if type=="p":
			nt="Producer"
		if type=="i":
			nt="Injector"
		comments=(myDialog.getListInput("Comments"))
		text=(myDialog.getTextInput("Text"))
		if comments == "I've my own comment...":
			end_comments = text
		else:
			end_comments = comments 
		db.datasetCreate(WELL,NSDS,"DEPT","Measured Depth","m",dlist)
		db.datasetPropertyChange(WELL,NSDS,"Date",date,"","Interpretation date (dd.mm.yy)")
		db.datasetPropertyChange(WELL,NSDS,"Well type",nt,"","Well type @ interpretation date")
		db.datasetPropertyChange(WELL,NSDS,"Logging Company","","","Contractor Name")
		db.datasetPropertyChange(WELL,NSDS,"Tool","","","Logging tool")
		db.datasetPropertyChange(WELL,NSDS,"Q","","m3","Liquid rate during PLT job")
		db.datasetPropertyChange(WELL,NSDS,"WC","","%","BSW during PLT job")
		db.datasetPropertyChange(WELL,NSDS,"Trigger","Perf","","PLT; BSW; New perforations; Analysis")
		db.datasetPropertyChange(WELL,NSDS,"LQC","","%","Log Quality Contorl")
		db.datasetPropertyChange(WELL,NSDS,"Comments",end_comments,"","Any operational comments. Print No if there is no any")
		db.variableCopy(WELL,DS,"PERF_FINAL",NSDS,"PERF_FINAL")
		db.variableCopy(WELL,DS,"Flowing",NSDS,"Flowing")
		wt=db.datasetPropertyValue(WELL,NSDS,"Well type")
		print "\n",wt
		if wt=="Injector":
			db.variableCopy(WELL,DS,"%_brine",NSDS,"%_water")
			_Oil=Variable(WELL,NSDS,"%_oil")
			_Oil.familyNameChange("Integrated Oil Flow")
			_Oil.save()
		else:
			db.variableCopy(WELL,DS,"%_oil",NSDS,"%_oil")
			db.variableCopy(WELL,DS,"%_water",NSDS,"%_water")
	db.variableDelete(WELL,DS,"%_oil")
	db.variableDelete(WELL,DS,"%_water")
	db.variableDelete(WELL,DS,"%_brine")
	file_txt.write("\r\n")
	file_txt.write("перфорация перед ГРП"+"\r\n")
	file_txt.write("освоение после ГРП"+"\r\n")
	file_txt.write("пересчет после ПГИ"+"\r\n")
	file_txt.write("освоение"+"\r\n")
	file_txt.write("дострел"+"\r\n")
	file_txt.write("перевод в ППД"+"\r\n")
	file_txt.write("изоляция интервала"+"\r\n")
	file_txt.write("корректировка")
#----Вывод на экран диаграммы по скважину-------------------------------------------------------------
	well = WELL
	cbl = "CBL"
	if db.datasetExists(well,cbl):
		if db.variableExists(well,cbl,"BI"):
			id = tp.logViewApplyTemplate("User\PPeval_CBL_BI",well,0)
			tp.logViewSetName(id,well)
			print "User\PPeval_CBL_BI"
		elif db.variableExists(well,cbl,"ALFK"):
			id = tp.logViewApplyTemplate("User\PPeval_CBL_ALFK",well,0)
			tp.logViewSetName(id,well)
			print "User\PPeval_CBL_ALFK"
		elif db.variableExists(well,cbl,"CMT"):
			id = tp.logViewApplyTemplate("User\PPeval_CBL_CMT",well,0)
			tp.logViewSetName(id,well)
			print "User\PPeval_CBL_CMT"
		else:
			print "Проверьте датасет CBL"
#----Закрытие текстового файла с результатами и открытие таблицы OIS_data-----------------------------
file_txt.close()
os.startfile(file_path)
os.startfile("C:\Apps\Routine\OIS\OIS_data.xlsx")

__author__ = """Maria PEREZHOGINA (MPerezhogina)"""
__date__ = """2012-03-23"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""