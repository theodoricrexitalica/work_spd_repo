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
def active_zone_counter(well,ds,data):
	zone_list_counter = []
	ds_zone = "ZONATION"
	zones = db.variableData(well,ds_zone,"ZONES")
	for i in zones:
			if i == "TD":
				zones.remove(i)
	for i in range(len(zones)):
		ind = db.datasetZoneIndice(well, ds, ds_zone, zones[i])
		if ind == None:
			continue
		zone_list_counter.append(zones[i])
	return zone_list_counter


def report_split_water(well,ds,data):
	list = []
	ds_zone = "ZONATION"
	zones = db.variableData(well,ds_zone,"ZONES")
	for i in zones:
			if i == "TD":
				zones.remove(i)
	for i in range(len(zones)):
		ind = db.datasetZoneIndice(well, ds, ds_zone, zones[i])
		if ind == None:
			continue
		top_data = 0
		bottom_data = 0
		for j in xrange(ind[0],ind[1]):
			if data[j] > 0:
				top_data = round(data[j],1)
				break
		if (top_data > 0):
			for j in xrange(ind[1],ind[0],-1):
				if data[j] > 0:
					bottom_data = round(data[j],1)
					break
		result = top_data - bottom_data
		list.append(float(result))
	return list


def report_perf(well,ds):
	ds_zone = "ZONATION"
	zones = db.variableData(well,ds_zone,"ZONES")
	for i in zones:
			if i == "TD":
				zones.remove(i)
	perf = db.variableData(well,ds,"PERF_FINAL")
	md = db.variableData(well, ds, db.referenceName(well,ds))
	list = []
	for i in range(len(zones)):
		top_perf= []
		bot_perf = []
		ind = db.datasetZoneIndice(well, ds, ds_zone, zones[i])
		if ind == None:
			continue
		#print zones[i], ind[0],ind[1]
		for j in xrange(ind[0],ind[1]):
			#Сделано на случай, если верх перфорации совпадает с кровлей пласта
			if perf[j] == 2 and perf[j-1] != 2 or perf[j] == 2 and j == ind[0]:
				top_perf.append(round(md[j],2))
			#if perf[j] == 2 and j == ind[0]:
				#top_perf.append(round(md[j],2))
			if perf[j] == 2 and j == ind[1]-1:
				bot_perf.append(round(md[j],2))
			if perf[j] != 2 and perf[j-1] == 2:
				bot_perf.append(round(md[j],2))
		#Добавляется 0.01 чтобы функция правильно округляла
		func = lambda x: round(x+0.01,1)
		top_perf = map(func, top_perf)
		bot_perf = map(func, bot_perf)
		list_perf = []
		for j in range(len(top_perf)):
			list_perf.append(str(top_perf[j]) + "-" + str(bot_perf[j]))
		list.append(list_perf)
	return list


def report_cooling_zone(well,ds):
	flow = db.variableData(well,ds,"Flowing")
	md = db.variableData(well,ds,db.referenceName(well,ds))
	cc = 0
	top_flow = 0
	bot_flow = 0
	for i in range(len(md)):
		if (flow[i] == 5 or flow[i] == 2) and (flow[i - 1] == MissingValue or flow[i - 1] == 0) and cc < 1:
			top_flow = md[i]
			cc += 1
		if (flow[i] == MissingValue or flow[i] == 0 or flow[-1]==5) and flow[i - 1] > 0:
			bot_flow = md[i-1]
	#print bot_flow, top_flow
	result = round(bot_flow - top_flow,0)
	return result


file_path = os.path.join(db.dirProject(), "Data", "report.txt")
file_txt = file(file_path, "wb")
for well in db.wellList():
	for ds in db.selectedDatasetList(well):
		zones = db.variableData(well,"ZONATION","ZONES")
		for i in zones:
			if i == "TD":
				zones.remove(i)
		water = db.variableData(well, ds, "%_water")
		spinner = db.variableData(well, ds, "QTZTP")
		water_res = report_split_water(well, ds, water)
		spinner_res = report_split_water(well, ds, spinner)
		perf = report_perf(well,ds)
		total_w = 0
		total_sp = 0
		print "Zones","Spinner", "%_water"
		file_txt.write(well + "\r\n")
		file_txt.write(ds + "\r\n")
		file_txt.write("\r\n")
		file_txt.write("Zones" + " " + "Spinner" + " " + "%_water" + " " + "\r\n")
		acvite_zones = len(active_zone_counter(well, ds, water))
		for i in range(acvite_zones):
			total_w += water_res[i]
			total_sp += spinner_res[i]
			print zones[i], round(spinner_res[i],0), round(water_res[i],0)
			file_txt.write(str(zones[i]) + " " + str( round(spinner_res[i],0)) + " " + str(round(water_res[i],0)) + "\r\n")
		file_txt.write("Total:" + " " + str(total_sp) + " " + str(total_w) + "\r\n")
		print "Total:",total_sp, total_w 
		print ""
		print "Perforations"
		file_txt.write("\r\n")
		file_txt.write("Perforations" + "\r\n") 
		for i in range(len(perf)):
			for j in perf[i]:
				print zones[i], j
				file_txt.write(zones[i] + " " + str(j) + "\r\n")
		print ""
		print "Cooling zone height"
		print report_cooling_zone(well,ds)
		file_txt.write("\r\n")
		file_txt.write("Cooling zone height" + "\r\n")
		file_txt.write(str(report_cooling_zone(well,ds)) + "\r\n")
file_txt.write("\r\n")
file_txt.write("Taras Dolgushin" + "\r\n" + "\r\n")
file_txt.write("There is the minor crossflow ~% from  m to m MD (from AS to AS)." + "\r\n")
file_txt.write("The injectivity rate is less then the spinner's limit of measurment." + "\r\n")
file_txt.write("Perforated interval - m MD AS doesn't take water." + "\r\n")
file_txt.write("Spinner data unavalaible due to contamination of sensor by mechanical inpurities." + "\r\n")
file_txt.write("Background Tlog shows  values then Injection Tlog." + "\r\n")
file_txt.write("Low discrepancy between consecutive T-logs." + "\r\n" )
file_txt.write("PLT tool was stopped into perforated interval." + "\r\n" + "\r\n")
file_txt.write("перевод в ППД" + "\r\n")
file_txt.write("изоляции" + "\r\n")
file_txt.write("корректировка" + "\r\n")
file_txt.write("пересчет после ПГИ по спинеру" + "\r\n")
file_txt.write("переток по результатам ПЛТ" + "\r\n")
file_txt.write("пересчет после ПГИ по температуре" + "\r\n")
file_txt.close()
os.startfile(file_path)

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-12-08"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""