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

def MainDetect(model,yolo_license_plate,img):
    platesv8 = model.predict(img,save = False, conf = 0.25,save_conf = True,imgsz = 640)[0]
    list_plates = list(platesv8.boxes.xyxy) # split the bounding data
    list_read_plates = set()

    # if not lp detect, just read the text 
    if len(list_plates) == 0:
        lp = helper.read_plate(yolo_license_plate,img)
        if lp != "unknown":
            cv2.putText(img, lp, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
            list_read_plates.add(lp)
    #else read the plate
    else:
        for plate in list_plates:
            flag = 0
            x = int(plate[0]) # xmin
            y = int(plate[1]) # ymin
            w = int(plate[2] - plate[0]) # xmax - xmin
            h = int(plate[3] - plate[1]) # ymax - ymin  
            crop_img = img[y:y+h, x:x+w]
            cv2.rectangle(img, (int(plate[0]),int(plate[1])), (int(plate[2]),int(plate[3])), color = (0,0,225), thickness = 2)
            cv2.imwrite("crop.jpg", crop_img)
            rc_image = cv2.imread("crop.jpg")
            lp = ""
            for cc in range(0,2):
                for ct in range(0,2):
                    lp = helper.read_plate(yolo_license_plate, utils_rotate.deskew(crop_img, cc, ct))
                    if lp != "unknown":
                        list_read_plates.add(lp)
                        province = query.getProvice(lp[0:2])
                        cv2.putText(img, lp, (int(plate[0]), int(plate[1]-25)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36,255,12), 2)
                        cv2.putText(img, "Province : " + province, (int(plate[0]), int(plate[1]-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,100,12), 2)
                        flag = 1
                        break
                if flag == 1:
                    break
        if(lp == "unknown"):
            img = utils_rotate.rotate_image(image=img,angle=0.0)
    return img
    