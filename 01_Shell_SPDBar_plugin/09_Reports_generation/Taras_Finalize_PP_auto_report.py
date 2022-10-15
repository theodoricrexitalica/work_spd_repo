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
from os import listdir, remove
import pythoncom
pythoncom.CoInitialize()
import win32com.client as win32
from sys import path
import TechlogPlot as tp
import TechlogStat as ts

def folder_path(well):
	path = r"C:\Apps\Routine\PP_eval" + "\\" + well
	if os.path.exists(path) == True:
		print "Папка скважины уже есть"
		pass
	else:
		os.mkdir(path)
		print "Папка скважины создана"
	return(path)

def report_creation(well,path):
	create_report_xl = open(path + "\\" + well + ".xls", "w")
	create_report_xl.close()
	report_xl_file = path + "\\" + well + ".xls"
	xl = win32.Dispatch("Excel.Application")
	xl.Visible = 1
	wb = xl.Workbooks.Open(report_xl_file)
	wb.Sheets(1).Name = "Depth plot"
	print "Файл отчета создан"
	return(wb)
		
def counter_zones(well):
	ds = "COMMON_05"
	zn = "ZONATION_PARAMETRS"
	zones = db.variableData(well, zn, "ZONE") #считаем сколько зон в отчете 
	q_zones = 0
	for i in zones:
		if i.startswith("AS"):
			q_zones +=1
	print "Количество зон @ " + str(q_zones)
	return(q_zones)

def draw_table(quantity_zones,wb):
	wb = wb.Sheets(1)
	wb.Range("A1:N59").BorderAround(1,3,1)		#рисуем глобальный контур 
	wb.Range("A55:D56").BorderAround(1,3,1)		#и все неизменные контуры
	wb.Range("E55:N55").BorderAround(1,3,1)
	wb.Range("E56:I56").BorderAround(1,3,1)
	wb.Range("J56:N56").BorderAround(1,3,1)
	wb.Range("E57:I59").BorderAround(1,3,1)
	
	
	#рисуем те контуры,которые зависят от кол-во зон в отчете 
	x = quantity_zones
	coord = ["B60","N" + str(59+x)]
	scope =":".join(coord)
	wb.Range(scope).BorderAround(1,3,1)
	
	coord = ["E60","I" + str(59+x+1)]
	scope =":".join(coord)
	wb.Range(scope).BorderAround(1,3,1)
	
	coord = ["A60","A" + str(59+x+1)]
	scope =":".join(coord)
	wb.Range(scope).BorderAround(1,3,1)
	
	coord = ["B" + str(59+x+1),"N" + str(59+x+1)]
	scope =":".join(coord)
	wb.Range(scope).BorderAround(1,3,1)
	
	coord = ["K60","K" + str(59+x+1)]
	scope =":".join(coord)
	wb.Range(scope).BorderAround(1,3,1)
	
	coord = ["M60","M" + str(59+x+1)]
	scope =":".join(coord)
	wb.Range(scope).BorderAround(1,3,1)
	
	coord = ["F60","F" + str(59+x+1)]
	scope =":".join(coord)
	wb.Range(scope).BorderAround(1,3,1)
	
	coord = ["H60","H" + str(59+x+1)]
	scope =":".join(coord)
	wb.Range(scope).BorderAround(1,3,1)
	
	coord = ["E" + str(59+x+1)]
	scope =":".join(coord)
	formula = "=sum(" + "E" + str(60) + ":" + "E" + str(59+x) + ")"
	wb.Range(scope).Formula = formula
	
	coord = ["F" + str(59+x+1)]
	scope =":".join(coord)
	formula = "=average(" + "F" + str(60) + ":" + "F" + str(59+x) + ")"
	wb.Range(scope).Formula = formula
	
	coord = ["G" + str(59+x+1)]
	scope =":".join(coord)
	formula = "=average(" + "G" + str(60) + ":" + "G" + str(59+x) + ")"
	wb.Range(scope).Formula = formula
	
	br = ""
	for i in range(x):
		coord = ["H" + str(60+i)]
		scope =":".join(coord)
		formula = "=(" + "E" + str(60+i) + "*" + "F" + str(60+i) + "*" + "G" + str(60+i) + ")"
		wb.Range(scope).Formula = formula
		
	coord = ["H" + str(59+x+1)]
	scope =":".join(coord)
	formula = "=sum(" + "H" + str(60) + ":" + "H" + str(59+x) + ")"
	wb.Range(scope).Formula = formula
	
	#Отрисовка отчетной таблицы на 1й странице
	wb.Cells(57,1).Value = "Well"
	wb.Cells(57,2).Value = "ZONE"
	wb.Cells(57,3).Value = "ZONE"
	wb.Cells(57,4).Value = "ZONE"
	wb.Cells(58,2).Value = "NAME"
	wb.Cells(58,3).Value = "TOP"
	wb.Cells(58,4).Value = "BASE"
	wb.Cells(59,3).Value = "(m TVDSS)"
	wb.Cells(59,3).Font.Size = 10
	wb.Cells(59,4).Value = "(m TVDSS)"
	wb.Cells(59,4).Font.Size = 10
	wb.Cells(56,7).Value = "Model predicted Net Pay non swept"
	wb.Cells(56,7).WrapText = False
	wb.Cells(56,12).Value = "Net Pay non swept"
	wb.Cells(56,12).WrapText = False
	wb.Cells(55,9).Value = "NON SWEPT NET PAY m TVDSS"
	wb.Cells(55,9).WrapText = False
	
	wb.Cells(57,5).Value ="NET"
	wb.Cells(57,6).Value ="AVG"
	wb.Cells(57,7).Value ="AVG"
	wb.Cells(57,8).Value ="EHC"
	wb.Cells(57,9).Value ="Kh"
	wb.Cells(58,5).Value ="PAY"
	wb.Cells(58,6).Value ="PHI"
	wb.Cells(58,7).Value ="Sh"
	wb.Cells(59,5).Value ="(m)"
	wb.Cells(59,6).Value ="(frac)"
	wb.Cells(59,7).Value ="(frac)"
		
	wb.Cells(57,10).Value ="NET"
	wb.Cells(57,11).Value ="AVG"
	wb.Cells(57,12).Value ="AVG"
	wb.Cells(57,13).Value ="EHC"
	wb.Cells(57,14).Value ="Kh"
	wb.Cells(58,10).Value ="PAY"
	wb.Cells(58,11).Value ="PHI"
	wb.Cells(58,12).Value ="Sh"
	wb.Cells(59,10).Value ="(m)"
	wb.Cells(59,11).Value ="(frac)"
	wb.Cells(59,12).Value ="(frac)"
	
	for x in range(1,15):
		for y in range(55,59):
			wb.Cells(y,x).Font.Bold = True

	for x in range(1,15):
		for y in range(55,66):
			wb.Cells(y,x).HorizontalAlignment = 3
	
	wb.Range("E55:N55").Interior.ColorIndex = 34
	wb.Range("A57:D59").Interior.ColorIndex = 34
	wb.Range("E56:I59").Interior.ColorIndex = 35
	wb.Range("J56:N59").Interior.ColorIndex = 34
	
	print "Таблица отрисована"

def final_report(well,quantity_zones,wb):
	wb = wb.Sheets(1)
	ds="ZONATION_PARAMETRS"
	if db.datasetExists(well,ds)==False:
		print "Please create dataset <", ds, ">"
		return -1
	vTOP_tvdss = db.variableData(well, ds, "TOP_tvdss")
	vBOT_tvdss= db.variableData(well, ds, "BOT_tvdss")
	vNET_NP= db.variableData(well, ds, "NET_NP")
	vZONE = db.variableData(well, ds, "ZONE")
	vPHI_NP= db.variableData(well, ds, "PHI_NP")
	vSo_WS_NP= db.variableData(well, ds, "So_WS_NP")
	vKbr_NP= db.variableData(well, ds, "Kbr_NP")
	
	j = 59
	y = quantity_zones	
	wb.Cells(60,1).Value=str(well.split("-")[0] \
							+ "-" + \
							 well.split("-")[1])
	sum_NET = []
	sum_PHI = []
	sum_So = []
	sum_EHC = []
	sum_KH = []
	for i in range(1,y+1):
		wb.Cells(j+i,2).Value=str(vZONE[i])
		wb.Cells(j+i,3).Value=str(round(vTOP_tvdss[i],1))
		wb.Cells(j+i,4).Value=str(round(vBOT_tvdss[i],1))
		wb.Cells(j+i,10).Value=str(round(vNET_NP[i],1))
		sum_NET.append(round(vNET_NP[i],1))
		wb.Cells(j+i,11).Value=str(round(vPHI_NP[i],2))
		sum_PHI.append(round(vPHI_NP[i],2))
		wb.Cells(j+i,12).Value=str(round(vSo_WS_NP[i],2))
		sum_So.append(round(vSo_WS_NP[i],2))
		wb.Cells(j+i,13).Value=str(round(vNET_NP[i]*vPHI_NP[i]*vSo_WS_NP[i],2))
		sum_EHC.append(vNET_NP[i]*vPHI_NP[i]*vSo_WS_NP[i])
		wb.Cells(j+i,14).Value=str(round(vNET_NP[i]*vKbr_NP[i],0))
		sum_KH.append(round(vNET_NP[i]*vKbr_NP[i],0))
		
	wb.Cells(j+y+1,2).Value = "Total"
	wb.Cells(j+y+1,10).Value = round(ts.sum(sum_NET),2)
	sum_PHI = filter(lambda x: x>0, sum_PHI)
	wb.Cells(j+y+1,11).Value = round(ts.average(sum_PHI),2)
	sum_So = filter(lambda x: x>0, sum_So)
	wb.Cells(j+y+1,12).Value = round(ts.average(sum_So),2)
	wb.Cells(j+y+1,13).Value = round(ts.sum(sum_EHC),2)
	wb.Cells(j+y+1,14).Value = round(ts.sum(sum_KH),0)
	print "Отчет готов"


def insert_1plot(well,path,wb):
	pict_path = path + "\\" + well+".png"
	if os.path.exists(pict_path) == True:
		Sheet = wb.Sheets(1)
		Sheet.Activate()
		Sheet.Range("A1").Select()
		Sheet.Shapes.AddPicture(pict_path, False, True,2,2,671,776)
		print "Диаграмма добавлена"
	else:
		print "Нет скважинной диаграммы в папке"


for well in db.selectedWellList():
	path = folder_path(well)
	wb = report_creation(well,path)
	quantity_zones = counter_zones(well)
	draw_table(quantity_zones,wb)
	final_report(well,quantity_zones,wb)
	insert_1plot(well,path,wb)

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-02-23"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""