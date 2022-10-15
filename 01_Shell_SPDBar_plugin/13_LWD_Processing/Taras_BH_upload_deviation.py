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
import TechlogDialogAdvanced as TDA


#Блок поиска пути для загрузки инклинометрии чз эксель-таблицу
def folder_path():
	#path  = r"C:\Apps\Routine\PP_eval"
	setting = "\\".join([db.dirUser(),"setting.txt"])
	with open(setting) as f:
		path = (f.readlines()[1]).split("\n")[0]
	list_folder = []
	tree_folder = os.listdir(path)
	for i in tree_folder:
		if not os.path.isfile(os.path.join(path,i)):
			list_folder.append(i)
	path_dialog = TDA.dialogAdvanced("Выбор каталога")
	path_dialog.addButtonsGroup("Path list",None,list_folder,1)
	path_dialog.execDialog()
	select_folder = path_dialog.getButtonsGroup("Path list")
	path = path + "\\" + select_folder[0]
	
	files = os.listdir(path)
	list_file = []
	for i in files:
		if i.endswith("xlsx") or i.endswith("xls"):
			list_file.append(i)
	path_dialog = TDA.dialogAdvanced("Выбор файла")
	path_dialog.addButtonsGroup("File list",None,list_file,1)
	path_dialog.execDialog()
	file = path_dialog.getButtonsGroup("File list")
	xls = []
	for i in file:
		if i.endswith("xlsx") or i.endswith("xls"):
			xls.append(i)
		else: pass
	path_xls = path + "\\" + xls[0]
	return(path_xls)


def upload_deviation(well,path):
	excel = win32.Dispatch("Excel.Application")
	wb = excel.Workbooks.Open(path)
	Sheet = wb.Sheets(1)
	write=False
	row = 1
	
	for i in range(1,100):
		if Sheet.Cells(i,1).Value =="MD\n(m)" \
		or Sheet.Cells(i,1).Value =="MD"  \
		or Sheet.Cells(i,1).Value =="Гл".decode("utf-8"):
			row = i
	row = row + 2
	MD=[]
	INC=[]
	AZI=[]
	while Sheet.Cells(row,1).Value!=None:
		if type(Sheet.Cells(row,1).Value) == float:
			MD.append(Sheet.Cells(row,1).Value)
			AZI.append(Sheet.Cells(row,3).Value)
			INC.append(Sheet.Cells(row,2).Value)
		row+=1
	wb.Close(True)
	ds = "deviation"
	ds_temp="deviation_temp"
	db.datasetCreate(well,ds_temp,"MD","Measured Depth","M",MD)
	db.datasetTypeChange(well,ds_temp,"trajectory")
	db.variableSave(well,ds_temp,"AZI","Hole Azimuth","DEG",AZI)
	db.variableSave(well,ds_temp,"INC","Hole Deviation","DEG",INC)
	db.datasetDelete(well,ds,1)
	db.datasetRename(well,ds_temp,ds)
	db.datasetDelete(well,ds_temp,1)


def elevation(well):
	elev = db.wellPropertyValue(well,"Elevation")
	if not elev:
		dialog = TDA.dialogAdvanced("Высота стола ротора")
		dialog.addDoubleInput("1D","Высота стола ротора",0,-214748.123,214748.123,2,0.01)
		dialog.execDialog()
		elev = round(dialog.getDoubleInput("1D"),2)
		elev_str = str(elev)
		db.wellPropertyChange(well,"Elevation",elev_str,"m","Drill floor elevation")	
	return elev


def index(well,elev):
	dev = "deviation"
	index = "Index"
	db.computeTVD(well,dev,index,"minimum curvature",float(elev),"m",0,"m",0,
				  "m","survey",0,0,"m",0,0,"m",0,0,"dega","first dip",
				  0,"m","extrapolate","m",0.01,"m",[1],1,1,"grid North")


for well in db.selectedWellList():
	file_dev = folder_path()
	upload_deviation(well,file_dev)
	elev = elevation(well)
	index(well,elev)
	print "Инклинометрия загружена"

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-03-15"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""