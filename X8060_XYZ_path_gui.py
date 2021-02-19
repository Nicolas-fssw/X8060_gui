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
            
            
            }
    
    if(flowplate == False):
        pathDict = {
            
            '1by4 Bottom Stack' : [7680, 13920, 29760, 7680, 38160, 29760, 18680, 13920, 29760, 18680, 38160, 29760, 29680, 13920, 29760, 29680, 38160, 29760, 40680, 13920, 29760, 40680, 38160, 29760],
            '8by12 Bottom Stack' : [31000, 17300, 35730, 31000, 38360, 35730, 31000, 33260, 35730, 31000, 56360, 35730, 41590, 17300, 35730, 41590, 38360, 35730, 41590, 33260, 35730, 41590, 56360, 35730], 
            
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
        
        vel = 20
        ######  
        Move_XYZ(TTA,acc,dcl,vel,pathDict[laserpath][i],pathDict[laserpath][i+1],pathDict[laserpath][i+2],delay)
    
        vel = 5
        LJX8060.write(b'T1\r') #Switch to communication mode 
        response = LJX8060.read(12)
        print(response)
    
        Move_XYZ(TTA,acc,dcl,vel,pathDict[laserpath][i+3],pathDict[laserpath][i+4],pathDict[laserpath][i+5],delay)

    
    Home(TTA)
    
    rm.close()
    LJX8060.close()
    
