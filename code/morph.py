#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 14:54:54 2024

@author: szabi
"""

import sys

sys.path.append(r'./code')

import os
import cv2
import numpy as np
from PIL import Image

from face_landmark_detection import generate_face_correspondences
from delaunay_triangulation import make_delaunay
from face_morph import generate_morph_sequence

image_dir=r'./resources/before_after_images'
result_dir=r'./outputs'
output='morph3b'
face_model_file=r'./resources/models/shape_predictor_68_face_landmarks.dat'    

# Define Wrapper Function
def doMorphing(img1, img2, duration, frame_rate,face_model_file):
    [size, img1, img2, points1, points2, list3] = generate_face_correspondences(img1, img2,face_model_file)
    gif=[]
    if len(points1)>0 and len(points2)>0:
        tri = make_delaunay(size[1], size[0], list3, img1, img2)
        gif = generate_morph_sequence(duration, frame_rate, img1, img2, points1, points2, tri, size)
    return gif

def create_gif(image1,image2):
    
    # from Pillow
    img1=cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2BGR)
    img2=cv2.cvtColor(np.array(image2), cv2.COLOR_RGB2BGR)
    
    gif=doMorphing(img1,img2,4,10,face_model_file)
    
    if len(gif)>0:
        gif[0].save(os.path.join(result_dir,f'{output}.gif'), save_all=True,optimize=False, append_images=gif[1:], loop=0)
    return gif

def main():

    os.listdir(image_dir)
    
    image1_name=os.path.join(image_dir,'before_DANI.png')
    image2_name=os.path.join(image_dir,'after_DANI.png')
    
    image1 = Image.open(image1_name)
    image2 = Image.open(image2_name)
    
    gif=create_gif(image1,image2)
