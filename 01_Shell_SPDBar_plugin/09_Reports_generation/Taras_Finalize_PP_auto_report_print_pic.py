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
import TechlogPlot as tp
import os
import webbrowser



def folder_path(well):
	path = r"C:\Apps\Routine\PP_eval" + "\\" + well
	if os.path.exists(path) == True:
		pass
	else:
		print "Well folder is done"
		os.mkdir(path)
	return(path)

def print_pic(well,path):
	well_pic = tp.logViewGetIdByName(well)
	corr_pic = tp.logViewGetIdByName("cor1")
	tp.printToFile(well_pic,'Custom','.png',path + "\\" + well,18.53,24.31,0,-1,0,-1,-1,False,200)
	tp.printToFile(corr_pic,'Custom','.pdf',path + "\\" + well + "_Correlation",30,23,0,-1,0,-1,-1,False,200)
	
	
for well in db.selectedWellList():
	path = folder_path(well)
	print_pic(well,path)
	webbrowser.open(path)

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-03-03"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""