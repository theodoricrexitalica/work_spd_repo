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

id = tp.logViewGetIdByName("OIS_Check")
if id != -1:
	tp.close(id,0)
	print "Диаграмма закрыта"
else:
	pass

ZDS = "ZONATION"
LIST=db.selectedWellList()
DS="COMMON_05"
p=" ;  "
for j in db.selectedWellList():
	WELL=j
	print WELL
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
	#KH_tvd_oil.save()
	#KH_tvd_water.save()
	#KH_brine.save()
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
	print"zone          top_bot        oil   water   brine_WI"
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

	#----Split based on KH_perf -------------------------------------------------------------------------------------
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
					+ str(round((kh_o_top-kh_o_bot)*100/kh_oil_max,0))+p
					+ str(round((kh_w_top-kh_w_bot)*100/kh_water_max,0))+p
					+ str(round((kh_b_top-kh_b_bot)*100/kh_brine_max,0)))
	tp.logViewApplyTemplate("User\\OIS_Check", WELL, 0)

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2017-10-28"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""