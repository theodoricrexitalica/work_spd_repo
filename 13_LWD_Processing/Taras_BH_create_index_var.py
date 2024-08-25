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
file_path = os.path.join(db.dirProject(), "Data", "report.txt")
file_txt = file(file_path, "wb")
for well in db.selectedWellList():
	index_flag = db.variableData(well,"LAS","Index_flag")
	litho_flag = db.variableData(well,"LAS","Litho_flag")
	md = db.variableData(well,"LAS",db.referenceName(well,"LAS"))
	md_zone = db.variableData(well,"ZONATION",db.referenceName(well,"ZONATION"))
	t1 = float(db.wellPropertyValue(well,"T1, m"))
	t2 = float(db.wellPropertyValue(well, "T2, m"))
	res_th = float(db.wellPropertyValue(well, "Oil+water flag, Ohm.m"))
	res_th_calc = float(db.wellPropertyValue(well, "High dens flag, Ohm.m"))
	gr_th = float(db.wellPropertyValue(well, "Non res flag, gAPI"))
	sample = round(md[1]-md[0],2)
	tool_len = 15
	oil_counter = 0
	oil_water_counter = 0
	hi_calc_counter = 0
	shale_counter = 0
	oil_counter_t2 = 0
	oil_water_counter_t2 = 0
	for i in range(len(md)):
		if md[i] >= md_zone[0] and index_flag[i] == 1:
			oil_counter +=1
		if md[i] >= md_zone[0] and index_flag[i] == 2:
			oil_water_counter +=1
		if md[i] >= md_zone[0] and litho_flag[i] == 3:
			hi_calc_counter +=1
		if md[i] >= md_zone[0] and litho_flag[i] == 2:
			shale_counter +=1
	for i in range(len(md)):
		if md[i] >= t2 and index_flag[i] == 1:
			oil_counter_t2 +=1
		if md[i] >= t2 and index_flag[i] == 2:
			oil_water_counter_t2 +=1
	net_pay = round(oil_counter*sample,0)
	oil_water = round(oil_water_counter*sample,0)
	total_oil = net_pay + oil_water
	
	shale_counter = round(shale_counter*sample,0)
	hi_calc = round(hi_calc_counter*sample,0)
	net_pay_t2 = round(oil_counter_t2*sample,0)
	oil_water_t2 = round(oil_water_counter_t2*sample,0)
	total_oil_t2 = net_pay_t2 + oil_water_t2
	cp_td = round(md_zone[-1]-md_zone[0],0) - tool_len
	t1_td = round(md_zone[-1]-t1,0) - tool_len
	t2_td = round(md_zone[-1]-t2,0) - tool_len
	t3    = round((float(db.wellPropertyValue(well,"T3, m")) - md_zone[-1]),0)
	print "Статистика по скважине:"
	print "Net pay:", net_pay, "m"
	print "Oil+water:", oil_water,  "m"
	print "Total net pay:", total_oil,  "m"
	print "Shale:", shale_counter, "m"
	#print "Shale:", cp_td - total_oil - hi_calc, "m"
	print "High calc:", hi_calc, "m"
	print "Non reservoir", hi_calc +shale_counter , "m"
	print "T1-TD:", (t1_td + tool_len), "m"
	print "T2-TD:", (t2_td + tool_len), "m"
	#print "CasingPoint-TD:", cp_td, "m"
	print "QC T1:", round((total_oil / t1_td)*100,0), "%"
	print "QC T2:", round((total_oil_t2 / t2_td)*100,0), "%"
	print "QC CP-TD:", round((total_oil/cp_td)*100,0), "%"
	print "Осталось бурить:", t3, "m"
	file_txt.write("Коллеги," + "\r\n")
	file_txt.write("Ниже предсталена информация по " + well + "\r\n"*3)
	file_txt.write("Статистика по скважине:" + "\r\n")
	file_txt.write("Net pay: " + "\t\t" + str(int(net_pay)) + "m" + "\r\n")
	file_txt.write("Oil+water: " + "\t\t" + str(int(oil_water)) + "m" + "\r\n")
	file_txt.write("Total net pay: " + "\t\t" + str(int(total_oil)) + "m" + "\r\n")
	file_txt.write("Shale: " + "\t\t\t" + str(shale_counter) + "m" + "\r\n")
	file_txt.write("High calc: " + "\t\t" + str(hi_calc) + "m" + "\r\n")
	file_txt.write("Non reservoir: " + "\t\t" + str(int(hi_calc + shale_counter)) + "m" + "\r\n")
	file_txt.write("T1-TD: " + "\t\t\t" + str(int(t1_td) + tool_len) +  "m" + "\r\n")
	file_txt.write("T2-TD: " + "\t\t\t" + str(int(t2_td) + tool_len) + "m" + "\r\n")
	#file_txt.write("CPoint-TD: " + "\t" + str(int(cp_td)) + "m" + "\r\n")
	file_txt.write("QC T1: " + "\t\t\t" + str(int(round((total_oil / t1_td)*100,0))) + "%" + "\r\n")
	file_txt.write("QC T2: " + "\t\t\t" + str(int(round((total_oil_t2 / t2_td)*100,0))) + "%" + "\r\n")
	#file_txt.write("QC CP-TD:" + "\t\t" + str(int(round((total_oil/cp_td)*100,0))) + "%" + "\r\n")
	file_txt.write("Осталось бурить:" + "\t" + str(t3) + "m" + "\r\n"*2)
	file_txt.write("*Интервалы водонефтяного насыщения выделены ориентировочно" + \
					 " по данным каротажа сопротивлений ниже " + str(res_th) + " ом*м" + "\r\n")
	file_txt.write("*Карбонатизированные интервалы выделены по" + \
					 " данным каротажа сопротивлений выше " + str(res_th_calc) + " ом*м" + "\r\n")
	file_txt.write("*Заглинизированные интервалы выделены" + \
					 " по показаниям ГК выше " + str(gr_th) + "апи" + "\r\n")
	file_txt.write("*Насыщение карбонатизированых интервалов " + \
					 " уточнено по газопоказаниям " + "\r\n")
	file_txt.write("\nТ1 – глубина башмака колонны 177.8мм" + "\r")
	file_txt.write("\nТ2 – глубина начала горизонтального участка" + "\r")
file_txt.close()
os.startfile(file_path)

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-10-19"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""