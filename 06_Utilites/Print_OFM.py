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
def PPpictures_print(well, Path='Z:\\SPD Moscow\Dept_05\OFM\PPevals\\'):
	id=TP.logViewGetIdByName(well)
	ok=TP.printToFile(id,"A4",".jpg",Path+well.split("-")[0]+"-"+well.split("-")[1],
					  21,29.7,0,-1,0,-1,-1,False,300)
wellList=db.selectedWellList()
for well in wellList:
	pictures=PPpictures_print(well)
	print "Диаграмма напечатана"

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2013-04-22"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""