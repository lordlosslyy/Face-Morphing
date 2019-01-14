# import the necessary packages
from PIL import Image
from visualize_facial_landmarks import visualize_facial_landmarks
from shape_to_numpy_array import shape_to_numpy_array
from detect_68_feature import detect_68_features
from face_triangle import face_triangle
from morph import morph
import numpy as np
import cv2
import argparse
import dlib
import imutils

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--shape-predictor", required=False,
	help="path to facial landmark predictor", default = "shape_predictor_68_face_landmarks.dat")
ap.add_argument("-i1", "--image1", required=False,
	help="path to input image 1", default = "./images/justin.jpg")
ap.add_argument("-i2", "--image2", required=False,
	help="path to input image 2", default = "./images/dick.jpg")
ap.add_argument("-p", "--part", required=False,
	help="desired path : lefteyes, righteyes, eyes, leftbrown, rightbrown, eyebrowns, nose, mouth, jaw, face", default = "face")
ap.add_argument("-a", "--alpha", type = float, required=False,
	help="the morphing ratio", default = 0.5)
# ap.add_argument("-i", "--image", required=False,
# help="path to input image", default = "./images/obama.jpg")
args = vars(ap.parse_args())

image_1 = args["image1"]
image_2 = args["image2"]
alpha = args["alpha"]
morph_image = "Morphed Face.png"
points68_out_1 = "1.txt"
points68_out_2 = "2.txt"
morph_part = args["part"]

detect_68_features(args["shape_predictor"],image_1,points68_out_1)

detect_68_features(args["shape_predictor"],image_2,points68_out_2)

if morph_part == "eyes":
    face_triangle(image_1,points68_out_1,"lefteye","tri")
    morph(image_1,image_2,points68_out_1,points68_out_2,alpha)
    face_triangle(image_1,points68_out_1,"righteye","tri")
    morph(morph_image,image_2,points68_out_1,points68_out_2,alpha)
elif morph_part == "eyebrowns":
    face_triangle(image_1,points68_out_1,"leftbrown","tri")
    morph(image_1,image_2,points68_out_1,points68_out_2,alpha)
    face_triangle(image_1,points68_out_1,"rightbrown","tri")
    morph(morph_image,image_2,points68_out_1,points68_out_2,alpha)  
else:
    face_triangle(image_1,points68_out_1,morph_part,"tri")
    morph(image_1,image_2,points68_out_1,points68_out_2,alpha)
