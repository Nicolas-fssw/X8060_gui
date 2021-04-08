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
        
        self.state_4.setText('Nothing Measured')  
        self.state_4.setStyleSheet("background-color:lightblue;  border: 1px solid black;")  #save indicator
        self.state_4.setAlignment(QtCore.Qt.AlignCenter)
        
        self.grading_1.setText('Nothing Measured')  
        self.grading_1.setStyleSheet("background-color:lightblue;  border: 1px solid black;")  #save indicator
        self.grading_1.setAlignment(QtCore.Qt.AlignCenter)
        
        self.grading_2.setText('Nothing Measured')  
        self.grading_2.setStyleSheet("background-color:lightblue;  border: 1px solid black;")  #save indicator
        self.grading_2.setAlignment(QtCore.Qt.AlignCenter)
        
        self.grading_3.setText('Nothing Measured')  
        self.grading_3.setStyleSheet("background-color:lightblue;  border: 1px solid black;")  #save indicator
        self.grading_3.setAlignment(QtCore.Qt.AlignCenter)
        
        self.grading_4.setText('Nothing Measured')  
        self.grading_4.setStyleSheet("background-color:lightblue;  border: 1px solid black;")  #save indicator
        self.grading_4.setAlignment(QtCore.Qt.AlignCenter)
        
        self.strip_grade_1.setText('Nothing Measured')  
        self.strip_grade_1.setStyleSheet("background-color:lightblue;  border: 1px solid black;")  #save indicator
        self.strip_grade_1.setAlignment(QtCore.Qt.AlignCenter)
        
        self.strip_grade_2.setText('Nothing Measured')  
        self.strip_grade_2.setStyleSheet("background-color:lightblue;  border: 1px solid black;")  #save indicator
        self.strip_grade_2.setAlignment(QtCore.Qt.AlignCenter)
        
        self.strip_grade_3.setText('Nothing Measured')  
        self.strip_grade_3.setStyleSheet("background-color:lightblue;  border: 1px solid black;")  #save indicator
        self.strip_grade_3.setAlignment(QtCore.Qt.AlignCenter)
        
        self.strip_grade_4.setText('Nothing Measured')  
        self.strip_grade_4.setStyleSheet("background-color:lightblue;  border: 1px solid black;")  #save indicator
        self.strip_grade_4.setAlignment(QtCore.Qt.AlignCenter)
        
        self.strip_grade_5.setText('Nothing Measured')  
        self.strip_grade_5.setStyleSheet("background-color:lightblue;  border: 1px solid black;")  #save indicator
        self.strip_grade_5.setAlignment(QtCore.Qt.AlignCenter)
        
        self.strip_grade_6.setText('Nothing Measured')  
        self.strip_grade_6.setStyleSheet("background-color:lightblue;  border: 1px solid black;")  #save indicator
        self.strip_grade_6.setAlignment(QtCore.Qt.AlignCenter)
        
        self.strip_grade_7.setText('Nothing Measured')  
        self.strip_grade_7.setStyleSheet("background-color:lightblue;  border: 1px solid black;")  #save indicator
        self.strip_grade_7.setAlignment(QtCore.Qt.AlignCenter)
        
        self.strip_grade_8.setText('Nothing Measured')  
        self.strip_grade_8.setStyleSheet("background-color:lightblue;  border: 1px solid black;")  #save indicator
        self.strip_grade_8.setAlignment(QtCore.Qt.AlignCenter)
        
        self.strip_grade_9.setText('Nothing Measured')  
        self.strip_grade_9.setStyleSheet("background-color:lightblue;  border: 1px solid black;")  #save indicator
        self.strip_grade_9.setAlignment(QtCore.Qt.AlignCenter)
        
        self.strip_grade_10.setText('Nothing Measured')  
        self.strip_grade_10.setStyleSheet("background-color:lightblue;  border: 1px solid black;")  #save indicator
        self.strip_grade_10.setAlignment(QtCore.Qt.AlignCenter)
        
        self.strip_grade_11.setText('Nothing Measured')  
        self.strip_grade_11.setStyleSheet("background-color:lightblue;  border: 1px solid black;")  #save indicator
        self.strip_grade_11.setAlignment(QtCore.Qt.AlignCenter)
        
        self.strip_grade_12.setText('Nothing Measured')  
        self.strip_grade_12.setStyleSheet("background-color:lightblue;  border: 1px solid black;")  #save indicator
        self.strip_grade_12.setAlignment(QtCore.Qt.AlignCenter)
        
        self.strip_grade_13.setText('Nothing Measured')  
        self.strip_grade_13.setStyleSheet("background-color:lightblue;  border: 1px solid black;")  #save indicator
        self.strip_grade_13.setAlignment(QtCore.Qt.AlignCenter)
        
        self.strip_grade_14.setText('Nothing Measured')  
        self.strip_grade_14.setStyleSheet("background-color:lightblue;  border: 1px solid black;")  #save indicator
        self.strip_grade_14.setAlignment(QtCore.Qt.AlignCenter)
        
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
        self.export_4.clicked.connect(self.export_4_click)
        self.measure_5.clicked.connect(self.measure_5_click)
        
    def measure_1_click(self):
        
        self.state_1.setText('Not Saved')  
        self.state_1.setStyleSheet("background-color: yellow;  border: 1px solid black;")
        self.grading_1.setText('Nothing Measured')  
        self.grading_1.setStyleSheet("background-color:lightblue;  border: 1px solid black;")
        
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
        self.plot_1.plot([0,7], [40,40], pen=pg.mkPen('g', width=2))
        self.plot_1.plot([0,7], [30,30], pen=pg.mkPen('g', width=2))
        
        actuator_thickness = float(self.actuator_input_1.text())/1000
        frame_thickness = float(self.frame_input_1.text())/1000
        
        if self.no_frame_1.isChecked():
            frame_thickness = 0
            
        self.inputList = [self.sample_id.text(), self.comments.text(), actuator_thickness, frame_thickness] 
    
        self.names = ['1LBCH','1LF2A','1RBCH','1RF2A','2LBCH','2LF2A','2RBCH','2RF2A','3LBCH','3LF2A','3RBCH','3RF2A','4LBCH','4LF2A','4RBCH','4RF2A']
                    
        if self.BCH_mask_1.isChecked():
            laser_path = '8by12 Bottom Stack'
            self.type = '8by12_'
            expected_output = ['4LBCH','4LF2A','4RBCH','4RF2A','2LBCH','2LF2A','2RBCH','2RF2A','3LBCH','3LF2A','3RBCH','3RF2A','1LBCH','1LF2A','1RBCH','1RF2A']
            progam_number = b'013'
            save_path = self.pathStart + r'Documents\KEYENCE\LJ-X Series Terminal-Software\USB\SD2\lj-x3d\result\SD1_013'
            
        if self.BCH_mask_2.isChecked(): 
            laser_path = '1by4 Bottom Stack'
            self.type = '1by4_'
            expected_output = ['4LBCH','4LF2A','4RBCH','4RF2A','3LBCH','3LF2A','3RBCH','3RF2A','2LBCH','2LF2A','2RBCH','2RF2A','1LBCH','1LF2A','1RBCH','1RF2A']
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
                self.state_1.setText('Warning: Bad Data')  
                self.state_1.setStyleSheet("background-color: red;  border: 1px solid black;")
            if self.data[i+1][0] != "Fail":
                droop = (np.median(self.data[i+1]) + frame_thickness) * 1000
                average_list[1].append(droop)
            else:
                droop = 999
                self.state_1.setText('Warning: Bad Data')  
                self.state_1.setStyleSheet("background-color: red;  border: 1px solid black;")
                
            self.summary.append([BCH, droop])
        
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
        
        for n in range(8):
            for i in range(7):
                self.tableWidget_2.setItem(n+1, i+1, QTableWidgetItem(999))

        self.names = ['1LHW', '1LHCD', '1LHCW', '1LC2A', '1ANC', '1LD', '1LT', '1RHW', '1RHCD', '1RHCW', '1RC2A', '1ANC', '1RD', '1RT',
                      '2LHW', '2LHCD', '2LHCW', '2LC2A', '2ANC', '2LD', '2LT', '2RHW', '2RHCD', '2RHCW', '2RC2A', '2ANC', '2RD', '2RT',
                      '3LHW', '3LHCD', '3LHCW', '3LC2A', '3ANC', '3LD', '3LT', '3RHW', '3RHCD', '3RHCW', '3RC2A', '3ANC', '3RD', '3RT',
                      '4LHW', '4LHCD', '4LHCW', '4LC2A', '4ANC', '4LD', '4LT', '4RHW', '4RHCD', '4RHCW', '4RC2A', '4ANC', '4RD', '4RT']
            
        if self.BCH_mask_3.isChecked():
            laser_path = '8by12 Actuator'
            self.type = '1B_'
            expected_output = ['3LD', '3RD', '3LHW', '3RHW', '3LHCW', '3RHCW', '3LHCD', '3RHCD', '3LC2A', '3RC2A', '3ANC', '3LT', '3RT',
                               '1LD', '1RD', '1LHW', '1RHW', '1LHCW', '1RHCW', '1LHCD', '1RHCD', '1LC2A', '1RC2A', '1ANC', '1LT', '1RT',
                               '4LD', '4RD', '4LHW', '4RHW', '4LHCW', '4RHCW', '4LHCD', '4RHCD', '4LC2A', '4RC2A', '4ANC', '4LT', '4RT',
                               '2LD', '2RD', '2LHW', '2RHW', '2LHCW', '2RHCW', '2LHCD', '2RHCD', '2LC2A', '2RC2A', '2ANC', '2LT', '2RT']
            progam_number = b'014'
            save_path = self.pathStart + r'Documents\KEYENCE\LJ-X Series Terminal-Software\USB\SD2\lj-x3d\result\SD1_014'
            
        if self.BCH_mask_9.isChecked():
            laser_path = '8by12 Actuator'
            self.type = '1D_'
            expected_output = ['3LD', '3RD', '3LHW', '3RHW', '3LHCW', '3RHCW', '3LHCD', '3RHCD', '3LC2A', '3RC2A', '3ANC', '3LT', '3RT',
                               '1LD', '1RD', '1LHW', '1RHW', '1LHCW', '1RHCW', '1LHCD', '1RHCD', '1LC2A', '1RC2A', '1ANC', '1LT', '1RT',
                               '4LD', '4RD', '4LHW', '4RHW', '4LHCW', '4RHCW', '4LHCD', '4RHCD', '4LC2A', '4RC2A', '4ANC', '4LT', '4RT',
                               '2LD', '2RD', '2LHW', '2RHW', '2LHCW', '2RHCW', '2LHCD', '2RHCD', '2LC2A', '2RC2A', '2ANC', '2LT', '2RT']
            progam_number = b''
            save_path = self.pathStart + r'Documents\KEYENCE\LJ-X Series Terminal-Software\USB\SD2\lj-x3d\result\SD1_'
            
        if self.BCH_mask_10.isChecked():
            laser_path = '8by12 Actuator'
            self.type = '1D_'
            expected_output = ['3LD', '3RD', '3LHW', '3RHW', '3LHCW', '3RHCW', '3LHCD', '3RHCD', '3LC2A', '3RC2A', '3ANC', '3LT', '3RT',
                               '1LD', '1RD', '1LHW', '1RHW', '1LHCW', '1RHCW', '1LHCD', '1RHCD', '1LC2A', '1RC2A', '1ANC', '1LT', '1RT',
                               '4LD', '4RD', '4LHW', '4RHW', '4LHCW', '4RHCW', '4LHCD', '4RHCD', '4LC2A', '4RC2A', '4ANC', '4LT', '4RT',
                               '2LD', '2RD', '2LHW', '2RHW', '2LHCW', '2RHCW', '2LHCD', '2RHCD', '2LC2A', '2RC2A', '2ANC', '2LT', '2RT']
            progam_number = b'000'
            save_path = self.pathStart + r'Documents\KEYENCE\LJ-X Series Terminal-Software\USB\SD2\lj-x3d\result\SD1_000'
            
        if self.BCH_mask_4.isChecked():
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
            
            if self.data[i][0] != "Fail":
                temp.append(np.median(self.data[i]))
            else:
                 temp.append(999)
                 self.state_2.setText('Warning: Bad Data')  
                 self.state_2.setStyleSheet("background-color: red;  border: 1px solid black;")
            if self.data[i+1][0] != "Fail":
                temp.append(np.median(self.data[i+1]))
            else:
                 temp.append(999)
                 self.state_2.setText('Warning: Bad Data')  
                 self.state_2.setStyleSheet("background-color: red;  border: 1px solid black;")
            if self.data[i+2][0] != "Fail":
                temp.append(np.median(self.data[i+2]))
            else:
                 temp.append(999)
                 self.state_2.setText('Warning: Bad Data')  
                 self.state_2.setStyleSheet("background-color: red;  border: 1px solid black;")
            if self.data[i+3][0] != "Fail":
                temp.append(np.median(self.data[i+3]))
            else:
                 temp.append(999)
                 self.state_2.setText('Warning: Bad Data')  
                 self.state_2.setStyleSheet("background-color: red;  border: 1px solid black;")
            if self.data[i+4][0] != "Fail":
                temp.append(np.median(self.data[i+4]))
            else:
                 temp.append(999)
                 self.state_2.setText('Warning: Bad Data')  
                 self.state_2.setStyleSheet("background-color: red;  border: 1px solid black;")
            if self.data[i+5][0] != "Fail":
                temp.append(np.median(self.data[i+5]))
            else:
                 temp.append(999)
                 self.state_2.setText('Warning: Bad Data')  
                 self.state_2.setStyleSheet("background-color: red;  border: 1px solid black;")
            if self.data[i+6][0] != "Fail":
                temp.append(np.median(self.data[i+6]))
            else:
                 temp.append(999)
                 self.state_2.setText('Warning: Bad Data')  
                 self.state_2.setStyleSheet("background-color: red;  border: 1px solid black;")
            
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
            
        ht = []
        grade = []
        left = []
        right = []
        
        for i in [sublist[0] for sublist in self.summary]:
            print(i)
            ht.append(i)
            
        for n in range(0,len(ht),2):
            if ht[n] == 999 or ht[n+1] == 999:
                continue
            else:
                grade.append(ht[n])
                grade.append(ht[n+1])
                
                
        left = [value for value in grade[::2]]
        right = [value for value in grade[1::2]]
        difference = np.abs((sum(left) - sum(right))/len(left))
        print(difference)
            
        if difference > 0.05:
            self.grading_2.setText('Grade Fail, HT')  
            self.grading_2.setStyleSheet("background-color: red;  border: 1px solid black;")
            

    def measure_3_click(self):
        self.state_3.setText('Not Saved')  
        self.state_3.setStyleSheet("background-color: yellow;  border: 1px solid black;")  #save indicator
        self.grading_3.setText('Nothing Measured')  
        self.grading_3.setStyleSheet("background-color:lightblue;  border: 1px solid black;")
        
        for n in range(4):
            for i in range(5):
                self.tableWidget_3.setItem(n+1, i+1, QTableWidgetItem(999))
        
        self.names = ['1LFC','1RFC','1LD','1RD','1AW','2LFC','2RFC','2LD','2RD','2AW','3LFC','3RFC','3LD','3RD','3AW','4LFC','4RFC','4LD','4RD','4AW']
                
        if self.BCH_mask_5.isChecked():
            laser_path = '8by12 Orifice'
            self.type = '8by12_'
            progam_number = b'017'
            save_path = self.pathStart + r'Documents\KEYENCE\LJ-X Series Terminal-Software\USB\SD2\lj-x3d\result\SD1_017'
            expected_output = ['4LFC','4RFC','4LD','4RD','4AW','2LFC','2RFC','2LD','2RD','2AW','3LFC','3RFC','3LD','3RD','3AW','1LFC','1RFC','1LD','1RD','1AW']
            
        if self.BCH_mask_6.isChecked(): 
            laser_path = '1by4 Orifice'
            self.type = '1by4_'
            progam_number = b'017'
            save_path = self.pathStart + r'Documents\KEYENCE\LJ-X Series Terminal-Software\USB\SD2\lj-x3d\result\SD1_017'
            expected_output = ['4LFC','4RFC','4LD','4RD','4AW','3LFC','3RFC','3LD','3RD','3AW','2LFC','2RFC','2LD','2RD','2AW','1LFC','1RFC','1LD','1RD','1AW']
                    
        flowplate = False    
        
        self.inputList = [self.sample_id.text(), self.comments.text()] 
        X8060_XYZ_path(progam_number,laser_path,flowplate)
        self.data = readTextFile(save_path,expected_output,self.names)
        
        self.summary = []
        for i in range(0,len(self.data),5):
            self.summary.append([np.median(self.data[i]), np.median(self.data[i+1]), np.median(self.data[i+2]),
                                 np.median(self.data[i+3]), np.median(self.data[i+4])])
        
        for n in range(len(self.summary)):
            for i in range(len(self.summary[n])):
                self.tableWidget_3.setItem(n+1, i+1, QTableWidgetItem('%.3f' % self.summary[n][i]))   
          
        for i in range(len(self.summary)):
            if self.summary[i][2] > 0.05 or self.summary[i][2] < 0.04 or self.summary[i][3] > 0.05 or self.summary[i][3] < 0.04:
                print(self.summary[i][1])
                self.grading_3.setText('Grade Fail - Cavity Depth')  
                self.grading_3.setStyleSheet("background-color: red;  border: 1px solid black;")
                return
            if np.abs(self.summary[i][0] - self.summary[i][1]) > 0.075:
                self.grading_3.setText('Grade Fail - Anchor Symmetry')  
                self.grading_3.setStyleSheet("background-color: red;  border: 1px solid black;")
                return

        self.grading_3.setText('Pass')  
        self.grading_3.setStyleSheet("background-color: green;  border: 1px solid black;")   

    def measure_4_click(self):
        self.grading_4.setText('Nothing Measured')  
        self.grading_4.setStyleSheet("background-color:lightblue;  border: 1px solid black;")
        self.state_4.setText('Not Saved')  
        self.state_4.setStyleSheet("background-color: yellow;  border: 1px solid black;")  #save indicator
        
        for n in range(8):
            for i in range(2):
                self.tableWidget_4.setItem(n+1, i+1, QTableWidgetItem(999))
        
        self.names = ['1LFC','1RFC','2LFC','2RFC','3LFC','3RFC','4LFC','4RFC']
                
        if self.BCH_mask_7.isChecked():
            laser_path = '8by12 Jet Channel'
            self.type = '8by12_'
            progam_number = b'018'
            save_path = self.pathStart + r'Documents\KEYENCE\LJ-X Series Terminal-Software\USB\SD2\lj-x3d\result\SD1_018'
            expected_output = ['4LFC','4RFC','2LFC','2RFC','3LFC','3RFC','1LFC','1RFC']
            
        if self.BCH_mask_8.isChecked():
            laser_path = '1by4 Jet Channel'
            self.type = '1by4_'
            progam_number = b'018'
            save_path = self.pathStart + r'Documents\KEYENCE\LJ-X Series Terminal-Software\USB\SD2\lj-x3d\result\SD1_018'
            expected_output = ['4LFC','4RFC','2LFC','2RFC','3LFC','3RFC','1LFC','1RFC']
            
        flowplate = False    
        
        self.inputList = [self.sample_id.text(), self.comments.text()] 
        X8060_XYZ_path(progam_number,laser_path,flowplate)
        self.data = readTextFile(save_path,expected_output,self.names)
        
        self.summary = []
        for i in range(0,len(self.data),2):
            self.summary.append([np.median(self.data[i]), np.median(self.data[i+1])])
        
        for n in range(len(self.summary)):
            for i in range(len(self.summary[n])):
                self.tableWidget_4.setItem(n+1, i+1, QTableWidgetItem('%.3f' % self.summary[n][i]))
          
        for i in range(len(self.summary)):
            if np.abs(self.summary[i][0] - self.summary[i][1]) > 0.1:
                self.grading_4.setText('Grade Fail - Anchor Symmetry')  
                self.grading_4.setStyleSheet("background-color: red;  border: 1px solid black;")
                return
            
        self.grading_4.setText('Pass')  
        self.grading_4.setStyleSheet("background-color: green;  border: 1px solid black;")   
       
        
    def measure_5_click(self):
        
        self.inputList = [self.sample_id.text(), self.comments.text()] 
        
        self.state_5.setText('Not Saved')  
        self.state_5.setStyleSheet("background-color: yellow;  border: 1px solid black;")  #save indicator

        self.names = ['1LHW', '1LHCD', '1LHCW', '1LC2A', '1ANC', '1LD', '1LT', '1RHW', '1RHCD', '1RHCW', '1RC2A', '1ANC', '1RD', '1RT',
                      '2LHW', '2LHCD', '2LHCW', '2LC2A', '2ANC', '2LD', '2LT', '2RHW', '2RHCD', '2RHCW', '2RC2A', '2ANC', '2RD', '2RT',
                      '3LHW', '3LHCD', '3LHCW', '3LC2A', '3ANC', '3LD', '3LT', '3RHW', '3RHCD', '3RHCW', '3RC2A', '3ANC', '3RD', '3RT',
                      '4LHW', '4LHCD', '4LHCW', '4LC2A', '4ANC', '4LD', '4LT', '4RHW', '4RHCD', '4RHCW', '4RC2A', '4ANC', '4RD', '4RT']
        
        self.summary = []
        temp = []
        pass_list = []
        color_list = []
        
        for m in [7,6,5,4,3,2,1,8,9,10,11,12,13,14]:
        
            if self.BCH_mask_12.isChecked():
                laser_path = '8by12 Actuator'
                self.type = '1B_'
                expected_output = ['3LD', '3RD', '3LHW', '3RHW', '3LHCW', '3RHCW', '3LHCD', '3RHCD', '3LC2A', '3RC2A', '3ANC', '3LT', '3RT',
                                   '1LD', '1RD', '1LHW', '1RHW', '1LHCW', '1RHCW', '1LHCD', '1RHCD', '1LC2A', '1RC2A', '1ANC', '1LT', '1RT',
                                   '4LD', '4RD', '4LHW', '4RHW', '4LHCW', '4RHCW', '4LHCD', '4RHCD', '4LC2A', '4RC2A', '4ANC', '4LT', '4RT',
                                   '2LD', '2RD', '2LHW', '2RHW', '2LHCW', '2RHCW', '2LHCD', '2RHCD', '2LC2A', '2RC2A', '2ANC', '2LT', '2RT']
                progam_number = b'014'
                save_path = self.pathStart + r'Documents\KEYENCE\LJ-X Series Terminal-Software\USB\SD2\lj-x3d\result\SD1_014'
                
             
            flowplate = False    
            
            X8060_XYZ_path(progam_number,laser_path,flowplate)
            self.data = readTextFile(save_path,expected_output,self.names)
        
        
            for i in range(0,len(self.data),7):    
                
                if self.data[i][0] != "Fail":
                    temp.append(np.median(self.data[i]))
                else:
                     temp.append(999)
                     self.state_5.setText('Warning: Bad Data')  
                     self.state_5.setStyleSheet("background-color: red;  border: 1px solid black;")
                     pass_list[m] = 'Warning: Bad Data'
                     color_list[m] = "background-color: red;  border: 1px solid black;"
                     continue
                if self.data[i+1][0] != "Fail":
                    temp.append(np.median(self.data[i+1]))
                else:
                     temp.append(999)
                     self.state_5.setText('Warning: Bad Data')  
                     self.state_5.setStyleSheet("background-color: red;  border: 1px solid black;")
                     pass_list[m] = 'Warning: Bad Data'
                     color_list[m] = "background-color: red;  border: 1px solid black;"
                     continue
                if self.data[i+2][0] != "Fail":
                    temp.append(np.median(self.data[i+2]))
                else:
                     temp.append(999)
                     self.state_5.setText('Warning: Bad Data')  
                     self.state_5.setStyleSheet("background-color: red;  border: 1px solid black;")
                     pass_list[m] = 'Warning: Bad Data'
                     color_list[m] = "background-color: red;  border: 1px solid black;"
                     continue
                if self.data[i+3][0] != "Fail":
                    temp.append(np.median(self.data[i+3]))
                else:
                     temp.append(999)
                     self.state_5.setText('Warning: Bad Data')  
                     self.state_5.setStyleSheet("background-color: red;  border: 1px solid black;")
                     pass_list[m] = 'Warning: Bad Data'
                     color_list[m] = "background-color: red;  border: 1px solid black;"
                     continue
                if self.data[i+4][0] != "Fail":
                    temp.append(np.median(self.data[i+4]))
                else:
                     temp.append(999)
                     self.state_5.setText('Warning: Bad Data')  
                     self.state_5.setStyleSheet("background-color: red;  border: 1px solid black;")
                     pass_list[m] = 'Warning: Bad Data'
                     color_list[m] = "background-color: red;  border: 1px solid black;"
                     continue
                if self.data[i+5][0] != "Fail":
                    temp.append(np.median(self.data[i+5]))
                else:
                     temp.append(999)
                     self.state_5.setText('Warning: Bad Data')  
                     self.state_5.setStyleSheet("background-color: red;  border: 1px solid black;")
                     pass_list[m] = 'Warning: Bad Data'
                     color_list[m] = "background-color: red;  border: 1px solid black;"
                     continue
                if self.data[i+6][0] != "Fail":
                    temp.append(np.median(self.data[i+6]))
                else:
                     temp.append(999)
                     self.state_5.setText('Warning: Bad Data')  
                     self.state_5.setStyleSheet("background-color: red;  border: 1px solid black;")
                     pass_list[m] = 'Warning: Bad Data'
                     color_list[m] = "background-color: red;  border: 1px solid black;"
                     continue
            
            self.summary.append(temp)
            temp = []
                    
            C2A = [] 
            grade = []
            for i in [sublist[3] for sublist in self.summary[m]]:
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
                pass_list[m] = 'Grade Fail - C2A'
                color_list[m] = "background-color: red;  border: 1px solid black;"
                continue
            
            if difference <= 0.1 and difference > 0.05:
                pass_list[m] = 'Grade C'
                color_list[m] = "background-color: yellow;  border: 1px solid black;"
            
            if difference <= 0.05 and difference > 0.025:
                pass_list[m] = 'Grade B'
                color_list[m] = "background-color: green;  border: 1px solid black;"
            
            if difference <= 0.025:
                pass_list[m] = 'Grade A'
                color_list[m] = "background-color: green;  border: 1px solid black;"
                
            ht = []
            grade = []
            left = []
            right = []
            
            for i in [sublist[0] for sublist in self.summary[m]]:
                ht.append(i)
                
            for n in range(0,len(ht),2):
                if ht[n] == 999 or ht[n+1] == 999:
                    continue
                else:
                    grade.append(ht[n])
                    grade.append(ht[n+1])
                    
                    
            left = [value for value in grade[::2]]
            right = [value for value in grade[1::2]]
            difference = np.abs((sum(left) - sum(right))/len(left))
            print(difference)
                
            if difference > 0.05:
                pass_list[m] = 'Grade Fail - HT'
                color_list[m] = "background-color: red;  border: 1px solid black;"
                
        self.strip_grade_1.setText(pass_list[0])  
        self.strip_grade_1.setStyleSheet(color_list[0])  #save indicator
        self.strip_grade_1.setAlignment(QtCore.Qt.AlignCenter)
        
        self.strip_grade_2.setText(pass_list[1])  
        self.strip_grade_2.setStyleSheet(color_list[1])  #save indicator
        self.strip_grade_2.setAlignment(QtCore.Qt.AlignCenter)
        
        self.strip_grade_3.setText(pass_list[2])  
        self.strip_grade_3.setStyleSheet(color_list[2])  #save indicator
        self.strip_grade_3.setAlignment(QtCore.Qt.AlignCenter)
        
        self.strip_grade_4.setText(pass_list[3])  
        self.strip_grade_4.setStyleSheet(color_list[3])  #save indicator
        self.strip_grade_4.setAlignment(QtCore.Qt.AlignCenter)
        
        self.strip_grade_5.setText(pass_list[4])  
        self.strip_grade_5.setStyleSheet(color_list[4])  #save indicator
        self.strip_grade_5.setAlignment(QtCore.Qt.AlignCenter)
        
        self.strip_grade_6.setText(pass_list[5])  
        self.strip_grade_6.setStyleSheet(color_list[5])  #save indicator
        self.strip_grade_6.setAlignment(QtCore.Qt.AlignCenter)
        
        self.strip_grade_7.setText(pass_list[6])  
        self.strip_grade_7.setStyleSheet(color_list[6])  #save indicator
        self.strip_grade_7.setAlignment(QtCore.Qt.AlignCenter)
        
        self.strip_grade_8.setText(pass_list[7])  
        self.strip_grade_8.setStyleSheet(color_list[7])  #save indicator
        self.strip_grade_8.setAlignment(QtCore.Qt.AlignCenter)
        
        self.strip_grade_9.setText(pass_list[8])  
        self.strip_grade_9.setStyleSheet(color_list[8])  #save indicator
        self.strip_grade_9.setAlignment(QtCore.Qt.AlignCenter)
        
        self.strip_grade_10.setText(pass_list[9])  
        self.strip_grade_10.setStyleSheet(color_list[9])  #save indicator
        self.strip_grade_10.setAlignment(QtCore.Qt.AlignCenter)
        
        self.strip_grade_11.setText(pass_list[10])  
        self.strip_grade_11.setStyleSheet(color_list[10])  #save indicator
        self.strip_grade_11.setAlignment(QtCore.Qt.AlignCenter)
        
        self.strip_grade_12.setText(pass_list[11])  
        self.strip_grade_12.setStyleSheet(color_list[11])  #save indicator
        self.strip_grade_12.setAlignment(QtCore.Qt.AlignCenter)
        
        self.strip_grade_13.setText(pass_list[12])  
        self.strip_grade_13.setStyleSheet(color_list[12])  #save indicator
        self.strip_grade_13.setAlignment(QtCore.Qt.AlignCenter)
        
        self.strip_grade_14.setText(pass_list[13])  
        self.strip_grade_14.setStyleSheet(color_list[13])  #save indicator
        self.strip_grade_14.setAlignment(QtCore.Qt.AlignCenter)
        
        
    def export_1_click(self):
        print('Saving Files')
        self.inputList[0] = self.sample_id.text()
        self.inputList[1] = self.comments.text()
        sides = ['1L', '1R', '2L', '2R', '3L', '3R', '4L', '4R']
        file_name = '\BCH&Droop_' + self.type + self.inputList[0] + '.xlsx'
        
        while True:
            try:
                dir_path = QFileDialog.getExistingDirectory(self, 'open a folder', self.pathStart + r'Frore Systems\RnD - Documents\Characterization\Keyence LJXMappingTool\data')
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
        file_name = '\\' + self.inputList[0] + '.xlsx'
        
        while True:
            try:
                dir_path = QFileDialog.getExistingDirectory(self, 'open a folder', self.pathStart + r'Frore Systems\RnD - Documents\Characterization\Keyence LJXMappingTool\data')
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
        self.inputList[0] = self.sample_id.text()
        self.inputList[1] = self.comments.text()
        cell = ['1','2','3','4']
        file_name = '\\' + self.inputList[0] + '.xlsx'
        
        while True:
            try:
                dir_path = QFileDialog.getExistingDirectory(self, 'open a folder', self.pathStart + r'Frore Systems\RnD - Documents\Characterization\Keyence LJXMappingTool\data')
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
        
        inputValues = pd.DataFrame({'names' : ['Sample ID', 'Comments'], 
                                    'values' : self.inputList})
        
        inputValues.to_excel(writer, sheet_name='Data', index=False, startcol=0, startrow=0)
        
        summaryValues = pd.DataFrame({'Cell' : cell, 
                                     'Left Frame to Anchor' : [self.summary[i][0] for i in range(4)],
                                     'Right Frame to Anchor' : [self.summary[i][1] for i in range(4)],
                                     'Left Cavity Depth' : [self.summary[i][2] for i in range(4)],
                                     'Right Cavity Depth' : [self.summary[i][3] for i in range(4)],
                                     'Anchor Width' : [self.summary[i][4] for i in range(4)]
                                     })
        
        summaryValues.to_excel(writer, sheet_name='Data', index=False, startcol=3, startrow=0)
        
        label = []
        for i in range(len(self.data)):
            temp = [self.names[i]] * len(self.data[i])
            label.append(temp)
            
        flat_data = [j for sub in self.data[::5] for j in sub]
        flat_names = [j for sub in label[::5] for j in sub]
        
        LeftF2A= pd.DataFrame({'Left Frame to Anchor' : flat_data, 
                             self.inputList[0] : flat_names})
                  
        LeftF2A.to_excel(writer, sheet_name='Data', index=False, startcol=10, startrow=0)
        
        flat_data = [j for sub in self.data[1::5] for j in sub]
        flat_names = [j for sub in label[1::5] for j in sub]
        
        RightF2A = pd.DataFrame({'Right Frame to Anchor' : flat_data, 
                              self.inputList[0] : flat_names})
        
        RightF2A.to_excel(writer, sheet_name='Data', index=False, startcol=13, startrow=0)
        
        flat_data = [j for sub in self.data[2::5] for j in sub]
        flat_names = [j for sub in label[2::5] for j in sub]
        
        Leftdepth = pd.DataFrame({'Left Cavity Depth' : flat_data, 
                              self.inputList[0] : flat_names})
        
        Leftdepth.to_excel(writer, sheet_name='Data', index=False, startcol=16, startrow=0)
        
        flat_data = [j for sub in self.data[3::5] for j in sub]
        flat_names = [j for sub in label[3::5] for j in sub]
        
        Rightdepth = pd.DataFrame({'Right Cavity Depth' : flat_data, 
                              self.inputList[0] : flat_names})
        
        Rightdepth.to_excel(writer, sheet_name='Data', index=False, startcol=19, startrow=0)
        
        flat_data = [j for sub in self.data[4::5] for j in sub]
        flat_names = [j for sub in label[4::5] for j in sub]
        
        AnchorW = pd.DataFrame({'Anchor Width' : flat_data, 
                              self.inputList[0] : flat_names})
        
        AnchorW.to_excel(writer, sheet_name='Data', index=False, startcol=22, startrow=0)
        
        writer.save()
        print('Finished Saving')
        self.state_3.setText('Saved File')
        self.state_3.setStyleSheet("background-color: green;  border: 1px solid black;") 
        
    def export_4_click(self):
        print('Saving Files')
        self.inputList[0] = self.sample_id.text()
        self.inputList[1] = self.comments.text()
        cell = ['1','2','3','4']
        file_name = '\\' + self.inputList[0] + '.xlsx'
        
        while True:
            try:
                dir_path = QFileDialog.getExistingDirectory(self, 'open a folder', self.pathStart + r'Frore Systems\RnD - Documents\Characterization\Keyence LJXMappingTool\data')
                break
            except PermissionError:
                return None
            
        if path.exists(dir_path + file_name): #testing if file already exists
            self.state_4.setText('Warning: File already exists')
            self.state_4.setStyleSheet("background-color: red;  border: 1px solid black;") 
            print('Could not Save')
            return None
        
        print('**************************')
        writer = pd.ExcelWriter(dir_path + file_name, engine='xlsxwriter')
        
        inputValues = pd.DataFrame({'names' : ['Sample ID', 'Comments'], 
                                    'values' : self.inputList})
        
        inputValues.to_excel(writer, sheet_name='Data', index=False, startcol=0, startrow=0)
        
        summaryValues = pd.DataFrame({'Cell' : cell, 
                                     self.inputList[0] + '_Left Frame to Anchor' : [self.summary[i][0] for i in range(4)],
                                     self.inputList[0] + '_Right Frame to Anchor' : [self.summary[i][1] for i in range(4)],
                                     })
        
        summaryValues.to_excel(writer, sheet_name='Data', index=False, startcol=3, startrow=0)
        
        label = []
        for i in range(len(self.data)):
            temp = [self.names[i]] * len(self.data[i])
            label.append(temp)
            
        flat_data = [j for sub in self.data[::2] for j in sub]
        flat_names = [j for sub in label[::2] for j in sub]
        
        Left = pd.DataFrame({'Left Frame to Anchor' : flat_data, 
                             self.inputList[0] : flat_names})
                  
        Left.to_excel(writer, sheet_name='Data', index=False, startcol=7, startrow=0)
        
        flat_data = [j for sub in self.data[1::2] for j in sub]
        flat_names = [j for sub in label[1::2] for j in sub]
        
        Right = pd.DataFrame({'Right Frame to Anchor' : flat_data, 
                              self.inputList[0] : flat_names})
        
        Right.to_excel(writer, sheet_name='Data', index=False, startcol=10, startrow=0)
        
        writer.save()
        print('Finished Saving')
        self.state_4.setText('Saved File')
        self.state_4.setStyleSheet("background-color: green;  border: 1px solid black;") 
        
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = X8060GUI()
    sys.exit(app.exec_())
    
