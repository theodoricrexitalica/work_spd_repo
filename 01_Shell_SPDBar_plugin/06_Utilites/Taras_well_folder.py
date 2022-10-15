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
import webbrowser
import os
path_ws="\\\europe.shell.com\europe\E & P\SPD Salym Central Processing Facility\\" + \
		"Dept_07\SPD Drilling & Completion Well File\West Salym"
path_sva="\\\europe.shell.com\europe\E & P\SPD Salym Central Processing Facility\\" + \
		"Dept_07\SPD Drilling & Completion Well File\Vadelyp"
path_us="\\\europe.shell.com\europe\E & P\SPD Salym Central Processing Facility\\" + \
		"Dept_07\SPD Drilling & Completion Well File\Upper Salym"

for well in db.selectedWellList():
	if well.startswith("WS"):
		pad = well.split("-")[2][1:4]
		well_folder = well.split("-")[:4]
		well_folder = "-".join(well_folder)
		if "ST" in well_folder:
			well_folder = well_folder.split("ST")[0] + "-ST"
		path_well = path_ws + "\Pad " + pad + "\\" + well_folder
		#path_well = path_ws + "\Pad " + pad + "\\" + well_folder + "\\1. DRILLING"
		if os.path.exists(path_well) == False:
			path_well = path_ws + "\Pad " + pad
		if pad == "49" or pad == "66":
			path_well = path_sva + "\Pad " + pad + "\\" + well_folder
			if os.path.exists(path_well) == False:
				path_well = path_sva + "\Pad " + pad
		else:
			pass
		webbrowser.open(path_well)
	elif well.startswith("SVA"):
		pad = well.split("-")[2][1:4]
		well_folder = well.split("-")[:4]
		well_folder = "-".join(well_folder)
		path_well = path_sva + "\Pad " + pad + "\\" + well_folder
		#path_well = path_sva + "\Pad " + pad + "\\" + well_folder + "\\1. DRILLING"
		if os.path.exists(path_well) == False:
			path_well = path_sva + "\Pad " + pad
		webbrowser.open(path_well)
	elif well.startswith("US"):
		pad = well.split("-")[2][1:4]
		well_folder = well.split("-")[:4]
		well_folder = "-".join(well_folder)
		path_well = path_us + "\Pad " + pad + "\\" + well_folder
		#path_well = path_us + "\Pad " + pad + "\\" + well_folder + "\\1. DRILLING"
		if os.path.exists(path_well) == False:
			path_well = path_us + "\Pad " + pad
		webbrowser.open(path_well)

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-02-21"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""