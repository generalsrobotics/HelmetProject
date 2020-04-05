import pyrealsense2 as rs
import numpy as np
import cv2
import json


class Detector:
    def __init__(self,server,w=640,h=480,fps=30):
        # Configure depth and color streams
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.width = w            
        self.height = h
        self.fps = fps
        #configure the realsense's color and depth stream given dimensions for width and height
        self.config.enable_stream(rs.stream.depth, self.width, self.height, rs.format.z16, fps)
        self.config.enable_stream(rs.stream.color, self.width, self.height, rs.format.bgr8, fps)
        self.box_width = 64
        self.box_height = 64
        #create array containing range values of interest in feet
        self.ranges = [20,10,5]
        self.colors = [(0,255,0),(0,255,255),(0,0,255)] #Green, Yellow, Red
        #defining measure area/box coordinates within image
        self.box_width_min = int((self.width - self.box_width)//2 -1)        #coordinates to center box within image. This is the first horizontal coordinate for the measure box
        self.box_height_min = int((self.height - self.box_height)//2 -1)     #y-coordinate to center box within image
        self.box_width_max = int(self.box_width_min + self.box_width)
        self.box_height_max = int(self.box_height_min + self.box_height)
        self.profile = None
        self.depth_scale = None
        self.server = server
        self.counter = 0

    def startStream(self):
        #start streaming
        self.profile = self.pipeline.start(self.config)
        #get data scale from the realsense to convert distance to meters
        self.depth_scale = self.profile.get_device().first_depth_sensor().get_depth_scale()


    def startDetecting(self):
        try:
            while True:
                #wait for a coherent pair of frames: depth and color
                frames = self.pipeline.wait_for_frames()
                depth_frame = frames.get_depth_frame()
                color_frame = frames.get_color_frame()
        
                # Convert images to numpy arrays
                depth_image = np.asanyarray(depth_frame.get_data())
                color_image = np.asanyarray(color_frame.get_data())
        
                #view depth data (as a matrix/array) of a meas_width x meas_height box in the center of the image
                resized_depth_image = depth_image[self.box_height_min : self.box_height_max : 1,self.box_width_min : self.box_width_max : 1].astype(float)
        
                # Get data scale from the device and convert to meters
                resized_depth_image = resized_depth_image * self.depth_scale
        
                #averaging range information inside the measurement box at center of image
                avg_dist = cv2.mean(resized_depth_image)[0] 
        
                #convert meters to feet
                avg_dist = round(avg_dist * 3.28084)
        
                #apply colors according to distance and notify user
                text_color = self.colors[2]
                box_color = text_color
                if avg_dist >= self.ranges[0]:
                    text_color = self.colors[0]
                    box_color = text_color
                elif avg_dist >= self.ranges[1]:
                    text_color = self.colors[1]
                    box_color = text_color
                elif avg_dist >= self.ranges[2]:
                    text_color = self.colors[2]
                    box_color = text_color
                if self.counter > 10:
                    self.server.send_message_to_all(json.dumps({"range":self.colors.index(text_color),"distance":avg_dist}))
                    self.counter = 0 
                else:
                    self.counter = self.counter + 1
                #print rectangle on color image for cyclist's benefit
                cv2.rectangle(color_image, (self.box_width_min, self.box_height_min), (self.box_width_max, self.box_height_max), box_color, 2)

                #creating an 'image' with dimensions as shown below to display the distance information stacked below the color image
                dist_bar_height = 100
                distance_bar = np.zeros([dist_bar_height,self.width,3], dtype=np.uint8)     #numpy array that will represent the 'image' or bar to print the distance measurement 

                #filling up numpy array with 255's to create a white background
                distance_bar.fill(127)

                #print distance measurement onto the distance bar image 
                cv2.putText(distance_bar, "Average distance to object: "+str(avg_dist) +" feet", (60,30), cv2.FONT_HERSHEY_COMPLEX, .9, text_color)
  
                #stack images vertically for displaying
                images = np.vstack((color_image,distance_bar))
        
        
                #Show images
                cv2.namedWindow('SmartHelmet', cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty('SmartHelmet',cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                cv2.imshow('SmartHelmet', images)
                cv2.waitKey(1)
        
        finally:

            # Stop streaming
            self.pipeline.stop()
