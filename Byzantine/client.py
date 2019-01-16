#!usr/bin/python
from socket import *
import math
import time
from random import randint
host = 'localhost' # '127.0.0.1' can also be used
port = 8080

index,noL,noT,command,defVal = -1,-1,-1,-1,-1

isT = -1
sock = socket()
sock.connect((host, port)) #Connect takes tuple of host and port

noOP = []
noIP = []
last = -1
while 1:
    data = sock.recv(1024)
    print (data)
    # print "\n"

    dataArr = data.split()
    keyWord = dataArr[0]

    if keyWord == "TRAITOR":
        isT = 1
    elif keyWord == "INDEX":
        index = int(dataArr[1])
    elif keyWord == "COMMAND":
        noL = int(dataArr[1])
        noT = int(dataArr[2])
        command = int(dataArr[4])
        defVal = command
        # path = dataArr[3]
        # pathLen = len(dataArr[3])
        # for i in range(noT - pathLen):
        for j in range(noL):
            if j != index:

                if isT==1:
                    random = randint(0,1)
                    time.sleep(0.5)
                    sock.send("INPUT C|%s %s %s" %(index,random,j))
                else:
                    time.sleep(0.5)
                    sock.send("INPUT C|%s %s %s" %(index,command,j))


    elif keyWord == "INPUT":
        # print "dataArr is: %s" %dataArr[1]
        noIP.append(dataArr[1])
        if len(noIP) == noL-1:
            for val in noIP:
                path = val.split("|")
                last = path[len(path)-1]
                # print last
                if isT==1:
                    # print "isT is: %s"%isT
                    # print "Running traitor"
                    time.sleep(0.5)
                    sock.send("OUTPUT %s %s" %(randint(0,1),last))
                else:
                    time.sleep(0.5)
                    sock.send("OUTPUT %s %s" %(command,last))

    elif keyWord == "OUTPUT":
        # try:
        #     if last!=-1:

        # print "DataArr is: %s"%dataArr
        noOP.append(dataArr[1])
        # print "OP is: %s" %noOP
        if len(noOP) == noL-1:
            time.sleep(5)
            if noOP.count("1")>noOP.count("0"):
                sock.send("MAJORITY 1")
                print ("MAJORITY 1")
            else:# noOP.count("1")<noOP.count("0"):
                sock.send("MAJORITY 0")
                print ("MAJORITY 0")
            # else:
            #     sock.send("MAJORITY %s"%defVal)
#     print "MAJORITY %s" %defVal