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
#-*- coding: uts-8 -*-
import TechlogDialogAdvanced as tda
import TechlogDialog as td
import win32com.client
import pythoncom
pythoncom.CoInitialize()
from win32com import client
import webbrowser
import os
import zipfile
path_gec = r"\\europe.shell.com\europe\E & P\SPD Salym Central Processing Facility\Dept_02\TM24-SSFT\SSFT\SSFT GE\GE-C\FinalWells2Petrel"
#---------------------------------LOG DATA BLOCK----------------------------------------
#neutron 
NEU_list=["NEU"] #.............................................................. new name
NEU_list=NEU_list+["Neutron Porosity in Limestone units"]#.....description
NEU_list=NEU_list+["TNPL","TNPH"]#..................................... old names
#density
DEN_list=["DEN"]#.............................................................. new name
DEN_list=DEN_list+["Bulk Density"]#......................................description
DEN_list=DEN_list+["RHOZ","SBD2"]#.................................... old names
#deconvolved density
DEN_ap_list=["DEN_ap"]#.............................................................. new name
DEN_ap_list=DEN_ap_list+["Bulk Density (Alpha-Processed/Deconvolved)"]#description
DEN_ap_list=DEN_ap_list+["RHOZ_apd"]#.................................... old names
#formation resistivity
RT_list=["RT"]#.............................................................. new name
RT_list=RT_list+["True Resistivity"]#..................................description
RT_list=RT_list+["RT"]#...................................................old names
#photo-electric factor
PE_list=["PE"]#.............................................................. new name
PE_list=PE_list+["Litho-Density"]#..................................description
PE_list=PE_list+["PEFZ","SNP2"]#.................................... old names
#caliper
CALI_list=["CALI"]#..........................................................new name
CALI_list=CALI_list+["Caliper"]#.........................................description
CALI_list=CALI_list+["HCAL","SCAL","APPC"]#.................................old names
#gamma ray
GR_list=["GR_list"]#.............................................................new name
GR_list=["Gamma Ray"]#......................................................description
GR_list=["GR", "SGRC","ECGR"]#........................................................old names
#micro resistivity
RES_MIC_list=["RES_MIC"]#..................................................new name
RES_MIC_list=RES_MIC_list+["Resistivity Micro"]#...................description
RES_MIC_list=RES_MIC_list+["RXOI"]#...................................ol names
#extra shallow resistivity
RES_ESLW_list=["RES_ESLW"]#..............................................new name
RES_ESLW_list=RES_ESLW_list+["Resistivity Extra Shallow"]#...description
RES_ESLW_list=RES_ESLW_list+["AE10", "SEXP","RLA1"]#..................old names
#shallow resistivity
RES_SLW_list=["RES_SLW"]#...................................................new name
RES_SLW_list=RES_SLW_list+["Resistivity Shallow"]#.................description
RES_SLW_list=RES_SLW_list+["AE20", "SESP","RLA2"]#........................old name
#medium resistivity
RES_MED_list=["RES_MED"]#..................................................new name
RES_MED_list=RES_MED_list+["Resistivity Medium"]#................description
RES_MED_list=RES_MED_list+["AE30","HLLS","SEMP","RLA3"]#.............old names
#deep resistivity
RES_DEP_list=["RES_DEP"]#....................................................new name
RES_DEP_list=RES_DEP_list+["Resistivity Deep"]#......................description
RES_DEP_list=RES_DEP_list+["AE60","HLLD","SEDP","RLA4"]#...........................old names
#extra deep resistivity
RES_EDEP_list=["RES_EDEP"]#.................................................new name
RES_EDEP_list=RES_EDEP_list+["Resistivity Extra Deep"]#...........description
RES_EDEP_list=RES_EDEP_list+["AE90","RLA5"]#............old names
#spontaneous potential
SP_list=["SP"]#.......................................................................new mane
SP_list=SP_list+["Spontaneous Potential"]#................................description
SP_list=SP_list+["SP"]#............................................................old names
#Sonic (compressional)
DT_list=["DT"]#..................................................................new name
DT_list=DT_list+["Sonic Compressional"]#..................................description
DT_list=DT_list+["DT"]#............................................................old names
#----------------------------------------PP eval curves Block------------------------------------
#Fluid type code
FLD_list=["FLD"]
FLD_list=FLD_list+["Fluid type code"]
FLD_list=FLD_list+["Fluid_Index"]
#cut curve
CUT_list=["cut"]
CUT_list=CUT_list+["Elimination of Preudo Reservoirs"]
CUT_list=CUT_list+["cut"]
#total porosity
POR_list=["POR"]
POR_list=POR_list+["Total Porosity"]
POR_list=POR_list+["Por_uncut"]
#net porosity
PORNET_list=["PORNET"]
PORNET_list=PORNET_list+["Net Porosity"]
PORNET_list=PORNET_list+["Porden"]
#Water Saturation Net (W-Sm)
SW_WS_list=["SWNET_ws"]
SW_WS_list=SW_WS_list+["Water Saturation Net (W-Sm)"]
SW_WS_list=SW_WS_list+["SWWS"]
#Water Saturation Net (SHF)
SW_CAP_list=["SWNET_cap"]
SW_CAP_list=SW_CAP_list+["Water Saturation Net (SHF)"]
SW_CAP_list=SW_CAP_list+["SW_SHF_bf"]
#Permeability (brine - 100% water saturation)
PERM_b_list=["PERM_b"]
PERM_b_list=PERM_b_list+["Permeability (brine - 100% water saturation)"]
PERM_b_list=PERM_b_list+["K_merge"]
#Permeability correction (multiplier)
COR_perm_list=["K_multiplier"]
COR_perm_list=COR_perm_list+["Permeability Correction (multiplier)"]
COR_perm_list=COR_perm_list+["K_multiplier"]
#Phase oil  Permeability 
PERM_o_list=["PERM_o"]
PERM_o_list=PERM_o_list+["Phase Oil Permeability"]
PERM_o_list=PERM_o_list+["Ko"]
#Phase water  Permeability 
PERM_w_list=["PERM_w"]
PERM_w_list=PERM_w_list+["Phase Water Permeability"]
PERM_w_list=PERM_w_list+["Kw"]
#Psedo shale volume (normilized GR)
VSH_GR_list=["VSH_gr"]
VSH_GR_list=VSH_GR_list+["Pseudo Shale Volume (normilized GR)"]
VSH_GR_list=VSH_GR_list+["Vclgr"]
#Psedo shale volume (normilized GR)
VSH_ND_list=["VSH_dn"]
VSH_ND_list=VSH_ND_list+["Pseudo Shale Volume (PHI_neu-PHI_den)"]
VSH_ND_list=VSH_ND_list+["Vsh_nd"]
#Lithology Code
LITH_list=["LITH"]
LITH_list=LITH_list+["Lithology Code"]
LITH_list=LITH_list+["RRT"]
#Irreducible Water
SWIR_list=["SWIRR"]
SWIR_list=SWIR_list+["Irreducible Water Saturation"]
SWIR_list=SWIR_list+["Swi_nd"]
#.........................................................................................list of Log lists
Mnemo_list=[NEU_list, DEN_list, DEN_ap_list, RT_list, PE_list, CALI_list, GR_list, RES_MIC_list, RES_ESLW_list, 
RES_SLW_list, RES_MED_list, RES_DEP_list, RES_EDEP_list, SP_list,DT_list, FLD_list, CUT_list, POR_list, 
PORNET_list ,SW_WS_list, SW_CAP_list, PERM_b_list, COR_perm_list, PERM_o_list, PERM_w_list,
VSH_GR_list, VSH_ND_list, LITH_list, SWIR_list]
#Source dataset
#--------------
DS="COMMON_05" 
#Destination dataset
#-------------------     
NDS="COMMON_05_st"

LIST=db.selectedWellList()
for j in LIST:
	WELL=j

	print ""
	if not db.datasetExists(WELL, NDS):
		#creation of new empty dataset sampled by 0.05m
		#----------------------------------------------
		DEPT=        Variable(WELL, DS, "DEPT")
		DEPT_LIST=DEPT.values()
		db.datasetCreate(WELL, NDS, "DEPTH", "Measured Depth", "m", DEPT_LIST)
		#variable copying from COMMON to NEW dataset
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

	filePath=path_gec												#рабочий путь
	#filePath="C:\Apps\Routine\\Send_xml"							#путь для тестирования скрипта
	#создание папки куста
	if os.path.exists(filePath + "\\" + str((WELL.split("-")[2:3])[0])):
		pass
	else:
		os.mkdir(filePath + "\\" + str((WELL.split("-")[2:3])[0]))
	exportOK =db.exportFile(filePath, [WELL+"."+NDS],"LAS 2.0")
	#Переименование лас-файла с данными для Петрела
	las_file = filePath + "\\" + WELL + "." + NDS + ".las"
	src = las_file
	dst = filePath + "\\" + str((WELL.split("-")[2:3])[0]) + "\\" + "-".join(WELL.split("-")[:5]) + "-Final.las"
	
	#удаление файла,если он уже есть, и копирование заново
	if os.path.isfile(dst):
		os.remove(dst)
		os.rename(src,dst)
	else:
		#exportOK =db.exportFile(filePath, [WELL+"."+NDS],"LAS 2.0")
		os.rename(src,dst)
	if exportOK:
		print ""
		print "Петрел-лас для " + "-".join(WELL.split("-")[:2]) + " успешно выгружен в GE-C\FinalWells2Petrel"
	db.datasetDelete(WELL,NDS)
	zip_path = filePath + "\\" + str((WELL.split("-")[2:3])[0])
	zip_name = "-".join(WELL.split("-")[:5]) 
	zip_las = zipfile.ZipFile(zip_path + "\\" + zip_name + "-Final.zip","w")
	zip_las.write(os.path.join(zip_path,zip_name + "-Final.las"),zip_name + "-Final.las",compress_type=zipfile.ZIP_DEFLATED)
	zip_las.close()
	attachment = zip_path + "\\" + zip_name + "-Final.zip"
#Выгрузка инклинометрии
ds = "ZONATION_PETREL"
dev = "deviation"
wellpath = "wellpath"
for well in db.selectedWellList():
#Блок копирования инфы инклинометрии
	wellname = "-".join(well.split("-")[:2])
	pad = str((well.split("-")[2:3])[0])
	filepath_dev = path_gec
	dev_md = db.variableData(well,dev,"MD")
	dev_inc = db.variableData(well,dev,"INC")
	dev_azi = db.variableData(well,dev,"AZI")
	wellname_txt = wellname + "_dev.txt"
	wh_result=open(filepath_dev + "\\" + pad + "\\" + wellname_txt, 'w+')
	wh_result.writelines("MD" +'\t'+ "INC"+'\t'+"AZI" + "\n")
	wh_result.writelines("m" +'\t'+ "deg"+'\t'+"deg" + "\n")
	for i in range(len(dev_md)):
		wh_result.writelines(str(round(dev_md[i],2)) + '\t' +\
							str(round(dev_inc[i],2)) + '\t' + \
							str(round(dev_azi[i],2)) + "\n")
	wh_result.close()
	attachment_incl = filepath_dev + "\\" + pad + "\\" + wellname_txt
	zip_path =  filepath_dev + "\\" + pad + "\\"
	print "Инклинометрия для ", wellname, " выгружена в GE-C\FinalWells2Petrel"
### Creating emails for distribution list
	email = win32com.client.Dispatch("Outlook.Application")
	Msg = email.CreateItem(0)
	Msg.To = "GPN-NTC_final_las"
	Msg.Cc = "ruf176"
	Msg.Subject = "SPD_" + WELL + "-Final"
	Msg.HTMLBody = "Добрый день, <br>Инклинометрия и лас-файл с финальной интерпретацией по ".decode("utf-8") + "-".join(WELL.split("-")[:3]) + \
	" во вложении.".decode("utf-8") + \
	"<p>Regards," + \
	"<br>Taras Dolgushin" +\
		"<br>Field Petrophysicist" + \
		"<br>Sub Surface Field Team" + \
	"<br>Salym Petroleum Development N.V." + \
	"<br>Phone:  +7 495 411 7074 ext.3486" + \
	"<br>Mobile: +7 932 440 29 29" + \
	"<br>E-mail work: SPD-SALYM-SSFT-GE-C@salympetroleum.ru" + \
	"<br>E-mail personal: Taras.Dolgushin@salympetroleum.ru"
	Msg.Attachments.Add(attachment)
	Msg.Attachments.Add(attachment_incl)
	Msg.Display()
	webbrowser.open(filePath + "\\" + pad)

path_log_send=r"Y:\SSFT GE\GE-C\Журнал отправки данных в ГПН.xlsx".decode("utf-8")
xlApp = win32com.client.Dispatch("Excel.Application")
xlApp.Visible = True
xlApp.Workbooks.Open(path_log_send)

__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""