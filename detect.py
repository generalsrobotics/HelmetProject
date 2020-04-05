import pyrealsense2 as rs
import numpy as np
import cv2

class Detector:
    def __init__(self,w=640,h=480,fps=30):
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.width = w            
        self.height = h
        self.fps = fps
        self.config.enable_stream(rs.stream.depth, self.width, self.height, rs.format.z16, fps)
        self.config.enable_stream(rs.stream.color, self.width, self.height, rs.format.bgr8, fps)
        self.profile = None
        self.depth_scale = None
        self.roi_width = 64
        self.roi_height = 64
        self.ranges = [20,10,5]


    def startStream(self):
        try:
            self.profile = self.pipeline.start(self.config)
            self.depth_scale = self.profile.get_device().first_depth_sensor().get_depth_scale()
            return True
        except:
            return False

    def getROIRect(self,img):
        y,x,c = img.shape
        startx = x//2 - self.roi_width//2
        starty = y//2 - self.roi_height//2
        roi = img[starty:starty+self.roi_height, startx:startx+self.roi_width, :]
        out = cv2.rectangle(img, (startx,starty), (startx+self.roi_width,starty+self.roi_height),(0,0,255),1) 
        return out,np.mean(roi)
        
    def getRange(self,dist):
        r = 0
        if dist <= self.ranges[2]:
            r = 2
        elif dist <= self.ranges[1]:
            r = 1
        return r         
           

    def getROI(self,img,background = None,dist_only = False):
        y,x,c = img.shape
        startx = x//2 - self.roi_width//2
        starty = y//2 - self.roi_height//2

        roi = img[starty:starty+self.roi_height, startx:startx+self.roi_width, :]
        out = None
        if dist_only:
            out = np.mean(roi)
        else:
            if background is None:
                out =  roi
            else:
                background[starty:starty+self.roi_height, startx:startx+self.roi_width, :] = roi
                out = background
        return out

    def convertDepthToFeet(self,depth_image):
        return depth_image * self.depth_scale * 3.28084

    def getFrame(self):
        try:
            align_to = rs.stream.color
            align = rs.align(align_to)
            frames = align.process(self.pipeline.wait_for_frames())
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            depth_image = np.asanyarray(depth_frame.get_data()) 
            color_image = np.asanyarray(color_frame.get_data())
        
            return color_image, depth_image
        except:
            return None, None   
        
    def cleanup():
            self.pipeline.stop()
