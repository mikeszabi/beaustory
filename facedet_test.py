#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 19:10:37 2024

@author: szabi
"""
import sys

sys.path.append(r'./code')

import os
import dlib
import glob
import numpy as np
from skimage import io
import cv2
from imutils import face_utils
from face_landmark_detection import generate_face_correspondences
from delaunay_triangulation import make_delaunay
from delaunay_triangulation import make_delaunay


sys.path.append('../utils')

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(r'./utils/shape_predictor_68_face_landmarks.dat')
corresp = np.zeros((68,2))


image_dir=r'./resources/before_after_images'

os.listdir(image_dir)

image1_name=os.path.join(image_dir,'before_1.jpg')
image2_name=os.path.join(image_dir,'after_1.jpg')


image1 = cv2.imread(image1_name)
image2 = cv2.imread(image2_name)

# Define Wrapper Function
def doMorphing(img1, img2, duration, frame_rate, output):
	[size, img1, img2, points1, points2, list3] = generate_face_correspondences(img1, img2)
	tri = make_delaunay(size[1], size[0], list3, img1, img2)
	generate_morph_sequence(duration, frame_rate, img1, img2, points1, points2, tri, size,output)