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
	if i.endswith("las"):
		list_file.append(i)
path_dialog = TDA.dialogAdvanced("Выбор файла")
path_dialog.addButtonsGroup("File list",None,list_file,1)
path_dialog.execDialog()
file = path_dialog.getButtonsGroup("File list")
las = []
for i in file:
	if i.endswith("las"):
		las.append(i)
	else: pass
path_las = path + "\\" + las[0]
db.importFile(path_las,1,"CP-1251","MULTIWELLFILW",0)
for well in db.selectedWellList():
	if db.datasetExists(well,"LAS"):
		db.datasetDelete(well,"LAS")
		print "Предыдущий датасет LAS удален"
	else:
		pass
	db.currentChange("import")
	for well_import in db.wellList():
		db.wellRename(well_import,well)
		db.projectBrowserImportRefresh()
	for well_import in db.wellList():
		ds_name = db.datasetList(well_import)[0]
		db.datasetRename(well_import,ds_name,"LAS")
		ds_name = db.datasetList(well_import)[0]
		db.datasetCopy(well_import,ds_name,"import","project")
		db.currentChange("project")	
		db.importBufferClose()
	print "Датасет LAS загружен"

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-07-10"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""