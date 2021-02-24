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
        
        self.goodmeasure_1.setText('Nothing Measured')  
        self.goodmeasure_1.setStyleSheet("background-color:lightblue;  border: 1px solid black;")  #save indicator
        self.goodmeasure_1.setAlignment(QtCore.Qt.AlignCenter)
        
        self.grading_1.setText('Nothing Measured')  
        self.grading_1.setStyleSheet("background-color:lightblue;  border: 1px solid black;")  #save indicator
        self.grading_1.setAlignment(QtCore.Qt.AlignCenter)
        
        self.goodmeasure_2.setText('Nothing Measured')  
        self.goodmeasure_2.setStyleSheet("background-color:lightblue;  border: 1px solid black;")  #save indicator
        self.goodmeasure_2.setAlignment(QtCore.Qt.AlignCenter)
        
        self.grading_2.setText('Nothing Measured')  
        self.grading_2.setStyleSheet("background-color:lightblue;  border: 1px solid black;")  #save indicator
        self.grading_2.setAlignment(QtCore.Qt.AlignCenter)
        
        self.plot_1.setBackground('w')
           
        my_absolute_dirpath = os.path.abspath(os.path.dirname(__file__))
        print(my_absolute_dirpath)
        catch = '\\'
        catch_count = 0
        count = 0
        end = 0
        for i in my_absolute_dirpath:
            count = count + 1
            if i == catch:
                catch_count = catch_count + 1
            
            if catch_count == 3:
                end = count
                break
        
        self.pathStart = my_absolute_dirpath[:end]
        print(self.pathStart)
        
        self.data = []
        self.summary = []
        self.inputList = []
        self.names = []
        self.type = []
        
        self.initUI()
        self.show()
        
    def initUI(self):
        self.measure_1.clicked.connect(self.measure_1_click)
        self.export_1.clicked.connect(self.export_1_click)
        self.measure_2.clicked.connect(self.measure_2_click)
        self.export_2.clicked.connect(self.export_2_click)
        self.measure_3.clicked.connect(self.measure_3_click)
        self.export_3.clicked.connect(self.export_3_click)
        self.measure_4.clicked.connect(self.measure_4_click)
        
    def measure_1_click(self):
        
        self.state_1.setText('Not Saved')  
        self.state_1.setStyleSheet("background-color: yellow;  border: 1px solid black;")
        self.grading_1.setText('Nothing Measured')  
        self.grading_1.setStyleSheet("background-color:lightblue;  border: 1px solid black;")
        self.goodmeasure_1.setText('Good Measurement')  
        self.goodmeasure_1.setStyleSheet("background-color: green;  border: 1px solid black;")
        
        self.BCH_1.setText("n/a")
        self.DROOP_1.setText("n/a")
        self.BCH_2.setText("n/a")
        self.DROOP_2.setText("n/a")
        self.BCH_3.setText("n/a")
        self.DROOP_3.setText("n/a")
        self.BCH_4.setText("n/a")
        self.DROOP_4.setText("n/a")
        self.BCH_5.setText("n/a")
        self.DROOP_5.setText("n/a")
        self.BCH_6.setText("n/a")
        self.DROOP_6.setText("n/a")
        self.BCH_7.setText("n/a")
        self.DROOP_7.setText("n/a")
        self.BCH_8.setText("n/a")
        self.DROOP_8.setText("n/a")
        self.BCH_average_1.setText("n/a")
        self.DROOP_average_1.setText("n/a")
        
        self.plot_1.clear()
        self.plot_1.plot([0,7], [25,25], pen=pg.mkPen('r', width=2))
        self.plot_1.plot([0,7], [35,35], pen=pg.mkPen('g', width=2))
        
        actuator_thickness = float(self.actuator_input_1.text())/1000
        frame_thickness = float(self.frame_input_1.text())/1000
        
        if self.no_frame_1.isChecked():
            frame_thickness = 0
            
        self.inputList = [self.sample_id.text(), self.comments.text(), actuator_thickness, frame_thickness] 
    
        self.names = ['1LBCH','1LF2A','1RBCH','1RF2A','2LBCH','2LF2A','2RBCH','2RF2A','3LBCH','3LF2A','3RBCH','3RF2A','4LBCH','4LF2A','4RBCH','4RF2A']
        
        if self.eightbyeight_1.isChecked(): 
            laser_path = '8by8 Bottom Stack'
            self.type = '8by8_'
            expected_output = ['4LBCH','4LF2A','4RBCH','4RF2A','2LBCH','2LF2A','2RBCH','2RF2A','3LBCH','3LF2A','3RBCH','3RF2A','1LBCH','1LF2A','1RBCH','1RF2A']
        
        if self.onebyfour_1.isChecked(): 
            laser_path = '1by4 Bottom Stack'
            self.type = '1by4_'
            expected_output = ['4LBCH','4LF2A','4RBCH','4RF2A','3LBCH','3LF2A','3RBCH','3RF2A','2LBCH','2LF2A','2RBCH','2RF2A','1LBCH','1LF2A','1RBCH','1RF2A']
            progam_number = b'015'
            save_path = self.pathStart + r'Documents\KEYENCE\LJ-X Series Terminal-Software\USB\SD2\lj-x3d\result\SD1_015'
                    
        if self.eightbytwelve_1.isChecked():
            laser_path = '8by12 Bottom Stack'
            self.type = '8by12_'
            expected_output = ['4LBCH','4LF2A','4RBCH','4RF2A','2LBCH','2LF2A','2RBCH','2RF2A','3LBCH','3LF2A','3RBCH','3RF2A','1LBCH','1LF2A','1RBCH','1RF2A']
            progam_number = b'013'
            save_path = self.pathStart + r'Documents\KEYENCE\LJ-X Series Terminal-Software\USB\SD2\lj-x3d\result\SD1_013'
                
        if self.flow_plate_1.isChecked():
            flowplate = True
        else:
            flowplate = False
            
        
        X8060_XYZ_path(progam_number,laser_path,flowplate)
        self.data = readTextFile(save_path,expected_output,self.names)
        
        self.summary = []
        average_list = [[],[]]

        for i in range(0,len(self.data),2):
            if self.data[i][0] != "Fail":
                BCH = (np.median(self.data[i]) - actuator_thickness) * 1000
                average_list[0].append(BCH)
                self.plot_1.plot([i/2], [BCH], symbol = 'o')
            else:
                BCH = 999
                self.goodmeasure_1.setText('Failed Measurement')  
                self.goodmeasure_1.setStyleSheet("background-color: red;  border: 1px solid black;")
            if self.data[i+1][0] != "Fail":
                droop = (np.median(self.data[i+1]) + frame_thickness) * 1000
                average_list[1].append(droop)
            else:
                droop = 999
                self.goodmeasure_1.setText('Failed Measurement')  
                self.goodmeasure_1.setStyleSheet("background-color: red;  border: 1px solid black;")
                
            self.summary.append([BCH, droop])
            
            if len(self.data[i]) < 20 or len(self.data[i+1]) < 20:
                self.goodmeasure_1.setText('Potentially Bad Measurement')  
                self.goodmeasure_1.setStyleSheet("background-color: red;  border: 1px solid black;")

        
        self.summary.append([np.average(average_list[0]), np.average(average_list[1])])
        
        
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
        
        try:
            grade = [value > 25 for sublist in self.summary[:8] for value in sublist[::2]]
            print(grade)
            if all(grade) == True:
                self.grading_1.setText('Pass - BCH above 25 microns')  
                self.grading_1.setStyleSheet("background-color:green;  border: 1px solid black;")  
            else:
                self.grading_1.setText('Fail - BCH too low')  
                self.grading_1.setStyleSheet("background-color:red;  border: 1px solid black;")   
        except:
            self.grading_1.setText('Fail - Measurement Error')  
            self.grading_1.setStyleSheet("background-color:red;  border: 1px solid black;")   
        
        
    def measure_2_click(self):
        
        self.inputList = [self.sample_id.text(), self.comments.text()] 
        
        self.state_2.setText('Not Saved')  
        self.state_2.setStyleSheet("background-color: yellow;  border: 1px solid black;")  #save indicator
        self.grading_2.setText('Nothing Measured')  
        self.grading_2.setStyleSheet("background-color:lightblue;  border: 1px solid black;")
        self.goodmeasure_2.setText('Good Measurement')  
        self.goodmeasure_2.setStyleSheet("background-color: green;  border: 1px solid black;")
        
        
        for n in range(8):
            for i in range(7):
                self.tableWidget_2.setItem(n+1, i+1, QTableWidgetItem(999))

        
        self.names = ['1LHW', '1LHCD', '1LHCW', '1LC2A', '1ANC', '1LD', '1LT', '1RHW', '1RHCD', '1RHCW', '1RC2A', '1ANC', '1RD', '1RT',
                      '2LHW', '2LHCD', '2LHCW', '2LC2A', '2ANC', '2LD', '2LT', '2RHW', '2RHCD', '2RHCW', '2RC2A', '2ANC', '2RD', '2RT',
                      '3LHW', '3LHCD', '3LHCW', '3LC2A', '3ANC', '3LD', '3LT', '3RHW', '3RHCD', '3RHCW', '3RC2A', '3ANC', '3RD', '3RT',
                      '4LHW', '4LHCD', '4LHCW', '4LC2A', '4ANC', '4LD', '4LT', '4RHW', '4RHCD', '4RHCW', '4RC2A', '4ANC', '4RD', '4RT']
                
        if self.eightbyeight_2.isChecked(): 
            laser_path = '8by8 Actuator'
            self.type = '8by8_'
            expected_output = ['3LD', '3RD', '3LHW', '3RHW', '3LHCW', '3RHCW', '3LHCD', '3RHCD', '3LC2A', '3RC2A', '3ANC', '3LT', '3RT',
                               '1LD', '1RD', '1LHW', '1RHW', '1LHCW', '1RHCW', '1LHCD', '1RHCD', '1LC2A', '1RC2A', '1ANC', '1LT', '1RT',
                               '4LD', '4RD', '4LHW', '4RHW', '4LHCW', '4RHCW', '4LHCD', '4RHCD', '4LC2A', '4RC2A', '4ANC', '4LT', '4RT',
                               '2LD', '2RD', '2LHW', '2RHW', '2LHCW', '2RHCW', '2LHCD', '2RHCD', '2LC2A', '2RC2A', '2ANC', '2LT', '2RT']
                
        if self.eightbytwelve_2.isChecked():
            laser_path = '8by12 Actuator'
            self.type = '8by12_'
            expected_output = ['3LD', '3RD', '3LHW', '3RHW', '3LHCW', '3RHCW', '3LHCD', '3RHCD', '3LC2A', '3RC2A', '3ANC', '3LT', '3RT',
                               '1LD', '1RD', '1LHW', '1RHW', '1LHCW', '1RHCW', '1LHCD', '1RHCD', '1LC2A', '1RC2A', '1ANC', '1LT', '1RT',
                               '4LD', '4RD', '4LHW', '4RHW', '4LHCW', '4RHCW', '4LHCD', '4RHCD', '4LC2A', '4RC2A', '4ANC', '4LT', '4RT',
                               '2LD', '2RD', '2LHW', '2RHW', '2LHCW', '2RHCW', '2LHCD', '2RHCD', '2LC2A', '2RC2A', '2ANC', '2LT', '2RT']
            progam_number = b'014'
            save_path = self.pathStart + r'Documents\KEYENCE\LJ-X Series Terminal-Software\USB\SD2\lj-x3d\result\SD1_014'
            
        if self.onebyfour_2.isChecked():
            laser_path = '1by4 Actuator'
            self.type = '1by4_'
            expected_output = ['1LD', '1RD', '1LHW', '1RHW', '1LHCW', '1RHCW', '1LHCD', '1RHCD', '1LC2A', '1RC2A', '1ANC', '1LT', '1RT',
                           '2LD', '2RD', '2LHW', '2RHW', '2LHCW', '2RHCW', '2LHCD', '2RHCD', '2LC2A', '2RC2A', '2ANC', '2LT', '2RT',
                           '3LD', '3RD', '3LHW', '3RHW', '3LHCW', '3RHCW', '3LHCD', '3RHCD', '3LC2A', '3RC2A', '3ANC', '3LT', '3RT',
                           '4LD', '4RD', '4LHW', '4RHW', '4LHCW', '4RHCW', '4LHCD', '4RHCD', '4LC2A', '4RC2A', '4ANC', '4LT', '4RT']
            progam_number = b'014'
            save_path = self.pathStart + r'Documents\KEYENCE\LJ-X Series Terminal-Software\USB\SD2\lj-x3d\result\SD1_014'
         
        flowplate = False    
        
        X8060_XYZ_path(progam_number,laser_path,flowplate)
        self.data = readTextFile(save_path,expected_output,self.names)
        
        self.summary = []
        temp = []
        for i in range(0,len(self.data),7):
            
            lengthcheck = [len(sublist) for sublist in self.data[i:i+6]]  
            print(lengthcheck)
            for r in lengthcheck:
                if r < 20:
                    self.goodmeasure_2.setText('Potentially Bad Measurement')  
                    self.goodmeasure_2.setStyleSheet("background-color: red;  border: 1px solid black;")
            
            if self.data[i][0] != "Fail":
                temp.append(np.median(self.data[i]))
            else:
                 temp.append(999)
                 self.goodmeasure_2.setText('Failed Measurement')  
                 self.goodmeasure_2.setStyleSheet("background-color: red;  border: 1px solid black;")
            if self.data[i+1][0] != "Fail":
                temp.append(np.median(self.data[i+1]))
            else:
                 temp.append(999)
                 self.goodmeasure_2.setText('Failed Measurement')  
                 self.goodmeasure_2.setStyleSheet("background-color: red;  border: 1px solid black;")
            if self.data[i+2][0] != "Fail":
                temp.append(np.median(self.data[i+2]))
            else:
                 temp.append(999)
                 self.goodmeasure_2.setText('Failed Measurement')  
                 self.goodmeasure_2.setStyleSheet("background-color: red;  border: 1px solid black;")
            if self.data[i+3][0] != "Fail":
                temp.append(np.median(self.data[i+3]))
            else:
                 temp.append(999)
                 self.goodmeasure_2.setText('Failed Measurement')  
                 self.goodmeasure_2.setStyleSheet("background-color: red;  border: 1px solid black;")
            if self.data[i+4][0] != "Fail":
                temp.append(np.median(self.data[i+4]))
            else:
                 temp.append(999)
                 self.goodmeasure_2.setText('Failed Measurement')  
                 self.goodmeasure_2.setStyleSheet("background-color: red;  border: 1px solid black;")
            if self.data[i+5][0] != "Fail":
                temp.append(np.median(self.data[i+5]))
            else:
                 temp.append(999)
                 self.goodmeasure_2.setText('Failed Measurement')  
                 self.goodmeasure_2.setStyleSheet("background-color: red;  border: 1px solid black;")
            if self.data[i+6][0] != "Fail":
                temp.append(np.median(self.data[i+6]))
            else:
                 temp.append(999)
                 self.goodmeasure_2.setText('Failed Measurement')  
                 self.goodmeasure_2.setStyleSheet("background-color: red;  border: 1px solid black;")
            
            self.summary.append(temp)
            temp = []
            
        for n in range(len(self.summary)):
            for i in range(len(self.summary[n])):
                self.tableWidget_2.setItem(n+1, i+1, QTableWidgetItem('%.3f' % self.summary[n][i]))
                
        C2A = [] 
        grade = []
        for i in [sublist[3] for sublist in self.summary]:
            C2A.append(i)
            
        for n in range(0,len(C2A),2):
            if C2A[n] == 999 or C2A[n+1] == 999:
                continue
            else:
                grade.append(C2A[n])
                grade.append(C2A[n+1])
                
        left = [value for value in grade[::2]]
        right = [value for value in grade[1::2]]
        difference = np.abs((sum(left) - sum(right))/len(left))
        print(difference)
            
        if difference > 0.1:
            self.grading_2.setText('Grade Fail')  
            self.grading_2.setStyleSheet("background-color: red;  border: 1px solid black;")
            
        if difference <= 0.1 and difference > 0.05:
            self.grading_2.setText('Grade C')  
            self.grading_2.setStyleSheet("background-color: yellow;  border: 1px solid black;")
            
        if difference <= 0.05 and difference > 0.025:
            self.grading_2.setText('Grade B')  
            self.grading_2.setStyleSheet("background-color: green;  border: 1px solid black;")
        
        if difference <= 0.025:
            self.grading_2.setText('Grade A')  
            self.grading_2.setStyleSheet("background-color: green;  border: 1px solid black;")
            

    def measure_3_click(self):
        self.state_3.setText('Not Saved')  
        self.state_3.setStyleSheet("background-color: yellow;  border: 1px solid black;")  #save indicator
        
        for n in range(8):
            for i in range(3):
                self.tableWidget_3.setItem(n+1, i+1, QTableWidgetItem(999))
        
        self.names = ['1LFC','1RFC','1D','2LFC','2RFC','2D','3LFC','3RFC','3D','4LFC','4RFC','4D']
        
        if self.eightbyeight_3.isChecked(): 
            prog = b'001'
            path = self.pathStart + r'Documents\KEYENCE\LJ-X Series Terminal-Software\USB\SD2\lj-x3d\result\SD1_001'
                
        if self.twelvebyeight_3.isChecked():
            laser_path = '8by12 Orifice'
            self.type = '8by12_'
            progam_number = b'017'
            save_path = self.pathStart + r'Documents\KEYENCE\LJ-X Series Terminal-Software\USB\SD2\lj-x3d\result\SD1_017'
            expected_output = ['4LFC','4RFC','4D','2LFC','2RFC','2D','3LFC','3RFC','3D','1LFC','1RFC','1D']
            
        flowplate = False    
        
        self.inputList = [self.sample_id.text(), self.comments.text()] 
        X8060_XYZ_path(progam_number,laser_path,flowplate)
        self.data = readTextFile(save_path,expected_output,self.names)
        
        self.summary = []
        for i in range(0,len(self.data),3):
            self.summary.append([np.median(self.data[i]), np.median(self.data[i+1]), np.median(self.data[i+2])])
        
        for n in range(len(self.summary)):
            for i in range(len(self.summary[n])):
                self.tableWidget_3.setItem(n+1, i+1, QTableWidgetItem('%.3f' % self.summary[n][i]))


    def measure_4_click(self):
        
        self.state_4.setText('Not Saved')  
        self.state_4.setStyleSheet("background-color: yellow;  border: 1px solid black;")
        
        self.v_1_4.setText("n/a")
        self.h_1_4.setText("n/a")
        self.v_2_4.setText("n/a")
        self.h_2_4.setText("n/a")
        self.v_3_4.setText("n/a")
        self.h_3_4.setText("n/a")
        self.v_4_4.setText("n/a")
        self.h_4_4.setText("n/a")
            
        self.inputList = [self.sample_id.text(), self.comments.text()]
    
        self.names = ['1TW', '1BW', '1TL', '1BL','2TW', '2BW', '2TL', '2BL','3TW', '3BW', '3TL', '3BL','4TW', '4BW', '4TL', '4BL']
        
        # if self.eightbyeight_1.isChecked(): 
        #     laser_path = '8by8 Jet Channel'
        #     self.type = '8by8_'
        #     expected_output = ['3TW','3BW','3TL','3BL','1TW','1BW','1TL','1BL','4TW','4BW','4TL','4BL','2TW','2BW','2TL','2BL']
        
        if self.onebyfour_4.isChecked(): 
            laser_path = '1by4 Jet Channel'
            self.type = '1by4_'
            expected_output = ['1TW', '1BW', '1TL', '1BL','2TW', '2BW', '2TL', '2BL','3TW', '3BW', '3TL', '3BL','4TW', '4BW', '4TL', '4BL']
            progam_number = b'0'
            save_path = self.pathStart + r'Documents\KEYENCE\LJ-X Series Terminal-Software\USB\SD2\lj-x3d\result\SD1_0'
                    
        if self.twobytwo_4.isChecked():
            laser_path = '8by12 Jet Channel'
            self.type = '8by12_'
            expected_output = ['3TW','3BW','3TL','3BL','1TW','1BW','1TL','1BL','4TW','4BW','4TL','4BL','2TW','2BW','2TL','2BL']
            progam_number = b'016'
            save_path = self.pathStart + r'Documents\KEYENCE\LJ-X Series Terminal-Software\USB\SD2\lj-x3d\result\SD1_016'
                
        flowplate = False
            
        X8060_XYZ_path(progam_number,laser_path,flowplate)
        self.data = readTextFile(save_path,expected_output,self.names)
        
        self.summary = []

        for i in range(0,len(self.data),4):
            if self.data[i][0] != "Fail":
                topwidth = np.median(self.data[i])
                
            else:
                topwidth = 999
                
            if self.data[i+1][0] != "Fail":
                bottomwidth = np.median(self.data[i])
                
            else:
                bottomwidth = 999
                
            if self.data[i+2][0] != "Fail":
                toplength = np.median(self.data[i])
                
            else:
                toplength = 999
                
            if self.data[i+3][0] != "Fail":
                bottomlength = np.median(self.data[i])
                
            else:
                bottomlength = 999

            temp = []
            if topwidth != 999 and bottomwidth != 999:
                temp.append(topwidth - bottomwidth)
            else:
                temp.append(999)
                
            if toplength != 999 and bottomlength != 999:
                temp.append(toplength - bottomlength)
            else:
                temp.append(999)
                
            self.summary.append(temp)
        
        
        self.v_1_4.setText("%.2f" %self.summary[0][0])
        self.h_1_4.setText("%.2f" %self.summary[0][1])
        self.v_2_4.setText("%.2f" %self.summary[1][0])
        self.h_2_4.setText("%.2f" %self.summary[1][1])
        self.v_3_4.setText("%.2f" %self.summary[2][0])
        self.h_3_4.setText("%.2f" %self.summary[2][1])
        self.v_4_4.setText("%.2f" %self.summary[3][0])
        self.h_4_4.setText("%.2f" %self.summary[3][1])
        
    def export_1_click(self):
        print('Saving Files')
        self.inputList[0] = self.sample_id.text()
        self.inputList[1] = self.comments.text()
        sides = ['1L', '1R', '2L', '2R', '3L', '3R', '4L', '4R']
        file_name = '\BCH&Droop_' + self.type + self.inputList[0] + '.xlsx'
        
        while True:
            try:
                dir_path = QFileDialog.getExistingDirectory(self, 'open a folder', self.pathStart + r'Frore Systems\RnD - Documents\Characterization\Keyence LJXMappingTool\data\X8060_gui_data')
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
        
        inputValues = pd.DataFrame({'names' : ['Sample ID', 'Comments', 'Actuator Thickness', 'Frame Thickness'], 
                                    'values' : self.inputList})
        
        inputValues.to_excel(writer, sheet_name='Data', index=False, startcol=0, startrow=0)
        
        summaryValues = pd.DataFrame({'side' : sides, 
                                     self.inputList[0] + '_BCH' : [self.summary[i][0] for i in range(8)],
                                     self.inputList[0] + '_Droop' : [self.summary[i][1] for i in range(8)],
                                     })
        
        summaryValues.to_excel(writer, sheet_name='Data', index=False, startcol=3, startrow=0)
        
        label = []
        for i in range(len(self.data)):
            temp = [self.names[i]] * len(self.data[i])
            label.append(temp)
            
        flat_data = [j for sub in self.data[::2] for j in sub]
        flat_names = [j for sub in label[::2] for j in sub]
        
        BCH = pd.DataFrame({'BCH' : flat_data, 
                          self.inputList[0] : flat_names})
                  
        BCH.to_excel(writer, sheet_name='Data', index=False, startcol=6, startrow=0)
        
        flat_data = [j for sub in self.data[1::2] for j in sub]
        flat_names = [j for sub in label[1::2] for j in sub]
        
        F2A = pd.DataFrame({'Droop' : flat_data, 
                          self.inputList[0] : flat_names})
        
        F2A.to_excel(writer, sheet_name='Data', index=False, startcol=9, startrow=0)
        
        
        writer.save()
        print('Finished Saving')
        self.state_1.setText('Saved File')
        self.state_1.setStyleSheet("background-color: green;  border: 1px solid black;") 
        
        
    def export_2_click(self):
        print('Saving Files')
        self.inputList[0] = self.sample_id.text()
        self.inputList[1] = self.comments.text()
        sides = ['1L', '1R', '2L', '2R', '3L', '3R', '4L', '4R']
        file_name = '\Actuator_' + self.inputList[0] + '.xlsx'
        
        while True:
            try:
                dir_path = QFileDialog.getExistingDirectory(self, 'open a folder', self.pathStart + r'Frore Systems\RnD - Documents\Characterization\Keyence LJXMappingTool\data\X8060_gui_data')
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
        
        inputValues = pd.DataFrame({'names' : ['Sample ID', 'Comments'], 
                                    'values' : self.inputList})
        
        inputValues.to_excel(writer, sheet_name='Data', index=False, startcol=0, startrow=0)
        
        summaryValues = pd.DataFrame({'side' : sides, 
                                     self.inputList[0] + '_HWidth' : [self.summary[i][0]*1000 for i in range(8)],
                                     self.inputList[0] + '_HCDepth' : [self.summary[i][1]*1000 for i in range(8)],
                                     self.inputList[0] + '_HCWidth' : [self.summary[i][2] for i in range(8)],
                                     self.inputList[0] + '_C2AWidth' : [self.summary[i][3] for i in range(8)],
                                     self.inputList[0] + '_AWidth' : [self.summary[i][4] for i in range(8)],
                                     self.inputList[0] + '_Droop' : [self.summary[i][5]*1000 for i in range(8)],
                                     self.inputList[0] + '_T' : [self.summary[i][6]*1000 for i in range(8)],
                                     })
        
        summaryValues.to_excel(writer, sheet_name='Data', index=False, startcol=3, startrow=0)
        
        label = []
        for i in range(len(self.data)):
            temp = [self.names[i]] * len(self.data[i])
            label.append(temp)
            
        columnNames = ['HWidth', 'HCDepth', 'HCWidth', 'C2AWidth', 'AWidth', 'Droop', 'T']
            
        for i in range(7):    
            
            flat_data = [j for sub in self.data[i::7] for j in sub]
            flat_names = [j for sub in label[i::7] for j in sub]
        
            rawData = pd.DataFrame({columnNames[i] : flat_data, 
                          self.inputList[0] : flat_names})
                  
            rawData.to_excel(writer, sheet_name='Data', index=False, startcol=11 + 3*i, startrow=0)
        
    
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
                dir_path = QFileDialog.getExistingDirectory(self, 'open a folder', self.pathStart + r'Frore Systems\RnD - Documents\Characterization\Keyence LJXMappingTool\data\X8060_gui_data')
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
    
