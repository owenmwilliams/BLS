import csv
import os
import numpy as np

class IndexGenerate():
    
    def __init__(self,*args):
        filename=''

    def OnOpen(self):
        """ Open a file"""
        self.filename = raw_input("Please enter the csv file name: ")
        
        return self.filename
    
    def IndexList(self, filename):
        data = csv.reader(open(filename, "rb"), delimiter = ';', quotechar = '"')
        self.IndexList = data.next()
        self.TypeList = data.next()
        return self.IndexList
        
    def SQLTableString(self):
    	self.Types = []
    	for i in range(len(self.TypeList)):
    		if isinstance(self.TypeList[i], str):
    			self.Types.append('STR')
    		elif isinstance(self.TypeList[i], int):
    			self.Types.append('INT')
    		elif isinstance(self.TypeList[i], float):
    			self.Types.append('FLT')
    	return self.Types

CallClass=IndexGenerate()

filename=CallClass.OnOpen()

print filename

print CallClass.IndexList(filename)

print CallClass.SQLTableString()
