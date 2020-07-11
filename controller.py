import pandas as pd
import Cipher
from pathlib import Path
import openpyxl
import json
import os
import time

class Settings:
    def __init__(self):
        self.defaultEncapsulationList = ['category']
        self.defaultRemovedList = ['postal']
        self.defaultPassword = "doraemon"
        self.cipherObj = Cipher.cipherClass()
        self.setPassword(self.defaultPassword)

    def setPassword(self, password):
        self.defaultPassword = password
        self.cipherObj.setKey(password)
            

class Model(Settings):
        
    def __init__(self):
        Settings.__init__(self)
        self.encapsulationList = []
        self.removeList =[]
        self.df = pd.DataFrame() 
        self.filePath = ''
        self.mode = 1
        self.createFile = False
    
    """
    Converting non xlsx format, i.e csv, xls
    param: fname: String
    output: new_fname: String
    """
    def fileConversion(self, fname):
        self.createFile = True
        new_fname = Path(fname).stem + '.xlsx'
        df = pd.read_excel(fname)
        df.to_excel(new_fname, index=False)
        return new_fname
    
    """
    Set file path to class variable
    param: fname: String
    output: None
    """
    def setFile(self,fname):
        self.filePath = fname

    """
    Read excel content and parse as class Dataframe
    param: None
    output: None
    """
    def readContent(self):
        self.df = pd.read_excel(self.filePath)
        #self.df = pd.concat(pd.read_excel(filename, sheet_name=None))
        if self.mode == 1:
            columns = self.df.columns.ravel()
            self.encapsulationList = self.filter_view(columns, self.defaultEncapsulationList)
            self.removeList = self.filter_view(columns, self.defaultRemovedList)
    
    """
    Return list difference
    param: ops: List
    output: List
    """
    def offset(self, ops):
        return list(set(self.df) - set(ops))

    """
    Return list of class df column like in default list
    param: columnList: List, defaultList: List
    output: temp: List
    """
    def filter_view(self, columnList, defaultList):
        temp = []
        for default in defaultList:
            for file_col in columnList:
                if default.lower() in file_col.lower():
                    temp.append(file_col)
        return temp
    
       
    """
    Drop class df column given remove list
    param: None
    output: None
    """ 
    def dropColumns(self):
        self.df.drop(self.removeList, axis=1, inplace=True)
    
    """
    Looping through class df column and encrypt before updating back to class df
    param: progress_bar: ProgressBar
    output: None
    """     
    def encapColumns(self, progress_bar): 
        totalrow = self.df.shape[0]
        totalcol = len(self.encapsulationList)
        total = totalrow * totalcol
        curr = 0

        for column in (self.encapsulationList):
            for index, row in self.df.iterrows():
                self.df.at[index, column]=  self.cipherObj.encrypt(self.df.at[index, column])
                if (curr % 100 == 0):
                    progress_bar.UpdateBar(((curr/ total))* 99)
                curr = curr+1
    
    """
    Looping through class df column and decrypt before updating back to class df
    param: progress_bar: ProgressBar
    output: None
    """             
    def decapColumns(self, progress_bar):
        totalrow = self.df.shape[0]
        totalcol = len(self.encapsulationList)
        total = totalrow * totalcol
        curr = 0
        for column in (self.encapsulationList):
            for index, row in self.df.iterrows():
                self.df.at[index, column]=  self.cipherObj.decrypt(self.df.at[index, column])
                if (curr % 100 == 0):
                    progress_bar.UpdateBar(((curr/ total))* 99)
                curr = curr+1
    
    
    """
    Setting excel file settings
    param: modeString: String, filename: String
    output: None
    """     
    def setAttribute(self, filename):
        if self.mode == 1:
            data = {
                'mode': 'Encryption',
                'value': self.encapsulationList
            }

        else:
            data = ''
        workbook = openpyxl.load_workbook(filename)
        workbook.properties.keywords = data
        workbook.save(filename)
    
    """
    Get excel file settings, determine file ops and set mode type
    param: None
    output: None
    """
    def getAttribute(self):
        workbook = openpyxl.load_workbook(self.filePath)
        if workbook.properties.keywords != None:
            attribute = (eval(workbook.properties.keywords))
            mode_file = attribute['mode']
            self.encapsulationList = attribute['value']
            if mode_file == 'Encryption':
                self.mode = 2
        else:
            self.mode = 1

    """
    Write df to excel, Remove file, if it have being created
    param: None
    output: None
    """
    def writeFile(self):
        filename = Path(self.filePath).stem
        filename_new = '%s_%s.xlsx' % (filename,str(int(round(time.time() * 1000))))
        self.df.to_excel (filename_new, index = False, header=True)
        self.setAttribute(filename_new)
        self.removeFile()
        
    def removeFile(self):
        if self.createFile == True:
            os.remove(self.filePath)

