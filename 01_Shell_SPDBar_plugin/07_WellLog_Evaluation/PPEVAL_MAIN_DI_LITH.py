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
from Techlog import *
from TechlogMath import *
from FUNLIB import *
#Управляющая функция__________________________________________________________________________________
for well in db.selectedWellList():
	if well.find("WS")>=0:
		from   WS_CONFIG  import *
	elif well.find("SVA")>=0:
			from  SVA_CONFIG  import *
	elif well.find("US")>=0: 
			from  US_CONFIG  import *
	else: 
		print  "Please select any well" 
		break
#Инизиализирую основную матрицу с входными параметрами
	mPoro=PoroInput()[0]
#Задаю сокращения для основных рабочих датасетов
	ds = "COMMON_05"
	dsz = "ZONATION"
	dsc="CONTACTS"
	dsi="Index"
	dsm='MAIN'
#Задаю минимальный набор датасетов  при, котором может сработать скрипт
	if db.datasetExists(well,ds)==False:  logds=dsm
	else: logds=ds
	MinDatasetList=[logds,dsi,dsz]
#Проверяю на наличие минимального набора датасетов
	# Сперва индексдатасет
	if db.datasetExists(well,dsi)==False: 
		if  db.datasetExists(well,'deviation'): 
			bb=IndexDataSetCreator(well,'deviation',dsi)
			if bb>0: 
				print 'Index dataset was created. Drill floor elevation was used', round(bb,2) , "m"
			else:
				print  '<font color=red size=+1> Please create dataset deviation</font>' 
		else:
			print  '<font color=red size=+1> Please create dataset deviation</font>' 
			break
	#Затем весь минимальный набор
	BreakFlag=MissingValue
	for i in range(0,len(MinDatasetList)):
		if db.datasetExists(well,MinDatasetList[i])==False: 
			BreakFlag=MinDatasetList[i]
			print '<font color=red size=+1> Please create dataset</font>' ,' <', MinDatasetList[i], ">"
	if BreakFlag!=MissingValue: break	
#Генерирую таблицу соответствий кривых
	mCurve=CurveList()
#В случае если нет датасета ds его создаю и проверяю, чтобы все кривые были названы правильно
	if db.datasetExists(well,ds)==False:
		if db.datasetExists(well,dsm)!=False:
			if db.datasetExists(well,"DLIS_08ft")!=False:
				if db.variableExists(well,"DLIS_08ft","SSW_column4")!=False: db.variableCopy(well,"DLIS_08ft","SSW_column4",dsm,"SSW_column4")
				if db.variableExists(well,"DLIS_08ft","RXOI")!=False: db.variableCopy(well,"DLIS_08ft","RXOI",dsm,"RXOI")		
			cc=dataset_curve_cheker(well, mCurve, dsm,ds)
			if cc!=0: print cc, "curves were renaned."
		else:
			if db.variableExists(well,dsm,"SSW_column4")==False:
				print "Please create dataset <MAIN>"
				break
#В случае КНГ и LWD подготовливая плотностной и нейтронника для обработки
		if well.find("KNG")>=0 or well.find("LWD")>=0 or len(well)==6:  
			GaussianSmoothing(well,ds, "RHOZ", "RHOZ_apd", 0.3)
			GaussianSmoothing(well,ds, "RHOZ_apd", "RHOZ", 0.3)
			GaussianSmoothing(well,ds, "TNPH", "TNPH", 0.3)
			GaussianSmoothing(well,ds, "GR", "GR", 0.3)
			if well.find("KNG")>=0: ConstantGenerator(well, ds, "DEPT", 220.7,"BS","Bit Size","MM") 
#Проверяю наличие кривой RT
	RTChecker(well, ds, "AE60", "AE90")
#Проверяю правильность единиц измерения
	cc=UnitChecker(well, ds)
	if cc<0: 
		print '<font color=red size=+1> Please check the variable unit </font>' 
		db.datasetDelete(well,ds)	
		break
#Копирую абсолютные отметки и зоны
	if db.datasetExists(well,'Index'): db.variableCopy(well,'Index',"TVDSS",dsz,"TVDSS")
	db.variableCopy(well,dsz,"ZONES",ds,"ZONES")
#Копирую абсолютные отметки
	db.variableCopy(well,"Index","TVDSS",ds,"TVDSS")
#Загружаю кривые
	vMD = db.variableData(well, ds, "DEPT")
	vZONES = db.variableData(well, ds, "ZONES")
	vZON = db.variableData(well, dsz, "ZONES")
	vZONDEPT = db.variableData(well, dsz, "DEPTH")
	vRHOZ_old= db.variableData(well, ds, "RHOZ")
	vRT= db.variableData(well, ds, "RT")
	vTNPH= db.variableData(well, ds, "TNPH")
	vGR= db.variableData(well, ds, "GR")
	vTVDSS=db.variableData(well, ds, "TVDSS")
	vCut= db.variableData(well, ds, "cut")
#Определяю не выходят ли топы за границы каротажа
	for i in range(0, len(vZONDEPT)):
		if vZONDEPT[i]>vMD[len(vMD)-1] or vZONDEPT[i]<vMD[0]:
			BreakFlag=1
			print '<font color=red size=+1> Please check MD of your tops in dataset </font>', dsz
	if BreakFlag!=MissingValue: break	
#Определяю шаг дискретизации данных
	step=vMD[10]-vMD[9]
#Деконволюция данных плотностного каротажа 
	if db.variableExists(well,ds,"RHOZ_apd")==False: 
		if well.find("PEX")>=0:
			if db.datasetExists(well,"DLIS_08ft")==False:
				print '<font color=red size=+1> Please create dataset DLIS_08ft or variable RHOZ_apd </font>' 
				break
			else:
				if db.variableExists(well,ds,"SSW_column4")==False:
					print '<font color=red size=+1> Please extract SSW_column4 from DLIS_08ft  </font>' 
					db.datasetDelete(well,ds)
					break
				else:
					vSSW_column4= db.variableData(well, ds, "SSW_column4")
					vRHOZ=deconvolution_Gaus_AP(vMD, vRHOZ_old, vSSW_column4, step)
		else:
			print   '<font color=red size=+1> Please create RHOZ_apd </font>' 
			break
	else:
			vRHOZ= db.variableData(well, ds, "RHOZ_apd")
#Здесь определяется максимальный индекс всех циклов, он определит длину массива пористости, а пористость длину остальных массивов 
	cNumberData=len(vRHOZ_old)
#Определяю список названий пластов, с которыми работаем 
	vZone_need=[]
	for i in range(0,len(mPoro)): vZone_need.append(mPoro[i][0])
#Выявляю возможные ошибки связанные с использованием одних и тех же названий для пластов и проверяю на наличие лишних зон
	pp= TheZoneChecker(vZON,vZone_need)
	if pp[0]==-1:
			print "There are two zones<", pp[1], "> in the dataset<", dsz, ">",'<font color=red size=+1> .Please chek.</font>'
			break
	if pp[0]==-2:
		print   '<font color=red size=+1> Please delit  the zone name</font>',  pp[1],  '<font color=red size=+1> in dataset  </font>' , dsz,  '<font color=red size=+1>or add into the config file.  </font>'
		break
#Определяю есть ли пласты БС и Ач в скважине
	FlagBS=zone_finder(vZON, "BS")
	FlagACH=zone_finder(vZON, "ACH")
	FlagPIM=zone_finder(vZON, "PIM")
#Проверяю соответствие названий зон в конфигфайле и датасете  zonation
	for i in range(0,len(vZone_need)): 
		FlagPrint=zone_checker(vZON, vZone_need[i],FlagBS,FlagACH,FlagPIM)
		if  FlagPrint==1: 
			print "The zone name <" , vZone_need[i], "> not existing in your dataset",  dsz,'.Please chek.'
#Формирую актуальную матрицу по датасету с названиями зон
	vActIndx=[]
	for i in range(0,len(vZone_need)): 
		if zone_finder(vZON,vZone_need[i])>0: vActIndx.append(i)
	mPoro_act=Actual_data(mPoro,vActIndx)
#Проверяю есть ли информация по контактам, если нет то формирую
	if db.datasetExists(well,dsc)==False: 
		dataset_contacts_cheker(well, dsc, vZON, mPoro_act)
		print  '<font color=red size=+1>Dataset</font>', dsc, '<font color=red size=+1> was created </font>'
#Проверяю соответствие названий зон в конфигфайле и датасете  contacts
	vFWL=db.variableData(well, dsc, "FWL_bf")
	vCONT_zones=db.variableData(well, dsc, "ZONES")
	for i in range(0,len(vZone_need)): 
		FlagPrint=zone_checker(vCONT_zones, vZone_need[i],FlagBS,FlagACH,FlagPIM)
		if  FlagPrint==1: print "The zone name <" , vZone_need[i], "> not existing in your dataset  <CONTACTS>. Please chek."
#Проверяю соответствие названий зон в  датасете zonation и contacts
	for i in range(0,len(vCONT_zones)): 
		FlagPrint=0
		FlagPrint=zone_checker(vZON,vCONT_zones[i],FlagBS,FlagACH,FlagPIM)
		if  FlagPrint==1: 
			print "The zone name <" , vCONT_zones[i], "> not existing in your dataset  <Zonation>, but it exists in your dataset <CONTACTS>. Please chek."
			break
	if  FlagPrint==1: break
#определяю индексы соответствующих пластов, если дельта выход за пределы данных, то её ограничиваю
	vDelta=Delta_definition()
	vIND=start_stop_ind_culc(vDelta, step,vZONES, vZone_need)
	if vIND[len(vIND)-1]>cNumberData: 
		vIND[len(vIND)-1]=cNumberData-5
#Инициализирую водонасыщенность и присваиваю ей 1 в интервале интерпретации
	vSWWS=[]
	for i in range(0, cNumberData): vSWWS.append(MissingValue)
	for i in range(vIND[0], vIND[len(vIND)-1]): vSWWS[i]=1
#Расчитываю пористость при водонасыщенности =1, следом считаю саму водонасыщнность		
	fGd =PoroInput()[1]
	vFluden=mPoro_act[1][1]
	vPoro=poro_culc(mPoro_act, fGd, vFluden, vRHOZ,vSWWS,cNumberData,vIND)
	mSat=Actual_data(SatInput(),vActIndx)
	vSWWS=saturation_culc(mSat, vPoro,vRT,vSWWS, vIND)
#Пересчитываю пористость уже с учетом фактической водонасыщенности
	vPoro=poro_culc(mPoro_act, fGd, vFluden, vRHOZ,vSWWS,cNumberData,vIND)
#Обрезаю пористость по отсечкам
	mCutoff=Actual_data(CutoffInput(),vActIndx)
	vPorden=porosity_cut(mCutoff, vPoro, vTNPH, vCut,vIND)
#Считаю  водонасыщенность по обрезанной пористости, в результате заведомо получаю водонасыщенность в неколлекторе =1
	vSWWS=saturation_culc(mSat, vPorden,vRT,vSWWS, vIND)
#Расчет проницаемости как функции от пористости
	mPerm=Actual_data(PermAsFuncPoroInput(),vActIndx)
	vPerm=perm_culc(mPerm,vPorden,vIND)
#Расчет водородосодержания твердой фазы	
	mKTim=Actual_data(KTimurInput(),vActIndx)
	vVsh_nd=Vsh_nd_culc(mKTim, vFluden, vRHOZ_old, vTNPH, vPorden, vIND)
#Расчет проницаемости по Тимуру
	vTemp=perm_Tim_culc(mKTim, vPorden, vVsh_nd, vIND)
	vK_tim=vTemp[0]
	vSwi_nd=vTemp[1]
#Определяю индивидуальные ограничения 
#RMP - это ограничение при объединении проницаемости по Тимуру и Кпр=F(Кп)
#ROP - это ограничение для обнуления проницаемости по нефти в модели Кори
	RMP=PermRestrictions(well)[0]
	ROP=PermRestrictions(well)[1]
#Объединяю проницаемости
	vK_merge=K_merge_culc(vPerm, vK_tim, vPorden,step,RMP,vIND)
#Учитываю мультипликативный коэффициент в проницаемости
	if db.variableExists(well,ds,"K_multiplier")==False: 
		vK_multiplier=[]
		for i in range(0, cNumberData): vK_multiplier.append(MissingValue)
		for i in range(vIND[0], vIND[len(vIND)-1]): vK_multiplier[i]=1
		db.variableSave(well, ds, "K_multiplier", "", "",vK_multiplier, 0)
	else:
		vK_multiplier= db.variableData(well, ds, "K_multiplier")
		vK_merge=K_multiplier_culc(vK_merge,vK_multiplier,vIND)
#Считаю насыщенность по модели переходной зоны
	mSHF=Actual_data(SHFInput(),vActIndx)
	vSHF=SHF_culc(mSHF, mPoro_act, vCONT_zones, vFWL, vPorden, vK_merge, vTVDSS, vIND)
#Реализую модель Кори расчета фазовых (1-впитывание, 0 - дренирование)
	mCorey=Actual_data(CoreyInput(),vActIndx)
	vCorey=Corey_culc(well, mCorey,vPorden,vK_merge, vSHF,ROP, 0, vIND)
	vKo=vCorey[0]
	vKw=vCorey[1]
	vWC_Corey=vCorey[2]
#Нормирую ГК
	vVclgr=normalization01(vGR, vIND)
#Угрубляю RT в окне window (в метрах) для расчета индекса насыщения, заодно выкидываю тонкие пропластки 
	window=3
	vAverParam=average_culc(vPorden,vRT, window, step)
	vRTaver=vAverParam[0]
	if db.variableExists(well,ds,"cut")==False: 
		vCut=vAverParam[1]
		db.variableSave(well, ds, "cut", "General Flag", "UNITLESS",vCut, 0)
#Считаю флюид индекс
	if db.variableExists(well,ds,"Fluid_Index")==False: 
		vFluid=fluid_index_culc(vPorden,vRTaver,mSat, step,vIND)
	else:
		vFluid=db.variableData(well, ds, "Fluid_Index")
#Проверяю чтобы везде где определена пористость была насыщенность
	for i in range(vIND[0], vIND[len(vIND)-1]):
		if vFluid[i]==MissingValue and vPorden[i]>0: 
			vFluid[i]=4
		else:
			if vPorden[i]==0:  vFluid[i]=MissingValue 
#Прогоняю модель Кори с насыщенностью по электрич. сопротивлениям (пригодится для интерпретации промытых зон)(0-впитывание, 1 - дренирование)
	vCorey=Corey_culc(well, mCorey,vPorden,vK_merge, vSWWS,ROP,1, vIND)
	vKo_fl=vCorey[0]
	vKw_fl=vCorey[1]
	vWC_Corey_fl=vCorey[2]
#Узнаю есть ли промытые зоны
	Flashed=FlashedFinder(vFluid)
#Если есть промытые зоны, то ставлю в фазоные проницаемости и WC модифицированные данные 
	if Flashed==1:
		for i in range(0,len(vFluid)):
			if vFluid[i]==5:
				vKo[i]=vKo_fl[i]
				vKw[i]=vKw_fl[i]
				vWC_Corey[i]=vWC_Corey_fl[i]
#Считаю накопленную проницаемость
	#ZoneIndex=db.datasetZoneIndice(well,ds, dsz,"BS8")
	#print ZoneIndex
	vBorders=[]
	for i in range(0,len(mPoro_act)):  
		vBorders.append(mPoro_act[i][4])
	vKH=kh_culc(vBorders, vK_merge,vKo,vKw, vTVDSS,vIND)
	vKH_tvd_oil=vKH[0]
	vKH_tvd_water=vKH[1]
	vK_tim_nd_int=vKH[2]
#Выполняю RGTI reporting в нём будут абсолютно все (даже очень мелкие) пропластки
	#rgti_reporting(well, ds, vMD, vTVDSS, vZONES,vPoro,vKo,vKw,vSWWS,vRT,vFluid)
	dsrgti="Rock_Properties_Table"
	mC=RGTIReporting(well, ds, vMD, vTVDSS, vZONES,vPoro,vKo,vKw,vSWWS,vRT,vFluid)
#Отфильтровываю тонкие пропластки в РГТИ таблице
	#Нужно создать временный массив для использовании функции фильтрации
	vTMC=[]
	for i in range(len(mC)): vTMC.append(mC[i][3])
	vRGTIFiltr=ThiknessFilter(mC[9][3], vTMC, len(mC), 0.35)
	if vRGTIFiltr[0]<0: print "Error during filtrarion of the RTGI table"
	#Чтобы использовать функциию сохранения приходится переформачивать
	vRGTI=[]
	for i in range(len(mC)): 
		vRGTI.append([])
		for j in range(len(mC[i])-1):  
			vRGTI[i].append(mC[i][j])
		vRGTI[i].append(vRGTIFiltr[1][i])
	#Сохраняю, предварительно удалив датасет, если он существует
	if db.datasetExists(well,dsrgti): db.datasetDelete(well,dsrgti)
	if VariableSaverLongDescription(well,  dsrgti, vRGTI)<0: 
		print "Error during saving of the RTGI table"		
		break
	db.datasetTypeChange(well,dsrgti,"interval")
#Ставлю РР контакты 
	if db.variableExists(well,dsc,"CONT_TVDSS_PP")==False: 
		vPPcont=PPcontFromRGTI(well, dsrgti, vCONT_zones)
		db.variableSave(well, dsc, "CONT_TVDSS_PP", "True Vertical Depth Sub Sea", "M",vPPcont, 0)
	else:
		vPPcont= db.variableData(well, dsc, "CONT_TVDSS_PP")
		FlagPPc=0
		for i in range(0,len(vPPcont)): 
			if vPPcont[i]!=MissingValue: FlagPPc=1
		if FlagPPc==0:
			vPPcont=PPcontFromRGTI(well,dsrgti, vCONT_zones)
			db.variableSave(well, dsc, "CONT_TVDSS_PP", "True Vertical Depth Sub Sea", "M",vPPcont, 0)
	print '<font color=red size=+1> CONTACTS_PP are following: </font>' 
	for i in range(0,len(vPPcont)): print vCONT_zones[i], "=",  round(vPPcont[i],2)
	print  '<font color=red size=+1>You have to delit  CONTACT_PP and run script again, if you have changed Fluid_Index  </font>' 
#Выполняю reporting, но сперва создаю двумерный массив [названия зон, контакты]
	vPPzone_cont=[vCONT_zones,vPPcont]
	#print vPPzone_cont
	mNC=NetComputation(well, vZONES, vMD, vTVDSS,vPorden,vSWWS,vSHF, vK_merge,vKo,vKw,vFluid,vIND,"NO_CONTACTS","","")
	NetComputation(well, vZONES, vMD, vTVDSS,vPorden,vSWWS,vSHF, vK_merge,vKo,vKw,vFluid,vIND,"CONTACTS_PP",vPPzone_cont, "nonswept")
	NetComputation(well, vZONES, vMD, vTVDSS,vPorden,vSWWS,vSHF, vK_merge,vKo,vKw,vFluid,vIND,"CONTACTS_PP",vPPzone_cont, "swept")
#Сохраняю кривые, для этого создаю массив из пар "название кривой-переменная", и потом запускаю функцию сохранения
	mCurve=[["RHOZ_apd", vRHOZ],["Fluid_Index",vFluid],["Por_uncut",vPoro],["Porden",vPorden],["SWWS", vSWWS],
					["Swi_nd",vSwi_nd],["Perm", vPerm],["Vsh_nd",vVsh_nd], ["K_tim_nd",vK_tim],["K_merge", vK_merge],
					["SW_SHF_bf", vSHF],["Vclgr", vVclgr],["Ko", vKo],["Kw", vKw],["WC_Corey", vWC_Corey],["KH_tvd_oil", vKH_tvd_oil],
					["KH_tvd_water", vKH_tvd_water],["KH_brine", vK_tim_nd_int]]
	if VariableSaver(well, ds, mCurve)==1: 
		print "All variables were saved"
	else:
		print "Not all variables were saved"
	print "Variable <cut> exists: ", db.variableExists(well,ds, "cut")
	print "OK"
############################################################################	
#__________________________Diameter_of_Inavasion___________________________________________
###########################################################################	

	import TechlogEnvCorrBakerHughes
	import TechlogMath
	AE90=db.variableData(well,ds,"AE90")# Deep induction resistivity
	AE20=db.variableData(well,ds,"AE30")# Medium induction resistivity
	RXOZ=db.variableData(well,ds,"AE10")# Flushed zone resistivity ytt
	Fluid_Index=db.variableData(well,ds,"Fluid_Index")
	DI=[0]*len(AE90)
	for i in range(len(AE90)):
		if Fluid_Index[i]!=MissingValue:
			if AE90[i]>=RXOZ[i]:
				DI[i]=TechlogEnvCorrBakerHughes.bh6_4DI(AE90[i],AE20[i],RXOZ[i])
			elif AE90[i]<RXOZ[i]:
				DI[i]=TechlogEnvCorrBakerHughes.bh6_5DI(AE90[i],AE20[i],RXOZ[i])	
			
			DI[i]=TechlogMath.unitValueConvert("in","M",DI[i])
			
	ok=db.variableSave(well,ds,"DI","Diameter Of Invasion","M",DI)
	if ok:
		print "DI successfully calculated and saved"	

############################################################################
############################################################################	
#__________________________Lithology___________________________________________
###########################################################################	
	Porden=db.variableData(well,ds,"Porden")
	Por_uncut=db.variableData(well,ds,"Por_uncut")
	Fluid_Index=db.variableData(well,ds,"Fluid_Index")
	TNPH=db.variableData(well,ds,"TNPH")
	LITH=[MissingValue]*len(Porden)
	for i in range(len(Porden)):
		if Por_uncut[i]!=MissingValue:
			if 	Porden[i]>0.165 and Fluid_Index[i]>0:
				LITH[i]=0
			if	Porden[i]<0.165 and Fluid_Index[i]>0:
				LITH[i]=1
			if Por_uncut[i]>0.14 and Fluid_Index[i]==-9999:
				LITH[i]=3
			if Fluid_Index[i]==-9999  and TNPH[i]<0.15:
				LITH[i]=2
			if LITH[i]==-9999:
				LITH[i]=4
	db.variableSave(well,ds,"LITH","Lithology","",LITH)	
	

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2015-12-31"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""