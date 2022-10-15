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


def upload_gases(well,path):
	excel = win32.Dispatch("Excel.Application")
	wb = excel.Workbooks.Open(path)
	Sheet = wb.Sheets(1)
	write=False
	row = 1
	column = 1
	while Sheet.Cells(row,1).Value!=None:
		row+=1
	print "Exl rows:", row
	while Sheet.Cells(1,column).Value!=None:
		column+=1
	print "Exl columns:", column
	dict = {}
	for j in range(1,column):
		if Sheet.Cells(1,j).Value!=None:
			list=[]
			for i in range(1,row):
				if type(Sheet.Cells(i,j).Value) == float:
					list.append(Sheet.Cells(i,j).Value)
			dict[Sheet.Cells(1,j).Value] = list
	wb.Close(True)
	ds_mdlg = "MUDLOG"
	print "Dict keys:\n",dict.keys()
	MD = 0
	C1 = 0
	C2 = 0
	C3 = 0
	C4 = 0
	C5 = 0
	Tgas = 0
	for i in range(len(dict.keys())):
		if "MD" in dict.keys()[i]:
			MD = i
		elif "C1_C6" in dict.keys()[i]:
			pass
		elif "C1" in dict.keys()[i]:
			C1 = i
		elif "C2" in dict.keys()[i]:
			C2 = i
		elif "C3" in dict.keys()[i]:
			C3 = i
		elif "C4" in dict.keys()[i]:
			C4 = i
		elif "C5" in dict.keys()[i]:
			C5 = i
		elif "Tgas" in dict.keys()[i]:
			Tgas = i
	db.datasetCreate(well,ds_mdlg,"MD","Measured Depth","M",dict[dict.keys()[MD]])
	db.variableSave(well,ds_mdlg,"Tgas","Total Gas","",dict[dict.keys()[Tgas]])
	db.variableSave(well,ds_mdlg,"C1","Mud Gas C1","",dict[dict.keys()[C1]])
	db.variableSave(well,ds_mdlg,"C2","Mud Gas C2","",dict[dict.keys()[C2]])
	db.variableSave(well,ds_mdlg,"C3","Mud Gas C3","",dict[dict.keys()[C3]])
	db.variableSave(well,ds_mdlg,"C4","Mud Gas IC4","",dict[dict.keys()[C4]])
	db.variableSave(well,ds_mdlg,"C5","Mud Gas IC5","",dict[dict.keys()[C5]])
	
	
for well in db.selectedWellList():
	if db.datasetExists(well, "MUDLOG"):
		db.datasetDelete(well, "MUDLOG", 1)
		print "MUDLOG удален"
	else:
		pass
	excel_gas = folder_path()
	upload_gases(well,excel_gas)

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2017-10-14"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""