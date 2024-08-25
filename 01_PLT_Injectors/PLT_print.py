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
import time
import os
import TechlogDialogAdvanced as TDA
import TechlogPlot as tp
import shutil
import webbrowser
import win32com.client
import pythoncom
pythoncom.CoInitialize()

#name = "2_Taras"				#здесь можно поменять имя каталога на Taras или Alexander

#Блок получения пути для печати картинок
path  = "C:\\Apps\\Routine\\PLT"
list = []
tree = os.listdir(path)
for i in tree:
	if not os.path.isfile(os.path.join(path,i)):
		list.append(i)
path_dialog = TDA.dialogAdvanced("Выбор каталога")
path_dialog.addButtonsGroup("Path list",None,list,1)
path_dialog.execDialog()
select = path_dialog.getButtonsGroup("Path list")
print_path = path + "\\" + select[0]

##Блок печати картинок в указанную print_path папку
for well in db.selectedWellList():
	id1=tp.logViewGetIdByName("PLT_500")
	id2=tp.logViewGetIdByName("PLT_200")
	tp.printToFile(id1,"Custom",".png",print_path + "\\" + "10k",11,36,0,-1,0,-1,-1,False,600)
	tp.printPlot(id2)
	
#Блок поиска предыдущей версии отчета по ПЛТ на Мск сервере
	dir = "Z:\\SPD Moscow\Dept_05\OFM\Load_files\Plt\\"
	names = os.listdir(dir)
	for name in names:
		if name == well.split("-")[0] + "-" + well.split("-")[1] + ".xls":
			fullname = os.path.join(dir, name)
			if os.path.isfile(fullname):        # проверка если это файл...
				shutil.copy(fullname,print_path)
				
				#Открытие предыдущего отчета ПЛТ в Эксель
				path_xl = print_path + "\\" + well.split("-")[0] + "-" + well.split("-")[1] + ".xls"
				xlApp = win32com.client.Dispatch("Excel.Application")
				xlApp.Visible = True
				xlApp.Workbooks.Open(path_xl)

#Копирование пары рабочих шаблонов в папку текущего ПЛТ
shutil.copy("C:\\Apps\Routine\PLT\\123_PLT.xls",print_path)
shutil.copy("C:\\Apps\Routine\PLT\\LQC_PLT_.xls",print_path)

#Открытие каталог с ПЛТ на сервере и каталога с текущей ПЛТ
webbrowser.open(print_path)
webbrowser.open(dir)

__author__ = """Maria PEREZHOGINA (MPerezhogina)"""
__date__ = """2012-03-22"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""