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
import pythoncom
pythoncom.CoInitialize()
path_ois =r"C:\Apps\Routine\OIS\OIS_data.xlsx"
xlApp = win32com.client.Dispatch("Excel.Application")
xlApp.Visible = True
xlApp.Workbooks.Open(path_ois)

__author__ = """Taras DOLGUSHIN (Taras.Dolgushin)"""
__date__ = """2017-06-27"""
__version__ = """1.0"""
__group__ = """"""
__suffix__ = """"""
__prefix__ = """"""