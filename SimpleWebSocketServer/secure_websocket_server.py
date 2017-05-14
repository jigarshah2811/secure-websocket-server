'''
The MIT License (MIT)
Copyright (c) 2013 Dave P.
'''

import signal
import sys
import ssl
from SimpleWebSocketServer.SimpleWebSocketServer import WebSocket, SimpleWebSocketServer, SimpleSSLWebSocketServer
from optparse import OptionParser
import json

configNetworkCmd = {
	'msg' : 'configNetworkApi',
	'username' : 'admin',
	'password' : 'secret'
}

clients = []
class SimpleWebSocket(WebSocket):

   def handleMessage(self):
      for client in clients:
         if client != self:
            client.sendMessage(self.address[0] + u' - ' + self.data)
      print (self.address, 'sent', self.data)

   def handleConnected(self):
      clients.append(self)
      print (self.address, 'connected')
      self.sendMessage(json.dumps(configNetworkCmd, ensure_ascii=False))

   def handleClose(self):
      clients.remove(self)
      print (self.address, 'closed')


if __name__ == "__main__":

   parser = OptionParser(usage="usage: %prog [options]", version="%prog 1.0")
   parser.add_option("--host", default='', type='string', action="store", dest="host", help="hostname (localhost)")
   parser.add_option("--port", default=8000, type='int', action="store", dest="port", help="port (8000)")
   parser.add_option("--ssl", default=1, type='int', action="store", dest="ssl", help="ssl (1: on, 0: off (default))")
   parser.add_option("--certfile", default='./server.crt', type='string', action="store", dest="cert", help="Server Cert self-signed or CA-signed (./server.crt)")
   parser.add_option("--keyfile", default='./server.key', type='string', action="store", dest="key", help="Server Private key file (./server.key)")
   parser.add_option("--ver", default=ssl.PROTOCOL_TLSv1, type=int, action="store", dest="ver", help="ssl version")

   (options, args) = parser.parse_args()

   if options.ssl:
      server = SimpleSSLWebSocketServer(options.host, options.port, SimpleWebSocket, options.cert, options.key, version=options.ver)
   else:
      server = SimpleWebSocketServer(options.host, options.port, cls)

   server.serveforever()
