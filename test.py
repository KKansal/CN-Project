import os
from socket import *
from time import sleep
import threading

rootDirectory="/home/keshavk/Documents/CN Project/Templates1/"
serverPort = 12000

serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(1)
print("The server is ready to receive")


def send_file(connectionSocket,filename):
	fp = open(rootDirectory + filename,"r")
	lines = fp.readlines()
	for i in lines:
		connectionSocket.send(i.encode())

def serverequest(connectionSocket,requestheader):
	if(requestheader[0]=="GET"):
		if(len(requestheader[1])==1):
			requestheader[1]="index.html"

		# if(requestheader[1] not in  os.listdir(rootDirectory)):
		# 	connectionSocket.send('HTTP/1.1 404 FILE NOT FOUND\n'.encode())
		# else:
		connectionSocket.send('HTTP/1.0 200 OK\n'.encode())
		connectionSocket.send('Content-Type: text/html\n'.encode())
		connectionSocket.send('\n'.encode())
		send_file(connectionSocket,requestheader[1])
		# connectionSocket.send("""
	 #    	<html>
	 #    	<body>
	 #    	<h1>Hello KK</h1> this is my server!
	 #    	</body>
	 #    	</html>""".encode())


while True :
	connectionSocket, addr = serverSocket.accept()
	print("Connection accepted")
	sentence = connectionSocket.recv(1024)
	httprequest = sentence.decode()
	print(httprequest)
	httprequest=httprequest.split('\r\n')
	for i in range(len(httprequest)):
		httprequest[i]=httprequest[i].split()

	t1=threading.Thread(target=serverequest,args=(connectionSocket,httprequest[0],))
	t1.start()
	serverequest(connectionSocket,httprequest[0])
	t1.join()
	connectionSocket.shutdown(SHUT_WR)
	connectionSocket.close()
	print("Connection Closed")
serverSocket.shutdown(SHUT_RDWR)
serverSocket.close()

