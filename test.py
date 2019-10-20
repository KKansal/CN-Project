from socket import *
from time import sleep
rootDirectory="\\"
serverPort = 12000

serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(1)
print("The server is ready to receive")

def serverequest(connectionSocket,requestheader):
	if(requestheader[0]=="GET"):
		connectionSocket.send('HTTP/1.0 200 OK\n'.encode())
		connectionSocket.send('Content-Type: text/html\n'.encode())
		connectionSocket.send('\n'.encode())
		connectionSocket.send("""
	    	<html>
	    	<body>
	    	<h1>Hello KK</h1> this is my server!
	    	</body>
	    	</html>""".encode())



connectionSocket, addr = serverSocket.accept()
print("Connection accepted")
sentence = connectionSocket.recv(1024)
httprequest = sentence.decode()
print(httprequest)
httprequest=httprequest.split('\r\n')


for i in range(len(httprequest)):
	httprequest[i]=httprequest[i].split()

serverequest(connectionSocket,httprequest[0])

connectionSocket.shutdown(SHUT_WR)
connectionSocket.close()
print("Connection Closed")
serverSocket.shutdown(SHUT_RDWR)
serverSocket.close()

