#!/usr/bin/env python
#version 00.00.04

import sys
import re
import msvcrt
import MySQLdb

end = False
usedb = False
for arg in sys.argv:
  if arg.startswith('-file='):
    fileName = arg.replace('-file=','',1)
  elif arg.startswith('-usedb'):
    usedb = True
  elif arg.startswith('-?'):
    print "python simplifyBom.py [OPTIONS]"
    print "    -?                 Options Help"
    print "    -file=fileName     File name of the original BOM, must end with .csv"
    print "    -usedb             Use DB to look up parts info"
    end = True
if end:
    print "\nPress any key to close window"
    ch = msvcrt.getch()
    sys.exit(0)
#Open file for read
if not re.search(r'.csv$',fileName):
    print "\nFile should be a .csv file."
    print "File name is %s" % fileName
    ch = msvcrt.getch()
    sys.exit(1)
try:
    inFileHndl = open(fileName,'r')
except IOError:
    print "Could not open csv file: %s" % fileName
    print "\nPress any key to close window"
    ch = msvcrt.getch()
    sys.exit(2)
line = inFileHndl.readline()
if (line.split(',')[0] != 'ref'):
    inFileHndl.close()
    print "\nBad input file."
    ch = msvcrt.getch()
    sys.exit(3)
#Walk through the lines in the file and form the dictionary
myDict = {}
dictValue = {}
dictManuf = {}
dictDist = {}
dictDistPN = {}
dictDNP = {}
dictKPartNum = {}
yeswords = ["Yes","yes","YES","Y","y","True","true","TRUE","1","DNP"]
if usedb == False:
  #Old method where manufacturing product ID (4th item) is key
  for line in inFileHndl:
      line = line.replace('\n','')
      splitLine = line.split(',')
      if len(splitLine) >= 4:
          #use manufacturing product ID as key
          tmpKey = str.upper(splitLine[3])
      else:
          tmpKey = 'NoInfo'
      if not myDict.has_key(tmpKey):
          myDict[tmpKey] = []
          if tmpKey != 'NoInfo':
              dictValue[tmpKey] = splitLine[1]
              dictManuf[tmpKey] = splitLine[2]
              dictDist[tmpKey] = splitLine[4]
              dictDistPN[tmpKey] = splitLine[5]
          else:
              dictValue[tmpKey] = splitLine[1]
              dictManuf[tmpKey] = ""
              dictDist[tmpKey] = ""
              dictDistPN[tmpKey] = ""
      myDict[tmpKey].append(str.upper(splitLine[0]))
else:
  #New method, partnum (3rd item) is key, 4th item exists if DNP
  for line in inFileHndl:
      line = line.replace('\n','')
      splitLine = line.split(',')
      dnp = False
      if len(splitLine) >= 3:
          #use manufacturing product ID as key
          tmpKey = splitLine[2]
          #if 4th item exists, component is DNP
          if len(splitLine) == 4:
              if splitLine[3] in yeswords:
                  dnp = True
      else:
          tmpKey = 'NoInfo'
          dnp = True
      if not myDict.has_key(tmpKey):
          myDict[tmpKey] = []
          if tmpKey != 'NoInfo':
              dictValue[tmpKey] = splitLine[1]
              dictKPartNum[tmpKey] = splitLine[2]
          else:
              dictValue[tmpKey] = splitLine[1]
              dictKPartNum[tmpKey] = ""
      myDict[tmpKey].append(str.upper(splitLine[0]))
      dictDNP[splitLine[0]] = dnp
inFileHndl.close()

#Open the database if using the database
if usedb:
    try:
        db=MySQLdb.connect(user='manuf',passwd="mzuuluei",db="partnumdb",host="eng-mysql")
        db.autocommit(True)
        cursor = db.cursor()
    except MySQLdb.Error, e:
        print "Failed to open database."
        print "Error %d: %s" % (e.args[0], e.args[1])
        ch = msvcrt.getch()
        sys.exit(4)

#Open new file for storing output
try:
    outFileHndl = open(fileName.replace(".csv", ".simp.csv"),"wb")
except IOError:
    if usedb:
        db.close()
    print "Could not open .simp.csv file for writing."
    print "\nPress any key to close window"
    ch = msvcrt.getch()
    sys.exit(5)

if usedb == False:
    outFileHndl.write("Part Num,Ref IDs,Num Parts,Value,Manuf,Manuf Part#,Dist,Dist Part#\r\n")
else:
    outFileHndl.write("Part Num,Ref IDs,Value,Cost,Num Parts,Tot Cost,JPartNum,KPartNum,Dist1,Dist1 Part#,Dist2,Dist2 Part#,Dist3,Dist3 Part#\r\n")
#Walk through each dictionary entry, and munge lists
index = 0
numPrefix = 0
totCost = 0.0
dnpRefDesStr = ""
for key, refDesList in myDict.iteritems():
    sortRefDesList = sorted(refDesList)
    prefixList = []
    totRefNumList = []
    currPrefix = ""
    for currRefDes in sortRefDesList:
        #This regexp removes all digits to the end of line leaving only the prefix
        nextPrefix = re.sub(r'\d*$',"",currRefDes)
        if currPrefix != nextPrefix:
            if currPrefix != "":
                #totRefNumList is list of lists of ref numbers with same prefix
                totRefNumList.append(refNumList)
            #Set up current prefix
            currPrefix = nextPrefix
            #Put new prefix in the prefixList
            prefixList.append(currPrefix)
            #Keep number of prefixes
            numPrefix += 1
            #Start new ref number list for this prefix
            refNumList = []
        #currNum is reference designator without the prefix
        currNum = int(currRefDes.replace(currPrefix,""))
        #Add the currNum to the refNumList which is list of all refdes with same prefix but prefix stripped
        refNumList.append(currNum)
    #Add last refNumList to totRefNumList since there won't be mismatch on prefix
    totRefNumList.append(refNumList)
    prefixIndex = 0
    numParts = 0
    totRefDesStr = ""
    numParts = 0
    #prefixList is list of all unique prefixes in design
    #Form groups so C1,C2,C3 is C1-C3, and individual refdes are listed properly
    for currPrefix in prefixList:
        #refNumList is sorted as an integer so 100 is after 2, not before.
        refNumList = sorted(totRefNumList[prefixIndex])
        refDesStr = currPrefix + str(refNumList[0])
        lastNum = -10
        printedDash = False
        #walk through sorted reference number list
        for currNum in refNumList:
            #See if this is last ref des + 1
            if (currNum == lastNum + 1):
                if printedDash:
                    #change ending reference designator for group
                    refDesStr = refDesStr.replace(currPrefix + str(lastNum), currPrefix + str(currNum))
                else:
                    #create the dash group (print - and next reference designator)
                    printedDash = True
                    refDesStr += ("-" + currPrefix + str(currNum))
            else:
                printedDash = False
                if lastNum != -10:
                    #if this isn't the first refdes, print a space to separate them
                    refDesStr += (" " + currPrefix + str(currNum))
            if usedb == False:
                numParts += 1
            else:
                #Check if this part is a DNP
                if dictDNP[currPrefix + str(currNum)] == False:
                    numParts += 1
                else:
                    if dnpRefDesStr != "":
                        dnpRefDesStr = dnpRefDesStr + " " + currPrefix + str(currNum)
                    else:
                        dnpRefDesStr = currPrefix + str(currNum)
                        
            lastNum = currNum
        #form total refdes string
        if totRefDesStr != "":
            totRefDesStr = totRefDesStr + " " + refDesStr
        else:
            totRefDesStr = refDesStr
        #move to next prefix index
        prefixIndex += 1
    index += 1
    if usedb == False:
        outFileHndl.write(str(index) + "," + totRefDesStr + "," + str(numParts) + "," + dictValue[key] + "," + \
            dictManuf[key] + "," + key + "," + dictDist[key] + "," + dictDistPN[key] + "\r\n")
    else:
        #lookup the information from the database
        try:
            sql = """SELECT jpartnum, dist, distpartnum, price FROM partnumtbl WHERE kpartnum = '%s' ORDER BY price"""
            numRows = cursor.execute(sql % (dictKPartNum[key]))
            if numRows == 0:
                #Row does not exist, so write appropriate info to simplified BOM
                outFileHndl.write(str(index) + "," + totRefDesStr + "," + dictValue[key] + ",0.00," + str(numParts) + ",0.00,," + \
                    dictKPartNum[key] + ",PartNotInDB\r\n")
            else:
                rownum = 0
                #Only print first three distributors
                while (rownum < numRows) and (rownum < 3):
                    row = cursor.fetchone()
                    #If first row, print beginning info
                    if (rownum == 0):
                        outFileHndl.write(str(index) + "," + totRefDesStr + "," + dictValue[key] + "," + \
                            ("%.3f" % row[3]) + "," + str(numParts) + "," + ("%.3f" % (row[3] * numParts)) + "," + \
                            row[0] + "," + dictKPartNum[key])
                        totCost = totCost + (row[3] * numParts)
                    outFileHndl.write("," + row[1] + "," + row[2])
                    rownum += 1
                outFileHndl.write("\r\n")
        except MySQLdb.Error, e:
            outFileHndl.close()
            db.close()
            print "DB Error %d: %s" % (e.args[0], e.args[1])
            print "\nPress any key to close window"
            ch = msvcrt.getch()
            sys.exit(6)
#If used the database, print the total cost at the end of the table, and close the database
if usedb:
    outFileHndl.write(",%s,,,,%.3f\r\n" % (dnpRefDesStr,totCost))
    db.close()
outFileHndl.close();
