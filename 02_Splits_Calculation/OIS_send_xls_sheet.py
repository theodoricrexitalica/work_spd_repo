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
from win32com import client
import TechlogPlot as TP
import TechlogDialogAdvanced as TDA

for well in db.selectedWellList():
	myDialog = TDA.dialogAdvanced("Dataset Header Properties")
	list_comments = (["перфорация перед ГРП",
					  "освоение после ГРП",
					  "освоение","дострел",
					  "перевод в ППД",
					  "изоляции",
					  "корректировка",
					  "пересчет после ПГИ по спинеру",
					  "переток по результатам ПЛТ",
					  "заполнение таблицы OIS после ПЛТ"])
	myDialog.addListBox("Jobs", "Операции", list_comments)
	myDialog.execDialog()
	type=(myDialog.getListBox("Jobs"))
	email = win32com.client.Dispatch("Outlook.Application")
	Msg = email.CreateItem(0)
	Msg.To = "OIS"
	Msg.Subject = "Split_" + well
	text1 = "Добрый день,<br>Добавлена скважина "
	text2 = "<p>Regards," + \
			"<br>Taras Dolgushin" + \
		 	"<br>Field Petrophysicist" + \
		 	"<br>Sub Surface Field Team" + \
			"<br>Salym Petroleum Development N.V." + \
			"<br>Phone:  +7 3463 297 300 ext.3486" + \
			"<br>Mobile: +7 932 440 29 29" + \
			"<br>E-mail work: SPD-SALYM-SSFT-GE-C@salympetroleum.ru" + \
			"<br>E-mail personal: Taras.Dolgushin@salympetroleum.ru"
	Msg.HTMLBody = text1.decode("utf-8") + well + " (" + type[0] + ")" + text2
	attachment = "C:\\Apps\\Routine\\OIS\\OIS_data.xlsx"
	Msg.Attachments.Add(attachment)
	Msg.Display()
	print "Письмо сформировано"

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2013-04-22"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""