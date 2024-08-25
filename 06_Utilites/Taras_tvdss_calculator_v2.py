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
#Функция Калькулятор
def Calculator (well,md,tvd,tvdss):
	
	MD = db.variableData(well,ods,"MD",0)
	TVD = db.variableData(well,ods,"TVD")
	TVDSS = db.variableData(well,ods,"TVDSS")
	
	if md >= 0.0:
		for i in MD:
			if md == round(i,2):
				ind = MD.index(i)
				md_res = round(MD[ind],2)
				
				tvd_res = round(TVD[ind],2)
				tvdss_res = round(TVDSS[ind],2)
	
	if tvd > 0:
		for i in TVD:
			if tvd == round(i,2):
				ind = TVD.index(i)
				
				md_res = round(MD[ind],2)
				tvd_res = round(TVD[ind],2)
				
				tvdss_res = round(TVDSS[ind],2)
	
	if tvdss > 0:
		for i in TVDSS:
			if tvdss == round(i,2):
				ind = TVDSS.index(i)
				md_res = round(MD[ind],2)
				tvd_res = round(TVD[ind],2)
				tvdss_res = round(TVDSS[ind],2)

	return (md_res, tvd_res, tvdss_res)

#Импорт библиотек и объявление переменных
import TechlogDialogAdvanced as tda
import TechlogDialog as td

ds = "deviation"
ods = "Calc_temp"

for well in db.selectedWellList():

#Блок проверки наличия DFE.Если нет DFE, необходимо ввести значение,которое сохранится в wellProperty
	elev = db.wellPropertyValue(well,"Elevation")
	if not elev:
		print "Type it"
		dialog = tda.dialogAdvanced("Высота стола ротора")
		dialog.addDoubleInput("1D","Высота стола ротора",0,-214748.123,214748.123,2,0.01)
		dialog.execDialog()
		elev = round(dialog.getDoubleInput("1D"),2)
		print elev
		elev_str = str(elev)
		db.wellPropertyChange(well,"Elevation",elev_str,"m","Drill floor elevation")

#Блок расчета временного датасета Calc_temp на базе датасета deviation с шагом 0.01м для работы калькулятора
	if not db.datasetExists(well,ds):
		td.information("Внимание","Нет датасета deviation")
		break
	
	db.computeTVD(well,ds,ods,"minimum curvature",float(elev),"m",0,"m",0, \
				  "m","survey",0,0,"m",0,0,"m",0,0,"dega","first dip", \
				  0,"m","extrapolate","m",0.01,"m",[1],1,1,"grid North")

#Запуск цикла для калькулятора
	for i in range(1,100):
		dialog = tda.dialogAdvanced("Калькулятор глубин")
		dialog.addDoubleInput("2D","MD",0,-214748.123,214748.123,2,0.01)
		dialog.addDoubleInput("3D","TVD",0,-214748.123,214748.123,2,0.01)
		dialog.addDoubleInput("4D","TVDSS",0,-214748.123,214748.123,2,0.01)
		toggle = dialog.execDialog()
		md = round(dialog.getDoubleInput("2D"),2)
		tvd = round(dialog.getDoubleInput("3D"),2)
		tvdss = round(dialog.getDoubleInput("4D"),2)
		
		result = Calculator(well,md,tvd,tvdss)
		
		dialog = tda.dialogAdvanced("Калькулятор глубин")
		dialog.addDoubleInput("2D","MD",result[0],-214748.123,214748.123,2,0.01)
		dialog.addDoubleInput("3D","TVD",result[1],-214748.123,214748.123,2,0.01)
		dialog.addDoubleInput("4D","TVDSS",result[2],-214748.123,214748.123,2,0.01)
		toggle = dialog.execDialog()

#Блок остановки калькулятора
		if toggle == 0:
			break
		else:
			continue
	db.datasetDelete(well,ods,1)

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2015-12-24"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""