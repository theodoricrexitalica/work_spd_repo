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
import win32com.client as win32
import pythoncom
pythoncom.CoInitialize()
import webbrowser
import time
import TechlogPlot as tp
import shutil


def folder_path(well):
	#Создание папки для эксель-отчета
	path = r"C:\Apps\Routine\PLT" + "\\" + "Y_" + "-".join(well.split("-")[:2])
	if os.path.exists(path) == True:
		print "Папка скважины уже существует"
		pass
	else:
		os.mkdir(path)
		print "Папка скважины",well, "создана"
	return(path)


def create_xls(well,ds,path):
	#Создание эксель-файла
	create_report_xl = open(path + "\\" + "Y_" + "-".join(well.split("-")[:2]) + \
							"_" + (ds.split("_")[2]) + ".xls", "w")
	create_report_xl.close()
	report_xl_file =path + "\\" + "Y_" + "-".join(well.split("-")[:2]) + \
					"_" + (ds.split("_")[2]) + ".xls"
	xl = win32.Dispatch("Excel.Application")
	xl.Visible = 1
	wb = xl.Workbooks.Open(report_xl_file)
	wb.Sheets(1).Name = "PLT_Y-TOOL"
	return(wb, xl)


def borders(wb,i, j, di, dj):
	#Отрисовка границ таблицы
	sheet = wb.Sheets(1)
	sheet.Range(sheet.Cells(i,j), sheet.Cells(i+di, j+dj-1)).Borders.LineStyle = 1
	sheet.Range(sheet.Cells(i,j), sheet.Cells(i+di, j+dj-1)).HorizontalAlignment = 3
	sheet.Range(sheet.Cells(i,j), sheet.Cells(i+di, j+dj-1)).VerticalAlignment = 2
	sheet.Range(sheet.Cells(i,j), sheet.Cells(i+di, j+dj-1)).BorderAround(1,3,1)
	sheet.Range(sheet.Cells(i,j), sheet.Cells(i, j+dj-1)).BorderAround(1,3,1)
	sheet.Range(sheet.Cells(i,j), sheet.Cells(i, j+dj)).Font.Bold = True
	sheet.Range(sheet.Cells(i,j), sheet.Cells(i, j+dj)).Font.Size = 12
	sheet.Range(sheet.Cells(i,j), sheet.Cells(i, j+dj-1)).Interior.ColorIndex = 35
	sheet.Range(sheet.Cells(i,j), sheet.Cells(i, j+dj-1)).ColumnWidth = 13.4
	sheet.Range(sheet.Cells(i,j+1), sheet.Cells(i+di,j+1)).WrapText = True
	sheet.Range(sheet.Cells(i+1,j), sheet.Cells(i+1,j+dj)).WrapText = True


def report(path,wb,xl,well):
	brk = "\t"
	wb.Sheets(1).Range("A1").Select()
	header = ["Zones", "Perf, MD","Oil, m3/d", "Oil, %", "Water, m3/d","Water, %", "Gas, m3/d","Gas, %" ]
	ds_zone = "ZONATION"
	ZONE = db.variableData(well, ds_zone, "ZONES")
	plt_list = ["PLT_Y"]
	for ds in plt_list:
		ds_index = 1
		table_start = 33
		oil = db.variableData(well, ds, "IFLOoil")
		water = db.variableData(well, ds, "IFLOw")
		gas = db.variableData(well, ds, "IFLOg")
		zone_size = db.datasetSize(well, ds_zone)
		perf = db.variableData(well,ds,"PERF_FINAL")
		perf_md = db.variableData(well,ds,db.referenceName(well,ds))
		dept_md = db.variableData(well, ds, db.referenceName(well,ds))
		print "Максимум Oil", round(max(oil),2)
		if round(max(oil),2) == 0: 
			max_oil = 0.00001 
		else: max_oil = round(max(oil),2)
		print "Максимум Water", round(max(water),2)
		if round(max(water),2) == 0: 
			max_water = 0.00001 
		else: max_water = round(max(water),2)
		print "Максимум Gas", round(max(gas),2)
		if round(max(gas),2) == 0: 
			max_gas = 0.00001 
		else: max_gas = round(max(gas),2)
		for i in xrange(zone_size):
			ind = db.datasetZoneIndice(well, ds, ds_zone, ZONE[i])
			dept_border = db.datasetZoneDetail(well, ds_zone,  ZONE[i])
			if not ind or dept_border[0] == MissingValue or dept_border[1] == MissingValue:
				continue
			#Определение интервало перфорация по PERF_FINAL в датасете с Y-Tool
			perf_list = []
			for k in xrange(ind[0],ind[1]):
				if perf[k-1] != 2 and perf[k] == 2:
					top_perf = round(perf_md[k],1)
				if perf[k-1] == 2 and perf[k] != 2:
					bot_perf = round(perf_md[k-1],1)
					perf_list.append(str(top_perf) + "-" + str(bot_perf))
			#Заполнение таблицы Эксель
			wb.Sheets(1).Cells(i+table_start,ds_index+0).Value = ZONE[i]
			wb.Sheets(1).Cells(i+table_start,ds_index+1).Value = " ".join(perf_list)
			wb.Sheets(1).Cells(i+table_start,ds_index+2).Value = round(oil[ind[0]]-oil[ind[1]],1)
			wb.Sheets(1).Cells(i+table_start,ds_index+3).Value = round(((oil[ind[0]]-oil[ind[1]])/max_oil)*100,0)
			wb.Sheets(1).Cells(i+table_start,ds_index+4).Value = round(water[ind[0]]-water[ind[1]],1)
			wb.Sheets(1).Cells(i+table_start,ds_index+5).Value = round(((water[ind[0]]-water[ind[1]])/max_water)*100,0)
			wb.Sheets(1).Cells(i+table_start,ds_index+6).Value = round(gas[ind[0]]-gas[ind[1]],1)
			wb.Sheets(1).Cells(i+table_start,ds_index+7).Value = round(((gas[ind[0]]-gas[ind[1]])/max_gas)*100,0)
		for k in xrange(len(header)):
			wb.Sheets(1).Cells(table_start-1,ds_index+k).Value = header[k]
		borders(wb, table_start-1, ds_index, i, len(header))


def print_pict(well):
	id=tp.logViewGetIdByName("PLT_Y_Tool")
	tp.printPlot(id)


for well in db.wellList():
	for ds in db.selectedDatasetList(well):
		path = folder_path(well)
		wb, xl = create_xls(well,ds,path)
		report(path,wb,xl,well)
		print_pict(well)
		webbrowser.open(path)
		shutil.copy("C:\\Apps\Routine\PLT\\LQC_PLT_Y.xlsx",path)

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-09-04"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""