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
#Скрипт для поиска ближайших инжекторов.Инжектора определяются по Well Type в Properties скважины
import time
import TechlogDialogAdvanced as tda
import TechlogPlot as tp
report_list = []
for well in db.selectedWellList():
#Список радиусов для поиска инжекторов
	R_list = ["1000","1500","3000","5000"]
	myDialog = tda.dialogAdvanced(R_list)
	myDialog.addListInput("Radius of seeking","Радиус поиска инжекторов,м",R_list)
	if myDialog.execDialog():
		R_str = (myDialog.getListInput("Radius of seeking"))
		R = int(R_str)
	report_list.append("Радиус поиска " + str(R) + "м")
#Блок расчета радиусов, если ЕСТЬ ZONATION_PETREL
	if "ZONATION_PETREL" in db.datasetList(well):
		print "Идет поиск инжекторов.Ждите"
		ZONES0=db.variableData(well,"ZONATION_PETREL","ZONES")
		i=ZONES0.index("AS10.0")
		X0=db.variableData(well,"ZONATION_PETREL","X")[i]
		Y0=db.variableData(well,"ZONATION_PETREL","Y")[i]
		wellList = []
		radius = []
		for wellName in db.wellList():
			if "ZONATION_PETREL" in db.datasetList(wellName)and wellName!=well:
				ZONES=db.variableData(wellName,"ZONATION_PETREL","ZONES")
				if "AS10.0" in ZONES:
					j=ZONES.index("AS10.0")
					if "X" in db.variableList(well,"ZONATION_PETREL"):
						X=db.variableData(wellName,"ZONATION_PETREL","X")[j]
						Y=db.variableData(wellName,"ZONATION_PETREL","Y")[j]
						R_act = round(sqrt((X-X0)**2+(Y-Y0)**2),0)
						if R_act < R and db.wellPropertyValue(wellName,"Well Type")=="I":
							wellList.append(wellName)
							radius.append(R_act)
#Блок расчета радиусов, если НЕТ ZONATION_PETREL
	else:
		print "ZONATION_PETREL отсутствуют"
#Первый раз,если нет координат, появляется окно для внесения координат цели
		if db.wellPropertyValue(well,"Y") == "" or db.wellPropertyValue(well,"X") == "":
			myDialog = tda.dialogAdvanced("Target")
			myDialog.addLabel("Target","\tCoordinates\n"+well)
			myDialog.addTextInput("Y_Input","Y Target","Type Northing...")
			myDialog.addTextInput("X_Input","X Target","Type Easting...")
			if myDialog.execDialog():
				Y0 = float(myDialog.getTextInput("Y_Input"))
				db.wellPropertyChange(well,"Y",str(Y0),"m","")
				X0 = float(myDialog.getTextInput("X_Input"))
				db.wellPropertyChange(well,"X",str(X0),"m","")
		else: 
			Y0 = float(db.wellPropertyValue(well,"Y"))
			X0 = float(db.wellPropertyValue(well,"X"))
		wellList = []
		radius = []
		print "Идет поиск инжекторов.Ждите"
		for wellName in db.wellList():
			if "ZONATION_PETREL" in db.datasetList(wellName):
				ZONES=db.variableData(wellName,"ZONATION_PETREL","ZONES")
				if "AS10.0" in ZONES:
					j=ZONES.index("AS10.0")
					if "X" in db.variableList(wellName,"ZONATION_PETREL"):
						X=db.variableData(wellName,"ZONATION_PETREL","X")[j]
						Y=db.variableData(wellName,"ZONATION_PETREL","Y")[j]
						R_act = round(sqrt((X-X0)**2+(Y-Y0)**2),0)
						if R_act < R and db.wellPropertyValue(wellName,"Well Type")=="I":
							wellList.append(wellName)
							radius.append(R_act)
#Формирование списка скважин
list = []
report_list.append("Найдены скважины:")
for i in range(0,len(wellList)):
	#text = (str(wellList[i]) + "   " + "Distance" + "  " + str(radius[i]) + "m" )
	text = (str(wellList[i].split("-")[0]+"-"+wellList[i].split("-")[1]+ \
	"-"+wellList[i].split("-")[2]) + "   " + "Distance" + "  " + str(radius[i]) + "m" )
	list.append(text)
	report_list.append(text)
#Вывод на экран списка скважин, нужно выбрать те, для которых будут созданы диаграммы
well_list = []
myDialog = tda.dialogAdvanced(well)
myDialog.addButtonsGroup("Injectors","Injectors",list,0)
if myDialog.execDialog():
	report_list.append("Выбраны скважины:")
	wells_print = myDialog.getButtonsGroup("Injectors")
	for j in wells_print:
		well_j = j.split("  ")[0]
		well_list.append(well_j)
		report_list.append(well_j)
#Блок печати выбранных инжекторов
	for k in well_list:
		for well in wellList:
			if k.split("-")[0]+"-"+k.split("-")[1] == well.split("-")[0]+"-"+well.split("-")[1]:
				plt_data = []
				for ds in db.datasetList(well):
					if ds.startswith("PLT_"):
						try:
							date = time.strptime(ds.split("_")[-1], "%b%y")
							plt_data.append(date)
						except:
							continue
					if plt_data!=[]:
						plt_data.sort()
						n = 0
#Временный датасет для даты и объема закачки
				ds_zone = "ZONATION"
				ZONE = Variable(well, ds_zone, "ZONES")
				dept_zone = db.datasetZoneDetail(well, ds_zone, ZONE.value(0))
				plt_sign = "PLT_temp"
				if len(plt_data) != 0:
					pdata = plt_data[-1]
					date_str = time.strftime("%b%y",pdata)
					ds_name = "PLT_" + date_str
					q = str(int(float(db.datasetPropertyValue(well,ds_name,"Q"))))
					values = [date_str + " " + q + "m3/d",""]
					db.datasetCreate(well, plt_sign, "DEPT", "Measured Depth", "m", [dept_zone[0], dept_zone[1]])
					db.variableSave(well, plt_sign, "date_str", "Zone Description", "", values)
					db.datasetDuplicate(well,ds_name,well,"PLT_FINAL")
				else:
					pass
#Проверка наличия переменной с зонейшенами
				wellName=well.split("-")[0]+"-"+well.split("-")[1]
				for var in db.variableList(well,"ZONATION"):
					if db.variableFamily(well,"ZONATION",var)=="Zone Name" and var!="ZONES" and var!="ZONE":
						ok=db.variableDelete(well,"ZONATION",var)
						if ok: print well+ " Delete " + var
				ZONES=db.variableData(well,"ZONATION","ZONES")
#Блок поиска и печати нужного темплейта
				if "PLT_FINAL" in db.datasetList(well):
					if "AS11.3.2" in ZONES and "AS9.0" not in ZONES:
						id=tp.logViewApplyTemplate("User\WITH_PLT_AS10-AS1132",well,False)
					elif "AS11.3.2" not in ZONES and "AS9.0" not in ZONES:
						id=tp.logViewApplyTemplate("User\WITH_PLT_AS10-AS1131",well,False)
					elif "AS11.3.2" not in ZONES and "AS9.0" in ZONES:
						id=tp.logViewApplyTemplate("User\WITH_PLT_AS9-AS1131",well,False)
					elif "AS11.3.2" in ZONES and "AS9.0" in ZONES:
						id=tp.logViewApplyTemplate("User\WITH_PLT_AS9-AS1132",well,False)
				else:
					if "AS11.3.2" in ZONES and "AS9.0" not in ZONES:
						id=tp.logViewApplyTemplate("User\NO_PLT_AS10-AS1132",well,False)
					elif "AS11.3.2" not in ZONES and "AS9.0" not in ZONES:
						id=tp.logViewApplyTemplate("User\NO_PLT_AS10-AS1131",well,False)
					elif "AS11.3.2" not in ZONES and "AS9.0" in ZONES:
						id=tp.logViewApplyTemplate("User\NO_PLT_AS9-AS1131",well,False)
print "Результаты:"
for i in range(len(report_list)):
	print report_list[i]

__author__ = """Sergey POLUSHKIN (Sergey.Polushkin)"""
__date__ = """2013-03-13"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""