# import the necessary packages
import numpy as np
from visualize_facial_landmarks import visualize_facial_landmarks
from shape_to_numpy_array import shape_to_numpy_array
import cv2
import argparse
import dlib
import imutils
from PIL import Image


def detect_68_features(shape_predictor,image_path,output_name):
    facial_features_cordinates = {}

    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(shape_predictor)

    # load the input image, resize it, and convert it to grayscale
    image = cv2.imread(image_path)
    image = cv2.resize(image, (500,500))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #image = imutils.resize(image, width=500)
    # image = Image.open(args["image"])
    # image = image.resize((256,256))
    # image.show()
    # image = np.array(image)

    print (image.shape)
    # detect faces in the grayscale image
    rects = detector(gray, 1)

    sort_order = {1:'Jaw', 2:'Right_Eyebrow', 3:'Left_Eyebrow', 4:'Nose' ,5:'Right_Eye',
                                            6:'Left_Eye', 7:'Mouth' }
    #sort_order = {1:'Jaw', 3:'Right_Eyebrow', 2:'Left_Eyebrow', 4:'Nose' ,6:'Right_Eye',
    #                                        5:'Left_Eye', 7:'Mouth' }
    # loop over the face detections
    with open("{0}".format(output_name), "w") as text_file:
        for (i, rect) in enumerate(rects):
            # determine the facial landmarks for the face region, then
            # convert the landmark (x, y)-coordinates to a NumPy array
            shape = predictor(gray, rect)
            shape = shape_to_numpy_array(shape)

            facial_features_cordinates, output = visualize_facial_landmarks(image, shape)
            #cv2.imshow("Image", output)
            count = 1
            for keys in sorted(sort_order):
                print (sort_order[keys])
                for values in facial_features_cordinates[sort_order[keys]]:

                    text_file.write("{0} {1}\n".format(values[0],values[1]))
                    
                    #print (values.shape)
                    #print (count)
                    #print (values)
                    #print ("\n")
                    count = count + 1 

        cv2.imwrite("{0}.jpg".format(output_name), output)
        cv2.waitKey(0)


