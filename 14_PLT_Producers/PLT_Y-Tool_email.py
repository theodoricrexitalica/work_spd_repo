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
import webbrowser
import win32com.client
from os import *
import pythoncom
pythoncom.CoInitialize()
from win32com import client

ds_zone = "ZONATION"
Path_plt = ""

for well in db.wellList():
	for ds in db.selectedDatasetList(well):
		email = win32com.client.Dispatch("Outlook.Application")
		Msg = email.CreateItem(0)
		Msg.To = "LQC-PLT"
		#Msg.CC = "more email addresses here"
		#Msg.BCC = "more email addresses here"
		Msg.Subject = "LQC_PLT_Y-tool_" + "-".join(well.split("-")[:4])
		Msg.Body =	"\n\rRegards," + \
					"\nTaras Dolgushin" + \
				 	"\nField Petrophysicist" + \
				 	"\nSub Surface Field Team" + \
					"\nSalym Petroleum Development N.V." + \
					"\nPhone:  +7 495 411 7074 ext.3486" + \
					"\nMobile: +7 932 440 29 29" + \
					"\nE-mail work: SPD-SALYM-SSFT-GE-C@salympetroleum.ru" + \
					"\nE-mail personal: Taras.Dolgushin@salympetroleum.ru"
		#attachment = "C:\\Apps\\OIS\\OIS_data.xlsx"
		#Msg.Attachments.Add(attachment)
		Msg.Display()
		#Msg.Send()
		
		Msg = email.CreateItem(0)
		Msg.To = "PLT_Y_Plot_Inform"
		#Msg.CC = "more email addresses here"
		#Msg.BCC = "more email addresses here"
		Msg.Subject = "-".join(well.split("-")[:3]) + "_" + ds
		Msg.Body =	"Dear All," +\
						"\nY-tool for well " + "-".join(well.split("-")[:4]) +\
						" is available in <\\\europe.shell.com\europe\E & P\SPD Moscow\Dept_05\OFM\Load_files\Plt producer\\>" +\
						"\n\rRegards," + \
						"\nTaras Dolgushin" + \
					 	"\nField Petrophysicist" + \
					 	"\nSub Surface Field Team" + \
						"\nSalym Petroleum Development N.V." + \
						"\nPhone:  +7 495 411 7074 ext.3486" + \
						"\nMobile: +7 932 440 29 29" + \
						"\nE-mail work: SPD-SALYM-SSFT-GE-C@salympetroleum.ru" + \
						"\nE-mail personal: Taras.Dolgushin@salympetroleum.ru"
		#attachment = "C:\\Apps\\OIS\\OIS_data.xlsx"
		#Msg.Attachments.Add(attachment)
		Msg.Display()
		#Msg.Send()
webbrowser.open(r"\\europe.shell.com\europe\E & P\SPD Moscow\Dept_05\OFM\Load_files\Plt producer")

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2015-12-20"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""