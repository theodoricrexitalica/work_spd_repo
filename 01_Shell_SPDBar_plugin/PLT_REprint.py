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
import TechlogDialogAdvanced as TDA
import TechlogPlot as tp

#Блок получения пути для печати картинок
path  = "C:\\Apps\\Routine\\PLT"
list = []
tree = os.listdir(path)
for i in tree:
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

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-03-11"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""