'''Script to test/validate the detect class.
This script sets up a camera stream with default constructor for detect() class
and polls the distance measurement to the ROI boundary box. The video stream is 
displayed with OpenCV and the depth measurements are printed to terminal. 
Finally, the range value (0 - 2) is queried and printed to terminal as well.
'''

import detect as rsdetect
import cv2

#Create camera object and use default inializers within class
rscam = rsdetect.Detector()

try:
    if rscam.startStream():                 #start stream if realsense profile was set up correctly
        print('Camera Stream Ready')
        while True:

            #get color and depth frames from realsense
            color_img, depth_img = rscam.getFrame()
            #print('Retrieved a color and depth frame')
            #print(color_img)

            #x,y = depth_img.shape          #this verifies that the depth image is a 2D numpy array of 1-tuples (used for debugging detect v01)
            #print(depth_img.shape)

            #getting depth measurements in feet
            dist = rscam.getROIdist(depth_img,background = None,dist_only = True)
            print('Distance to object within ROI: ',dist)

            #Get range value for alarming --> this will be sent to the D1 module 
            range_val = rscam.getRange(dist)
            print('Range value is: ', range_val)

            #getROIRect returns an image frame with an overlay boundary box outlining th ROI for depth measurements
            color_img = rscam.getROIRect(color_img,dist)
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('Realsense', color_img)
            #cv2.waitKey(0)          #press any key on keyboard to close image window         

            #Press ESC to stop stream
            c = cv2.waitKey(7) % 0x100
            if c == 27 or c == 10:
                cv2.destroyWindow('Realsense')
                break
finally:
    rscam.cleanup()