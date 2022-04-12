import os
import shutil
import time

replaceChars = {'&amp;': '&'}
receivePath = './receive'
backupPath = './receive/pythonBackup'
timeSleep = 60 #second

def __createLogPath__():
    logPath = 'log/' + time.strftime("%Y%m")
    try:
        os.makedirs(logPath)
    except:
        __writeLog__("Log folder existed")
        
def __writeLog__(logMsg):  
    logPath = 'log/' + time.strftime("%Y%m")
    fileName = time.strftime("%Y%m%d") + ".log"
    logTime = time.strftime("%Y-%m-%d %H:%M:%S")
    logFile = open(os.path.join(logPath, fileName), "a+", encoding='utf-8')
    print("[" + logTime + "]---[" + logMsg + "]")
    logFile.write("[" + logTime + "]---[" + logMsg + "]\n")
    logFile.close()      
    
def __checkThenBackup__():
    global replaceChars
    global receivePath 
    global backupPath 
    path, dirs, files = next(os.walk(receivePath))
    allWrong = []
    for file in files:
        if file.endswith('.csv') and not file.endswith('tmp.csv'): #check all file .csv
            try:
                with open(os.path.join(receivePath, file), "r", encoding='utf-8') as readFile: #read file
                    content = readFile.readlines()
                    readFile.close()
            except:
                continue
            eachLine= 0
            for line in content:
                checkVar = True
                wrongDetails = []
                for wrongKey in replaceChars.keys():
                    if line.find(wrongKey) != -1: #found
                        checkVar = False #detect wrong character
                        shutil.copyfile(os.path.join(receivePath, file), os.path.join(backupPath, file)) #backup
                        wrongDetails.append(file)     #0
                        wrongDetails.append(eachLine) #1
                        wrongDetails.append(line)     #2 
                        wrongDetails.append(wrongKey) #3    #grep each wrong line
                        allWrong.append(wrongDetails)       #grep all wrong lines
                        checkVar = True
                eachLine += 1 
    return allWrong
    
#if __name__ == "__main__":
def __main__():
    __createLogPath__()
    while True:
        allWrong = __checkThenBackup__()
        if allWrong == None:
            break
        for wrongDetails in allWrong:
            __writeLog__(str(wrongDetails))
            with open(os.path.join(receivePath, wrongDetails[0]), "r", encoding='utf-8') as readFile: #read file
                content = readFile.readlines()
                readFile.close()
            eachLine= 0
            with open(os.path.join(receivePath, wrongDetails[0]), 'w', encoding='utf-8') as reWrite: #fix file
                for line in content:
                    if eachLine != wrongDetails[1]:
                        reWrite.write(line)
                    else:
                        reWrite.writelines(line.replace(wrongDetails[3], replaceChars[wrongDetails[3]])) #remove wrong char
                    eachLine += 1
                reWrite.close()
        print("[" + time.strftime("%Y-%m-%d %H:%M:%S") + "]---No error found. Please wait "+ str(timeSleep) +"s for the next scan")
        time.sleep(timeSleep)