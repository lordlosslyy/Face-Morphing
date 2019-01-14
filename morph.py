# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 21:24:37 2018

@author: user
"""
from morph_function import readPoints
from morph_function import applyAffineTransform
from morph_function import morphTriangle
import numpy as np
import cv2
import sys
import pdb


def morph(image1,image2,txt1,txt2, alpha):
    
    # Read images
    img1 = cv2.imread(image1)
    img2 = cv2.imread(image2)
    img1 = cv2.resize(img1,(500,500))
    img2 = cv2.resize(img2,(500,500))
    cv2.imwrite('D_resize.png', np.uint8(img1))
    cv2.imwrite('T_resize.png', np.uint8(img2))
    # Convert Mat to float data type
    img1 = np.float32(img1)
    img2 = np.float32(img2)
    
    # Read array of corresponding points
    points1 = readPoints(txt1)
    points2 = readPoints(txt2)
    points = []
    
    HSV = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    H1, S1, V1 = cv2.split(HSV)
    
    
    HSV = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
    H2, S2, V2 = cv2.split(HSV)
    
    #ratioH=(H1[points1[27]]+H1[points1[28]]+H1[points1[29]]+H1[points1[30]])/(H2[points2[27]]+H2[points2[28]]+H2[points2[29]]+H2[points2[30]])
    #ratioS=(S1[points1[27]]+S1[points1[28]]+S1[points1[29]]+S1[points1[30]])/(S2[points2[27]]+S2[points2[28]]+S2[points2[29]]+S2[points2[30]])
    ratioV=(V1[points1[27]]+V1[points1[28]]+V1[points1[29]]+V1[points1[30]])/(V2[points2[27]]+V2[points2[28]]+V2[points2[29]]+V2[points2[30]])

    H11 = H1[points1[29]] 
    H22 = H2[points2[29]]
    
    S11 = S1[points1[28]]#+S1[points1[29]]
    S22 = S2[points2[28]]#+S2[points2[29]]

    V11 = V1[points1[28]]#+V1[points1[29]] 
    V22 = V2[points2[28]]#+V2[points2[29]]

    print ("H1 = {0}, H2 = {1}".format(H11,H22))
    print ("S1 = {0}, S2 = {1}".format(S11,S22))  
    print ("V1 = {0}, V2 = {1}".format(V11,V22))  

    ratioH=(H1[points1[29]])/(H2[points2[29]])
    ratioS=(S1[points1[28]])/(S2[points2[28]])
    #ratioV=(V1[points1[28]])/(V2[points2[28]])

    print ("ratioH = {0}".format(ratioH))
    print ("ratioS = {0}".format(ratioS))
    print ("ratioV = {0}".format(ratioV))
    
    # Compute weighted average point coordinates
    for i in range(0, len(points1)):
  #      x = ( 1 - alpha ) * points1[i][0] + alpha * points2[i][0]
  #      y = ( 1 - alpha ) * points1[i][1] + alpha * points2[i][1]
         x = points1[i][0]
         y = points1[i][1]
         points.append((x,y))


    # Allocate space for final output
    imgMorph = np.zeros(img1.shape, dtype = img1.dtype)

    # Read triangles from tri.txt
    with open("tri.txt") as file :
        for line in file :
            x,y,z = line.split()
            
            x = int(x)
            y = int(y)
            z = int(z)
            
            t1 = [points1[x], points1[y], points1[z]]
            t2 = [points2[x], points2[y], points2[z]]
            t = [ points[x], points[y], points[z] ]

            # Morph one triangle at a time.
            morphTriangle(img1, img2, imgMorph, t1, t2, t, alpha,ratioH,ratioS,ratioV)


    # Display Result
    cv2.imshow("Morphed Face", np.uint8(img1))
    cv2.imwrite('Morphed Face.png', np.uint8(img1))
    cv2.waitKey(0)