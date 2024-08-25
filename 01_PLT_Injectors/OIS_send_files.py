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
import shutil
import webbrowser

pathxml="C:\\Apps\Routine\Send_xml\\"

for well in db.wellList():
	for ds in db.selectedDatasetList(well):
		name = well
		db.exportFile(pathxml,[well+"."+ds],"XML")
		shutil.copy(pathxml+well+"."+ds+".xml\\"+well+"_"+ds+".xml",pathxml+"sended")
		shutil.rmtree(pathxml+well+"."+ds+".xml")
		try:
			src=db.dirProject()+"\\Images\\"+well+"\\"+ds+"\\"
			Image=os.listdir(src)[0]
			src=src+Image
			shutil.copy(src,pathxml+"sended")
		except:
			continue

email = win32com.client.Dispatch("Outlook.Application")
Msg = email.CreateItem(0)
Msg.Subject = name
Msg.To = "Splits XML"
Msg.Body =	"\n\rRegards," + \
			"\nTaras Dolgushin" + \
		 	"\nField Petrophysicist" + \
		 	"\nSub Surface Field Team" + \
			"\nSalym Petroleum Development N.V." + \
			"\nPhone:  +7 495 411 7074 ext.3486" + \
			"\nMobile: +7 932 440 29 29" + \
			"\nE-mail work: SPD-SALYM-SSFT-GE-C@salympetroleum.ru" + \
			"\nE-mail personal: Taras.Dolgushin@salympetroleum.ru"
Msg.Display()

#os.startfile("C:\Users\Taras.Dolgushin\Desktop\Fish.txt")

webbrowser.open(pathxml + "sended")

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2014-05-02"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""