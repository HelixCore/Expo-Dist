import time
from socket import *
from _thread import *
import math
from random import randint

GlobalReq = 0
q={}

# Defining server address and port
host = ''  #'localhost' or '127.0.0.1' or '' are all same
port = 8080 #Use port > 1024, below it all are reserved



# print "Enter"
print ("# of L, # of T, isTraitor?, Command\n")
# s = input().split()
# s=[int(x) for x in s]
noL,noT,isT,command = 5,1,0,1
noM = []

ran = []  ## List to store the Random Traitors
for i in range(noT-isT):
    while True:
        x = randint(0,noL-1)
        if x not in ran:
            ran.append(x)
            break



#Creating socket object
sock = socket()
#Binding socket to a address. bind() takes tuple of host and port.
sock.bind((host, port))
#Listening at the address
sock.listen(noL) #5 denotes the number of clients can queue

def clientthread(conn):

     while True:
         data = conn.recv(1024) # 1024 stands for bytes of data to be received
         print (data)
         #time.sleep(0.05)
         dataArr = data.split()
         keyWord = dataArr[0]
        #  print dataArr
         if keyWord == "INPUT":
             path = dataArr[1]
             cmd = dataArr[2]
             child = connList[int(dataArr[3])]
             child.send( ("INPUT %s %s" %(path, cmd)).encode())  

         if keyWord == "OUTPUT":
            #  print "dataArr is: %s"%dataArr
             cmd = dataArr[1]
             child = connList[int(dataArr[2])]
             child.send( ("OUTPUT %s" %(cmd)).encode() )

         if keyWord == "MAJORITY":
             noM.append(dataArr[1])
             if(len(noM) == noL):
                 if noM.count("1")>noM.count("0"):
                     print ("Final output: 1")
                 else:
                     print ("Final output: 0")


connList = []
while True:
    conn, addr = sock.accept()
    connList.append(conn)  ## List to store the conn objects
    start_new_thread(clientthread,(conn,)) #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    print ("Connected to: %s" %(len(connList)-1))
    if len(connList)==noL:
        break

for x in range(noL):
    connList[x].send( ("INDEX %s"%x).encode() )
    time.sleep(0.5)

for i in ran:
    connList[i].send( ("TRAITOR %s"%i).encode() ) 
    time.sleep(0.5)


#starting algorithm
if isT==1:
    for x in range(noL):
        time.sleep(1)
        connList[x].send( ("COMMAND %s %s C %s" %(noL, noT, randint(0,1))).encode() )
else:
    for x in range(noL):
        time.sleep(1)
        connList[x].send( ("COMMAND %s %s C %s" %(noL, noT, command)).encode() )

while 1:
    a=1