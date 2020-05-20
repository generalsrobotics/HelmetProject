#!/usr/bin/env python
from flask import Flask, render_template, Response
import io
import cv2
import datetime
import threading
from random  import randrange
import numpy as np
from detect import Detector
import random

app = Flask(__name__)
#b = "10"
#vc = cv2.VideoCapture("rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov")

#vc = cv2.VideoCapture(1)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/')
def index():
    """Video streaming home page."""
    now = datetime.datetime.now()
    print (now.strftime("%Y-%m-%d %H:%M:%S"))
    #return render_template('index.html', value=now.strftime("%Y-%m-%d %H:%M:%S")+" "+color(randrange(2)))
    return render_template('index.html', value=color(randrange(2)))
    threading.Timer(0.1, index).start()


@app.route('/update')
def update():
    now = datetime.datetime.now()
    T = now.strftime("%H:%M:%S")
    
    #dist = detector.getROIdist(depth_frame,background = None, dist_only = True)
    #range_val = detector.getRange(dist)
    #print(dist)
    return b
    #return render_template('update.html', suggestions = dist)


def color(num):
    col=["#ff0000","#ffff00","#00ff00"]
    return col[num]




def gen():
    global dist    
    """Video streaming generator function."""
    while True:
        color_frame, depth_frame = detector.getFrame()
       # global dist
        dist= detector.getROIdist(depth_frame,background = None, dist_only = True)
        global b
        b = str(dist)
        range_val = detector.getRange(dist)
        
        #read_return_code, frame = color_frame
        #frame = color_frame
        
        color_img = detector.getROIRect(color_frame,dist)
        frame = color_img

        encode_return_code, image_buffer = cv2.imencode('.jpg', frame)
        io_buf = io.BytesIO(image_buffer)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + io_buf.read() + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(
        gen(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


if __name__ == '__main__':
    detector = Detector()
    
    if detector.startStream():
    
        app.run(host='192.168.1.10', debug=False, threaded=True)

        
                #color_frame, depth_frame = detector.getFrame()
    #app.run(host='10.1.1.16', debug=False, threaded=True)
