from ast import Not
from operator import not_
from pathlib import Path
from socket import close #to check file exist
import config

import os #to get file base name

class XmlEdit:
    fromColumn = -1
    toColumn = -1
    baseFileAdress = ""
    columnChar = ""

def getFile(fileName):
    try:
        file = open(fileName, config.READ)
        return file
    except :
        print(f"File '{fileName}' not found.")
        return None

def runFileEdit(xmlEditClass, filePath):
    fromFile = getFile(filePath)
    if getFile == None:
        print("Error: unknown problem with opening file: " + filePath)
        return
    newFilePath = os.path.dirname(filePath) + "\\copy_" + os.path.basename(filePath)
    #print(os.path.dirname(filePath))
    copiedFile = open(newFilePath, config.APPEND)
    if copiedFile == None:
        getFile.close()
        return
    print("New copy created: " + newFilePath)
    intFromColumn = int(xmlEditClass.fromColumn)
    intToColumn = int(xmlEditClass.toColumn)
    lineNum = 0
    print("editing start...")
    for line in fromFile:
        actualColumn = 1
        lineToCopy = ""
        for char in line:
            if char == xmlEditClass.columnChar:
                if not (actualColumn >= intFromColumn and actualColumn <= intToColumn):
                    lineToCopy += char
                actualColumn += 1
            else:
                if actualColumn >= intFromColumn and actualColumn <= intToColumn:
                    continue #skip this column
                else:
                    lineToCopy += char
        copiedFile.write(lineToCopy)
        lineNum += 1
        if lineNum % 1000 == 0:
            print("...editing continue on line: " + str(lineNum))
    print("editing end on line: " + str(lineNum) + "\n")
    fromFile.close()
    copiedFile.close()

def getUserInputs(xmlEditClass):
    fileToCheck = None
    userInput = ""
    filePathToImport = ""

    while True:
        if  filePathToImport == "":
            print("enter the path of file with extension included")
            #get import path from user
            filePathToImport = input()
            #fileToCheck = getFile(filePathToImport)
            if not os.path.exists(filePathToImport):
                 #file not exist or wrong input
                print("Wrong input: The file at the specified address does not exist")
                filePathToImport = ""
            else: continue #right file input
                
        elif len(xmlEditClass.columnChar) != 1:
            print("enter the column character, eg. ; or | or , etc.")
            #get import path from user
            xmlEditClass.columnChar = input()
            if len(xmlEditClass.columnChar) != 1: 
                print("Wrong input: It is allowed to add only one character")
                xmlEditClass.columnChar = ""
            else: continue #right input
        elif xmlEditClass.fromColumn == config.DEFAULT_COLUMN_NUM:
            print("Delete from column ...? (first columnt = 1,input included)")
            checkFromColumn= input()
            if not checkFromColumn.isdigit():
                print("Wrong input: input have to be a positive number")
            else: #right input
                xmlEditClass.fromColumn = int(checkFromColumn)
                continue 
        elif xmlEditClass.toColumn == config.DEFAULT_COLUMN_NUM:
            print("Delete to column ...? (first columnt = 1, input included)")
            checkToColumn = input()
            if  not checkToColumn.isdigit():
                print("Wrong input: input have to be a positive number")
                continue
            intToColumn = int(checkToColumn)
            if  intToColumn < xmlEditClass.fromColumn:
                print("Wrong input: delete \'to column\' have to be greater than \'from column\'")
                xmlEditClass.toColumn = config.DEFAULT_COLUMN_NUM
            else: #right input
                xmlEditClass.toColumn = intToColumn
                continue 
        else: #all conditions is confirmed
            runFileEdit(xmlEditClass, filePathToImport)
            break