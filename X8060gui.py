# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 16:47:38 2021

@author: Nicolas Madhavapeddy
"""




import pandas as pd
import sys
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTableWidgetItem
from PyQt5.QtCore import QCoreApplication
import pyqtgraph as pg
import numpy as np
import visa
import matplotlib.pyplot as plt
import os
from os import path
import time

from X8060_XYZ_path_gui import X8060_XYZ_path
from readTextFile_gui import readTextFile

class X8060GUI(QMainWindow):
    def __init__(self):
        super(X8060GUI, self).__init__()
        uic.loadUi('X8060gui.ui', self) 
        
        self.state_1.setText('Nothing Measured')  
        self.state_1.setStyleSheet("background-color:lightblue;  border: 1px solid black;")  #save indicator
        self.state_1.setAlignment(QtCore.Qt.AlignCenter)
        
        self.state_2.setText('Nothing Measured')  
        self.state_2.setStyleSheet("background-color:lightblue;  border: 1px solid black;")  #save indicator
        self.state_2.setAlignment(QtCore.Qt.AlignCenter)
        
        self.state_3.setText('Nothing Measured')  
        self.state_3.setStyleSheet("background-color:lightblue;  border: 1px solid black;")  #save indicator
        self.state_3.setAlignment(QtCore.Qt.AlignCenter)
        
        self.plot_1.setBackground('w')
        self.plot_2.setBackground('w')
        self.plot_3.setBackground('w')
        self.plot_4.setBackground('w')
        self.plot_5.setBackground('w')
        self.plot_6.setBackground('w')
        self.plot_7.setBackground('w')
        self.plot_8.setBackground('w')
        
        self.data = []
        self.summary = []
        self.inputList = []
        self.names = []
        
        self.initUI()
        self.show()
        
    def initUI(self):
        self.measure_1.clicked.connect(self.measure_1_click)
        self.export_1.clicked.connect(self.export_1_click)
        self.measure_2.clicked.connect(self.measure_2_click)
        self.export_2.clicked.connect(self.export_2_click)
        self.measure_3.clicked.connect(self.measure_3_click)
        self.export_3.clicked.connect(self.export_3_click)
        
    def measure_1_click(self):
        
        actuator = float(self.actuator_input_1.text())
        frame = float(self.frame_input_1.text())
        
        self.plot_1.clear()
        self.plot_2.clear()
        self.plot_3.clear()
        self.plot_4.clear()
        self.plot_5.clear()
        self.plot_6.clear()
        self.plot_7.clear()
        self.plot_8.clear()
        
        if self.eightbyeight_1.isChecked(): 
            if self.frame_1.isChecked():
                prog = b'008'
                path = r'C:\Users\nmadh\Documents\KEYENCE\LJ-X Series Terminal-Software\USB\SD2\lj-x3d\result\SD1_008'
                    
        if self.twelvebyeight_1.isChecked():
            if self.frame_1.isChecked():
                prog = b'011'
                path = r'C:\Users\nmadh\Documents\KEYENCE\LJ-X Series Terminal-Software\USB\SD2\lj-x3d\result\SD1_011'
                
            if self.no_frame_1.isChecked():
                frame = 0
                prog = b'010'
                path = r'C:\Users\nmadh\Documents\KEYENCE\LJ-X Series Terminal-Software\USB\SD2\lj-x3d\result\SD1_010'
                
        if self.flow_plate_1.isChecked():
            flowplate = True
            
        if self.no_flow_plate_1.isChecked():
            flowplate = False
                    
                                     
        self.state_1.setText('Not Saved')  
        self.state_1.setStyleSheet("background-color: yellow;  border: 1px solid black;")  #save indicator
        
        
        self.inputList = [self.sample_id.text(), self.comments.text(), actuator, frame] 
        X8060_XYZ_path(prog,flowplate)
        expected = ['2LBCH','2LF2A','2RBCH','2RF2A','4LBCH','4LF2A','4RBCH','4RF2A','1LBCH','1LF2A','1RBCH','1RF2A','3LBCH','3LF2A','3RBCH','3RF2A']
        self.names = ['1LBCH','1LF2A','1RBCH','1RF2A','2LBCH','2LF2A','2RBCH','2RF2A','3LBCH','3LF2A','3RBCH','3RF2A','4LBCH','4LF2A','4RBCH','4RF2A']
        self.data = readTextFile(path,expected,self.names)
        
        self.summary = []
        for i in range(0,len(self.data),2):
            self.summary.append([(np.median(self.data[i]) - actuator) * 1000, (np.median(self.data[i+1]) + frame) * 1000])
          
        self.summary.append([np.average([item[0] for item in self.summary]), np.average([item[1] for item in self.summary])])
        
        self.plot_1.plot(range(len(self.data[0])), self.data[0])
        self.plot_2.plot(range(len(self.data[2])), self.data[2])
        self.plot_3.plot(range(len(self.data[4])), self.data[4])
        self.plot_4.plot(range(len(self.data[6])), self.data[6])
        self.plot_5.plot(range(len(self.data[8])), self.data[8])
        self.plot_6.plot(range(len(self.data[10])), self.data[10])
        self.plot_7.plot(range(len(self.data[12])), self.data[12])
        self.plot_8.plot(range(len(self.data[14])), self.data[14])
        
        self.BCH_1.setText("%.2f" %self.summary[0][0])
        self.DROOP_1.setText("%.2f" %self.summary[0][1])
        self.BCH_2.setText("%.2f" %self.summary[1][0])
        self.DROOP_2.setText("%.2f" %self.summary[1][1])
        self.BCH_3.setText("%.2f" %self.summary[2][0])
        self.DROOP_3.setText("%.2f" %self.summary[2][1])
        self.BCH_4.setText("%.2f" %self.summary[3][0])
        self.DROOP_4.setText("%.2f" %self.summary[3][1])
        self.BCH_5.setText("%.2f" %self.summary[4][0])
        self.DROOP_5.setText("%.2f" %self.summary[4][1])
        self.BCH_6.setText("%.2f" %self.summary[5][0])
        self.DROOP_6.setText("%.2f" %self.summary[5][1])
        self.BCH_7.setText("%.2f" %self.summary[6][0])
        self.DROOP_7.setText("%.2f" %self.summary[6][1])
        self.BCH_8.setText("%.2f" %self.summary[7][0])
        self.DROOP_8.setText("%.2f" %self.summary[7][1])
        self.BCH_average_1.setText("%.2f" %self.summary[8][0])
        self.DROOP_average_1.setText("%.2f" %self.summary[8][1])
        

    def measure_2_click(self):
        
        if self.eightbyeight_2.isChecked(): 
            
            if self.integrated_baffle_2.isChecked():
                prog = b'005'
                path = r'C:\Users\nmadh\Documents\KEYENCE\LJ-X Series Terminal-Software\USB\SD2\lj-x3d\result\SD1_005'
            if self.no_integrated_baffle_2.isChecked():
                prog = b'003'
                path = r'C:\Users\nmadh\Documents\KEYENCE\LJ-X Series Terminal-Software\USB\SD2\lj-x3d\result\SD1_003'
                
        if self.twelvebyeight_2.isChecked():
            prog = b'004'
            path = r'C:\Users\nmadh\Documents\KEYENCE\LJ-X Series Terminal-Software\USB\SD2\lj-x3d\result\SD1_004'
            
        if self.flow_plate_2.isChecked():
            flowplate = True
            
        if self.no_flow_plate_2.isChecked():
            flowplate = False    
            
        
        self.state_2.setText('Not Saved')  
        self.state_2.setStyleSheet("background-color: yellow;  border: 1px solid black;")  #save indicator
        
        self.inputList = [self.sample_id.text(), self.comments.text()] 
        X8060_XYZ_path(prog,flowplate)
        expected = []
        self.names = []
        self.data = readTextFile(path,expected,self.names)
        
        for n in range(len(self.data)):
            for i in range(len(self.data[n])):
                self.tableWidget_2.setItem(n+1, i+1, QTableWidgetItem('%.3f' % self.data[n][i]))
                
    def measure_3_click(self):
        if self.eightbyeight_3.isChecked(): 
            prog = b'001'
        if self.twelvebyeight_3.isChecked():
            prog = b'001'
        self.state_3.setText('Not Saved')  
        self.state_3.setStyleSheet("background-color: yellow;  border: 1px solid black;")  #save indicator
        
        self.inputList = [self.sample_id.text(), self.comments.text()] 
        X8060_XYZ_path(prog)
        if self.eightbyeight.isChecked(): 
            self.data = readTextFile(r'C:\Users\nmadh\Documents\KEYENCE\LJ-X Series Terminal-Software\USB\SD2\lj-x3d\result\SD1_001')
        if self.twelvebyeight.isChecked():
            self.data = readTextFile(r'C:\Users\nmadh\Documents\KEYENCE\LJ-X Series Terminal-Software\USB\SD2\lj-x3d\result\SD1_001')
        
        for n in range(len(self.data)):
            for i in range(len(self.data[n])):
                self.tableWidget_3.setItem(i+1, n+1, QTableWidgetItem('%.3f' % self.data[n][i]))

        
    def export_1_click(self):
        print('Saving Files')
        self.inputList = [self.sample_id.text(), self.comments.text()] 
        file_name = '\BCH&Droop_' + self.inputList[0] + '.xlsx'
        
        while True:
            try:
                dir_path = QFileDialog.getExistingDirectory(self, 'open a folder', r'C:\Users\nmadh\Frore Systems\RnD - Documents\Characterization\Keyence LJXMappingTool\data\X8060_gui_data')
                break
            except PermissionError:
                return None
            
        if path.exists(dir_path + file_name): #testing if file already exists
            self.state_1.setText('Warning: File already exists')
            self.state_1.setStyleSheet("background-color: red;  border: 1px solid black;") 
            print('Could not Save')
            return None
        
        print('**************************')
        writer = pd.ExcelWriter(dir_path + file_name, engine='xlsxwriter')
        
        label = []
        print(len(self.data), len(self.names))
        for i in range(len(self.data)):
            temp = [self.names[i]] * len(self.data[i])
            label.append(temp)
            
        flat_data = [j for sub in self.data[::2] for j in sub]
        flat_names = [j for sub in label[::2] for j in sub]
        
        BCH = pd.DataFrame({'BCH' : flat_data, 
                          self.inputList[0] : flat_names})
        
            
        BCH.to_excel(writer, sheet_name='Data', index=False, startcol=0, startrow=0)
        
        flat_data = [j for sub in self.data[1::2] for j in sub]
        flat_names = [j for sub in label[1::2] for j in sub]
        
        F2A = pd.DataFrame({'Frame to Actuator' : flat_data, 
                          self.inputList[0] : flat_names})
        
        F2A.to_excel(writer, sheet_name='Data', index=False, startcol=3, startrow=0)
        
        
        writer.save()
        print('Finished Saving')
        self.state_1.setText('Saved File')
        self.state_1.setStyleSheet("background-color: green;  border: 1px solid black;") 
        
        
    def export_2_click(self):
        print('Saving Files')
        self.inputList = [self.sample_id.text(), self.comments.text()] 
        file_name = '\Actuator_' + self.inputList[0] + '.xlsx'
        
        while True:
            try:
                dir_path = QFileDialog.getExistingDirectory(self, 'open a folder', r'C:\Users\nmadh\Frore Systems\RnD - Documents\Characterization\Keyence LJXMappingTool\data\X8060_gui_data')
                break
            except PermissionError:
                return None
            
        if path.exists(dir_path + file_name): #testing if file already exists
            self.state_2.setText('Warning: File already exists')
            self.state_2.setStyleSheet("background-color: red;  border: 1px solid black;") 
            print('Could not Save')
            return None
        
        print('**************************')
        writer = pd.ExcelWriter(dir_path + file_name, engine='xlsxwriter')
        given = pd.DataFrame({'names':['Sample ID', 'Comments'], 
                              'values' : self.inputList
                              })
        given.to_excel(writer, sheet_name='Data', header=False, index=False, startcol=0,startrow=0)
        
        names = ['Maximum Hammertail Cavity', 'Minimum Hammertail Cavity', 'Average Hammertail Cavity', 
                 'Maximum Cavity to Anchor', 'Minimum Cavity to Anchor', 'Average Cavity to Anchor',
                 'Maximum Anchor', 'Minimum Anchor', 'Average Anchor']
        
        for i in range(9):
            dataCollected = pd.DataFrame({'Cell':['1L', '1R', '2L', '2R', '3L', '3R', '4L', '4R'],
                                 names[i] : self.data[i]})
            
            dataCollected.to_excel(writer, sheet_name='Data', index=False, startcol=3 + (i * 3), startrow=0)
        
        
        writer.save()
        print('Finished Saving')
        self.state_2.setText('Saved File')
        self.state_2.setStyleSheet("background-color: green;  border: 1px solid black;") 
        
    def export_3_click(self):
        print('Saving Files')
        self.inputList = [self.sample_id.text(), self.comments.text()] 
        file_name = '\Orifice_' + self.inputList[0] + '.xlsx'
        
        while True:
            try:
                dir_path = QFileDialog.getExistingDirectory(self, 'open a folder', r'C:\Users\nmadh\Frore Systems\RnD - Documents\Characterization\Keyence LJXMappingTool\data\X8060_gui_data')
                break
            except PermissionError:
                return None
            
        if path.exists(dir_path + file_name): #testing if file already exists
            self.state_3.setText('Warning: File already exists')
            self.state_3.setStyleSheet("background-color: red;  border: 1px solid black;") 
            print('Could not Save')
            return None
        
        print('**************************')
        writer = pd.ExcelWriter(dir_path + file_name, engine='xlsxwriter')
        given = pd.DataFrame({'names':['Sample ID', 'Comments'], 
                              'values' : self.inputList
                              })
        given.to_excel(writer, sheet_name='Data', header=False, index=False, startcol=0,startrow=0)
        
        names = ['Maximum Frame to Cavity', 'Minimum Frame to Cavity', 'Average Frame to Cavity', 
                 'Maximum Cavity Length', 'Minimum Cavity Length', 'Average Cavity Length',
                 'Maximum Cavity Height', 'Minimum Cavity Height', 'Average Cavity Height', 
                 'Maximum Anchor', 'Minimum Anchor', 'Average Anchor']
        
        for i in range(12):
            dataCollected = pd.DataFrame({'Cell':['1L', '1R', '2L', '2R', '3L', '3R', '4L', '4R'],
                                 names[i] : self.data[i]})
            
            dataCollected.to_excel(writer, sheet_name='Data', index=False, startcol=3 + (i * 3), startrow=0)
        
        
        writer.save()
        print('Finished Saving')
        self.state_3.setText('Saved File')
        self.state_3.setStyleSheet("background-color: green;  border: 1px solid black;") 
        
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = X8060GUI()
    sys.exit(app.exec_())
    
