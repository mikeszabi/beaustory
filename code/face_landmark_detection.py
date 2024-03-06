import sys
import os
import dlib
import glob
import numpy as np
from skimage import io
import cv2
from imutils import face_utils

class NoFaceFound(Exception):
   """Raised when there is no face found"""
   pass

def rescale_and_pad_image(img1, img2):
    # Determine which image is larger
    firstSmaller=None
    if img1.shape[0] * img1.shape[1] > img2.shape[0] * img2.shape[1]:
        larger_img = img1
        smaller_img = img2
        firstSmaller=False
    else:
        larger_img = img2
        smaller_img = img1
        firstSmaller=True

    # Calculate the scale factor, keeping the aspect ratio
    height_ratio = larger_img.shape[0] / smaller_img.shape[0]
    width_ratio = larger_img.shape[1] / smaller_img.shape[1]
    scale_factor = min(height_ratio, width_ratio)
    
    # Rescale the smaller image
    new_size = (int(smaller_img.shape[1] * scale_factor), int(smaller_img.shape[0] * scale_factor))
    resized_img = cv2.resize(smaller_img, new_size, interpolation=cv2.INTER_AREA)
    
    # Calculate padding sizes
    pad_vertical = (larger_img.shape[0] - resized_img.shape[0]) // 2
    pad_horizontal = (larger_img.shape[1] - resized_img.shape[1]) // 2
    
    # Create padded image
    padded_img = cv2.copyMakeBorder(resized_img, 
                                    pad_vertical, 
                                    larger_img.shape[0] - resized_img.shape[0] - pad_vertical, 
                                    pad_horizontal, 
                                    larger_img.shape[1] - resized_img.shape[1] - pad_horizontal, 
                                    cv2.BORDER_CONSTANT, 
                                    value=[255, 255, 255]) # White padding
    
    if firstSmaller:
        imgList=[padded_img,img2]
    else:
        imgList=[img1,padded_img]
    
    return imgList

def generate_face_correspondences(img1, img2, model_file):
    # Detect the points of face.
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(model_file)
    corresp = np.zeros((68,2))

    imgList = rescale_and_pad_image(img1,img2)
    list1 = []
    list2 = []
    j = 1

    for img in imgList:

        size = (img.shape[0],img.shape[1])
        if(j == 1):
            currList = list1
        else:
            currList = list2

        # Ask the detector to find the bounding boxes of each face. The 1 in the
        # second argument indicates that we should upsample the image 1 time. This
        # will make everything bigger and allow us to detect more faces.

        dets = detector(img, 1)

        try:
            if len(dets) == 0:
                raise NoFaceFound
        except NoFaceFound:
            print("Sorry, but I couldn't find a face in the image.")

        j=j+1

        for k, rect in enumerate(dets):
            
            # Get the landmarks/parts for the face in rect.
            shape = predictor(img, rect)
            # corresp = face_utils.shape_to_np(shape)
            
            for i in range(0,68):
                x = shape.part(i).x
                y = shape.part(i).y
                currList.append((x, y))
                corresp[i][0] += x
                corresp[i][1] += y
                # cv2.circle(img, (x, y), 2, (0, 255, 0), 2)

            # Add back the background
            currList.append((1,1))
            currList.append((size[1]-1,1))
            currList.append(((size[1]-1)//2,1))
            currList.append((1,size[0]-1))
            currList.append((1,(size[0]-1)//2))
            currList.append(((size[1]-1)//2,size[0]-1))
            currList.append((size[1]-1,size[0]-1))
            currList.append(((size[1]-1),(size[0]-1)//2))

    # Add back the background
    narray = corresp/2
    narray = np.append(narray,[[1,1]],axis=0)
    narray = np.append(narray,[[size[1]-1,1]],axis=0)
    narray = np.append(narray,[[(size[1]-1)//2,1]],axis=0)
    narray = np.append(narray,[[1,size[0]-1]],axis=0)
    narray = np.append(narray,[[1,(size[0]-1)//2]],axis=0)
    narray = np.append(narray,[[(size[1]-1)//2,size[0]-1]],axis=0)
    narray = np.append(narray,[[size[1]-1,size[0]-1]],axis=0)
    narray = np.append(narray,[[(size[1]-1),(size[0]-1)//2]],axis=0)
    
    return [size,imgList[0],imgList[1],list1,list2,narray]
