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
import win32com.client
from os import *
import pythoncom
pythoncom.CoInitialize()
import TechlogPlot as TP
import webbrowser


Path='C:\Apps\Routine\PP_eval\\'

def PPpictures_print(well, Path):
	pictures=[]
	id1=TP.logViewGetIdByName(well)
	ok1=TP.printToFile(id1,'Custom','.png',Path+well,18.53,24.31,0,-1,0,-1,-1,False,100)
	if ok1: 
		print Path+well, " successfully exported"
		pictures.append(well)
	else: print "failed to export ", Path,well

	id2=TP.logViewGetIdByName('cor1')
	ok2=TP.printToFile(id2,'Custom','.pdf',Path+well+"_Correlation",30,23,0,-1,0,-1,-1,False,100)
	if ok2: 
		print Path,well+"_Correlation", " successfully exported" 
		pictures.append("cor1")
	else: print "failed to export ", Path,"cor1"

for well in db.selectedWellList():
	pictures=PPpictures_print(well,Path)
	webbrowser.open(Path)

__author__ = """Sergey POLUSHKIN (Sergey.Polushkin)"""
__date__ = """2012-08-13"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""