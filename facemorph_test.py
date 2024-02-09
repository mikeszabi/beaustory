#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 19:10:37 2024

@author: szabi
"""
import sys

sys.path.append(r'./code')

import os
import cv2
from face_landmark_detection import generate_face_correspondences
from delaunay_triangulation import make_delaunay
from face_morph import generate_morph_sequence


# Define Wrapper Function
def doMorphing(img1, img2, duration, frame_rate,face_model_file):
    [size, img1, img2, points1, points2, list3] = generate_face_correspondences(img1, img2,face_model_file)
    if len(points1)>0 and len(points2)>0:
        tri = make_delaunay(size[1], size[0], list3, img1, img2)
        gif = generate_morph_sequence(duration, frame_rate, img1, img2, points1, points2, tri, size)
    return gif
    
face_model_file=r'./utils/shape_predictor_68_face_landmarks.dat'    
image_dir=r'./resources/before_after_images'
result_dir=r'.'
output='morph3b'


os.listdir(image_dir)

image1_name=os.path.join(image_dir,'Picture1.b.png')
image2_name=os.path.join(image_dir,'Picture1.a.png')


img1 = cv2.imread(image1_name)
img2 = cv2.imread(image2_name)

gif=doMorphing(img1,img2,5,10,face_model_file)

gif[0].save(os.path.join(result_dir,f'{output}.gif'), save_all=True,optimize=False, append_images=gif[1:], loop=0)
