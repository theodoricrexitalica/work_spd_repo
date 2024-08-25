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
import TechlogStat as ts
import TechlogDialogAdvanced as tda

def cmt_calc(data_cutoff,well_dict):
	if db.datasetExists(well,"CBL"):
		date = db.datasetInformation(well,"COMMON_05","creation").split("T")[0]
		if date > data_cutoff and not "kmod" in well and not "LWD" in well:
			cmt = db.variableData(well,"CBL","CCC")
			md = map(lambda x: round(x,0), db.variableData(well,"CBL",db.referenceName(well,"CBL")))
			md1 = round(db.variableData(well,"ZONATION",db.referenceName(well,"ZONATION"))[0],0)
			md2 = round(db.variableData(well,"ZONATION",db.referenceName(well,"ZONATION"))[-1],0)
			md2_cbl = round(db.variableData(well,"CBL",db.referenceName(well,"CBL"))[-1],0)
			if md2_cbl < md2:
				md2 = md2_cbl
			try:
				ind1 = md.index(md1)
				ind2 = md.index(md2)
				list_prod_cmt = []
				list_cmt = cmt[ind1:ind2]
				avg_cmt = round(ts.average(list_cmt),2)
				stdev_cmt = round(ts.stdev(list_cmt),2)
				report = ("-".join(well.split("-")[:3]) + ": " + str(avg_cmt) + ": " \
						 + str(stdev_cmt) + ": " + str(md1))
				well_dict[date] = report
			except:
				print well, " - не посчитано"
				pass
		else:
			pass
	else:
		pass
	return well_dict


dialog = tda.dialogAdvanced("Cmt wells")
func_list = ["For all wells","For selected wells"]
dialog.addButtonsGroup("cmt_wells","Algorithm",func_list,1)
dialog.addTextInput("cmt_data","Data cut-off","yyyy-mm-dd",0)
dialog.execDialog()
response = dialog.getButtonsGroup("cmt_wells")
data_cutoff = dialog.getTextInput("cmt_data")
if data_cutoff == "yyyy-mm-dd":
	data_cutoff = "1900-01-01"
if response[0] == "For all wells":
	print "date", " : ", "well", ": ", "avg cmt", ": ", "stdev cmt", ": ", "md1"
	well_dict = {}
	for well in db.wellList():
		well_dict_final = cmt_calc(data_cutoff,well_dict)
	for key in sorted(well_dict_final.iterkeys()):
		print "%s : %s" % (key,well_dict_final[key])
else:
	print "date", " : ", "well", ": ", "avg cmt", ": ", "stdev cmt", ": ", "md1"
	well_dict = {}
	for well in db.selectedWellList():
		well_dict_final = cmt_calc(data_cutoff,well_dict)
	for key in sorted(well_dict_final.iterkeys()):
		print "%s : %s" % (key,well_dict_final[key])

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2017-01-20"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""