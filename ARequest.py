import re

class ARequest():

    def __init__(self, dataIn):
        self.data = dataIn
        self.method = ""
        self.version = ""
        self.path = ""
        self.connection =""
        self.server = ""
        self.parseData()

    # takes in the request and separates it into fields needed for the response
    def parseData(self):
        lineSplit = self.data.split("\r\n")
        reponseHeader= lineSplit[0].split(" ")
        serverInfo = lineSplit[5].split(" ")
        connectionInfo = lineSplit[7].split(" ")
        self.method = reponseHeader[0]
        self.path = reponseHeader[1]
        self.version = reponseHeader[2]
        self.server = serverInfo[1]
        self.connection = connectionInfo[1]

    #check to make sure the request is in a valid format with a method , file, and http version
    def validRequest(self):
        method = False
        validFile = False
        http = False
        if self.method == "GET" or self.method == "HEAD":
            method = True
        if re.match("/.*\.*", self.path):
            validFile = True
        if self.version == "HTTP/1.1":
            http = True
        if method and validFile and http:
            return True
        else:
            return False

    #check to make sure the request is either a get or head request, everything else considered invalid for this project
    def validMethod(self):
        if self.method == "GET" or self.method == "HEAD":
            return True
        else:
            return False
