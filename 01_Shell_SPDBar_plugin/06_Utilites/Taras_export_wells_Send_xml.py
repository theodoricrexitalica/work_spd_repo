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
path = r"C:\Apps\Routine\Send_xml"
well_list = []
for well in db.selectedWellList():
	well_list.append(well)
for i in range(len(well_list)):
	wells = well_list[i:i+1]
	print "Скважина",wells[0],"экспортирована"
	db.exportFile(path,wells,"XML")
webbrowser.open(path)
	

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-03-08"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""