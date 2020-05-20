from websocket_server import WebsocketServer

from threading import Thread


import time
import cv2
import numpy as np
from flask import Flask, render_template, Response


from detect import Detector
import datetime

app = Flask(__name__)
dist = 0
color_frame = None
depth_frame = None
gray_frame = None
zone = 0

print("Starting Server")


app.config["TEMPLATES_AUTO_RELOAD"] = True
@app.route('/')
def index():
    """Video streaming home page."""
    now = datetime.datetime.now()
    print (now.strftime("%Y-%m-%d %H:%M:%S"))
    return render_template('index.html', value=color(zone))

@app.route('/point_cloud')
def point_cloud():
    now = datetime.datetime.now()
    print (now.strftime("%Y-%m-%d %H:%M:%S"))
    return render_template('points.html')

@app.route('/update')
def update():
    now = datetime.datetime.now()
    T = now.strftime("%H:%M:%S")
    updateReadings()
    return render_template('update.html', suggestions = dist or -1)


def color(num):
    col=["#ff0000","#ffff00","#00ff00"]
    return col[num]

def updateReadings():
    color_frame, depth_frame = detector.getFrame()
    dist = detector.getROIdist(depth_frame,background = None, dist_only = True)

def gen():
    global dist
    global color_frame
    while True:
        color_img = detector.getROIRect(color_frame,dist)
        encode_return_code, image_buffer = cv2.imencode('.jpg', color_img)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image_buffer.tobytes() + b'\r\n')

def gen_depth():
    global gray_frame
    while True:
        encode_return_code, image_buffer = cv2.imencode('.jpg', gray_frame)
        yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + image_buffer.tobytes() + b'\r\n')




@app.route('/video_feed')
def video_feed():

    return Response(
        gen(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@app.route('/depth_feed')
def depth_feed():

    return Response(
        gen_depth(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )



class Backend:
    def __init__(self,wsPort=8000,httpPort=5000):
        self.clients = []
        self.wsServer = WebsocketServer(wsPort,host="0.0.0.0")
        self.httpServer = app


    def runHTTP(self):
        self.httpServer.run(host='0.0.0.0',threaded=True)
        
    def online(self):
        try:
            Thread(target=self.notifyHelmet,daemon=True).start()
            Thread(target=self.runHTTP,daemon=True).start()
            print("Backend Online")
            return True
        except Exception as e:
            print(e)
            return False

    def notifyHelmet(self):
        Thread(target=self.wsServer.serve_forever,daemon=True).start()
        while True:
            self.wsServer.send_message_to_all(str(zone))
            time.sleep(0.3)

              




if __name__ == "__main__":
    detector = Detector()
    backend = Backend()
    if backend.online():
        if detector.startStream():
            while True:
                color_frame, depth_frame,gray_frame = detector.getFrame()
                dist = detector.getROIdist(depth_frame,background = None, dist_only = True)
                
                zone = detector.getRange(dist)

            print("Stream stopped")
        else:
            print("Error loading realsense")
    else:
        print("Error loading Backend")

