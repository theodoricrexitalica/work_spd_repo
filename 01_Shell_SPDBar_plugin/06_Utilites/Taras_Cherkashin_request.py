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
import win32com.client
from os import *
import pythoncom
pythoncom.CoInitialize()
import webbrowser
import TechlogDialogAdvanced as tda

#---------------------------------LOG DATA BLOCK----------------------------------------
#neutron 
NEU_list=["NEU"] #.............................................................. new name
NEU_list=NEU_list+["Neutron Porosity in Limestone units"]#.....description
NEU_list=NEU_list+["TNPL","TNPH","TRNP"]#..................................... old names

#density
DEN_list=["DEN"]#.............................................................. new name
DEN_list=DEN_list+["Bulk Density"]#......................................description
DEN_list=DEN_list+["RHOZ","SBD2","RHOB"]#.................................... old names

#formation resistivity
RT_list=["RT"]#.............................................................. new name
RT_list=RT_list+["True Resistivity"]#..................................description
RT_list=RT_list+["RT"]#...................................................old names

#gamma ray
GR_list=["GR_list"]#.............................................................new name
GR_list=["Gamma Ray"]#......................................................description
GR_list=["GR", "SGRC","ECGR"]#........................................................old names

#medium resistivity
RES_MED_list=["RES_MED"]#..................................................new name
RES_MED_list=RES_MED_list+["Resistivity Medium"]#................description
RES_MED_list=RES_MED_list+["AE30","HLLS","SEMP","RLA3","Z35"]#.............old names

#deep resistivity
RES_DEP_list=["RES_DEP"]#....................................................new name
RES_DEP_list=RES_DEP_list+["Resistivity Deep"]#......................description
RES_DEP_list=RES_DEP_list+["AE60","HLLD","SEDP","RLA4","Z60"]#...........................old names

#extra deep resistivity
RES_EDEP_list=["RES_EDEP"]#.................................................new name
RES_EDEP_list=RES_EDEP_list+["Resistivity Extra Deep"]#...........description
RES_EDEP_list=RES_EDEP_list+["AE90","RLA5","Z90"]#............old names

#.........................................................................................list of Log lists
Mnemo_list=[NEU_list, DEN_list, RT_list, GR_list, RES_MED_list, RES_DEP_list, RES_EDEP_list]

#Source dataset
#--------------
DS="MAIN" 
#Destination dataset
#-------------------     
NDS="Cherkashin"

LIST=db.selectedWellList()
for j in LIST:
	WELL=j
	print WELL
	if db.datasetExists(WELL,DS):
		pass
	else:
		print "Нет датасета MAIN"
	if not db.datasetExists(WELL, NDS):
		#creation of new empty dataset sampled by 0.05m
		#----------------------------------------------
		DEPT = db.variableData(WELL, DS, db.referenceName(WELL,DS))
		DEPT_LIST=[]
		for i in DEPT:
			DEPT_LIST.append(round(i,2))
		db.datasetCreate(WELL, NDS, "DEPTH", "Measured Depth", "m", DEPT_LIST)
		
		#variable copying from MAIN to NEW MAIN dataset
		#----------------------------------------------
		VarList=db.variableList(WELL, DS)
		for x in Mnemo_list:
			check="no"
			count=1
			for j in VarList:
				var=j
				if db.variableFamily(WELL, DS, j)<>"Measured Depth":
					if var in x:
						new_name=x[0]
						if count>1:
							new_name=new_name+"_"+str(count)
							print  x[0],  '<font color=blue size=+2>Duplication!</font>'
						print var+" --> "+ new_name+ " O'k"
						db.variableCopy(WELL, DS, var, NDS, new_name)
						V=db.variableData(WELL,NDS, new_name)
						for i in range(len(V)):
							if V[i]==-9999:V[i]=-999.25
						family=db.variableFamily(WELL,NDS,new_name)
						unit=db.variableUnit(WELL,NDS,new_name)	
						db.variableSave(WELL,NDS, new_name,family,unit,V)	
						db.variableDescriptionChange(WELL,NDS,new_name, x[1]+" *** old name "+var+"***")
						check="ok"
						count=count+1
			if check=="no":
				print  '<font color=red size=+2>"Warning! " </font>'+  x[0]+ '<font color=red size=+2>" is not found" </font>' 
	else:
		print '<font color=blue size=+3>specified dataset exists</font>'
		
	
	filePath="\\\europe.shell.com\europe\E & P\SPD Salym Central Processing Facility\Dept_02\TM24-SSFT\DATA Exchange Area\Log data store area"
	exportOK =db.exportFile(filePath, [WELL+"."+NDS],"LAS 2.0")
	#Переименование лас-файла с данными для Петрела
	las_file = filePath + "\\" + WELL + "." + NDS + ".las"
	src = las_file
	dst = filePath + "\\" + "-".join(WELL.split("-")[:2]) + ".las"
	#удаление файла,если он уже есть, и копирование заново
	if os.path.isfile(dst):
		os.remove(dst)
		os.rename(src,dst)
	else:
		exportOK =db.exportFile(filePath, [WELL+"."+NDS],"LAS 2.0")
		os.rename(src,dst)
	if exportOK:
		print WELL + " successfully exported"
	db.datasetDelete(WELL,NDS)
	
dialog = tda.dialogAdvanced("LogsEmail")
dialog_list = ["Send email", "Local Petrel"]
dialog.addButtonsGroup("Emails","Emails", dialog_list, 1)
dialog.execDialog()
response = dialog.getButtonsGroup("Emails")
if response[0] == "Send email":
	well_list = []
	for well in db.selectedWellList():
		well_list.append(well)
	email = win32com.client.Dispatch("Outlook.Application")
	Msg = email.CreateItem(0)
	Msg.To = " "
	Msg.Subject = str(", ".join(well_list))
	Msg.Body = "Dear  All, \nPlease find requested files at link below " + \
	"\n<\\\europe.shell.com\europe\E & P\SPD Salym Central Processing Facility\Dept_02\TM24-SSFT\DATA Exchange Area\Log data store area>" +\
	"\n\rRegards," + \
	"\nTaras Dolgushin" +\
	"\nField Petrophysicist" + \
	"\nSub Surface Field Team" + \
	"\nSalym Petroleum Development N.V." + \
	"\nPhone:  +7 495 411 7074 ext.3486" + \
	"\nMobile: +7 932 440 29 29" + \
	"\nE-mail work: SPD-SALYM-SSFT-GE-C@salympetroleum.ru" + \
	"\nE-mail personal: Taras.Dolgushin@salympetroleum.ru"
	Msg.Display()
else:
	pass
webbrowser.open(filePath)

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2015-12-31"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""