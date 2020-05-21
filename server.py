from websocket_server import WebsocketServer
from threading import Thread
from multiprocessing import Process
import time
import cv2
import numpy as np
from flask import Flask, render_template, Response, jsonify
from detect import Detector

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
    return render_template('template.html',js="../static/js/2D.js")

@app.route('/point_cloud')
def point_cloud():
    return render_template('template.html',js="../static/js/3D.js")

@app.route('/info')
def info():
    return jsonify(distance=dist,zone=zone)


def updateReadings():
    global detector
    global color_frame
    global depth_frame
    global gray_frame
    global dist
    global zone
    detector = Detector()
    detector.startStream()
    while True:
        color_frame, depth_frame, gray_frame = detector.getFrame()
        dist = detector.getROIdist(depth_frame,background = None, dist_only = True)
        zone = detector.getRange(dist)

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
    def __init__(self,port=8000):
        self.wsServer = WebsocketServer(port,host="0.0.0.0")

    def notifyHelmet(self):
        Thread(target=self.wsServer.serve_forever,daemon=True).start()
        while True:
            self.wsServer.send_message_to_all(str(zone))
            time.sleep(0.3)




if __name__ == "__main__":
    backend = Backend()
    Thread(target=updateReadings,daemon=True).start()
    Thread(target=backend.notifyHelmet,daemon=True).start()
    app.run(host='0.0.0.0',threaded=True)
    
   
