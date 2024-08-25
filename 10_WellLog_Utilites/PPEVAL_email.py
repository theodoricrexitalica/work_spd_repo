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

for well in db.selectedWellList():
	as_top = round(db.variableData(well,"ZONATION","DEPTH")[0],2)
	zone = db.variableData(well,"ZONATION","ZONES")[0]
	print zone,"=",as_top
	
	### Creating emails for distribution list
	email = win32com.client.Dispatch("Outlook.Application")
	
	### Creating Interim PP picture
	Msg = email.CreateItem(0)
	Msg.To = "Interim PP picture"
	Msg.Subject = "PPEval_interrim_" + well
	Msg.Body = "Dear  All, \nPlease see attached Interim Picture of " + \
	"PP evaluation for well " + well +\
	"\nPreliminary net pay m, expected m \nPreliminary KH" +\
	"\n\n* Predicted properties were taken from well proposals" +\
	"\n* Predicted properties were taken from PP Proposed for current well" +\
	"\n\rPlease find Field Petrel curves and survey for well  follow the link:" +\
	"\n<\\\europe.shell.com\europe\E & P\SPD Salym Central Processing Facility\Dept_02\TM24-SSFT\DATA Exchange Area\Log data store area>" +\
	"\n\rRegards," + \
	"\nTaras Dolgushin" +\
 	"\nField Petrophysicist" + \
 	"\nSub Surface Field Team" + \
	"\nSalym Petroleum Development N.V." + \
	"\nPhone:  +7 495 411 7074 ext.3486" + \
	"\nMobile: +7 932 440 29 29" + \
	"\nE-mail work: SPD-SALYM-SSFT-GE-C@salympetroleum.ru" + \
	"\nE-mail personal: Taras.Dolgushin@salympetroleum.ru"
	Msg.Display()

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2016-01-03"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""