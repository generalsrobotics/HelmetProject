from SimpleWebSocketServer import SimpleSSLWebSocketServer, WebSocket
from threading import Thread
from multiprocessing import Process, Pipe
import json
import time
import cv2
import numpy as np
from http.server import SimpleHTTPRequestHandler
import ssl
import socketserver
import random
from detect import Detector

class ClientHandler(WebSocket):
    role = None
    backend = None
    def handleMessage(self):
       parsed = None
       try:
           parsed = json.loads(self.data)
       finally:
           if parsed is not None and "role" in parsed.keys():
               self.role = parsed["role"]
               print("New client connected as %s"%self.role)

    def handleConnected(self):
       self.backend.clients.append(self)

    def handleClose(self):
       self.backend.clients.remove(self)
       print(self.address, 'closed')

class UIHandler(SimpleHTTPRequestHandler):
            def log_message(self, format, *args):
                return
       
class Backend:
    def __init__(self,wsPort=9001,httpPort=80):
        self.clients = []
        handler = ClientHandler
        handler.backend = self
        self.wsServer = SimpleSSLWebSocketServer("0.0.0.0", wsPort, handler, "cert.pem", "key.pem", ssl.PROTOCOL_TLSv1_2)
        self.httpServer = socketserver.TCPServer(('0.0.0.0', httpPort), UIHandler)
        self.httpServer.socket = ssl.wrap_socket(self.httpServer.socket, server_side=True, certfile='cert.pem', keyfile='key.pem', ssl_version=ssl.PROTOCOL_TLSv1_2)
        self.zone = 0
        self.p = Pipe()


        
    def online(self):
        try:
            Process(target=self.wsLoop,args=(self.p[1],),daemon=True).start()
            Process(target=self.httpServer.serve_forever,daemon=True).start()
            print("Backend Online")
            return True
        except Exception as e:
            print(e)
            return False

    def sendFrame(self,frame):
        assert type(frame) is np.ndarray
        packed = cv2.imencode(".jpeg",frame)[1]
        [client.sendMessage(packed) for client in self.clients if client.role == "viewer"]
    
    def wsLoop(self,conn):
        Thread(target=self.notifyHelmet,daemon=True).start()
        while True:
            n = conn.recv()
            if isinstance(n,np.ndarray):
                self.sendFrame(n)
            elif isinstance(n,int):
                self.zone = n 
            self.wsServer.serveonce()               


    def notifyHelmet(self):

        while True:
            try:
                msg = json.dumps({"range":self.zone})
                [client.sendMessage(msg) for client in self.clients if client.role == "helmet"]
                time.sleep(0.3)
            except:
                print("Error notifying helmet")
        


if __name__ == "__main__":
    detector = Detector()
    backend = Backend()
    if backend.online():
        if detector.startStream():
            while True:
                frame, depth = detector.getFrame()
                backend.p[0].send(frame)
            print("Stream stopped")
        else:
            print("Error loading realsense")
    else:
        print("Error loading Backend")
#    cam = cv2.VideoCapture(0)
#    backend = Backend()
#    if backend.online():
#        while True:
#            ready, test = cam.read()
#            if ready:
#                frame = cv2.cvtColor(test, cv2.COLOR_RGB2RGBA)
#                dummyRange = random.choice([0,1,2])
#                backend.p[0].send(frame)
#                backend.p[0].send(dummyRange)
                
   
