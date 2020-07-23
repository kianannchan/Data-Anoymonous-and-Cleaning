
import Cipher
from pathlib import Path
import openpyxl
import json
import os
import pandas as pd
import time
import numpy as np


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
    Read and Set file path to class variable
    param: fname: String
    output: None
    """
    def setFilePath(self,filePath):
        self.filePath = filePath
        if 'xls' in filePath:
            self.df = pd.read_excel(filePath, sheet_name=None, ignore_index=True)
        else:
            self.df = pd.read_csv(filePath)


    """
    Determine source file header exist
    param: None
    output: Bool
    """
    def detectCommonHeader(self):
        for sheet in range(len(self.df)):
            col= self.df[list(self.df.keys())[sheet]].columns.tolist()
            if sheet != len(self.df) - 1:
                col2= self.df[list(self.df.keys())[sheet + 1]].columns.tolist()
                if (col != col2):
                    return False
        return True
    
    """
    Parse sheets data into singular sheet base on common header
    param: None
    output: None
    """  
    def SubsequentHeader(self):
        self.df = pd.concat(self.df)
        self.df.replace(np.nan, '' , inplace=True)

    
    """
    Parse sheets data into singular sheet base on casading mode
    param: None
    output: None
    """    
    def noSubsequentHeader(self):
        col= self.df[list(self.df.keys())[0]].columns.tolist()
        list_DF =[]

        # accessing from data
        for index in range(len(self.df)):
            subsequent_frame = self.df[list(self.df.keys())[index]]
            subsequent_frame.loc[-1] = subsequent_frame.columns.tolist()
            subsequent_frame.index = subsequent_frame.index + 1  # shifting index
            subsequent_frame.sort_index(inplace=True) 
            subsequent_frame.columns = col
            list_DF.append(subsequent_frame)

        self.df = pd.concat(list_DF, ignore_index= True)
        self.df = self.df[1:]  



    """
    Extracting Default List to Encryption and Removed List
    param: None
    output: None
    """
    def readContent(self):
        columns = self.df.columns.tolist()
        self.encapsulationList = self.filter_view(columns, self.defaultEncapsulationList)
        if self.mode == 1:
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
                if (default.lower() in file_col.lower()): 
                    if(file_col not in temp and ( file_col not in self.encapsulationList and file_col not in self.removeList)):
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
            self.df[[column]] = self.df[[column]].astype(str)
            for index, row in self.df.iterrows():
                colValue = str(self.df.at[index, column])
                if len(colValue) > 0:
                        self.df.at[index, column]=  self.cipherObj.encrypt((colValue))
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
            self.defaultEncapsulationList = attribute['value']
            if mode_file == 'Encryption':
                self.mode = 2
        else:
            self.mode = 1

    """
    Write df to excel
    param: None
    output: None
    """
    def writeFile(self):
        filename = Path(self.filePath).stem
        filename_new = '%s_%s.xlsx' % (filename,str(int(round(time.time() * 1000))))
        self.df.to_excel (filename_new, index = False, header=True)
        self.setAttribute(filename_new)
    

    
    """
    Create new predefine data to JSON file
    param: None
    output: None
    """      
    def writeDefaultList(self):
        new_remove = []
        new_encap = []
        [new_remove.append(x) for x in (" ".join(self.removeList)).split() if x not in new_remove]
        [new_encap.append(x) for x in (" ".join(self.encapsulationList)).split() if x not in new_encap]
        settings = {
            'default_remove': new_remove,
            'default_encap': new_encap
        }
        with open('settings.json', 'w') as json_file:
            json.dump(settings, json_file)
            
    
    """
    Read predefine JSON file and update to default list
    param: None
    output: None
    """    
    def readDefaultList(self):
        if (Path('settings.json').exists()):
            with open('settings.json') as f:
                data = json.load(f)
                self.defaultRemovedList = (data['default_remove'])
                self.defaultEncapsulationList = (data['default_encap'])


if __name__ == '__main__':
    pass


    