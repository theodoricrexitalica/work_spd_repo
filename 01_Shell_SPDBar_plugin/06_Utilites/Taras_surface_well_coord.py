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
#-*- coding: cp1251 -*-
import os
import pythoncom
pythoncom.CoInitialize()
import win32com.client as win32
import webbrowser

#Функция генерации пути для скважины на месторождении
def path_creation(well,field):
	pad = well.split("-")[2][1:4]
	well_folder = well.split("-")[:4]
	well_folder = "-".join(well_folder)
	if "ST" in well_folder:
		well_folder = well_folder.split("ST")[0] + "-ST"
	path_well = field + "\Pad " + pad + "\\" + well_folder + "\\1. DRILLING" + "\\Daily Geological Report"
	if os.path.exists(path_well) == False:
		print "Проверьте название скважины"
	return path_well


#Блок поиска пути месторождения + функция пути к DGR
def folder_path(well):
	path_ws="\\\europe.shell.com\europe\E & P\SPD Salym Central Processing Facility\\" + \
		"Dept_07\SPD Drilling & Completion Well File\West Salym"
	path_sva="\\\europe.shell.com\europe\E & P\SPD Salym Central Processing Facility\\" + \
			"Dept_07\SPD Drilling & Completion Well File\Vadelyp"
	path_us="\\\europe.shell.com\europe\E & P\SPD Salym Central Processing Facility\\" + \
			"Dept_07\SPD Drilling & Completion Well File\Upper Salym"
	if well.split("-")[2] == "K49":
		path_xl = path_creation(well,path_sva)
	elif well.startswith("WS"):
		path_xl = path_creation(well,path_ws)
	elif well.startswith("SVA"):
		path_xl = path_creation(well,path_sva)
	elif well.startswith("US"):
		path_xl = path_creation(well,path_us)
	return path_xl


def connect_excel(path_xl):
	files = os.listdir(path_xl)
	list_file = []
	for xls in files:
		list_file.append(xls)
	xls_file = path_xl + "\\" + list_file[0]
	excel = win32.Dispatch("Excel.Application")
	wb = excel.Workbooks.Open(xls_file)
	Sheet = wb.Sheets(1)
	Y = Sheet.Cells(7,4).Value
	X = Sheet.Cells(8,4).Value
	wb.Close(True)
	return Y,X


for well in db.selectedWellList():
	path_xl = folder_path(well)
	coord = connect_excel(path_xl)
	Y = coord[0] 
	X = coord[1]
	db.wellPropertyChange(well,"Y",str(Y),"m","surf coord f/ DGR")
	db.wellPropertyChange(well,"X",str(X),"m","surf coord f/ DGR")
	db.projectBrowserRefresh()

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-10-21"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""