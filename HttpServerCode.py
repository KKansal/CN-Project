import os
import sys
import gzip
from socket import *
import threading
import functools

rootDirectory="/home/keshavk/Documents/CN Project/Templates1"
serverPort = 12000

serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(1)

supportedFileTypes=['html','css','eot','svg','ttf','woff','js']
supportedImageFiles=['png','jpeg','jpg']

print("The server is ready to receive at Port",serverPort)
print("The root Root Directory is",rootDirectory)


def send_file(connectionSocket,filename):
	print("opening -",filename)
	fp = open(rootDirectory +filename,"r")
	lines = fp.readlines()
	for i in lines:
		connectionSocket.send(i.encode())



def serve_request(connectionSocket,requestheader):
	if(requestheader[0]=="GET"):
		filepath=functools.reduce(lambda x,y:x+ '/' + y,requestheader[1].split('/')[:-1])
		if(len(filepath)==0):
			filepath='/'
		requestedfile=requestheader[1].split('/')[-1]

		if(len(requestedfile)==1):
			requestedfile="index.html"


		if(requestedfile not in  os.listdir(rootDirectory + filepath)):
		 	connectionSocket.send('HTTP/1.0 404 FILE NOT FOUND\n'.encode())
		 	print("File Not found - ",requestedfile)
		 	

		elif(requestheader[1].split('.')[-1] in supportedFileTypes):	
			connectionSocket.send('HTTP/1.0 200 OK\n'.encode())
			connectionSocket.send(('Content-Type: text/' + requestheader[1].split('.')[-1] + '\n').encode())
			connectionSocket.send('\n'.encode())
			send_file(connectionSocket,filepath+ "/"+ requestedfile)

		elif(requestheader[1].split('.')[-1] in supportedImageFiles):
			try:
				#compress image
				if not (requestedfile+'.gz' in os.listdir(rootDirectory + filepath)):
				# if not (requestheader[1] + '.gz' in os.listdir()):	
					with open(rootDirectory +filepath + '/'+ requestedfile,"rb") as img:
						data = img.read()

					bindata = bytearray(data)
					with gzip.open(rootDirectory + filepath + '/' + requestedfile +'.gz', "wb") as f:
						f.write(bindata)
				
				#read compressed image
				with gzip.open(rootDirectory + filepath + '/' + requestedfile + '.gz', "rb") as imageFile:
				# with gzip.open(requestheader[1][1:]+'.gz', "rb") as imageFile:
					s=imageFile.read()
				
				connectionSocket.send('HTTP/1.0 200 OK\n'.encode())
				connectionSocket.send(('Content-Type: image/' + requestheader[1].split('.')[-1] + '\n').encode())
				connectionSocket.send('\n'.encode())
				connectionSocket.send(s)

			except:
				print("File Read Error",rootDirectory + "/"+ filepath)
		else:
			print("File not found")
			connectionSocket.send("HTTP/1.0 500 Server Error- The server is capable of handling GET request".encode())
			#todo Server Error



try:
	while True :
		connectionSocket,ipaddr = serverSocket.accept()
		print("Connection accepted from- ",ipaddr,'\n')
		sentence = connectionSocket.recv(1024)
		httprequest = sentence.decode()
		print(httprequest)
		httprequest=httprequest.split('\r\n')
		for i in range(len(httprequest)):
			httprequest[i]=httprequest[i].split()

		t1=threading.Thread(target=serve_request,args=(connectionSocket,httprequest[0],))
		t1.start()
		t1.join()
		connectionSocket.shutdown(SHUT_WR)
		connectionSocket.close()
		print("Connection Closed")

except KeyboardInterrupt:
	print("Server Error")
	serverSocket.shutdown(SHUT_RDWR)
	serverSocket.close()
