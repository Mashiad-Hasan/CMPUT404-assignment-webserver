#  coding: utf-8 
import socketserver, os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# Copyright: 2023 Mashiad Hasan (new)
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        
        s = str(self.data) 
    
        # The string parsing code was adapted from StackOverFlow
        # Originally Answered by ansetou and David Arenburg
        # URL: https://stackoverflow.com/questions/3368969/find-string-between-two-substrings

        start = "b'GET "
        end = ' HTTP'
        request = s[s.find(start)+len(start):s.rfind(end)]

        method = s[2:5]

        # HTTP Headers and Responses (Status codes) were implemented with accordance to MDN Web Docs
        # URL: https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages
        
        if method != "GET":
            self.request.sendall('HTTP/1.1 405 Method Not Allowed\n\n'.encode())  
            self.request.sendall('405 Method Not Allowed'.encode())

        elif request!= '/favicon.ico':
            if not os.path.exists('www' + request):
                self.request.sendall('HTTP/1.1 404 Not Found\n\n'.encode())
                self.request.sendall('404 Not Found'.encode())
                
            
            elif '..' in request:
                self.request.sendall('HTTP/1.1 404 Not Found\n\n'.encode())
                self.request.sendall('404 Not Found'.encode())

            elif (('.html' in request) or ('.css' in request)):
                try:
                    fp = open(('www'+ request),'r' )
                    content = fp.read()
                    self.request.sendall(('HTTP/1.1 200 OK\n').encode())
                    if '.html' in request:
                        self.request.sendall('Content-Type: text/html; charset=utf-8\n\n'.encode())
                    elif '.css' in request:
                        self.request.sendall('Content-Type: text/css; charset=utf-8\n\n'.encode())
                    
                    self.request.sendall(content.encode())

                except:
                    self.request.sendall('HTTP/1.1 404 Not Found\n\n'.encode())
                    self.request.sendall('404 Not Found'.encode())    

            elif ('/' != request[-1]) :   
                self.request.sendall('HTTP/1.1 301 Moved Permanently\n'.encode())
                
                request = request + '/'
                self.request.sendall(('Location: http://127.0.0.1:8080' + request + '\n' ).encode()) # new line

                try:
                    fp = open(('www'+ request + 'index.html'),'r' )
                    content = fp.read()
                    self.request.sendall('Content-Type: text/html; charset=utf-8\n\n'.encode())
                    self.request.sendall(content.encode())

                except:
                    self.request.sendall('\n\n'.encode())
                    self.request.sendall('301 Moved Permanently'.encode())
                
            elif ('/' == request[-1]):
                try:
                    self.request.sendall('HTTP/1.1 200 OK\n'.encode())

                    fp = open(('www'+ request + 'index.html'),'r' )
                    self.request.sendall('Content-Type: text/html; charset=utf-8\n\n'.encode())
                    content = fp.read()
                    self.request.sendall(content.encode())

                except:

                    self.request.sendall('No index.html file in this directory'.encode())
        
            else:
                self.request.sendall('HTTP/1.1 400 Bad Request\n\n'.encode())
                self.request.sendall('Cannot serve this file'.encode())

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C

    server.serve_forever()
    
    
   
    
