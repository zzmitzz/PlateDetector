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
model_path = os.path.join("model","best.pt")
yolo_license_plate = torch.hub.load('yolov5', 'custom', path='model/LP_ocr.pt', force_reload=True, source='local')
model = YOLO(model_path)

imageName = "117.jpg" # <== image,video name here


if imageName.lower().endswith((".mp4", ".avi", ".mkv")):
    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        print("Error: Could not open the video file.")
    else:
        # You can proceed to read and process the video frames here.
        cap.release()
elif imageName.lower().endswith((".jpg", ".jpeg")):
    img = cv2.imread(os.path.join("test_image",imageName))  
    detector.MainDetect(model,yolo_license_plate,img,imageName) 