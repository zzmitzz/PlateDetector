from PIL import Image
import cv2
import torch
import math 
from ultralytics import YOLO
import os
from PIL import Image
from numpy import asarray
import time
import argparse
import function.utils_rotate as utils_rotate
import function.helper as helper
import function.plateQuey as query
import function.Detection as detector


#Load model 
model_path = os.path.join("model","model10_10.pt")
yolo_license_plate = torch.hub.load('yolov5', 'custom', path='model/LP_ocr.pt', force_reload=True, source='local')
model = YOLO(model_path)

imageName = "biendep_ldct.jpg" # <== image,video name here


if imageName.lower().endswith((".mp4", ".avi", ".mkv", ".gif")):
    cap = cv2.VideoCapture(os.path.join("test_image",imageName))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = int(cap.get(5))
    out = cv2.VideoWriter(os.path.join("result",imageName), fourcc, fps, (frame_width, frame_height))
    i = 1
    if not cap.isOpened():
        print("Error: Could not open the video file.")
    else:
        # You can proceed to read and process the video frames here.
        while True:
            print(f"Frame rendered {i}".format(i))
            i+=1
            ret,frame = cap.read()
            if not ret:
                break
            frame = detector.MainDetect(model,yolo_license_plate,frame) 
            out.write(frame)
        cap.release()
        out.release()

elif imageName.lower().endswith((".jpg", ".jpeg", ".png")):
    try:
        img = cv2.imread(os.path.join("test_image",imageName)) 
        detector.MainDetect(model,yolo_license_plate,img)
        cv2.imwrite(os.path.join("result",imageName), img)
        cv2.waitKey()
        cv2.destroyAllWindows() 
    except:
        print("File not Found")
    