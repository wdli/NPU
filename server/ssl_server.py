#!/usr/bin/python
#
# create: 4/17
#
# 4/17: simple test using curl -v -ssl http://localhost:4443
#       no reply from server
#

import BaseHTTPServer, SimpleHTTPServer
import ssl

httpd = BaseHTTPServer.HTTPServer(('localhost', 4443), SimpleHTTPServer.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket (httpd.socket, certfile='../openssl-ca/certs/cs535B_entity_cert.pem', server_side=True)
httpd.serve_forever()
