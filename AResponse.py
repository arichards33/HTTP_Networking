import datetime
import re


class AResponse():

# response example:
# HTTP/1.1 200 OK
# Date: Mon, 27 Jul 2009 12:28:53 GMT
# Server: Apache/2.2.14 (Win32)
# Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
# Content-Length: 88
# Content-Type: text/html
# Connection: Closed

    #holds the mimetypes needed for this project
    contentTypes = {".html": "text/html", ".txt": "text/plain", ".pdf": "application/pdf", \
    ".png": "mage/png", ".jpeg": "image/jpeg", ".jpg": "image/jpg"}

    def __init__(self, request, responseCode, bodyContent, location):
        self.method = request.method
        self.httpVersion = request.version
        self.path = request.path
        self.status = responseCode
        self.location = location
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.server = "Server: AlexWebServer"
        self.contentLength = len(bodyContent)
        self.contentType = ""
        self.connection = "Connection: Closed"
        self.bodyContent = bodyContent
        self.determineContentType()

    # format the reponse the way the server is expecting
    def formattedResponse(self):
        formatted = self.httpVersion + " " + self.status + "\r\n" + "Date: " + self.date + "\r\n" + self.server \
                    + "\r\n" + "Content-Length: " + str(self.contentLength) + "\r\n" \
                    + "Content-Type: " + self.contentType + "\r\n" + self.connection + "\r\n"
        if not self.location == None: #only return the relocation if the file is in the redirects file
            formatted = formatted + "Location: " + self.location + "\r\n"
        formatted = formatted + "\r\n"
        if not self.bodyContent == "" and not self.method == "HEAD": #should not return any body content for a head request or if the body is empty
            formatted = formatted + self.bodyContent
        return formatted

    # ensure there is an extension and then parse it out as a return field in the response
    def determineContentType(self):
        extension = re.search("(\.\w+)", self.path)
        if not extension == None:
            extensionRead = extension.group(0)
            if extensionRead in AResponse.contentTypes.keys():
                self.contentType = AResponse.contentTypes[extensionRead]
