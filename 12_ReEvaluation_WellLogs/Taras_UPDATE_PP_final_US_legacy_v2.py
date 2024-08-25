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
DS="COMMON_05"
ZDS="ZONATION"
CDS="FLUID_CONTACTS"
		
#LIST=db.wellList()
LIST=db.selectedWellList()
for j in LIST:
	WELL=j
	print j
	
	if db.variableExists(WELL, DS, "ZDEN"):	
		#PA_block______________________________________
		TNPH=            Variable(WELL, "COMMON_05", "CN")
		RHOZ=            Variable(WELL, "COMMON_05", "RHOZ_d")
		RHOZ_old=        Variable(WELL, DS, "RHOZ_d")
		GR=              Variable(WELL, "COMMON_05", "GR")
	if db.variableExists(WELL, DS, "RHOZ"):	
		#PEX_block______________________________________
		TNPH=            Variable(WELL, DS, "TNPH")
		if db.variableExists(WELL, DS, "RHOZ_d"):
			RHOZ=            Variable(WELL, DS, "RHOZ_d")
			RHOZ_old=        Variable(WELL, DS, "RHOZ_d")
		else:
			RHOZ=            Variable(WELL, "COMMON_05", "RHOZ_apd") 
			RHOZ_old=        Variable(WELL, DS, "RHOZ")	
		GR=              Variable(WELL, DS, "GR")
		#LWD_block _____________________________________
	if db.variableExists(WELL, "COMMON_05", "SBD2"):
		TNPH=            Variable(WELL, DS, "TNPL")
		RHOZ=            Variable(WELL, DS, "RHOZ_d")
		RHOZ_old=        Variable(WELL, DS, "RHOZ_d")
		GR=              Variable(WELL, DS, "SGRC")
	#__________________________________________________

	RT=              Variable(WELL, DS, "RT")
	ZONE=            Variable(WELL, "ZONATION", "ZONES")
	DeptZone=        Variable(WELL, "ZONATION", "DEPTH")
	TVDSSZone=       Variable(WELL, "ZONATION", "TVDSS")
	DEPT=            Variable(WELL, DS, "DEPT")
	TVDSS=           Variable(WELL, DS, "TVDSS")
	Porden=         Variable(WELL, DS, "Porden")
	Por_uncut=     Variable(WELL, DS, "Por_uncut")
	SWWS=         Variable(WELL, DS,"SWWS")
	Perm=            Variable(WELL, DS, "Perm")
	K_tim_nd_int=    Variable(WELL, DS, "KH_brine")
	K_merge_thk=        Variable(WELL,DS, "K_merge")
	WaterCut=        Variable(WELL, DS, "WaterCut")
	Vclgr=           Variable(WELL, DS, "Vclgr")
	Vsh_nd=          Variable(WELL, DS, "Vsh_nd")
	Swi_nd=          Variable(WELL, DS, "Swi_nd")
	K_tim_nd=        Variable(WELL, DS, "K_tim_nd")
	Fluid_Index=     Variable(WELL, DS, "Fluid_Index")
	Cut=                Variable(WELL, DS,"cut")
	K_multiplier=     Variable(WELL, DS, "K_multiplier")

	#WC_Corey_Entry_paraneters______________________
	SW=Variable(WELL, DS, "SW_SHF_bf") 
	Swirr=Variable(WELL, DS, "Swi_k")
	Perm_wc=Variable(WELL, DS, "K_tim_nd")
	Kro=Variable(WELL, DS, "Kro")
	Krw=Variable(WELL, DS, "Krw")
	Ko=Variable(WELL, DS, "Ko")
	Kw=Variable(WELL, DS, "Kw")
	WC_Corey=Variable(WELL, DS, "WC_Corey")
	KH_tvd_oil=Variable(WELL, DS, "KH_tvd_oil")
	KH_tvd_water=Variable(WELL, DS, "KH_tvd_water") 
	
	#SHF_parameters_____________________________________
	SW_SHF=      Variable(WELL, DS, "SW_SHF_bf")
	Swi_K=           Variable(WELL, DS, "Swi_K")
	ZONES_cont=    Variable(WELL, CDS, "ZONES_cont")
	FWL_bf=      Variable(WELL, CDS, "FWL_bf")
	
	# Families & units assinment_____________________________
	Porden.unitNameChange("v/v")
	Porden.familyNameChange("Total Porosity")
	Por_uncut.unitNameChange("v/v")
	Por_uncut.familyNameChange("Porosity")
	Perm.unitNameChange("mD")
	Perm.familyNameChange("Permeability")
	SWWS.unitNameChange("v/v")
	SWWS.familyNameChange("Water Saturation")
	WaterCut.unitNameChange("%")
	SW_SHF.unitNameChange("v/v")
	SW_SHF.familyNameChange("Water Saturation")
	
	#Delta top & bottom for interval of processing_____________
	delta_top=5 #(m)
	delta_bot=1 #(m)
	
	#GR limits for Vcl_gr calculation____________________
	GRmin=55
	GRmax=130
	
	#Net cutoff's________________________________
	NEU_cutoff=0.27
	PHI_cutoff=0.13
	PHI_max_cutoff=0.26

	#Waxman-Smits coeffisients______________________
	BQv = 1.26
	Rw = 0.17
	m = 1.97
	n = 1.94
	
	# Corey tuniing parameters___________________________
	Sor_init=0.18 	  #Remaining oil saturation
	Krwe=1			#End point rel perm water
	Kroe=0.90			#End point rel perm oil
	Nw=3.5				#Corey exponent water
	No=1.90				#Corey exponent oil
	Uo=2.2				#Viscosity oil
	Uw=0.4				#Viscosity water
	W=0.3				#Wettability
	
	# Zones indexes variables inicialization____________________
	Start_ind=-9999
	AS9_0_ind=-9999
	AS9_0_SH_ind=-9999
	AS10_0_ind=-9999
	AS11_1_ind=-9999
	AS11_2_ind=-9999
	AS11_3_ind=-9999
	AS11_3_SH_ind=-9999
	Stop_ind=-9999
	
	# Zones indexes in Log Dataset identification__________________
	for z in range(0, ZONE.size()):
		zone=ZONE.value(z)
		deptzone=DeptZone.value(z)
		if zone=="AS9.0":
			AS9_0_ind= db.datasetZoneIndice(WELL, DS, ZDS, zone)[0]
			Start_ind=AS9_0_ind
		if zone=="AS9.0_SH":
			AS9_0_SH_ind= db.datasetZoneIndice(WELL, DS, ZDS, zone)[0]
		if zone=="AS10.0":
			AS10_0_ind= db.datasetZoneIndice(WELL, DS, ZDS, zone)[0]
		if zone=="AS11.1":
			AS11_1_ind= db.datasetZoneIndice(WELL, DS, ZDS, zone)[0]
		if zone=="AS11.2":
			AS11_2_ind= db.datasetZoneIndice(WELL, DS, ZDS, zone)[0]
		if zone=="AS11.3.1":
			AS11_3_ind= db.datasetZoneIndice(WELL, DS, ZDS, zone)[0]
		if zone=="Prodelta":
			AS11_3_SH_ind= db.datasetZoneIndice(WELL, DS, ZDS, zone)[0]
			Stop_ind=db.datasetZoneIndice(WELL, DS, ZDS, zone)[0]
		
	#warning if zones are absent______________________________
	if AS11_3_ind==-9999:
		print "AS11.3 is absent"
	
	#estimation of Log Dataset sampling rate_________________________
	SR=DEPT.samplingRate()
	
	# final reconciliation of processing boundaries______________________
	print "Pr",  Stop_ind
	if Stop_ind==-9999:
		Stop_ind=int(round(DEPT.size()-12/SR,0))
	
	Start_ind=int(round(Start_ind-delta_top/SR,0))
	Stop_ind=int(round(Stop_ind+delta_bot/SR,0)) 
	print  Stop_ind
	if Stop_ind>DEPT.size():
		Stop_ind=DEPT.size()
		
	# 100% water saturation initialization_____________________________
	for s in range (Start_ind, Stop_ind):
		swws=SWWS.value(s)
		dept=DEPT.value(s)
		swws=1
		SWWS.setValue(s, swws)
	#SWWS.save()
	
	# K_multiplier initialization___________________________________
	if not db.variableExists(WELL, DS, "K_multiplier"):
		for i in range(Start_ind, Stop_ind):
			K_multiplier.setValue(i, 1)
		K_multiplier.save()
	# iterative porosity & saturation calculation______________________
	for j in range (0,2):
		for i in range (Start_ind, Stop_ind):
			dept_ind=i
			rhoz = RHOZ.value(i)
			tnhp = TNPH.value(i)
			rt = RT.value(i)
			cut = Cut.value(i)
			por_uncut=Por_uncut.value(i)
			swws=SWWS.value(i)
			porden=Porden.value(i)

			shxo =1-(swws**0.2)
			fluden = (1-shxo)*1.01+(shxo)*0.8
			if dept_ind>AS9_0_ind and dept_ind<AS11_1_ind:
				if rhoz>2.425:
					Gd=2.685
				elif rhoz<2.341:
					Gd=2.63
				else:
					Gd=39.1264*rhoz-8.075652*pow(rhoz, 2)-44.70633
			else:
				Gd=+33.10218*rhoz-13.39015*pow(rhoz, 2)+1.810695*pow(rhoz, 3)-24.67913-0.00	
			porden = (Gd-rhoz)/(Gd-fluden)
			por_uncut=porden
			if porden < PHI_cutoff or tnhp >NEU_cutoff or cut==1 or porden>PHI_max_cutoff :
				porden = 0	
			if rt > 0 and porden > 0:
				swws = (Rw/(rt*(porden**m)))**(1/n)
				for j in range (0, 10):
					a= (rt*(porden**m))/(Rw)
					b= 1+(Rw*BQv)/swws
					swws = (a*b)**(-1/n)
			else:	
				swws = 1
			if swws>1:
				swws = 1
			SWWS.setValue(i, swws)
			Porden.setValue(i, porden)
			Por_uncut.setValue(i, por_uncut)
		Porden.save()
		Por_uncut.save()
		SWWS.save()
	#print "porosity & saturation are calculated"
	
	#units & families assinment________________________________________________
	Vsh_nd.familyNameChange("Shale Volume From Neutron and Density Porosity")
	Vsh_nd.unitNameChange("v/v")
	K_tim_nd.familyNameChange("Permeability")
	K_tim_nd.unitNameChange("mD")
	Swi_nd.familyNameChange("Irreducible Water Saturation")
	Swi_nd.unitNameChange("v/v")
	K_merge_thk.familyNameChange("Permeability")
	K_merge_thk.unitNameChange("mD")
	
	# extra parameters calculation__________________
	for i in range (Start_ind, Stop_ind):
		dept_ind=i
		perm=Perm.value(i)
		swws=SWWS.value(i)
		porden=Porden.value(i)
		watercut=WaterCut.value(i)
		rhoz=RHOZ.value(i)
		rhoz_old=RHOZ_old.value(i)
		gr=GR.value(i)
		tnph=TNPH.value(i)
		vsh_nd=Vsh_nd.value(i)
		dept=DEPT.value(i)
		swi_nd=Swi_nd.value(i)
		k_tim_nd=K_tim_nd.value(i)
		vclgr=Vclgr.value(i)
		
		# perm calcution____________________________________
		if porden >= PHI_cutoff:	
			if AS9_0_ind<dept_ind<AS9_0_SH_ind:
				perm =0.57*10**(+ 15.66762 * log10(porden/0.96) + 12.78244)
			if AS10_0_ind<dept_ind<AS11_1_ind:
				perm =0.57*10**( - 163.4489 * pow(porden/0.96, 2) + 96.01653 * porden/0.96 - 10.93067)
			if AS9_0_SH_ind<dept_ind<AS10_0_ind or  AS11_1_ind<i<AS11_2_ind:
				perm =0.57*10**( - 10.58756 * pow(porden/0.96, 2) + 35.18426 * porden/0.96 - 5.409782)
			if AS11_2_ind<dept_ind<AS11_3_ind:
				perm=0.57*10**( - 74.99309 * pow(porden/0.96, 2) + 50.78489 * porden/0.96 - 5.361396)
			if AS11_3_ind<dept_ind:
				perm=0.57*10**(- 34.4459 * pow(porden/0.96, 2) + 44.46815 * porden/0.96 - 6.007478)
		else:
			perm = 0.0001
		
		# calculation of Vsh_nd and Vclgr________________________
		vsh_nd=tnph-(2.65-rhoz_old)/1.64
		vclgr=(gr-GRmin)/(GRmax-GRmin)
		
		# calculation of Swi_nd
		if dept_ind>AS9_0_ind and dept_ind<AS11_1_ind:
			swi_nd=limitValue(10.0**(5.0763279*vsh_nd-0.68619953)+0.03, 0, 1)
		else:
			swi_nd=limitValue(10.0**(4.3839193*vsh_nd-0.58381749), 0, 1)
			
		# calculation of K_tim_nd_____________________________________________________________
		k_tim_nd=exp10(13.417868*(porden*(1-(swi_nd)))-3.0141375*(swi_nd)+0.75991657)*0.57
		if porden<0.1:
			swi_nd=0.999
			k_tim_nd=0.0001
			
		Vsh_nd.setValue(i, vsh_nd)
		K_tim_nd.setValue(i, k_tim_nd)
		Swi_nd.setValue(i, swi_nd)
		Vclgr.setValue(i, vclgr)
		WaterCut.setValue(i, watercut)
		Perm.setValue(i, perm)
	Perm.save()
	Vsh_nd.save()
	K_tim_nd.save()
	Swi_nd.save()
	Vclgr.save()
	
	#K_merge calculation____________________________________		
	count=0
	window=0.3
	s_r=DEPT.value(2)-DEPT.value(1)		
	treshold=	int(window/s_r)
	
	for j in range (Start_ind, Stop_ind):
		merge=0
		porden=Porden.value(j)
		perm=Perm.value(j)
		k_tim=K_tim_nd.value(j)
		k_merge=K_merge_thk.value(j)
		for t in range (j, j-treshold, -1):
			if Porden.value(t)==0:
				merge=1
		if merge==1:
			k_merge=perm
		else:
			k_merge=k_tim		
		
		K_merge_thk.setValue(j, k_merge) 		
	K_merge_thk.save()
	for j in range (Stop_ind, Start_ind,  -1):
		merge=0
		porden=Porden.value(j)
		perm=Perm.value(j)
		k_tim=K_tim_nd.value(j)
		k_merge=K_merge_thk.value(j)
		for t in range (j,j+treshold):
			if Porden.value(t)==0:
				merge=1
		if merge==1:
			k_merge=perm
		else:
			k_merge=k_tim		
		if perm/k_tim>3:
			k_merge=perm
		if k_merge<0:
			k_merge=0.0001
		
		K_merge_thk.setValue(j, k_merge) 		
	K_merge_thk.save()

	for j in range (Stop_ind, Start_ind,  -1):
		merge=0
		k_m=K_multiplier.value(j)
		k_merge=K_merge_thk.value(j)

		k_merge=k_merge*k_m
		
		K_merge_thk.setValue(j, k_merge) 		
	K_merge_thk.save()
	
	#Satiration Height Function application______________________________________
	for z in range(0, ZONES_cont.size()):
		zone=ZONES_cont.value(z)
		FWL=FWL_bf.value(z)
		#print zone, FWL
		if zone=="AS9.0":
			Start_ind_shf=AS9_0_ind
			Stop_ind_shf=AS9_0_SH_ind
		if zone=="AS10.0":
			Start_ind_shf=AS10_0_ind
			Stop_ind_shf=AS11_1_ind
		if zone=="AS9.0_SH":
			Start_ind_shf=AS9_0_SH_ind
			Stop_ind_shf=AS10_0_ind
		if zone=="AS11.1":
			Start_ind_shf=AS11_1_ind
			Stop_ind_shf=AS11_2_ind
		if zone=="AS11.2":
			Start_ind_shf=AS11_2_ind
			Stop_ind_shf=AS11_3_ind
		if zone=="AS11.3.1":
			Start_ind_shf=AS11_3_ind
			Stop_ind_shf=Stop_ind
			
		#print Start_ind_shf, Stop_ind_shf
	
		for i in range (Start_ind_shf, Stop_ind_shf):
			HAFWL = FWL-TVDSS.value(i) 
			SW = SW_SHF.value(i)
			tvdss = TVDSS.value(i)
			dept = DEPT.value(i)
			K= K_merge_thk.value(i)/0.57
#			if K>300:
#			  K=300
#			if K<0.01:
#			  K=0.01
			POR=Porden.value(i)/0.96
			SWi=Swi_K.value(i)
			PCe=0
			if FWL<>-9999:
				PC_IFT1 = (HAFWL * (1.01 - 0.82) * 0.0981 * (1.0 / (30 * 0.866)))
				if  POR>0:
					SWi = 0.268145 - 0.00308514 * sqrt(K / POR)
					try:
						PCe = 0.0280682 * pow(sqrt(K / POR), -1.23057)
						N = 2
						if (PCe / PC_IFT1)>0:
							SW = min(1, max(0, SWi + (1 - SWi) * (PCe / PC_IFT1) ** (1.0 / N)))
					except:
						SW=1		
				else:
					SW=1
				if tvdss>FWL	:
					SW=1
			else:
				SW=1
			SW_SHF.setValue(i, SW)
		SW_SHF.save()
	
	
			
	#Corey model____________________________________________________________
	for i in range (Start_ind, Stop_ind):		
		por=Porden.value(i)
		Sw=SW_SHF.value(i)
		Swir = Swirr.value(i)
		K_ro = Kro.value(i)
		K_rw = Krw.value(i)
		K_o = Ko.value(i)
		K_w = Kw.value(i)
		perm = K_merge_thk.value(i)
		WC = WC_Corey.value(i)

		swi_k=limitValue(10**(-0.19805342*log10(max((perm/1.33)/0.57,0.001))-0.17303015), 0, 0.9999)
		PcEntry=limitValue((0.8*(10.625*swi_k-2.03125)),0.001, 100)
		Prkpa=1*(9.81*40)*(1-0.82)
		Swir =(Prkpa/PcEntry)**(-0.37)*(1-0.65*swi_k)+0.65*swi_k
		#Swir = - 0.145 * log10(perm) + 0.635
		if Swir >= 0.780468:
			Swir=1

		
		if Sw<Swir:
			Swir=Sw
		
		if 1==1:
			if por>PHI_cutoff: 
			
				if (1-Sw)<Sor_init:
					Sor=1-Sw
				else:
					Sor=Sor_init			
				
				K_ro=limitValue((Kroe*((1-Sw)/(max(1-Swir,0.01)))**No), 0, 1)
				K_o=perm*K_ro
				if perm<5:
					K_o=0.001
				
				K_rw=limitValue((Krwe*((Sw-Swir)/(max(1-Swir,0.01)))**Nw), 0, 1)
				#K_rw=limitValue((Krwe*((Sw-Swir)/(max(1-Sor-Swir,0.01)))**Nw), 0, 1)
				K_w=perm*K_rw
				
				WC = limitValue(100*(K_w/Uw)/limitValue(((K_o/Uo)+(K_w/Uw)),1e-9,1e9), 0, 100)
				if perm<5:
					WC=0

			else:
				K_ro=0.001
				K_rw=0.001
				K_o=0.001
				K_w=0.001
				WC=0

			if Porden.value(i+1)==0 or Porden.value(i-1)==0: 
				WC=0
				
#		Kro.setValue(i, K_ro)
#		Krw.setValue(i, K_rw)
		Ko.setValue(i, K_o)
		Kw.setValue(i, K_w)
		WC_Corey.setValue(i, WC)
		Swirr.setValue(i, Swir)
	Ko.save()
	Kw.save()
	WC_Corey.save()
	#KH
	#=================================================================
	kh_o=0
	kh_w=0
	KH=0
	for k in range (Stop_ind, Start_ind, -1):
		dept=DEPT.value(k)
		tvdss=TVDSS.value(k)
		K_o=Ko.value(k)
		if K_o<0:
			K_o=0.0001
		K_w=Kw.value(k)
		if K_w<0:
			K_w=0.0001
		K=K_merge_thk.value(k)
		if K<0:
			K=0.0001
		if K_o>0:
			kh_o = kh_o + K_o*(TVDSS.value(k+1)-tvdss)
		KH_tvd_oil.setValue(k, kh_o)
		if K_w>0:
			kh_w = kh_w + K_w*(TVDSS.value(k+1)-tvdss)
		KH_tvd_water.setValue(k, kh_w)
		KH=KH+K*(TVDSS.value(k+1)-tvdss)
		K_tim_nd_int.setValue(k, KH)
	KH_tvd_oil.save()
	KH_tvd_water.save()
	K_tim_nd_int.save()
	print "ok"
import Fluid_Index_US_M_W

__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""