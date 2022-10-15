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
ds = "COMMON_05"
for well in db.selectedWellList():
	for var in db.variableList(well,ds):
		if var == "TNPH":
			list = []
			list.append(well + "." + ds + "." + "TNPH")
			db.variableDuplicate(well,ds,"TNPH","TNPH_orig")
			list.append(well + "." + ds + "." + "TNPH_orig")
			db.dataEditorOpen(list)
			print "TNPH dublicated"
		if var == "RHOZ":
			list = []
			list.append(well + "." + ds + "." + "RHOZ")
			db.variableDuplicate(well,ds,"RHOZ","RHOZ_orig")
			list.append(well + "." + ds + "." + "RHOZ_orig")
			db.dataEditorOpen(list)
			print "RHOZ dublicated"
		if var == "RHOZ_apd":
			list = []
			list.append(well + "." + ds + "." + "RHOZ_apd")
			db.variableDuplicate(well,ds,"RHOZ_apd","RHOZ_apd_orig")
			list.append(well + "." + ds + "." + "RHOZ_apd_orig")
			db.dataEditorOpen(list)
			print "RHOZ_apd dublicated"

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-04-24"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""