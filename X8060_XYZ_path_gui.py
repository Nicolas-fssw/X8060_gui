# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 13:09:26 2021

@author: Nicolas Madhavapeddy
"""

from xyz_functions_gui import Servo_on, Home, Move_XYZ
import time
import serial
import pyvisa as visa

def X8060_XYZ_path(programNumber, laserpath, flowplate):
    
    if(flowplate == True):
        pathDict = {
            '8by12 Bottom Stack' : [121000, 25300, 17610, 121000, 46360, 17610, 121000, 41260, 17610, 121000, 64360, 17610, 131590, 25300, 17610, 131590, 46360, 17610, 131590, 41260, 17610, 131590, 64360, 17610], 
            
            }
    
    if(flowplate == False):
        pathDict = {
            
            '8by12 Bottom Stack' : [177760, 44635, 31920, 177760, 67570, 31920, 177760, 60605, 31920, 177760, 83540, 31920, 188650, 44635, 31920, 188650, 67570, 31920, 188650, 60605, 31920, 188650, 83540, 31920],
            '1by4 Bottom Stack'  : [166870, 29365, 31920, 166870, 52300, 31920, 177760, 29365, 31920, 177760, 52300, 31920, 188650, 29365, 31920, 188650, 52300, 31920, 199540, 29365, 31920, 199540, 52300, 31920],
            
            '8by12 Actuator' : [177760, 44635, 31920, 177760, 67570, 31920, 177760, 60605, 31920, 177760, 83540, 31920, 188650, 44635, 31920, 188650, 67570, 31920, 188650, 60605, 31920, 188650, 83540, 31920,], 
            '1by4 Actuator' : [166870, 29365, 31920, 166870, 52300, 31920, 177760, 29365, 31920, 177760, 52300, 31920, 188650, 29365, 31920, 188650, 52300, 31920, 199540, 29365, 31920, 199540, 52300, 31920],
            
            '8by12 Jet Channel' : [177760, 44635, 31920, 177760, 67570, 31920, 177760, 60605, 31920, 177760, 83540, 31920, 188650, 44635, 31920, 188650, 67570, 31920, 188650, 60605, 31920, 188650, 83540, 31920,],
            '1by4 Jet Channel' : [166870, 29365, 31920, 166870, 52300, 31920, 177760, 29365, 31920, 177760, 52300, 31920, 188650, 29365, 31920, 188650, 52300, 31920, 199540, 29365, 31920, 199540, 52300, 31920],
            
            '8by12 Orifice' : [177760, 44635, 31920, 177760, 67570, 31920, 177760, 60605, 31920, 177760, 83540, 31920, 188650, 44635, 31920, 188650, 67570, 31920, 188650, 60605, 31920, 188650, 83540, 31920,],
            '1by4 Orifice' : [166870, 29365, 31920, 166870, 52300, 31920, 177760, 29365, 31920, 177760, 52300, 31920, 188650, 29365, 31920, 188650, 52300, 31920, 199540, 29365, 31920, 199540, 52300, 31920]
            }
    

    LJX8060 = serial.Serial(
                        port='COM7',
                        baudrate=115200,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=0.5, 
                        xonxoff=False, 
                        rtscts=False, 
                        write_timeout=None, 
                        dsrdtr=False, 
                        inter_byte_timeout=None, 
                        exclusive=None
                        )
    
    print(LJX8060.name)
    
    LJX8060.write(b'R0\r') #Switch to communication mode
    response = LJX8060.read(12)
    print(response)
    
    LJX8060.write(b'PW,1,' + programNumber + b'\r') #Switch to BCH Program
    response = LJX8060.read(12)
    print(response)
    
    LJX8060.write(b'TE,1\r') #Switch to communication mode 
    response = LJX8060.read(12)
    print(response)
     
    
    rm = visa.ResourceManager()
    TTA = rm.open_resource('COM4') 
    Servo_on(TTA)
    Home(TTA)
    time.sleep(1)
    
    acc = 20
    dcl = 20
    delay = 0.1
      
    for i in range(0,len(pathDict[laserpath]),6):
        
        vel = 150
        ######  
        Move_XYZ(TTA,acc,dcl,vel,pathDict[laserpath][i],pathDict[laserpath][i+1],pathDict[laserpath][i+2],delay)
    
        vel = 19
        LJX8060.write(b'T1\r') #Switch to communication mode 
        Move_XYZ(TTA,acc,dcl,vel,pathDict[laserpath][i+3],pathDict[laserpath][i+4],pathDict[laserpath][i+5],delay)

     
    #time.sleep(1)   
    vel = 150
    Move_XYZ(TTA,acc,dcl,vel,10,10,10,delay)
    Home(TTA)
    
    rm.close()
    LJX8060.close()
    
def X8060_strip_path(programNumber, laserpath, iteration):
    
    
    pathDict = {
                '2x7 12x8' : [19515, 81720, 31920, 19515, 104655, 31920, 19515, 97690, 31920, 19515, 120625, 31920, 30405, 81720, 31920, 30405, 104655, 31920, 30405, 97690, 31920, 30405, 120625, 31920],
                '3x4 1x4' : [15840,91000,31920,15840,113935,31920,26730,91000,31920,26730,113935,31920,37620,91000,31920,37620,113935,31920,48510,91000,31920,48510,113935,31920]
               }
    
    
    LJX8060 = serial.Serial(
                        port='COM7',
                        baudrate=115200,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=0.5, 
                        xonxoff=False, 
                        rtscts=False, 
                        write_timeout=None, 
                        dsrdtr=False, 
                        inter_byte_timeout=None, 
                        exclusive=None
                        )
    
    print(LJX8060.name)
    
    LJX8060.write(b'R0\r') #Switch to communication mode
    response = LJX8060.read(12)
    print(response)
    
    LJX8060.write(b'PW,1,' + programNumber + b'\r') #Switch to BCH Program
    response = LJX8060.read(12)
    print(response)
    
    LJX8060.write(b'TE,1\r') #Switch to communication mode 
    response = LJX8060.read(12)
    print(response)
     
    
    rm = visa.ResourceManager()
    TTA = rm.open_resource('COM4') 
    Servo_on(TTA)
    if iteration == 1:
        Home(TTA)
        time.sleep(1)
     
        
    if laserpath ==  '2x7 12x8':
        if iteration > 1 and iteration < 8:
            for t in range(0,24,3):
                pathDict[laserpath][t] = pathDict[laserpath][t] + 26000 * (iteration-1)
                
        if iteration > 7:
            for t in range(0,24,3):
                pathDict[laserpath][t] = pathDict[laserpath][t] + 26000 * (iteration-8)
            for t in range(1,24,3):
                pathDict[laserpath][t] = pathDict[laserpath][t] - 36300
                
    if laserpath ==  '3x4 1x4':
        if iteration > 1 and iteration < 5:
            for t in range(0,24,3):
                pathDict[laserpath][t] = pathDict[laserpath][t] + 47000 * (iteration-1)
                
        if iteration > 4 and iteration < 9:
            for t in range(0,24,3):
                pathDict[laserpath][t] = pathDict[laserpath][t] + 47000 * (iteration-5)
            for t in range(1,24,3):
                pathDict[laserpath][t] = pathDict[laserpath][t] - 20700
                
        if iteration > 8:
            for t in range(0,24,3):
                pathDict[laserpath][t] = pathDict[laserpath][t] + 47000 * (iteration-9)
            for t in range(1,24,3):
                pathDict[laserpath][t] = pathDict[laserpath][t] - 20700 * 2
        
        
    acc = 20
    dcl = 20
    delay = 0.1
      
    for i in range(0,len(pathDict[laserpath]),6):
        
        vel = 150
        ######  
        Move_XYZ(TTA,acc,dcl,vel,pathDict[laserpath][i],pathDict[laserpath][i+1],pathDict[laserpath][i+2],delay)
    
        vel = 19
        LJX8060.write(b'T1\r') #Switch to communication mode 
        Move_XYZ(TTA,acc,dcl,vel,pathDict[laserpath][i+3],pathDict[laserpath][i+4],pathDict[laserpath][i+5],delay)

    if laserpath ==  '2x7 12x8':
        if iteration == 14:  
            vel = 150
            Move_XYZ(TTA,acc,dcl,vel,10,10,10,delay)
            Home(TTA) 
            
    if laserpath ==  '3x4 1x4':
        if iteration == 12:  
            vel = 150
            Move_XYZ(TTA,acc,dcl,vel,10,10,10,delay)
            Home(TTA) 
    
    time.sleep(0.8)
    rm.close()
    LJX8060.close()
