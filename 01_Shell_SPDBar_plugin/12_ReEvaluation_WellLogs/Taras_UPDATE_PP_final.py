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
import os
import win32com.client as win32
import pythoncom
pythoncom.CoInitialize()
import webbrowser
import math
import TechlogStat as ts


def folder_path(well):
	path = r"C:\Apps\UPDATE_PPEVAL" + "\\" + well
	if os.path.exists(path) == True:
		pass
	else:
		print "Well folder is done"
		os.mkdir(path)
	return(path)


def create_xls(well):
	path = folder_path(well)
	create_report_xl = open(folder_path(well) + "\\" + well + ".xls", "w")
	create_report_xl.close()
	report_xl_file = path + "\\" + well + ".xls"
	xl = win32.Dispatch("Excel.Application")
	xl.Visible = 1
	wb = xl.Workbooks.Open(report_xl_file)
	for i in range(0,7):
		wb.Sheets.Add()
	wb.Sheets(1).Name = "Depth plot"
	wb.Sheets(2).Name = "sumavs tvdss_cher"
	wb.Sheets(3).Name = "Remarks PP_PG_RE"
	wb.Sheets(4).Name = "Reference Log"
	wb.Sheets(5).Name = "Rock_Properties_Table"
	wb.Sheets(6).Name = "QC"
	wb.Sheets(7).Name = "Map"
	wb.Sheets(8).Name = "cor_panel"
	return(wb)

def insert_1plot(well,path,wb):
	pict_path = path + "\\" + well+".png"
	if os.path.exists(pict_path) == True:
		Sheet = wb.Sheets(1)
		Sheet.Activate()
		Sheet.Range("A1").Select()
		Sheet.Shapes.AddPicture(pict_path, False, True,0,0,671,776)
	else:
		print "Нет скважинной диаграммы в папке"

def insert_1and2page(well,path, wb):
	s = ','
	Sheet = wb.Sheets(2)
	#Sheet.Activate()
	
	i=3
	com_ds = 'COMMON_05'
	md = db.variableData(well, com_ds, 'DEPT')
	tvdss = db.variableData(well, com_ds, 'TVDSS')
	porden = db.variableData(well, com_ds, 'Porden')
	perm = db.variableData(well, com_ds, 'K_merge')
	permo = db.variableData(well, com_ds, 'Ko')
	permw = db.variableData(well, com_ds, 'Kw')
	swws = db.variableData(well, com_ds, 'SWWS')
	sw_shf_bf = db.variableData(well, com_ds, 'SW_SHF_bf')
	fi = db.variableData(well, com_ds, 'Fluid_Index')
	z_ds = 'ZONATION'
	zones = db.variableData(well, z_ds, 'ZONES')
	pp_ds = 'CONTACTS'
	#gg_ds = 'CONTACTS_GG'
	if db.datasetExists(well, pp_ds):
		zone_c = db.variableData(well, pp_ds, 'ZONES')
		tvdss_c = db.variableData(well, pp_ds, 'CONT_TVDSS_PP')
		cont_type = pp_ds
	#else:
		#zone_c = db.variableData(well, pp_ds, 'ZONES')
		#tvdss_c = db.variableData(well, pp_ds, 'CONT_TVDSS')
		#cont_type = pp_ds
	for ind in range(1,18):
		wb.Sheets(2).Cells(i-1,ind).BorderAround(1,2,1)
	wb.Sheets(2).Cells(i-1,1).Value="Well"
	wb.Sheets(2).Columns(1).ColumnWidth = 25
	wb.Sheets(2).Cells(i-1,2).Value="Mode"
	wb.Sheets(2).Cells(i-1,3).Value="ZONE"
	wb.Sheets(2).Cells(i-1,4).Value="TOP_md"
	wb.Sheets(2).Cells(i-1,5).Value="BOT_md"
	wb.Sheets(2).Cells(i-1,6).Value="Gross_md"
	wb.Sheets(2).Cells(i-1,7).Value="TOP_tvdss"
	wb.Sheets(2).Cells(i-1,8).Value="BOT_tvdss"
	wb.Sheets(2).Cells(i-1,9).Value="Gross_tvdss"
	wb.Sheets(2).Cells(i-1,10).Value="NET"
	wb.Sheets(2).Cells(i-1,11).Value="PHI"
	wb.Sheets(2).Cells(i-1,12).Value="So_WS"
	wb.Sheets(2).Cells(i-1,13).Value="So_shf"
	wb.Sheets(2).Cells(i-1,14).Value="Kbr"
	wb.Sheets(2).Cells(i-1,15).Value="Ko"
	wb.Sheets(2).Cells(i-1,16).Value="Kw"
	wb.Sheets(2).Cells(i-1,17).Value="CONTACT"
	for zone in zones:
		# Zone border definitions
		if zone == "AS9.0" or zone == "AS9.0_SH" or zone == "AS10.0" or zone == "AS11.1" or zone == "AS11.2" or zone == "AS11.3" or zone == "AS11.3_1" or zone == "AS11.3_2"  or zone == "AS11.3.1" or zone == "AS11.3.2":  
			zone_top_ind=db.datasetZoneIndice(well, com_ds, z_ds, zone)[0]
			zone_bot_ind=db.datasetZoneIndice(well, com_ds, z_ds, zone)[1]
			zone_top_tvdss = tvdss[zone_top_ind]
			zone_bot_tvdss = tvdss[zone_bot_ind]
			zone_top_md = md[zone_top_ind]
			zone_bot_md = md[zone_bot_ind]
			por_h, sum_h, sw_h_por, swshf_h_por, h_por, perm_h, ko_h, kw_h, H = 0, 0.0001, 0, 0, 0.0001, 0, 0, 0, 0
			# Net Sand Computation
			for j in range(zone_top_ind, zone_bot_ind):
				tvd = tvdss[j]
				por = porden[j]
				sw = swws[j]
				k = perm[j]
				ko = permo[j]
				kw = permw[j]
				sw_shf = sw_shf_bf[j]
				if por < 0:	por = 0
				if sw < 0:	sw = 1
				if sw_shf < 0:	sw_shf = 1
				if k < 0.001:	k = 0.001
				if ko < 0.001:	ko = 0.001
				if kw < 0.001:	kw = 0.001
				if por>0 and tvd>zone_top_tvdss and tvd<zone_bot_tvdss:
					if porden[j-1]<>0 and porden[j+1]<>0:
						por_h += por*(tvd-tvdss[j-1])
						sum_h += tvd-tvdss[j-1]
						sw_h_por += sw*por*(tvd-tvdss[j-1])
						swshf_h_por += sw_shf*por*(tvd-tvdss[j-1])
						h_por += por*(tvd-tvdss[j-1])
						perm_h += k*(tvd-tvdss[j-1])
						ko_h += ko*(tvd-tvdss[j-1])
						kw_h += kw*(tvd-tvdss[j-1])
					H += (tvd-tvdss[j-1]) #but for total net thickness boundary samples are included
			if sw_h_por==0:
				sw_h_por=1
				swshf_h_por=1
				h_por=1
			# Note: average properties defined as por_h/sum_h - ie using summations without boundary samples; Total net is H - ie with boundary samples
			for ind in range(1,18):
				wb.Sheets(2).Cells(i,ind).BorderAround(1,2,1)
			wb.Sheets(2).Cells(i,1).Value=well
			wb.Sheets(2).Cells(i,2).Value="NET_sand"
			wb.Sheets(2).Cells(i,3).Value=zone
			wb.Sheets(2).Cells(i,4).Value=zone_top_md
			wb.Sheets(2).Cells(i,5).Value=zone_bot_md
			wb.Sheets(2).Cells(i,6).Value=zone_bot_md-zone_top_md
			wb.Sheets(2).Cells(i,7).Value=zone_top_tvdss
			wb.Sheets(2).Cells(i,8).Value=zone_bot_tvdss
			wb.Sheets(2).Cells(i,9).Value=zone_bot_tvdss-zone_top_tvdss
			wb.Sheets(2).Cells(i,10).Value=H
			wb.Sheets(2).Cells(i,11).Value=por_h/sum_h
			wb.Sheets(2).Cells(i,12).Value=1-sw_h_por/h_por
			wb.Sheets(2).Cells(i,13).Value=1-swshf_h_por/h_por	
			wb.Sheets(2).Cells(i,14).Value=perm_h/sum_h	
			wb.Sheets(2).Cells(i,15).Value=ko_h/sum_h
			wb.Sheets(2).Cells(i,16).Value=kw_h/sum_h
			
			i+=1
	i+=3
	for ind in range(1,18):
		wb.Sheets(2).Cells(i-1,ind).BorderAround(1,2,1)
	wb.Sheets(2).Cells(i-1,1).Value="Well"
	wb.Sheets(2).Cells(i-1,2).Value="Mode"
	wb.Sheets(2).Cells(i-1,3).Value="ZONE"
	wb.Sheets(2).Cells(i-1,4).Value="TOP_md"
	wb.Sheets(2).Cells(i-1,5).Value="BOT_md"
	wb.Sheets(2).Cells(i-1,6).Value="Gross_md"
	wb.Sheets(2).Cells(i-1,7).Value="TOP_tvdss"
	wb.Sheets(2).Cells(i-1,8).Value="BOT_tvdss"
	wb.Sheets(2).Cells(i-1,9).Value="Gross_tvdss"
	wb.Sheets(2).Cells(i-1,10).Value="NET"
	wb.Sheets(2).Cells(i-1,11).Value="PHI"
	wb.Sheets(2).Cells(i-1,12).Value="So_WS"
	wb.Sheets(2).Cells(i-1,13).Value="So_shf"
	wb.Sheets(2).Cells(i-1,14).Value="Kbr"
	wb.Sheets(2).Cells(i-1,15).Value="Ko"
	wb.Sheets(2).Cells(i-1,16).Value="Kw"
	wb.Sheets(2).Cells(i-1,17).Value="CONTACT"
	
	
	for x in range(2):
		if x == 1:	x_type = 'TOTAL_NET_pay'
		if x == 0:	x_type = 'NON_SWEPT_NET_pay'
		sum_1page_h = []
		sum_1page_phi = []
		sum_1page_sh = []
		sum_1page_ehc = []
		sum_1page_kh = []
		
		for zone in zones:
			# Zone border definitions
			if zone == "AS9.0" or zone == "AS9.0_SH" or zone == "AS10.0" or zone == "AS11.1" or zone == "AS11.2" or zone == "AS11.3" or zone == "AS11.3_1" or zone == "AS11.3_2" or zone == "AS11.3.1" or zone == "AS11.3.2":
				zone_top_ind=db.datasetZoneIndice(well, com_ds, z_ds, zone)[0]
				zone_bot_ind=db.datasetZoneIndice(well, com_ds, z_ds, zone)[1]
				zone_top_tvdss = tvdss[zone_top_ind]
				zone_bot_tvdss = tvdss[zone_bot_ind]
				zone_top_md = md[zone_top_ind]
				zone_bot_md = md[zone_bot_ind]
				if db.datasetExists(well, pp_ds):
					CONTACT= MissingValue
					for z in range(len( zone_c)):
						if zone==zone_c[z]:
							CONTACT=tvdss_c[z]
					por_h, sum_h, sw_h_por, swshf_h_por, h_por, perm_h, ko_h, kw_h, H = 0, 0.0001, 0, 0, 0.0001, 0, 0, 0, 0
					# Net Pay Computation
					for j in range(zone_top_ind, zone_bot_ind):
						m = 1
						if x == 0 and fi[j] == 5:
							m = 0
						tvd = tvdss[j]
						por = porden[j]
						sw = swws[j]
						k = perm[j]
						ko = permo[j]
						kw = permw[j]
						sw_shf = sw_shf_bf[j]
						if por < 0:	por = 0
						if sw < 0:	sw = 1
						if sw_shf < 0:	sw_shf = 1
						if k < 0.001:	k = 0.001
						if ko < 0.001:	ko = 0.001
						if kw < 0.001:	kw = 0.001
						if por>0 and tvd>zone_top_tvdss and tvd<zone_bot_tvdss and tvd<CONTACT:
							if porden[j-1]<>0 and porden[j+1]<>0:
								por_h += m*por*(tvd-tvdss[j-1])
								sum_h +=m*(tvd-tvdss[j-1])
								sw_h_por += m*sw*por*(tvd-tvdss[j-1])
								swshf_h_por += m*sw_shf*por*(tvd-tvdss[j-1])
								h_por += m*por*(tvd-tvdss[j-1])
								perm_h += m*k*(tvd-tvdss[j-1])
								ko_h += m*ko*(tvd-tvdss[j-1])
								kw_h += m*kw*(tvd-tvdss[j-1])
							H += m*(tvd-tvdss[j-1])
							
					if sw_h_por==0:
						sw_h_por=1
						swshf_h_por=1
						h_por=1
					if well.startswith("SVA"):
						if x_type=="NON_SWEPT_NET_pay":
							for ind in range(1,18):
								wb.Sheets(2).Cells(i,ind).BorderAround(1,2,1)
							wb.Sheets(2).Cells(i,1).Value=well			
							wb.Sheets(2).Cells(i,2).Value=x_type
							wb.Sheets(2).Cells(i,3).Value=zone
							wb.Sheets(1).Cells(50+i,2).Value=zone
							wb.Sheets(2).Cells(i,4).Value=zone_top_md
							wb.Sheets(2).Cells(i,5).Value=zone_bot_md
							wb.Sheets(2).Cells(i,6).Value=zone_bot_md-zone_top_md
							wb.Sheets(2).Cells(i,7).Value=zone_top_tvdss
							wb.Sheets(1).Cells(50+i,3).Value=zone_top_tvdss
							wb.Sheets(2).Cells(i,8).Value=zone_bot_tvdss
							wb.Sheets(1).Cells(50+i,4).Value=zone_bot_tvdss
							wb.Sheets(2).Cells(i,9).Value=zone_bot_tvdss-zone_top_tvdss
							wb.Sheets(2).Cells(i,10).Value=H
							wb.Sheets(1).Cells(50+i,10).Value=round(H,2)
							wb.Sheets(2).Cells(i,11).Value=por_h/sum_h
							wb.Sheets(1).Cells(50+i,11).Value=round(por_h/sum_h,2)
							wb.Sheets(2).Cells(i,12).Value=1-sw_h_por/h_por
							wb.Sheets(1).Cells(50+i,12).Value=round(1-sw_h_por/h_por,2)
							wb.Sheets(2).Cells(i,13).Value=1-swshf_h_por/h_por
							wb.Sheets(1).Cells(50+i,13).Value=round(H*(por_h/sum_h)*(1-sw_h_por/h_por),2)
							wb.Sheets(2).Cells(i,14).Value=perm_h/sum_h
							wb.Sheets(1).Cells(50+i,14).Value=round(H*(perm_h/sum_h),0)
							wb.Sheets(2).Cells(i,15).Value=ko_h/sum_h
							wb.Sheets(2).Cells(i,16).Value=kw_h/sum_h	
							wb.Sheets(2).Cells(i,17).Value=CONTACT
	
						elif x_type=="TOTAL_NET_pay":
							for ind in range(1,18):
								wb.Sheets(2).Cells(i+2,ind).BorderAround(1,2,1)
							wb.Sheets(2).Cells(i+3,1).Value=well			
							wb.Sheets(2).Cells(i+3,2).Value=x_type
							wb.Sheets(2).Cells(i+3,3).Value=zone
							wb.Sheets(2).Cells(i+3,4).Value=zone_top_md
							wb.Sheets(2).Cells(i+3,5).Value=zone_bot_md
							wb.Sheets(2).Cells(i+3,6).Value=zone_bot_md-zone_top_md
							wb.Sheets(2).Cells(i+3,7).Value=zone_top_tvdss
							wb.Sheets(2).Cells(i+3,8).Value=zone_bot_tvdss
							wb.Sheets(2).Cells(i+3,9).Value=zone_bot_tvdss-zone_top_tvdss
							wb.Sheets(2).Cells(i+3,10).Value=H
							wb.Sheets(2).Cells(i+3,11).Value=por_h/sum_h
							wb.Sheets(2).Cells(i+3,12).Value=1-sw_h_por/h_por
							wb.Sheets(2).Cells(i+3,13).Value=1-swshf_h_por/h_por
							wb.Sheets(2).Cells(i+3,14).Value=perm_h/sum_h
							wb.Sheets(2).Cells(i+3,15).Value=ko_h/sum_h
							wb.Sheets(2).Cells(i+3,16).Value=kw_h/sum_h	
							wb.Sheets(2).Cells(i+3,17).Value=CONTACT
							for ind in range(1,18):
								wb.Sheets(2).Cells(i+3,ind).BorderAround(1,2,1)
							
							#Создаются списки для подсчета параметров на 1й странице
							sum_1page_h.append(round(H,1))
							sum_1page_phi.append(round(por_h/sum_h,2))
							sum_1page_sh.append(round(1-sw_h_por/h_por,2))
							sum_1page_ehc.append(round(H*(por_h/sum_h)*(1-sw_h_por/h_por),2))
							sum_1page_kh.append(round(H*(perm_h/sum_h),0))
						i+=1
						
					if well.startswith("WS"):
						if x_type=="NON_SWEPT_NET_pay":
							for ind in range(1,18):
								wb.Sheets(2).Cells(i,ind).BorderAround(1,2,1)
							wb.Sheets(2).Cells(i,1).Value=well			
							wb.Sheets(2).Cells(i,2).Value=x_type
							wb.Sheets(2).Cells(i,3).Value=zone
							wb.Sheets(1).Cells(49+i,2).Value=zone
							wb.Sheets(2).Cells(i,4).Value=zone_top_md
							wb.Sheets(2).Cells(i,5).Value=zone_bot_md
							wb.Sheets(2).Cells(i,6).Value=zone_bot_md-zone_top_md
							wb.Sheets(2).Cells(i,7).Value=zone_top_tvdss
							wb.Sheets(1).Cells(49+i,3).Value=zone_top_tvdss
							wb.Sheets(2).Cells(i,8).Value=zone_bot_tvdss
							wb.Sheets(1).Cells(49+i,4).Value=zone_bot_tvdss
							wb.Sheets(2).Cells(i,9).Value=zone_bot_tvdss-zone_top_tvdss
							wb.Sheets(2).Cells(i,10).Value=H
							wb.Sheets(1).Cells(49+i,10).Value=round(H,2)
							wb.Sheets(2).Cells(i,11).Value=por_h/sum_h
							wb.Sheets(1).Cells(49+i,11).Value=round(por_h/sum_h,2)
							wb.Sheets(2).Cells(i,12).Value=1-sw_h_por/h_por
							wb.Sheets(1).Cells(49+i,12).Value=round(1-sw_h_por/h_por,2)
							wb.Sheets(2).Cells(i,13).Value=1-swshf_h_por/h_por
							wb.Sheets(1).Cells(49+i,13).Value=round(H*(por_h/sum_h)*(1-sw_h_por/h_por),2)
							wb.Sheets(2).Cells(i,14).Value=perm_h/sum_h
							wb.Sheets(1).Cells(49+i,14).Value=round(H*(perm_h/sum_h),0)
							wb.Sheets(2).Cells(i,15).Value=ko_h/sum_h
							wb.Sheets(2).Cells(i,16).Value=kw_h/sum_h	
							wb.Sheets(2).Cells(i,17).Value=CONTACT
	
						elif x_type=="TOTAL_NET_pay":
							for ind in range(1,18):
								wb.Sheets(2).Cells(i+2,ind).BorderAround(1,2,1)
							wb.Sheets(2).Cells(i+3,1).Value=well			
							wb.Sheets(2).Cells(i+3,2).Value=x_type
							wb.Sheets(2).Cells(i+3,3).Value=zone
							wb.Sheets(2).Cells(i+3,4).Value=zone_top_md
							wb.Sheets(2).Cells(i+3,5).Value=zone_bot_md
							wb.Sheets(2).Cells(i+3,6).Value=zone_bot_md-zone_top_md
							wb.Sheets(2).Cells(i+3,7).Value=zone_top_tvdss
							wb.Sheets(2).Cells(i+3,8).Value=zone_bot_tvdss
							wb.Sheets(2).Cells(i+3,9).Value=zone_bot_tvdss-zone_top_tvdss
							wb.Sheets(2).Cells(i+3,10).Value=H
							wb.Sheets(2).Cells(i+3,11).Value=por_h/sum_h
							wb.Sheets(2).Cells(i+3,12).Value=1-sw_h_por/h_por
							wb.Sheets(2).Cells(i+3,13).Value=1-swshf_h_por/h_por
							wb.Sheets(2).Cells(i+3,14).Value=perm_h/sum_h
							wb.Sheets(2).Cells(i+3,15).Value=ko_h/sum_h
							wb.Sheets(2).Cells(i+3,16).Value=kw_h/sum_h	
							wb.Sheets(2).Cells(i+3,17).Value=CONTACT
							for ind in range(1,18):
								wb.Sheets(2).Cells(i+3,ind).BorderAround(1,2,1)
							
							#Создаются списки для подсчета параметров на 1й странице
							sum_1page_h.append(round(H,1))
							sum_1page_phi.append(round(por_h/sum_h,2))
							sum_1page_sh.append(round(1-sw_h_por/h_por,2))
							sum_1page_ehc.append(round(H*(por_h/sum_h)*(1-sw_h_por/h_por),2))
							sum_1page_kh.append(round(H*(perm_h/sum_h),0))
						i+=1
	
	if well.startswith("WS"):
		i-=3
		wb.Sheets(2).Cells(i,1).Value="Well"
		wb.Sheets(2).Cells(i,2).Value="Mode"
		wb.Sheets(2).Cells(i,3).Value="ZONE"
		wb.Sheets(2).Cells(i,4).Value="TOP_md"
		wb.Sheets(2).Cells(i,5).Value="BOT_md"
		wb.Sheets(2).Cells(i,6).Value="Gross_md"
		wb.Sheets(2).Cells(i,7).Value="TOP_tvdss"
		wb.Sheets(2).Cells(i,8).Value="BOT_tvdss"
		wb.Sheets(2).Cells(i,9).Value="Gross_tvdss"
		wb.Sheets(2).Cells(i,10).Value="NET"
		wb.Sheets(2).Cells(i,11).Value="PHI"
		wb.Sheets(2).Cells(i,12).Value="So_WS"
		wb.Sheets(2).Cells(i,13).Value="So_shf"
		wb.Sheets(2).Cells(i,14).Value="Kbr"
		wb.Sheets(2).Cells(i,15).Value="Ko"
		wb.Sheets(2).Cells(i,16).Value="Kw"
		wb.Sheets(2).Cells(i,17).Value="CONTACT"
		
	if well.startswith("SVA"):
		i-=2
		wb.Sheets(2).Cells(i,1).Value="Well"
		wb.Sheets(2).Cells(i,2).Value="Mode"
		wb.Sheets(2).Cells(i,3).Value="ZONE"
		wb.Sheets(2).Cells(i,4).Value="TOP_md"
		wb.Sheets(2).Cells(i,5).Value="BOT_md"
		wb.Sheets(2).Cells(i,6).Value="Gross_md"
		wb.Sheets(2).Cells(i,7).Value="TOP_tvdss"
		wb.Sheets(2).Cells(i,8).Value="BOT_tvdss"
		wb.Sheets(2).Cells(i,9).Value="Gross_tvdss"
		wb.Sheets(2).Cells(i,10).Value="NET"
		wb.Sheets(2).Cells(i,11).Value="PHI"
		wb.Sheets(2).Cells(i,12).Value="So_WS"
		wb.Sheets(2).Cells(i,13).Value="So_shf"
		wb.Sheets(2).Cells(i,14).Value="Kbr"
		wb.Sheets(2).Cells(i,15).Value="Ko"
		wb.Sheets(2).Cells(i,16).Value="Kw"
		wb.Sheets(2).Cells(i,17).Value="CONTACT"
	
#Присваивание ячейкам на 1й странице отчестных значений
	if well.startswith("WS"):
		i+=3
		wb.Sheets(1).Cells(44+i,2).Value="Total"
		wb.Sheets(1).Cells(44+i,10).Value = round(ts.sum(sum_1page_h),1)
		sum_1page_phi = filter(lambda x: x>0, sum_1page_phi)
		wb.Sheets(1).Cells(44+i,11).Value = round(ts.average(sum_1page_phi),2)
		sum_1page_sh = filter(lambda x: x>0, sum_1page_sh)
		wb.Sheets(1).Cells(44+i,12).Value = round(ts.average(sum_1page_sh),2)
		wb.Sheets(1).Cells(44+i,13).Value = round(ts.sum(sum_1page_ehc),2)
		wb.Sheets(1).Cells(44+i,14).Value = round(ts.sum(sum_1page_kh),0)
		
	if well.startswith("SVA"):
		i+=4
		wb.Sheets(1).Cells(44+i,2).Value="Total"
		wb.Sheets(1).Cells(44+i,10).Value = round(ts.sum(sum_1page_h),1)
		sum_1page_phi = filter(lambda x: x>0, sum_1page_phi)
		wb.Sheets(1).Cells(44+i,11).Value = round(ts.average(sum_1page_phi),2)
		sum_1page_sh = filter(lambda x: x>0, sum_1page_sh)
		wb.Sheets(1).Cells(44+i,12).Value = round(ts.average(sum_1page_sh),2)
		wb.Sheets(1).Cells(44+i,13).Value = round(ts.sum(sum_1page_ehc),2)
		wb.Sheets(1).Cells(44+i,14).Value = round(ts.sum(sum_1page_kh),0)
		
#Отрисовка отчетной таблицы на 1й странице
	wb.Sheets(1).Cells(57,1).Value = "Well"
	wb.Sheets(1).Cells(57,2).Value = "ZONE"
	wb.Sheets(1).Cells(57,3).Value = "ZONE"
	wb.Sheets(1).Cells(57,4).Value = "ZONE"
	wb.Sheets(1).Cells(58,2).Value = "NAME"
	wb.Sheets(1).Cells(58,3).Value = "TOP"
	wb.Sheets(1).Cells(58,4).Value = "BASE"
	wb.Sheets(1).Cells(59,3).Value = "(m TVDSS)"
	wb.Sheets(1).Cells(59,3).Font.Size = 10
	wb.Sheets(1).Cells(59,4).Value = "(m TVDSS)"
	wb.Sheets(1).Cells(59,4).Font.Size = 10
	wb.Sheets(1).Cells(56,7).Value = "Model predicted Net Pay non swept"
	wb.Sheets(1).Cells(56,7).WrapText = False
	wb.Sheets(1).Cells(56,12).Value = "Net Pay non swept"
	wb.Sheets(1).Cells(56,12).WrapText = False
	wb.Sheets(1).Cells(55,9).Value = "NON SWEPT NET PAY m TVDSS"
	wb.Sheets(1).Cells(55,9).WrapText = False
	
	wb.Sheets(1).Cells(57,5).Value ="NET"
	wb.Sheets(1).Cells(57,6).Value ="AVG"
	wb.Sheets(1).Cells(57,7).Value ="AVG"
	wb.Sheets(1).Cells(57,8).Value ="EHC"
	wb.Sheets(1).Cells(57,9).Value ="Kh"
	wb.Sheets(1).Cells(58,5).Value ="PAY"
	wb.Sheets(1).Cells(58,6).Value ="PHI"
	wb.Sheets(1).Cells(58,7).Value ="Sh"
	wb.Sheets(1).Cells(59,5).Value ="(m)"
	wb.Sheets(1).Cells(59,6).Value ="(frac)"
	wb.Sheets(1).Cells(59,7).Value ="(frac)"
		
	wb.Sheets(1).Cells(57,10).Value ="NET"
	wb.Sheets(1).Cells(57,11).Value ="AVG"
	wb.Sheets(1).Cells(57,12).Value ="AVG"
	wb.Sheets(1).Cells(57,13).Value ="EHC"
	wb.Sheets(1).Cells(57,14).Value ="Kh"
	wb.Sheets(1).Cells(58,10).Value ="PAY"
	wb.Sheets(1).Cells(58,11).Value ="PHI"
	wb.Sheets(1).Cells(58,12).Value ="Sh"
	wb.Sheets(1).Cells(59,10).Value ="(m)"
	wb.Sheets(1).Cells(59,11).Value ="(frac)"
	wb.Sheets(1).Cells(59,12).Value ="(frac)"
	
	for x in range(1,15):
		for y in range(55,59):
			wb.Sheets(1).Cells(y,x).Font.Bold = True

	for x in range(1,15):
		for y in range(55,66):
			wb.Sheets(1).Cells(y,x).HorizontalAlignment = 3

	if well.startswith("WS"):
		wb.Sheets(1).Range("A1:N65").BorderAround(1,3,1)
		wb.Sheets(1).Range("E55:N55").BorderAround(1,3,1)
		wb.Sheets(1).Range("E56:I56").BorderAround(1,3,1)
		wb.Sheets(1).Range("J56:N56").BorderAround(1,3,1)
		wb.Sheets(1).Range("J57:N59").BorderAround(1,3,1)
		wb.Sheets(1).Range("A55:D56").BorderAround(1,3,1)
		wb.Sheets(1).Range("A57:D59").BorderAround(1,3,1)
		wb.Sheets(1).Range("E57:I59").BorderAround(1,3,1)
		wb.Sheets(1).Range("E60:I65").BorderAround(1,3,1)
		wb.Sheets(1).Range("A60:A65").BorderAround(1,3,1)
		wb.Sheets(1).Range("B60:D64").BorderAround(1,3,1)
		wb.Sheets(1).Range("K60:K65").BorderAround(1,3,1)
		wb.Sheets(1).Range("M60:M65").BorderAround(1,3,1)
		wb.Sheets(1).Range("B65:N65").BorderAround(1,3,1)
		for x in range(1,15):
			for y in range(55,66):
				wb.Sheets(1).Cells(y,x).HorizontalAlignment = 3

	if well.startswith("SVA"):
		wb.Sheets(1).Range("A1:N64").BorderAround(1,3,1)
		wb.Sheets(1).Range("E55:N55").BorderAround(1,3,1)
		wb.Sheets(1).Range("E56:I56").BorderAround(1,3,1)
		wb.Sheets(1).Range("J56:N56").BorderAround(1,3,1)
		wb.Sheets(1).Range("J57:N59").BorderAround(1,3,1)
		wb.Sheets(1).Range("A55:D56").BorderAround(1,3,1)
		wb.Sheets(1).Range("A57:D59").BorderAround(1,3,1)
		wb.Sheets(1).Range("E57:I59").BorderAround(1,3,1)
		wb.Sheets(1).Range("E60:I64").BorderAround(1,3,1)
		wb.Sheets(1).Range("A60:A64").BorderAround(1,3,1)
		wb.Sheets(1).Range("B60:D64").BorderAround(1,3,1)
		wb.Sheets(1).Range("K60:K64").BorderAround(1,3,1)
		wb.Sheets(1).Range("M60:M64").BorderAround(1,3,1)
		wb.Sheets(1).Range("B64:N64").BorderAround(1,3,1)
		for x in range(1,15):
			for y in range(55,65):
				wb.Sheets(1).Cells(y,x).HorizontalAlignment = 3

	elif well.startswith("US"):
		wb.Sheets(1).Range("A1:N68").BorderAround(1,3,1)
		wb.Sheets(1).Range("E55:N55").BorderAround(1,3,1)
		wb.Sheets(1).Range("E56:I56").BorderAround(1,3,1)
		wb.Sheets(1).Range("J56:N56").BorderAround(1,3,1)
		wb.Sheets(1).Range("J57:N59").BorderAround(1,3,1)
		wb.Sheets(1).Range("A55:D56").BorderAround(1,3,1)
		wb.Sheets(1).Range("A57:D59").BorderAround(1,3,1)
		wb.Sheets(1).Range("E57:I59").BorderAround(1,3,1)
		wb.Sheets(1).Range("E60:I68").BorderAround(1,3,1)
		wb.Sheets(1).Range("A60:A68").BorderAround(1,3,1)
		wb.Sheets(1).Range("B60:D68").BorderAround(1,3,1)
		wb.Sheets(1).Range("K60:K68").BorderAround(1,3,1)
		wb.Sheets(1).Range("M60:M68").BorderAround(1,3,1)
		wb.Sheets(1).Rows(60).EntireRow.Delete()
		wb.Sheets(1).Rows(66).EntireRow.Delete()
		wb.Sheets(1).Range("J66:N66").BorderAround(1,3,1)
		wb.Sheets(1).Range("B66:D66").BorderAround(1,3,1)
		for x in range(1,15):
			for y in range(55,67):
				wb.Sheets(1).Cells(y,x).HorizontalAlignment = 3
	
	wb.Sheets(1).Range("E55:N55").Interior.ColorIndex = 34
	wb.Sheets(1).Range("A57:D59").Interior.ColorIndex = 34
	wb.Sheets(1).Range("E56:I59").Interior.ColorIndex = 35
	wb.Sheets(1).Range("J56:N59").Interior.ColorIndex = 34



def insert_3page(well,path, wb):
	Sheet = wb.Sheets(3)
	Sheet.Activate()	
	ds, dsf, petrel = "CONTACTS","CONTACTS", "ZONATION_PETREL"
	ZONES=db.variableData(well,ds,"ZONES")
	COMMENT=db.variableData(well,ds,"CONTACT")
	CONT_TVDSS=db.variableData(well,ds,"CONT_TVDSS_PP")
	FWL_bf=db.variableData(well,dsf,"FWL_bf")
	ZONES_cont=db.variableData(well,dsf,"ZONES")
	ZONES_petrel = db.variableData(well,petrel,"ZONES")
	tvdss_petrel = db.variableData(well,petrel,"TVDSS")
	X_petrel = db.variableData(well,petrel,"X")
	Y_petrel = db.variableData(well,petrel,"Y")
	md_petrel = db.variableData(well,petrel,"DEPTH")
	
	Sheet.Cells(1,1).Value = "REMARKS PETROPHYSICS"
	Sheet.Cells(1,1).Font.Bold = True
	Sheet.Cells(3,1).Value = "Well"
	Sheet.Cells(3,1).HorizontalAlignment = 3
	Sheet.Cells(6,1).Value = str(well.split("-")[0] + "-" + well.split("-")[1])
	Sheet.Cells(6,1).HorizontalAlignment = 3
	Sheet.Cells(3,2).Value = "ZONE"
	Sheet.Cells(3,2).HorizontalAlignment = 3
	Sheet.Cells(4,2).Value = "NAME"
	Sheet.Cells(4,2).HorizontalAlignment = 3
	Sheet.Cells(3,3).Value = "COMMENT on CONTACTS"
	Sheet.Cells(3,3).HorizontalAlignment = 3
	Sheet.Columns(3).ColumnWidth = 21
	Sheet.Cells(3,4).Value = "Used FWL best fit"
	Sheet.Cells(3,4).HorizontalAlignment = 3
	Sheet.Columns(4).ColumnWidth = 21
	Sheet.Cells(4,4).Value = "(m, TVDSS)"
	Sheet.Cells(4,4).HorizontalAlignment = 3
	for y in range(3,6):
		for x in range(1,6):
			Sheet.Cells(y,x).Font.Bold = True
	
	for x in range(1,6):
		for y in range(6,len(ZONES_cont)+6):
			Sheet.Cells(y,x).BorderAround(1,2,1)
	Sheet.Range("A3:E5").BorderAround(1,3,1)
	Sheet.Range("B3:B5").BorderAround(1,3,1)
	Sheet.Range("D3:D5").BorderAround(1,3,1)
	Sheet.Range("A3:E5").Interior.ColorIndex = 35
	
	x, y=2, 6
	for i in range(0,len(ZONES_cont)):
		if (ZONES_cont[i] == "AS9.0" or ZONES_cont[i]=="AS10.0" or 
			ZONES_cont[i]=="AS11.1" or ZONES_cont[i]=="AS11.2" or 
			ZONES_cont[i]=="AS11.3" or ZONES_cont[i]=="AS11.3_1" or 
			ZONES_cont[i]=="AS11.3_2" or ZONES_cont[i] == "AS11.3.1" or 
			ZONES_cont[i] == "AS11.3.2"):
			
			Sheet.Cells(y,x).Value=ZONES_cont[i]
			if FWL_bf[i]!=-9999:
				Sheet.Cells(y,x+2).Value=FWL_bf[i]
				
			#for j in range(0,len(ZONES)):
				#if ZONES[j]==ZONES_cont[i] and (ZONES_cont[i]!="AS9.0_SH" or "ZONES_cont[i]!=AS11.3_SH"):
					
					#if CONT_TVDSS[j] !=-9999:
						#Sheet.Cells(y,x+1).Value=str(COMMENT[j])+" "+str(round(CONT_TVDSS[j],1))+" m TVDSS"
						#Sheet.Cells(y,x+1).HorizontalAlignment = 3
						
					#else:
						#Sheet.Cells(y,x+1).Value=COMMENT[j]
						#Sheet.Cells(y,x+1).HorizontalAlignment = 3
						
			y=y+1
			
	y2 = y + 2
	x2 = 1
	Sheet.Cells(y2,1).Value = "REMARKS GEOLOGY"
	Sheet.Cells(y2,1).Font.Bold = True
	Sheet.Cells(y2+2,1).Value = "Well"
	Sheet.Cells(y2+2,2).Value = "Surface"
	Sheet.Cells(y2+2,3).Value = "X"
	Sheet.Cells(y2+2,4).Value = "Y"
	Sheet.Cells(y2+2,5).Value = "TVDSS"
	Sheet.Cells(y2+2,6).Value = "MD"
	for i in range(1,7):
		Sheet.Cells(y2+2,i).HorizontalAlignment = 3
		Sheet.Cells(y2+2,i).BorderAround(1,3,1)
		Sheet.Cells(y2+2,i).Interior.ColorIndex = 34
		Sheet.Cells(y2+2,i).Font.Bold = True
	
		
	for i in range(0,len(ZONES_petrel)):
		#Sheet.Cells(y2+3,i).BorderAround(1,2,1)
		if (ZONES_petrel[i] == "AS9.0" or ZONES_petrel[i]=="AS10.0" or 
			ZONES_petrel[i]=="AS11.1" or ZONES_petrel[i]=="AS11.2" or 
			ZONES_petrel[i]=="AS11.3" or ZONES_petrel[i]=="AS11.3_1" or 
			ZONES_petrel[i]=="AS11.3_2" or ZONES_petrel[i] == "AS11.3.1" or 
			ZONES_petrel[i] == "AS11.3.2"):
			
			Sheet.Cells(y2+3,x2).Value = str(well.split("-")[0] + 
											"-" + well.split("-")[1])
			Sheet.Cells(y2+3,x2).BorderAround(1,2,1)
			Sheet.Cells(y2+3,x2+1).Value=ZONES_petrel[i]
			Sheet.Cells(y2+3,x2+1).BorderAround(1,2,1)
			Sheet.Cells(y2+3,x2+1).HorizontalAlignment = 3
			Sheet.Cells(y2+3,x2+2).Value=X_petrel[i]
			Sheet.Cells(y2+3,x2+2).BorderAround(1,2,1)
			Sheet.Cells(y2+3,x2+2).HorizontalAlignment = 3
			Sheet.Cells(y2+3,x2+3).Value=Y_petrel[i]
			Sheet.Cells(y2+3,x2+3).BorderAround(1,2,1)
			Sheet.Cells(y2+3,x2+3).HorizontalAlignment = 3
			Sheet.Cells(y2+3,x2+4).Value=tvdss_petrel[i]
			Sheet.Cells(y2+3,x2+4).BorderAround(1,2,1)
			Sheet.Cells(y2+3,x2+4).HorizontalAlignment = 3
			Sheet.Cells(y2+3,x2+5).Value=md_petrel[i]
			Sheet.Cells(y2+3,x2+5).BorderAround(1,2,1)
			Sheet.Cells(y2+3,x2+5).HorizontalAlignment = 3
			y2 = y2 + 1
	
	Sheet.Cells(y2+5,x2).Value = "REMARKS PP"
	Sheet.Cells(y2+5,x2).Font.Bold = True
	if db.variableExists(well,"COMMON_05","RHOZ_orig"):
		RHOZ_orig=ts.average(db.variableData(well,"COMMON_05","RHOZ_orig"))
		RHOZ=ts.average(db.variableData(well,"COMMON_05","RHOZ"))
		d_RHOZ=RHOZ-RHOZ_orig
		Sheet.Cells(y2+6,1).Value="* Correction "+str(round(d_RHOZ,3))+" g/c3 was applied to the density log \n"
		Sheet.Cells(y2+6,1).WrapText = False
		Sheet.Cells(y2+6,1).Font.ColorIndex = 3
		Sheet.Cells(y2+6,1).Font.Bold = True
	if db.variableExists(well,"COMMON_05","TNPH_orig"):
		TNPH_orig=ts.average(db.variableData(well,"COMMON_05","TNPH_orig"))
		TNPH=ts.average(db.variableData(well,"COMMON_05","TNPH"))
		d_TNPH=TNPH-TNPH_orig
		Sheet.Cells(y2+7,1).Value = "* Correction "+str(round(d_TNPH,3))+" v/v was applied to the neutron log \n"
		Sheet.Cells(y2+7,1).WrapText = False
		Sheet.Cells(y2+7,1).Font.ColorIndex = 3
		Sheet.Cells(y2+7,1).Font.Bold = True


def insert_5page(well,path, wb):
	Sheet = wb.Sheets(5)
	Sheet.Activate()
	
	DS="COMMON_05"
	db.variableCopy(well, "ZONATION",  "ZONES" ,DS, "ZONES")
	DEPT=        Variable(well, DS, "DEPT")
	TVDSS=       Variable(well, DS, "TVDSS")
	ZONES=       Variable(well,DS, "ZONES")
	Porden=      Variable(well,DS, "Porden")
	Ko=        Variable(well, DS, "Ko")
	Kw=        Variable(well, DS, "Kw")
	SWWS=        Variable(well, DS, "SWWS")
	RT=          Variable(well, DS, "RT")
	saturation=  Variable(well, DS, "Fluid_Index")

	commonSize=DEPT.size()

	top_md=0
	bot_md=0
	top_tv=0
	bot_tv=0
	count=0.000001
	por_sum=0
	ko_sum=0
	kw_sum=0
	swws_sum=0
	rt_sum=0

	phi=0
	k=0
	so=0
	res=0

	#print well
	wb.Sheets(5).Cells(1,1).Value=well
	#print "zone", "top_md", "bot_md", "H_md", "top_tv", "bot_tv", "H_tv", "Rt", "phi", "k_oil", "k_water", "So", "saturation"
	wb.Sheets(5).Cells(2,1).Value="zone"
	wb.Sheets(5).Cells(2,2).Value="top_md"
	wb.Sheets(5).Cells(2,3).Value="bot_md"
	wb.Sheets(5).Cells(2,4).Value="H_md"
	wb.Sheets(5).Cells(2,5).Value="top_tv"
	wb.Sheets(5).Cells(2,6).Value="bot_tv"
	wb.Sheets(5).Cells(2,7).Value="H_tv"
	wb.Sheets(5).Cells(2,8).Value="Rt"
	wb.Sheets(5).Cells(2,9).Value="phi"
	wb.Sheets(5).Cells(2,10).Value="k_oil"
	wb.Sheets(5).Cells(2,11).Value="k_water"
	wb.Sheets(5).Cells(2,12).Value="So"
	#	wb.Sheets(5).Cells(2,13).Value="saturation"

	#print "-", "M", "M", "M", "M", "M", "M", "ohmm", "v/v", "mD", "mD", "v/v", "-"
	wb.Sheets(5).Cells(3,1).Value="-"
	wb.Sheets(5).Cells(3,2).Value="M"
	wb.Sheets(5).Cells(3,3).Value="M"
	wb.Sheets(5).Cells(3,4).Value="M"
	wb.Sheets(5).Cells(3,5).Value="M"
	wb.Sheets(5).Cells(3,6).Value="M"
	wb.Sheets(5).Cells(3,7).Value="M"
	wb.Sheets(5).Cells(3,8).Value="ohmm"
	wb.Sheets(5).Cells(3,9).Value="v/v"
	wb.Sheets(5).Cells(3,10).Value="mD"
	wb.Sheets(5).Cells(3,11).Value="mD"
	wb.Sheets(5).Cells(3,12).Value="v/v"
	wb.Sheets(5).Cells(3,13).Value="-"
	y=4
	for i in range (0, commonSize):
		dept = DEPT.value(i)
		tvdss=TVDSS.value(i)
		sat=saturation.value(i)
		porden=Porden.value(i)
		ko=Ko.value(i)
		kw=Kw.value(i)
		swws=SWWS.value(i)
		zones=ZONES.value(i)
		rt=RT.value(i)

		if sat>=1 and sat<>saturation.value(i-1):
			top_md=dept
			top_tv=tvdss

		if sat>=1 and sat==saturation.value(i+1) and sat==saturation.value(i-1):
			count=count+1
			por_sum=por_sum+porden
			ko_sum=ko_sum+ko
			kw_sum=kw_sum+kw
			swws_sum=swws_sum+swws
			rt_sum=rt_sum+rt

		if sat>=1 and sat<>saturation.value(i+1):
			if sat==1:
				s_type="oil"
			elif sat==2:
				s_type="o+w"
			elif sat==3:
				s_type="water"
			elif sat==4:
				s_type="unknown"
			elif sat==5:
				s_type="swept"


			bot_md=DEPT.value(i+1)
			bot_tv=TVDSS.value(i+1)


			phi=por_sum/count
			so=1-(swws_sum/count)
			k_o=ko_sum/count
			k_w=kw_sum/count
			res=rt_sum/count
			if (bot_md-top_md) <0.4:
				phi="-"
				k_o="-"
				k_w="-"
			if (bot_md-top_md) <0.4:
				so="-"
				res="-" 

			if sat==1 and so<0.25:
				so="-"
				res="-" 

			if sat==2 and so<0.15:
				so="-"
				#				res="-" 

			if sat==4:	
				so="-"
				res="-" 

			if (zones=="achimov" or zones=="AS10.0" or zones=="AS11.1" or zones=="AS11.2" or zones=="AS11.3_1" or zones=="AS11.3_2" or zones=="AS11.3" or zones=="AS9.0" or zones=="AS9.0_SH"  or zones == "AS11.3.1" or zones == "AS11.3.2") and (bot_md-top_md)>0.2 and (bot_tv-top_tv)>=0.05 :
				#print zones, top_md, bot_md, bot_md-top_md, top_tv, bot_tv, bot_tv-top_tv, res, phi, k_o, k_w, so, s_type
				wb.Sheets(5).Cells(y,1).Value=zones
				wb.Sheets(5).Cells(y,2).Value=top_md
				wb.Sheets(5).Cells(y,3).Value= bot_md
				wb.Sheets(5).Cells(y,4).Value=bot_md-top_md
				wb.Sheets(5).Cells(y,5).Value=top_tv
				wb.Sheets(5).Cells(y,6).Value=bot_tv
				wb.Sheets(5).Cells(y,7).Value=bot_tv-top_tv
				wb.Sheets(5).Cells(y,8).Value=res
				wb.Sheets(5).Cells(y,9).Value=phi
				wb.Sheets(5).Cells(y,10).Value=k_o
				wb.Sheets(5).Cells(y,11).Value=k_w
				wb.Sheets(5).Cells(y,12).Value=so		
				wb.Sheets(5).Cells(y,13).Value=s_type		
				y+=1

			count=0.000001
			por_sum=0
			ko_sum=0
			kw_sum=0
			swws_sum=0
			rt_sum=0

			phi=0
			so=0 		
			k_w=0
			k_o=0
			res=0
			s_type="-"			
	for x in range(1,15):
		for y in range(1,4):
			wb.Sheets(5).Cells(y,x).Font.Bold = True




def insert_QC_corr(well,path,wb):
	corr_path = path + "\\" + "cor1" + ".png"
	if os.path.exists(corr_path) == True:
		Sheet = wb.Sheets(8)
		Sheet.Activate()
		Sheet.Shapes.AddPicture(corr_path, False, True,0,0,700,450)
	else:
		print "Нет корреляции в папке"
		
	rhoz_path = path + "\\" + "RHOZ" + ".png"
	if os.path.exists(rhoz_path) == True:
		Sheet = wb.Sheets(6)
		Sheet.Shapes.AddPicture(rhoz_path, False, True,0,0,300,300)
	else:
		print "Нет RHOZ в папке"

	neu_path = path + "\\" + "TNPH" + ".png"
	if os.path.exists(neu_path) == True:
		Sheet = wb.Sheets(6)
		Sheet.Shapes.AddPicture(neu_path, False, True,350,0,300,300)
	else:
		print "Нет TNPH в папке"



for well in db.selectedWellList():
	report_folder_path = folder_path(well)
	print "Папка скважины создана"
	wb = create_xls(well)
	print "Файл отчета создан"
	insert_1plot(well,report_folder_path,wb)
	print "Создана 1я страница"
	insert_1and2page(well,report_folder_path,wb)
	print "Заполнены страницы 1 и 2"
	insert_3page(well,report_folder_path,wb)
	print "Заполнена 3я страница"
	insert_5page(well,report_folder_path,wb)
	print "Заполнена 5я страница"
	insert_QC_corr(well,report_folder_path,wb)
	print "Страница QC заполнена"
	webbrowser.open(report_folder_path)
	print "Генерация отчета завершена"

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-02-24"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""