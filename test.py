import os
import gzip
from socket import *
from time import sleep
import threading

rootDirectory="./"
serverPort = 1246

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

		if(requestheader[1] not in  os.listdir()):
		 	connectionSocket.send('HTTP/1.1 404 FILE NOT FOUND\n'.encode())
		if(requestheader[1]=="/kk.html"):	
			connectionSocket.send('HTTP/1.0 200 OK\n'.encode())
			connectionSocket.send('Content-Type: text/html\n'.encode())
			connectionSocket.send('\n'.encode())
			send_file(connectionSocket,requestheader[1])
		elif(requestheader[1].endswith("png") or requestheader[1].endswith("jpg") or requestheader[1].endswith("jpeg")):
			try:
				#compress image
				if not (requestheader[1][1:]+'.gz' in os.listdir()):
					with open(requestheader[1][1:],"rb") as img:
						data = img.read()
					bindata = bytearray(data)
					with gzip.open(requestheader[1][1:]+'.gz', "wb") as f:
						f.write(bindata)
				
				#read compressed image
				with gzip.open(requestheader[1][1:]+'.gz', "rb") as imageFile:
					s=imageFile.read()
				
				connectionSocket.send('HTTP/1.0 200 OK\n'.encode())
				connectionSocket.send('Content-Type: image/png\n'.encode())
				connectionSocket.send('\n'.encode())
				connectionSocket.send(s)
			except:
				pass

try:
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
except KeyboardInterrupt:
	serverSocket.shutdown(SHUT_RDWR)
	serverSocket.close()
