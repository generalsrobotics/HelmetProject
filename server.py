from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
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

       
class Backend:
    def __init__(self,wsPort=9001,httpPort=8000):
        self.clients = []
        handler = ClientHandler
        handler.backend = self
        self.wsServer = SimpleWebSocketServer("0.0.0.0", wsPort, handler)
        self.httpServer = socketserver.TCPServer(('0.0.0.0', httpPort), SimpleHTTPRequestHandler)
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
        packed = cv2.imencode(".jpeg",frame,(cv2.IMWRITE_JPEG_QUALITY, 100))[1]
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
                color_frame, depth_frame = detector.getFrame()
                dist = rscam.getROIdist(depth_img,background = None,dist_only = True)
                range_val = rscam.getRange(dist)
                color_img = rscam.getROIRect(color_img,dist)
                backend.p[0].send(color_img)
                backend.p[0].send(range_val)
            print("Stream stopped")
        else:
            print("Error loading realsense")
    else:
        print("Error loading Backend")
#    cam = cv2.VideoCapture(0)
#    backend = Backend()
#    if backend.online():
#        while True:
#            t0 = time.time()
#            ready, test = cam.read()
#            if ready:
#                dummyRange = random.choice([0,1,2])
#                backend.p[0].send(test)
#                backend.p[0].send(dummyRange)
#                print((time.time()-t0))
                
   
