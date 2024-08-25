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
import numpy as np
import TechlogPlot as tp
import TechlogDialogAdvanced as tda


def check_miss_val(data):
	if data == MissingValue:
		data = 0
	else:
		data = data
	return data


def perf_copy(well):
	splits_list = []
	for i in db.datasetList(well):
		if i.startswith("REPORT_SPLIT"):
			splits_list.append(i + "-->" + db.datasetPropertyValue(well,i,"Date"))
	dialog = tda.dialogAdvanced("PLT_Y-Tool")
	dialog.addListBox("list","Выбор датасета",splits_list)
	dialog.execDialog()
	split_source = dialog.getListBox("list")
	split_source = split_source[0].split("-->")[0]
	print "Датасет", split_source, "для PLT_Y найден"
	return split_source

def plt_y_zone(well):
	plt_y_zone = "PLT_Y_ZONE"
	ds = "PLT_Y"
	db.datasetDuplicate(well,"ZONATION",well,plt_y_zone)
	qo=db.variableData(well, ds,"IFLOoil")
	qw=db.variableData(well,ds,"IFLOw")
	qg=db.variableData(well,ds,"IFLOg")
	dept=db.variableData(well,ds,"DEPT")
	perf=db.variableData(well,ds,"PERF_FINAL")
	ZONES=db.variableData(well, "ZONATION", "ZONES")	
	qo_n=[MissingValue]*len(ZONES)
	max_o=round(max(qo),2)
	qw_n=[MissingValue]*len(ZONES)
	max_w=round(max(qw),2)
	qg_n=[MissingValue]*len(ZONES)
	max_g=round(max(qg),2)
	if max_g == 0:
		max_g = 0.00001
	for i in range (len(ZONES)):
		if  ZONES[i] == "Prodelta" or \
			ZONES[i] == "PIM" or \
			ZONES[i] == "Pim" or \
			ZONES[i] == "TD":
			pass
		else:
			index=db.datasetZoneIndice(well,ds, "ZONATION", ZONES[i])
		try:
			if 2 in perf[index[0]:index[1]]:	
				qo[index[1]] = check_miss_val(qo[index[1]])
				qw[index[1]] = check_miss_val(qw[index[1]])
				qg[index[1]] = check_miss_val(qg[index[1]])
				qo_split=qo[index[0]]-qo[index[1]]
				qw_split=qw[index[0]]-qw[index[1]]
				qg_split=qg[index[0]]-qg[index[1]]
				qo_p=(qo_split/max_o)*100
				qw_p=(qw_split/max_w)*100
				qg_p=(qg_split/max_g)*100
				qo_n[i]=qo_p
				qw_n[i]=qw_p
				qg_n[i]=qg_p
		except TypeError:
			pass
	qo_n = map(int,np.around(qo_n))
	qw_n = map(int,np.around(qw_n))
	qg_n = map(int,np.around(qg_n))
	o=[MissingValue]*len(ZONES)
	w=[MissingValue]*len(ZONES)
	g=[MissingValue]*len(ZONES)
	for j in range (len(qo_n)):
		if qo_n[j]>=0: o[j]=str(int(qo_n[j]))
		if qo_n[j]==MissingValue: o[j] = ""
		if qw_n[j]>=0: w[j]=str(int(qw_n[j]))
		if qw_n[j]==MissingValue: w[j] = ""
		if qg_n[j]>=0: g[j]=str(int(qg_n[j]))
		if qg_n[j]==MissingValue: g[j] = ""
	db.variableSave( well,plt_y_zone,"Split_o", "Ratio", "%", o, 0)
	db.variableTypeChange( well,plt_y_zone, "Split_o", "RichText")
	db.variableSave( well,plt_y_zone, "Split_w", "Ratio", "%", w, 0)
	db.variableTypeChange( well,plt_y_zone, "Split_w", "RichText")
	db.variableSave( well,plt_y_zone, "Split_g", "Ratio", "%", g, 0)
	db.variableTypeChange( well,plt_y_zone, "Split_g", "RichText")
	print "Датасет",plt_y_zone,"создан"
	ness_list = set(["Split_o", "Split_w", "Split_g","DEPTH"])
	zone_list = set(db.variableList(well,plt_y_zone))
	result_set =list(zone_list - ness_list)
	for i in result_set:
		db.variableDelete(well,plt_y_zone,i)
	print "Лишние переменные в",plt_y_zone,"удалены"

def plt_y(well,split_source):
	if db.datasetExists(well,"PLT_Y"):
		db.datasetDelete(well,"PLT_Y",1)
		print "Предыдущий датасует PLT_Y удален"
	else:
		print "Датасет PLT_Y еще не создан"
	dialog = tda.dialogAdvanced("PLT_Y-Tool")
	db.datasetDuplicate(well,ds,well,"PLT_Y")
	db.variableCopy(well,split_source,"%_oil","PLT_Y","%_oil")
	db.variableCopy(well,split_source,"%_water","PLT_Y","%_water")
	db.variableCopy(well,split_source,"PERF_FINAL","PLT_Y","PERF_FINAL")
	print "Переменные из", split_source, "скопированы"
	#Вызов функции для расчета зонейшена
	plt_y_zone(well)
	tp.logViewApplyTemplate("User\\PLT_Y_Tool",well, False)
	print "Диаграмма по датасету", "-".join(well.split("-")[:2]),"-",ds," создана"


for well in db.wellList():
	for ds in db.selectedDatasetList(well):
		split_source = perf_copy(well)
		plt_y(well,split_source)

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-09-01"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""