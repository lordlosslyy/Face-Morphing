# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 17:12:16 2018

@author: user
"""
import cv2
import numpy as np
import random
import pdb 
import imutils
from tri_function import rect_contains
from tri_function import draw_point


def face_triangle(image_path,txt_path,morph_part,output_name):
    img = cv2.imread(image_path)
    img = cv2.resize(img,(500,500))
    size = img.shape
    rect = (0, 0, size[1], size[0])
    delaunay_color=(255, 255, 255)
    # Create an instance of Subdiv2D
    subdiv = cv2.Subdiv2D(rect)
    # Create an array of points.
    points = []
    # Read in the points from a text file
    with open(txt_path) as file :
        for line in file :
            x, y = line.split()
            points.append((int(x), int(y)))
    # Insert points into subdiv
#    for p in points :
#        subdiv.insert(p)
    leftbrown = points[17:22]
    rightbrown = points[22:27]
    #lefteyes = [points[1],points[17],points[27],points[28]]
    #righteyes = [points[15],points[26],points[27],points[28]]
    lefteye = points[36:42]
    righteye = points[42:48]
    mouth = points[48:68]
    face = points [0:68]
    #nose = [points[3],points[13],points[27],points[31],points[35]]+points[31:36]
    nose = points[27:36] + [points[39],points[42]]
    jaw = points[6:11]
    if morph_part == "mouth":
        subdiv.insert(mouth)   
    elif morph_part == "leftbrown":
        subdiv.insert(leftbrown)
    elif morph_part == "rightbrown":
        subdiv.insert(rightbrown)
    elif morph_part == "lefteye":
        subdiv.insert(lefteye)
    elif morph_part == "righteye":
        subdiv.insert(righteye)
    elif morph_part == "jaw":
        subdiv.insert(jaw)
    elif morph_part == "nose":
        subdiv.insert(nose)
    else:    
        subdiv.insert(face)
    triangleList = subdiv.getTriangleList()
    tri=[]
    with open("tri.txt","w") as file: 
        for t in triangleList :        
            pt1 = (t[0], t[1])
            pt2 = (t[2], t[3])
            pt3 = (t[4], t[5])
            
            if rect_contains(rect, pt1) and rect_contains(rect, pt2) and rect_contains(rect, pt3) :
                for i in range(len(points)):
                    if points[i]==pt1:
                        x=i
                for i in range(len(points)):
                    if points[i]==pt2:
                        y=i
                for i in range(len(points)):
                    if points[i]==pt3:
                        z=i
                tri.append((x,y,z))
                file.write("{0} {1} {2}\n".format(x,y,z))
                cv2.line(img, pt1, pt2, delaunay_color, 1, cv2.LINE_AA, 0)
                cv2.line(img, pt2, pt3, delaunay_color, 1, cv2.LINE_AA, 0)
                cv2.line(img, pt3, pt1, delaunay_color, 1, cv2.LINE_AA, 0)
                
#    draw_delaunay( img, subdiv, (255, 255, 255) );
    # Draw points
    for p in points :
        draw_point(img, p, (0,0,255))
        
    cv2.imwrite('{0}.png'.format(output_name),img)