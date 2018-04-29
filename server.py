import sys
import socket
import threading
import os
import re
from ARequest import ARequest
from AResponse import AResponse

class SocketServer():

    def __init__(self, port):
        self.port = int(port)
        self.redirects = {}
        self.mapRedirects()
        self.redirectURL = ""
        self.status = ""


    def startListening(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #bind the socket to a public hostand port
        serversocket.bind(('', self.port))
        #become a server socket
        serversocket.listen(5)
        while 1:
            (clientSocket, address) = serversocket.accept()
            t = threading.Thread(target=self.threadedSocketReceive, args =(clientSocket, address))
            t.daemon = True
            t.start()

    #update the status of the request and create a response depending on the status
    def threadedSocketReceive(self, clientSocket, address):
        dataRequest = clientSocket.recv(2048)
        newRequest = ARequest(dataRequest)
        redirectURL = self.checkRedirect(newRequest)
        if not newRequest.validMethod():
            status = "405 Method Not Allowed"
            newResponse = AResponse(newRequest, status, "", None)
        elif not newRequest.validRequest():
            status = "400 Bad Request"
            newResponse = AResponse(newRequest, status, "", None)
        elif not redirectURL == None:
            status ="301 Permanently Moved "
            newResponse = AResponse(newRequest, status, "", redirectURL)
        elif self.foundFile(newRequest):
            status ="200 OK"
            f = self.returnFile(newRequest.path)
            newResponse = AResponse(newRequest, status, f, None)
        else:
            status ="404 File Not Found"
            newResponse = AResponse(newRequest, status, "", None)
        print newResponse.formattedResponse()
        clientSocket.sendall(newResponse.formattedResponse())
        clientSocket.close()

    #check that the file input in the request is a file available on the server
    def foundFile(self, request):
        return os.path.isfile("./www" + request.path)

    #read in the redirect file (when server opens, so dont have to read for every request) and put values in a dict
    def mapRedirects(self):
          redir = open("./www/redirect.defs", "r")
          lines = redir.readlines()
          for line in lines:
              key = line.split(" ")[0]
              value = line.split(" ")[1][:-1]
              self.redirects[key] = value

    #check if the request file is in the redirects dictionary and if so returns the right location
    def checkRedirect(self, request):
        redirectPath = None
        keyCheck = re.match("(/\w+)", request.path)
        if keyCheck != None:
            path = keyCheck.group(0)
            if path in self.redirects.keys():
                redirectPath = self.redirects[path]
        return redirectPath

    def returnFile(self, path):
        f = open("./www" + path, "r")
        fullFile = f.read()
        return fullFile


if __name__ == '__main__':
    port = (sys.argv[1]) #take in the file name from the command line
    socketServer = SocketServer(port)
    socketServer.startListening()
