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
        #self.config.enable_device_from_file("EC_Recording3.bag")
        self.profile = None
        self.depth_scale = None
        self.roi_width = 64
        self.roi_height = 64
        self.ranges = [1,3,6]
        self.rect_color = (0,255,0)     #initialize to green
        self.colorizer = rs.colorizer()
        self.colorizer.set_option(rs.option.color_scheme, 2)


    def setRanges(self,r1,r2,r3):
        self.ranges[0] , self.ranges[1], self.ranges[2] = r1, r2, r3

    def startStream(self):
        try:
            self.profile = self.pipeline.start(self.config)
            self.depth_scale = self.profile.get_device().first_depth_sensor().get_depth_scale()
            return True
        except:
            return False

    def getFrame(self,raw=True):
        try:
            align_to = rs.stream.color
            align = rs.align(align_to)
            frames = align.process(self.pipeline.wait_for_frames())
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())
            gray_image = np.asanyarray(self.colorizer.colorize(depth_frame).get_data())
            return color_image, depth_image,gray_image
        except Exception as e:
            print(e)
            return None, None, None

   
            
        


    def getROIRect(self,img,dist):
        colors = [(0,255,0),(0,255,255),(0,0,255)]
        y,x,c = img.shape
        startx = x//2 - self.roi_width//2
        starty = y//2 - self.roi_height//2

        roi = img[starty : starty + self.roi_height : 1, startx : startx + self.roi_width : 1]

        self.rect_color = colors[self.getRange(dist)]

        out = cv2.rectangle(img, (startx,starty), (startx+self.roi_width,starty+self.roi_height),self.rect_color,1)

        #I am coverting the distance measurement straight into feet in the getROIdist method to avoid multiple computations
        return out


    def getRange(self,dist):
        if (dist<=self.ranges[0]):
            return 2
        elif (dist<=self.ranges[1]):
            return 1
        else:
            return 0



    def getROIdist(self,img,background = None,dist_only = False):
        '''this method expects a depth image (numpy array)'''
        y,x = img.shape     #depth image numpy array unpacks two dimensions only
        startx = x//2 - self.roi_width//2
        starty = y//2 - self.roi_height//2

        #roi = img[starty:starty+self.roi_height, startx:startx+self.roi_width, :]  indices had an error
        roi = img[starty : starty + self.roi_height : 1, startx : startx + self.roi_width : 1]

        out = None
        if dist_only:
            roi_feet = self.depth_scale*roi*3.28084
            out = np.mean(roi_feet)
        else:
            if background is None:
                out =  roi
            else:
                background[starty:starty+self.roi_height, startx:startx+self.roi_width, :] = roi
                out = background
        return out

    def convertDepthToFeet(self,depth_image):
        #we may not need this one here
        return depth_image * self.depth_scale * 3.28084



    def cleanup():
            self.pipeline.stop()
