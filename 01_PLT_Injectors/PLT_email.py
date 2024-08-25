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
import TechlogDialogAdvanced as tda

ds_zone = "ZONATION"
Path_plt = ""

rem_list = ["crossflow", "out-of-run interval", "ok"]
dialog = tda.dialogAdvanced("Remarks")
dialog.addButtonsGroup("Remarks","Remarks",rem_list,1)
dialog.execDialog()
oper_issue = dialog.getButtonsGroup("Remarks")
if oper_issue[0] == "ok":
	remark = ""
else:
	remark = " + " + oper_issue[0]

for well in db.selectedWellList():
	email = win32com.client.Dispatch("Outlook.Application")
	Msg = email.CreateItem(0)
	Msg.To = "LQC-PLT"
	#Msg.CC = "more email addresses here"
	#Msg.BCC = "more email addresses here"
	Msg.Subject = "LQC_PLT_" + "-".join(well.split("-")[:4])
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
	Msg.To = "PLT_Plot_Inform"
	#Msg.CC = "more email addresses here"
	#Msg.BCC = "more email addresses here"
	Msg.Subject = "PLT_Plot_" + "-".join(well.split("-")[:2]) + remark
	Msg.Body =	"Dear All," +\
					"\nWell " + "-".join(well.split("-")[:2]) +\
					" is available in OFM." +\
					"\n\rRegards," + \
					"\nTaras Dolgushin" + \
				 	"\nField Petrophysicist" + \
				 	"\nSub Surface Field Team" + \
					"\nSalym Petroleum Development N.V." + \
					"\nPhone:  +7 3463 297 300 ext.3486" + \
					"\nMobile: +7 932 440 29 29" + \
					"\nE-mail work: SPD-SALYM-SSFT-GE-C@salympetroleum.ru" + \
					"\nE-mail personal: Taras.Dolgushin@salympetroleum.ru"
	#attachment = "C:\\Apps\\OIS\\OIS_data.xlsx"
	#Msg.Attachments.Add(attachment)
	Msg.Display()
	#Msg.Send()
	
#os.startfile("E:\TECHLOG_PROJECT\USER_FOLDER\Report\PLT.txt")

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2015-12-20"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""