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
import TechlogDialogAdvanced as tda
import Techlog
import TechlogStat as ts

#Функция формирует переменные cut и Index_flag на основании записаных в свойства скважины
#граничных значений
def create_index_var(well,ds):
	try:
		thres_dens = float(db.wellPropertyValue(well,"High dens flag, Ohm.m"))
		thres_oilwater = float(db.wellPropertyValue(well,"Oil+water flag, Ohm.m"))
		thres_non_res = float(db.wellPropertyValue(well,"Non res flag, gAPI"))
		t1 =  float(db.wellPropertyValue(well,"T1, m"))
		t2 =  float(db.wellPropertyValue(well,"T2, m"))
	except ValueError:
		print "Укажите граничные значения"
	res = db.variableData(well,"LAS","RES_PH2")
	gr = db.variableData(well,"LAS","GR")
	md = db.variableData(well,"LAS",db.referenceName(well,"LAS"))
	func = lambda x: round(x,0)
	md = map(func, md)
	md_zone = db.variableData(well,"ZONATION",db.referenceName(well,"ZONATION"))
	if db.variableExists(well,ds,"cut"):
		print "Cut существует"
	else:
		cut = []
		for i in range(len(md)):
			cut.append(MissingValue)
		db.variableSave(well,ds,"cut","General Flag","unitless",cut)
		print "Cut создан"
	cut = db.variableData(well,ds,"cut")
	index_flag = []
	litho_flag = []
	res_count = 0
	oil_water_count = 0
	non_res_count = 0
	ind1 = md.index(md_zone[0])
	ind2 = res.index(-9999.0,ind1)
	for i in range(len(md)):
		index_flag.append(MissingValue)
		litho_flag.append(MissingValue)
	for i in range(ind1,ind2):
		#нефтяная зона
		if   res[i] <= thres_dens and \
			 res[i] >= thres_oilwater and \
			 gr[i] <= thres_non_res:
			 index_flag.pop(i)
			 index_flag.insert(i,1)
			 litho_flag.pop(i)
			 litho_flag.insert(i,1)
			 res_count += md[1] - md[0]
		#водонефтяная зона
		elif res[i] <= (thres_oilwater) and \
			 gr[i] <= thres_non_res:
			 index_flag.pop(i)
			 index_flag.insert(i,2)
			 litho_flag.pop(i)
			 litho_flag.insert(i,1)
		#водяная зона
		elif res[i] <= (thres_oilwater-2) and \
			 gr[i] <= thres_non_res:
			 index_flag.pop(i)
			 index_flag.insert(i,3)
			 litho_flag.pop(i)
			 litho_flag.insert(i,1)
		#глина
		elif gr[i] >= thres_non_res:
			 litho_flag.pop(i)
			 litho_flag.insert(i,2)
		#карбонат
		elif res[i] >= (thres_dens) and \
			 gr[i] <= thres_non_res:
			 litho_flag.pop(i)
			 litho_flag.insert(i,3)
		else:
			 index_flag.pop(i)
			 index_flag.insert(i,MissingValue)
		if  cut[i] == 1:
			index_flag.pop(i)
			index_flag.insert(i,MissingValue)
	db.variableSave(well,ds,"Litho_flag","Net Reservoir Flag","unitless",litho_flag)
	db.variableSave(well,ds,"Index_flag","Saturation_Index","unitless",index_flag)
	print "Index_flag посчитан и сохранен"


def add_trajectory(well):
	dialog = tda.dialogAdvanced("Wellpath")
	wellpath_list = []
	for ds in db.datasetList(well):
		if "_WellPath" in ds:
			wellpath_list.append(ds)
	dialog.addButtonsGroup("wlp","Trajectories",wellpath_list,1)
	dialog.execDialog()
	results = dialog.getButtonsGroup("wlp")
	return results


def add_ph2_threshold(well):
	if db.variableExists(well,"LAS","RES_PH2"):
		thres_oilwater = float(db.wellPropertyValue(well,"Oil+water flag, Ohm.m"))
		db.variableDuplicate(well,"LAS","RES_PH2","res_ph2_threshold")
		res_ph2_threshold = map(lambda x:x*0+thres_oilwater,db.variableData(well,"LAS","res_ph2_threshold"))
		db.variableSave(well,"LAS","res_ph2_threshold","","ohm.m",res_ph2_threshold)
		print "Граничное значение резистивити создано"
	else:
		print "Переменная RES_PH2 отсутствует"
		pass
	
	
def gaussian_smooth(well):
	smooth_window = int(db.wellPropertyValue(well,"GausianSmooth, pnt").split(".")[0])
	if db.variableExists(well,"LAS","GR_orig"):
		print "Перемнная GR_orig существует"
		pass
	else:
		gr = db.variableData(well,"LAS","GR")
		db.variableDuplicate(well,"LAS","GR","GR_orig")
		gr_gaus = ts.gaussianSmooth(gr,smooth_window)
		db.variableSave(well,"LAS","GR","Gamma Ray","gAPI",gr_gaus)
		print "Переменная GR отфильтрована по окну", smooth_window
	
#Запускается формирование диаграммы + выполняется функция по расчету индекса насыщения
for well in db.selectedWellList():
	ds = "LAS"
#Запуск функции расчета насыщения	
	create_index_var(well,ds)
#Удаление предыдущей диаграммы,если она есть
	if tp.logViewGetIdByName("HRZ_LWD") < 0:
		pass
	else:
		id_last = tp.logViewGetIdByName("HRZ_LWD")
		tp.close(id_last,0)
		print "Предыдущая диаграмма удалена"
#Создание переменной граничного значения резистивити
	add_ph2_threshold(well)
	gaussian_smooth(well)
#Применение шаблона HRZ_LWD к данным из скважины и определение id шаблона
	tp.logViewApplyTemplate("User\HRZ_LWD",well,0)
	id = tp.logViewGetIdByName("HRZ_LWD")
##Объявление переменных для диаграммы
	tvdss = [well + ".Index.TVDSS"]
	tvdss_max = round(db.variableData(well,"ZONATION","TVDSS")[0],0) - 2
	tvdss_min = round(db.variableData(well,"ZONATION","TVDSS")[-1],0) + 2
	wellpath_list = add_trajectory(well)
	wellpath = [well + "." + wellpath_list[0] + ".TVDSS"]
#Расчет сколько метров осталось бурить	
	md_traj_total = db.variableData(well,wellpath_list[0], db.referenceName(well,wellpath_list[0]))[-1]
	md_current = db.variableData(well,"ZONATION", db.referenceName(well,"ZONATION"))[-1]
	db.wellPropertyChange(well,"T3, m", str(round(md_traj_total,0)), "m")
#TVDSS
	tp.logViewInsertTrackByWell(id,well,0,6)
	tp.logViewTrackSizeByWell(id,well,6,200)
	tp.logViewInsertVariable(id,tvdss,6)
	tp.logViewSetAxeLimitTypeByVariable(id,tvdss[0],1)
	tp.logViewSetMinMaxUserByVariable(id,tvdss[0],tvdss_max,tvdss_min,1)
	tp.logViewSetLineProperties(id,tvdss[0],1,1,2)
#Wellpath	
	tp.logViewInsertVariable(id,wellpath,6)
	tp.logViewSetAxeLimitTypeByVariable(id,wellpath[0],1)
	tp.logViewSetMinMaxUserByVariable(id,wellpath[0],tvdss_max,tvdss_min,1)
	tp.logViewSetLineProperties(id,wellpath[0],2,1,2)
	tp.logViewSetVariableColour(id,wellpath[0],50,205,50)
#Поворот заголовков вертикально на 4м треке	
	tp.logViewSetHeaderOrientation(id,[6],1)
	print "Диаграмма сформирована"
	print "Осталось бурить:", round(md_traj_total - md_current,0), " m"

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-07-11"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""