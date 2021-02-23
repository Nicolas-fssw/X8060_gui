import glob
import os


def readTextFile(path,expectedOrder,requiredOrder):
    
    dataList = []
    
    filepath = glob.glob(path + '\*.txt')
    latest_file = max(filepath, key=os.path.getmtime)
    file = open(latest_file, 'r')
    raw = file.read()
    raw = raw.replace('\n', ',')
    raw = raw.replace('+', '')
    data = raw.split(',')
    data.pop(-1)
    data = [float(i) for i in data]
    
    
    temp = []
    for i in range(0,len(data),101):
        if data[i] == 0:
            dataList.append(["Fail"])
            continue
        if data[i] != 0:
            count = 0
            total = data[i]
            for n in range(i+1, i + int(data[i]) + 1):
                if data[n] != 0:
                    temp.append(data[n])
                    count = count + 1
            if count < total:
                for i in range(total - count):
                    temp.append(0)
                   
            dataList.append(temp)
            temp = []
    
    temp = []
    for i in requiredOrder:
        for n in expectedOrder:
            if i == n:
                temp.append(dataList[expectedOrder.index(n)])
                
    dataList = temp
    
    return dataList