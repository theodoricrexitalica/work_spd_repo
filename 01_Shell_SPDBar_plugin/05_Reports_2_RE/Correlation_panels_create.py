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
import webbrowser
import TechlogPlot as tp
import TechlogDialogAdvanced as tda
res=300
ds_zone = "ZONATION"
Path="\\\europe.shell.com\\europe\\E & P\\SPD Moscow\\Dept_05\\OFM\\Correlation Panel\\PPevals_for_panel\\"
#Поиск скважин с ПЛТ
for well in db.selectedWellList():
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
#Временный датасет, чтоб сгенерировать дату
		ZONE = Variable(well, ds_zone, "ZONES")
		dept_zone = db.datasetZoneDetail(well, ds_zone, ZONE.value(0))
		plt_sign = "PLT_temp"
		pdata = plt_data[-1]
		date_str = time.strftime("%b%y",pdata)
		ds_name = "PLT_" + date_str
#Добавление к дате коммента про кислотку или ВПП 
		treat_list = ["Acid","VPP","Nothing"]
		producer_box = ["Producer PLT"]
		myDialog = tda.dialogAdvanced(treat_list)
		myDialog.addButtonsGroup("Treatment","Action",treat_list,1)
		myDialog.addButtonsGroup("Producer","Producer",producer_box,0)
		myDialog.addTextInput("Reason", "Provide reason for PLT", "")
		myDialog.addTextInput("Date", "Date  dd.mm.yy ", "")
		if myDialog.execDialog():
			ltreat = (myDialog.getButtonsGroup("Treatment"))
			reason = (myDialog.getTextInput("Reason"))
			prod = (myDialog.getButtonsGroup("Producer"))
			treat = ltreat[0]
			if treat == "Nothing":
				treat = " "
			date_tr = (myDialog.getTextInput("Date"))
			if date_tr == "Pls type date...":
				date_tr = " "
			#db.datasetPropertyChange(well,ds_name,"Treatment",treat)
			#db.datasetPropertyChange(well,ds_name,"Date of treatment",date_tr)
#Считывание объема закачки и запись всех данных в текстовую переменную временного датасета
#На входе проверят продюсер ПЛТ это или нет
		if "Producer PLT" in prod:
			pass
		else:
			q = str(int(float(db.datasetPropertyValue(well,ds_name,"Q"))))
			values = [date_str + " " + q + "m3/d" + " " + treat + reason + " " + date_tr,""]
			db.datasetCreate(well, plt_sign, "DEPT", "Measured Depth", "m", [dept_zone[0], dept_zone[1]])
			db.variableSave(well, plt_sign, "date_str", "Zone Description", "", values)
			db.datasetDuplicate(well,ds_name,well,"PLT_FINAL")
#Применение правильного темплейта для каждого случая
for well in db.selectedWellList():
	wellName=well.split("-")[0]+"-"+well.split("-")[1]
	for var in db.variableList(well,"ZONATION"):
		if db.variableFamily(well,"ZONATION",var)=="Zone Name" and var!="ZONES" and var!="ZONE":
			ok=db.variableDelete(well,"ZONATION",var)
			if ok: print well+ " Delete " + var
	ZONES=db.variableData(well,"ZONATION","ZONES")
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
		#elif "AS11.3.2" in ZONES and "AS9.0" in ZONES:
			#id=tp.logViewApplyTemplate("User\NO_PLT_AS9-AS1132",well,False)

__author__ = """Sergey POLUSHKIN (Sergey.Polushkin)"""
__date__ = """2014-10-16"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""