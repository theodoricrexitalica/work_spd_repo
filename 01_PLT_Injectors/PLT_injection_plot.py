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
import TechlogPlot as plot
import time
import TechlogGUIQt as tqt


template200 = "User\PLT_200"
template500 = "User\PLT_500"
ds_zone = "ZONATION"

for well in db.selectedWellList():
	id_plot = plot.logViewApplyTemplate(template200, well, 0)
	plt_data = []
	for ds in db.datasetList(well):
		if ds.startswith("PLT_") and not ds.startswith("PLT_Y"):
			for vars in db.variableList(well, ds):
				if vars.startswith("WTEP"):
					db.variableFamilyChange(well, ds, vars, "Borehole Temperature")
			try:
				date = time.strptime(ds.split("_")[-1], "%b%y")
				plt_data.append(date)
			except:
				continue
	plt_data.sort()
	n = 0

#Временный датасет для даты и объема закачки
	ZONE = Variable(well, ds_zone, "ZONES")
	dept_zone = db.datasetZoneDetail(well, ds_zone, ZONE.value(0))
	plt_sign = "PLT_temp"
	ds_list = []							#Создается список ПЛТ-датасетов на всякий случай
	db.datasetCreate(well, plt_sign, "DEPT", "Measured Depth", "m", [dept_zone[0], dept_zone[1]])
	#for pdata in plt_data[-3:]:			#Печать 3х последних по дате диаграмм
	for pdata in plt_data:
		date_str = time.strftime("%b%y",pdata)
		ds_name = "PLT_" + date_str
		ds_list.append(ds_name)
		q = str(int(float(db.datasetPropertyValue(well,ds_name,"Q")))) #detection of injection rate into dataset propertys
		if not db.variableExists(well, plt_sign, date_str):
			values = [date_str + " " + q + "m3/d",""]
			db.variableSave(well, plt_sign, date_str, "Zone Description", " ", values)
	
	
#PERF_FINAL, QTZTP, %_water
		track_num =4 + n*3
		n += 1
		plot.logViewInsertTrackByWell(id_plot, well, 0, track_num)
		plot.logViewTrackSizeByWell(id_plot, well, track_num, 90)
		date_id = well + "." + plt_sign + "." + date_str
		plot.logViewInsertVariable(id_plot, date_id, track_num)
		water_id = well + "." + ds_name + ".%_water"
		plot.logViewInsertVariable(id_plot, water_id, track_num)
		plot.logViewSetVariableColour(id_plot, water_id, 0, 170, 255)
		plot.logViewSetLineProperties(id_plot, water_id, 2, 1, 1)
		qtztp_id = well + "." + ds_name + ".QTZTP"
		plot.logViewInsertVariable(id_plot, qtztp_id, track_num)
		plot.logViewSetVariableColour(id_plot, qtztp_id, 255, 0, 0)
		plot.logViewRemoveFill(id_plot,qtztp_id)
		plot.logViewSetAxeLimitTypeByVariable(id_plot, qtztp_id, 1)
		plot.logViewSetMinMaxUserByVariable(id_plot, qtztp_id, 0, 100, False)
		plot.logViewZonationAreaFilling(id_plot, 0)
		plot.logViewInsertVariable(id_plot, well + "." + ds_name + ".PERF_FINAL", track_num)
				
#Flowing
		if db.variableExists(well, ds_name, "Flowing"):
			track_num += 1
			plot.logViewInsertTrackByWell(id_plot, well, 0, track_num)
			plot.logViewTrackSizeByWell(id_plot, well, track_num, 20)
			plot.logViewInsertVariable(id_plot, well + "." + ds_name + ".Flowing", track_num)
		
#WTEP + покраска кривых по имени кривой
		wtep_list = db.variableListByFamily(well, ds_name, "Borehole Temperature")
		if wtep_list:
			track_num += 1
			plot.logViewInsertTrackByWell(id_plot, well, 0, track_num)
			plot.logViewTrackSizeByWell(id_plot, well, track_num, 300)
		wtep_list.sort()
		for wtep in wtep_list:
			var_id =  well + "." + ds_name + "." + wtep
			plot.logViewInsertVariable(id_plot, var_id, track_num)
			plot.logViewSetAxeLimitTypeByVariable(id_plot, var_id, 1)
			plot.logViewSetMinMaxUserByVariable(id_plot, var_id, 50, 90, False)
			if wtep == "WTEP_G":
				plot.logViewSetLineProperties(id_plot, var_id, 2, 1, 1)
				plot.logViewSetVariableColour(id_plot, var_id, 255, 0, 0)
			elif wtep == "WTEP_B":
				plot.logViewSetLineProperties(id_plot, var_id, 1, 1, 2)
				plot.logViewSetVariableColour(id_plot, var_id, 0, 0, 0)
			elif wtep == "WTEP_1":
				plot.logViewSetLineProperties(id_plot, var_id, 1, 1, 1)
				plot.logViewSetVariableColour(id_plot, var_id, 0,170,255)
			elif wtep == "WTEP_2":
				plot.logViewSetLineProperties(id_plot, var_id, 1, 1, 1)
				plot.logViewSetVariableColour(id_plot, var_id, 0,0,255)
			elif wtep == "WTEP_3":
				plot.logViewSetLineProperties(id_plot, var_id, 1, 1, 1)
				plot.logViewSetVariableColour(id_plot, var_id,128,128,128)
			elif wtep.endswith("_WI"):
				plot.logViewSetLineProperties(id_plot, var_id, 1, 1, 1)
				plot.logViewSetVariableColour(id_plot, var_id, 255, 0, 0)
			elif wtep.endswith("_WI_1"):
				plot.logViewSetLineProperties(id_plot, var_id, 1, 1, 1)
				plot.logViewSetVariableColour(id_plot, var_id, 255, 0, 0)
			elif wtep.endswith("_WI_2"):
				plot.logViewSetLineProperties(id_plot, var_id, 1, 1, 1)
				plot.logViewSetVariableColour(id_plot, var_id, 0, 190, 0)
#Сильно умный алгоритм, заточенный под последний знак в имени переменной
			#else:
				#try:
					#ver = int(wtep[-1])
				#except:
					#continue
				#if ver == 1:
					#clr = (0,170,255)
				#elif ver == 2:
					#clr = (0,0,255)
				#else:
					#clr = (128,128,128)
			#plot.logViewSetVariableColour(id_plot, var_id, clr[0], clr[1], clr[2])
	plot.logViewZonationAreaFilling(id_plot, 0, 0)
	date_str_last = time.strftime("%b%y",plt_data[-1])
	ds_name_last = "PLT_" + date_str_last
	gr_ch_id = well + "." + ds_name_last + ".GR_CH"
	plot.logViewInsertVariable(id_plot, gr_ch_id, 1)
	plot.logViewSetVariableColour(id_plot, gr_ch_id, 0, 190, 0)
	plot.logViewSetLineProperties(id_plot, gr_ch_id, 1, 1, 2)
	plot.logViewSetLayoutScale(id_plot,500)
#Счетчик для поиска последнего датасета с ПЛТ500
	plt_data = []
	for ds in db.datasetList(well):
		if ds.startswith("PLT500_"):
			#print ds
			try:
				date = time.strptime(ds.split("_")[-1], "%b%y")
				plt_data.append(date)
			except:
				continue
	plt_data.sort()
	ds_name_list = []
	for pdata in plt_data:
		date_str = time.strftime("%b%y",pdata)
		ds_name = "PLT500_" + date_str
		ds_name_list.append(ds_name)
	ds=ds_name_list[-1]

#Отображение ПЛТ500 с использованием темплейта
	wtep_b = well + "." + ds_list[-1] + "." + "WTEP_B"
	t_b = well + "." + ds + "." + "T_s"
	plot.logViewApplyTemplate(template500,well + "_" + ds,1)
	id_plot = plot.logViewGetIdByName("PLT_500")
	plot.logViewInsertVariableInTrack(id_plot,t_b,wtep_b)
	plot.logViewSetAxeLimitTypeByVariable(id_plot,wtep_b,1)
	plot.logViewSetLineProperties(id_plot,wtep_b,1,1,2)
	plot.logViewSetMinMaxUserByVariable(id_plot,wtep_b,0,100,0)
	
	

__author__ = """Maria PEREZHOGINA (MPerezhogina)"""
__date__ = """2012-03-22"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""