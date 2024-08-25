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
for well in db.selectedWellList():
	ref_main = db.referenceName(well,"MAIN")
	ref_zone = db.referenceName(well,"ZONATION")
	md_bot = db.variableData(well,"MAIN",ref_main)[-1]
	md_top = db.variableData(well,"MAIN",ref_main)[0]
	#print md_top, md_bot
	zone_md_bot = db.variableData(well,"ZONATION",ref_zone)[-1]
	zone_md_top = db.variableData(well,"ZONATION",ref_zone)[0]
	#print zone_md_top, zone_md_bot
	if md_top < zone_md_top:
		print "Top if MAIN is OK"
	else: print "Problem Top if MAIN"
	if md_bot > zone_md_bot:
		print "Bottom of MAIN is OK"
	else: print "Problem Bottom if MAIN"

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-03-17"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""