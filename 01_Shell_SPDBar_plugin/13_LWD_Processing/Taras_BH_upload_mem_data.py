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
import TechlogDialogAdvanced as tda
import TechlogPlot as tp

las = "LAS"
def upload_las(well):
	path  = r"C:\Apps\Routine\PP_eval"
	list_folder = []
	tree_folder = os.listdir(path)
	for i in tree_folder:
		if not os.path.isfile(os.path.join(path,i)):
			list_folder.append(i)
	path_dialog = tda.dialogAdvanced("Выбор каталога")
	path_dialog.addButtonsGroup("Path list",None,list_folder,1)
	path_dialog.execDialog()
	select_folder = path_dialog.getButtonsGroup("Path list")
	path = path + "\\" + select_folder[0]
	files = os.listdir(path)
	list_file = []
	for i in files:
		if i.endswith("las"):
			list_file.append(i)
	path_dialog = tda.dialogAdvanced("Выбор файла")
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
	db.currentChange("import")
	for well_import in db.wellList():
		db.wellRename(well_import,well)
		db.projectBrowserImportRefresh()
	for well_import in db.wellList():
		ds_name = db.datasetList(well_import)[0]
		db.datasetRename(well_import,ds_name,"LAS_MEM")
		ds_name = db.datasetList(well_import)[0]
		db.datasetCopy(well_import,ds_name,"import","project")
		db.currentChange("project")	
		db.importBufferClose()
	print "Датасет LAS_MEM загружен"


def rename_property(well):
#Очистка списка имен переменных в свойствах скважины
	equation_var_list = ["GR_Por","gr_a","gr_b","gr_c",
				 "Res_Por","res_a","res_b","res_c",
				 "Equation_status","Elevation"]
	var_las_list = db.variableList(well,"LAS_MEM")
	list_total = db.wellPropertyList(well)
	result = set(list_total) - set(equation_var_list)
	print "Список на удаление сформирован"
	for i in range(len(list(result))):
		db.wellPropertyDelete(well,(list(result))[i])
#Диалог назвачения переменным в датасете LAS правильных названий 
#из списка list_neccessary_var
	list_neccessary_var = ["Zero","GR","RES_AT2","RES_AT400","RES_PH2","RES_PH400"]
	list_num = []
	for i in range(len(var_las_list)):
		list_num.append("num_" + str(i))
	dialog = tda.dialogAdvanced("")
	for i in range(len(var_las_list)):
		dialog.addListInput(list_num[i],var_las_list[i],list_neccessary_var)
	dialog.execDialog()
	final_las_list = []
	for j in range(len(var_las_list)):
		final_las_list.append(dialog.getListInput(list_num[j]))
	for i in range(len(var_las_list)):
		db.wellPropertyChange(well,var_las_list[i],final_las_list[i])
	db.wellPropertyChange(well,"Var_name_status","1")
	print "Переменные перемензваны"


def rename_var(well):
	well_prop_list = db.wellPropertyList(well)
	las_list = db.variableList(well,"LAS_MEM")
	for i in range(len(well_prop_list)):
		for j in range(len(las_list)):
			if well_prop_list[i] == las_list[j]:
				if db.wellPropertyValue(well,well_prop_list[i]) != "Zero":
					db.variableRename(well,"LAS_MEM",las_list[j], db.wellPropertyValue(well,well_prop_list[i]))
					print las_list[j],"--->",db.wellPropertyValue(well,well_prop_list[i])


for well in db.selectedWellList():
	db.wellDuplicate(well,well+"_rt")
	db.projectBrowserRefresh()
	if db.datasetExists(well,las):
		db.datasetDuplicate(well,las,well,"LAS_RT")
		print "Датасет LAS переименован"
	else:
		print "Нет датасета LAS или он уже переименован"
	db.wellPropertyChange(well,"Var_name_status","0")
	upload_las(well)
	rename_property(well)
	rename_var(well)
	tp.logViewApplyTemplate("User\\HRZ_mem_data",well,0)

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2017-01-26"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""