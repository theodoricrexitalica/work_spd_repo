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
	path = r"C:\Apps\UPDATE_PPEVAL" + "\\" + well
	if os.path.exists(path) == True:
		pass
	else:
		os.mkdir(path)
	return(path)

def print_pic(well,path):
	well_pic = tp.logViewGetIdByName(well)
	corr_pic = tp.logViewGetIdByName("cor1")
	tp.printToFile(well_pic,'Custom','.png',path + "\\" + well,18.53,24.31,0,-1,0,-1,-1,False,200)
	tp.printToFile(corr_pic,'Custom','.png',path + "\\" + "cor1",30,23,0,-1,0,-1,-1,False,200)
	
def print_hist(well,path):
	if well.startswith("SVA"):
		dens_pic = tp.histogramGetIdByName("SVA_Bulk Density")
		neut_pic = tp.histogramGetIdByName("SVA_Neutron Porosity")
		tp.printToFile(dens_pic,'Custom','.png',path + "\\" + "RHOZ",16,16,0,-1,0,-1,-1,False,150)
		tp.printToFile(neut_pic,'Custom','.png',path + "\\" + "TNPH",16,16,0,-1,0,-1,-1,False,150)
	if well.startswith("WS"):
		dens_pic = tp.histogramGetIdByName("WS_Bulk Density")
		neut_pic = tp.histogramGetIdByName("WS_Neutron Porosity")
		tp.printToFile(dens_pic,'Custom','.png',path + "\\" + "RHOZ",16,16,0,-1,0,-1,-1,False,150)
		tp.printToFile(neut_pic,'Custom','.png',path + "\\" + "TNPH",16,16,0,-1,0,-1,-1,False,150)


for well in db.selectedWellList():
	path = folder_path(well)
	print "Пусть к папке найден"
	print_pic(well,path)
	print "Диаграммы распечатаны"
	print_hist(well,path)
	print "Гистограммы распечатаны"
	webbrowser.open(path)

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-02-29"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""