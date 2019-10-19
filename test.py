from socket import *

rootDirectory="\\"
serverPort = 12000

serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(1)
print("The server is ready to receive")


def serveRequest(request,addr,connectionSocket):
	if(request[0]=="GET"):
		data="""HTTP/1.1 200 OK\r    
				Content-Type: text/plain\r
				Content-Length: 8\r
				Last-Modified: Mon, 15 May 2017 18:04:40 GMT\r
				ETag: "ae780585f49b94ce1444eb7d28906123"\r
				Accept-Ranges: bytes\r
				Server: AmazonS3\r
				X-Amz-Cf-Id: CET7ZfbMr3lC71Nv26uOz2wXkflPZ89Z5TNSgRJN-GHQUxsOjR0p9g==\r
				Cache-Control: no-cache, no-store, must-revalidate\r
				Date: Fri, 18 Oct 2019 16:55:46 GMT\r
				Via: HTTP/1.1 forward.http.proxy:3128\r
				Connection: keep-alive\n""".encode()
		connectionSocket.send(data)

		
	else:
		print("Bad Request")




connectionSocket, addr = serverSocket.accept()
print("Connection accepted")
sentence = connectionSocket.recv(1024)
httprequest = sentence.decode().split('\r\n')
for i in range(len(httprequest)):
	httprequest[i]=httprequest[i].split()
print(httprequest)

serveRequest(httprequest[0],addr,connectionSocket)

connectionSocket.close()
print("Connection Closed")
serverSocket.close()