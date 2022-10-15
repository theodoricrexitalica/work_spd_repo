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
for well in db.selectedWellList():
#Проверка наличия уже названных переменных
	if db.wellPropertyValue(well,"Var_name_status") == "1":
		print "Названия переменных объявлены"
		print "Если необходимо обновить данные, назначьте Var_name_status=0"
		pass
	else:
#Очистка списка имен переменных в свойствах скважины
		equation_var_list = ["GR_Por","gr_a","gr_b","gr_c",
					 "Res_Por","res_a","res_b","res_c",
					 "Equation_status","Elevation"]
		var_las_list = db.variableList(well,"LAS")
		list_total = db.wellPropertyList(well)
		result = set(list_total) - set(equation_var_list)
		print "Список на удаление сформирован"
		for i in range(len(list(result))):
			db.wellPropertyDelete(well,(list(result))[i])
#Диалог назвачения переменным в датасете LAS правильных названий 
#из списка list_neccessary_var
		list_neccessary_var = ["Zero","GR","RES_AT2","RES_AT400","RES_PH2","RES_PH400","ROP"]
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

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-08-25"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""