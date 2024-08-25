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
import TechlogPlot as TP
import webbrowser
path='Z:\\SPD Moscow\Dept_05\OFM\PPevals\\'
def PPpictures_print(well, path):
	id=TP.logViewGetIdByName(well)
	ok=TP.printToFile(id,"A4",".jpg",path + well.split("-")[0] + \
					  "-"+well.split("-")[1] + "_ACH", \
					  21,29.7,0,-1,0,-1,-1,False,300)
					  
					  
wellList=db.selectedWellList()
for well in wellList:
	pictures=PPpictures_print(well,path)
	webbrowser.open(path)
	print "Диаграмма по Ачимову напечатана"

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2013-04-22"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""